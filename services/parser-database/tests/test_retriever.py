from unittest import mock
import requests  # pylint: disable=import-error
import pytest  # pylint: disable=import-error
import responses  # pylint: disable=import-error
import retriever

@responses.activate
def test_http_error_retrieving():
    """
    Tests re raising of status code 400 when calling keywords endpoint
    """
    mock_url = "http://somerealurl.com/"
    mock_file_path = "/here.pdf"
    responses.add(responses.GET, mock_url, status=400)

    with pytest.raises(requests.HTTPError):
        retriever.get_document(mock_url, mock_file_path)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == mock_url
    assert responses.calls[0].response.status_code == 400
