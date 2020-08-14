from parser import identify_articles


test_file = {
    "hash":
    "afafbfbdce8c40924edae00f6ce54f0c639ce42a2" +
    "c0fbbfa6ab82ea6925827c51",
    "jurisdiction": "tests/test_document",
}

'''
def test_file_parsability():
    parse(test_file)
'''

articles = (
    "articulo 1.- los ciclistas se deben de orillar"
    + " articulo 2- los ciclistas no se deben de orillar"
    + " articulo 3. velocidad maxima de 10kmh"
    + " artículo 4.- carros de mas de 3/4 toneladas requieren licencia de chofer"
    + " artículo 5.- no te pueden infraccionar en navidad"
    + " artículo 6.- marcar al seguro y al 911 al chocar"
)


def test_article_extraction_by_number_of_articles_extracted():
    recieved_articles = identify_articles(articles.strip().split())
    assert len(recieved_articles) == 6


def test_article_extraction_by_article_content():
    recieved_articles = identify_articles(articles.strip().split())
    assert recieved_articles[1].text == " los ciclistas se deben de orillar"
    assert recieved_articles[4].text == " carros de mas de 3/4 toneladas requieren licencia de chofer"
