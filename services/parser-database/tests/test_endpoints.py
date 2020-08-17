import json


def test_parse_endpoint(app, client):
    res = client.post('/parse')
    assert res.status_code == 200


def test_if_article_107_was_parsed():
    pass