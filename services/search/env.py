import os


def get_db_endpoint():
    return os.getenv('DB_ENDPOINT')


def get_keyword_endpoint():
    return os.getenv('KEYWORDS_ENDPOINT')
