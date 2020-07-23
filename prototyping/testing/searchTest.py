import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from Search import Search

# Assuming articles already come in lemma form, lemma form created manually using cloud natural language
article_1 = "El conductor y ocupante de bicicleta, bicimoto o triciclos poder utilizar de preferencia casco de proteccion para el seguridad."
article_2 = "El autoridad municipal poder determinar el instalación de reloj estacionometros en el via publico, previo estudio de factibilidad elaborar por el Secretaria."
article_3 = "No se autorizar ninguno exclusivo para taxi a un distancia menor de 300-trescientos metro a el redonda de otro sitio de taxi autorizar."
article_4 = "El calcomania de refrendo de vehiculo deber colocar en el espacio establecer en el placa de circulacion."
articles = [ article_1, article_2, article_3, article_4 ]

keywords_article_1 = ["forzoso", "bicicleta","usar" ,"casco"] # Es forzoso en bicicleta usar casco
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
    result = { article_1 : 3 }

    assert result == Search(keywords_article_1, synonyms_article_1, articles).score_articles()

def test_double_weights_synonyms():
    result = { article_1 : 4 }
    
    assert result == Search(keywords_article_1, synonyms_article_1, articles, synonyms_weight=2).score_articles()

def test_multiple_articles():
    result = { article_3 : 2, article_4 : 2}

    assert result == Search(keywords_article_1, synonyms_article_1, articles).score_articles()
