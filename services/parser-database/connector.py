"""conector.py - One stop connector for external
services/databases"""
import random
import logging

import constants

logging.basicConfig(level=logging.INFO)

articles_in_memory = {}
keywords_in_memory = {}


def get_documents_to_parse():
    # When database is integrated, this will go away
    document_list = []
    document_list.append(constants.mty_document)
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
                articles_that_match_keyword[str(article["id"])] = article["frequency"]
        matching_articles[keyword] = articles_that_match_keyword
    return matching_articles


def save_keywords_in_memory(keywords, article):
    """Saves the keywords from an article in memory

    Args:
        keywords (JSON): contains keywords
        article (Article): article object
    """
    for keyword in keywords:
        frequency = article["content"].count(keyword)
        if keyword not in keywords_in_memory:
            keywords_in_memory[keyword] = []
        keywords_in_memory[keyword].append({
            "number": article["number"],
            "id": article["id"],
            "frequency": frequency
        })


def store_article(article_dict):
    articles_in_memory[article_dict["id"]] = article_dict
    save_keywords_in_memory(get_keywords(article_dict["content"]), article_dict)
    logging.info('Article ' + article_dict["id"] + ' assigned keywords')
