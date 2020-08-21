"""parser.py - Parses a PDF document to extract driving
regulation articles and store them in memory.
"""
import logging
import hashlib
import re

import slate  # pylint: disable=import-error

import connector
import retriever

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
        self.id = str(number)

    def to_dict(self):
        article_dict = {
            "articleNumber": self.number,
            "id": self.id,
            "text": self.text,
            "wordCount": len(self.text.split())
        }
        return article_dict


def identify_articles(pdf_text):
    """Identifies articles and returns a list of Article objects.

    Args:
        pdf_text (string): contains the PDF text where articles
        are to be identified.

    Returns:
        list: article objects
    """
    articles = []
    article_count = 1
    i = 2
    res = re.split(r'(ART[ÍI]CULO *\d+ *\.?-?)', pdf_text)
    while i < len(res):
        articles.append(Article(article_count, res[i].strip()))
        logging.info("Article #" + str(article_count) + " recognized!")
        article_count += 1
        i += 2
    return articles


def parse_all_documents():
    """Parses all documents that are specified on the DB"""
    document_list = connector.get_documents_to_parse()
    for document in document_list:
        file_name = document["jurisdiction"] + ".pdf"
        retriever.get_document(document["url"], file_name)
        logging.info('File downloaded')
        parse(document)


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
        sha_hash = hasher.hexdigest()
        if sha_hash == past_hash:
            return False
        return True


def parse(document_to_parse):
    """Parses all PDF documents that are in the DB"""
    file_name = document_to_parse["jurisdiction"] + '.pdf'
    if has_file_changed(document_to_parse["hash"], file_name):
        logging.info('File has changed')
        with open(file_name, "rb") as pdf_file:
            doc = slate.PDF(pdf_file)
            final_text = ""
            for page in doc:
                final_text += page
            articles = identify_articles(final_text)

            for article in articles:
                dictionary = article.to_dict()
                connector.store_article(dictionary)
