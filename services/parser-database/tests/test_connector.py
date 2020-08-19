from unittest import mock
import connector
import constants


in_memory_value_mock = {
    "ciclista": [
            {
                "articleNumber": 5,
                "frequency": 3
            },
            {
                "articleNumber": 45,
                "frequency": 1
            },
            {
                "articleNumber": 99,
                "frequency": 7
            },
            ],
    "licencia": [
            {
                "articleNumber": 89,
                "frequency": 3
            },
            {
                "articleNumber": 45,
                "frequency": 3
            },
            {
                "articleNumber": 125,
                "frequency": 2
            },
            ],
}


@mock.patch('connector.keywords_in_memory', in_memory_value_mock)
def test_get_articles_that_match_keywords_empty_result_one_keyword():
    keywords = ["alcohol"]
    result = connector.get_articles_that_match_keywords(keywords)
    assert result["alcohol"] == {}


@mock.patch('connector.keywords_in_memory', in_memory_value_mock)
def test_get_articles_that_match_keywords_empty_result_two_keywords():
    keywords = ["vehiculo", "conductor"]
    result = connector.get_articles_that_match_keywords(keywords)
    assert result["vehiculo"] == {}
    assert result["conductor"] == {}


@mock.patch('connector.keywords_in_memory', in_memory_value_mock)
def test_get_articles_that_match_keywords_non_empty_result_one_keyword():
    keywords = ["licencia"]
    result = connector.get_articles_that_match_keywords(keywords)
    assert "licencia" in result


@mock.patch('connector.keywords_in_memory', in_memory_value_mock)
def test_get_articles_that_match_keywords_non_empty_result_two_keywords():
    keywords = ["licencia", "ciclista"]
    result = connector.get_articles_that_match_keywords(keywords)
    assert "licencia" in result
    assert "ciclista" in result


def test_get_documents():
    assert connector.get_documents_to_parse() == [constants.mty_document]

