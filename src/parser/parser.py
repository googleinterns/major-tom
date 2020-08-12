"""Program that parses PDF documents and separates it by article for database storage.
"""
import logging
import hashlib
import datetime
import requests
from collections import namedtuple


import slate


import retriever
import database


logging.basicConfig(level=logging.INFO)


class Document:
    """Class for Regulations Documents"""

    def __init__(self, jurisdiction, hash, url):
        self.id = None
        self.jurisdiction = jurisdiction
        self.hash = hash
        self.url = url

    @staticmethod
    def from_dict():
        pass

    def to_dict(self):
        pass

    def __repr__(self):
        return f"Document(\
                id={self.id}, \
                jurisdiction={self.jurisdiction}, \
                lastUpdated={self.lastUpdated}, \
                url={self.url}, \
                hash={self.hash}\
            )"


class Article:
    """Class for storing articles.
    """

    def __init__(self, number, text):
        self.number = number
        self.text = text


class Keyword:
    """Class for storing keywords.
    """

    def __init__(self, number, text):
        self.number = number
        self.text = text


articles_in_memory = []


def get_article_by_number(artNum):
    for item in articles_in_memory:
        if artNum == str(item["articleNumber"]):
            return item
    return "No article matches such ID", 402


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
            or pdf_text[i + 1] == str(article_count) + "."
        ):
            logging.info("Article #" + str(article_count) + " recognized!")
            articles.append(Article(article_count, article_text))
            article_text = ""
            article_count += 1
            i += 1
        else:
            article_text += " " + pdf_text[i]
        i += 1
    for article in articles:
        print("Article: " + str(article.number - 1) + " Text: " + article.text)
    return articles


keywords = {}
documents = {
    'hash': 'afafbfbdce8c40924edae00f6ce54f0c639ce42a2c0fbbfa6ab82ea6925827c51',  # Added one at last
    'jurisdiction': 'Monterrey',
    'url': 'http://www.guadalupe.gob.mx/wp-content/uploads/2019/09/Nuevo-Reglamento-Homologado-1.pdf'
 }
document_list = []
document_list.append(documents)


def parse():
    """Parses all PDF documents that are in the DB"""
    # docs = database.get_regulation_documents()  # DB Component
    for document_to_parse in document_list:
        # document = doc.to_dict()  # used when using DB Comp
        retriever.get_document(document_to_parse["url"])  # Change to document when using DB

        # Check if the file is different, this has to be done in a different open file instance
        # if not, Python returns some weird errors
        hasher = hashlib.sha256()
        with open("regs.pdf", "rb") as pdf_file:
            file_buffer = pdf_file.read()
            hasher.update(file_buffer)
            if hasher.hexdigest() == document_to_parse["hash"]:
                print("Downloaded document is the same as the one currently stored")
                return 'Succesful Operation - File did not change', 200

        with open("regs.pdf", "rb") as pdf_file:
            doc = slate.PDF(pdf_file)
            final_text = ""
            for page in doc:
                final_text += page
            final_text = final_text.strip().lower().split()
            articles = count_articles(final_text)
            for article in articles:
                articleDict = {}
                articleDict['articleNumber'] = article.number
                articleDict['text'] = article.text
                articleDict['wordCount'] = len(article.text.split())
                articles_in_memory.append(articleDict)
                print('Adding ' + str(articleDict))
                # Get keywords that relate to this article (Javier's service)
                '''
                    keywords_service_response = requests.get(
                    "localhost:8000", params={"text": article.text}
                    ).json()
                '''
                split_article = article.text.split()
                '''
                for keyword in keywords_service_response["keywords"]:
                    frequency = split_article.count(keyword)
                    keywords[keyword] = namedtuple(article.number, frequency)
                    '''
    return 'Successful Operation', 200
