from unittest import mock
from search_engine import SearchEngine  # pylint: disable=import-error
import test_constants as constants
import utils  # pylint: disable=import-error


def reqs_list(arr):
    """
    Returns a list of same length as arr
    """
    return [""] * len(arr)


def to_json(req):
    """
    Returns the mocked json response with ten synonyms returned
    """
    return {"sinonimos": [{"sinonimo": "my_synonym"}] * constants.TEN_SYNONYMS}


def test_one_synonym():
    """
    Tests one synonym call with default max synonyms (5)
    """
    result = ["my_synonym"] * constants.DEFAULT_MAX_SYNONYMS

    with mock.patch('utils.SynonymExtractor.create_conc_reqs', side_effect=reqs_list):
        with mock.patch('utils.SynonymExtractor.req_to_json', side_effect=to_json):

            assert result == utils.create_synonym_list_esp(["word"])


def test_no_synonyms():
    """
    Tests no synonym calls
    """
    result = []

    with mock.patch('utils.SynonymExtractor.create_conc_reqs', side_effect=reqs_list):
        with mock.patch('utils.SynonymExtractor.req_to_json', side_effect=to_json):

            assert result == utils.create_synonym_list_esp([])


def test_multiple_synonyms():
    """
    Tests two synonym call with default max synonyms (5)
    """
    result = ["my_synonym", "my_synonym"] * constants.DEFAULT_MAX_SYNONYMS

    with mock.patch('utils.SynonymExtractor.create_conc_reqs', side_effect=reqs_list):
        with mock.patch('utils.SynonymExtractor.req_to_json', side_effect=to_json):

            assert result == utils.create_synonym_list_esp(["word1", "word2"])


def test_increased_max_synonyms():
    """
    Tests one synonym call with increased max synonyms (8)
    """
    result = ["my_synonym"] * constants.INCREASED_MAX_SYNONYMS

    with mock.patch('utils.SynonymExtractor.create_conc_reqs', side_effect=reqs_list):
        with mock.patch('utils.SynonymExtractor.req_to_json', side_effect=to_json):

            assert result == utils.create_synonym_list_esp([
                "word1"], max_synonyms=constants.INCREASED_MAX_SYNONYMS)


def test_same_weights_for_all():
    """
    Have the query only apply for article 1, and the weights be the same
    for keywords and synonyms (default args.)
    """
    result = {1: 3}

    assert result == SearchEngine().search_query(constants.KEYWORDS_ARTICLE_1,
                                                 constants.SYNONYMS_ARTICLE_1)


def test_double_weights_synonyms():
    """
    Have the query only apply for article 1, and double the synonym weights
    """
    result = {1: 4}

    assert result == SearchEngine(synonyms_weight=2).search_query(constants.KEYWORDS_ARTICLE_1,
                                                                  constants.SYNONYMS_ARTICLE_1)

# I mocked the db endpoint to only be for article 1
# therefore this test is not yet available without the endpoint
#
# def test_multiple_articles():
#    """
#    Have the query apply for two articles
#    """
#    result = {3: 2, 4: 2}
#    assert result == SearchEngine(constants.ARTICLES).search_query(constants.KEYWORDS_MULTIPLE,
#                                                                   constants.SYNONYMS_MULTIPLE)
