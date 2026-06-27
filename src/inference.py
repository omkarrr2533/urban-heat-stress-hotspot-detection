"""Canonical inference + cooling-scenario logic for UrbanHeat AI.

This is the single source of truth used by BOTH the Streamlit dashboard
(``app.py``) and the REST API (``api.py``). Keeping the logic here means the
interactive app and the programmatic API can never silently drift apart.

The deployed model is an XGBoost regressor trained on Dataset V3 with 11
physical / land-cover features (see ``MODEL_FEATURES``). It predicts Land
Surface Temperature (LST, deg C).

Cooling simulation note
-----------------------
The intervention sliders are translated into changes in environmental
indicators (NDVI, NDBI, land-cover fractions) using the fixed sensitivity
coefficients in ``INTERVENTION_COEFFICIENTS``. **These coefficients are
transparent planning assumptions, not empirically calibrated causal effects.**
The trained model then re-predicts LST from the modified indicators, so the
output is a comparative "what-if" scenario for prioritisation — not a
guaranteed real-world temperature outcome.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import joblib


# --------------------------------------------------------------------------
# Paths & feature schema (must match the deployed model exactly)
# --------------------------------------------------------------------------

DEFAULT_MODEL_PATH = Path("outputs/models/xgboost_v3_landcover_model.pkl")
DEFAULT_DATA_PATH = Path("data/processed/featured_uhi_v3.csv")

LANDCOVER_COLS = [
    "LandCover_Bare_sparse_vegetation",
    "LandCover_Built-up land",
    "LandCover_Cropland",
    "LandCover_Grassland",
    "LandCover_Permanent_water_bodies",
    "LandCover_Shrubland",
    "LandCover_Tree cover",
]

MODEL_FEATURES = ["NDVI", "NDBI", "Elevation", "Population"] + LANDCOVER_COLS

# Hotspot thresholds (deg C). Single 5-tier scheme used everywhere.
HOTSPOT_THRESHOLDS = [
    (42, "Extreme"),
    (38, "Very High"),
    (34, "High"),
    (30, "Moderate"),
]
EXTREME_THRESHOLD_C = 42

# Sensitivity coefficients: change in indicator per +1% of each intervention.
# Transparent planning assumptions (see module docstring) — exposed so they can
# be documented in the UI and tuned in one place.
INTERVENTION_COEFFICIENTS = {
    "ndvi": {"green_cover": 0.0025, "tree_cover": 0.0035, "permeable_surface": 0.0010},
    "ndbi": {"builtup_reduction": 0.0020, "green_cover": 0.0010, "tree_cover": 0.0010},
    "tree_cover": {"tree_cover": 0.004, "green_cover": 0.002},
    "built_up": {"builtup_reduction": 0.004, "permeable_surface": 0.002, "cool_roofs": 0.001},
    "cropland": {"green_cover": 0.0005},
    "grassland": {"green_cover": 0.001, "permeable_surface": 0.001},
    "shrubland": {"green_cover": 0.0005},
    "bare": {"green_cover": 0.001},
}


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def load_model(model_path: str | Path = DEFAULT_MODEL_PATH):
    """Load the trained XGBoost model. Requires the ``xgboost`` package."""
    return joblib.load(model_path)


def load_dataset(data_path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the featured Dataset V3 used for simulation."""
    return pd.read_csv(data_path)


def missing_features(df: pd.DataFrame) -> list[str]:
    """Return any required model features absent from ``df``."""
    return [f for f in MODEL_FEATURES if f not in df.columns]


# --------------------------------------------------------------------------
# Core helpers
# --------------------------------------------------------------------------

def _clip(series, low=None, high=None):
    if low is not None:
        series = np.maximum(series, low)
    if high is not None:
        series = np.minimum(series, high)
    return series


def normalize_landcover(df: pd.DataFrame) -> pd.DataFrame:
    """Re-normalise land-cover fractions so each row sums to 1."""
    total = df[LANDCOVER_COLS].sum(axis=1).replace(0, 1)
    df[LANDCOVER_COLS] = df[LANDCOVER_COLS].div(total, axis=0)
    return df


def classify_hotspot(lst: float) -> str:
    """Map an LST value (deg C) to a 5-tier hotspot category."""
    for threshold, label in HOTSPOT_THRESHOLDS:
        if lst >= threshold:
            return label
    return "Low"


def predict_lst(model, df: pd.DataFrame) -> np.ndarray:
    """Predict LST for the rows in ``df`` (must contain ``MODEL_FEATURES``)."""
    return model.predict(df[MODEL_FEATURES])


