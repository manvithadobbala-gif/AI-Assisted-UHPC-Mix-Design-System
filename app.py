import streamlit as st
import pandas as pd

from utils.predictor import predict_strength
from utils.pso_optimizer import pso_optimize
from utils.engineering_validation import (
    engineering_validation,
    estimate_cost_co2
)
from utils.recommendation_engine import generate_recommendations

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="UHPC AI Engineering Suite",

    page_icon="🏗️",

    layout="wide"

)
# =====================================================
# SESSION STATE
# =====================================================

if "results" not in st.session_state:
    st.session_state.results = None

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "best" not in st.session_state:
    st.session_state.best = None
# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🏗️ UHPC AI")

st.sidebar.caption("AI Engineering Suite")

page = st.sidebar.selectbox(

    "Navigation",

    [

        "🏠 Home",

        "📈 Strength Predictor",

        "🚀 AI Mix Designer",

        "📊 Engineering Results",

        "ℹ️ About"

    ]

)

st.sidebar.divider()

st.sidebar.markdown("### Modules")

st.sidebar.write("🧠 XGBoost Prediction")

st.sidebar.write("⚙️ PSO Optimization")

st.sidebar.write("🏗️ Engineering Validation")

st.sidebar.write("🌱 Sustainability")

# =====================================================
# HOME
# =====================================================

if page == "🏠 Home":

    st.title("🏗️ AI-Assisted UHPC Mix Design System")
    st.success(
    "🚀 AI-Assisted Decision Support System for Ultra High Performance Concrete (UHPC) Mix Design"
    )

    st.subheader("Design • Optimize • Validate")

    st.write("")

    st.markdown(
            """
    Welcome to the **AI-Assisted UHPC Mix Design System**.

    This application combines:

    - 🧠 Machine Learning (XGBoost)
    - ⚙️ Particle Swarm Optimization (PSO)
    - 🏗️ Engineering Validation
    - 💰 Cost Estimation
    - 🌱 CO₂ Assessment

    to generate optimized Ultra High Performance Concrete (UHPC) mix designs.
    """
    )
 
    st.divider()

    st.subheader("📊 System Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "AI Models",
            "2",
            "XGBoost + PSO"
        )

    with c2:
        st.metric(
            "Target Strength",
            "80–200 MPa",
            "Supported"
        )

    with c3:
        st.metric(
            "Optimization",
            "Top 5",
            "Recommended Mixes"
        )

    with c4:
        st.metric(
            "Outputs",
            "CSV",
            "Export Ready"
        )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "AI Model",
            "XGBoost"
        )

    with c2:

        st.metric(
            "Optimization",
            "PSO"
        )

    with c3:

        st.metric(
            "Validation",
            "Engineering Rules"
        )

    st.divider()

    st.subheader("✨ Core Features")

    c1, c2 = st.columns(2)

    with c1:
            st.success("🤖 XGBoost Prediction")
            st.success("⚙️ PSO Optimization")
            st.success("🏗 Engineering Validation")
            st.success("🌱 Sustainability Analysis")

    with c2:
            st.success("📊 Interactive Dashboard")
            st.success("📥 CSV Export")
            st.success("🏆 AI Recommendation Engine")
        
    st.divider()

    st.subheader("🧠 AI Engineering Workflow")

    st.markdown("""
        ### 1️⃣ Input Design Requirements
        - Target compressive strength
        - Design objective

        ### 2️⃣ Machine Learning Prediction
        - XGBoost predicts achievable strength

        ### 3️⃣ AI Optimization
        - Particle Swarm Optimization generates candidate UHPC mixes

        ### 4️⃣ Engineering Validation
        - Practical feasibility checks
        - Binder ratio verification

        ### 5️⃣ Recommendation Engine
        - Cost
        - CO₂
        - Engineering score

        ### 6️⃣ Export Results
        - CSV
        """)
# =====================================================
# STRENGTH PREDICTOR
# =====================================================

