import os


def get_keywords_endpoint():
    return os.getenv("KEYWORDS_SERVICE")
