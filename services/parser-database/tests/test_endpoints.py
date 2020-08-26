from unittest.mock import MagicMock
import random
import json

import retriever


class MockRetrieverResponse:
    @staticmethod
    def get_document():
        return None


def load_data(endpoint, *args, **kwargs):
    splited_text = endpoint.split()
    keywords = [
        splited_text[random.randint(0, len(splited_text) - 1)],
        splited_text[random.randint(0, len(splited_text) - 1)],
    ]
    return keywords


def test_parse_endpoint(app, client, monkeypatch, mocker):
    def mock_retriever(*args, **kwargs):
        return MockRetrieverResponse()

    mock_keywords = MagicMock(name="get_keywords")
    mock_keywords.get.side_effect = load_data
    mocker.patch("connector.get_keywords", new=mock_keywords)

    monkeypatch.setattr(retriever, "get_document", mock_retriever)

    res = client.post("/parse")
    assert res.status_code == 200


def test_if_article_119_was_parsed(app, client):
    app.config['JSON_AS_ASCII'] = False
    res = client.get("/articles/119")
    data = json.loads(res.get_data(as_text=True))
    must_match = {
        'id': '119',
        'number': 119,
        'content': "Las escuelas deberán contar con lugares especiales y debidamente señalizados \n\npara que los vehículos de transporte escolar efectúen el ascenso y descenso de los escolares, sin que \n\nafecte u obstaculice la circulación en la vía pública. En caso de que el lugar de ascenso y descenso \n\nde escolares, ocasione conflictos viales, o ponga en riesgo la integridad física de los mismos, dichos \n\nlugares serán ubicados en las inmediaciones de los planteles donde técnicamente sea factible a \n\npropuesta de las escuelas y previa autorización de la Autoridad Municipal, observando de manera \n\nprimordial lo necesario para garantizar la seguridad de los escolares.",  # noqa: E501
        'wordCount': 100
    }
    assert data == must_match


def test_if_article_25_was_parsed(app, client):
    app.config['JSON_AS_ASCII'] = False
    res = client.get("/articles/25")
    data = json.loads(res.get_data(as_text=True))
    must_match = {
        'id': '25',
        'number': 25,
        'content': "Queda prohibido que los vehículos que circulen en la vía pública porten los accesorios \n\no artículos siguientes: \n\nI. \n\nII. \n\nFaros encendidos o reflejantes de colores diferentes al blanco o ámbar en la parte delantera;  \n\nFaros encendidos o reflejantes de colores diferentes al rojo o ámbar en la parte posterior; con \n\nexcepción solamente de las luces de reversa y de placa; \n\n \n \n \n \n \n \n\fIII. \n\nDispositivos de rodamiento con superficie metálica que haga contacto con el pavimento. Esto \n\nincluye cadenas sobre las llantas; \n\nIV. \n\nRadios que utilicen la frecuencia de la Dependencia de Tránsito correspondiente o cualquier \n\notro cuerpo de seguridad; \n\nV. \n\nPiezas del vehículo que no estén debidamente sujetas de tal forma que puedan desprenderse \n\nconstituyendo un peligro; \n\nVI. \n\nSirena o aparatos que emitan sonidos semejantes a ella, torreta y/o luces estroboscópicas de \n\ncualquier color con excepción de los vehículos oficiales, de emergencia o especiales; \n\nArtículos u objetos que impidan u obstaculicen la visibilidad del conductor; y \n\nMofles directos, rotos o que emitan un ruido excesivo. \n\nVII. \n\nVIII.",  # noqa: E501
        'wordCount': 165
    }
    assert data == must_match
