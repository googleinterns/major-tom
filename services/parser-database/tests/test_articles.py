"""This tests only test (duh) the parser's ability of
identifying individual articles, and does not test
parsing ability"""
from parser import identify_articles


test_file = {
    "hash":
    "afafbfbdce8c40924edae00f6ce54f0c639ce42a2" +
    "c0fbbfa6ab82ea6925827c51",
    "jurisdiction": "tests/test_document",
}


articles = (
    "articulo 1.- los ciclistas se deben de orillar"
    + " articulo 2- los ciclistas no se deben de orillar"
    + " articulo 3. velocidad maxima de 10kmh"
    + " artículo 4.- carros de mas de 3/4 toneladas requieren licencia de chofer"
    + " artículo 5.- no te pueden infraccionar en navidad"
    + " artículo 6.- marcar al seguro y al 911 al chocar"
).strip()
articles = articles.split()


def test_article_extraction_by_number_of_articles_extracted():
    """Tests if the right number of articles is extracted"""
    recieved_articles = identify_articles(articles)
    assert len(recieved_articles) == 6
    assert recieved_articles[0].number == 1
    assert recieved_articles[1].number == 2
    assert recieved_articles[2].number == 3
    assert recieved_articles[3].number == 4
    assert recieved_articles[4].number == 5
    assert recieved_articles[5].number == 6
    assert recieved_articles[0].text == "los ciclistas se deben de orillar"
    assert recieved_articles[1].text == "los ciclistas no se deben de orillar"
    assert recieved_articles[2].text == "velocidad maxima de 10kmh"
    assert recieved_articles[3].text == "carros de mas de 3/4 toneladas requieren licencia de chofer"
    assert recieved_articles[4].text == "no te pueden infraccionar en navidad"
    assert recieved_articles[5].text == "marcar al seguro y al 911 al chocar"
