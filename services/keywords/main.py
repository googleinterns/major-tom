import utils

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
