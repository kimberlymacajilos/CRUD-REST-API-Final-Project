import unittest
import warnings
from api import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getemployees(self):
        response = self.app.get("/employees")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Ahmad" in response.data.decode())

    def test_getemployees_by_ssn(self):
        response = self.app.get("/employees/639639639")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Wolfgang" in response.data.decode())

    def test_getdependentname_by_essn(self):
        response = self.app.get("/dependents/987654321")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Abner" in response.data.decode())


if __name__ == "__main__":
    unittest.main()