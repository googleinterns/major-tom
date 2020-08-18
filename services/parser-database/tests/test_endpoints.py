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


def test_if_article_120_was_parsed(app, client):
    app.config['JSON_AS_ASCII'] = False
    res = client.get("/articles/120")
    data = json.loads(res.get_data(as_text=True))
    must_match = {
        'articleNumber': 120,
        'text': 'las escuelas deberán contar con lugares especiales y debidamente señalizados para que los vehículos de transporte escolar efectúen el ascenso y descenso de los escolares, sin que afecte u obstaculice la circulación en la vía pública. en caso de que el lugar de ascenso y descenso de escolares, ocasione conflictos viales, o ponga en riesgo la integridad física de los mismos, dichos lugares serán ubicados en las inmediaciones de los planteles donde técnicamente sea factible a propuesta de las escuelas y previa autorización de la autoridad municipal, observando de manera primordial lo necesario para garantizar la seguridad de los escolares.',  # noqa: E501
        'wordCount': 100
    }
    assert data["articleNumber"] == must_match["articleNumber"]
    assert data["text"] == must_match["text"]
    assert data["wordCount"] == must_match["wordCount"]


def test_if_article_26_was_parsed(app, client):
    app.config['JSON_AS_ASCII'] = False
    res = client.get("/articles/26")
    data = json.loads(res.get_data(as_text=True))
    must_match = {
        'articleNumber': 26,
        'text': 'queda prohibido que los vehículos que circulen en la vía pública porten los accesorios o artículos siguientes: i. ii. faros encendidos o reflejantes de colores diferentes al blanco o ámbar en la parte delantera; faros encendidos o reflejantes de colores diferentes al rojo o ámbar en la parte posterior; con excepción solamente de las luces de reversa y de placa; iii. dispositivos de rodamiento con superficie metálica que haga contacto con el pavimento. esto incluye cadenas sobre las llantas; iv. radios que utilicen la frecuencia de la dependencia de tránsito correspondiente o cualquier otro cuerpo de seguridad; v. piezas del vehículo que no estén debidamente sujetas de tal forma que puedan desprenderse constituyendo un peligro; vi. sirena o aparatos que emitan sonidos semejantes a ella, torreta y/o luces estroboscópicas de cualquier color con excepción de los vehículos oficiales, de emergencia o especiales; artículos u objetos que impidan u obstaculicen la visibilidad del conductor; y mofles directos, rotos o que emitan un ruido excesivo. vii. viii.',  # noqa: E501
        'wordCount': 165
    }
    assert data["articleNumber"] == must_match["articleNumber"]
    assert data["text"] == must_match["text"]
    assert data["wordCount"] == must_match["wordCount"]
