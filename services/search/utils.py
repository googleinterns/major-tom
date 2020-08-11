import requests  # pylint: disable=import-error
import constants


def create_synonym_list_esp(word_arr, max_synonyms=5):
    """
    Retrieves a synonym list given a word list
    Attributes:
        word_arr: The word list which we wish to find synonyms for
        max_synonyms: The maximum number of synonyms per word in word_arr
            optional: Default value 5
    Returns: a list of synonyms
    """
    synonyms = []
    for word in word_arr:
        try:
            payload = requests.get(constants.SPANISH_API_URL+word)
            payload.raise_for_status()
        except requests.exceptions.HTTPError as err:
            return {"error": {"type": "HTTPError", "status_code": err.response.status_code,
                "message": getattr(err, 'message', str(err))}}
        except requests.exceptions.RequestException as err:
            return {"error": {"type": "RequestException",
                "message": getattr(err, 'message', str(err))}}

        word_synonyms = payload.json()['sinonimos']
        if len(word_synonyms) > max_synonyms:
            word_synonyms = word_synonyms[:max_synonyms]
        for synonym in word_synonyms:
            synonyms.append(synonym['sinonimo'])

    return synonyms
