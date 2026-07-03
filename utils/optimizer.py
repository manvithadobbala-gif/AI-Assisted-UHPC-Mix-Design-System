import numpy as np


def generate_candidate_mix():

    binder = np.random.uniform(700, 1100)

    scm_percent = np.random.uniform(0.15, 0.40)

    scm = binder * scm_percent

    cement = binder - scm

    silica = scm * np.random.uniform(0.20, 0.40)

    flyash = scm * np.random.uniform(0.00, 0.30)

    ggbs = scm - silica - flyash

    wb = np.random.uniform(0.16, 0.22)

    water = binder * wb

    sand = binder * np.random.uniform(0.80, 1.20)

    sp = binder * np.random.uniform(0.02, 0.05)

    fiber = np.random.uniform(120, 180)

    return {

        "Cement Amount  (kg/m³)": round(cement, 2),

        "Silica Fume (kg/m³)": round(silica, 2),

        "Flayash Amount   (kg/m³)": round(flyash, 2),

        "GGBFS  (kg/m³)": round(ggbs, 2),

        "Water (kg/m³)": round(water, 2),

        "Fine Aggregate (kg/m³)": round(sand, 2),

        "Superplasticizer (kg/m³)": round(sp, 2),

        "Amount / Quantity of Fiber": round(fiber, 2),

        "Binder": round(binder, 2),

        "Water_Binder_Ratio": round(wb, 3)

    }
import pandas as pd
from utils.predictor import predict_strength


def generate_top20_mixes(target_strength, n_candidates=500):

    results = []

    for _ in range(n_candidates):

        candidate = generate_candidate_mix()

        strength = predict_strength(candidate)

        candidate["Predicted Strength (MPa)"] = round(strength, 2)

        candidate["Error"] = abs(strength - target_strength)

        results.append(candidate)

    df = pd.DataFrame(results)

    # Engineering Score Components
    df["Cement_Penalty"] = df["Cement Amount  (kg/m³)"] / 1000

    df["WB_Penalty"] = abs(df["Water_Binder_Ratio"] - 0.18)

    df["SP_Penalty"] = df["Superplasticizer (kg/m³)"] / 100

    df["GGBS_Reward"] = -df["GGBFS  (kg/m³)"] / 1000

    # Final Engineering Score
    df["Engineering_Score"] = (

        df["Error"] * 0.50 +

        df["Cement_Penalty"] * 0.20 +

        df["WB_Penalty"] * 0.15 +

        df["SP_Penalty"] * 0.05 +

        df["GGBS_Reward"] * 0.10

    )

    df = df.sort_values("Engineering_Score")

    return df.head(20)