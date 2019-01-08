from time import time
from flask import Flask, request, Response, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

mongo = MongoClient('mongo', 27017)
db = mongo.domainsdb

time_start = time()

app = Flask(__name__)

def calc_time_taken(time_start):
    current_time = time()
    return round(current_time - time_start, 6)

@app.before_request
def before_request():
    global time_start
    time_start = time()

    response = jsonify({
        "success": 0,
        "data": {
            "error": 'required parameter "key" is missing'
        },
        "time": calc_time_taken()
    })

    if not "key" in request.args:
        return response, 400
    if not request.args["key"]:
        return response, 400

@app.route('/host/<ip>')
def get_domains(ip):
    current_time = time()
    page = request.args.get('page', 0)
    records = db.domains.find({"A": ip}, {"domain": ip}).limit(100).skip(int(page))
    domains = []
    for item in records:
        domains.append(item['domain'])

    return jsonify({
        "success": 1,
        "data": {
            "domains": domains,
            "time": calc_time_taken(current_time)
        }
    })


@app.route('/host/<ip>/count')
def count_items(ip):
    current_time = time()
    number_of_domains = db.domains.find({"A": ip}).count()
    return jsonify({
        "success": 1,
        "data": {
            "count": number_of_domains,
            "time": calc_time_taken(current_time)
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
