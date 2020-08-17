"""conector.py - One stop connector for external
services/databases"""

import json
import os
import requests

import keywordmock  # pylint: disable=import-error


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


# TODO Change to point to Javier's service
def get_keywords(text):
    """Get keywords that relate to this article (Javier's service)

    Args:
        text (sting): text to extract keywords from

    Returns:
        [list]: list of extracted keywords
    """

    extracted_keywords = []
    request = {'text': text}
    nlp_output = requests.post(os.getenv("KEYWORDS_SERVICE"), json=request)
    # nlp_output = keywordmock.get_keywords(text)
    json_output = nlp_output.json()
    for keyword in json_output["tokens"]:
        extracted_keywords.append(keyword["lemma"])
    return extracted_keywords


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
        frequency = article.count(keyword)
        if keyword not in keywords_in_memory:
            keywords_in_memory[keyword] = []
        keywords_in_memory[keyword].append({
            "articleNumber": article.number,
            "frequency": frequency
        })
