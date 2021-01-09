import json
from covidWarnApp import create_app
import unittest


class FlaskTest(unittest.TestCase):

    def test_index(self):
        tester = create_app().test_client(self)
        response = tester.get("/")
        status_code = response.status_code

        # Check for response 200
        self.assertEqual(status_code, 200)

    def test_health(self):
        tester = create_app().test_client(self)
        response = tester.get("/health")
        status_code = response.status_code
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['status'], "UP")
        # Check for response 200
        self.assertEqual(status_code, 200)
