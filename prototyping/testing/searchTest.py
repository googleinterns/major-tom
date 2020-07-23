import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from Search import Search

# Assuming articles already come in lemma form, lemma form created manually using cloud natural language
articles = [
        "El conductor y ocupante de bicicleta, bicimoto o triciclos poder utilizar de preferencia casco de proteccion para el seguridad.",
	"El autoridad municipal poder determinar el instalación de reloj estacionometros en el via publico, previo estudio de factibilidad elaborar por el Secretaria.",
	"No se autorizar ninguno exclusivo para taxi a un distancia menor de 300-trescientos metro a el redonda de otro sitio de taxi autorizar.",
	"El calcomania de refrendo de vehiculo deber colocar en el espacio establecer en el placa de circulacion."
    ]
keywords_article_1 = ["forzoso", "bicicleta","usar" ,"casco"] # Es forzoso en bicicleta usar casco
synonyms_article_1 = ["obligatorio", "inexcusable", "imprescindible", "preciso", "necesario",
                      "bici", "velocipedo", "tandem",
                      "emplear", "utilizar", "gastar", "acostumbrar", "practicar",
                      "copa", "suelo", "pezuna", "vaso", "cabeza"]

def test_same_weights_for_all():
    result = {"El conductor y ocupante de bicicleta, bicimoto o triciclos poder utilizar de preferencia casco de proteccion para el seguridad." : 3}

    assert result == Search(keywords_article_1, synonyms_article_1, articles).score_articles()
