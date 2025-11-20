from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load model + imputer
model = joblib.load("disease_model.pkl")
imputer = joblib.load("imputer.pkl")

# Load CSV to extract symptom columns
df = pd.read_csv("Final_Augmented_dataset_Diseases_and_Symptoms.csv")
symptom_columns = list(df.drop("diseases", axis=1).columns)

# Convert column names to lowercase to match frontend inputs more flexibly
symptom_map = {col.lower(): col for col in symptom_columns}


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    symptoms = data.get("symptoms", [])

    # Create zero row
    input_row = {col: 0 for col in symptom_columns}

    # Set selected symptoms = 1
    for s in symptoms:
        s_clean = s.strip().lower()
        if s_clean in symptom_map:  # exact match in lowercase
            col_name = symptom_map[s_clean]
            input_row[col_name] = 1

    # Convert to DataFrame
    input_df = pd.DataFrame([input_row])

    # Apply imputer
    input_df = imputer.transform(input_df)

    # Predict
    prediction = model.predict(input_df)[0]

    # Probabilities
    probs = model.predict_proba(input_df)[0]
    prob_list = [
        {
            "disease": disease,
            "prob": round(prob * 100, 2)
        }
        for disease, prob in zip(model.classes_, probs)
    ]

    return jsonify({
        "prediction": prediction,
        "probabilities": prob_list
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
