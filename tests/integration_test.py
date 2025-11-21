import unittest
from app import app

class TestModelAppIntegration(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_model_app_integration(self):
        form_data = {
            'temperature': '275.15',
            'pressure': '1013',
            'humidity': '85',
            'wind_speed': '3.6',
            'wind_deg': '180',
            'rain_1h': '0',
            'rain_3h': '0',
            'snow': '0',
            'clouds': '20'
        }

        response = self.client.post('/', data=form_data)
        html_text = response.data.decode('utf-8').lower()

        # App responds OK
        self.assertEqual(response.status_code, 200)
        # Main page rendered correctly
        self.assertIn("weather classification", html_text)
        self.assertIn("<form", html_text)

if __name__ == '__main__':
    unittest.main()

