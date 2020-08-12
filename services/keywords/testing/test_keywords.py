import json
import mock  # pylint: disable=import-error
import flask  # pylint: disable=import-error
from munch import munchify  # pylint: disable=import-error
from main import get_keywords_service as get_keywords  # pylint: disable=no-name-in-module
import test_constants as constants


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


def test_single_word_keyword():
    """
    Only one word in input, but it is a keyword
    """
    result = {'lan': 'es', 'tokens': [
        {'word': 'hablando', 'lemma': 'hablar', 'part_of_speech': 'VERB'}]}
    mock_response = {'language': 'es', 'tokens': [constants.HABLANDO_TOKEN]}
    response_obj = munchify(mock_response)

    with mock.patch('extract.gcloud_syntax_extraction', return_value=response_obj):
        assert result == get_keywords(make_flask_request({'text': 'hablando'}))


def test_single_word_not_keyword():
    """
    Only one word in input, but it isn't a keyword
    """
    result = {'lan': 'es', 'tokens': []}
    mock_response = {'language': 'es', 'tokens': [constants.EL_TOKEN]}
    response_obj = munchify(mock_response)

    with mock.patch('extract.gcloud_syntax_extraction', return_value=response_obj):
        assert result == get_keywords(make_flask_request({'text': 'el'}))


def test_no_words():
    """
    No words in input
    """
    result = {'lan': 'es', 'tokens': []}

    mock_response = {'tokens': [], 'language': 'es'}
    response_obj = munchify(mock_response)

    with mock.patch('extract.gcloud_syntax_extraction', return_value=response_obj):
        assert result == get_keywords(make_flask_request({'text': ''}))


def test_wrong_input():
    """
    text in json body missing from request
    """
    result = {"error": {"message": "ValueError: Expected 'text' field in json body is missing"}}

    assert result == get_keywords(make_flask_request({'': ''}))