if page == "📈 Strength Predictor":

    st.title("📈 UHPC Strength Predictor")

    st.markdown(
        """
Predict the compressive strength of a UHPC mix using the trained
**XGBoost Machine Learning model**.
"""
    )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        cement = st.number_input(
            "Cement (kg/m³)",
            value=500.0
        )

        silica = st.number_input(
            "Silica Fume (kg/m³)",
            value=100.0
        )

        ggbs = st.number_input(
            "GGBS (kg/m³)",
            value=400.0
        )

        water = st.number_input(
            "Water (kg/m³)",
            value=140.0
        )

    with c2:

        fine = st.number_input(
            "Fine Aggregate (kg/m³)",
            value=1000.0
        )

        sp = st.number_input(
            "Superplasticizer (kg/m³)",
            value=15.0
        )

        fibre = st.number_input(
            "Steel Fiber (kg/m³)",
            value=150.0
        )
    if st.button("🧠 Predict Strength"):

       binder = cement + silica + ggbs

       wb = water / binder

       candidate = {

    "Cement Amount  (kg/m³)": cement,

    "Silica Fume (kg/m³)": silica,

    "Flayash Amount   (kg/m³)": 0,

    "GGBFS  (kg/m³)": ggbs,

    "Water (kg/m³)": water,

    "Fine Aggregate (kg/m³)": fine,

    "Superplasticizer (kg/m³)": sp,

    "Amount / Quantity of Fiber": fibre,

    "Binder": binder,

    "Water_Binder_Ratio": wb

}

       strength = predict_strength(candidate)

       st.success("Prediction Completed Successfully!")

       st.metric(

            "Predicted Compressive Strength",

            f"{strength:.2f} MPa"

        )
# =====================================================
# AI MIX DESIGNER
# =====================================================

