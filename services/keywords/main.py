import traceback
import logging
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
    logging.info("Endpoint request:", json)

    if json is None or "text" not in json:
        error = {"error": {"message": "ValueError: Expected 'text' field in json body is missing"}}
        logging.error(error['error']['message'])
        return error

    text = json["text"]
    try:
        response = extract.extract_keywords(text)
    except Exception as e:
        error = {"error": {"message": getattr(e, 'message', str(e)),
                          "trace": traceback.format_exc()}}
        logging.error(error['error'])
        return error

    logging.info("Endpoint response:", response)
    return response
