from unittest import mock
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
        {"id": "5", "articleNumber": 5, "frequency": 3},
        {"id": "45", "articleNumber": 45, "frequency": 1},
        {"id": "99", "articleNumber": 99, "frequency": 7},
    ],
    "licencia": [
        {"id": "89", "articleNumber": 89, "frequency": 3},
        {"id": "45", "articleNumber": 45, "frequency": 3},
        {"id": "125", "articleNumber": 125, "frequency": 2},
    ],
}


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
    result_to_assert_3 = {"licencia": {"89": {"weight": 3},
                                       "45": {"weight": 3}, "125": {"weight": 2}}}
    keywords = ["licencia"]
    result = connector.get_articles_that_match_keywords(keywords)
    assert result == result_to_assert_3


@mock.patch("connector.keywords_in_memory", in_memory_value_mock)
def test_get_articles_that_match_keywords_non_empty_result_two_keywords():
    result_to_assert_4 = {
        "licencia": {"89": {"weight": 3}, "45": {"weight": 3}, "125": {"weight": 2}},
        "ciclista": {"5": {"weight": 3}, "45": {"weight": 1}, "99": {"weight": 7}},
    }
    keywords = ["licencia", "ciclista"]
    result = connector.get_articles_that_match_keywords(keywords)
    assert result == result_to_assert_4


def test_get_documents():
    assert connector.get_documents_to_parse() == [constants.mty_document]
