from unittest.mock import MagicMock
from unittest import mock
import parser
import retriever


class MockRetrieverResponse:
    @staticmethod
    def get_document():
        return None


def test_has_file_changed_if_true():
    """Tests if the hash has changed, assuming it has.
    """
    past_hash = "afafbfbdce8c40924edae00f6ce54f0c639ce42a"\
                "2c0fbbfa6ab82ea6925827c51"
    file_name = "Monterrey.pdf"
    response = parser.has_file_changed(past_hash, file_name)
    assert response == True


def test_has_file_changed_if_false():
    """Tests if the hash has changed, assuming it has not.
    """
    past_hash = "afafbfbdce8c40924edae00f6ce54f0c639ce42a2c"\
                "0fbbfa6ab82ea6925827c5"
    file_name = "Monterrey.pdf"
    response = parser.has_file_changed(past_hash, file_name)
    assert response == False


def test_parse_all_documents(monkeypatch, mocker, mock_parser):
    mock_patch_parser = "parser.parse"
    with mock.patch(mock_patch_parser) as mck_parser:
        mck_parser.side_effect = mock_parser
        result = parser.parse_all_documents()
        assert result[0] == "afafbfbdce8c40924edae00f6ce54f0c639ce42a2c0fbbfa6ab82ea6925827c51"


mty_document = {
        "hash":
        "afafbfbdce8c40924edae00f6ce54f0c639ce42a2" +
        "c0fbbfa6ab82ea6925827c51",
        "jurisdiction":
        "Monterrey",
        "url":
        "http://www.guadalupe.gob.mx/wp-content/up" +
        "loads/2019/09/Nuevo-Reglamento-Homologado-1.pdf",
    }


def test_parse():
    parser.parse(mty_document, "Monterrey.pdf")

    # Mock Identify Articles
    # Mock Store Articles (no need to store them I guess,
    # just make it not break when its called, maybe
    # return none or something like that)