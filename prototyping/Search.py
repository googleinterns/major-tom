class Search:
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
    def __init__(self, keywords, synonyms, articles, keywords_weight=1, synonyms_weight=1):
        """
        Inits  the search class with all the attributes.
        The weights attributes are default arguments for ease of use
        """
        self.keywords = keywords
        self.synonyms = synonyms
        self.articles = articles
        self.keywords_weight = keywords_weight
        self.synonyms_weight = synonyms_weight

    def score_articles(self):
        """
        Counts the number of indices between article words, keywords, and synonyms
        implementing the different weights for the different type of weight values

        Returns:
            A map of the score for every article
        """

        return {}
