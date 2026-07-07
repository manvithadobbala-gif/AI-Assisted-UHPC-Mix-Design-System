import random
import numpy as np
import pandas as pd

from utils.predictor import predict_strength

# ==========================================================
# MATERIAL LIMITS
# ==========================================================

LIMITS = {

    "cement": (600,900),

    "silica": (50,250),

    "ggbs": (0,300),

    "water": (120,180),

    "sand": (700,1100),

    "sp": (10,40),

    "fiber": (120,220)

}

# ==========================================================
# MATERIAL DATABASE
# ==========================================================

MATERIAL_DB = {

    "cement":{"cost":8.5,"co2":0.90},

    "silica":{"cost":35,"co2":0.08},

    "ggbs":{"cost":6,"co2":0.07},

    "water":{"cost":0.05,"co2":0.00},

    "sand":{"cost":1.5,"co2":0.005},

    "sp":{"cost":120,"co2":1.50},

    "fiber":{"cost":95,"co2":2.20}

}

# ==========================================================
# PARTICLE
# ==========================================================

class Particle:

    def __init__(self):

        self.position={

            "cement":random.uniform(*LIMITS["cement"]),

            "silica":random.uniform(*LIMITS["silica"]),

            "ggbs":random.uniform(*LIMITS["ggbs"]),

            "water":random.uniform(*LIMITS["water"]),

            "sand":random.uniform(*LIMITS["sand"]),

            "sp":random.uniform(*LIMITS["sp"]),

            "fiber":random.uniform(*LIMITS["fiber"])

        }

        self.velocity={k:0 for k in self.position}

        self.best_position=self.position.copy()

        self.best_score=-999999
# ==========================================================
# FITNESS FUNCTION
# ==========================================================

def fitness(position, target_strength, design_objective):

    candidate = {

        "Cement Amount  (kg/m³)": position["cement"],

        "Silica Fume (kg/m³)": position["silica"],

        "Flayash Amount   (kg/m³)": 0,

        "GGBFS  (kg/m³)": position["ggbs"],

        "Water (kg/m³)": position["water"],

        "Fine Aggregate (kg/m³)": position["sand"],

        "Superplasticizer (kg/m³)": position["sp"],

        "Amount / Quantity of Fiber": position["fiber"]

    }

    binder = (

        position["cement"]

        + position["silica"]

        + position["ggbs"]

    )

    candidate["Binder"] = binder

    candidate["Water_Binder_Ratio"] = (

        position["water"] / binder

    )

    # ---------------------------------------
    # AI Prediction
    # ---------------------------------------

    strength = predict_strength(candidate)

    # ---------------------------------------
    # Strength Score
    # ---------------------------------------

    strength_score = max(

        0,

        100 - abs(strength - target_strength)

    )

    # ---------------------------------------
    # Engineering Score
    # ---------------------------------------

    engineering_score = 100

    wb = candidate["Water_Binder_Ratio"]

    # ---------------------------------------
    # Water–Binder Ratio
    # ---------------------------------------

    if wb > 0.20:
        engineering_score -= 20
    elif wb > 0.18:
        engineering_score -= 10

    # ---------------------------------------
    # Total Binder Content
    # ---------------------------------------

    if binder < 800:
        engineering_score -= 15
    elif binder > 1100:
        engineering_score -= 10

    # ---------------------------------------
    # Cement Content
    # ---------------------------------------

    if position["cement"] < 600:
        engineering_score -= 20

    # ---------------------------------------
    # Silica Fume Content
    # ---------------------------------------

    if position["silica"] < 50:
        engineering_score -= 10

    elif position["silica"] > 250:
        engineering_score -= 5

    # ---------------------------------------
    # Steel Fibre
    # ---------------------------------------

    if position["fiber"] < 120:
        engineering_score -= 10

    elif position["fiber"] > 220:
        engineering_score -= 5

    # ---------------------------------------
    # Fine Aggregate
    # ---------------------------------------

    if position["sand"] < 700:
        engineering_score -= 5

    elif position["sand"] > 1100:
        engineering_score -= 5

    # ---------------------------------------
    # Cost
    # ---------------------------------------

    cost = (

        position["cement"]*MATERIAL_DB["cement"]["cost"]

        + position["silica"]*MATERIAL_DB["silica"]["cost"]

        + position["ggbs"]*MATERIAL_DB["ggbs"]["cost"]

        + position["water"]*MATERIAL_DB["water"]["cost"]

        + position["sand"]*MATERIAL_DB["sand"]["cost"]

        + position["sp"]*MATERIAL_DB["sp"]["cost"]

        + position["fiber"]*MATERIAL_DB["fiber"]["cost"]

    )

    cost_score = max(

        0,

        100 - cost/100

    )

    # ---------------------------------------
    # CO₂
    # ---------------------------------------

    co2 = (

        position["cement"]*MATERIAL_DB["cement"]["co2"]

        + position["silica"]*MATERIAL_DB["silica"]["co2"]

        + position["ggbs"]*MATERIAL_DB["ggbs"]["co2"]

        + position["water"]*MATERIAL_DB["water"]["co2"]

        + position["sand"]*MATERIAL_DB["sand"]["co2"]

        + position["sp"]*MATERIAL_DB["sp"]["co2"]

        + position["fiber"]*MATERIAL_DB["fiber"]["co2"]

    )

    co2_score = max(

        0,

        100 - co2/10

    )

    # ---------------------------------------
    # DESIGN OBJECTIVE
    # ---------------------------------------

    if design_objective == "⭐ Balanced Design (Recommended)":

        fitness_score = (
            0.35 * strength_score +
            0.30 * engineering_score +
            0.20 * cost_score +
            0.15 * co2_score
        )

    elif design_objective == "💰 Minimize Cost":

        fitness_score = (
            0.25 * strength_score +
            0.25 * engineering_score +
            0.40 * cost_score +
            0.10 * co2_score
        )

    elif design_objective == "🌱 Minimize Carbon Footprint":

        fitness_score = (
            0.25 * strength_score +
            0.25 * engineering_score +
            0.10 * cost_score +
            0.40 * co2_score
        )

    elif design_objective == "💪 Maximize Strength":

        fitness_score = (
            0.60 * strength_score +
            0.20 * engineering_score +
            0.10 * cost_score +
            0.10 * co2_score
        )

    elif design_objective == "🏗️ Maximize Practicality":

        fitness_score = (
            0.25 * strength_score +
            0.55 * engineering_score +
            0.10 * cost_score +
            0.10 * co2_score
        )

    else:
        fitness_score = (
            0.35 * strength_score +
            0.30 * engineering_score +
            0.20 * cost_score +
            0.15 * co2_score
        )
    return fitness_score, strength
