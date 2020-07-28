from MockArticle import Article

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
    def __init__(self, articles):
        """
        Inits the search engine by loading all articles
        """
        self.articles = articles

    def query(self, keywords, synonyms, keywords_weight=1, synonyms_weight=1):
        """
        Loads all necessary data from the query.
        The weights attributes are default arguments for ease of use
        """
        self.keywords = keywords
        self.synonyms = synonyms
        self.keywords_weight = keywords_weight
        self.synonyms_weight = synonyms_weight

    def score_articles(self):
        """
        Counts the number of incidences between article words, keywords, and synonyms
        implementing the different weights for the different type of weight values

        Returns:
            A map of the score for every article
        """

        score_per_article = {}
        for article in self.articles:
            score = 0
            article_frequency = article.keywords
            for keyword in self.keywords:
                score += article_frequency.get(keyword, 0) * self.keywords_weight

            for synonym in self.synonyms:
                score += article_frequency.get(synonym, 0) * self.synonyms_weight

            if score != 0:
                score_per_article[article.id] = score
        
        return score_per_article
