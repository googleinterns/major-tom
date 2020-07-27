import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from Search import Search
from MockArticle import Article

# Assuming articles already come in lemma form, lemma form created manually using cloud natural language
article_1 = Article(1,"El conductor y ocupante de bicicleta, bicimoto o triciclos poder utilizar de preferencia casco de proteccion para el seguridad.", 
                    {"conductor" : 1, "ocupante" : 1, "bicicleta" : 1, "bicimoto" : 1, "triciclos" : 1, "poder" : 1, "utilizar" : 1, "preferencia" : 1,
                     "casco" : 1, "proteccion"  : 1, "seguridad" : 1})
article_2 = Article(2, "El autoridad municipal poder determinar el instalación de reloj estacionometros en el via publico, previo estudio de factibilidad elaborar por el Secretaria.",
                    {"autoridad" : 1, "municipal" : 1, "poder" : 1, "determinar" : 1, "instalación" : 1, "reloj" : 1, "estacionometros" : 1, "via" : 1, "publico" : 1, "previo" : 1,
                     "estudio" : 1, "factibilidad" : 1, "elaborar" : 1, "secretaria" : 1})
article_3 = Article(3, "No se autorizar ninguno exclusivo para taxi a un distancia menor de 300-trescientos metro a el redonda de otro sitio de taxi autorizar.",
                      {"autorizar" : 2, "ninguno" : 1, "exclusivo" : 1, "taxi" : 2, "distancia" : 1, "menor" : 1, "300-trescientos" : 1, "metro" : 1, "redonda" : 1, "sitio" : 1})
article_4 = Article(4, "El calcomania de refrendo de vehiculo deber colocar en el espacio establecer en el placa de circulacion.",
                      {"calcomania" : 1, "refrendo" : 1, "vehiculo" : 1, "deber" : 1, "colocar" : 1, "espacio" : 1, "establecer" : 1, "placa" : 1, "circulacion" : 1})



articles = [ article_1, article_2, article_3, article_4 ]

keywords_article_1 = ["forzoso", "bicicleta","usar" ,"casco"] # Es forzoso en bicicleta usar casco
# Synonyms created using design doc's mentioned spanish synonym api and limiting to 5 results
synonyms_article_1 = ["obligatorio", "inexcusable", "imprescindible", "preciso", "necesario",
                      "bici", "velocipedo", "tandem",
                      "emplear", "utilizar", "gastar", "acostumbrar", "practicar",
                      "copa", "suelo", "pezuna", "vaso", "cabeza"]

keywords_multiple = ["taxi", "tener", "calcomania", "placa"] # Mi taxi no tiene estampa en la placa
synonyms_multiple = ["taximetro",
                     "haber", "poseer", "detentar", "sujetar", "coger",
                     "copia", "reproduccion", "estampa", "adhesivo",
                     "lamina", "plancha", "chapa", "hoja", "pelicula"]


def test_same_weights_for_all():
    """
    Have the query only apply for article 1, and the weights be the same for keywords and synonyms (default args.)
    """
    result = { article_1 : 3 }

    assert result == Search(keywords_article_1, synonyms_article_1, articles).score_articles()

def test_double_weights_synonyms():
    """
    Have the query only apply for article 1, and double the synonym weights
    """
    result = { article_1 : 4 }
    
    assert result == Search(keywords_article_1, synonyms_article_1, articles, synonyms_weight=2).score_articles()

def test_multiple_articles():
    """
    Have the query apply for two articles
    """
    result = { article_3 : 2, article_4 : 2}

    assert result == Search(keywords_multiple, synonyms_multiple, articles).score_articles()
