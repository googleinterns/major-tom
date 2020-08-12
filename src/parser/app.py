from flask import Flask
from flask import request
from flask import jsonify

import database
import parser


app = Flask(__name__)


@app.route('/parse', endpoint='parser', methods=['POST'])
def trigger_parsing():
    # return parser.parse_without_database()
    return parser.parse()


@app.route('/articles/byKeywords', methods=['POST'])
def by_keywords():
    data = request.get_json()
    print(data)
    return jsonify(data)
    # return jsonify(parser.get_articles_that_match_keywords(data['keywords']))
    # else:
    #     return "Invalid Request Body", 500

@app.route('/articles/<id>', methods=['GET'])
def get_article_by_number_in_memory(id):
    return jsonify(parser.get_article_by_number(id))

# parser.parse('regs.pdf')
