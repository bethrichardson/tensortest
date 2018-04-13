#  Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

import api_data

BATCH_SIZE = 100
TRAIN_STEPS = 1000


def run_training(training_data):
    # Fetch the data
    (train_x, train_y), (test_x, test_y) = api_data.load_data(training_data)

    # Feature columns describe how to use the input.
    my_feature_columns = []
    for key in train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))

    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 10 nodes each.
        hidden_units=[10, 10],
        # The model must choose between 3 classes.
        n_classes=3)

    print(my_feature_columns)

    # Train the Model.
    classifier.train(
        input_fn=lambda: api_data.train_input_fn(train_x, train_y,
                                                 BATCH_SIZE),
        steps=TRAIN_STEPS)

    # Evaluate the model.
    eval_result = classifier.evaluate(
        input_fn=lambda: api_data.eval_input_fn(test_x, test_y,
                                                BATCH_SIZE))

    print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))
    print(classifier.config)
    feature_spec = tf.feature_column.make_parse_example_spec(my_feature_columns)
    classifier.export_savedmodel('./saved_models', tf.estimator.export.build_parsing_serving_input_receiver_fn(
        feature_spec))
    print("COMPLETED SAVE")
    # features=features,
    #       labels=labels,
    #       mode=mode,
    #       head=head,
    #       hidden_units=hidden_units,
    #       feature_columns=tuple(feature_columns or []),
    #       optimizer=optimizer,
    #       activation_fn=activation_fn,
    #       dropout=dropout,
    #       input_layer_partitioner=input_layer_partitioner,
    #       config=config
    return classifier


def run_test(test_value, expected, training_data):
    classifier = run_training(training_data)
    # Generate predictions from the model
    predict_x = test_value

    predictions = classifier.predict(
        input_fn=lambda: api_data.eval_input_fn(predict_x,
                                                labels=None,
                                                batch_size=BATCH_SIZE))

    for pred_dict, expec in zip(predictions, expected):
        template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')

        class_id = pred_dict['class_ids'][0]
        probability = pred_dict['probabilities'][class_id]

        print(template.format(api_data.SPECIES[class_id],
                              100 * probability, expec))

        return api_data.SPECIES[class_id], 100 * probability, expec
