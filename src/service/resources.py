from flask import Flask, jsonify, request, abort
from flask_pymongo import PyMongo
from tester import run_test
from bson.objectid import ObjectId
import simplejson as json
from werkzeug import Response
import pandas as pd
from flask_cors import CORS
import test_application
import random

app = Flask(__name__)
CORS(app)

app.config['MONGO2_DBNAME'] = 'tensortest'
app.config['MONGO2_HOST'] = 'local.docker'

mongo = PyMongo(app, config_prefix='MONGO2')
NUM_TRAINING_RUNS = 350
MIN_TEST_INPUT_RANGE = 0
MAX_TEST_INPUT_RANGE = 5
MIN_ACCEPTABLE_ACCURACY = 95
NUM_TRAINING_RUN_INCREMENT = 50


@app.route('/')
@app.route('/index')
def index():
    return "Test time!"


class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)


@app.route('/test')
def get_all_docs():
    cursor = mongo.db.api.find()
    return Response(json.dumps(list(cursor), cls=MongoJsonEncoder), mimetype='application/json')


def get_training_data():
    cursor = mongo.db.api.find()
    df = pd.DataFrame(list(cursor))
    df.pop('_id')
    # print("printing frame")
    # print(df)
    return df


@app.route('/train')
def make_test():
    name = int(request.args.get('name'))
    env = int(request.args.get('environment'))
    typ = int(request.args.get('type'))
    code = int(request.args.get('code'))
    status = test_application.run(name, env, typ, code)

    if int(status) not in [0, 1, 2]:
        return abort(400)

    train_data = {
        "Status": status,
        "Name": name,
        "Environment": env,
        "Type": typ,
        "Code": code
    }
    doc = mongo.db.api.insert_one(train_data)
    response = {
        "acknowledged": doc.acknowledged,
        "id": doc.inserted_id
    }
    return Response(json.dumps(response, cls=MongoJsonEncoder), mimetype='application/json')


def run_training_set(size):
    for i in range(0, size):
        name = random.randint(MIN_TEST_INPUT_RANGE, MAX_TEST_INPUT_RANGE)
        env = random.randint(MIN_TEST_INPUT_RANGE, MAX_TEST_INPUT_RANGE)
        typ = random.randint(MIN_TEST_INPUT_RANGE, MAX_TEST_INPUT_RANGE)
        code = random.randint(MIN_TEST_INPUT_RANGE, MAX_TEST_INPUT_RANGE)
        status = test_application.run(name, env, typ, code)

        train_data = {
            "Status": status,
            "Name": name,
            "Environment": env,
            "Type": typ,
            "Code": code
        }
        mongo.db.api.insert_one(train_data)

@app.route('/train/random')
def train_exhaustively():
    run_training_set(NUM_TRAINING_RUNS)
    name = random.randint(MIN_TEST_INPUT_RANGE, MAX_TEST_INPUT_RANGE)
    env = random.randint(MIN_TEST_INPUT_RANGE, MAX_TEST_INPUT_RANGE)
    typ = random.randint(MIN_TEST_INPUT_RANGE, MAX_TEST_INPUT_RANGE)
    code = random.randint(MIN_TEST_INPUT_RANGE, MAX_TEST_INPUT_RANGE)

    test_value = {
        'Name': [name],
        'Environment': [env],
        'Type': [typ],
        'Code': [code]
    }

    prediction, probability, accuracy = run_test(test_value, get_training_data())
    print("Accuracy is:" + str(accuracy))
    num_tests = 1
    while accuracy < MIN_ACCEPTABLE_ACCURACY:
        print("Adding additional training set. Accuracy is too low: " + str(accuracy))
        run_training_set(NUM_TRAINING_RUN_INCREMENT)
        prediction, probability, accuracy = run_test(test_value, get_training_data())
        num_tests += 1

    response = {
        "acknowledged": True,
        "num_test_runs": num_tests,
        "accuracy": accuracy
    }
    return Response(json.dumps(response, cls=MongoJsonEncoder), mimetype='application/json')


@app.route('/test/run')
def run_rest_test():
    test_value = {
        'Name': [int(request.args.get('name'))],
        'Environment': [int(request.args.get('environment'))],
        'Type': [int(request.args.get('type'))],
        'Code': [int(request.args.get('code'))]
    }
    prediction, probability, accuracy = run_test(test_value, get_training_data())

    return jsonify({
        "prediction": prediction,
        "probability": probability,
        "accuracy": accuracy
    })


@app.route('/test/delete')
def delete_all_tests():
    mongo.db.api.delete_many({})
    status_message = "deleted all."
    print(status_message)
    return status_message


if __name__ == '__main__':
    app.run(debug=True)
