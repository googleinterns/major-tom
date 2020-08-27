from unittest import mock
import json
import pytest  # pylint: disable=import-error
import requests  # pylint: disable=import-error
import flask  # pylint: disable=import-error
import responses  # pylint: disable=import-error
from search_engine import SearchEngine  # pylint: disable=import-error
import test_constants as constants
from main import search_service  # pylint: disable=no-name-in-module
import synonym_extractor  # pylint: disable=import-error


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


class MockJson:
    def __init__(self, json_test_value):
        self.json_test_value = json_test_value

    def json(self):
        return self.json_test_value

    def raise_for_status(self):
        pass


class MockJsonHTTPError:
    def __init__(self, json_test_value):
        self.json_test_value = json_test_value

    def json(self):
        return self.json_test_value

    def raise_for_status(self):
        raise requests.exceptions.HTTPError("some status code not 200")


class MockResult:
    def __init__(self, json_test_value):
        self.mock_json = MockJson(json_test_value)

    def result(self):
        return self.mock_json


class MockResultHTPPError:
    def __init__(self, json_test_value):
        self.mock_json = MockJsonHTTPError(json_test_value)

    def result(self):
        return self.mock_json


def json_mock():
    return {"sinonimos": [{"sinonimo": "my_synonym"}] * constants.TEN_SYNONYMS}


def test_synonym_http_error():
    """
    Tests one synonym call with an http error
    """
    req_list = MockResultHTPPError(json_mock())
    with mock.patch('requests_futures.sessions.FuturesSession.get', return_value=req_list):
        with pytest.raises(requests.HTTPError):
            synonym_extractor.create_synonym_list_esp(["word"])


def test_one_synonym():
    """
    Tests one synonym call with default max synonyms (5)
    """
    expected = ["my_synonym"] * constants.DEFAULT_MAX_SYNONYMS
    req_list = MockResult(json_mock())
    with mock.patch('requests_futures.sessions.FuturesSession.get', return_value=req_list):

        assert expected == synonym_extractor.create_synonym_list_esp(["word"])


def test_no_synonyms():
    """
    Tests no synonym calls
    """
    expected = []

    req_list = MockResult(json_mock())
    with mock.patch('requests_futures.sessions.FuturesSession.get', return_value=req_list):

        assert expected == synonym_extractor.create_synonym_list_esp([])


def test_multiple_synonyms():
    """
    Tests two synonym call with default max synonyms (5)
    """
    expected = ["my_synonym", "my_synonym"] * constants.DEFAULT_MAX_SYNONYMS

    req_list = MockResult(json_mock())
    with mock.patch('requests_futures.sessions.FuturesSession.get', return_value=req_list):

        assert expected == synonym_extractor.create_synonym_list_esp(["word1", "word2"])


def test_increased_max_synonyms():
    """
    Tests one synonym call with increased max synonyms (8)
    """
    expected = ["my_synonym"] * constants.INCREASED_MAX_SYNONYMS

    req_list = MockResult(json_mock())
    with mock.patch('requests_futures.sessions.FuturesSession.get', return_value=req_list):

        assert expected == synonym_extractor.create_synonym_list_esp(
            ["word1"], max_synonyms=constants.INCREASED_MAX_SYNONYMS)


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

    responses.add(
        responses.POST, constants.MOCK_URL_DB, json=constants.KEYWORDS_DB_MOCK_1, status=200)
    responses.add(
        responses.POST, constants.MOCK_URL_KEYWORDS,
        json=constants.KEYWORD_ENDPOINT_MOCK, status=200)

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
                assert responses.calls[0].response.text == json.dumps(
                    constants.KEYWORD_ENDPOINT_MOCK)


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
                assert responses.calls[1].response.text == json.dumps(
                    constants.KEYWORDS_DB_MULTIPLE)
                assert responses.calls[0].request.url == constants.MOCK_URL_KEYWORDS
                assert responses.calls[0].response.text == json.dumps(keyword_mock)


@responses.activate
def test_http_error_calling_db():
    """
    Tests re raising of status code 400 when calling db endpoint
    """
    responses.add(responses.POST, constants.MOCK_URL_DB, status=400)

    with mock.patch('env.get_db_endpoint', return_value=constants.MOCK_URL_DB):

        with pytest.raises(requests.HTTPError):
            SearchEngine().search_query(constants.KEYWORDS_ARTICLE_1,
                                        constants.SYNONYMS_ARTICLE_1)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == constants.MOCK_URL_DB
    assert responses.calls[0].response.status_code == 400


@responses.activate
def test_http_error_calling_keyword():
    """
    Tests re raising of status code 400 when calling keywords endpoint
    """
    responses.add(responses.POST, constants.MOCK_URL_KEYWORDS, status=400)

    with mock.patch('env.get_keyword_endpoint', return_value=constants.MOCK_URL_KEYWORDS):
        with pytest.raises(requests.HTTPError):
            SearchEngine().query("Some super real query")
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == constants.MOCK_URL_KEYWORDS
    assert responses.calls[0].response.status_code == 400
