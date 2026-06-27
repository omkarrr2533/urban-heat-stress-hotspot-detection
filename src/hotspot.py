"""Heat-risk classification helpers.

The canonical 5-tier classifier (Low / Moderate / High / Very High / Extreme)
lives in ``src/inference.py`` and is used by the dashboard, the API and the
training notebooks so every surface agrees on thresholds.
"""

from .inference import classify_hotspot


def detect_hotspots(df, lst_column: str = "Predicted_LST"):
    """Add a ``Heat_Risk`` column by classifying each predicted LST value."""
    df = df.copy()
    df["Heat_Risk"] = df[lst_column].apply(classify_hotspot)
    return df
