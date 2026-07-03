import pandas as pd


def engineering_validation(mix):

    report = []
    score = 100

    binder = (
        mix["Cement"]
        + mix["Silica Fume"]
        + mix["GGBS"]
    )

    water = mix["Water"]
    wb = water / binder

    if 0.15 <= wb <= 0.22:
        report.append(("Water/Binder Ratio", "PASS", round(wb, 3)))
    else:
        report.append(("Water/Binder Ratio", "FAIL", round(wb, 3)))
        score -= 20

    if binder >= 800:
        report.append(("Binder Content", "PASS", round(binder, 1)))
    else:
        report.append(("Binder Content", "FAIL", round(binder, 1)))
        score -= 20

    if 120 <= mix["Steel Fiber"] <= 180:
        report.append(("Steel Fiber", "PASS", round(mix["Steel Fiber"], 1)))
    else:
        report.append(("Steel Fiber", "FAIL", round(mix["Steel Fiber"], 1)))
        score -= 15

    if 10 <= mix["Superplasticizer"] <= 35:
        report.append(("Superplasticizer", "PASS", round(mix["Superplasticizer"], 1)))
    else:
        report.append(("Superplasticizer", "FAIL", round(mix["Superplasticizer"], 1)))
        score -= 15

    if 700 <= mix["Fine Aggregate"] <= 1100:
        report.append(("Fine Aggregate", "PASS", round(mix["Fine Aggregate"], 1)))
    else:
        report.append(("Fine Aggregate", "FAIL", round(mix["Fine Aggregate"], 1)))
        score -= 10

    validation = pd.DataFrame(
        report,
        columns=["Parameter", "Status", "Value"]
    )

    return validation, score


def estimate_cost_co2(mix):

    cost = (
        mix["Cement"] * 8.5 +
        mix["Silica Fume"] * 35 +
        mix["GGBS"] * 6 +
        mix["Water"] * 0.05 +
        mix["Fine Aggregate"] * 1.5 +
        mix["Superplasticizer"] * 120 +
        mix["Steel Fiber"] * 95
    )

    co2 = (
        mix["Cement"] * 0.90 +
        mix["Silica Fume"] * 0.08 +
        mix["GGBS"] * 0.07 +
        mix["Water"] * 0 +
        mix["Fine Aggregate"] * 0.005 +
        mix["Superplasticizer"] * 1.50 +
        mix["Steel Fiber"] * 2.20
    )

    return cost, co2