import pytest  # pylint: disable=import-error

from app import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(name="mock_parser", scope="session")
def fixture_parser_mock():
    def _mock(past_hash, file_name):
        return [past_hash, file_name]
    return _mock


@pytest.fixture(name="mock_retriever", scope="session")
def fixture_mock_retriever():
    def _mock(url, file_name):
        return None
    return _mock
