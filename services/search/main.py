import traceback  # pylint: disable=import-error
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
    if "query" not in json:
        return {"error": {"message": "ValueError: Expected 'query' field in json body is missing"}}

    query = json["query"]
    search = SearchEngine(keywords_weight=2)
    try:
        score_per_article = search.query(query)
    except Exception as e:
        return {"error": {"message": getattr(e, 'message', str(e)),
                          "trace": traceback.format_exc()}}

    # sorts dictionary by value in DESC order
    articles_sorted = [k for k, v in sorted(
        score_per_article.items(),
        key=lambda item: item[1], reverse=True)]

    return {"articles": articles_sorted}
