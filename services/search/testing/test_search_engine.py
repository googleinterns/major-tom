import mock  # pylint: disable=import-error
import json
from search_engine import SearchEngine  # pylint: disable=import-error
import test_constants as constants
import env  # pylint: disable=import-error
import responses  # pylint: disable=import-error


@responses.activate
def test_same_weights_for_all():
    """
    Have the query only apply for article 1, and the weights be the same
    for keywords and synonyms (default args.)
    """
    result = {1: 3}

    responses.add(
            responses.POST, constants.MOCK_URL, json=constants.KEYWORDS_DB_MOCK_1, status=200)
    with mock.patch('env.get_db_endpoint', return_value=constants.MOCK_URL):
        assert result == SearchEngine().search_query(constants.KEYWORDS_ARTICLE_1,
                                                         constants.SYNONYMS_ARTICLE_1)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == constants.MOCK_URL
        assert responses.calls[0].response.text == json.dumps(constants.KEYWORDS_DB_MOCK_1)


@responses.activate
def test_double_weights_synonyms():
    """
    Have the query only apply for article 1, and double the synonym weights
    """
    result = {1: 4}

    responses.add(
            responses.POST, constants.MOCK_URL, json=constants.KEYWORDS_DB_MOCK_1, status=200)
    with mock.patch('env.get_db_endpoint', return_value=constants.MOCK_URL):
        assert result == SearchEngine(synonyms_weight=2).search_query(constants.KEYWORDS_ARTICLE_1,
                                                                          constants.SYNONYMS_ARTICLE_1)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == constants.MOCK_URL
        assert responses.calls[0].response.text == json.dumps(constants.KEYWORDS_DB_MOCK_1)


@responses.activate
def test_multiple_articles():
    """
    Have the query apply for two articles
    """
    result = {3: 2, 4: 2}

    responses.add(
            responses.POST, constants.MOCK_URL, json=constants.KEYWORDS_DB_MULTIPLE, status=200)
    with mock.patch('env.get_db_endpoint', return_value=constants.MOCK_URL):
        assert result == SearchEngine().search_query(constants.KEYWORDS_MULTIPLE,
                                                         constants.SYNONYMS_MULTIPLE)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == constants.MOCK_URL
        assert responses.calls[0].response.text == json.dumps(constants.KEYWORDS_DB_MULTIPLE)
