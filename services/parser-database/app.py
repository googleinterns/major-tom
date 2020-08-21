import os
from copy import copy

from flask import Flask  # pylint: disable=import-error
from flask import request  # pylint: disable=import-error
from flask import jsonify  # pylint: disable=import-error

from parser import parse_all_documents
from connector import get_articles_that_match_keywords
from connector import get_article_by_number

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/parse', endpoint='parser', methods=['POST'])
def trigger_parsing():
    try:
        parse_all_documents()
    except Exception as e:
        print(e)
        return {"error": {"message": "Internal Parser Error"}}, 500
    return "Sucessful Operation", 200


@app.route('/articles/byKeywords', methods=['POST'])
def get_keywords():
    json_request = request.get_json()
    if "keywords" not in json_request:
        return {"error": {"message": "keywords request body is missing"}}, 400
    else:
        return jsonify(get_articles_that_match_keywords(json_request['keywords']))


@app.route('/articles/<id>', methods=['GET'])
def get_article_by_number_in_memory(id):
    """Returns the article that matches the ID value
    accoring to the apiSpec.yaml file"""
    article = get_article_by_number(str(id))
    if article is not None:
        article = copy(article)
        del article["id"]
        return jsonify(article)
    else:
        return {"error": {
            "message": "Article not found with submitted ID"}}, 404


if __name__ == '__main__':
    parse_all_documents()
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT"))
