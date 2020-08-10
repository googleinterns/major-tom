"""Program that parses PDF documents and separates it by article for database storage.
"""
import logging
import hashlib
import datetime


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


# Acts as main
def parse():
    """Parses all PDF documents that are in the DB"""
    docs = database.get_regulation_documents()
    for doc in docs:
        document = doc.to_dict()
        retriever.get_document(document["url"])
        hasher = hashlib.sha256()
        with open("regs.pdf", "rb") as pdf_file:
            file_buffer = pdf_file.read()
            hasher.update(file_buffer)
            if hasher.hexdigest() != document["hash"]:
                doc = slate.PDF(pdf_file)
                final_text = ""
                for page in doc:
                    final_text.join(page)
                final_text = final_text.strip().lower().split()
                count_articles(final_text)
            else:
                print("Downloaded document is the same as the one currently stored")


parse()
