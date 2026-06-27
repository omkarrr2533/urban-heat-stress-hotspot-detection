import os
import joblib
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="UrbanHeat AI · Thermal Intelligence Platform",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# DESIGN SYSTEM  —  "Thermal Command Center"
# ==================================================

st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=Figtree:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&display=swap" rel="stylesheet">

    <style>
    :root {
        --bg-0:#060611;
        --bg-1:#0a0a18;
        --bg-2:#0f0f22;
        --bg-3:#15152e;
        --glass:rgba(255,255,255,0.035);
        --glass-2:rgba(255,255,255,0.06);
        --bd-1:rgba(255,255,255,0.06);
        --bd-2:rgba(255,255,255,0.1);
        --fire:#ff5a1e;
        --fire-2:#ff7d3c;
        --ember:#ff9d2e;
        --gold:#ffc233;
        --cool:#27b6ff;
        --green:#26d07c;
        --red:#ff3b54;
        --txt:#edeef5;
        --txt-2:#9a9ab8;
        --txt-3:#6b6b88;
        --f-display:'Bricolage Grotesque',sans-serif;
        --f-body:'Figtree',sans-serif;
        --f-mono:'JetBrains Mono',monospace;
    }

    /* ---- hide streamlit chrome ---- */
    #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { display:none !important; }
    header[data-testid="stHeader"] { background:transparent !important; height:0 !important; }
    .block-container { padding-top:1.4rem !important; padding-bottom:2rem !important; max-width:1400px !important; }

    /* ---- base ---- */
    .stApp {
        background:var(--bg-0) !important;
        font-family:var(--f-body) !important;
        color:var(--txt) !important;
    }
    .stApp::before {
        content:'';
        position:fixed; inset:0; z-index:0; pointer-events:none;
        background:
            radial-gradient(ellipse 60% 50% at 10% 0%, rgba(255,90,30,0.10), transparent 60%),
            radial-gradient(ellipse 50% 50% at 90% 10%, rgba(255,157,46,0.07), transparent 55%),
            radial-gradient(ellipse 60% 60% at 80% 100%, rgba(39,182,255,0.05), transparent 60%);
        animation:drift 14s ease-in-out infinite;
    }
    .stApp::after {
        content:'';
        position:fixed; inset:0; z-index:0; pointer-events:none; opacity:0.45;
        background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
    }
    @keyframes drift { 0%,100%{opacity:0.7;} 50%{opacity:1;} }
    [data-testid="stAppViewContainer"] > .main { position:relative; z-index:1; }

    /* ---- sidebar ---- */
    [data-testid="stSidebar"] {
        background:linear-gradient(180deg, var(--bg-1), var(--bg-0)) !important;
        border-right:1px solid var(--bd-1) !important;
    }
    [data-testid="stSidebar"]::before {
        content:''; position:absolute; top:0; left:0; right:0; height:2px;
        background:linear-gradient(90deg, var(--fire), var(--ember), var(--gold), transparent);
    }
    [data-testid="stSidebar"] * { font-family:var(--f-body) !important; color:var(--txt) !important; }

    /* sidebar radio -> nav pills */
    [data-testid="stSidebar"] [role="radiogroup"] { gap:3px !important; }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        padding:9px 12px !important;
        border-radius:9px !important;
        border:1px solid transparent !important;
        transition:all .18s ease !important;
        cursor:pointer !important;
        margin:0 !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background:var(--glass) !important;
        border-color:var(--bd-1) !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label p {
        font-size:0.88rem !important; font-weight:500 !important; color:var(--txt-2) !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
        background:linear-gradient(90deg, rgba(255,90,30,0.16), rgba(255,90,30,0.02)) !important;
        border-color:rgba(255,90,30,0.32) !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
        color:var(--txt) !important; font-weight:600 !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] [data-testid="stMarkdownContainer"] { width:100%; }

    /* ---- typography ---- */
    h1,h2,h3 { font-family:var(--f-display) !important; color:var(--txt) !important; letter-spacing:-0.02em !important; }
    h1 { font-weight:800 !important; }
    h2 { font-weight:700 !important; border:none !important; padding:0 !important; }
    h3 { font-weight:600 !important; }
    p,li { font-family:var(--f-body) !important; color:var(--txt-2) !important; }

    /* ---- metrics (fallback) ---- */
    [data-testid="stMetric"] {
        background:var(--glass) !important; border:1px solid var(--bd-1) !important;
        border-radius:14px !important; padding:18px 20px !important;
        backdrop-filter:blur(14px) !important; position:relative; overflow:hidden;
        transition:transform .25s, border-color .25s !important;
    }
    [data-testid="stMetric"]::before {
        content:''; position:absolute; top:0; left:0; right:0; height:2px;
        background:linear-gradient(90deg,var(--fire),var(--ember)); opacity:.8;
    }
    [data-testid="stMetric"]:hover { transform:translateY(-3px); border-color:rgba(255,90,30,0.3) !important; }
    [data-testid="stMetricLabel"] p {
        font-family:var(--f-mono) !important; font-size:0.66rem !important; font-weight:500 !important;
        color:var(--txt-3) !important; text-transform:uppercase !important; letter-spacing:0.12em !important;
    }
    [data-testid="stMetricValue"] { font-family:var(--f-display) !important; font-weight:800 !important; color:var(--txt) !important; font-size:1.8rem !important; }
    [data-testid="stMetricDelta"] { font-family:var(--f-mono) !important; font-size:0.74rem !important; }

    /* ---- buttons ---- */
    .stButton > button {
        background:var(--glass-2) !important; border:1px solid var(--bd-2) !important;
        border-radius:10px !important; color:var(--txt) !important;
        font-family:var(--f-body) !important; font-weight:600 !important; transition:all .2s !important;
    }
    .stButton > button:hover { border-color:rgba(255,90,30,0.45) !important; background:rgba(255,90,30,0.08) !important; }
    [data-testid="stBaseButton-primary"] {
        background:linear-gradient(135deg,var(--fire),var(--ember)) !important; border:none !important;
        color:#0a0a12 !important; font-family:var(--f-display) !important; font-weight:700 !important;
        letter-spacing:0.01em !important; box-shadow:0 6px 26px rgba(255,90,30,0.4) !important;
    }
    [data-testid="stBaseButton-primary"]:hover { transform:translateY(-2px) !important; box-shadow:0 10px 36px rgba(255,90,30,0.55) !important; }
    [data-testid="stDownloadButton"] button {
        background:var(--glass-2) !important; border:1px solid rgba(38,208,124,0.4) !important;
        color:var(--green) !important; font-weight:600 !important;
    }

    /* ---- inputs ---- */
    div[data-baseweb="select"] > div {
        background:var(--bg-2) !important; border-color:var(--bd-2) !important;
        border-radius:10px !important; color:var(--txt) !important; font-family:var(--f-body) !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div { color:var(--txt) !important; }
    div[data-baseweb="popover"], div[data-baseweb="menu"] { background:var(--bg-2) !important; border:1px solid var(--bd-2) !important; border-radius:10px !important; }
    div[data-baseweb="menu"] li { color:var(--txt) !important; }
    div[data-baseweb="menu"] li:hover { background:var(--glass-2) !important; }
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        background:rgba(255,90,30,0.18) !important; border:1px solid rgba(255,90,30,0.4) !important;
        border-radius:7px !important; color:var(--txt) !important; font-family:var(--f-mono) !important; font-size:0.72rem !important;
    }
    label p { font-family:var(--f-body) !important; color:var(--txt-2) !important; font-size:0.84rem !important; }

    /* ---- slider ---- */
    [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] { background:var(--fire) !important; box-shadow:0 0 0 4px rgba(255,90,30,0.2) !important; }
    [data-testid="stSlider"] [data-baseweb="slider"] > div > div { background:linear-gradient(90deg,var(--fire),var(--ember)) !important; }

    /* ---- dataframe ---- */
    [data-testid="stDataFrame"] { background:var(--glass) !important; border:1px solid var(--bd-1) !important; border-radius:14px !important; overflow:hidden !important; }
    [data-testid="stDataFrame"] * { font-family:var(--f-mono) !important; font-size:0.78rem !important; color:var(--txt) !important; }

    /* ---- alerts ---- */
    [data-testid="stAlert"] { background:var(--glass) !important; border:1px solid var(--bd-2) !important; border-radius:12px !important; }
    [data-testid="stAlert"] p { color:var(--txt) !important; font-family:var(--f-body) !important; }

    /* ---- scrollbar ---- */
    ::-webkit-scrollbar { width:6px; height:6px; }
    ::-webkit-scrollbar-track { background:var(--bg-1); }
    ::-webkit-scrollbar-thumb { background:linear-gradient(var(--fire),var(--ember)); border-radius:3px; }

    /* ===================== CUSTOM COMPONENTS ===================== */

    /* hero */
    .hero {
        position:relative; overflow:hidden;
        border:1px solid var(--bd-1); border-radius:22px;
        padding:30px 34px; margin-bottom:22px;
        background:
            radial-gradient(ellipse 50% 140% at 0% 0%, rgba(255,90,30,0.18), transparent 55%),
            radial-gradient(ellipse 60% 160% at 100% 100%, rgba(255,194,51,0.10), transparent 55%),
            linear-gradient(135deg, var(--bg-2), var(--bg-1));
        box-shadow:0 20px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
    }
    .hero::before {
        content:''; position:absolute; top:-50%; right:-10%; width:55%; height:200%;
        background:conic-gradient(from 180deg at 50% 50%, transparent, rgba(255,90,30,0.10), transparent, rgba(255,194,51,0.08), transparent);
        animation:spin 22s linear infinite; pointer-events:none;
    }
    @keyframes spin { to { transform:rotate(360deg); } }
    .hero-grid { display:flex; justify-content:space-between; align-items:flex-start; gap:24px; flex-wrap:wrap; position:relative; z-index:1; }
    .hero-mark { display:flex; align-items:center; gap:16px; }
    .hero-logo {
        width:54px; height:54px; border-radius:15px; flex-shrink:0;
        display:flex; align-items:center; justify-content:center; font-size:1.7rem;
        background:linear-gradient(135deg, rgba(255,90,30,0.25), rgba(255,194,51,0.12));
        border:1px solid rgba(255,90,30,0.4);
        box-shadow:0 0 30px rgba(255,90,30,0.35), inset 0 0 18px rgba(255,90,30,0.18);
        animation:pulse 3s ease-in-out infinite;
    }
    @keyframes pulse { 0%,100%{box-shadow:0 0 30px rgba(255,90,30,0.3),inset 0 0 18px rgba(255,90,30,0.15);} 50%{box-shadow:0 0 48px rgba(255,90,30,0.55),inset 0 0 24px rgba(255,90,30,0.3);} }
    .hero-title {
        font-family:var(--f-display); font-size:2.5rem; font-weight:800; line-height:0.98; letter-spacing:-0.04em; margin:0;
        background:linear-gradient(110deg, #ffffff 0%, #ffd9c2 35%, #ff7d3c 70%, #ffc233 100%);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    }
    .hero-sub { font-family:var(--f-body); font-size:0.92rem; color:var(--txt-2); margin-top:7px; font-weight:400; max-width:440px; }
    .hero-pills { display:flex; gap:10px; flex-wrap:wrap; align-items:center; }
    .pill {
        display:flex; align-items:center; gap:7px; padding:8px 14px; border-radius:999px;
        background:var(--glass); border:1px solid var(--bd-2); backdrop-filter:blur(10px);
    }
    .pill-k { font-family:var(--f-mono); font-size:0.6rem; color:var(--txt-3); text-transform:uppercase; letter-spacing:0.1em; }
    .pill-v { font-family:var(--f-display); font-size:0.95rem; font-weight:700; color:var(--txt); }
    .pill-live { border-color:rgba(38,208,124,0.4); }
    .dot { width:7px; height:7px; border-radius:50%; background:var(--green); box-shadow:0 0 10px var(--green); animation:blink 1.6s ease-in-out infinite; }
    @keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

    /* kpi grid */
    .kpi-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:14px; margin:4px 0 6px; }
    .kpi {
        position:relative; overflow:hidden; border-radius:16px; padding:18px 18px 16px;
        background:linear-gradient(160deg, var(--glass-2), var(--glass));
        border:1px solid var(--bd-1); backdrop-filter:blur(14px);
        transition:transform .28s cubic-bezier(.2,.8,.2,1), border-color .28s, box-shadow .28s;
        animation:rise .5s ease both;
    }
    .kpi:hover { transform:translateY(-4px); border-color:color-mix(in srgb, var(--accent) 45%, transparent); box-shadow:0 14px 40px rgba(0,0,0,0.45), 0 0 28px color-mix(in srgb, var(--accent) 18%, transparent); }
    .kpi::after { content:''; position:absolute; top:0; left:0; width:100%; height:3px; background:var(--accent); opacity:0.85; }
    .kpi-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
    .kpi-icon {
        width:38px; height:38px; border-radius:11px; display:flex; align-items:center; justify-content:center; font-size:1.05rem;
        background:color-mix(in srgb, var(--accent) 16%, transparent);
        border:1px solid color-mix(in srgb, var(--accent) 35%, transparent);
    }
    .kpi-bars { display:flex; gap:3px; align-items:flex-end; height:22px; }
    .kpi-bars span { width:4px; border-radius:2px; background:color-mix(in srgb, var(--accent) 55%, transparent); }
    .kpi-value { font-family:var(--f-display); font-size:1.95rem; font-weight:800; color:var(--txt); line-height:1; letter-spacing:-0.02em; }
    .kpi-label { font-family:var(--f-mono); font-size:0.62rem; color:var(--txt-3); text-transform:uppercase; letter-spacing:0.12em; margin-top:8px; }
    .kpi-sub { font-family:var(--f-body); font-size:0.72rem; color:var(--txt-2); margin-top:3px; }
    @keyframes rise { from{opacity:0; transform:translateY(16px);} to{opacity:1; transform:translateY(0);} }
    .kpi:nth-child(1){animation-delay:.03s;} .kpi:nth-child(2){animation-delay:.09s;}
    .kpi:nth-child(3){animation-delay:.15s;} .kpi:nth-child(4){animation-delay:.21s;}
    .kpi:nth-child(5){animation-delay:.27s;} .kpi:nth-child(6){animation-delay:.33s;}

    /* section header */
    .sec-head { margin:26px 0 14px; }
    .sec-badge {
        display:inline-flex; align-items:center; gap:7px; padding:5px 12px; border-radius:999px;
        background:var(--glass); border:1px solid var(--bd-2);
        font-family:var(--f-mono); font-size:0.62rem; font-weight:500; color:var(--fire-2);
        text-transform:uppercase; letter-spacing:0.16em; margin-bottom:11px;
    }
    .sec-badge::before { content:''; width:6px; height:6px; border-radius:50%; background:var(--fire); box-shadow:0 0 8px var(--fire); }
    .sec-title { font-family:var(--f-display); font-size:1.7rem; font-weight:800; color:var(--txt); letter-spacing:-0.03em; line-height:1.05; }
    .sec-sub { font-family:var(--f-body); font-size:0.9rem; color:var(--txt-2); margin-top:6px; max-width:760px; line-height:1.55; }

    /* glass panel */
    .glass-panel {
        background:var(--glass); border:1px solid var(--bd-1); border-radius:16px;
        padding:20px 22px; margin-bottom:16px; backdrop-filter:blur(14px); position:relative; overflow:hidden;
    }
    .panel-heading { font-family:var(--f-display); font-size:0.85rem; font-weight:700; color:var(--txt); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:14px; }

    /* alerts */
    .alert { border-radius:13px; padding:15px 18px; margin:12px 0 18px; border:1px solid var(--bd-1); border-left:3px solid; font-family:var(--f-body); font-size:0.88rem; line-height:1.65; backdrop-filter:blur(10px); }
    .alert b { font-weight:600; color:var(--txt); }
    .alert-heat { background:rgba(255,90,30,0.08); border-left-color:var(--fire); color:rgba(255,225,210,0.9); }
    .alert-cool { background:rgba(38,208,124,0.08); border-left-color:var(--green); color:rgba(205,255,228,0.9); }
    .alert-info { background:rgba(39,182,255,0.07); border-left-color:var(--cool); color:rgba(205,238,255,0.9); }
    .alert-risk { background:rgba(255,59,84,0.08); border-left-color:var(--red); color:rgba(255,210,218,0.9); }

    /* steps */
    .steps { list-style:none; padding:0; margin:0; }
    .steps li { display:flex; gap:14px; align-items:flex-start; padding:11px 0; border-bottom:1px solid var(--bd-1); font-family:var(--f-body); font-size:0.88rem; color:rgba(220,220,240,0.86); line-height:1.55; }
    .steps li:last-child { border-bottom:none; }
    .step-n { font-family:var(--f-display); font-size:0.95rem; font-weight:800; color:#0a0a12; min-width:26px; height:26px; border-radius:8px; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg,var(--fire),var(--ember)); flex-shrink:0; }

    /* scenario cards */
    .scn { border-radius:13px; padding:15px 17px; margin:10px 0 14px; border:1px solid var(--bd-1); border-left:3px solid var(--c); background:var(--bg); }
    .scn-k { font-family:var(--f-mono); font-size:0.64rem; color:var(--c); text-transform:uppercase; letter-spacing:0.12em; margin-bottom:7px; }
    .scn-d { font-family:var(--f-body); font-size:0.78rem; color:var(--txt-2); margin-bottom:7px; }
    .scn-v { font-family:var(--f-display); font-size:1.65rem; font-weight:800; color:var(--txt); line-height:1; }
    .scn-unit { font-size:0.85rem; color:var(--txt-2); font-weight:500; }

    /* study + team cards in sidebar */
    .sb-card { background:var(--glass); border:1px solid var(--bd-1); border-radius:12px; padding:14px; margin-top:14px; }
    .sb-label { font-family:var(--f-mono); font-size:0.6rem; color:var(--fire-2); text-transform:uppercase; letter-spacing:0.14em; margin-bottom:8px; }
    .sb-val { font-family:var(--f-body); font-size:0.84rem; color:rgba(235,235,255,0.86); line-height:1.7; }

    /* footer */
    .footer { text-align:center; padding:22px; font-family:var(--f-mono); font-size:0.68rem; color:var(--txt-3); letter-spacing:0.08em; text-transform:uppercase; border-top:1px solid var(--bd-1); margin-top:30px; }

    /* empty-state */
    .empty { text-align:center; padding:48px 24px; border-radius:18px; border:1px dashed var(--bd-2); background:var(--glass); }
    .empty-ico { font-size:2.8rem; margin-bottom:14px; filter:drop-shadow(0 0 20px rgba(255,90,30,0.5)); animation:float 3s ease-in-out infinite; }
    @keyframes float { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-8px);} }
    .empty-t { font-family:var(--f-display); font-size:1.2rem; font-weight:700; color:var(--txt); margin-bottom:8px; }
    .empty-s { font-family:var(--f-body); font-size:0.9rem; color:var(--txt-2); max-width:440px; margin:0 auto; line-height:1.6; }

    /* team grid */
    .team { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }
    .team-c { text-align:center; padding:16px 12px; border-radius:13px; background:var(--glass); border:1px solid var(--bd-1); transition:transform .25s, border-color .25s; }
    .team-c:hover { transform:translateY(-3px); border-color:rgba(255,90,30,0.3); }
    .team-av { width:42px; height:42px; border-radius:50%; margin:0 auto 10px; display:flex; align-items:center; justify-content:center; font-family:var(--f-display); font-weight:800; font-size:1rem; color:#0a0a12; background:linear-gradient(135deg,var(--fire),var(--gold)); }
    .team-n { font-family:var(--f-display); font-size:0.92rem; font-weight:700; color:var(--txt); }
    .team-r { font-family:var(--f-mono); font-size:0.6rem; color:var(--fire-2); text-transform:uppercase; letter-spacing:0.08em; margin-top:4px; }

    /* generic list */
    .clean-list { font-family:var(--f-body); font-size:0.88rem; color:rgba(220,220,240,0.85); line-height:1.95; padding-left:18px; margin:0; }

    .stPlotlyChart { border-radius:12px; overflow:hidden; }
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# DATA LOADING
# ==================================================

DATA_FOLDER = "outputs/dashboard_data"


@st.cache_data
def load_data():
    hotspot_map        = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_hotspot_map_v3.csv"))
    scenario_map       = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_scenario_map_v3.csv"))
    priority_zones     = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_priority_zones_v3.csv"))
    intervention_zones = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_intervention_zones_v3.csv"))
    shap_importance    = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_shap_importance_v3.csv"))
    model_comparison   = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_model_comparison.csv"))
    scenario_summary   = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_scenario_summary_v3.csv"))
    kpis               = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_kpis_v3.csv"))
    vulnerability_map  = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_vulnerability_map_v3.csv"))
    vulnerability_zones= pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_vulnerability_zones_v3.csv"))
    return (
        hotspot_map, scenario_map, priority_zones, intervention_zones,
        shap_importance, model_comparison, scenario_summary, kpis,
        vulnerability_map, vulnerability_zones
    )


try:
    (
        hotspot_map, scenario_map, priority_zones, intervention_zones,
        shap_importance, model_comparison, scenario_summary, kpis,
        vulnerability_map, vulnerability_zones
    ) = load_data()
except FileNotFoundError as error:
    st.error("Dashboard data file not found. Run Notebook 13 first.")
    st.code(str(error))
    st.stop()


# ==================================================
# COLOUR SYSTEM  (thermal imaging palette)
# ==================================================

HEAT_COLOR_MAP = {
    "Low": "#1184d8", "Moderate": "#f59e0b", "High": "#f5511e", "Very High": "#c20f2f"
}
VULNERABILITY_COLOR_MAP = dict(HEAT_COLOR_MAP)
INTERVENTION_COLOR_MAP = {"Urban greening": "#26d07c", "Cool/permeable surfaces": "#27b6ff"}
HEAT_CATEGORY_ORDER = ["Low", "Moderate", "High", "Very High"]
MAP_LEGEND_TITLES = {
    "Heat_Category": "Heat Stress Level",
    "Vulnerability_Category": "Vulnerability Level",
    "Recommended_Intervention": "Recommended Strategy"
}


# ==================================================
# HELPERS
# ==================================================

def get_kpi_value(kpi_dict, possible_names, default=0):
    for name in possible_names:
        if name in kpi_dict:
            return kpi_dict[name]
    return default


def clean_map_columns(dataframe, columns_to_keep):
    return [c for c in columns_to_keep if c in dataframe.columns]


def format_hover_labels(hover_columns):
    label_map = {
        "Observed_LST_C": "Observed LST (°C)", "Predicted_LST_C": "Predicted LST (°C)",
        "Baseline_Predicted_LST_C": "Baseline Predicted LST (°C)",
        "Greening_Cooling_C": "+20% Green Cover Change (°C)",
        "Cool_Surface_Cooling_C": "Cool/Permeable Surface Change (°C)",
        "Best_Cooling_C": "Best Predicted LST Change (°C)", "NDVI": "NDVI", "NDBI": "NDBI",
        "Population": "Population Exposure", "LandCover_Class": "Land Cover", "Zone_ID": "Zone ID",
        "Heat_Hazard_Score": "Heat Hazard Score", "Population_Exposure_Score": "Population Exposure Score",
        "Heat_Vulnerability_Index": "Heat Vulnerability Index"
    }
    return {c: label_map.get(c, c.replace("_", " ")) for c in hover_columns}


def section_header(badge, title, subtitle=None):
    sub = f'<div class="sec-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f'<div class="sec-head"><div class="sec-badge">{badge}</div>'
        f'<div class="sec-title">{title}</div>{sub}</div>',
        unsafe_allow_html=True
    )


