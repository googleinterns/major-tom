from search.search_engine import SearchEngine
from mock_article import Article

# Assuming articles already come in lemma form,
# lemma form created manually using cloud natural language
ARTICLE_1 = Article(1, 1, "El conductor y ocupante de bicicleta, bicimoto o triciclos poder utilizar de preferencia casco de proteccion para el seguridad.",
                    {"conductor" : 1, "ocupante" : 1, "bicicleta" : 1, "bicimoto" : 1, "triciclos" : 1, "poder" : 1, "utilizar" : 1, "preferencia" : 1,
                     "casco" : 1, "proteccion"  : 1, "seguridad" : 1})
ARTICLE_2 = Article(2, 2, "El autoridad municipal poder determinar el instalación de reloj estacionometros en el via publico, previo estudio de factibilidad elaborar por el Secretaria.",
                    {"autoridad" : 1, "municipal" : 1, "poder" : 1, "determinar" : 1, "instalación" : 1, "reloj" : 1, "estacionometros" : 1, "via" : 1, "publico" : 1, "previo" : 1,
                     "estudio" : 1, "factibilidad" : 1, "elaborar" : 1, "secretaria" : 1})
ARTICLE_3 = Article(3, 3, "No se autorizar ninguno exclusivo para taxi a un distancia menor de 300-trescientos metro a el redonda de otro sitio de taxi autorizar.",
                    {"autorizar" : 2, "ninguno" : 1, "exclusivo" : 1, "taxi" : 2, "distancia" : 1, "menor" : 1, "300-trescientos" : 1, "metro" : 1, "redonda" : 1, "sitio" : 1})
ARTICLE_4 = Article(4, 4, "El calcomania de refrendo de vehiculo deber colocar en el espacio establecer en el placa de circulacion.",
                    {"calcomania" : 1, "refrendo" : 1, "vehiculo" : 1, "deber" : 1, "colocar" : 1, "espacio" : 1, "establecer" : 1, "placa" : 1, "circulacion" : 1})



ARTICLES = [ARTICLE_1, ARTICLE_2, ARTICLE_3, ARTICLE_4]

KEYWORDS_ARTICLE_1 = ["forzoso", "bicicleta", "usar", "casco"] # Es forzoso en bicicleta usar casco
# Synonyms created using design doc's mentioned spanish synonym api and limiting to 5 results
SYNONYMS_ARTICLE_1 = ["obligatorio", "inexcusable", "imprescindible", "preciso", "necesario",
                      "bici", "velocipedo", "tandem",
                      "emplear", "utilizar", "gastar", "acostumbrar", "practicar",
                      "copa", "suelo", "pezuna", "vaso", "cabeza"]

KEYWORDS_MULTIPLE = ["taxi", "tener", "calcomania", "placa"] # Mi taxi no tiene estampa en la placa
SYNONYMS_MULTIPLE = ["taximetro",
                     "haber", "poseer", "detentar", "sujetar", "coger",
                     "copia", "reproduccion", "estampa", "adhesivo",
                     "lamina", "plancha", "chapa", "hoja", "pelicula"]


def test_same_weights_for_all():
    """
    Have the query only apply for article 1, and the weights be the same for keywords and synonyms (default args.)
    """
    result = {1 : 3}

    assert result == SearchEngine(ARTICLES).query(KEYWORDS_ARTICLE_1, SYNONYMS_ARTICLE_1)

def test_double_weights_synonyms():
    """
    Have the query only apply for article 1, and double the synonym weights
    """
    result = {1 : 4}

    assert result == SearchEngine(ARTICLES, synonyms_weight=2).query(KEYWORDS_ARTICLE_1, SYNONYMS_ARTICLE_1)

def test_multiple_articles():
    """
    Have the query apply for two articles
    """
    result = {3 : 2, 4 : 2}

    assert result == SearchEngine(ARTICLES).query(KEYWORDS_MULTIPLE, SYNONYMS_MULTIPLE)
