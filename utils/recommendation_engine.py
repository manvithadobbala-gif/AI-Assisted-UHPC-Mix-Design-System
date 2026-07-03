import pandas as pd
from utils.engineering_validation import (
    engineering_validation,
    estimate_cost_co2
)

def generate_recommendations(results):

    df = results.copy()

    engineering_scores = []
    costs = []
    co2s = []

    for _, mix in df.iterrows():

        _, score = engineering_validation(mix)

        cost, co2 = estimate_cost_co2(mix)

        engineering_scores.append(score)

        costs.append(cost)

        co2s.append(co2)

    df["Engineering Score"] = engineering_scores
    df["Estimated Cost"] = costs
    df["Estimated CO2"] = co2s

    recommendations = []

    # ⭐ Balanced Design
    balanced = df.sort_values(
        "Fitness",
        ascending=False
    ).iloc[0].copy()

    balanced["Recommendation"] = "⭐ Balanced Design"

    recommendations.append(balanced)

    # 💰 Economical Design
    economical = df.sort_values(
        "Estimated Cost",
        ascending=True
    ).iloc[0].copy()

    economical["Recommendation"] = "💰 Economical Design"

    recommendations.append(economical)

    # 🌱 Sustainable Design
    sustainable = df.sort_values(
        "Estimated CO2",
        ascending=True
    ).iloc[0].copy()

    sustainable["Recommendation"] = "🌱 Sustainable Design"

    recommendations.append(sustainable)

    # 💪 High Performance
    strongest = df.sort_values(
        "Predicted Strength",
        ascending=False
    ).iloc[0].copy()

    strongest["Recommendation"] = "💪 High Performance"

    recommendations.append(strongest)

    # 🏗 Practical Design
    practical = df.sort_values(
        "Engineering Score",
        ascending=False
    ).iloc[0].copy()

    practical["Recommendation"] = "🏗 Practical Design"

    recommendations.append(practical)

    recommendations = pd.DataFrame(recommendations)

    recommendations = recommendations.drop_duplicates()

    recommendations.reset_index(
        drop=True,
        inplace=True
    )

    return recommendations
