"""Training reference for the UrbanHeat AI LST model.

The deployed model (``outputs/models/xgboost_v3_landcover_model.pkl``) is an
XGBoost regressor evaluated with **spatial block cross-validation** rather than
a naive random split. Random splits leak spatially-correlated neighbours
between train and test and produce optimistic, misleading scores; spatial CV
holds out whole geographic blocks, giving an honest estimate of performance at
unseen locations. This is why the reported R² (~0.57) is conservative but
trustworthy.

The functions below document and reproduce that approach. The authoritative,
executed workflow lives in ``notebooks/10_xgboost.ipynb``; inference is served
from ``src/inference.py``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

from .inference import MODEL_FEATURES

# Hyper-parameters of the deployed Dataset V3 model.
XGB_PARAMS = dict(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42,
)

TARGET = "LST"


def make_spatial_blocks(df: pd.DataFrame, n_bins: int = 10) -> pd.Series:
    """Cut the study area into an ``n_bins`` × ``n_bins`` grid and return a
    per-row block id. Rows in the same block are never split across folds.
    """
    lat_bin = pd.cut(df["Latitude"], bins=n_bins, labels=False)
    lon_bin = pd.cut(df["Longitude"], bins=n_bins, labels=False)
    return lat_bin.astype(str) + "_" + lon_bin.astype(str)


def spatial_cross_validate(df: pd.DataFrame, n_splits: int = 5) -> dict:
    """Evaluate the XGBoost model with spatial block GroupKFold and return
    out-of-fold metrics (R², MAE, RMSE). This is the honest score reported in
    the dashboard's Model Validation page.
    """
    X = df[MODEL_FEATURES]
    y = df[TARGET]
    groups = make_spatial_blocks(df)

    gkf = GroupKFold(n_splits=n_splits)
    oof = np.zeros(len(y))
    for train_idx, test_idx in gkf.split(X, y, groups):
        model = XGBRegressor(**XGB_PARAMS)
        model.fit(X.iloc[train_idx], y.iloc[train_idx])
        oof[test_idx] = model.predict(X.iloc[test_idx])

    rmse = float(np.sqrt(mean_squared_error(y, oof)))
    return {
        "r2": float(r2_score(y, oof)),
        "mae_c": float(mean_absolute_error(y, oof)),
        "rmse_c": rmse,
        "n_splits": n_splits,
    }


def train_final_model(df: pd.DataFrame) -> XGBRegressor:
    """Fit the production model on all available rows (after spatial CV has been
    used to estimate generalisation). Returns the fitted estimator.
    """
    model = XGBRegressor(**XGB_PARAMS)
    model.fit(df[MODEL_FEATURES], df[TARGET])
    return model
