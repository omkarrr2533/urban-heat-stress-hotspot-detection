"""Generate original report diagrams and plots from repository data.
Run from the repository root with numpy, pandas and matplotlib installed.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Rectangle
from matplotlib.lines import Line2D
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'report'/'assets';OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'Times New Roman','font.size':12,'axes.titlesize':14,'axes.labelsize':12,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','figure.facecolor':'white','savefig.facecolor':'white','axes.labelcolor':'#172b43','text.color':'#172b43','axes.edgecolor':'#81909d','xtick.color':'#34485b','ytick.color':'#34485b'})
NAVY='#19364d';TEAL='#147d80';ORANGE='#d77736';BLUE='#447ea8';PALE='#eef4f7';GRAY='#637586'
def canvas(w=10,h=6):
 fig,ax=plt.subplots(figsize=(w,h));ax.set_xlim(0,10);ax.set_ylim(0,10);ax.axis('off');fig.subplots_adjust(.015,.015,.985,.985);return fig,ax
def box(ax,x,y,w,h,text,fc=PALE,ec=NAVY,fs=16,rounding=.12):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0.08,rounding_size={rounding}',facecolor=fc,edgecolor=ec,linewidth=1.3))
 ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs,linespacing=1.25)
def arrow(ax,a,b,color=NAVY,style='-|>',rad=0,label=None):
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle=style,mutation_scale=16,lw=1.5,color=color,connectionstyle=f'arc3,rad={rad}'))
 if label:ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+.16,label,ha='center',fontsize=11,color=GRAY)
def save(fig,name):fig.savefig(OUT/name,dpi=230,bbox_inches='tight',pad_inches=.12);plt.close(fig)
def flow(name,steps,w=10,h=7):
 fig,ax=canvas(w,h);n=len(steps);bh=.9;gap=(9.4-n*bh)/(n-1)
 for i,t in enumerate(steps):
  y=9.5-bh-i*(bh+gap);box(ax,1.5,y,7,bh,t,fc='#eaf4f3' if i%2 else PALE,fs=15)
  if i<n-1:arrow(ax,(5,y),(5,y-gap))
 save(fig,name)
flow('fig_workflow.png',['Earth-observation and population layers','Audit, cleaning and physical feature engineering','LST modelling and spatial block validation','Hotspot detection and SHAP interpretation','Population-aware vulnerability assessment','Cooling scenarios and zone prioritisation','Streamlit dashboard and FastAPI access'],h=8)
# Stack diagram
fig,ax=canvas(10,6.8)
rows=[('PRESENTATION','Streamlit  |  Plotly maps and charts  |  CSV export',8),('SERVICE','FastAPI  |  Pydantic validation  |  Uvicorn',6.1),('INTELLIGENCE','scikit-learn  |  XGBoost  |  SHAP  |  Joblib',4.2),('DATA & GEOSPATIAL','Pandas  |  NumPy  |  Earth Engine sources  |  Folium',2.3),('ARTEFACTS','Raw / processed CSV  |  model pickle  |  HTML maps',.4)]
for title,sub,y in rows:box(ax,.5,y,9,1.35,title+'\n'+sub,fs=15)
for y in [8,6.1,4.2,2.3]:arrow(ax,(5,y-.08),(5,y-.48))
save(fig,'fig_stack.png')
# Process model
fig,ax=canvas(10,6.5)
st=[('1  Audit\nsource quality',.4,6),('2  Prepare\nfeatures',3.6,6),('3  Validate\nmodels',6.8,6),('4  Interpret\nheat & exposure',6.8,2),('5  Simulate\ninterventions',3.6,2),('6  Deliver\ndashboard & API',.4,2)]
for t,x,y in st:box(ax,x,y,2.6,1.7,t,fs=15)
for a,b in [((3,6.85),(3.6,6.85)),((6.2,6.85),(6.8,6.85)),((8.1,6),(8.1,3.7)),((6.8,2.85),(6.2,2.85)),((3.6,2.85),(3,2.85))]:arrow(ax,a,b)
arrow(ax,(1.7,3.7),(1.7,6),color=TEAL,rad=0,label='Feedback / new dataset')
save(fig,'fig_process.png')
# Architecture
fig,ax=canvas(11,7.5)
box(ax,.2,7.8,10.6,1.5,'DATA SOURCES\nLandsat LST  •  Sentinel-2 indices  •  SRTM  •  WorldPop  •  WorldCover',fs=15)
box(ax,.2,5.3,4.7,1.55,'Offline analytical pipeline\n13 notebooks + reusable src modules',fs=15)
box(ax,6.1,5.3,4.7,1.55,'Versioned file artefacts\nCSV datasets + XGBoost pickle + reports',fs=15)
box(ax,.2,2.8,4.7,1.5,'Streamlit dashboard\nCached CSV views + interactive simulator',fc='#eaf4f3',fs=15)
box(ax,6.1,2.8,4.7,1.5,'FastAPI service\nValidated prediction + simulation endpoints',fc='#eaf4f3',fs=15)
box(ax,2.9,.25,5.2,1.35,'Canonical inference module\nsrc/inference.py',fc='#fff2e6',ec=ORANGE,fs=15)
arrow(ax,(5.5,7.8),(2.5,6.85));arrow(ax,(4.9,6.05),(6.1,6.05));arrow(ax,(8.45,5.3),(8.45,4.3));arrow(ax,(6.1,5.8),(2.5,4.3));arrow(ax,(2.5,2.8),(4.5,1.6));arrow(ax,(8.45,2.8),(6.5,1.6))
save(fig,'fig_architecture.png')
# DFD 0
fig,ax=canvas(10,5.6)
box(ax,.2,3.5,2.5,1.5,'Planner /\nresearcher');box(ax,7.3,3.5,2.5,1.5,'External GIS /\nAPI client');box(ax,3.5,2.7,3,2.4,'0\nUrbanHeat AI\ndecision-support\nsystem',fc='#eaf4f3',fs=16)
arrow(ax,(2.7,4.65),(3.5,4.65),label='Filters / scenarios');arrow(ax,(3.5,3.35),(2.7,3.35),label='Maps / priorities');arrow(ax,(6.5,4.65),(7.3,4.65),label='JSON outputs');arrow(ax,(7.3,3.35),(6.5,3.35),label='Feature records')
box(ax,3.4,.2,3.2,1.2,'CSV + trained model',fs=14);arrow(ax,(5,2.7),(5,1.4))
save(fig,'fig_dfd0.png')
# DFD 1
fig,ax=canvas(11,7.5)
box(ax,.1,5.5,2,1.4,'Data analyst',fs=14);box(ax,8.8,5.5,2,1.4,'Planner / client',fs=14)
for x,y,n,t in [(3,5.6,'1','Clean and\nencode'),(6,5.6,'2','Train and\nvalidate'),(3,2.6,'3','Analyse heat\nand vulnerability'),(6,2.6,'4','Simulate and\ncommunicate')]:box(ax,x,y,2.1,1.5,n+'  '+t,fs=14)
box(ax,3, .3,5.1,1.15,'D1  Processed CSV / model / dashboard outputs',fs=14)
arrow(ax,(2.1,6.3),(3,6.3));arrow(ax,(5.1,6.3),(6,6.3));arrow(ax,(7.05,5.6),(7.05,4.1));arrow(ax,(6,3.2),(5.1,3.2));arrow(ax,(8.1,3.6),(9.8,5.5));arrow(ax,(4.05,5.6),(4.05,4.1));arrow(ax,(4.05,2.6),(4.05,1.45));arrow(ax,(7.05,2.6),(7.05,1.45))
save(fig,'fig_dfd1.png')
# DFD2
flow('fig_dfd2.png',['5.1  Validate slider values and feature schema','5.2  Copy baseline data; modify NDVI, NDBI and land cover','5.3  Clip indicators and normalise land-cover fractions','5.4  Predict baseline and scenario LST with the same model','5.5  Calculate cooling, threshold crossings and summaries','5.6  Return dashboard charts / API JSON / CSV export'],h=7.5)
# Use case
fig,ax=canvas(10,7.2)
ax.add_patch(Rectangle((2.3,.25),5.4,6.7,fill=False,edgecolor=NAVY,lw=1.3));ax.text(5,6.65,'UrbanHeat AI',ha='center',weight='bold',fontsize=16)
for y,t in [(5.5,'View heat hotspots'),(4.55,'Inspect heat drivers'),(3.6,'Compare vulnerability'),(2.65,'Simulate cooling'),(1.7,'Predict / validate / export')]:ax.add_patch(Ellipse((5,y),4.3,.72,facecolor=PALE,edgecolor=NAVY));ax.text(5,y,t,ha='center',va='center',fontsize=14)
for x,y,label in [(.85,4.7,'Planner'),(.85,1.8,'Researcher'),(9,2.2,'GIS / API\nclient')]:
 ax.plot(x,y+.35,'o',color=NAVY,ms=10);ax.plot([x,x],[y-.1,y+.2],color=NAVY);ax.plot([x-.2,x+.2],[y+.08,y+.08],color=NAVY);ax.plot([x,x-.16],[y-.1,y-.4],color=NAVY);ax.plot([x,x+.16],[y-.1,y-.4],color=NAVY);ax.text(x,y-.7,label,ha='center',fontsize=14)
 targets=([5.85,3.95,2.05] if y>3 else [5.85,4.9,3.95,2.05,1.1]) if x<2 else [3.0,2.05]
 start=(x+.25,y+.15) if x<2 else (x-.25,y+.15)
 for yy in targets:arrow(ax,start,(2.85 if x<2 else 7.15,yy),style='-',color=GRAY)
save(fig,'fig_usecase.png')
# Sequence
fig,ax=canvas(11,7)
xs=[1,3.7,6.4,9.2];labels=['User','Streamlit / API','Inference','Model + CSV']
for x,t in zip(xs,labels):box(ax,x-.85,8.5,1.7,.9,t,fs=14);ax.plot([x,x],[.4,8.5],ls='--',color='#a4b0ba',lw=1)
msgs=[(0,1,7.65,'Select controls / submit JSON'),(1,2,6.55,'Validate and call simulate()'),(2,3,5.45,'Load cached artefacts; predict baseline'),(2,3,4.35,'Modify features; predict scenario'),(3,2,3.25,'Before / after LST arrays'),(2,1,2.15,'Summary and modified records'),(1,0,1.05,'Charts, metrics and export')]
for a,b,y,t in msgs:arrow(ax,(xs[a],y),(xs[b],y),color=TEAL if b<a else NAVY);ax.text((xs[a]+xs[b])/2,y+.18,t,ha='center',fontsize=12)
save(fig,'fig_sequence.png')
# Data lineage / logical schema
fig,ax=canvas(11,7)
box(ax,.2,5,3,2.5,'SAMPLE LOCATION\nLatitude + Longitude + Zone_ID\nNDVI, NDBI, Elevation\nPopulation, LandCover\nObserved LST',fs=14)
box(ax,4.1,5,3.1,2.5,'MODEL ARTEFACT\n11-feature ordered schema\nXGBoost parameters\nSaved estimator\nValidation metrics',fs=14)
box(ax,8,5,2.8,2.5,'ZONE SUMMARY\nZone_ID\nHeat statistics\nHVI and exposure\nCooling potential',fs=14)
box(ax,.2,.7,3,2.4,'PREDICTION RECORD\nPredicted LST\nHeat category\nResidual (offline)',fs=14)
box(ax,4.1,.7,3.1,2.4,'SCENARIO RECORD\nBefore / after LST\nCooling estimate\nRecommended action',fs=14)
box(ax,8,.7,2.8,2.4,'DASHBOARD VIEW\nFiltered map rows\nKPI aggregates\nPriority tables',fs=14)
arrow(ax,(3.2,6.2),(4.1,6.2));arrow(ax,(7.2,6.2),(8,6.2));arrow(ax,(1.7,5),(1.7,3.1));arrow(ax,(3.2,1.9),(4.1,1.9));arrow(ax,(7.2,1.9),(8,1.9));arrow(ax,(9.4,5),(9.4,3.1))
save(fig,'fig_data_model.png')
# Spatial CV
fig,ax=canvas(10,6.5)
rng=np.random.default_rng(2)
for r in range(5):
 for c in range(5):ax.add_patch(Rectangle((.5+c*.65,2+r*.65),.61,.61,facecolor=['#dbe7ef','#c8e5df','#f6dfc9','#dce5d3','#eadde9'][(r+c)%5],edgecolor='white'))
ax.text(2.1,5.7,'Geographic blocks',ha='center',weight='bold',fontsize=14);ax.text(2.1,1.45,'Whole blocks stay together',ha='center',fontsize=13)
box(ax,4.6,5,4.8,1.3,'GroupKFold: five folds\n334 approximately 0.02° zones',fs=15)
box(ax,4.6,3,4.8,1.3,'Train on four fold groups\nTest on the held-out group',fs=15)
box(ax,4.6,1,4.8,1.3,'Collect out-of-fold predictions\nReport R², MAE and RMSE',fs=15)
arrow(ax,(3.8,3.7),(4.6,3.7));arrow(ax,(7,5),(7,4.3));arrow(ax,(7,3),(7,2.3));save(fig,'fig_spatial_cv.png')
# Notebook dependency
fig,ax=canvas(11,6.5)
items=[('01–04\nAudit → EDA → features',.2,6),('05\nBaseline + final V3 model',3.9,6),('06\nHotspot detection',7.6,6),('07\nSHAP interpretation',7.6,3.2),('08\nCooling scenarios',3.9,3.2),('12\nVulnerability',.2,3.2),('11\nFolium maps',7.6,.4),('13\nDashboard-ready outputs',3.9,.4)]
for t,x,y in items:box(ax,x,y,3,1.35,t,fs=14)
for a,b in [((3.2,6.65),(3.9,6.65)),((6.9,6.65),(7.6,6.65)),((9.1,6),(9.1,4.55)),((9.1,3.2),(9.1,1.75)),((7.6,3.85),(6.9,3.85)),((3.9,3.85),(3.2,3.85)),((1.7,3.2),(5.4,1.75)),((7.6,1.05),(6.9,1.05))]:arrow(ax,a,b)
ax.text(.3,.9,'09–10: earlier four-feature\nRF / XGBoost experiments\n(not the final V3 training path)',fontsize=12,color=GRAY)
save(fig,'fig_notebooks.png')
# Data plots
raw=pd.read_csv(ROOT/'data/raw/Sambhajinagar_Dataset_V3_Final.csv');hot=pd.read_csv(ROOT/'data/processed/hotspot_predictions_v3.csv');sc=pd.read_csv(ROOT/'data/processed/scenario_predictions_v3.csv');vu=pd.read_csv(ROOT/'data/processed/vulnerability_predictions_v3.csv')
fig,ax=plt.subplots(figsize=(9,5.8));p=ax.scatter(raw.Longitude,raw.Latitude,c=raw.LST,cmap='inferno',s=6,vmin=30,vmax=50,alpha=.85);ax.set_xlabel('Longitude (°E)');ax.set_ylabel('Latitude (°N)');ax.set_title('Observed LST across the sampled study-area extent');ax.grid(alpha=.15);ax.set_aspect(1/np.cos(np.deg2rad(19.89)));fig.colorbar(p,label='Observed LST (°C)',shrink=.8);fig.tight_layout();save(fig,'fig_study_lst.png')
fig,axes=plt.subplots(1,2,figsize=(11,4.8));axes[0].hist(raw.LST,bins=35,color=BLUE,edgecolor='white');axes[0].axvline(raw.LST.mean(),color=ORANGE,lw=2,label=f'Mean {raw.LST.mean():.2f} °C');axes[0].set(xlabel='Observed LST (°C)',ylabel='Sampled locations',title='LST distribution');axes[0].legend(frameon=False)
lc=pd.read_csv(ROOT/'outputs/reports/v3_landcover_distribution.csv').sort_values('Pixel_Count');axes[1].barh(lc.LandCover_Name,lc.Percentage,color=TEAL);axes[1].set(xlabel='Share of samples (%)',title='Land-cover composition');axes[1].tick_params(axis='y',labelsize=10);fig.tight_layout();save(fig,'fig_distributions.png')
corr=pd.read_csv(ROOT/'outputs/reports/v3_continuous_feature_correlation.csv',index_col=0);fig,ax=plt.subplots(figsize=(7.5,6));im=ax.imshow(corr.values,cmap='RdBu_r',vmin=-1,vmax=1);ax.set_xticks(range(len(corr)),corr.columns,rotation=35,ha='right');ax.set_yticks(range(len(corr)),corr.index)
for i in range(len(corr)):
 for j in range(len(corr)):ax.text(j,i,f'{corr.iloc[i,j]:.2f}',ha='center',va='center',color='white' if abs(corr.iloc[i,j])>.65 else NAVY,fontsize=12)
fig.colorbar(im,shrink=.8,label='Pearson correlation');ax.set_title('Continuous-feature correlation');fig.tight_layout();save(fig,'fig_correlation.png')
# Model comparison
comp=pd.DataFrame({'Model':['Linear\nregression','Random\nforest','XGBoost'],'R²':[.4896,.5569,.5691],'MAE':[1.8303,1.6858,1.6645],'RMSE':[2.3039,2.1455,2.1163]})
fig,axes=plt.subplots(1,2,figsize=(10.5,4.5));axes[0].bar(comp.Model,comp['R²'],color=[GRAY,BLUE,TEAL]);axes[0].set(title='Spatial-CV R² (higher is better)',ylim=(0,.7));axes[1].bar(comp.Model,comp.MAE,color=BLUE,label='MAE');axes[1].bar(comp.Model,comp.RMSE-comp.MAE,bottom=comp.MAE,color=ORANGE,label='Additional RMSE');axes[1].set(title='Error comparison (lower is better)',ylabel='Temperature error (°C)');axes[1].legend(frameon=False,fontsize=10)
for ax in axes:ax.tick_params(axis='x',labelsize=11);ax.grid(axis='y',alpha=.12)
fig.tight_layout();save(fig,'fig_model_comparison.png')
oof=np.load(Path(__file__).resolve().parents[1]/'evidence/v3_oof.npz');obs=oof['observed'];pre=oof['predicted'];res=obs-pre
fig,axes=plt.subplots(1,2,figsize=(11,4.8));axes[0].scatter(obs,pre,s=5,alpha=.2,color=TEAL);axes[0].plot([27,53],[27,53],'--',color=ORANGE,lw=1.6);axes[0].set(xlabel='Observed LST (°C)',ylabel='Out-of-fold predicted LST (°C)',title='Independent reproduction: spatial OOF');axes[1].hist(res,bins=50,color=BLUE,edgecolor='white');axes[1].axvline(0,color=ORANGE,lw=2);axes[1].set(xlabel='Observed − predicted (°C)',ylabel='Locations',title='Out-of-fold residual distribution');fig.tight_layout();save(fig,'fig_oof.png')
fig,ax=plt.subplots(figsize=(9,5));bp=ax.boxplot([sc.Greening_Cooling_C,sc.Cool_Surface_Cooling_C],tick_labels=['Urban greening','Cool / permeable surfaces'],patch_artist=True,showfliers=False,medianprops=dict(color=NAVY,lw=2));
for patch,c in zip(bp['boxes'],[TEAL,BLUE]):patch.set_facecolor(c);patch.set_alpha(.65)
ax.axhline(0,color=ORANGE,ls='--');ax.set(ylabel='Predicted LST reduction (°C)',title='Notebook scenarios: distribution of location-level effects');ax.text(.02,.03,'Negative values indicate predicted warming, not cooling.',transform=ax.transAxes,fontsize=10,color=GRAY);fig.tight_layout();save(fig,'fig_scenario_box.png')
fig,ax=plt.subplots(figsize=(9,5.8));p=ax.scatter(vu.Baseline_Predicted_LST,vu.Population,c=vu.Heat_Vulnerability_Index,cmap='viridis',s=7,alpha=.7);ax.set_yscale('symlog',linthresh=10);ax.set(xlabel='Baseline predicted LST (°C)',ylabel='Population proxy (symmetric-log scale)',title='Heat hazard and population exposure are distinct');fig.colorbar(p,label='Heat Vulnerability Index',shrink=.8);fig.tight_layout();save(fig,'fig_vulnerability.png')
# Static vulnerability map, no external tiles required
fig,ax=plt.subplots(figsize=(9,5.8));p=ax.scatter(vu.Longitude,vu.Latitude,c=vu.Heat_Vulnerability_Index,cmap='viridis',s=7,alpha=.85);ax.set(xlabel='Longitude (°E)',ylabel='Latitude (°N)',title='Population-aware Heat Vulnerability Index');ax.set_aspect(1/np.cos(np.deg2rad(19.89)));ax.grid(alpha=.15);fig.colorbar(p,label='HVI (0–1)',shrink=.8);fig.tight_layout();save(fig,'fig_hvi_map.png')
# priority comparison
zones=pd.read_csv(ROOT/'outputs/reports/intervention_priority_v3.csv').head(10).iloc[::-1];fig,ax=plt.subplots(figsize=(10,5.8));y=np.arange(len(zones));ax.barh(y-.18,zones.Mean_Greening_Cooling_C,height=.34,color=TEAL,label='Urban greening');ax.barh(y+.18,zones.Mean_Cool_Surface_Cooling_C,height=.34,color=BLUE,label='Cool / permeable surfaces');ax.set_yticks(y,zones.Zone_ID);ax.set(xlabel='Mean predicted cooling (°C)',title='Top ten zones ranked by mean best-location cooling');ax.legend(frameon=False);fig.tight_layout();save(fig,'fig_intervention_zones.png')
print('Generated',len(list(OUT.glob('fig_*.png'))),'original diagrams and analytical figures.')
