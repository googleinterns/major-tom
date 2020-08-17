"""conector.py - One stop connector for external 
services/databases"""

import json

import keywordmock


articles_in_memory = {}
keywords_in_memory = {}


# TODO Change to point to Javier's service
def get_keywords(text):
    """Get keywords that relate to this article (Javier's service)

    Args:
        text (sting): text to extract keywords from

    Returns:
        [list]: list of extracted keywords
    """

    """
    return requests.post(
        "localhost:8000", params={"text": text}
    ).json()
    """
    extracted_keywords = []
    nlp_output = keywordmock.get_keywords(text)
    json_output = json.loads(nlp_output)
    for keyword in json_output["keywords"]:
        extracted_keywords.append(keyword)
    return extracted_keywords


def get_article_by_number(art_num):
    if art_num in articles_in_memory:
        return articles_in_memory[art_num]
    return None


def get_articles_that_match_keywords(keywords_list):
    """Returns articles that match the the given keyword(s)

    Args:
        keywords_list (list): Keyword(s) to look for

    Returns:
        list: articles that match such keyword(s)
    """
    matching_articles = []
    for keyword in keywords_list:
        articles_that_match_keyword = []
        if keyword in keywords_in_memory:
            for article in keywords_in_memory[keyword]:
                articles_that_match_keyword.append(
                    {
                        article["articleNumber"]: article["frequency"]
                    }
                )
        matching_articles.append({keyword: articles_that_match_keyword})
    return matching_articles