if page == "🚀 AI Mix Designer":

    st.title("🚀 AI Mix Designer")

    st.markdown("""
Generate optimized UHPC mix designs using:

- 🧠 XGBoost Machine Learning
- ⚙️ Particle Swarm Optimization (PSO)
- 🏗️ Engineering Validation
- 💰 Cost Estimation
- 🌱 CO₂ Assessment
""")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        target_strength = st.number_input(

            "🎯 Target Strength (MPa)",

            min_value=80.0,

            max_value=250.0,

            value=150.0,

            step=5.0

        )

    with col2:

        design_objective = st.selectbox(

            "🎯 Design Objective",

            [

                "⭐ Balanced Design (Recommended)",

                "💰 Minimize Cost",

                "🌱 Minimize Carbon Footprint",

                "💪 Maximize Strength",

                "🏗️ Maximize Practicality"

            ]

        )

    st.write("")

    if st.button("🧠 Generate AI Mix Designs"):

        with st.spinner("Generating optimized UHPC mixes..."):

            results = pso_optimize(

                target_strength=target_strength,

                design_objective=design_objective,

                swarm_size=40,

                iterations=50

            )

        recommendations = generate_recommendations(results)

        best = recommendations.iloc[0]

        st.session_state.results = results

        st.session_state.recommendations = recommendations

        st.session_state.best = best

        st.success("✅ AI Mix Designs Generated Successfully!")

        st.divider()

        st.subheader("🧠 AI Processing Summary")

        st.success("✔ XGBoost Prediction")

        st.success("✔ Particle Swarm Optimization")

        st.success("✔ Engineering Validation")

        st.success("✔ Recommendation Engine")
        st.divider()

        st.subheader("📊 Recommendation Summary")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "Target Strength",

                f"{target_strength:.0f} MPa"

            )

        with c2:

            st.metric(

                "Candidate Mixes",

                len(results)

            )

        with c3:

            st.metric(

                "Recommended Mixes",

                len(recommendations)

            )
        st.divider()

        st.header("🏆 AI Recommended Mix Designs")

        for i, mix in recommendations.iterrows():

            with st.expander(
            f"{mix['Recommendation']}   |   {mix['Predicted Strength']:.2f} MPa",
            expanded=(i==0)
            ):

             c1, c2, c3, c4 = st.columns(4)
             
             c1.metric(
                    "Strength",
                    f"{mix['Predicted Strength']:.2f} MPa"
                )

             c2.metric(
                    "Engineering",
                    f"{mix['Engineering Score']}/100"
                )

             c3.metric(
                    "Cost",
                    f"₹ {mix['Estimated Cost']:.0f}"
                )

             c4.metric(
                    "CO₂",
                    f"{mix['Estimated CO2']:.1f}"
                    )

             st.subheader("📋 Material Composition")

             composition = pd.DataFrame({

                    "Material":[

                        "Cement",

                        "Silica Fume",

                        "GGBS",

                        "Water",

                        "Fine Aggregate",

                        "Superplasticizer",

                        "Steel Fiber"

                    ],

                    "Quantity (kg/m³)":[

                        mix["Cement"],

                        mix["Silica Fume"],

                        mix["GGBS"],

                        mix["Water"],

                        mix["Fine Aggregate"],

                        mix["Superplasticizer"],

                        mix["Steel Fiber"]

                    ]

            })

            st.dataframe(
                    composition,
                    hide_index=True,
                    use_container_width=True
                )
                                    
            binder = (
                mix["Cement"] +
                mix["Silica Fume"] +
                mix["GGBS"]
            )

            wb = mix["Water"] / binder

            st.write("")

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "Binder Content",
                    f"{binder:.1f} kg/m³"
                )

            with c2:

                st.metric(
                    "Water/Binder Ratio",
                    f"{wb:.3f}"
                )
            
            validation, score = engineering_validation(mix)

            st.write("")

            st.subheader("🏗️ Engineering Validation")

            st.dataframe(
                validation,
                hide_index=True,
                use_container_width=True
            )

            st.metric(
                "Overall Engineering Score",
                f"{score}/100"
            )

            st.divider()

            st.subheader("📊 Material Contribution Analysis")

            materials = {
                "Cement": mix["Cement"],
                "Silica Fume": mix["Silica Fume"],
                "GGBS": mix["GGBS"],
                "Water": mix["Water"],
                "Fine Aggregate": mix["Fine Aggregate"],
                "Superplasticizer": mix["Superplasticizer"],
                "Steel Fiber": mix["Steel Fiber"]
            }

            material_df = pd.DataFrame({
                "Material": list(materials.keys()),
                "Quantity (kg/m³)": list(materials.values())
            })

            st.bar_chart(
                material_df.set_index("Material")
            )   

        st.subheader("🧠 Why did the AI recommend this mix?")

        reason = []

        # Strength
        if mix["Predicted Strength"] >= target_strength:
            reason.append(
                f"✅ Predicted strength ({mix['Predicted Strength']:.1f} MPa) meets the target strength."
            )

        # Engineering
        if score >= 90:
            reason.append(
                "✅ Excellent engineering feasibility based on validation rules."
            )

        # Cost
        if mix["Estimated Cost"] <= recommendations["Estimated Cost"].mean():
            reason.append(
                "💰 Cost is lower than the average of the generated candidate mixes."
            )

        # Sustainability
        if mix["Estimated CO2"] <= recommendations["Estimated CO2"].mean():
            reason.append(
                "🌱 Carbon footprint is lower than the average generated mix."
            )

        # Recommendation
        reason.append(
            "🏆 This mix achieved one of the highest overall AI recommendation scores."
        )

        for r in reason:
                st.success(r)

        if st.session_state.recommendations is not None:

            st.divider()

            st.subheader("📥 Export Results")

            csv = recommendations.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📄 Download AI Mix Designs (CSV)",
                data=csv,
                file_name="UHPC_AI_Mix_Designs.csv",
                mime="text/csv",
                key="csv_download"
            )
# =====================================================
# ENGINEERING RESULTS
# =====================================================

