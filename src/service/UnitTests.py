import unittest
import requests
import json

base_url = url = 'http://127.0.0.1:5000/'
test_endpoint = base_url + 'test'
training_endpoint = base_url + 'train'
run_test_endpoint = base_url + 'test/run'


class Test(unittest.TestCase):
    def test_can_get_results(self):
        response = requests.get(test_endpoint)
        print response.json
        self.assertEquals(response.status_code, 200)
        data = json.dumps(response.json())
        responses = json.loads(data)
        self.assertGreater(len(responses), 0)
        self.assertGreater(responses[0]['Status'], -1)

    def test_can_run_training(self):
        status = 0
        name = 2
        environment = 3
        type = 4
        code = 4
        data = str.format("?status={0}&name={1}&environment={2}&type={3}&code={4}",
                          status,
                          name,
                          environment,
                          type,
                          code)

        response = requests.get(training_endpoint + data)
        self.assertEquals(response.status_code, 200)

    def test_can_run_test(self):
        status = 0
        name = 2
        environment = 3
        type = 4
        code = 4
        data = str.format("?status={0}&name={1}&environment={2}&type={3}&code={4}",
                          status,
                          name,
                          environment,
                          type,
                          code)

        response = requests.get(training_endpoint + data)
        self.assertEquals(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

