from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

# ------------------ Load the trained model ------------------
with open("wqi_model_rf.pkl", "rb") as f:
    model = pickle.load(f)

# ------------------ Flask app setup ------------------
app = Flask(__name__)

# Optional helper: categorize WQI
def get_water_quality_category(wqi):
    if wqi >= 80:
        return "Excellent", "Safe for drinking and all uses"
    elif wqi >= 60:
        return "Good", "Acceptable quality, minor treatment needed"
    elif wqi >= 40:
        return "Moderate", "Needs treatment before use"
    else:
        return "Poor", "Unsafe, high risk of waterborne diseases"

# ------------------ API endpoint ------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        tds = float(data.get("tds"))
        ph = float(data.get("ph"))
        turbidity = float(data.get("turbidity"))

        features = np.array([[tds, ph, turbidity]])
        wqi = model.predict(features)[0]

        category, description = get_water_quality_category(wqi)

        result = {
            "wqi_score": round(wqi, 2),
            "quality_category": category,
            "description": description,
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ------------------ Run the server ------------------
if __name__ == "__main__":
    app.run(debug=True)