if page == "📊 Engineering Results":

    st.title("📊 Engineering Results")

    if st.session_state.recommendations is None:

        st.warning(
            "⚠️ Please generate AI Mix Designs first."
        )

    else:

        recommendations = st.session_state.recommendations

        st.success(
            f"{len(recommendations)} AI Mix Designs Available"
        )

        st.divider()

        best = recommendations.iloc[0]

        st.subheader("🏆 Best AI Mix")

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(

                "Strength",

                f"{best['Predicted Strength']:.2f} MPa"

            )

        with c2:

            st.metric(

                "Engineering",

                f"{best['Engineering Score']}/100"

            )

        with c3:

            st.metric(

                "Cost",

                f"₹ {best['Estimated Cost']:.0f}"

            )

        with c4:

            st.metric(

                "CO₂",

                f"{best['Estimated CO2']:.1f}"

        )

        st.divider()

        st.subheader("📊 Complete AI Mix Comparison")

        st.dataframe(

            recommendations,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        st.subheader("📈 Strength Comparison")

        chart = recommendations.set_index("Recommendation")["Predicted Strength"]

        st.bar_chart(chart)

        st.subheader("🏗️ Engineering Score Comparison")

        chart = recommendations.set_index("Recommendation")["Engineering Score"]

        st.bar_chart(chart)

        st.subheader("💰 Cost Comparison")

        chart = recommendations.set_index("Recommendation")["Estimated Cost"]

        st.bar_chart(chart)

        st.subheader("🌱 Carbon Footprint Comparison")

        chart = recommendations.set_index("Recommendation")["Estimated CO2"]

        st.bar_chart(chart)

        st.divider()

        st.subheader("📈 Strength Comparison")

        st.bar_chart(
            recommendations.set_index("Recommendation")["Predicted Strength"]
        )

        st.subheader("🏗️ Engineering Score Comparison")

        st.bar_chart(
            recommendations.set_index("Recommendation")["Engineering Score"]
        )

        st.subheader("💰 Cost Comparison")

        st.bar_chart(
            recommendations.set_index("Recommendation")["Estimated Cost"]
        )

        st.subheader("🌱 CO₂ Emission Comparison")

        st.bar_chart(
            recommendations.set_index("Recommendation")["Estimated CO2"]
        )

# ============================================
# ABOUT
# ============================================

elif page == "ℹ️ About":
    st.title("ℹ️ About")

    st.markdown("""
    # 🏗️ AI-Assisted UHPC Mix Design System

    The **AI-Assisted UHPC Mix Design System** is an intelligent decision-support application developed to assist engineers and researchers in designing **Ultra-High Performance Concrete (UHPC)** mixtures using Artificial Intelligence and optimization techniques.

    This software combines machine learning, engineering validation, optimization algorithms, and sustainability assessment to recommend practical UHPC mix designs that satisfy specified compressive strength requirements while considering engineering feasibility, cost, and environmental impact.

    ---
    """)

    st.subheader("🎯 Project Objectives")

    st.markdown("""
    - Predict UHPC compressive strength using Machine Learning
    - Generate optimized UHPC mix proportions
    - Minimize material cost
    - Reduce carbon footprint
    - Perform engineering validation of generated mixes
    - Recommend practical and sustainable UHPC mixtures
    """)

    st.divider()

    st.subheader("⚙️ Technologies Used")

    col1, col2 = st.columns(2)

    with col1:

        st.success("🤖 XGBoost Machine Learning")

        st.success("⚙️ Particle Swarm Optimization (PSO)")

        st.success("🏗️ Engineering Validation")

    with col2:

        st.success("🌱 Sustainability Assessment")

        st.success("📊 Streamlit Dashboard")

        st.success("🐍 Python")

    st.divider()

    st.subheader("🧠 AI Workflow")

    st.markdown("""
    1. User enters the target compressive strength.

    2. XGBoost predicts achievable strength.

    3. Particle Swarm Optimization (PSO) generates candidate UHPC mix designs.

    4. Engineering validation evaluates each generated mix.

    5. Cost and CO₂ emissions are estimated.

    6. Recommendation Engine ranks the best performing UHPC mixes.

    7. Final AI-generated mix designs can be exported as CSV file.
        
    """)
    
    st.divider()

    st.subheader("📊 Key Features")

    st.markdown("""
        - UHPC Strength Prediction

        - AI-Based Mix Design Generation

        - Particle Swarm Optimization

        - Engineering Validation

        - Cost Estimation

        - Carbon Footprint Estimation

        - Recommendation Engine

        - Interactive Dashboard

        - CSV Export

    """)

    st.divider()

    st.subheader("🚀 Future Scope")

    st.markdown("""
    - Multi-objective optimization
    - Explainable Artificial Intelligence (XAI)
    - Life Cycle Assessment (LCA)
    - Integration with laboratory databases
    - Cloud-based deployment
    - Real-time material price updates
    - Additional supplementary cementitious materials (SCMs)
    """)

    st.divider()

    st.subheader("👨‍🎓 Project Information")

st.info("""
    **Project Title**

    AI-Assisted UHPC Mix Design System

    **Developed For**

    Internship

    Department of Civil Engineering

    **Framework**

    Python • Streamlit • XGBoost • PSO
""")

st.divider()

st.caption("© 2026 AI-Assisted UHPC Mix Design System")