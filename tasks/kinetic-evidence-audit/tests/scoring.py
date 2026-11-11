"""Fully automatic per-task scoring on [0, 1], version 0.5."""
import json,math
from pathlib import Path
GROUPS=['mapping','correction','qc','binding','reportability','quantification','fit_consistency','decisions','execution']
WEIGHTS={
'campaign-adjudication':[6,10,10,14,10,6,6,14,4],
'solvent-reference-recovery':[4,24,8,14,6,8,6,6,4],
'kinetic-evidence-audit':[4,8,8,8,20,16,8,4,4],
'condition-consistency':[4,8,8,8,20,8,16,4,4],
'model-adequacy':[4,8,8,8,20,8,16,4,4],
'surface-activity-drift':[4,16,22,10,8,8,4,4,4],
'replicate-adjudication':[4,8,18,12,18,8,4,4,4],
'campaign-reconstruction':[22,14,10,8,8,6,4,4,4],
'pipeline-repair':[8,10,10,10,10,10,10,8,4],
'budgeted-validation':[4,8,8,10,10,8,6,22,4]}
WEIGHTS['pipeline-repair']=[6,10,10,10,10,10,10,10,4]
assert all(sum(v)==80 for v in WEIGHTS.values())
WEIGHTS={task:[value/80 for value in values]for task,values in WEIGHTS.items()}
def avg(v):return sum(v)/len(v)if v else 0.
def parameter_credit(actual,truth):
 if type(actual)not in (int,float)or not math.isfinite(actual)or actual<=0:return 0.
 e=abs(actual-truth)/abs(truth)
 return 1. if e<=.01 else max(0.,(.25-e)/.24)
def case_score(out,case,legacy):
 out,case=Path(out),Path(case);g=json.loads((case/'truth.json').read_text());checks=legacy.get('checks',[]);by={x['name']:float(x['passed'])for x in checks};groups={k:[]for k in GROUPS};critical=[]
 try:a=json.loads((out/'results.json').read_text());ar={x['compound_id']:x for x in a['compounds']}
 except Exception:a={};ar={}
 gr={x['compound_id']:x for x in g['compounds']}
 # Macro-average evidence calls across present ground-truth classes.
 classes={}
 for cid,y in gr.items():
  x=ar.get(cid,{})
  classes.setdefault(y['binding_call'],[]).append(float(x.get('binding_call')==y['binding_call']))
  groups['reportability'].append(float(x.get('kinetics_status')==y['kinetics_status']))
  groups['qc'].append(by.get(cid+'/issues',0.))
  groups['decisions'].append(by.get(cid+'/decision',0.))
  for key in ['KD_M','kon_M_inv_s_inv','koff_s_inv']:
   if y[key]is not None:groups['quantification'].append(parameter_credit(x.get(key),y[key]))
   else:groups['reportability'].append(float(key in x and x[key]is None))
  if cid in a.get('selected',[])and y['kinetics_status']!='supported':critical.append('unsupported_advancement:'+cid)
  if y['kinetics_status']!='supported'and any(x.get(k)is not None for k in ['KD_M','kon_M_inv_s_inv','koff_s_inv']):critical.append('unsupported_precision:'+cid)
 groups['binding']=[avg(v)for v in classes.values()]
 for name,val in by.items():
  if name in ['compound_coverage','batch_coverage','trace_coverage']:groups['mapping'].append(val)
  elif name.endswith('/mapping')or name.endswith('/concentration'):groups['mapping'].append(val)
  elif name.endswith('/corrected_response')or name.endswith('/reference_response')or name.endswith('/calibration'):groups['correction'].append(val)
  elif name.endswith('/activity')or name.endswith('/validity')or name.endswith('/batch_flag'):groups['qc'].append(val)
  elif name.endswith('/fit_reproduction')or name in ['condition_fit_coverage','unique_condition_fits']:groups['fit_consistency'].append(val)
 groups['decisions']=[.5*avg(groups['decisions'])+.5*avg([by.get('selection',0),by.get('selection_order',0)])]
 groups['execution']=[by.get('input_provenance',0.),float(bool(ar))]
 # Keep trace counts from overwhelming calibration: first average each measurement category.
 for group in ['mapping','correction','qc','fit_consistency']:
  if group in ['mapping','correction','qc','fit_consistency']:
   sub={}
   valid={'mapping':['mapping','concentration','compound_coverage','batch_coverage','trace_coverage'],'correction':['corrected_response','reference_response','calibration'],'qc':['issues','activity','validity','batch_flag'],'fit_consistency':['fit_reproduction','condition_fit_coverage','unique_condition_fits']}[group]
   for name,val in by.items():
    suffix=name.rsplit('/',1)[-1]
    if suffix in valid:sub.setdefault(suffix,[]).append(val)
   groups[group]=[avg(sub.get(suffix,[]))for suffix in valid]
 for cid in a.get('selected',[]):
  if cid not in gr:critical.append('unsupported_advancement:'+str(cid))
 cap=.49 if any(x.startswith('unsupported_advancement:')for x in critical)else .69 if critical else 1.
 if any(x['name'].startswith('output_contract/')for x in checks):
  groups={k:[]for k in GROUPS};cap=0.;critical.append('invalid_output_contract')
 return {'fractions':{k:avg(v)for k,v in groups.items()},'critical_errors':critical,'total_cap':cap}
def aggregate(task,cases):
 weights=dict(zip(GROUPS,WEIGHTS[task]));details={}
 for group,w in weights.items():
  values=[c.get('score_details',{}).get('fractions',{}).get(group,0.)for c in cases]
  fraction=avg(values)if len(cases)==3 else 0.
  details[group]={'weight':w,'weight_percent':w*100,'achievement':round(fraction,12),'contribution':round(w*fraction,12)}
 uncapped=round(sum(x['contribution']for x in details.values()),12)
 cap=min([c.get('score_details',{}).get('total_cap',1.)for c in cases]+[1.])
 return {'scoring_version':'0.5','task':task,'score':round(min(uncapped,cap),12),'uncapped_score':uncapped,'score_cap':cap,'components':details,'case_weights':[1/3]*3,'fully_automatic':True,'critical_errors':[{'case':c.get('case'), 'errors':c.get('score_details',{}).get('critical_errors',[])}for c in cases if c.get('score_details',{}).get('critical_errors')]}
