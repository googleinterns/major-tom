import logging
import hashlib

# import datetime
# import requests
import json

import slate  # pylint: disable=import-error

import retriever  # pylint: disable=import-error
# import database  # pylint: disable=import-error
import keywordmock  # pylint: disable=import-error

logging.basicConfig(level=logging.INFO)


class Document:
    """Class for Regulations Documents"""
    def __init__(self, jurisdiction, shahash, url, last_updated):
        self.id = None
        self.jurisdiction = jurisdiction
        self.shahash = shahash
        self.url = url
        self.last_updated = last_updated

    def __repr__(self):
        return f"Document(\
                id={self.id}, \
                jurisdiction={self.jurisdiction}, \
                last_updated={self.last_updated}, \
                url={self.url}, \
                shahash={self.shahash}\
            )"


class Article:
    """Class for storing articles.
    """
    def __init__(self, number, text):
        self.number = number
        self.text = text


articles_in_memory = {}
keywords_in_memory = {}


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
    matching_articles = []
    for keyword in keywords_list:
        articles_that_match_keyword = []
        if keyword in keywords_in_memory:
            for article in keywords_in_memory[keyword]:
                articles_that_match_keyword.append({article["articleNumber"]: article["frequency"]})
                print('ama')
        print(articles_that_match_keyword)
        matching_articles.append({keyword: articles_that_match_keyword})
        print('ma')
        print(matching_articles)
    return matching_articles


def identify_articles(pdf_text):
    """Identifies articles and returns a list of Article objects.

    Args:
        pdf_text (string): contains the PDF text where articles
        are to be identified.

    Returns:
        list: article objects
    """
    articles = []
    article_text = ""
    article_count = 1
    i = 0
    while i < len(pdf_text) - 1:
        if (pdf_text[i] == "artículo" or pdf_text[i] == "articulo") and (
                pdf_text[i + 1] == str(article_count) + ".-"
                or pdf_text[i + 1] == str(article_count) + "-"
                or pdf_text[i + 1] == str(article_count) + "."):
            logging.info("Article #" + str(article_count) + " recognized!")
            articles.append(Article(article_count, article_text))
            article_text = ""
            article_count += 1
            i += 1
        else:
            article_text += " " + pdf_text[i]
        i += 1
    return articles


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


def parse_all_documents():
    """Parses all documents that are specified on the DB
    (For obvious reasons, this won't work as is while the DB is not in use)
    (But will still parse the hardcoded document)"""
    for document in document_list:
        file_name = document["jurisdiction"] + ".pdf"
        download_file(document["url"], file_name)
        logging.info('File downloaded')
        parse(document, file_name)


def has_file_changed(past_hash, file_name):
    """Sees if the file is different.

    Args:
        past_hash (string): hash to compare from

    Returns:
        [boolean]: [if the file has changed or not]
    """
    hasher = hashlib.sha256()
    with open(file_name, "rb") as pdf_file:
        file_buffer = pdf_file.read()
        hasher.update(file_buffer)
        if hasher.hexdigest() == past_hash:
            return False
        return True


# TODO Change to point to Javier's service
def get_keywords(text):
    """Get keywords that relate to this article (Javier's service)

    Args:
        text (sting): text to extract keywords from

    Returns:
        [list]: list of extracted keywords
    """
    """
    return requests.post(
        "localhost:8000", params={"text": text}
    ).json()
    """
    extracted_keywords = []
    nlp_output = keywordmock.get_keywords(text)
    json_output = json.loads(nlp_output)
    for keyword in json_output["keywords"]:
        extracted_keywords.append(keyword)
    return extracted_keywords


def article_to_dictionary(article):
    """Converts an parsed article to a dictionary and saves it

    Args:
        article (Article): [article object]
    """
    article_dict = {
        "articleNumber": article.number,
        "text": article.text,
        "wordCount": len(article.text.split())
    }
    articles_in_memory[str(article.number)] = article_dict
    keywords = get_keywords(article.text)
    save_keywords_in_memory(keywords, article)


def save_keywords_in_memory(keywords, article):
    """Saves the keywords from an article in memory

    Args:
        keywords (JSON): contains keywords
        article (Article): article object
    """
    split_article = article.text.split()
    for keyword in keywords:
        frequency = split_article.count(keyword)
        if keyword not in keywords_in_memory:
            keywords_in_memory[keyword] = []
        keywords_in_memory[keyword].append({
            "articleNumber": article.number,
            "frequency": frequency
        })


def download_file(url, filename_to_use):
    """Downloads file from the given URL

    Args:
        url (string): [URL that contains the file to download]
        file_name_to_use (string): [file name for file to save]
    """
    retriever.get_document(url, filename_to_use)


def parse(document_to_parse, file_name):
    """Parses all PDF documents that are in the DB"""

    if has_file_changed(document_to_parse["hash"], file_name):
        logging.info('File has changed')
        with open(file_name, "rb") as pdf_file:
            doc = slate.PDF(pdf_file)
            final_text = ""
            for page in doc:
                final_text += page
            final_text = final_text.strip().lower().split()
            articles = identify_articles(final_text)

            for article in articles:
                article_to_dictionary(article)
