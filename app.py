from flask import Flask, request, render_template
import pickle
import numpy as np
import time
import sklearn  # Required for unpickling scikit-learn models

app = Flask(__name__)

# List of valid weather classes
weather_classes = [
    'clear', 'cloudy', 'drizzly', 'foggy', 'hazey',
    'misty', 'rainy', 'smokey', 'thunderstorm'
]

# -----------------------------
# Load Model
# -----------------------------
def load_model(model_path='model/model.pkl'):
    return pickle.load(open(model_path, 'rb'))

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
            # Safely extract & convert input values
            features = [
                float(request.form.get('temperature', 0)),
                float(request.form.get('pressure', 0)),
                float(request.form.get('humidity', 0)),
                float(request.form.get('wind_speed', 0)),
                float(request.form.get('wind_deg', 0)),
                float(request.form.get('rain_1h', 0)),
                float(request.form.get('rain_3h', 0)),
                float(request.form.get('snow', 0)),
                float(request.form.get('clouds', 0)),
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

