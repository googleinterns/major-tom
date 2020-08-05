import constants
import utils
from search.search_engine import SearchEngine

def get_keywords_service(request):
    """
    Parses http json request and returns keywords and language of text
    Args:
        request: http POST body request as json
    Returns:
        json of language detected and keywords for text
    """
    json = request.get_json()
    text = json["text"]
    return utils.extract_keywords(text)

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
