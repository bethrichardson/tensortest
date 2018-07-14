import unittest
import requests
import json

base_url = url = 'http://127.0.0.1:5000/'
test_endpoint = base_url + 'test'
training_endpoint = base_url + 'train'
run_test_endpoint = base_url + 'test/run'
delete_endpoint = base_url + 'test/delete'


def get_low_value_input():
    return 0, 1, 0, 1


def get_mid_value_input():
    return 5, 1, 0, 0


def get_high_value_input():
    return 5, 1, 0, 1


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        name, environment, type, code = get_high_value_input()
        data = str.format("?name={0}&environment={1}&type={2}&code={3}",
                          name,
                          environment,
                          type,
                          code)
        for i in range(1, 5):
            requests.get(training_endpoint + data)

        name, environment, type, code = get_mid_value_input()
        data = str.format("?name={0}&environment={1}&type={2}&code={3}",
                          name,
                          environment,
                          type,
                          code)
        for i in range(1, 5):
            requests.get(training_endpoint + data)

        name, environment, type, code = get_low_value_input()
        data = str.format("?name={0}&environment={1}&type={2}&code={3}",
                          name,
                          environment,
                          type,
                          code)
        for i in range(1, 5):
            requests.get(training_endpoint + data)

    def test_run_training(self):
        name, environment, type, code = get_high_value_input()
        data = str.format("?name={0}&environment={1}&type={2}&code={3}",
                          name,
                          environment,
                          type,
                          code)
        response = requests.get(training_endpoint + data)
        self.assertEquals(response.status_code, 200)

    def test_can_get_results(self):
        response = requests.get(test_endpoint)
        self.assertEquals(response.status_code, 200)
        data = json.dumps(response.json())
        responses = json.loads(data)
        print responses
        self.assertGreater(len(responses), 0)
        self.assertGreater(responses[0]['Status'], -1)

    def test_can_identify_high_value_inputs(self):
        name, environment, type, code = get_high_value_input()
        data = str.format("?name={0}&environment={1}&type={2}&code={3}",
                          name,
                          environment,
                          type,
                          code)

        response = requests.get(run_test_endpoint + data)
        self.assertEquals(response.status_code, 200)

        data = json.dumps(response.json())
        result = json.loads(data)
        self.assertEquals(result['prediction'], 'high value')
        self.assertGreater(result['probability'], 0)

    def test_can_identify_mid_value_inputs(self):
        name, environment, type, code = get_mid_value_input()
        data = str.format("?name={0}&environment={1}&type={2}&code={3}",
                          name,
                          environment,
                          type,
                          code)

        response = requests.get(run_test_endpoint + data)
        self.assertEquals(response.status_code, 200)

        data = json.dumps(response.json())
        result = json.loads(data)
        self.assertEquals(result['prediction'], 'mid value')
        self.assertGreater(result['probability'], 0)

    def test_can_identify_low_value_inputs(self):
        name, environment, type, code = get_low_value_input()
        data = str.format("?name={0}&environment={1}&type={2}&code={3}",
                          name,
                          environment,
                          type,
                          code)

        response = requests.get(run_test_endpoint + data)
        self.assertEquals(response.status_code, 200)

        data = json.dumps(response.json())
        result = json.loads(data)
        self.assertEquals(result['prediction'], 'low value')
        self.assertGreater(result['probability'], 0)

    @classmethod
    def tearDownClass(cls):
        requests.get(delete_endpoint)


if __name__ == '__main__':
    unittest.main()

