import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
import joblib

# Load dataset
df = pd.read_csv("Final_Augmented_dataset_Diseases_and_Symptoms.csv")

# Features and target
X = df.drop("diseases", axis=1)
y = df["diseases"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Imputer (fills missing values)
imputer = SimpleImputer(strategy="mean")
X_train_imputed = imputer.fit_transform(X_train)

# Train model
model = LogisticRegression(max_iter=2000)
model.fit(X_train_imputed, y_train)

# Save model + imputer
joblib.dump(model, "disease_model.pkl")
joblib.dump(imputer, "imputer.pkl")

print("✔️ Model and imputer saved successfully!")
print("Files created:")
print(" - disease_model.pkl")
print(" - imputer.pkl")
