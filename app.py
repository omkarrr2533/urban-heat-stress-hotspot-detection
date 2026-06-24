import os
import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="UrbanHeat AI | Cooling Strategy Dashboard",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #071a2f 0%, #0b2545 48%, #102a43 100%);
            color: #f4f8ff;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #061526 0%, #0a2742 100%);
        }

        [data-testid="stSidebar"] * {
            color: #eef6ff;
        }

        h1 {
            color: #ffffff !important;
            font-size: 2.8rem !important;
            font-weight: 800 !important;
            letter-spacing: -1px;
        }

        h2, h3 {
            color: #6ee7f9 !important;
        }

        .hero-text {
            color: #b7f7ff;
            font-size: 1.08rem;
            line-height: 1.7;
            max-width: 1000px;
        }

        .section-note {
            background: rgba(6, 78, 59, 0.55);
            border-left: 5px solid #34d399;
            border-radius: 8px;
            padding: 14px 18px;
            margin: 10px 0 22px 0;
            color: #eafff7;
        }

        [data-testid="stMetric"] {
            background: rgba(5, 26, 48, 0.78);
            border: 1px solid rgba(103, 232, 249, 0.38);
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 8px 22px rgba(0, 0, 0, 0.22);
        }

        [data-testid="stMetricLabel"] {
            color: #a5f3fc !important;
        }

        [data-testid="stMetricValue"] {
            color: #ffffff !important;
        }

        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }

        .footer-text {
            text-align: center;
            color: #a5f3fc;
            padding: 10px;
            font-size: 0.9rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("Urban Heat Mitigation and Cooling Strategy Optimization")

st.markdown(
    """
    <div class="hero-text">
        Satellite-driven hotspot detection, machine-learning-based heat prediction,
        heat-vulnerability analysis, and scenario-based cooling intervention planning.
        <br><br>
        <b>Study Area:</b> Chhatrapati Sambhajinagar, Maharashtra, India
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

DATA_FOLDER = "outputs/dashboard_data"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    hotspot_map = pd.read_csv(
        os.path.join(DATA_FOLDER, "dashboard_hotspot_map_v3.csv")
    )

    scenario_map = pd.read_csv(
        os.path.join(DATA_FOLDER, "dashboard_scenario_map_v3.csv")
    )

    priority_zones = pd.read_csv(
        os.path.join(DATA_FOLDER, "dashboard_priority_zones_v3.csv")
    )

    intervention_zones = pd.read_csv(
        os.path.join(DATA_FOLDER, "dashboard_intervention_zones_v3.csv")
    )

    shap_importance = pd.read_csv(
        os.path.join(DATA_FOLDER, "dashboard_shap_importance_v3.csv")
    )

    model_comparison = pd.read_csv(
        os.path.join(DATA_FOLDER, "dashboard_model_comparison.csv")
    )

    scenario_summary = pd.read_csv(
        os.path.join(DATA_FOLDER, "dashboard_scenario_summary_v3.csv")
    )

    kpis = pd.read_csv(
        os.path.join(DATA_FOLDER, "dashboard_kpis_v3.csv")
    )

    vulnerability_map = pd.read_csv(
        os.path.join(DATA_FOLDER, "dashboard_vulnerability_map_v3.csv")
    )

    vulnerability_zones = pd.read_csv(
        os.path.join(DATA_FOLDER, "dashboard_vulnerability_zones_v3.csv")
    )

    return (
        hotspot_map,
        scenario_map,
        priority_zones,
        intervention_zones,
        shap_importance,
        model_comparison,
        scenario_summary,
        kpis,
        vulnerability_map,
        vulnerability_zones
    )


try:
    (
        hotspot_map,
        scenario_map,
        priority_zones,
        intervention_zones,
        shap_importance,
        model_comparison,
        scenario_summary,
        kpis,
        vulnerability_map,
        vulnerability_zones
    ) = load_data()

except FileNotFoundError as error:
    st.error("Dashboard data file not found.")
    st.write("Please run Notebook 13 again before running the dashboard.")
    st.code(str(error))
    st.stop()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.markdown("## UrbanHeat AI")
st.sidebar.caption("Decision-support dashboard")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Select Dashboard Section",
    [
        "Project Overview",
        "Model Performance",
        "Urban Heat Hotspots",
        "Cooling Intervention Planning",
        "Heat Vulnerability",
        "Explainable AI"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Team AstroByte")
st.sidebar.caption("Bharatiya Antariksh Hackathon 2026")

st.sidebar.markdown(
    """
    **Priyal Deshmukh**  
    AI/ML Lead  

    **Srushti Bawaskar**  
    Geospatial and Data Lead  

    **Rishika Deshmukh**  
    Research, Documentation and Dashboard Lead  
    """
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Satellite Data | Geospatial Analytics | AI/ML | Cooling Planning"
)


# --------------------------------------------------
# PROJECT OVERVIEW
# --------------------------------------------------

if page == "Project Overview":

    st.header("Project Overview")

    st.write(
        "This dashboard supports urban heat mitigation planning using "
        "satellite-derived indicators, machine learning, hotspot detection, "
        "cooling scenario simulation, and heat vulnerability analysis."
    )

    st.markdown(
        """
        <div class="section-note">
            The dashboard converts satellite-derived urban heat indicators into
            location-specific planning insights: where heat is highest, where people
            are most exposed, and which cooling intervention is predicted to help most.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Key Performance Indicators")

    kpi_values = dict(zip(kpis["Metric"], kpis["Value"]))

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Dataset V3 XGBoost R²",
        f"{float(kpi_values.get('Dataset V3 XGBoost R2', 0)):.3f}"
    )

    col2.metric(
        "Dataset V3 XGBoost MAE",
        f"{float(kpi_values.get('Dataset V3 XGBoost MAE (C)', 0)):.2f} °C"
    )

    col3.metric(
        "Sampled Locations",
        f"{int(float(kpi_values.get('Total Sampled Locations', 0))):,}"
    )

    col4.metric(
        "High-Priority Hotspot Zones",
        f"{int(float(kpi_values.get('High Priority Hotspot Zones', 0)))}"
    )

    st.markdown("---")

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Project Workflow")
        st.markdown(
            """
            1. Satellite data extraction using Google Earth Engine  
            2. Dataset V3 preparation with NDVI, NDBI, Elevation, Population, and LandCover  
            3. Leakage-aware spatial machine-learning validation  
            4. Urban heat hotspot detection  
            5. SHAP-based feature interpretation  
            6. Cooling intervention simulation  
            7. Heat Vulnerability Index and priority-zone identification  
            """
        )

    with right_col:
        st.subheader("Dataset V3 Features")

        feature_table = pd.DataFrame({
            "Feature": [
                "NDVI",
                "NDBI",
                "Elevation",
                "Population",
                "LandCover",
                "LST"
            ],
            "Purpose": [
                "Vegetation density",
                "Built-up intensity",
                "Terrain context",
                "Population exposure proxy",
                "Dominant surface class",
                "Land Surface Temperature target"
            ]
        })

        st.dataframe(feature_table, use_container_width=True, hide_index=True)


# --------------------------------------------------
# MODEL PERFORMANCE
# --------------------------------------------------

elif page == "Model Performance":

    st.header("Model Performance Comparison")

    st.markdown(
        """
        <div class="section-note">
            Dataset V2 and Dataset V3 are compared using the same leakage-aware
            spatial block cross-validation approach.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(model_comparison, use_container_width=True, hide_index=True)

    excluded_columns = ["Dataset", "Model"]

    metric_options = [
        column for column in model_comparison.columns
        if column not in excluded_columns
        and pd.api.types.is_numeric_dtype(model_comparison[column])
    ]

    if metric_options:
        selected_metric = st.selectbox(
            "Select Performance Metric",
            metric_options
        )

        fig = px.bar(
            model_comparison,
            x="Dataset",
            y=selected_metric,
            color="Dataset",
            text_auto=".3f",
            title=f"Dataset V2 vs Dataset V3: {selected_metric}"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f4f8ff"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Latitude and Longitude are excluded from prediction features "
        "to prevent spatial leakage."
    )


# --------------------------------------------------
# URBAN HEAT HOTSPOTS
# --------------------------------------------------

elif page == "Urban Heat Hotspots":

    st.header("Urban Heat Hotspots")

    st.markdown(
        """
        <div class="section-note">
            Point colours represent observed Land Surface Temperature categories.
            High-priority zones are ranked using mean LST and hotspot concentration.
        </div>
        """,
        unsafe_allow_html=True
    )

    heat_category_options = sorted(
        hotspot_map["Heat_Category"].dropna().astype(str).unique()
    )

    heat_categories = st.multiselect(
        "Select Heat Categories",
        options=heat_category_options,
        default=heat_category_options
    )

    filtered_hotspots = hotspot_map[
        hotspot_map["Heat_Category"].astype(str).isin(heat_categories)
    ].copy()

    if len(filtered_hotspots) > 0:
        filtered_hotspots["Map_Marker_Size"] = (
            filtered_hotspots["Observed_LST_C"]
            - filtered_hotspots["Observed_LST_C"].min()
            + 0.1
        )

        fig = px.scatter_mapbox(
            filtered_hotspots,
            lat="Latitude",
            lon="Longitude",
            color="Heat_Category",
            size="Map_Marker_Size",
            size_max=16,
            hover_data=[
                "Observed_LST_C",
                "Predicted_LST_C",
                "NDVI",
                "NDBI",
                "Population",
                "LandCover_Class",
                "Zone_ID"
            ],
            zoom=10,
            height=600,
            title="Observed Urban Heat-Stress Categories"
        )

        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 50, "l": 0, "b": 0}
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No locations match the selected heat categories.")

    st.subheader("Top 10 High-Priority Hotspot Zones")
    st.dataframe(priority_zones, use_container_width=True, hide_index=True)


# --------------------------------------------------
# COOLING INTERVENTION PLANNING
# --------------------------------------------------

elif page == "Cooling Intervention Planning":

    st.header("Cooling Intervention Planning")

    st.markdown(
        """
        <div class="section-note">
            Two model-based interventions are compared: urban greening and
            cool/permeable surfaces. Results are comparative planning estimates.
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = px.bar(
        scenario_summary,
        x="Scenario",
        y="Mean_Cooling_C",
        text="Mean_Cooling_C",
        title="Mean Predicted Cooling by Intervention Scenario"
    )

    fig.update_traces(
        texttemplate="%{text:.3f} °C",
        textposition="outside"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f4f8ff"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Zones by Cooling Potential")
    st.dataframe(intervention_zones, use_container_width=True, hide_index=True)

    intervention_options = sorted(
        scenario_map["Recommended_Intervention"].dropna().astype(str).unique()
    )

    intervention_choice = st.selectbox(
        "Filter Map by Recommended Intervention",
        options=["All"] + intervention_options
    )

    if intervention_choice == "All":
        filtered_scenarios = scenario_map.copy()
    else:
        filtered_scenarios = scenario_map[
            scenario_map["Recommended_Intervention"].astype(str)
            == intervention_choice
        ].copy()

    if len(filtered_scenarios) > 0:
        filtered_scenarios["Map_Marker_Size"] = (
            filtered_scenarios["Best_Cooling_C"]
            - filtered_scenarios["Best_Cooling_C"].min()
            + 0.01
        )

        fig = px.scatter_mapbox(
            filtered_scenarios,
            lat="Latitude",
            lon="Longitude",
            color="Recommended_Intervention",
            size="Map_Marker_Size",
            size_max=16,
            hover_data=[
                "Baseline_Predicted_LST_C",
                "Greening_Cooling_C",
                "Cool_Surface_Cooling_C",
                "Best_Cooling_C",
                "Population",
                "Zone_ID"
            ],
            zoom=10,
            height=600,
            title="Recommended Cooling Intervention by Location"
        )

        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 50, "l": 0, "b": 0}
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No locations match the selected intervention.")

    st.warning(
        "Cooling values are model-based comparative estimates and should be "
        "validated using local feasibility, cost, land availability, and field data."
    )


# --------------------------------------------------
# HEAT VULNERABILITY
# --------------------------------------------------

elif page == "Heat Vulnerability":

    st.header("Heat Vulnerability Index")

    st.markdown(
        """
        <div class="section-note">
            The Heat Vulnerability Index combines model-predicted heat hazard with
            population exposure to identify locations where heat may affect the
            greatest number of people.
        </div>
        """,
        unsafe_allow_html=True
    )

    vulnerability_category_options = sorted(
        vulnerability_map["Vulnerability_Category"]
        .dropna()
        .astype(str)
        .unique()
    )

    vulnerability_categories = st.multiselect(
        "Select Vulnerability Categories",
        options=vulnerability_category_options,
        default=vulnerability_category_options
    )

    filtered_vulnerability = vulnerability_map[
        vulnerability_map["Vulnerability_Category"]
        .astype(str)
        .isin(vulnerability_categories)
    ].copy()

    if len(filtered_vulnerability) > 0:
        filtered_vulnerability["Map_Marker_Size"] = (
            filtered_vulnerability["Heat_Vulnerability_Index"]
            - filtered_vulnerability["Heat_Vulnerability_Index"].min()
            + 0.01
        )

        fig = px.scatter_mapbox(
            filtered_vulnerability,
            lat="Latitude",
            lon="Longitude",
            color="Vulnerability_Category",
            size="Map_Marker_Size",
            size_max=16,
            hover_data=[
                "Baseline_Predicted_LST_C",
                "Population",
                "Heat_Hazard_Score",
                "Population_Exposure_Score",
                "Heat_Vulnerability_Index",
                "Zone_ID"
            ],
            zoom=10,
            height=600,
            title="Heat Vulnerability Across Chhatrapati Sambhajinagar"
        )

        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 50, "l": 0, "b": 0}
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No locations match the selected vulnerability categories.")

    st.subheader("Top High-Priority Vulnerability Zones")
    st.dataframe(vulnerability_zones, use_container_width=True, hide_index=True)


# --------------------------------------------------
# EXPLAINABLE AI
# --------------------------------------------------

elif page == "Explainable AI":

    st.header("Explainable AI: SHAP Feature Importance")

    st.markdown(
        """
        <div class="section-note">
            SHAP values show how strongly each Dataset V3 feature influenced
            XGBoost model predictions. They explain model behaviour but do not
            independently prove causation.
        </div>
        """,
        unsafe_allow_html=True
    )

    shap_plot_data = shap_importance.sort_values(
        by="Mean_Absolute_SHAP",
        ascending=True
    ).copy()

    fig = px.bar(
        shap_plot_data,
        x="Mean_Absolute_SHAP",
        y="Readable_Feature",
        orientation="h",
        title="Dataset V3 SHAP Global Feature Importance"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f4f8ff"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Feature-Importance Table")

    st.dataframe(
        shap_importance[
            ["Readable_Feature", "Mean_Absolute_SHAP"]
        ],
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div class="footer-text">
        Team AstroByte | Bharatiya Antariksh Hackathon 2026 |
        Urban Heat Mitigation and Cooling Strategy Optimization
    </div>
    """,
    unsafe_allow_html=True
)