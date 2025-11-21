import unittest
import numpy as np

from app import app, classify_weather, load_model, weather_classes


class TestUnit(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # -----------------------------
    # 1) Missing field in POST data
    # -----------------------------
    def test_post_missing_field(self):
        """App should handle missing fields without crashing."""
        form_data = {
            "temperature": "270.277",
            "pressure": "1006",
            "humidity": "84",
            # wind_speed is deliberately missing
            "wind_deg": "274",
            "rain_1h": "0",
            "rain_3h": "0",
            "snow": "0",
            "clouds": "9",
        }

        response = self.client.post("/", data=form_data)

        # App should not return 500
        self.assertEqual(response.status_code, 200)
        # And should still render the form page
        self.assertIn(b"<form", response.data)

    # -----------------------------
    # 2) Model can be loaded
    # -----------------------------
    def test_model_can_be_loaded(self):
        """Model should load successfully from disk."""
        model = load_model()
        self.assertIsNotNone(model)
        # basic sanity check – model should have predict method
        self.assertTrue(hasattr(model, "predict"))

    # -------------------------------------------------------
    # 3) Classification output should be one of 9 valid classes
    #    (different inputs for clear / rainy / cloudy cases)
    # -------------------------------------------------------
    def test_clear_classification_output(self):
        """Prediction for a 'clear'-type input should be a valid class."""
        test_input = np.array([269.686, 1002, 78, 0, 23, 0, 0, 0, 0]).reshape(1, -1)
        class_result, _ = classify_weather(test_input)
        # Just ensure the result is one of the known weather classes
        self.assertIn(class_result, weather_classes)

    def test_rainy_classification_output(self):
        """Prediction for a 'rainy'-type input should be a valid class."""
        test_input = np.array([279.626, 998, 99, 1, 314, 0.3, 0, 0, 88]).reshape(1, -1)
        class_result, _ = classify_weather(test_input)
        self.assertIn(class_result, weather_classes)

    def test_cloudy_classification_output(self):
        """
        Use the cloudy array from the lecturer’s email:
        [291.15, 1028, 61, 1, 260, 0, 0, 0, 75]
        """
        test_input = np.array([291.15, 1028, 61, 1, 260, 0, 0, 0, 75]).reshape(1, -1)
        class_result, _ = classify_weather(test_input)
        self.assertIn(class_result, weather_classes)


if __name__ == "__main__":
    unittest.main()

