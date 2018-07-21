import unittest
import requests
import json

base_url = url = 'http://127.0.0.1:5000/'
test_endpoint = base_url + 'test'
training_endpoint = base_url + 'train'
run_test_endpoint = base_url + 'test/run'
delete_endpoint = base_url + 'test/delete'
random_training_endpoint = base_url + 'train/random'
actual_result_endpoint = base_url + 'test/validate'


# name, environment, type, code
def get_low_value_input():
    return 0, 0, 2, 3


# name, environment, type, code
def get_mid_value_input():
    return 5, 5, 5, 0


def get_high_value_input():
    return 0, 1, 0, 5


def train_tensortest_with_random_data():
    response = requests.get(random_training_endpoint)
    data = json.dumps(response.json())
    result = json.loads(data)
    print result


def reset_all_training_data():
    requests.get(delete_endpoint)


def build_data(name, environment, typ, code):
    return str.format("?name={0}&environment={1}&type={2}&code={3}",
                      name,
                      environment,
                      typ,
                      code)


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        train_tensortest_with_random_data()

    # def test_run_single_training(self):
    #     name, environment, type, code = get_high_value_input()
    #     data = str.format("?name={0}&environment={1}&type={2}&code={3}",
    #                       name,
    #                       environment,
    #                       type,
    #                       code)
    #     response = requests.get(training_endpoint + data)
    #     self.assertEquals(response.status_code, 200)

    def get_actual_result(self, name, environment, typ, code, expected):
        data = build_data(name, environment, typ, code)

        response = requests.get(actual_result_endpoint + data)
        self.assertEquals(response.status_code, 200)

        data = json.dumps(response.json())
        result = json.loads(data)
        print result
        self.assertEquals(result['status'], expected)

    def run_test(self, name, environment, typ, code, expected_result):
        data = build_data(name, environment, typ, code)

        response = requests.get(run_test_endpoint + data)
        self.assertEquals(response.status_code, 200)

        data = json.dumps(response.json())
        result = json.loads(data)
        print result
        self.assertEquals(result['prediction'], expected_result)
        self.assertGreater(result['probability'], 0)
        self.assertGreater(result['accuracy'], 70)

    def test_can_get_results(self):
        response = requests.get(test_endpoint)
        self.assertEquals(response.status_code, 200)
        data = json.dumps(response.json())
        responses = json.loads(data)
        self.assertGreater(len(responses), 0)
        self.assertGreater(responses[0]['Status'], -1)

    def test_can_identify_high_value_inputs(self):
        name, environment, typ, code = get_high_value_input()
        expected = 'high value'
        self.run_test(name, environment, typ, code, expected)

    def test_can_identify_mid_value_inputs(self):
        name, environment, typ, code = get_mid_value_input()
        expected = 'mid value'
        self.run_test(name, environment, typ, code, expected)

    def test_can_identify_low_value_inputs(self):
        name, environment, typ, code = get_low_value_input()
        expected = 'low value'
        self.run_test(name, environment, typ, code, expected)

    def test_can_get_actual_value_for_high_value(self):
        name, environment, typ, code = get_low_value_input()
        expected = 0
        self.get_actual_result(name, environment, typ, code, expected)

    def test_can_get_actual_value_for_mid_value(self):
        name, environment, typ, code = get_mid_value_input()
        expected = 1
        self.get_actual_result(name, environment, typ, code, expected)

    def test_can_get_actual_value_for_low_value(self):
        name, environment, typ, code = get_high_value_input()
        expected = 2
        self.get_actual_result(name, environment, typ, code, expected)

    @classmethod
    def tearDownClass(cls):
        reset_all_training_data()


if __name__ == '__main__':
    unittest.main()

