from app import create_app
import os,pytest

@pytest.fixture
def app():
    app = create_app()
    return app

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
