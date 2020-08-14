import os
import requests  # pylint: disable=import-error
import constants
import testing.test_constants
import utils


class SearchEngine:
    """
    This class implements the functions to score every article
    by the amount of incidences between keywords and synonyms to articles

    Attributes:
        keywords: A list of keywords
        synonyms: A list of synonyms for the keywords
        articles: A list of articles
        keywords_weight: The weight that a keyword has on the scorig algorithm
            Optional: default argument as 1
        synonyms_weight: The weight that a synonym has on the scoring algorithm
            Optional: default argument as 1
    """
    def __init__(self, keywords_weight=1, synonyms_weight=1):
        """
        Inits the search engine by loading all articles
        """
        self.keywords_weight = keywords_weight
        self.synonyms_weight = synonyms_weight

    def query(self, query):
        """
        Extracts keywords, from keywords endpoint,
        and synonyms, from local function,
        to call search query and calculate the score for articles
        Args:
            query: query string
        Returns:
            A map of the score of every article
        """
        query_text = {'text': query}
        keywords_endpoint = os.getenv('KEYWORDS_ENDPOINT') is not None or 'http://localhost:8081'
        response = requests.post(keywords_endpoint, json=query_text)
        response = response.json()

        if 'error' in response:
            raise Exception(response['error']['message'])

        lan = response['lan']

        if lan not in constants.SUPPORTED_LANGUAGES:
            raise ValueError(f'{lan} not supported')

        keywords = []

        for token in response['tokens']:
            keywords.append(token['lemma'])

        synonyms = utils.create_synonym_list_esp(keywords)

        return self.search_query(keywords, synonyms)

    def _calculate_score(self, frequency, weight, words, target_dict):
        """
        Helper function to update score for resulting array
        Attributes:
            frequency: db frequency result
            weight: the weight for the current call
            iwords: keywords in search engine
            target_dict: dictionary to update
        """
        for word in words:
            if word in frequency:
                for key, value in frequency[word].items():
                    score = target_dict.get(key, 0) + value * weight
                    if score != 0:
                        target_dict[key] = score

    def search_query(self, keywords, synonyms):
        """
        Counts the number of incidences between article words, keywords, and synonyms
        implementing the different weights for the different type of weight values

        Returns:
            A map of the score for every article
        """

        score_per_article = {}

        # keywords_json = {"keywords": keywords}
        # synonyms_json = {"keywords": synonyms}
        # article_keywords_frequency = requests.post(db_endpoint, json=keywords_json)
        # article_synonyms_frequency = requests.post(db_endpoint, json=synonyms_json)

        article_keywords_frequency = testing.test_constants.KEYWORDS_DB_MOCK_1
        article_synonyms_frequency = testing.test_constants.SYNONYMS_DB_MOCK_1

        self._calculate_score(article_keywords_frequency, self.keywords_weight,
                              keywords, score_per_article)
        self._calculate_score(article_synonyms_frequency, self.synonyms_weight,
                              synonyms, score_per_article)

        return score_per_article
