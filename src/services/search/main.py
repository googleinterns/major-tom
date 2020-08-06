if __name__ == "main":
    __package__ = "src.services.search"

import sys
sys.path.append('../../')
import constants
from search.search_engine import SearchEngine

def search_service(request):
    """
    Parses http json request and returns list of articles and their
    scores depending on the input query
    Args:
        request: http POST body request as json
    Returns:
        list of articles with their respective scores
    """
    json = request.get_json()
    query = json["query"]
    #articles = requests.post(/get_articles_from_keywords)
    articles = constants.ARTICLES
    search = SearchEngine(articles, keywords_weight=2)
    return search.query(query)

