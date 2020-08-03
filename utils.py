import requests # pylint: disable=import-error
from google.cloud import language # pylint: disable=import-error
from google.cloud.language import enums, types # pylint: disable=import-error

SPANISH_API_URL = "http://sesat.fdi.ucm.es:8080/servicios/rest/sinonimos/json/"
KEY_PARTS_OF_SPEECH = ["ADJ", "NOUN", "NUM", "VERB"]

def gcloud_syntax_extraction(text):
    """
    Calls the gcloud natural langauge api's analyze syntax
    Attributes:
        text: the text which we wish to analyze
    Returns:
        the response given by the api call
    """
    client = language.LanguageServiceClient()
    # pylint: disable=no-member
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_syntax(document=document)

    return response

def from_gcloud_remove_extra(gcloud_response):
    """
    Removes extra information from the gcloud response. This includes everything that is not
    the language, the words found, the lemma version of said words, the part of speech for said word
    and any word that is not part of the key parts of speech constants.
    Attributes:
        gcloud_response: the response given by the natural language api
    Returns:
        An object with the language, the keywords as defined by the design doc,
        the lemma and part of speech for said keywords
    """
    tokens_shortened = []
    for token in gcloud_response.tokens:
        # pylint: disable=no-member
        part_of_speech_tag = enums.PartOfSpeech.Tag(token.part_of_speech.tag).name
        if part_of_speech_tag in KEY_PARTS_OF_SPEECH:
            token_data = {'word' : token.text.content, 'lemma' : token.lemma,
                          'part_of_speech' : part_of_speech_tag}
            tokens_shortened.append(token_data)

    response = {'lan' : gcloud_response.language, 'tokens' : tokens_shortened}

    return response

def create_synonym_list_esp(word_arr, max_synonyms=5):
    """
    Retrieves a synonym list given a word list
    Attributes:
        word_arr: The word list which we wish to find synonyms for
        max_synonyms: The maximum number of synonyms per word in word_arr
            optional: Default value 5
    Returns: a list of synonyms
    """
    synonyms = []
    for word in word_arr:
        payload = requests.get(SPANISH_API_URL+word)
        word_synonyms = payload.json()['sinonimos']
        if len(word_synonyms) > max_synonyms:
            word_synonyms = word_synonyms[:max_synonyms]
        for synonym in word_synonyms:
            synonyms.append(synonym['sinonimo'])

    return synonyms
