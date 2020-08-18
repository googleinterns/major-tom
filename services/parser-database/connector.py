"""conector.py - One stop connector for external
services/databases"""
# import requests  # pylint: disable=import-error
import random

articles_in_memory = {}
keywords_in_memory = {}


def get_documents_to_parse():
    # When database is integrated, this will go away
    mty_document = {
        "hash":
        "afafbfbdce8c40924edae00f6ce54f0c639ce42a2" +
        "c0fbbfa6ab82ea6925827c51",
        "jurisdiction":
        "Monterrey",
        "url":
        "http://www.guadalupe.gob.mx/wp-content/up" +
        "loads/2019/09/Nuevo-Reglamento-Homologado-1.pdf",
    }
    document_list = []
    document_list.append(mty_document)
    return document_list


def get_keywords(text):
    """Get keywords that relate to this article

    Args:
        text (sting): text to extract keywords from

    Returns:
        [list]: list of extracted keywords
    """
    splited_text = text.split()
    keywords = [
        splited_text[random.randint(0, len(splited_text) - 1)],
        splited_text[random.randint(0, len(splited_text) - 1)],
    ]
    return keywords


def get_article_by_number(art_num):
    if art_num in articles_in_memory:
        return articles_in_memory[art_num]
    return None


def get_articles_that_match_keywords(keywords_list):
    """Returns articles that match the the given keyword(s)

    Args:
        keywords_list (list): Keyword(s) to look for

    Returns:
        list: articles that match such keyword(s)
    """
    matching_articles = {}
    for keyword in keywords_list:
        articles_that_match_keyword = {}
        if keyword in keywords_in_memory:
            for article in keywords_in_memory[keyword]:
                articles_that_match_keyword[article["articleNumber"]] = article["frequency"]
        matching_articles[keyword] = articles_that_match_keyword
    return matching_articles


def save_keywords_in_memory(keywords, article):
    """Saves the keywords from an article in memory

    Args:
        keywords (JSON): contains keywords
        article (Article): article object
    """
    # split_article = article.text.split()
    for keyword in keywords:
        frequency = article.text.count(keyword)
        if keyword not in keywords_in_memory:
            keywords_in_memory[keyword] = []
        keywords_in_memory[keyword].append({
            "articleNumber": article.number,
            "frequency": frequency
        })
