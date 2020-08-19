from unittest import mock
import parser
import constants
from parser import Article


many_documents = [
        {
            "hash":
            "afafbfbdcfsefsesedae00f6ce54f0c639ce42a2"
            "c0fbbfa6ab82ea6925827c51",
            "jurisdiction":
            "Saltillo",
            "url":
            "http://www.guadalupe.gob.mx/wp-content/up"
            "loads/2019/09/Nuevo-Reglamento-Homologado-1.pdf",
        },
        {
            "hash":
            "afafbfbdce8c40924edae00f6ce54f0c639ce42a2"
            "c0fbbfa6ab82ea6925827c51",
            "jurisdiction":
            "Monterrey",
            "url":
            "http://www.guadalupe.gob.mx/wp-content/up"
            "loads/2019/09/Nuevo-Reglamento-Homologado-1.pdf",
        }
    ]


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
            mock_connector.return_value = many_documents
            parser.parse_all_documents()
            mock_parser.assert_any_call(many_documents[0])
            mock_parser.assert_any_call(many_documents[1])


mock_article_values = [
                        Article(1, "Este es un ariculo del reglamento de transito"),
                        Article(2, "Este es otro articulo del reglamento de transito"),
                        Article(3, "Este es el ultimo articulo del reglamento de transito.")
                        ]


def test_parse_if_file_has_changed():
    mock_article_identifier = "parser.identify_articles"
    mock_patch = "connector.store_article"
    mock_file_change_patch = "parser.has_file_changed"
    with mock.patch(mock_article_identifier) as mock_id_articles:
        with mock.patch(mock_patch) as mock_article_storage:
            with mock.patch(mock_file_change_patch) as mock_file_change:
                mock_id_articles.return_value = mock_article_values
                mock_file_change.return_value = True
                parser.parse(constants.mty_document)
                mock_article_storage.assert_any_call(mock_article_values[0].to_dict())
                mock_article_storage.assert_any_call(mock_article_values[1].to_dict())
                mock_article_storage.assert_any_call(mock_article_values[2].to_dict())


def test_parse_if_file_has_not_changed():
    mock_article_identifier = "parser.identify_articles"
    mock_patch = "connector.store_article"
    mock_file_change_patch = "parser.has_file_changed"
    with mock.patch(mock_article_identifier) as mock_id_articles:
        with mock.patch(mock_patch) as mock_article_storage:
            with mock.patch(mock_file_change_patch) as mock_file_change:
                mock_id_articles.return_value = mock_article_values
                mock_file_change.return_value = False
                parser.parse(constants.mty_document)
                mock_article_storage.assert_not_called()
