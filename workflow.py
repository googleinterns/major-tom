import utils
from search.search_engine import SearchEngine
import constants

def query_workflow(search, query):
    short_gresponse = utils.from_gcloud_remove_extra(utils.gcloud_syntax_extraction(query))

    keywords = []

    for token in short_gresponse['tokens']:
        keywords.append(token['lemma'])

    lan = short_gresponse['lan']
    synonyms = []
    if lan == 'es':
        for word in keywords:
            for synonym in utils.create_synonym_list_esp(word):
                synonyms.append(synonym)

    return search.query(keywords, synonyms)

def main():
    search = SearchEngine(constants.ARTICLES, keywords_weight=2)
    print(query_workflow(search, constants.QUERY_ARTICLE_1))

if __name__ == '__main__':
    main()
