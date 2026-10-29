"""Read-only technical checks and spatial-CV reproduction for the project report.
Run from the repository root: python report/tools/validate_project.py
Requires the project dependencies. Does not overwrite project models or datasets.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import json
import warnings
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import GroupKFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor
from fastapi.testclient import TestClient
from src import inference
from api import app

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'report'
checks = []
def check(name, condition, detail):
    checks.append({'check': name, 'passed': bool(condition), 'detail': detail})

raw = pd.read_csv(ROOT/'data/raw/Sambhajinagar_Dataset_V3_Final.csv')
df = pd.read_csv(ROOT/'data/processed/model_ready_uhi_v3.csv')
featured = inference.load_dataset(ROOT/'data/processed/featured_uhi_v3.csv')
hot = pd.read_csv(ROOT/'data/processed/hotspot_predictions_v3.csv')
sc = pd.read_csv(ROOT/'data/processed/scenario_predictions_v3.csv')
vul = pd.read_csv(ROOT/'data/processed/vulnerability_predictions_v3.csv')
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    model = inference.load_model(ROOT/'outputs/models/xgboost_v3_landcover_model.pkl')
order = pd.read_csv(ROOT/'outputs/models/xgboost_v3_feature_order.csv').Feature.tolist()
check('V3 audit dimensions', raw.shape == (9893,10), str(raw.shape))
check('V3 missing and duplicate audit', raw.isna().sum().sum()==0 and raw.duplicated().sum()==0, '0 missing cells; 0 duplicate rows')
check('Model feature order', order==inference.MODEL_FEATURES and list(model.feature_names_in_)==order, '11 features in identical order')
check('One-hot integrity', np.allclose(df[inference.LANDCOVER_COLS].sum(axis=1),1), 'Every row sums to 1')
check('Coordinates excluded', not set(['Latitude','Longitude']).intersection(order), 'Spatial fields are not predictors')
pred = inference.predict_lst(model,df)
delta = float(np.max(np.abs(pred-hot.Predicted_LST)))
check('Saved model/output agreement',delta<1e-5,f'Maximum absolute difference {delta:.8g} °C')
check('HVI formula',np.allclose(vul.Heat_Vulnerability_Index,0.5*(vul.Heat_Hazard_Score+vul.Population_Exposure_Score)), 'Equal-weight mean reproduced exactly')
check('Spatial-zone lineage',hot.Zone_ID.nunique()==334 and set(hot.Zone_ID)==set(sc.Zone_ID)==set(vul.Zone_ID), '334 shared approximately 0.02-degree zones')
check('Hotspot quartile lineage',len(hot[hot.Heat_Category=='Very High'])==2472, '2472 points in the upper observed-LST quartile')
_,zero = inference.simulate(model,featured)
check('Zero-intervention identity',zero['mean_reduction']==0 and zero['avg_lst_before']==zero['avg_lst_after'], 'No change for all-zero controls')
modified=inference.apply_interventions(featured,100,100,100,100,100)
check('Scenario bounds and normalization',modified.NDVI.between(-1,1).all() and modified.NDBI.between(-1,1).all() and np.allclose(modified[inference.LANDCOVER_COLS].sum(axis=1),1) and (modified[inference.LANDCOVER_COLS]>=0).all().all(), 'Valid even at 100% control settings')
check('Hotspot boundary rules',[inference.classify_hotspot(x) for x in [29.99,30,34,38,42]]==['Low','Moderate','High','Very High','Extreme'], 'Canonical API classifier checked at thresholds')
client=TestClient(app)
r=client.get('/health');check('API health',r.status_code==200 and r.json()['status']=='ok','GET /health → 200')
r=client.get('/model-info');check('API metadata',r.status_code==200 and r.json()['n_features']==11,'GET /model-info → 200; 11 features')
row=featured.iloc[0][order].to_dict()
r=client.post('/predict',json={'locations':[row]})
check('API single prediction',r.status_code==200 and abs(r.json()['predictions'][0]['predicted_lst_c']-float(pred[0]))<0.001,'POST /predict agrees with canonical inference to 0.001 °C')
r=client.post('/predict',json={'locations':[]});check('Empty request rejected',r.status_code==400,'POST /predict with empty list → 400')
r=client.post('/predict',json={'locations':[{'NDVI':0.2}]});check('Incomplete feature schema rejected',r.status_code==422,'Missing required numeric features → 422')
r=client.post('/simulate',json={'green_cover':101});check('Upper control bound enforced',r.status_code==422,'green_cover=101 → 422')
r=client.post('/simulate',json={'green_cover':-1});check('Lower control bound enforced',r.status_code==422,'green_cover=-1 → 422')
r=client.post('/simulate',json={k:0 for k in ['green_cover','tree_cover','cool_roofs','permeable_surface','builtup_reduction']})
check('API zero scenario',r.status_code==200 and r.json()['summary']['mean_reduction']==0,'All-zero scenario returns zero mean change')
_,live=inference.simulate(model,featured,20,25,15,15,10)
r=client.post('/simulate',json={'green_cover':20,'tree_cover':25,'cool_roofs':15,'permeable_surface':15,'builtup_reduction':10})
check('API/dashboard simulation parity',r.status_code==200 and abs(r.json()['summary']['mean_reduction']-live['mean_reduction'])<0.00011,'Same canonical simulation; API summary rounded to four decimals')
check('Notebook greening reproduction',np.allclose(model.predict(inference.normalize_landcover(featured.assign(NDVI=(featured.NDVI*1.2).clip(upper=1),NDBI=featured.NDBI*.9))[order]),sc.Greening_Predicted_LST,atol=1e-5),'Multiplicative notebook scenario reproduced')
check('Notebook cool-surface reproduction',np.allclose(model.predict(featured.assign(NDBI=featured.NDBI*.8)[order]),sc.Cool_Surface_Predicted_LST,atol=1e-5),'Multiplicative notebook scenario reproduced')
comparison=pd.read_csv(ROOT/'outputs/reports/v2_vs_v3_xgboost_comparison.csv')
check('Published metric lineage',np.allclose(comparison.iloc[1][['R2','MAE_C','RMSE_C']].astype(float),[.5691,1.6645,2.1163]),'Dashboard comparison agrees with saved report CSV')

# Reproduce the exact notebook grouping and estimator settings, not src/model.py's
# alternative 10x10 grouping. This produces genuine out-of-fold predictions.
lat=np.floor((df.Latitude-df.Latitude.min())/.02).astype(int)
lon=np.floor((df.Longitude-df.Longitude.min())/.02).astype(int)
groups=lat.astype(str)+'_'+lon.astype(str)
check('Grouped-fold separation',groups.nunique()==334,'334 groups; each group assigned to one test fold')
params={k:model.get_params()[k] for k in ['n_estimators','learning_rate','max_depth','min_child_weight','subsample','colsample_bytree','objective','random_state']}
params['n_jobs']=2
X=df[order];y=df.LST
out=np.zeros(len(df));fold_metrics=[];leakage=False
for i,(tr,te) in enumerate(GroupKFold(5).split(X,y,groups),1):
    leakage |= bool(set(groups.iloc[tr]) & set(groups.iloc[te]))
    m=XGBRegressor(**params);m.fit(X.iloc[tr],y.iloc[tr]);out[te]=m.predict(X.iloc[te])
    fold_metrics.append({'fold':i,'train_n':len(tr),'test_n':len(te),'r2':r2_score(y.iloc[te],out[te]),'mae_c':mean_absolute_error(y.iloc[te],out[te]),'rmse_c':float(np.sqrt(mean_squared_error(y.iloc[te],out[te])))})
check('No shared train/test spatial groups',not leakage,'Zero group intersection in all five folds')
pooled={'r2':r2_score(y,out),'mae_c':mean_absolute_error(y,out),'rmse_c':float(np.sqrt(mean_squared_error(y,out)))}
fold_mean={k:float(np.mean([f[k] for f in fold_metrics])) for k in ['r2','mae_c','rmse_c']}
(OUT/'evidence').mkdir(exist_ok=True)
np.savez_compressed(OUT/'evidence/v3_oof.npz',observed=y.to_numpy(),predicted=out)
result={'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'pooled_oof':pooled,'mean_fold_metrics':fold_mean,'fold_metrics':fold_metrics,'live_default_simulation':live,'model_parameters':params,'stored_comparison':comparison.to_dict('records'),'note':'Read-only checks. Model and source datasets were not modified. Software versions are recorded separately.'}
(OUT/'validation_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'passed':result['passed'],'total':result['total'],'pooled_oof':pooled,'mean_fold_metrics':fold_mean,'failed':[c for c in checks if not c['passed']]},indent=2))
