from flask import Flask, request, render_template
import pickle
import numpy as np
import time
import sklearn  

app = Flask(__name__)

# List of valid weather classes
weather_classes = [
    'clear', 'cloudy', 'drizzly', 'foggy', 'hazey',
    'misty', 'rain', 'smokey', 'thunderstorm'
]

# -----------------------------
# Load Model
# -----------------------------
def load_model(model_path='model/model.pkl'):
    with open(model_path, 'rb') as f:
        return pickle.load(f)

# -----------------------------
# Prediction Function
# -----------------------------
def classify_weather(features):
    model = load_model()
    start_time = time.time()

    # Predict class
    prediction_index = model.predict(features)[0]
    prediction = weather_classes[prediction_index]

    # Calculate latency (ms)
    latency = round((time.time() - start_time) * 1000, 2)

    return prediction, latency

# -----------------------------
# MAIN ROUTE
# -----------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Define required fields
            required_fields = [
                'temperature', 'pressure', 'humidity', 'wind_speed',
                'wind_deg', 'rain_1h', 'rain_3h', 'snow', 'clouds'
            ]
            
            # Check if all required fields are present
            missing_fields = [field for field in required_fields if field not in request.form]
            if missing_fields:
                error_msg = f"Missing required fields: {', '.join(missing_fields)}"
                return render_template('form.html', error=error_msg), 200
            
            # Safely extract & convert input values
            features = [
                float(request.form.get('temperature')),
                float(request.form.get('pressure')),
                float(request.form.get('humidity')),
                float(request.form.get('wind_speed')),
                float(request.form.get('wind_deg')),
                float(request.form.get('rain_1h')),
                float(request.form.get('rain_3h')),
                float(request.form.get('snow')),
                float(request.form.get('clouds')),
            ]

            # Prepare for model input
            features = np.array(features).reshape(1, -1)

            # Run model
            prediction, latency = classify_weather(features)

            # Show results
            return render_template(
                'result.html',
                prediction=prediction,
                latency=latency
            )

        except Exception as e:
            # Graceful failure for DevOps logging
            error_msg = f"Error processing input: {e}"
            return render_template('form.html', error=error_msg), 200

    # If GET request → show form
    return render_template('form.html')

# -----------------------------
# Run Flask (if local)
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

