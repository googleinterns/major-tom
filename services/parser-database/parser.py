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

    @staticmethod
    def from_dict():
        pass

    def to_dict(self):
        pass

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


articles_in_memory = []
keywords_in_memory = {}


def get_article_by_number(art_num):
    for item in articles_in_memory:
        if art_num == str(item["articleNumber"]):
            return item
    return None


def get_articles_that_match_keywords(keywords_list):
    """Returns articles that match the the given keyword(s)

    Args:
        keywords_list (list): Keyword(s) to look for

    Returns:
        list: articles that match such keyword(s)
    """
    to_return = []
    for keyword in keywords_list:
        if keyword in keywords_in_memory:
            print(keyword)
            to_return.append(keywords_in_memory[keyword])
    return to_return


def count_articles(pdf_text):
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
    "afafbfbdce8c40924edae00f6ce54f0c639ce42a2c0fbbfa6ab82ea6925827c51",  # pylint: disable=line-too-long
    "jurisdiction":
    "Monterrey",
    "url":
    "http://www.guadalupe.gob.mx/wp-content/uploads/2019/09/Nuevo-Reglamento-Homologado-1.pdf",  # pylint: disable=line-too-long
}
document_list = []
document_list.append(mty_document)


def parse_all_documents():
    """Parses all documents that are specified on the DB
    (For obvious reasons, this won't work as is while the DB is not in use)
    (But will still parse the hardcoded document)"""
    for document in document_list:
        parse(document)


def has_file_changed(past_hash):
    """Sees if the file is different.

    Args:
        past_hash (string): hash to compare from

    Returns:
        [boolean]: [if the file has changed or not]
    """
    hasher = hashlib.sha256()
    with open("regs.pdf", "rb") as pdf_file:
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
        [JSON]: extracted keywords
    """
    """
    return requests.post(
        "localhost:8000", params={"text": text}
    ).json()
    """
    keywords_service_response = keywordmock.get_keywords(text)
    return json.loads(keywords_service_response)


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
    articles_in_memory.append(article_dict)
    save_keywords_in_memory(get_keywords(article.text), article)


def save_keywords_in_memory(keywords, article):
    """Saves the keywords from an article in memory

    Args:
        keywords (JSON): contains keywords
        article (Article): article object
    """
    split_article = article.text.split()
    for keyword in keywords["keywords"]:
        frequency = split_article.count(keyword)
        if keyword not in keywords:
            keywords_in_memory[keyword] = []
        keywords_in_memory[keyword].append({
            "articleNumber": article.number,
            "frequency": frequency
        })


# When the time comes to implement the DB, the commented stuff will allow
# that (with a few additions)
def parse(document_to_parse):
    """Parses all PDF documents that are in the DB"""
    retriever.get_document(document_to_parse["url"])
    print('File downloaded')
    if has_file_changed(document_to_parse["hash"]):
        print('File has changed')
        with open("regs.pdf", "rb") as pdf_file:
            doc = slate.PDF(pdf_file)
            final_text = ""
            for page in doc:
                final_text += page
            final_text = final_text.strip().lower().split()
            articles = count_articles(final_text)

            for article in articles:
                article_to_dictionary(article)
