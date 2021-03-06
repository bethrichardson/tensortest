from flask import Flask, jsonify, request, abort
from flask_pymongo import PyMongo
from tester import run_test
from bson.objectid import ObjectId
import simplejson as json
from werkzeug import Response
import pandas as pd
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MONGO2_DBNAME'] = 'tensortest'
app.config['MONGO2_HOST'] = 'local.docker'

mongo = PyMongo(app, config_prefix='MONGO2')


@app.route('/')
@app.route('/index')
def index():
    return "Test time!"

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)


## '5abd1f8b468470aa1794cde2'
@app.route('/test')
def get_all_docs():
    cursor = mongo.db.api.find()
    return Response(json.dumps(list(cursor), cls=MongoJsonEncoder), mimetype='application/json')

# TODO: use api to query for correct data
def get_training_data():
    cursor = mongo.db.api.find()
    df = pd.DataFrame(list(cursor))
    df.pop('_id')
    print("printing frame")
    print(df)
    print ("done frame")
    return df


# TODO: Handle non float values
@app.route('/train')
def make_test():
    if int(request.args.get('status')) not in [0, 1, 2]:
        return abort(400)

    train_data = {
        "Status": int(request.args.get('status')),
        "Name": int(request.args.get('name')),
        "Environment": int(request.args.get('environment')),
        "Type": int(request.args.get('type')),
        "Code": int(request.args.get('code'))
    }
    doc = mongo.db.api.insert_one(train_data)
    response = {
        "acknowledged": doc.acknowledged,
        "id": doc.inserted_id
    }
    return Response(json.dumps(response, cls=MongoJsonEncoder), mimetype='application/json')


# TODO: Handle non float values
@app.route('/test/run')
def run_rest_test():
    test_value = {
        'Name': [int(request.args.get('name'))],
        'Environment': [int(request.args.get('environment'))],
        'Type': [int(request.args.get('type'))],
        'Code': [int(request.args.get('code'))]
    }
    name = request.args.get('name')
    print("Received API: " + name)
    actual_status = [request.args.get('status')]
    prediction, probability, expectation = run_test(test_value, actual_status, get_training_data())

    return jsonify({
        "prediction": prediction,
        "probability": probability,
        "expectation": expectation
    })


@app.route('/test/delete')
def delete_all_tests():
    doc = mongo.db.api.delete_many({})
    return "deleted all."


if __name__ == '__main__':
    app.run(debug=True)
