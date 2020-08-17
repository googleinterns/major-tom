import traceback  # pylint: disable=import-error
import logging
import constants
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
    logging.info(json)

    if "query" not in json:
        error = {"error": {"message": "ValueError: Expected 'query' field in json body is missing"}}
        logging.error(error['error']['message'])
        return error

    query = json["query"]
    search = SearchEngine(keywords_weight=constants.KEYWORDS_WEIGHT)
    try:
        score_per_article = search.query(query)
    except Exception as e:
        error = {"error": {"message": getattr(e, 'message', str(e)),
                          "trace": traceback.format_exc()}}
        logging.error(error['error'])
        return error

    # sorts dictionary by value in DESC order
    articles_sorted = [k for k, v in sorted(
        score_per_article.items(),
        key=lambda item: item[1], reverse=True)]

    response = {"articles": articles_sorted}

    logging.info(response)
    return response
