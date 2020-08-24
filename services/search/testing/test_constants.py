KEYWORDS_DB_MOCK_1 = {"forzoso": {}, "bicicleta": {1: {"weight": 1}}, "usar": {},
                      "casco": {1: {"weight": 1}},
                      "obligatorio": {}, "inexcusable": {}, "imprescindible": {},
                      "preciso": {}, "necesario": {}, "bici": {}, "velocipedo": {}, "tandem": {},
                      "emplear": {}, "utilizar": {1: {"weight": 1}}, "gastar": {}, "acostumbrar": {},
                      "practicar": {},
                      "copa": {}, "suelo": {}, "pezuna": {}, "vaso": {}, "cabeza": {}}

KEYWORDS_DB_MULTIPLE = {"taxi": {3: {"weight": 2}}, "tener": {},
                        "calcomania": {4: {"weight": 1}}, "placa": {4: {"weight": 1}},
                        "taximetro": {},
                        "haber": {}, "poseer": {}, "detentar": {}, "sujetar": {}, "coger": {},
                        "copia": {}, "reproduccion": {}, "estampa": {}, "adhesivo": {},
                        "lamina": {}, "plancha": {}, "chapa": {}, "hoja": {}, "pelicula": {}}

KEYWORDS_ARTICLE_1 = ["forzoso", "bicicleta", "usar", "casco"]  # Es forzoso en bicicleta usar casco
# Synonyms created using design doc's mentioned spanish synonym api and limiting to 5 results
SYNONYMS_ARTICLE_1 = ["obligatorio", "inexcusable", "imprescindible", "preciso", "necesario",
                      "bici", "velocipedo", "tandem",
                      "emplear", "utilizar", "gastar", "acostumbrar", "practicar",
                      "copa", "suelo", "pezuna", "vaso", "cabeza"]

KEYWORDS_MULTIPLE = ["taxi", "tener", "calcomania", "placa"]  # Mi taxi no tiene estampa en la placa
SYNONYMS_MULTIPLE = ["taximetro",
                     "haber", "poseer", "detentar", "sujetar", "coger",
                     "copia", "reproduccion", "estampa", "adhesivo",
                     "lamina", "plancha", "chapa", "hoja", "pelicula"]

DEFAULT_MAX_SYNONYMS = 5
TEN_SYNONYMS = 10
INCREASED_MAX_SYNONYMS = 8
DECREASED_MAX_SYNONYMS = 3

MOCK_URL_DB = "http://somerealurl.com/"
MOCK_URL_KEYWORDS = "http://someotherurl.com/"
