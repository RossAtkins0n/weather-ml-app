import unittest
from app import app


class TestAppSmoke(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # Test that the app runs and returns HTTP 200 on the home page
    def test_prediction_route_success(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # Test that the form is actually rendered on the page
    def test_get_form(self):
        response = self.client.get('/')
        # check that there is a <form> tag in the returned HTML
        self.assertIn(b'<form', response.data)


if __name__ == '__main__':
    unittest.main()

