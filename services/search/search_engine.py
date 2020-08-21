import logging
import requests  # pylint: disable=import-error
import constants
import synonym_extractor
import env


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

        logging.debug("keywords location: %s", env.get_keyword_endpoint())

        response = requests.post(env.get_keyword_endpoint(), json=query_text)
        response = response.json()
        logging.info("keywords response: %s", response)

        if 'error' in response:
            raise Exception(response['error']['message'])

        lan = response['lan']

        if lan not in constants.SUPPORTED_LANGUAGES:
            logging.warning("%s not supported", lan)

        keywords = []

        for token in response['tokens']:
            keywords.append(token['lemma'])

        logging.info("keywords: %s", keywords)

        synonyms = synonym_extractor.create_synonym_list_esp(keywords)

        logging.info("synonyms: %s", synonyms)

        return self.search_query(keywords, synonyms)

    def _calculate_individual(self, word, frequency, weight, target_dict):
        if word in frequency:
            for key, value in frequency[word].items():
                score = target_dict.get(int(key), 0) + value * weight
                if score != 0:
                    target_dict[int(key)] = score

    def _calculate_score(self, frequency, keywords, synonyms, target_dict):
        """
        Helper function to update score for resulting array
        Attributes:
            frequency: db frequency result
            weight: the weight for the current call
            iwords: keywords in search engine
            target_dict: dictionary to update
        """
        for word in keywords:
            self._calculate_individual(word, frequency, self.keywords_weight, target_dict)

        for word in synonyms:
            self._calculate_individual(word, frequency, self.synonyms_weight, target_dict)

    def search_query(self, keywords, synonyms):
        """
        Counts the number of incidences between article words, keywords, and synonyms
        implementing the different weights for the different type of weight values

        Returns:
            A map of the score for every article
        """

        score_per_article = {}

        keywords_json = {"keywords": keywords+synonyms}
        article_keywords_frequency = requests.post(env.get_db_endpoint(), json=keywords_json).json()

        logging.info("DB Endpoint response: %s", article_keywords_frequency)

        if 'error' in article_keywords_frequency:
            raise Exception(article_keywords_frequency['error']['message'])

        self._calculate_score(article_keywords_frequency, keywords, synonyms, score_per_article)

        return score_per_article
