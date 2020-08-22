from unittest import mock
import pytest  # pylint: disable=import-error
import connector
import constants


many_documents = [
    {
        "hash": "afafbfbdcfsefsesedae00f6ce54f0c639ce42a2" "c0fbbfa6ab82ea6925827c51",
        "jurisdiction": "Saltillo",
        "url": "http://www.guadalupe.gob.mx/wp-content/up"
        "loads/2019/09/Nuevo-Reglamento-Homologado-1.pdf",
    },
    {
        "hash": "afafbfbdce8c40924edae00f6ce54f0c639ce42a2" "c0fbbfa6ab82ea6925827c51",
        "jurisdiction": "Monterrey",
        "url": "http://www.guadalupe.gob.mx/wp-content/up"
        "loads/2019/09/Nuevo-Reglamento-Homologado-1.pdf",
    },
]


in_memory_value_mock = {
    "ciclista": [
        {"id": 5, "frequency": 3},
        {"id": 45, "frequency": 1},
        {"id": 99, "frequency": 7},
    ],
    "licencia": [
        {"id": 89, "frequency": 3},
        {"id": 45, "frequency": 3},
        {"id": 125, "frequency": 2},
    ],
}


in_memory_value_mock_no_decimals = {
    "ciclista": [
        {"number": 5, "frequency": 3},
        {"number": 45, "frequency": 6},
        {"number": 99, "frequency": 9},
    ],
    "licencia": [
        {"number": 89, "frequency": 3},
        {"number": 45, "frequency": 3},
        {"number": 125, "frequency": 15},
    ],
}


articles_in_memory = {'5': {'wordCount': 32}, '45': {'wordCount': 40}, '89': {'wordCount': 16},
                      '99': {'wordCount': 50}, '125': {'wordCount': 200}}


articles_in_memory_no_wordCount = {'5': {}, '45': {}, '89': {}, '99': {}, '125': {}}


def logn(num):
    """
    Mocks the natural log of a number to try to
    minimize decimal points
    """
    return num


@mock.patch("connector.keywords_in_memory", in_memory_value_mock)
def test_get_articles_that_match_keywords_empty_result_one_keyword():
    result_to_assert_1 = {"alcohol": {}}
    keywords = ["alcohol"]
    result = connector.get_articles_that_match_keywords(keywords)
    assert result == result_to_assert_1


@mock.patch("connector.keywords_in_memory", in_memory_value_mock)
def test_get_articles_that_match_keywords_empty_result_two_keywords():
    result_to_assert_2 = {"vehiculo": {}, "conductor": {}}
    keywords = ["vehiculo", "conductor"]
    result = connector.get_articles_that_match_keywords(keywords)
    assert result == result_to_assert_2


@mock.patch("connector.keywords_in_memory", in_memory_value_mock)
def test_get_articles_that_match_keywords_non_empty_result_one_keyword():
    result_to_assert_3 = {"licencia": {"89": 3, "45": 3, "125": 2}}
    keywords = ["licencia"]
    result = connector.get_articles_that_match_keywords(keywords)
    assert result == result_to_assert_3


@mock.patch("connector.keywords_in_memory", in_memory_value_mock_no_decimals)
@mock.patch("connector.articles_in_memory", articles_in_memory)
def test_get_articles_by_tfidf_value():
    expected = {
        "licencia": {"89": {"weight": .3125}, "45": {"weight": .125}, "125": {"weight": .125}},
        "ciclista": {"5": {"weight": .15625}, "45": {"weight": .25}, "99": {"weight": .3}},
    }
    keywords = ["licencia", "ciclista"]
    with mock.patch("numpy.log", side_effect=logn):
        assert expected == connector.get_articles_by_tfidf_value(keywords)


@mock.patch("connector.keywords_in_memory", in_memory_value_mock_no_decimals)
@mock.patch("connector.articles_in_memory", articles_in_memory)
def test_get_articles_by_tfidf_value_empty_result():
    expected = {
        "casco": {},
        "luz": {},
    }
    keywords = ["casco", "luz"]
    with mock.patch("numpy.log", side_effect=logn):
        assert expected == connector.get_articles_by_tfidf_value(keywords)


@mock.patch("connector.keywords_in_memory", in_memory_value_mock_no_decimals)
@mock.patch("connector.articles_in_memory", articles_in_memory_no_wordCount)
def test_get_articles_by_tfidf_value_missing_word_count():
    keywords = ["licencia", "ciclista"]
    with mock.patch("numpy.log", side_effect=logn):
        with pytest.raises(KeyError):
            connector.get_articles_by_tfidf_value(keywords)


def test_get_documents():
    assert connector.get_documents_to_parse() == [constants.mty_document]
