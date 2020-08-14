import os

from flask import Flask  # pylint: disable=import-error
from flask import request  # pylint: disable=import-error
from flask import jsonify  # pylint: disable=import-error

from parser import parse_all_documents  # pylint: disable=import-error
from parser import get_articles_that_match_keywords  # pylint: disable=import-error
from parser import get_article_by_number  # pylint: disable=import-error

app = Flask(__name__)


@app.route('/parse', endpoint='parser', methods=['POST'])
def trigger_parsing():
    # return parser.parse_without_database()
    try:
        parse_all_documents()
    except Exception as e:
        print(e)
        return "Internal Server Error", 500
    return "Sucessful Operation", 200


@app.route('/articles/byKeywords', methods=['POST'])
def get_keywords():
    json_request = request.get_json()
    if "keywords" not in json_request:
        return {"error": "keywords request body is missing"}, 400
    else:
        return jsonify(get_articles_that_match_keywords(json_request['keywords']))


@app.route('/articles/<id>', methods=['GET'])
def get_article_by_number_in_memory(id):
    """Returns the articlle that matches the ID value
    accoring to the apiSpec.yaml file"""
    article = get_article_by_number(id)
    if article is not None:
        return jsonify(article)
    else:
        return {"error": "Article not found with submitted ID"}, 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT"))
