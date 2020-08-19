import mock  # pylint: disable=import-error
from search_engine import SearchEngine  # pylint: disable=import-error
import test_constants as constants
import env  # pylint: disable=import-error


def test_same_weights_for_all():
    """
    Have the query only apply for article 1, and the weights be the same
    for keywords and synonyms (default args.)
    """
    result = {1: 3}

    with mock.patch('requests.post', return_value=constants.KEYWORDS_DB_MOCK_1) as mocked:
        with mock.patch('env.get_db_endpoint', return_value="http://somerealurl.com"):
            assert result == SearchEngine().search_query(constants.KEYWORDS_ARTICLE_1,
                                                         constants.SYNONYMS_ARTICLE_1)
            mocked.assert_called_once_with(
                env.get_db_endpoint(),
                json={"keywords": constants.KEYWORDS_ARTICLE_1 + constants.SYNONYMS_ARTICLE_1})


def test_double_weights_synonyms():
    """
    Have the query only apply for article 1, and double the synonym weights
    """
    result = {1: 4}

    with mock.patch('requests.post', return_value=constants.KEYWORDS_DB_MOCK_1) as mocked:
        with mock.patch('env.get_db_endpoint', return_value="http://somerealurl.com"):
            assert result == SearchEngine(synonyms_weight=2).search_query(constants.KEYWORDS_ARTICLE_1,
                                                                          constants.SYNONYMS_ARTICLE_1)
            mocked.assert_called_once_with(
                env.get_db_endpoint(),
                json={"keywords": constants.KEYWORDS_ARTICLE_1 + constants.SYNONYMS_ARTICLE_1})


def test_multiple_articles():
    """
    Have the query apply for two articles
    """
    result = {3: 2, 4: 2}

    with mock.patch('requests.post', return_value=constants.KEYWORDS_DB_MULTIPLE) as mocked:
        with mock.patch('env.get_db_endpoint', return_value="http://somerealurl.com"):
            assert result == SearchEngine().search_query(constants.KEYWORDS_MULTIPLE,
                                                         constants.SYNONYMS_MULTIPLE)
            mocked.assert_called_once_with(
                env.get_db_endpoint(),
                json={"keywords": constants.KEYWORDS_MULTIPLE + constants.SYNONYMS_MULTIPLE})