def kpi_card(icon, value, label, sub, accent, bars):
    bar_spans = "".join(
        f'<span style="height:{h}%"></span>' for h in bars
    )
    return (
        f'<div class="kpi" style="--accent:{accent}">'
        f'<div class="kpi-top"><div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-bars">{bar_spans}</div></div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-sub">{sub}</div></div>'
    )


def style_map(fig, zoom=11.4):
    existing_title = fig.layout.title.text or ""
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(zoom=zoom, pitch=0, bearing=0),
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#edeef5", font_family="JetBrains Mono, monospace",
        title=dict(text=existing_title, font=dict(family="Bricolage Grotesque, sans-serif", size=14, color="#edeef5")),
        legend=dict(
            bgcolor="rgba(255,255,255,0.94)", bordercolor="rgba(0,0,0,0.12)", borderwidth=1,
            font=dict(size=11, family="JetBrains Mono, monospace", color="#1a1a2e"),
            title_font=dict(size=11, family="JetBrains Mono, monospace", color="#1a1a2e"),
            x=0.99, y=0.98, xanchor="right", yanchor="top"
        )
    )
    return fig


def style_chart(fig):
    existing_title = fig.layout.title.text or ""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(12,12,26,0.6)",
        font_color="#edeef5", font_family="JetBrains Mono, monospace",
        title=dict(text=existing_title, font=dict(color="#edeef5", family="Bricolage Grotesque, sans-serif", size=15)),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)",
                   zerolinecolor="rgba(255,255,255,0.08)",
                   tickfont=dict(family="JetBrains Mono, monospace", size=10, color="#9a9ab8")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)",
                   zerolinecolor="rgba(255,255,255,0.08)",
                   tickfont=dict(family="JetBrains Mono, monospace", size=10, color="#9a9ab8")),
        legend=dict(bgcolor="rgba(10,10,24,0.85)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1,
                    font=dict(family="JetBrains Mono, monospace", size=11, color="#edeef5"))
    )
    return fig


