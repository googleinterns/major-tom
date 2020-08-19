from unittest import mock
import parser
import constants
import connector


def test_has_file_changed_if_true():
    """Tests if the hash has changed, assuming it has.
    """
    past_hash = "afafbfbdce8c40924edae00f6ce54f0c639ce42a"\
                "2c0fbbfa6ab82ea6925827c51"
    file_name = "Monterrey.pdf"
    response = parser.has_file_changed(past_hash, file_name)
    assert response is True


def test_has_file_changed_if_false():
    """Tests if the hash has changed, assuming it has not.
    """
    past_hash = "afafbfbdce8c40924edae00f6ce54f0c639ce42a2c"\
                "0fbbfa6ab82ea6925827c5"
    file_name = "Monterrey.pdf"
    response = parser.has_file_changed(past_hash, file_name)
    assert response is False


def test_parse_all_documents():
    mock_patch_parser = "parser.parse"
    mock_patch_get_documents = "connector.get_documents_to_parse"
    with mock.patch(mock_patch_parser) as mock_parser:
        with mock.patch(mock_patch_get_documents) as mock_connector:
            mock_connector.return_value = [constants.mty_document]
            parser.parse_all_documents()
            mock_parser.assert_called_once_with(constants.mty_document)


def test_parse_all_documents_multiple_documents():
    mock_patch_parser = "parser.parse"
    mock_patch_get_documents = "connector.get_documents_to_parse"
    with mock.patch(mock_patch_parser) as mock_parser:
        with mock.patch(mock_patch_get_documents) as mock_connector:
            mock_connector.return_value = constants.many_documents
            parser.parse_all_documents()
            assert mock_parser.call_count == len(constants.many_documents)


def test_parse():
    mock_article_identifier = "parser.identify_articles"
    mock_patch = "connector.store_article"
    with mock.patch(mock_article_identifier) as mock_id_articles:
        with mock.patch(mock_patch) as mock_article_storage:
            mock_id_articles.return_value = constants.mock_article_values
            parser.parse(constants.mty_document)
            assert mock_article_storage.call_count == len(constants.mock_article_values)


def test_get_documents():
    assert connector.get_documents_to_parse() == [constants.mty_document]


def test_get_articles_that_match_keywords():
    pass
    # Mock in memory keywords in memory
    # Test this against the keywords in memory
    # Assert results