import unittest
import requests
import json


BASE_URL = 'http://localhost:8000/api/v1'


VALID_PERSON_DATA = {
    "name": "AAA",
    "age": 12,
    "work": "BBB",
    "address": "CCC"
}


INVALID_PERSON_DATA = {
    "work": "BBB",
    "address": "CCC"
}
PERSON_ID = 2


class ApiTest(unittest.TestCase):

    def test_insert_person(self):
        headers = {'Content-Type': 'application/json'}

        response = requests.post(
            BASE_URL + "/persons", json.dumps(VALID_PERSON_DATA), headers=headers)

        self.assertEqual(response.status_code, 201, "wrong response status")
        location = response.headers.get('Location')
        self.assertTrue(location.startswith('/api/v1/persons'))

        response = requests.post(
            BASE_URL + "/persons", json.dumps(INVALID_PERSON_DATA), headers=headers)

        self.assertEqual(response.status_code, 400)

    def test_get_persons(self):
        headers = {'Content-Type': 'application/json'}
        response = requests.get(BASE_URL + f"/persons", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list,
                              "GET persons is not an array")

    def test_patch_person(self):
        headers = {'Content-Type': 'application/json'}

        response = requests.patch(
            BASE_URL + f"/persons/{PERSON_ID}", json.dumps(VALID_PERSON_DATA), headers=headers)

        self.assertEqual(response.status_code, 200)

        response_1 = requests.get(
            BASE_URL + f"/persons/{PERSON_ID}", headers=headers)

        person_1 = response_1.json()

        self.assertEqual(person_1["name"], VALID_PERSON_DATA["name"])
        self.assertEqual(person_1["work"], VALID_PERSON_DATA["work"])


if __name__ == '__main__':
    unittest.main()
