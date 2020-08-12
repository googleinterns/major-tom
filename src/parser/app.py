from flask import Flask # pylint: disable=import-error
from flask import request # pylint: disable=import-error
from flask import jsonify # pylint: disable=import-error

import database # pylint: disable=import-error
import parser # pylint: disable=import-error


app = Flask(__name__)


@app.route('/parse', endpoint='parser', methods=['POST'])
def trigger_parsing():
    # return parser.parse_without_database()
    return parser.parse()


@app.route('/articles/byKeywords', methods=['POST'])
def get_keywords():
    data = request.get_json()
    return jsonify(parser.get_articles_that_match_keywords(data['keywords']))
    # else:
    #     return "Invalid Request Body", 500

@app.route('/articles/<id>', methods=['GET'])
def get_article_by_number_in_memory(id):
    return jsonify(parser.get_article_by_number(id))

# parser.parse('regs.pdf')
