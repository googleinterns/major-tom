from requests_futures.sessions import FuturesSession  # pylint: disable=import-error
import constants


class SynonymExtractor:
    """
    Wrapper class for requests_futures methods
    """
    def __init__(self, max_synonyms):
        self.max_synonyms = max_synonyms
        self.session = FuturesSession()

    def create_conc_reqs(self, word_arr):
        """
        create an asynchronous request list using requests-futures
        Attributes:
            word_arr: A list of words which each is a different request
            session: A requests-futures session
        Return:
            A list of requests for every word
        """
        reqs = []
        for word in word_arr:
            reqs.append(self.session.get(constants.SPANISH_API_URL+word))  # pylint: disable=no-member

        return reqs

    def req_to_json(self, json):
        """
        Returns json from request
        """
        return json.result().json()


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

    synonym_extractor = SynonymExtractor(max_synonyms)

    for req in synonym_extractor.create_conc_reqs(word_arr):
        resp = synonym_extractor.req_to_json(req)
        logging.info(resp)

        if 'sinonimos' not in resp:
            raise Exception("Unexpected synonyms API response format")

        word_synonyms = resp['sinonimos']

        if len(word_synonyms) > max_synonyms:
            word_synonyms = word_synonyms[:max_synonyms]
        for synonym in word_synonyms:
            synonyms.append(synonym['sinonimo'])

    return synonyms
