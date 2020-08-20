import json
import mock  # pylint: disable=import-error
import flask
import responses  # pylint: disable=import-error
from search_engine import SearchEngine  # pylint: disable=import-error
import test_constants as constants
from main import search_service


def make_flask_request(data):
    """
    Makes post flask request from a dict
    Attributes:
        data: dictionary which gets converted to json
    return
        flask post request
    """
    return flask.Request.from_values(
        method='POST', content_type="application/json", data=json.dumps(data))


@responses.activate
def test_same_weights_for_all():
    """
    Have the query only apply for article 1, and the weights be the same
    for keywords and synonyms (default args.)
    """
    result = {1: 3}

    responses.add(
        responses.POST, constants.MOCK_URL_DB, json=constants.KEYWORDS_DB_MOCK_1, status=200)
    with mock.patch('env.get_db_endpoint', return_value=constants.MOCK_URL_DB):
        assert result == SearchEngine().search_query(constants.KEYWORDS_ARTICLE_1,
                                                     constants.SYNONYMS_ARTICLE_1)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == constants.MOCK_URL_DB
        assert responses.calls[0].response.text == json.dumps(constants.KEYWORDS_DB_MOCK_1)


@responses.activate
def test_double_weights_synonyms():
    """
    Have the query only apply for article 1, and double the synonym weights
    """
    result = {1: 4}

    responses.add(
        responses.POST, constants.MOCK_URL_DB, json=constants.KEYWORDS_DB_MOCK_1, status=200)
    with mock.patch('env.get_db_endpoint', return_value=constants.MOCK_URL_DB):
        assert result == SearchEngine(synonyms_weight=2).search_query(constants.KEYWORDS_ARTICLE_1,
                                                                      constants.SYNONYMS_ARTICLE_1)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == constants.MOCK_URL_DB
        assert responses.calls[0].response.text == json.dumps(constants.KEYWORDS_DB_MOCK_1)


@responses.activate
def test_multiple_articles():
    """
    Have the query apply for two articles
    """
    result = {3: 2, 4: 2}

    responses.add(
        responses.POST, constants.MOCK_URL_DB, json=constants.KEYWORDS_DB_MULTIPLE, status=200)
    with mock.patch('env.get_db_endpoint', return_value=constants.MOCK_URL_DB):
        assert result == SearchEngine().search_query(constants.KEYWORDS_MULTIPLE,
                                                     constants.SYNONYMS_MULTIPLE)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == constants.MOCK_URL_DB
        assert responses.calls[0].response.text == json.dumps(constants.KEYWORDS_DB_MULTIPLE)

@responses.activate
def test_full_workflow_search():
    """
    Only one word in input, but it is a keyword
    """
    result = {'articles': [1]}
    keyword_mock = {'lan': 'es',
                    'tokens': [{'lemma': word} for word in constants.KEYWORDS_ARTICLE_1]}

    responses.add(
        responses.POST, constants.MOCK_URL_DB, json=constants.KEYWORDS_DB_MOCK_1, status=200)
    responses.add(
        responses.POST, constants.MOCK_URL_KEYWORDS, json=keyword_mock, status=200)

    with mock.patch('env.get_db_endpoint', return_value=constants.MOCK_URL_DB):
        with mock.patch('env.get_keyword_endpoint', return_value=constants.MOCK_URL_KEYWORDS):
            with mock.patch('synonym_extractor.create_synonym_list_esp',
                            return_value=constants.SYNONYMS_ARTICLE_1):

                assert result == search_service(
                        make_flask_request({'query': 'es forzoso usar casco en bicicleta?'}))
                assert len(responses.calls) == 2
                assert responses.calls[1].request.url == constants.MOCK_URL_DB
                assert responses.calls[1].response.text == json.dumps(constants.KEYWORDS_DB_MOCK_1)
                assert responses.calls[0].request.url == constants.MOCK_URL_KEYWORDS
                assert responses.calls[0].response.text == json.dumps(keyword_mock)


@responses.activate
def test_full_workflow_search_multiple():
    """
    Only one word in input, but it is a keyword
    """
    result = {'articles': [3, 4]}
    keyword_mock = {'lan': 'es',
                    'tokens': [{'lemma': word} for word in constants.KEYWORDS_MULTIPLE]}

    responses.add(
        responses.POST,
        constants.MOCK_URL_DB, json=constants.KEYWORDS_DB_MULTIPLE, status=200)
    responses.add(
        responses.POST, constants.MOCK_URL_KEYWORDS, json=keyword_mock, status=200)

    with mock.patch('env.get_db_endpoint', return_value=constants.MOCK_URL_DB):
        with mock.patch('env.get_keyword_endpoint', return_value=constants.MOCK_URL_KEYWORDS):
            with mock.patch('synonym_extractor.create_synonym_list_esp',
                            return_value=constants.SYNONYMS_MULTIPLE):

                assert result == search_service(
                        make_flask_request({'query': 'es forzoso usar casco en bicicleta?'}))
                assert len(responses.calls) == 2
                assert responses.calls[1].request.url == constants.MOCK_URL_DB
                assert responses.calls[1].response.text == json.dumps(constants.KEYWORDS_DB_MULTIPLE)
                assert responses.calls[0].request.url == constants.MOCK_URL_KEYWORDS
                assert responses.calls[0].response.text == json.dumps(keyword_mock)
