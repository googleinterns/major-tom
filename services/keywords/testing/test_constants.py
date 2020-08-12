from google.cloud.language import enums

VERB_TAG = enums.PartOfSpeech.Tag.VERB
DET_TAG = enums.PartOfSpeech.Tag.DET

HABLANDO_TOKEN = {'text': {'content': 'hablando'},
                  'lemma': 'hablar', 'part_of_speech': {'tag': VERB_TAG}}
EL_TOKEN = {'text': {'content': 'el'}, 'lemma': 'el', 'part_of_speech': {'tag': DET_TAG}}
