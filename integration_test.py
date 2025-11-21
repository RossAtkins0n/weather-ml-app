import unittest
from app import app  # Import your Flask app instance


class TestModelAppIntegration(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_model_app_integration(self):
        # Valid test input that should work with the trained model / route
        form_data = {
            'temperature': '275.15',   # Kelvin
            'pressure': '1013',        # hPa
            'humidity': '85',          # %
            'wind_speed': '3.6',       # m/s
            'wind_deg': '180',         # degrees
            'rain_1h': '0',            # mm
            'rain_3h': '0',            # mm
            'snow': '0',               # mm
            'clouds': '20'             # %
        }

        response = self.client.post('/', data=form_data)

        # 1) App should respond without crashing
        self.assertEqual(response.status_code, 200)

        # 2) Decode HTML so we can search it
        html_text = response.data.decode('utf-8').lower()

        # 3) Make sure we got the main page with the form + heading
        #    This proves the Flask route, template and form are wired together.
        self.assertIn("weather classification", html_text)
        self.assertIn("<form", html_text)


if __name__ == '__main__':
    unittest.main()

