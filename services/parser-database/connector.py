"""conector.py - One stop connector for external
services/databases"""
import requests  # pylint: disable=import-error
import logging
import numpy as np  # pylint: disable=import-error
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import constants
import env

logging.basicConfig(level=logging.INFO)

class Keywords:
    """Class for storing articles.
    """
    def __init__(self, keyword):
        self.keyword = keyword
        self.articles_that_contain_keyword = {}

    def to_dict(self):
        article_dict = {
            "keyword": self.number,
            "contain": self.articles_that_contain_keyword,
        }
        return article_dict

    @staticmethod
    def from_dict(src):
        self.number = src["number"]
        self.id = src["id"]
        self.content = src["keyword"]
        self.wordCount = src["frequency"]

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'major-tom-285619',
})

db = firestore.client()

articles_in_memory = {}
keywords_in_memory = {}


def get_documents_to_parse_db():
    documents_ref = db.collection(u'documents')
    docs = documents_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    return docs


def get_documents_to_parse():
    # When database is integrated, this will go away
    document_list = []
    document_list.append(constants.mty_document)
    return document_list


def get_keywords(text):
    """Get keywords that relate to this article (from NLP service)
    Args:
        text (sting): text to extract keywords from
    Returns:
        [list]: list of extracted keywords
    """
    extracted_keywords = []
    request = {'text': text}
    nlp_output = requests.post(env.get_keywords_endpoint(), json=request)
    json_output = nlp_output.json()
    if 'error' in json_output:
        raise Exception(json_output['error']['message'])
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
                articles_that_match_keyword[str(article["id"])] = {"weight": article["frequency"]}
        matching_articles[keyword] = articles_that_match_keyword
    return matching_articles


def get_articles_by_tfidf_value(keywords_list):
    """
    Returns a value for every article based on a keyword
    for a keyword list, value is based on
    term frequency inverse document frequency (tfidf)
    Args:
        keywords_list (list): Keyword(s) to look for

    Returns:
        list: articles and value for such keyword(s)
    """
    matching_articles = {}
    for keyword in keywords_list:
        articles_that_match_keyword = {}
        if keyword in keywords_in_memory:
            for article in keywords_in_memory[keyword]:
                # tfidf computation
                word_count = articles_in_memory[str(article["number"])]["wordCount"]
                term_density_in_article = article["frequency"]/word_count
                document_frequency = len(articles_in_memory)/len(keywords_in_memory[keyword])
                inverse_doc_freq = np.log(document_frequency)
                weight = term_density_in_article * inverse_doc_freq

                articles_that_match_keyword[str(article["number"])] = {"weight": weight}
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


def store_article_in_db(article_dict):
    db.collection(u'articles').document(article_dict["id"]).set(article_dict)
    save_keywords_in_db(get_keywords(article_dict["content"]), article_dict)
    logging.info('Article ' + article_dict["id"] + ' assigned keywords')


def save_keywords_in_db(keywords, article):
    """Saves the keywords from an article in memory

    Args:
        keywords (JSON): contains keywords
        article (Article): article object
    """
    for keyword in keywords:
        frequency = article["content"].count(keyword)

        doc_ref = db.collection(u'keywords').where('keyword', '==', keyword)
        doc = doc_ref.get()
        
        if len(doc) != 0 and doc[0] is not None:
            from_db = doc[0].to_dict()
            print(from_db)
            from_db["matching_articles"][article["id"]] = frequency
            #print(from_db)
            db.collection(u'keywords').document(doc[0].id).set(from_db)
        else:
            to_send = {"keyword": keyword, "matching_articles": {article["id"]: frequency}}
            db.collection(u'keywords').add(to_send)


def get_articles_that_match_keywords_db(keywords_list):
    matching_articles = {}
    for keyword in keywords_list:
        articles_that_match_keyword = {}
        doc_ref = db.collection(u'keywords').where('keyword', '==', keyword)
        doc = doc_ref.get()
        if doc.exists():
            doc_dict = doc.to_dict()
            for article in doc_dict[keyword]:
                articles_that_match_keyword[str(article["id"])] = {"weight": article["frequency"]}
        matching_articles[keyword] = articles_that_match_keyword
    return matching_articles


def get_article_by_id_db(art_num):
    documents_ref = db.collection(u'articles').document(art_num)
    doc = documents_ref.get()
    if doc is not None:
        return doc.to_dict()
    else:
        return None