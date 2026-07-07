import random
import numpy as np
import pandas as pd

from utils.predictor import predict_strength

# ==========================================================
# MATERIAL LIMITS (Engineering-Based)
# ==========================================================

LIMITS = {

    # Typical UHPC cement content
    "cement": (600, 900),

    # Silica fume improves packing and strength
    "silica": (50, 250),

    # GGBFS as supplementary cementitious material
    "ggbs": (0, 300),

    # Practical UHPC water content
    "water": (120, 180),

    # Fine aggregate
    "sand": (700, 1100),

    # High-range water reducer
    "sp": (10, 40),

    # Steel fibre dosage
    "fiber": (120, 220)

}

# ==========================================================
# FITNESS WEIGHTS
# ==========================================================
FITNESS_WEIGHTS = {

    "strength":0.45,

    "engineering":0.20,

    "cost":0.15,

    "co2":0.15,


}
# ==========================================================
# MATERIAL DATABASE
# Representative Indian Market Prices and Literature-Based
# CO₂ Emission Factors
# ==========================================================

MATERIAL_DB = {

    "cement": {
        "cost": 8.5,
        "co2": 0.90
    },

    "silica": {
        "cost": 28.0,
        "co2": 0.03
    },

    "ggbs": {
        "cost": 5.0,
        "co2": 0.07
    },

    "water": {
        "cost": 0.05,
        "co2": 0.00
    },

    "sand": {
        "cost": 1.2,
        "co2": 0.005
    },

    "sp": {
        "cost": 180.0,
        "co2": 2.50
    },

    "fiber": {
        "cost": 130.0,
        "co2": 1.90
    }

}
# ==========================================================
# CREATE ONE FEASIBLE MIX
# ==========================================================

def generate_individual():

    cement = random.uniform(*LIMITS["cement"])

    silica = random.uniform(*LIMITS["silica"])

    ggbs = random.uniform(*LIMITS["ggbs"])

    water = random.uniform(*LIMITS["water"])

    sand = random.uniform(*LIMITS["sand"])

    sp = random.uniform(*LIMITS["sp"])

    fiber = random.uniform(*LIMITS["fiber"])

    binder = cement + silica + ggbs

    wb = water / binder

    # Keep generating until W/B is feasible
    while wb < 0.16 or wb > 0.22:

        water = random.uniform(*LIMITS["water"])

        binder = cement + silica + ggbs

        wb = water / binder

    return {

        "Cement Amount  (kg/m³)": cement,

        "Silica Fume (kg/m³)": silica,

        "Flayash Amount   (kg/m³)": 0,

        "GGBFS  (kg/m³)": ggbs,

        "Water (kg/m³)": water,

        "Fine Aggregate (kg/m³)": sand,

        "Superplasticizer (kg/m³)": sp,

        "Amount / Quantity of Fiber": fiber,

        "Binder": binder,

        "Water_Binder_Ratio": wb

    }
# ==========================================================
# FITNESS FUNCTION
# ==========================================================

def fitness(

    individual,

    target_strength,

    min_cost,

    max_cost,

    min_co2,

    max_co2

):

    # ------------------------------------------------------
    # Predict Strength
    # ------------------------------------------------------

    strength = predict_strength(individual)

    # ------------------------------------------------------
    # Engineering Parameters
    # ------------------------------------------------------

    engineering_score = calculate_engineering_score(individual)

    cost = calculate_cost(individual)

    co2 = calculate_co2(individual)

    wb = individual["Water_Binder_Ratio"]

    # ------------------------------------------------------
    # Strength Score
    # ------------------------------------------------------

    strength_error = abs(strength - target_strength)

    strength_score = max(0,100-strength_error)

    # ------------------------------------------------------
    # Cost Score
    # ------------------------------------------------------

    cost_score = normalize(

    cost,

    min_cost,

    max_cost,

    reverse=True

)

    # ------------------------------------------------------
    # CO₂ Score
    # ------------------------------------------------------

    co2_score = normalize(

    co2,

    min_co2,

    max_co2,

    reverse=True

)
    # ------------------------------------------------------
    #    Final Fitness
    # ------------------------------------------------------

    total_score = (

        FITNESS_WEIGHTS["strength"] * strength_score +

        FITNESS_WEIGHTS["engineering"] * engineering_score +

        FITNESS_WEIGHTS["cost"] * cost_score +

        FITNESS_WEIGHTS["co2"] * co2_score

)

    # ------------------------------------------------------
    # Save Everything
    # ------------------------------------------------------

    individual["Predicted Strength (MPa)"] = strength

    individual["Engineering Score"] = engineering_score

    individual["Cost"] = cost

    individual["CO2"] = co2

    individual["Fitness"] = total_score

    return individual
