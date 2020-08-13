import random
import json


def get_keywords(text):
    splited_text = text.split()
    keywords = {"keywords": [splited_text[random.randint(0, len(splited_text)-1)], splited_text[random.randint(0, len(splited_text)-1)]]}
    return json.dumps(keywords)
