import traceback
import extract


def get_keywords_service(request):
    """
    Parses http json request and returns keywords and language of text
    Args:
        request: http POST body request as json
    Returns:
        json of language detected and keywords for text
    """
    json = request.get_json()
    if json is None or "text" not in json:
        return {"error": {"message": "ValueError: Expected 'text' field in json body is missing"}}

    text = json["text"]
    try:
        response = extract.extract_keywords(text)
    except Exception as e:
        return {"error": {"message": getattr(e, 'message', str(e)),
                          "trace": traceback.format_exc()}}
    return response