# ==========================================================
# COST FUNCTION
# ==========================================================

def calculate_cost(individual):

    cost = (

        individual["Cement Amount  (kg/m³)"] * MATERIAL_DB["cement"]["cost"]

        + individual["Silica Fume (kg/m³)"] * MATERIAL_DB["silica"]["cost"]

        + individual["GGBFS  (kg/m³)"] * MATERIAL_DB["ggbs"]["cost"]

        + individual["Water (kg/m³)"] * MATERIAL_DB["water"]["cost"]

        + individual["Fine Aggregate (kg/m³)"] * MATERIAL_DB["sand"]["cost"]

        + individual["Superplasticizer (kg/m³)"] * MATERIAL_DB["sp"]["cost"]

        + individual["Amount / Quantity of Fiber"] * MATERIAL_DB["fiber"]["cost"]

    )

    return cost
# ==========================================================
# CO₂ FUNCTION
# ==========================================================

def calculate_co2(individual):

    co2 = (

        individual["Cement Amount  (kg/m³)"] * MATERIAL_DB["cement"]["co2"]

        + individual["Silica Fume (kg/m³)"] * MATERIAL_DB["silica"]["co2"]

        + individual["GGBFS  (kg/m³)"] * MATERIAL_DB["ggbs"]["co2"]

        + individual["Water (kg/m³)"] * MATERIAL_DB["water"]["co2"]

        + individual["Fine Aggregate (kg/m³)"] * MATERIAL_DB["sand"]["co2"]

        + individual["Superplasticizer (kg/m³)"] * MATERIAL_DB["sp"]["co2"]

        + individual["Amount / Quantity of Fiber"] * MATERIAL_DB["fiber"]["co2"]

    )

    return co2
# ==========================================================
# NORMALIZATION
# ==========================================================

def normalize(value, minimum, maximum, reverse=False):

    if maximum == minimum:
        return 100

    score = (value - minimum) / (maximum - minimum)

    if reverse:
        score = 1 - score

    return score * 100
# ==========================================================
# ENGINEERING SCORE
# ==========================================================

def calculate_engineering_score(individual):

    score = 0

    # -----------------------------
    # Water/Binder Ratio (30)
    # -----------------------------
    wb = individual["Water_Binder_Ratio"]

    if 0.16 <= wb <= 0.19:
        score += 30
    elif 0.19 < wb <= 0.21:
        score += 20
    else:
        score += 10

    # -----------------------------
    # Fiber Dosage (25)
    # -----------------------------
    fiber = individual["Amount / Quantity of Fiber"]

    if 140 <= fiber <= 170:
        score += 25
    elif 130 <= fiber <= 180:
        score += 18
    else:
        score += 10

    # -----------------------------
    # Binder Content (25)
    # -----------------------------
    binder = individual["Binder"]

    if 850 <= binder <= 1100:
        score += 25
    elif 750 <= binder < 850:
        score += 18
    else:
        score += 10

    # -----------------------------
    # Fine Aggregate (20)
    # -----------------------------
    sand = individual["Fine Aggregate (kg/m³)"]

    if 850 <= sand <= 1100:
        score += 20
    elif 750 <= sand < 850:
        score += 15
    else:
        score += 8

    return score
# ==========================================================
# INITIAL POPULATION
# ==========================================================

def initialize_population(population_size):

    population = []

    for _ in range(population_size):

        population.append(generate_individual())

    return population
# ==========================================================
# TOURNAMENT SELECTION
# ==========================================================

def tournament_selection(population, tournament_size=5):

    tournament = random.sample(population, tournament_size)

    tournament = sorted(
        tournament,
        key=lambda x: x["Fitness"],
        reverse=True
    )

    return tournament[0]
# ==========================================================
# UNIFORM CROSSOVER
# ==========================================================

def crossover(parent1, parent2):

    child = {}

    genes = [

        "Cement Amount  (kg/m³)",

        "Silica Fume (kg/m³)",

        "Flayash Amount   (kg/m³)",

        "GGBFS  (kg/m³)",

        "Water (kg/m³)",

        "Fine Aggregate (kg/m³)",

        "Superplasticizer (kg/m³)",

        "Amount / Quantity of Fiber"

    ]

    for gene in genes:

        child[gene] = random.choice([

            parent1[gene],

            parent2[gene]

        ])

    binder = (

        child["Cement Amount  (kg/m³)"]

        + child["Silica Fume (kg/m³)"]

        + child["GGBFS  (kg/m³)"]

    )

    child["Binder"] = binder

    child["Water_Binder_Ratio"] = (

        child["Water (kg/m³)"] / binder

    )

    return child
