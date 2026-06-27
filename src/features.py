"""Feature engineering used during exploration (notebook 04).

NOTE: the *deployed* Dataset V3 model uses physical + land-cover features only
(see ``src.inference.MODEL_FEATURES``): NDVI, NDBI, Elevation, Population and
the seven land-cover fractions. The composite ratios below were explored during
EDA to probe interactions; they are intentionally **excluded** from the final
model to keep it interpretable and to avoid collinearity with the raw indices.
They are kept here for reproducibility of the exploration phase.
"""


def create_features(df):
    df = df.copy()

    # Vegetation relative to built-up surface.
    df["Green_Built_Ratio"] = df["NDVI"] / (df["NDBI"].abs() + 0.01)

    # Population weighted by built-up intensity (exposure proxy).
    df["Population_Heat_Index"] = df["Population"] * df["NDBI"]

    # Elevation weighted by vegetation (cooling proxy).
    df["Elevation_Cooling_Index"] = df["Elevation"] * df["NDVI"]

    return df
