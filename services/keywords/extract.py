import logging
from google.cloud import language  # pylint: disable=import-error
from google.cloud.language import enums, types  # pylint: disable=import-error
import constants


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


def extract_keywords(text):
    """
    Removes extra information from the gcloud response. This includes everything that is not
    the language, the words found, the lemma version of said words, the part of speech for said word
    and any word that is not part of the key parts of speech constants.
    Attributes:
        text: The text which we wish to extract lemmatized keywords
    Returns:
        An object with the language, the keywords as defined by the design doc,
        the lemma and part of speech for said keywords
    """
    gcloud_response = gcloud_syntax_extraction(text)
    logging.info("gcloud syntax response: %s", gcloud_response)

    tokens_shortened = []
    for token in gcloud_response.tokens:
        part_of_speech_tag = enums.PartOfSpeech.Tag(token.part_of_speech.tag).name
        if part_of_speech_tag in constants.KEY_PARTS_OF_SPEECH:
            token_data = {'word': token.text.content, 'lemma': token.lemma,
                          'part_of_speech': part_of_speech_tag}
            tokens_shortened.append(token_data)

    response = {'lan': gcloud_response.language, 'tokens': tokens_shortened}

    return response
