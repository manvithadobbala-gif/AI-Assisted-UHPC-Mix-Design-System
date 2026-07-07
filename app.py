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

    page_title="AI-Assisted UHPC Mix Design System",

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

    st.info("""
    ### 🚀 AI-Assisted Decision Support Platform

    Core capabilities include:

    • 🧠 XGBoost Machine Learning

    • ⚙️ Particle Swarm Optimization (PSO)

    • 🏗️ Engineering Validation

    • 💰 Cost Estimation

    • 🌱 Sustainability Assessment

    to generate optimized Ultra High Performance Concrete (UHPC) mix designs.
    """)

 
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

    st.subheader("✨ Core Features")

    c1, c2 = st.columns(2)

    with c1:
            st.success("🤖 XGBoost Strength Prediction")
            st.success("⚙️ Particle Swarm Optimization")
            st.success("🏗 Engineering Feasibilty Checks")
            st.success("🌱 Sustainability Assessment")

    with c2:
            st.success("📊 Interactive Engineering Dashboard")
            st.success("📥 CSV Export")
            st.success("🏆 AI Recommendation Engine")
        
    st.divider()

    st.subheader("🧠 AI Engineering Workflow")

    st.markdown("""
    **1️⃣ Define Design Requirements**

    - Target compressive strength
    - Design objective

    ---

    **2️⃣ Machine Learning Prediction**

    - XGBoost estimates achievable compressive strength

    ---

    **3️⃣ Optimization**

    - Particle Swarm Optimization generates candidate UHPC mixes

    ---

    **4️⃣ Engineering Validation**

    - Binder ratio verification
    - Practical feasibility assessment

    ---

    **5️⃣ AI Recommendation**

    - Engineering score
    - Cost estimation
    - CO₂ assessment

    ---

    **6️⃣ Export Results**

    - Download optimized mix designs in CSV format
    """)

    st.divider()

    st.info(
    """
    ### 💡 Project Purpose

    This application demonstrates the integration of Artificial Intelligence
    with Civil Engineering to support faster, more reliable and sustainable
    UHPC mix design.

    Developed as part of an academic internship project.
    """
    )
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
            
            st.write(results.head())
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

        st.subheader("🎯 Optimization Strategy")

        if design_objective == "⭐ Balanced Design (Recommended)":
            st.info("""
        **Balanced Design**

        The optimization simultaneously considered compressive strength, engineering feasibility, material cost, and CO₂ emissions to identify a well-balanced UHPC mix design.
        """)

        elif design_objective == "💰 Minimize Cost":
            st.info("""
        **Cost-Optimized Design**

        The optimization prioritized minimizing the estimated material cost while satisfying the target compressive strength and maintaining engineering feasibility.
        """)

        elif design_objective == "🌱 Minimize Carbon Footprint":
            st.info("""
        **Sustainable Design**

        The optimization prioritized reducing the estimated embodied CO₂ emissions while maintaining the required compressive strength and practical mix proportions.
        """)

        elif design_objective == "💪 Maximize Strength":
            st.info("""
        **High-Strength Design**

        The optimization prioritized maximizing the predicted compressive strength while ensuring that the generated mix remained practically feasible.
        """)

        elif design_objective == "🏗️ Maximize Practicality":
            st.info("""
        **Practical Engineering Design**

        The optimization prioritized engineering feasibility by emphasizing practical UHPC mix proportions, realistic water–binder ratios, and appropriate binder and fibre contents.
        """)
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

            st.subheader("📌 Engineering Assessment")

            if score >= 90:
                st.success("✅ Excellent engineering feasibility. The generated mix satisfies the recommended UHPC design guidelines.")

            elif score >= 75:
                st.warning("⚠ Good engineering feasibility. Minor adjustments may further improve practical performance.")

            else:
                st.error("❌ Engineering feasibility is limited. Review the material proportions before practical implementation.")

            binder = (
                mix["Cement"] +
                mix["Silica Fume"] +
                mix["GGBS"]
            )

            wb = mix["Water"] / binder

            checks = []

            # Cement
            if mix["Cement"] >= 600:
                checks.append("✅ Cement content is within the recommended UHPC range.")
            else:
                checks.append("❌ Cement content is below the recommended minimum.")

            # Water–binder ratio
            if wb <= 0.20:
                checks.append(f"✅ Water–binder ratio ({wb:.3f}) is acceptable.")
            else:
                checks.append(f"⚠ Water–binder ratio ({wb:.3f}) is relatively high.")

            # Binder
            if 800 <= binder <= 1100:
                checks.append(f"✅ Total binder content ({binder:.1f} kg/m³) is within the recommended range.")
            else:
                checks.append(f"⚠ Total binder content ({binder:.1f} kg/m³) is outside the recommended range.")

            # Steel fibre
            if 120 <= mix["Steel Fiber"] <= 220:
                checks.append("✅ Steel fibre dosage is within the recommended range.")
            else:
                checks.append("⚠ Steel fibre dosage should be reviewed.")

            for item in checks:
                st.write(item)

            st.subheader("📋 Engineering Recommendations")

            st.info("""
            ### Recommended Materials and Construction Practice

            **Fine Aggregate**
            • Material: Quartz sand or high-quality silica sand
            • Maximum particle size: ≤ 2 mm

            **Steel Fibres**
            • Use high-strength steel fibres.
            • Ensure uniform dispersion during mixing to prevent fibre balling.

            **Superplasticizer**
            • Use a Polycarboxylate Ether (PCE)-based high-range water reducer.

            **Mixing Procedure**
            • Dry-mix all powder constituents before adding water and superplasticizer.
            • Add steel fibres gradually at the final stage of mixing.

            **Curing**
            • Follow the curing procedure adopted in the selected experimental programme or the project specification to achieve the desired mechanical performance.

            **Quality Control**
            • Verify workability before casting.
            • Maintain the specified water-to-binder ratio.
            • Ensure proper compaction and curing.
            """)
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
    st.title("ℹ️ About the system")

    st.markdown("""
    # 🏗️ AI-Assisted UHPC Mix Design System

    The **AI-Assisted UHPC Mix Design System** is an intelligent decision-support platform developed to support engineers and researchers in designing **Ultra-High Performance Concrete (UHPC)** mixtures using machine learning and optimization techniques.

    The system integrates **XGBoost**, **Particle Swarm Optimization (PSO)**, engineering validation, cost estimation, and sustainability assessment to recommend optimized UHPC mix designs that satisfy target compressive strength while maintaining practical feasibility.

    ---
    """)

    st.subheader("🎯 Project Objectives")

    st.markdown("""
    - Predict UHPC compressive strength using Machine Learning
    - Generate optimized UHPC mix proportions
    - Optimize material cost
    - - Assess environmental impact (CO₂ emissions)
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

        st.success("🐍 Python Programming")

    st.divider()

    st.subheader("🧠 AI Workflow")

    st.markdown("""
    1. User enters the target compressive strength.

    2. XGBoost predicts achievable strength.

    3. Particle Swarm Optimization (PSO) generates candidate UHPC mix designs.

    4. Engineering validation evaluates each generated mix.

    5. Cost and CO₂ emissions are estimated.

    6. Recommendation Engine ranks candidate mixes based on engineering performance, cost, and sustainability.

    7. Final AI-generated mix designs can be exported as CSV file.
        
    """)
    
    st.divider()

    st.subheader("📊 Key Features")

    st.markdown("""
        - UHPC Strength Prediction

        - AI-Assisted Mix Design Generation

        - Particle Swarm Optimization

        - Engineering Validation

        - Cost Estimation

        - CO₂ Emission Assessment

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
    - Web-based collaborative deployment
    - Real-time material price updates
    - Additional supplementary cementitious materials (SCMs)
    """)

    st.divider()

    st.subheader("⚠️ Engineering Assumptions and Limitations")

    st.warning("""
    - Material costs are estimated using representative Indian market prices.
    - CO₂ emissions are estimated using literature-based embodied carbon emission factors.
    - Optimization is constrained within practical UHPC material limits.
    - Predictions are valid only within the range of the training dataset.
    - AI-generated mix designs should be experimentally validated before practical implementation.
    """)

    st.divider()

    st.subheader("👨‍🎓 Project Information")

    st.info("""
        **Project Title**

        AI-Assisted UHPC Mix Design System

        **Developed For**

        Internship

        Department of Civil Engineering

        **Core Technologies**

        Python
        Streamlit
        XGBoost
        Particle Swarm Optimization (PSO)
    """)

st.divider()

st.caption("© 2026 AI-Assisted UHPC Mix Design System | Developed by Manvitha Dobbala")