def make_small_clean_map(dataframe, color_column, hover_columns, title, color_map, height=600):
    map_data = dataframe.copy()
    if len(map_data) > 2000:
        map_data = map_data.sample(n=2000, random_state=42)
    category_order = HEAT_CATEGORY_ORDER if color_column in ["Heat_Category", "Vulnerability_Category"] else None
    fig = px.scatter_mapbox(
        map_data, lat="Latitude", lon="Longitude", color=color_column,
        hover_data=hover_columns, labels=format_hover_labels(hover_columns),
        zoom=11.4, height=height, title=title, color_discrete_map=color_map,
        category_orders={color_column: category_order} if category_order else None
    )
    fig.update_traces(marker=dict(size=9, opacity=0.85))
    fig.update_layout(legend_title_text=MAP_LEGEND_TITLES.get(color_column, color_column.replace("_", " ")))
    return style_map(fig, zoom=11.4)


def get_scenario_display_name(scenario_name):
    s = str(scenario_name).lower()
    if "green" in s or "vegetation" in s:
        return "🌿 +20% Green Cover"
    if "cool" in s or "permeable" in s:
        return "🏙️ Cool / Permeable Surface"
    return str(scenario_name)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.markdown(
    """
    <div style="display:flex;align-items:center;gap:11px;padding:6px 0 8px;">
        <div style="width:40px;height:40px;border-radius:12px;display:flex;align-items:center;
                    justify-content:center;font-size:1.3rem;
                    background:linear-gradient(135deg,rgba(255,90,30,0.25),rgba(255,194,51,0.12));
                    border:1px solid rgba(255,90,30,0.4);box-shadow:0 0 22px rgba(255,90,30,0.35);">🔥</div>
        <div>
            <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:1.12rem;font-weight:800;
                        color:#edeef5;letter-spacing:-0.02em;line-height:1;">UrbanHeat AI</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#ff7d3c;
                        text-transform:uppercase;letter-spacing:0.14em;margin-top:4px;">Thermal Intelligence</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#6b6b88;"
    "text-transform:uppercase;letter-spacing:0.14em;margin:14px 0 8px;'>— Navigation</div>",
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Select dashboard section",
    [
        "🏠  Project Overview",
        "🔥  Urban Heat Hotspots",
        "📊  Heat Drivers",
        "👥  Heat Vulnerability",
        "🛰  Cooling Strategy",
        "✓  Model Validation",
        "ℹ  About Project"
    ],
    label_visibility="collapsed"
)
# normalise (strip emoji prefix) so downstream logic is unchanged
page = page.split("  ", 1)[-1].strip()

st.sidebar.markdown(
    """
    <div class="sb-card">
        <div class="sb-label">◎ Study Area</div>
        <div class="sb-val">
            Chhatrapati Sambhajinagar<br>(Aurangabad), Maharashtra<br><br>
            <span style="color:#9a9ab8;">Year</span> &nbsp;2025<br>
            <span style="color:#9a9ab8;">Data</span> &nbsp;Sentinel-2 · Landsat 8/9<br>
            <span style="color:#9a9ab8;">Model</span> &nbsp;XGBoost
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <div class="sb-card">
        <div class="sb-label">⬡ Team AstroByte</div>
        <div class="sb-val">
            <b style="color:#edeef5;">Priyal Deshmukh</b><br>
            <span style="color:#9a9ab8;font-size:0.78rem;">AI/ML Lead</span><br><br>
            <b style="color:#edeef5;">Srushti Bawaskar</b><br>
            <span style="color:#9a9ab8;font-size:0.78rem;">Geospatial & Data Lead</span><br><br>
            <b style="color:#edeef5;">Rishika Deshmukh</b><br>
            <span style="color:#9a9ab8;font-size:0.78rem;">Research & Dashboard Lead</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HERO HEADER  (persistent)
# ==================================================

kpi_values = dict(zip(kpis["Metric"], kpis["Value"]))
hero_r2 = float(get_kpi_value(kpi_values, ["Dataset V3 XGBoost R2", "Dataset V3 XGBoost R²"], 0))
hero_locs = int(float(get_kpi_value(kpi_values, ["Total Sampled Locations", "Sampled Locations"], 0)))

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-grid">
            <div class="hero-mark">
                <div class="hero-logo">🔥</div>
                <div>
                    <div class="hero-title">URBANHEAT&nbsp;AI</div>
                    <div class="hero-sub">Satellite-driven machine learning for urban heat-stress
                    detection &amp; cooling-strategy optimization</div>
                </div>
            </div>
            <div class="hero-pills">
                <div class="pill pill-live"><span class="dot"></span>
                    <div><div class="pill-k">Status</div><div class="pill-v">Live</div></div></div>
                <div class="pill"><div><div class="pill-k">Model R²</div><div class="pill-v">{hero_r2:.3f}</div></div></div>
                <div class="pill"><div><div class="pill-k">Locations</div><div class="pill-v">{hero_locs:,}</div></div></div>
                <div class="pill"><div><div class="pill-k">Region</div><div class="pill-v">C. Sambhajinagar</div></div></div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# PROJECT OVERVIEW
# ==================================================

if page == "Project Overview":

    section_header(
        "Mission Control",
        "Urban Heat Intelligence Overview",
        "A geospatial decision-support system that pinpoints heat-stress hotspots, ranks "
        "population vulnerability, explains heat drivers, and simulates cooling interventions."
    )

    r2_value = float(get_kpi_value(kpi_values, ["Dataset V3 XGBoost R2", "Dataset V3 XGBoost R²"], 0))
    mae_value = float(get_kpi_value(kpi_values, ["Dataset V3 XGBoost MAE (C)", "Dataset V3 XGBoost MAE"], 0))
    total_locations = int(float(get_kpi_value(kpi_values, ["Total Sampled Locations", "Sampled Locations"], 0)))
    priority_count = int(float(get_kpi_value(kpi_values, ["High Priority Hotspot Zones", "High-Priority Hotspot Zones"], 0)))

    if "Heat_Category" in hotspot_map.columns:
        high_heat_share = (
            hotspot_map["Heat_Category"].astype(str)
            .str.contains("High", case=False, na=False).mean() * 100
        )
    else:
        high_heat_share = 0.0

    cards = [
        kpi_card("◎", f"{r2_value:.3f}", "Model R² Score", "Spatial CV accuracy", "#26d07c", [40, 65, 50, 80, 70]),
        kpi_card("△", f"{mae_value:.2f}°", "Mean Abs Error", "Average LST deviation", "#27b6ff", [60, 45, 70, 40, 55]),
        kpi_card("⬡", f"{total_locations:,}", "Total Locations", "Sampled grid points", "#ffc233", [50, 70, 60, 85, 75]),
        kpi_card("🔥", f"{priority_count}", "Priority Zones", "High-priority hotspots", "#ff5a1e", [70, 55, 85, 60, 90]),
        kpi_card("▦", f"{high_heat_share:.1f}%", "High Heat Share", "Zones at High / Very High", "#cc1133", [80, 65, 75, 90, 70]),
    ]
    st.markdown(f'<div class="kpi-grid">{"".join(cards)}</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass-panel" style="margin-top:18px;">
            <div class="panel-heading">🧭 How to Use This Platform</div>
            <ol class="steps">
                <li><span class="step-n">1</span><span><b>Locate heat stress</b> — Urban Heat Hotspots surfaces High and Very High heat zones.</span></li>
                <li><span class="step-n">2</span><span><b>Prioritize people at risk</b> — Heat Vulnerability overlays heat with population exposure.</span></li>
                <li><span class="step-n">3</span><span><b>Understand why</b> — Heat Drivers reveals which variables most influence predicted LST.</span></li>
                <li><span class="step-n">4</span><span><b>Compare interventions</b> — Cooling Strategy runs real-time XGBoost simulations.</span></li>
                <li><span class="step-n">5</span><span><b>Verify before action</b> — priority-zone tables support field assessment and planning.</span></li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

    left_col, right_col = st.columns([1.45, 0.55])

    with left_col:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-heading">🔥 Urban Heat Hotspot Map</div>', unsafe_allow_html=True)
        heat_options = [c for c in HEAT_CATEGORY_ORDER if c in hotspot_map["Heat_Category"].dropna().astype(str).unique()]
        selected_heat = st.multiselect("Filter heat-stress categories", options=heat_options, default=heat_options, key="overview_heat_filter")
        filtered_hotspots = hotspot_map[hotspot_map["Heat_Category"].astype(str).isin(selected_heat)].copy()
        if len(filtered_hotspots) > 0:
            hover_columns = clean_map_columns(filtered_hotspots, ["Observed_LST_C", "Predicted_LST_C", "NDVI", "NDBI", "Population", "LandCover_Class", "Zone_ID"])
            fig = make_small_clean_map(filtered_hotspots, "Heat_Category", hover_columns, "Land Surface Temperature (°C)", HEAT_COLOR_MAP, height=440)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No locations match the selected heat categories.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-heading">Heat Stress Distribution</div>', unsafe_allow_html=True)
        if "Heat_Category" in hotspot_map.columns:
            heat_counts = (hotspot_map["Heat_Category"].astype(str).value_counts().reindex(HEAT_CATEGORY_ORDER, fill_value=0).reset_index())
            heat_counts.columns = ["Heat Category", "Count"]
            fig = px.pie(heat_counts, names="Heat Category", values="Count", hole=0.66, color="Heat Category", color_discrete_map=HEAT_COLOR_MAP, category_orders={"Heat Category": HEAT_CATEGORY_ORDER})
            fig.update_traces(textinfo="none", hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>", marker=dict(line=dict(color="rgba(10,10,24,0.9)", width=2)))
            fig.update_layout(
                height=320, margin=dict(l=5, r=5, t=10, b=5), paper_bgcolor="rgba(0,0,0,0)",
                font_color="#edeef5", font_family="JetBrains Mono, monospace", showlegend=True,
                legend=dict(orientation="v", x=1.02, y=0.5, xanchor="left", yanchor="middle", font=dict(size=10, family="JetBrains Mono, monospace", color="#edeef5"), bgcolor="rgba(0,0,0,0)"),
                annotations=[dict(text="<b>HEAT</b>", x=0.5, y=0.5, font=dict(size=15, color="#ff7d3c", family="Bricolage Grotesque, sans-serif"), showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1.05, 0.95])

    with col_a:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-heading">📊 Top Heat Drivers (SHAP)</div>', unsafe_allow_html=True)
        shap_plot = shap_importance.sort_values("Mean_Absolute_SHAP", ascending=True).copy()
        fig = px.bar(shap_plot, x="Mean_Absolute_SHAP", y="Readable_Feature", orientation="h", color="Mean_Absolute_SHAP", color_continuous_scale=["#27b6ff", "#ffc233", "#ff5a1e", "#cc1133"])
        fig.update_layout(coloraxis_showscale=False, height=330, title="", xaxis_title="Mean |SHAP|", yaxis_title="")
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-heading">❄️ Scenario Cooling Predictions</div>', unsafe_allow_html=True)
        if len(scenario_summary) > 0:
            for _, row in scenario_summary.iterrows():
                scenario_name = str(row["Scenario"])
                cooling_value = float(row["Mean_Cooling_C"])
                display_name = get_scenario_display_name(scenario_name)
                is_green = "green" in scenario_name.lower() or "vegetation" in scenario_name.lower()
                c = "#26d07c" if is_green else "#27b6ff"
                bg = "rgba(38,208,124,0.07)" if is_green else "rgba(39,182,255,0.07)"
                st.markdown(
                    f'<div class="scn" style="--c:{c};--bg:{bg};">'
                    f'<div class="scn-k">{display_name}</div>'
                    f'<div class="scn-d">Predicted LST Δ from baseline</div>'
                    f'<div class="scn-v">{cooling_value:.3f}<span class="scn-unit"> °C</span></div></div>',
                    unsafe_allow_html=True
                )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="alert alert-info"><b>💡 Planning insight:</b> combine hotspot intensity, vulnerability level,
        and scenario-based predicted LST change to prioritize where interventions deliver the most impact.</div>
        <div class="alert alert-risk"><b>Decision-support disclaimer:</b> predicted LST changes are model-based
        estimates supporting comparison and prioritization — not guaranteed real-world outcomes. Field verification,
        feasibility, costs, land availability, and local conditions must be assessed before implementation.</div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# URBAN HEAT HOTSPOTS
# ==================================================

elif page == "Urban Heat Hotspots":

    section_header(
        "Hazard Mapping", "Urban Heat Hotspots",
        "Identify locations with elevated observed land surface temperature (LST, °C) and "
        "prioritize concentrated hotspot zones for intervention."
    )

    heat_options = [c for c in HEAT_CATEGORY_ORDER if c in hotspot_map["Heat_Category"].dropna().astype(str).unique()]
    selected_heat = st.multiselect("Select heat-stress categories", options=heat_options, default=heat_options, key="hotspot_heat_filter")
    filtered_hotspots = hotspot_map[hotspot_map["Heat_Category"].astype(str).isin(selected_heat)].copy()

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    if len(filtered_hotspots) > 0:
        hover_columns = clean_map_columns(filtered_hotspots, ["Observed_LST_C", "Predicted_LST_C", "NDVI", "NDBI", "Population", "LandCover_Class", "Zone_ID"])
        fig = make_small_clean_map(filtered_hotspots, "Heat_Category", hover_columns, "Urban Heat-Stress Distribution — LST (°C)", HEAT_COLOR_MAP, height=610)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No locations match the selected heat categories.")
    st.markdown("</div>", unsafe_allow_html=True)

    section_header("Field Priorities", "Top High-Priority Hotspot Zones")
    st.dataframe(priority_zones, use_container_width=True, hide_index=True)


# ==================================================
# HEAT DRIVERS
# ==================================================

elif page == "Heat Drivers":

    section_header(
        "Explainable AI", "Heat Drivers & Feature Attribution",
        "Understand which environmental and urban features most strongly influence predicted "
        "land surface temperature (LST, °C) in the XGBoost model."
    )

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    shap_plot = shap_importance.sort_values("Mean_Absolute_SHAP", ascending=True).copy()
    fig = px.bar(shap_plot, x="Mean_Absolute_SHAP", y="Readable_Feature", orientation="h", color="Mean_Absolute_SHAP", title="Global SHAP Feature Importance", color_continuous_scale=["#27b6ff", "#ffc233", "#ff5a1e", "#cc1133"])
    fig.update_layout(coloraxis_showscale=False, height=500, xaxis_title="Mean Absolute SHAP Value", yaxis_title="")
    st.plotly_chart(style_chart(fig), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="alert alert-info"><b>Interpretation:</b> a higher mean absolute SHAP value means that feature
        has a stronger overall influence on model predictions. These results support transparency, but do not
        independently prove causation.</div>
        """,
        unsafe_allow_html=True
    )
    st.dataframe(shap_importance[["Readable_Feature", "Mean_Absolute_SHAP"]], use_container_width=True, hide_index=True)


# ==================================================
# HEAT VULNERABILITY
# ==================================================

elif page == "Heat Vulnerability":

    section_header(
        "Population Risk", "Heat Vulnerability",
        "Prioritize areas where predicted heat hazard overlaps with higher population exposure — "
        "the hottest location is not always the most vulnerable one."
    )

    vulnerability_options = [c for c in HEAT_CATEGORY_ORDER if c in vulnerability_map["Vulnerability_Category"].dropna().astype(str).unique()]
    selected_vulnerability = st.multiselect("Select vulnerability categories", options=vulnerability_options, default=vulnerability_options)
    filtered_vulnerability = vulnerability_map[vulnerability_map["Vulnerability_Category"].astype(str).isin(selected_vulnerability)].copy()

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    if len(filtered_vulnerability) > 0:
        hover_columns = clean_map_columns(filtered_vulnerability, ["Baseline_Predicted_LST_C", "Population", "Heat_Hazard_Score", "Population_Exposure_Score", "Heat_Vulnerability_Index", "Zone_ID"])
        fig = make_small_clean_map(filtered_vulnerability, "Vulnerability_Category", hover_columns, "Population-Aware Heat Vulnerability — Predicted LST (°C)", VULNERABILITY_COLOR_MAP, height=610)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No locations match the selected vulnerability categories.")
    st.markdown("</div>", unsafe_allow_html=True)

    section_header("Field Priorities", "Top High-Priority Vulnerability Zones")
    st.dataframe(vulnerability_zones, use_container_width=True, hide_index=True)


# ==================================================
# COOLING STRATEGY
# ==================================================

elif page == "Cooling Strategy":

    section_header(
        "Live Simulation", "🛰 AI Cooling Intervention Simulator",
        "Real-time AI prediction with the trained XGBoost model — interventions modify urban "
        "environmental indicators and the model re-predicts Land Surface Temperature through inference."
    )

    MODEL_PATH = Path("outputs/models/xgboost_v3_landcover_model.pkl")
    DATA_PATH  = Path("data/processed/featured_uhi_v3.csv")

    MODEL_FEATURES = [
        "NDVI", "NDBI", "Elevation", "Population",
        "LandCover_Bare_sparse_vegetation", "LandCover_Built-up land", "LandCover_Cropland",
        "LandCover_Grassland", "LandCover_Permanent_water_bodies", "LandCover_Shrubland", "LandCover_Tree cover",
    ]

    @st.cache_resource
    def load_ai_model():
        return joblib.load(MODEL_PATH)

    @st.cache_data
    def load_simulation_dataset():
        return pd.read_csv(DATA_PATH)

    try:
        model = load_ai_model()
        simulation_df = load_simulation_dataset().copy()
    except FileNotFoundError as err:
        st.markdown('<div class="alert alert-risk"><b>Model or data file missing.</b> Run the training notebooks to generate the XGBoost model and featured dataset.</div>', unsafe_allow_html=True)
        st.code(str(err))
        st.stop()
    except ModuleNotFoundError as err:
        st.markdown(f'<div class="alert alert-risk"><b>Missing dependency:</b> {err}. Install it with <code>pip install xgboost</code> and restart.</div>', unsafe_allow_html=True)
        st.stop()

    missing_features = [f for f in MODEL_FEATURES if f not in simulation_df.columns]
    if missing_features:
        st.markdown('<div class="alert alert-risk"><b>Required model features are missing:</b><br>' + "<br>".join(missing_features) + '</div>', unsafe_allow_html=True)
        st.stop()

    left_col, right_col = st.columns([1, 1.8])

    with left_col:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-heading">⚙ Cooling Interventions</div>', unsafe_allow_html=True)
        green_cover       = st.slider("🌿 Green Cover Increase (%)", 0, 100, 20, 1)
        tree_cover        = st.slider("🌳 Tree Plantation (%)", 0, 100, 25, 1)
        cool_roofs        = st.slider("🏠 Cool Roof Adoption (%)", 0, 100, 15, 1)
        permeable_surface = st.slider("🧱 Permeable Surface (%)", 0, 100, 15, 1)
        builtup_reduction = st.slider("🏢 Built-up Reduction (%)", 0, 100, 10, 1)
        run_simulation = st.button("🛰 Run AI Simulation", use_container_width=True, type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown(
            """
            <div class="glass-panel">
                <div class="panel-heading">⟶ Simulation Pipeline</div>
                <ol class="steps">
                    <li><span class="step-n">1</span><span>Selected interventions modify environmental indicators.</span></li>
                    <li><span class="step-n">2</span><span>NDVI increases with vegetation-related actions.</span></li>
                    <li><span class="step-n">3</span><span>NDBI decreases with built-up reduction.</span></li>
                    <li><span class="step-n">4</span><span>Land-cover proportions are updated and normalized.</span></li>
                    <li><span class="step-n">5</span><span>The trained XGBoost model predicts the new LST.</span></li>
                    <li><span class="step-n">6</span><span>Results are compared against the original scenario.</span></li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )

    def _clip(series, low=None, high=None):
        if low is not None:
            series = np.maximum(series, low)
        if high is not None:
            series = np.minimum(series, high)
        return series

    def normalize_landcover(df):
        cols = ["LandCover_Bare_sparse_vegetation", "LandCover_Built-up land", "LandCover_Cropland",
                "LandCover_Grassland", "LandCover_Permanent_water_bodies", "LandCover_Shrubland", "LandCover_Tree cover"]
        total = df[cols].sum(axis=1).replace(0, 1)
        df[cols] = df[cols].div(total, axis=0)
        return df

    def apply_interventions(df):
        s = df.copy()
        ndvi_increase = green_cover * 0.0025 + tree_cover * 0.0035 + permeable_surface * 0.0010
        s["NDVI"] = _clip(s["NDVI"] + ndvi_increase, -1, 1)
        ndbi_decrease = builtup_reduction * 0.0020 + green_cover * 0.0010 + tree_cover * 0.0010
        s["NDBI"] = _clip(s["NDBI"] - ndbi_decrease, -1, 1)
        s["LandCover_Tree cover"]             = _clip(s["LandCover_Tree cover"] + tree_cover * 0.004 + green_cover * 0.002, 0)
        s["LandCover_Built-up land"]          = _clip(s["LandCover_Built-up land"] - builtup_reduction * 0.004 - permeable_surface * 0.002 - cool_roofs * 0.001, 0)
        s["LandCover_Cropland"]               = _clip(s["LandCover_Cropland"] + green_cover * 0.0005, 0)
        s["LandCover_Grassland"]              = _clip(s["LandCover_Grassland"] + green_cover * 0.001 + permeable_surface * 0.001, 0)
        s["LandCover_Shrubland"]              = _clip(s["LandCover_Shrubland"] + green_cover * 0.0005, 0)
        s["LandCover_Bare_sparse_vegetation"] = _clip(s["LandCover_Bare_sparse_vegetation"] - green_cover * 0.001, 0)
        s["LandCover_Permanent_water_bodies"] = _clip(s["LandCover_Permanent_water_bodies"], 0)
        return normalize_landcover(s)

    def classify_hotspot(lst):
        if lst >= 42:
            return "Extreme"
        if lst >= 38:
            return "Very High"
        if lst >= 34:
            return "High"
        if lst >= 30:
            return "Moderate"
        return "Low"

    if run_simulation:
        simulated_df = apply_interventions(simulation_df)
        simulated_df["LST_Before"]            = model.predict(simulation_df[MODEL_FEATURES])
        simulated_df["LST_After"]             = model.predict(simulated_df[MODEL_FEATURES])
        simulated_df["Temperature_Reduction"] = simulated_df["LST_Before"] - simulated_df["LST_After"]
        simulated_df["Hotspot_Before"]        = simulated_df["LST_Before"].apply(classify_hotspot)
        simulated_df["Hotspot_After"]         = simulated_df["LST_After"].apply(classify_hotspot)

        avg_before, avg_after = simulated_df["LST_Before"].mean(), simulated_df["LST_After"].mean()
        max_before, max_after = simulated_df["LST_Before"].max(), simulated_df["LST_After"].max()
        reduction = avg_before - avg_after
        pixels_cooled_pct = (simulated_df["Temperature_Reduction"] > 0).mean() * 100
        # "Hotspots" = Extreme zones (LST >= 42 deg C): the genuinely dangerous, actionable areas.
        # This city's land-surface temps are uniformly high (>30 deg C almost everywhere), so a
        # "not Low" count can't reflect improvement -- the Extreme threshold tracks real heat-risk reduction.
        hotspots_before = (simulated_df["Hotspot_Before"] == "Extreme").sum()
        hotspots_after  = (simulated_df["Hotspot_After"] == "Extreme").sum()
        improvement = 0 if hotspots_before == 0 else (hotspots_before - hotspots_after) / hotspots_before * 100

        section_header("Results", "📊 AI Simulation Results")
        cards = [
            kpi_card("△", f"{avg_before:.2f}°", "Avg LST Before", "Baseline mean", "#ff5a1e", [70, 80, 75, 85, 78]),
            kpi_card("▽", f"{avg_after:.2f}°", "Avg LST After", f"↓ {reduction:.2f}°C cooler", "#26d07c", [60, 50, 55, 45, 40]),
            kpi_card("▲", f"{max_before:.2f}°", "Max LST Before", "Hottest point", "#cc1133", [85, 90, 80, 95, 88]),
            kpi_card("▼", f"{max_after:.2f}°", "Max LST After", f"↓ {(max_before-max_after):.2f}°C", "#27b6ff", [70, 60, 65, 55, 50]),
        ]
        st.markdown(f'<div class="kpi-grid">{"".join(cards)}</div>', unsafe_allow_html=True)
        cards2 = [
            kpi_card("🔥", f"{int(hotspots_before):,}", "Extreme Zones Before", "LST ≥ 42°C", "#ff5a1e", [80, 75, 85, 70, 78]),
            kpi_card("❄", f"{int(hotspots_after):,}", "Extreme Zones After", "Post-intervention", "#27b6ff", [55, 45, 50, 40, 48]),
            kpi_card("✦", f"{improvement:.1f}%", "Extreme-Zone Reduction", "Fewer ≥42°C zones", "#26d07c", [50, 65, 70, 85, 90]),
            kpi_card("💧", f"{pixels_cooled_pct:.1f}%", "Pixels Cooled", "Net temperature drop", "#ffc233", [60, 70, 80, 88, 92]),
        ]
        st.markdown(f'<div class="kpi-grid">{"".join(cards2)}</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-heading">📈 Average LST Comparison</div>', unsafe_allow_html=True)
            comparison_df = pd.DataFrame({"Scenario": ["Before", "After"], "Average LST": [avg_before, avg_after]})
            fig = px.bar(comparison_df, x="Scenario", y="Average LST", color="Scenario", text="Average LST", color_discrete_sequence=["#ff5a1e", "#26d07c"])
            fig.update_traces(texttemplate="%{text:.2f} °C", textposition="outside", textfont=dict(family="Bricolage Grotesque", size=14))
            fig.update_layout(height=380, showlegend=False, xaxis_title="", yaxis_title="Average LST (°C)")
            st.plotly_chart(style_chart(fig), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-heading">📉 Pixel-wise Temperature Reduction</div>', unsafe_allow_html=True)
            fig = px.histogram(simulated_df, x="Temperature_Reduction", nbins=40, color_discrete_sequence=["#26d07c"])
            fig.update_layout(height=380, xaxis_title="Temperature Reduction (°C)", yaxis_title="Pixel Count")
            st.plotly_chart(style_chart(fig), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-heading">🛰 AI Predicted Heat Hotspots (After Intervention)</div>', unsafe_allow_html=True)
        hotspot_colors = {"Low": "#1184d8", "Moderate": "#f59e0b", "High": "#f5511e", "Very High": "#c20f2f", "Extreme": "#7a0a1e"}
        fig = px.scatter_mapbox(
            simulated_df, lat="Latitude", lon="Longitude", color="Hotspot_After", hover_name="Hotspot_After",
            hover_data={"Latitude": ":.4f", "Longitude": ":.4f", "LST_Before": ":.2f", "LST_After": ":.2f", "Temperature_Reduction": ":.2f"},
            color_discrete_map=hotspot_colors,
            category_orders={"Hotspot_After": ["Low", "Moderate", "High", "Very High", "Extreme"]},
            zoom=11.4, height=600
        )
        fig.update_traces(marker=dict(size=9, opacity=0.85))
        fig.update_layout(
            mapbox_style="carto-positron", margin=dict(l=0, r=0, t=0, b=0), legend_title="Hotspot Category",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(bgcolor="rgba(255,255,255,0.94)", bordercolor="rgba(0,0,0,0.12)", borderwidth=1,
                        font=dict(size=11, family="JetBrains Mono, monospace", color="#1a1a2e"),
                        title_font=dict(size=11, family="JetBrains Mono, monospace", color="#1a1a2e"))
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        c3, c4 = st.columns([1.2, 0.8])
        with c3:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-heading">🔥 Updated Hotspot Classification</div>', unsafe_allow_html=True)
            hotspot_table = (
                simulated_df[["Latitude", "Longitude", "LST_Before", "LST_After", "Temperature_Reduction", "Hotspot_Before", "Hotspot_After"]]
                .sort_values("LST_After", ascending=False).reset_index(drop=True)
                .rename(columns={"LST_Before": "Before (°C)", "LST_After": "After (°C)", "Temperature_Reduction": "Cooling (°C)", "Hotspot_Before": "Category Before", "Hotspot_After": "Category After"})
            )
            st.dataframe(hotspot_table, use_container_width=True, hide_index=True, height=360)
            st.markdown("</div>", unsafe_allow_html=True)
        with c4:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-heading">📍 Category Summary</div>', unsafe_allow_html=True)
            before_summary = simulated_df["Hotspot_Before"].value_counts().rename("Before")
            after_summary = simulated_df["Hotspot_After"].value_counts().rename("After")
            hotspot_summary = (pd.concat([before_summary, after_summary], axis=1).fillna(0).astype(int).reindex(["Extreme", "Very High", "High", "Moderate", "Low"], fill_value=0).reset_index())
            hotspot_summary.columns = ["Hotspot Category", "Before", "After"]
            fig = px.bar(hotspot_summary, x="Hotspot Category", y=["Before", "After"], barmode="group", color_discrete_sequence=["#ff5a1e", "#26d07c"])
            fig.update_layout(height=360, yaxis_title="Pixels", xaxis_title="", legend_title="")
            fig.update_xaxes(tickangle=-30)
            st.plotly_chart(style_chart(fig), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        recommendations = []
        if avg_after >= 40:
            recommendations.append("🔥 Immediate intervention is recommended for high-temperature urban zones.")
        if tree_cover < 30:
            recommendations.append("🌳 Increase urban tree plantation to improve canopy density and shading.")
        if green_cover < 30:
            recommendations.append("🌿 Develop additional green parks, roadside plantations, and urban forests.")
        if cool_roofs < 25:
            recommendations.append("🏠 Promote cool roof technology for public and commercial buildings.")
        if permeable_surface < 25:
            recommendations.append("🧱 Replace impervious pavements with permeable materials wherever feasible.")
        if builtup_reduction < 20:
            recommendations.append("🏢 Encourage redevelopment strategies that reduce excessive built-up density.")
        if reduction >= 2:
            recommendations.append("❄ The selected scenario shows strong cooling potential and should be prioritized.")
        if not recommendations:
            recommendations.append("✅ The current strategy is balanced. Continue monitoring urban heat conditions.")

        section_header("Advisory", "🏛 AI Municipal Recommendation")
        rec_html = "".join(f'<div style="padding:9px 0;border-bottom:1px solid var(--bd-1);font-family:var(--f-body);font-size:0.9rem;color:rgba(205,255,228,0.92);">{r}</div>' for r in recommendations)
        st.markdown(f'<div class="alert alert-cool" style="padding:6px 18px;">{rec_html}</div>', unsafe_allow_html=True)

        c5, c6 = st.columns([1, 1])
        with c5:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-heading">📋 Simulation Summary</div>', unsafe_allow_html=True)
            summary_df = pd.DataFrame({
                "Metric": ["Average LST Before (°C)", "Average LST After (°C)", "Temperature Reduction (°C)", "Maximum LST Before (°C)", "Maximum LST After (°C)", "Extreme Zones Before (≥42°C)", "Extreme Zones After (≥42°C)", "Extreme-Zone Reduction (%)", "Pixels Cooled (%)"],
                "Value": [round(avg_before, 2), round(avg_after, 2), round(reduction, 2), round(max_before, 2), round(max_after, 2), int(hotspots_before), int(hotspots_after), round(improvement, 2), round(pixels_cooled_pct, 2)]
            })
            st.dataframe(summary_df, use_container_width=True, hide_index=True, height=320)
            st.markdown("</div>", unsafe_allow_html=True)
        with c6:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-heading">📥 Export & Disclaimer</div>', unsafe_allow_html=True)
            csv = simulated_df.to_csv(index=False).encode("utf-8")
            st.download_button("📄 Download Simulation Results (CSV)", data=csv, file_name="UrbanHeat_AI_Simulation.csv", mime="text/csv", use_container_width=True)
            st.markdown(
                '<div class="alert alert-info" style="margin-top:14px;"><b>AI decision-support disclaimer:</b> '
                'predictions are estimates from the trained XGBoost model. Actual cooling depends on implementation '
                'quality, environmental conditions, land availability, engineering feasibility, maintenance, and '
                'climatic variability. Use alongside detailed engineering and environmental assessments.</div>',
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown(
            """
            <div class="empty">
                <div class="empty-ico">🛰</div>
                <div class="empty-t">Ready to Simulate</div>
                <div class="empty-s">Adjust the intervention sliders on the left, then click
                <b style="color:#ff7d3c;">Run AI Simulation</b> to generate real-time predictions
                using the trained XGBoost model.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-heading">📈 Intervention Mix (Preview)</div>', unsafe_allow_html=True)
            effectiveness_df = pd.DataFrame({
                "Intervention": ["Green Cover", "Tree Plantation", "Cool Roof", "Permeable Surface", "Built-up Reduction"],
                "Selected (%)": [green_cover, tree_cover, cool_roofs, permeable_surface, builtup_reduction]
            })
            fig = px.bar(effectiveness_df, x="Selected (%)", y="Intervention", orientation="h", color="Selected (%)", color_continuous_scale=["#27b6ff", "#ffc233", "#ff5a1e", "#26d07c"])
            fig.update_layout(height=320, coloraxis_showscale=False, xaxis_title="Selected %", yaxis_title="")
            st.plotly_chart(style_chart(fig), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(
                """
                <div class="glass-panel">
                    <div class="panel-heading">🤖 Key AI Observations</div>
                    <div class="alert alert-cool" style="margin:0;">
                        • Higher NDVI values generally reduce predicted urban heat.<br><br>
                        • Reducing built-up intensity lowers predicted LST in densely urbanized regions.<br><br>
                        • Tree plantation helps via both increased NDVI and tree-cover proportion.<br><br>
                        • Combining multiple interventions usually yields greater cooling than any single action.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ==================================================
# MODEL VALIDATION
# ==================================================

elif page == "Model Validation":

    section_header(
        "Rigor", "Model Validation",
        "Dataset V2 and V3 are evaluated with spatial block cross-validation to reduce spatial "
        "leakage and provide a realistic estimate of performance in unseen locations."
    )

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.dataframe(model_comparison, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    metric_options = [c for c in model_comparison.columns if c not in ["Dataset", "Model"] and pd.api.types.is_numeric_dtype(model_comparison[c])]
    if metric_options:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        selected_metric = st.selectbox("Select performance metric", metric_options)
        fig = px.bar(model_comparison, x="Dataset", y=selected_metric, color="Dataset", text_auto=".3f", title=f"Dataset V2 vs Dataset V3 — {selected_metric}", color_discrete_sequence=["#ff5a1e", "#ffc233", "#26d07c"])
        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="alert alert-info">Latitude and Longitude are used only for mapping and spatial grouping. '
        'They are excluded from model features to prevent target and spatial leakage.</div>',
        unsafe_allow_html=True
    )


# ==================================================
# ABOUT PROJECT
# ==================================================

elif page == "About Project":

    section_header(
        "Briefing", "About the Project",
        "An AI/ML-powered geospatial decision-support system for Chhatrapati Sambhajinagar, integrating "
        "satellite-derived NDVI, NDBI, LST, elevation, population, and land-cover data."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="glass-panel">
                <div class="panel-heading">📡 Key Inputs</div>
                <ul class="clean-list">
                    <li>Sentinel-2 SR Harmonized</li>
                    <li>Landsat 8/9 Collection 2 Level 2</li>
                    <li>SRTM Elevation</li>
                    <li>WorldPop India 2020</li>
                    <li>Google Earth Engine</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="glass-panel">
                <div class="panel-heading">📊 Key Outputs</div>
                <ul class="clean-list">
                    <li>Urban heat hotspot map</li>
                    <li>XGBoost LST prediction model</li>
                    <li>Spatial cross-validation results</li>
                    <li>SHAP feature importance</li>
                    <li>Cooling intervention comparison</li>
                    <li>Heat vulnerability priority zones</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="alert alert-risk"><b>Limitations:</b> satellite-derived LST is not the same as near-surface
        air temperature. Population is used as an exposure proxy, and scenario outputs are decision-support
        estimates. Field validation and local feasibility assessment are required before implementation.</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-heading">⬡ Team AstroByte</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="team">
            <div class="team-c"><div class="team-av">PD</div><div class="team-n">Priyal Deshmukh</div><div class="team-r">AI / ML Lead</div></div>
            <div class="team-c"><div class="team-av">SB</div><div class="team-n">Srushti Bawaskar</div><div class="team-r">Geospatial & Data Lead</div></div>
            <div class="team-c"><div class="team-av">RD</div><div class="team-n">Rishika Deshmukh</div><div class="team-r">Research & Dashboard Lead</div></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        Team AstroByte &nbsp;·&nbsp; Bharatiya Antariksh Hackathon 2026
        &nbsp;·&nbsp; Urban Heat Mitigation &amp; Cooling Strategy Optimization
    </div>
    """,
    unsafe_allow_html=True
)
