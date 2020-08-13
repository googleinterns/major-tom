from flask import Flask  # pylint: disable=import-error
from flask import request  # pylint: disable=import-error
from flask import jsonify  # pylint: disable=import-error

import parser  # pylint: disable=import-error


app = Flask(__name__)


@app.route('/parse', endpoint='parser', methods=['POST'])
def trigger_parsing():
    # return parser.parse_without_database()
    try:
        parser.parse_all_documents()
    except Exception:
        return "Internal Server Error", 500
    return "Sucessful Operation", 200


@app.route('/articles/byKeywords', methods=['POST'])
def get_keywords():
    json_request = request.get_json()
    if "keywords" not in json_request:
        return {"error": "keywords request body is missing"}, 500
    else:
        return jsonify(parser.get_articles_that_match_keywords(json_request['keywords']))


@app.route('/articles/<id>', methods=['GET'])
def get_article_by_number_in_memory(id):
    """Returns the articlle that matches the ID value
    accoring to the apiSpec.yaml file"""
    article = parser.get_article_by_number(id)
    if article is not None:
        return jsonify(article)
    else:
        return "No article matches such ID", 402


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8082)
