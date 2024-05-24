import unittest
import warnings
from api import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

        login_response = self.app.post('/login', json={"username": "company", "password": "company2024"})
        self.access_token = login_response.json['access_token']

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getemployees(self):
        response = self.app.get("/employees", headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Ahmad" in response.data.decode())

    def test_getemployees_by_ssn(self):
        response = self.app.get("/employees/453453453", headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Joyce" in response.data.decode())

    def test_getdependentname_by_essn(self):
        response = self.app.get("/dependents/987654321", headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Abner" in response.data.decode())

    def test_get_essn_hours(self):
        response = self.app.get("/workson/1", headers=self.get_headers())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("123456789" in response.data.decode())


if __name__ == "__main__":
    unittest.main()