import testing.test_constants as constants
from search_engine import SearchEngine

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
    score_per_article = search.query(query)
    
    if 'error' in score_per_article:
        return score_per_article
    
    articles_sorted = [k for k,v in sorted(score_per_article.items(),
        key=lambda item: item[1], reverse=True)] # sorts dictionary by value in DESC order
    return {"articles":articles_sorted}
