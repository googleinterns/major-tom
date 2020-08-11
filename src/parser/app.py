from flask import Flask
from flask import request
from flask import jsonify

import database
import parser


app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/parse', endpoint='parser', methods=['POST'])
def trigger_parsing():
    parser.parse()


@app.route('/articles/byKeywords/', endpoint='database', methods=['GET'])
def by_keywords(id):
    data = request.data
    if data != '':
        pass


    return jsonify(database.get_article(id))

@app.route('/articles/<id>', endpoint='database', methods=['GET'])
def trigger_parsing(id):
    return jsonify(database.get_article(id))

# parser.parse('regs.pdf')
