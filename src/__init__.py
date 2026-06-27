"""UrbanHeat AI — source package.

Modules
-------
inference : canonical model loading, prediction, hotspot classification and
            cooling-scenario simulation. Shared by the Streamlit dashboard
            (``app.py``) and the REST API (``api.py``) so both behave identically.
model     : training reference (XGBoost + spatial block cross-validation).
features  : feature engineering used during exploration.
cleaning  : data-cleaning helpers.
hotspot   : heat-risk classification helpers.
utils     : small IO helpers.
"""
