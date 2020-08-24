from unittest import mock
import pytest  # pylint: disable=import-error
import connector
import env
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
        {"id": "5", "number": 5, "frequency": 3},
        {"id": "45", "number": 45, "frequency": 1},
        {"id": "99", "number": 99, "frequency": 7},
    ],
    "licencia": [
        {"id": "89", "number": 89, "frequency": 3},
        {"id": "45", "number": 45, "frequency": 3},
        {"id": "125", "number": 125, "frequency": 2},
    ],
}


keywords_mock = ["forzoso", "bicicleta", "usar", "casco"]


article_mock = {"id": 1, "number": 1, "content": "en bicicleta es siempre forzoso usar casco"}


expected_in_memory = {"forzoso": [{"id": 1, "number": 1, "frequency": 1}],
                      "bicicleta": [{"id": 1, "number": 1, "frequency": 1}],
                      "usar": [{"id": 1, "number": 1, "frequency": 1}],
                      "casco": [{"id": 1, "frequency": 1, "number": 1}]}


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


@mock.patch("requests.post")
def test_get_keywords_from_nlp(mock_get):
    with mock.patch('env.get_keywords_endpoint', return_value="http://example.org"):
        text_to_keywordize = 'es forzoso en bicicleta usar casco?'
        output_to_assert_nlp_keywords = ['ser', 'forzoso', 'bicicleta', 'usar', 'casco']
        mock_get.return_value.json.return_value = {"lan": "es", "tokens": [{"lemma": "ser", "part_of_speech": "VERB", "word": "es"}, {"lemma": "forzoso", "part_of_speech": "ADJ", "word": "forzoso"}, {"lemma": "bicicleta", "part_of_speech": "NOUN", "word": "bicicleta"}, {"lemma": "usar", "part_of_speech": "VERB", "word": "usar"}, {"lemma": "casco", "part_of_speech": "NOUN", "word": "casco"}]}  # noqa: E501
        result = connector.get_keywords(text_to_keywordize)
        mock_get.assert_called_once_with(env.get_keywords_endpoint(), json={"text": text_to_keywordize})
        assert result == output_to_assert_nlp_keywords


@mock.patch("requests.post")
def test_if_got_error_from_keywords_service(mock_get):
    text_to_keywordize = 'es forzoso en bicicleta usar casco?'
    mock_get.return_value.json.return_value = {'error': {'message': "something happened"}}  # noqa: E501
    with pytest.raises(Exception):
        assert connector.get_keywords(text_to_keywordize)


def test_no_errors_set_keywords_in_memory():
    try:
        connector.save_keywords_in_memory(keywords_mock, article_mock)
        assert expected_in_memory == connector.keywords_in_memory
    except Exception as e:
        pytest.fail("Error: " + str(e))