def apply_interventions(
    df: pd.DataFrame,
    green_cover: float = 0.0,
    tree_cover: float = 0.0,
    cool_roofs: float = 0.0,
    permeable_surface: float = 0.0,
    builtup_reduction: float = 0.0,
) -> pd.DataFrame:
    """Return a copy of ``df`` with environmental indicators modified by the
    selected interventions (percentages 0-100), using
    ``INTERVENTION_COEFFICIENTS``. Land-cover fractions are re-normalised.
    """
    c = INTERVENTION_COEFFICIENTS
    s = df.copy()

    ndvi_gain = (
        green_cover * c["ndvi"]["green_cover"]
        + tree_cover * c["ndvi"]["tree_cover"]
        + permeable_surface * c["ndvi"]["permeable_surface"]
    )
    s["NDVI"] = _clip(s["NDVI"] + ndvi_gain, -1, 1)

    ndbi_drop = (
        builtup_reduction * c["ndbi"]["builtup_reduction"]
        + green_cover * c["ndbi"]["green_cover"]
        + tree_cover * c["ndbi"]["tree_cover"]
    )
    s["NDBI"] = _clip(s["NDBI"] - ndbi_drop, -1, 1)

    s["LandCover_Tree cover"] = _clip(
        s["LandCover_Tree cover"]
        + tree_cover * c["tree_cover"]["tree_cover"]
        + green_cover * c["tree_cover"]["green_cover"],
        0,
    )
    s["LandCover_Built-up land"] = _clip(
        s["LandCover_Built-up land"]
        - builtup_reduction * c["built_up"]["builtup_reduction"]
        - permeable_surface * c["built_up"]["permeable_surface"]
        - cool_roofs * c["built_up"]["cool_roofs"],
        0,
    )
    s["LandCover_Cropland"] = _clip(s["LandCover_Cropland"] + green_cover * c["cropland"]["green_cover"], 0)
    s["LandCover_Grassland"] = _clip(
        s["LandCover_Grassland"]
        + green_cover * c["grassland"]["green_cover"]
        + permeable_surface * c["grassland"]["permeable_surface"],
        0,
    )
    s["LandCover_Shrubland"] = _clip(s["LandCover_Shrubland"] + green_cover * c["shrubland"]["green_cover"], 0)
    s["LandCover_Bare_sparse_vegetation"] = _clip(
        s["LandCover_Bare_sparse_vegetation"] - green_cover * c["bare"]["green_cover"], 0
    )
    s["LandCover_Permanent_water_bodies"] = _clip(s["LandCover_Permanent_water_bodies"], 0)

    return normalize_landcover(s)


def simulate(
    model,
    df: pd.DataFrame,
    green_cover: float = 0.0,
    tree_cover: float = 0.0,
    cool_roofs: float = 0.0,
    permeable_surface: float = 0.0,
    builtup_reduction: float = 0.0,
):
    """Run a full cooling scenario.

    Returns ``(result_df, summary)`` where ``result_df`` adds LST_Before,
    LST_After, Temperature_Reduction, Hotspot_Before and Hotspot_After, and
    ``summary`` is a dict of headline metrics.
    """
    simulated = apply_interventions(
        df,
        green_cover=green_cover,
        tree_cover=tree_cover,
        cool_roofs=cool_roofs,
        permeable_surface=permeable_surface,
        builtup_reduction=builtup_reduction,
    )

    simulated["LST_Before"] = predict_lst(model, df)
    simulated["LST_After"] = predict_lst(model, simulated)
    simulated["Temperature_Reduction"] = simulated["LST_Before"] - simulated["LST_After"]
    simulated["Hotspot_Before"] = simulated["LST_Before"].apply(classify_hotspot)
    simulated["Hotspot_After"] = simulated["LST_After"].apply(classify_hotspot)

    extreme_before = int((simulated["LST_Before"] >= EXTREME_THRESHOLD_C).sum())
    extreme_after = int((simulated["LST_After"] >= EXTREME_THRESHOLD_C).sum())

    summary = {
        "avg_lst_before": float(simulated["LST_Before"].mean()),
        "avg_lst_after": float(simulated["LST_After"].mean()),
        "mean_reduction": float(simulated["Temperature_Reduction"].mean()),
        "max_lst_before": float(simulated["LST_Before"].max()),
        "max_lst_after": float(simulated["LST_After"].max()),
        "extreme_zones_before": extreme_before,
        "extreme_zones_after": extreme_after,
        "extreme_zone_reduction_pct": (
            0.0 if extreme_before == 0 else (extreme_before - extreme_after) / extreme_before * 100
        ),
        "pixels_cooled_pct": float((simulated["Temperature_Reduction"] > 0).mean() * 100),
        "n_locations": int(len(simulated)),
    }
    return simulated, summary