# ==========================================================
# MUTATION
# ==========================================================

def mutate(individual, mutation_rate=0.10):

    if random.random() < mutation_rate:

        individual["Cement Amount  (kg/m³)"] += random.uniform(-20,20)

    if random.random() < mutation_rate:

        individual["Silica Fume (kg/m³)"] += random.uniform(-10,10)

    if random.random() < mutation_rate:

        individual["GGBFS  (kg/m³)"] += random.uniform(-20,20)

    if random.random() < mutation_rate:

        individual["Water (kg/m³)"] += random.uniform(-5,5)

    if random.random() < mutation_rate:

        individual["Fine Aggregate (kg/m³)"] += random.uniform(-20,20)

    if random.random() < mutation_rate:

        individual["Superplasticizer (kg/m³)"] += random.uniform(-2,2)

    if random.random() < mutation_rate:

        individual["Amount / Quantity of Fiber"] += random.uniform(-5,5)

    # ---------- Clamp Limits ----------

    individual["Cement Amount  (kg/m³)"] = np.clip(
        individual["Cement Amount  (kg/m³)"],
        *LIMITS["cement"]
    )

    individual["Silica Fume (kg/m³)"] = np.clip(
        individual["Silica Fume (kg/m³)"],
        *LIMITS["silica"]
    )

    individual["GGBFS  (kg/m³)"] = np.clip(
        individual["GGBFS  (kg/m³)"],
        *LIMITS["ggbs"]
    )

    individual["Water (kg/m³)"] = np.clip(
        individual["Water (kg/m³)"],
        *LIMITS["water"]
    )

    individual["Fine Aggregate (kg/m³)"] = np.clip(
        individual["Fine Aggregate (kg/m³)"],
        *LIMITS["sand"]
    )

    individual["Superplasticizer (kg/m³)"] = np.clip(
        individual["Superplasticizer (kg/m³)"],
        *LIMITS["sp"]
    )

    individual["Amount / Quantity of Fiber"] = np.clip(
        individual["Amount / Quantity of Fiber"],
        *LIMITS["fiber"]
    )

    binder = (
        individual["Cement Amount  (kg/m³)"]
        + individual["Silica Fume (kg/m³)"]
        + individual["GGBFS  (kg/m³)"]
    )

    individual["Binder"] = binder

    individual["Water_Binder_Ratio"] = (
        individual["Water (kg/m³)"] / binder
    )

    return individual
# ==========================================================
# EVOLVE POPULATION
# ==========================================================

def evolve_population(

    population,

    target_strength,

    min_cost,

    max_cost,

    min_co2,

    max_co2

):

    new_population = []

    population = sorted(

        population,

        key=lambda x: x["Fitness"],

        reverse=True

    )

    # ---------- Elitism ----------

    new_population.extend(population[:5])

    while len(new_population) < len(population):

        parent1 = tournament_selection(population)

        parent2 = tournament_selection(population)

        child = crossover(parent1, parent2)

        child = mutate(child)

        child = fitness(

            child,

            target_strength,

            min_cost,

            max_cost,

            min_co2,

            max_co2

        )

        new_population.append(child)

    return new_population

# ==========================================================
# GENETIC ALGORITHM
# ==========================================================

def genetic_algorithm(
        
    target_strength,

    population_size,

    generations

):

    # -----------------------------------
    # Initial Population
    # -----------------------------------
    print("Step 1 - Initializing population") 

    population = initialize_population(population_size)

    # -----------------------------------
    # Evaluate Initial Population
    # -----------------------------------

    costs = [calculate_cost(i) for i in population]

    co2_values = [calculate_co2(i) for i in population]

    min_cost = min(costs)
    max_cost = max(costs)

    min_co2 = min(co2_values)
    max_co2 = max(co2_values)

    evaluated_population = []

    print("Step 2 - Evaluating initial population")

    for individual in population:

        evaluated_population.append(

            fitness(

                individual,

                target_strength,

                min_cost,

                max_cost,

                min_co2,

                max_co2

            )

        )

    population = evaluated_population

    print("Step 3 - Initial population complete")

    # -----------------------------------
    # Evolution
    # -----------------------------------

    for generation in range(generations):

    print(f"Generation {generation+1}/{generations}")
        
        print(f"Generation {generation+1}/{generations}")

        population = evolve_population(

            population,

            target_strength,

            min_cost,

            max_cost,

            min_co2,

            max_co2

        )

    population = sorted(

        population,

        key=lambda x: x["Fitness"],

        reverse=True

    )

    return pd.DataFrame(population[:20])