# ==========================================================
# PARTICLE SWARM OPTIMIZATION
# ==========================================================

def pso_optimize(
    target_strength,
    design_objective,
    swarm_size=40,
    iterations=50
):

    # PSO Constants
    w = 0.7
    c1 = 1.5
    c2 = 1.5

    # Create Swarm
    swarm = [Particle() for _ in range(swarm_size)]

    global_best_position = None
    global_best_score = -999999
    # -----------------------------------------
    # Initial Evaluation
    # -----------------------------------------

    for particle in swarm:

        score, strength = fitness(
           particle.position,
           target_strength,
           design_objective
        )

        particle.best_score = score
        particle.best_position = particle.position.copy()

        if score > global_best_score:

            global_best_score = score
            global_best_position = particle.position.copy()
    # -----------------------------------------
    # Optimization Loop
    # -----------------------------------------

    for iteration in range(iterations):

        for particle in swarm:

            for key in particle.position:

                r1 = random.random()
                r2 = random.random()

                particle.velocity[key] = (

                    w * particle.velocity[key]

                    + c1 * r1 *

                    (particle.best_position[key] - particle.position[key])

                    + c2 * r2 *

                    (global_best_position[key] - particle.position[key])

                )

                particle.position[key] += particle.velocity[key]
                                      # -----------------------------------------
            # Clamp Limits
            # -----------------------------------------

            particle.position["cement"] = np.clip(
                particle.position["cement"],
                *LIMITS["cement"]
            )

            particle.position["silica"] = np.clip(
                particle.position["silica"],
                *LIMITS["silica"]
            )

            particle.position["ggbs"] = np.clip(
                particle.position["ggbs"],
                *LIMITS["ggbs"]
            )

            particle.position["water"] = np.clip(
                particle.position["water"],
                *LIMITS["water"]
            )

            particle.position["sand"] = np.clip(
                particle.position["sand"],
                *LIMITS["sand"]
            )

            particle.position["sp"] = np.clip(
                particle.position["sp"],
                *LIMITS["sp"]
            )

            particle.position["fiber"] = np.clip(
                particle.position["fiber"],
                *LIMITS["fiber"]
            )

            score, strength = fitness(
              particle.position,
              target_strength,
              design_objective
            )

            if score > particle.best_score:

                particle.best_score = score
                particle.best_position = particle.position.copy()

            if score > global_best_score:

                global_best_score = score
                global_best_position = particle.position.copy()
    # -----------------------------------------
    # Create Results DataFrame
    # -----------------------------------------

    results = []

    for particle in swarm:

        score, strength = fitness(
           particle.position,
           target_strength,
           design_objective
        )

        results.append({

            "Predicted Strength": round(strength, 2),

            "Fitness": round(score, 2),

            "Cement": round(particle.position["cement"], 2),

            "Silica Fume": round(particle.position["silica"], 2),

            "GGBS": round(particle.position["ggbs"], 2),

            "Water": round(particle.position["water"], 2),

            "Fine Aggregate": round(particle.position["sand"], 2),

            "Superplasticizer": round(particle.position["sp"], 2),

            "Steel Fiber": round(particle.position["fiber"], 2)

        })

    df = pd.DataFrame(results)

    df = df.sort_values(
        "Fitness",
        ascending=False
    )

    return df.head(20).reset_index(drop=True)                