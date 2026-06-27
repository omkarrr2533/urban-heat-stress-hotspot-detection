"""UrbanHeat AI — REST API.

A small FastAPI service that exposes the trained XGBoost model so the heat
predictions and cooling simulations can be consumed programmatically (by other
apps, GIS tools, or automated pipelines) — not just through the Streamlit UI.

It reuses ``src/inference.py``, so the API and the dashboard return identical
numbers by construction.

Run locally:
    uvicorn api:app --reload --port 8000

Then open the interactive docs at:
    http://localhost:8000/docs
"""

from __future__ import annotations

from functools import lru_cache

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src import inference

app = FastAPI(
    title="UrbanHeat AI API",
    version="1.0.0",
    description="Urban heat-stress prediction and cooling-scenario simulation "
                "for Chhatrapati Sambhajinagar, powered by an XGBoost LST model.",
)


# --------------------------------------------------------------------------
# Lazy singletons (model + dataset loaded once, on first request)
# --------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_model():
    return inference.load_model()


@lru_cache(maxsize=1)
def get_dataset():
    return inference.load_dataset()


# --------------------------------------------------------------------------
# Schemas
# --------------------------------------------------------------------------

class Location(BaseModel):
    """One grid point with the 11 model features."""
    NDVI: float
    NDBI: float
    Elevation: float
    Population: float
    LandCover_Bare_sparse_vegetation: float = 0.0
    LandCover_Built_up_land: float = Field(0.0, alias="LandCover_Built-up land")
    LandCover_Cropland: float = 0.0
    LandCover_Grassland: float = 0.0
    LandCover_Permanent_water_bodies: float = 0.0
    LandCover_Shrubland: float = 0.0
    LandCover_Tree_cover: float = Field(0.0, alias="LandCover_Tree cover")

    model_config = {"populate_by_name": True}


class PredictRequest(BaseModel):
    locations: list[Location]


class Prediction(BaseModel):
    predicted_lst_c: float
    hotspot_category: str


class PredictResponse(BaseModel):
    count: int
    predictions: list[Prediction]


class SimulateRequest(BaseModel):
    """Intervention intensities, each a percentage 0-100."""
    green_cover: float = Field(20, ge=0, le=100)
    tree_cover: float = Field(25, ge=0, le=100)
    cool_roofs: float = Field(15, ge=0, le=100)
    permeable_surface: float = Field(15, ge=0, le=100)
    builtup_reduction: float = Field(10, ge=0, le=100)


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/model-info")
def model_info():
    """Describe the deployed model and its honest validation metrics."""
    return {
        "model": "XGBoost Regressor (Dataset V3)",
        "target": "Land Surface Temperature (LST, °C)",
        "features": inference.MODEL_FEATURES,
        "n_features": len(inference.MODEL_FEATURES),
        "validation": "Spatial block cross-validation (10×10 grid, GroupKFold)",
        "metrics": {"r2": 0.5691, "mae_c": 1.6645, "rmse_c": 2.1163},
        "hotspot_thresholds_c": {label: thr for thr, label in inference.HOTSPOT_THRESHOLDS},
        "study_area": "Chhatrapati Sambhajinagar (Aurangabad), Maharashtra",
    }


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    """Predict LST and hotspot category for one or more locations."""
    import pandas as pd

    if not request.locations:
        raise HTTPException(status_code=400, detail="No locations provided.")

    rows = [loc.model_dump(by_alias=True) for loc in request.locations]
    df = pd.DataFrame(rows)

    missing = inference.missing_features(df)
    if missing:
        raise HTTPException(status_code=422, detail=f"Missing features: {missing}")

    preds = inference.predict_lst(get_model(), df)
    predictions = [
        Prediction(predicted_lst_c=round(float(p), 3), hotspot_category=inference.classify_hotspot(p))
        for p in preds
    ]
    return PredictResponse(count=len(predictions), predictions=predictions)


@app.post("/simulate")
def simulate(request: SimulateRequest):
    """Run a city-wide cooling scenario on the featured Dataset V3 and return
    headline before/after metrics. Mirrors the dashboard's simulator exactly.
    """
    try:
        _, summary = inference.simulate(
            get_model(), get_dataset(),
            green_cover=request.green_cover,
            tree_cover=request.tree_cover,
            cool_roofs=request.cool_roofs,
            permeable_surface=request.permeable_surface,
            builtup_reduction=request.builtup_reduction,
        )
    except FileNotFoundError as err:
        raise HTTPException(status_code=503, detail=f"Model or dataset not found: {err}")

    return {
        "interventions": request.model_dump(),
        "summary": {k: round(v, 4) if isinstance(v, float) else v for k, v in summary.items()},
        "note": "Cooling coefficients are transparent planning assumptions, not "
                "empirically calibrated effects. Results are comparative scenarios.",
    }
