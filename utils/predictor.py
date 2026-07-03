import joblib
import pandas as pd

optimizer_model = joblib.load("models/Optimizer_AI_Model.pkl")


def predict_strength(candidate):


    input_df = pd.DataFrame([candidate])

    print(input_df.columns)

    strength = optimizer_model.predict(input_df)[0]

    return strength

    input_df = pd.DataFrame([candidate])

    print(input_df.columns)

    strength = optimizer_model.predict(input_df)[0]

    print("Prediction Done")

    return strength