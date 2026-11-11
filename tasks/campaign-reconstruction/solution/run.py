"""Research workflow reference; reads only supplied experimental files."""
import argparse,csv,json,hashlib
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

def read(p):
 with open(p) as f:return list(csv.DictReader(f))
def writecsv(p,rows,fields):
 with open(p,'w',newline='')as f:w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
def model(t,c,kon,koff,rm,end):
 rate=kon*c+koff
 return rm*kon*c/rate*(-np.expm1(-rate*np.minimum(np.maximum(t,0),end)))*np.exp(-koff*np.maximum(t-end,0))
def fit(traces):
 t=np.concatenate([x['t'][x['t']>=0]for x in traces]);c=np.concatenate([np.full(sum(x['t']>=0),x['c'])for x in traces]);y=np.concatenate([x['y'][x['t']>=0]for x in traces]);end=np.concatenate([np.full(sum(x['t']>=0),x['end'])for x in traces])
 fits=[least_squares(lambda p:model(t,c,*np.exp(p),end)-y,np.log(start),bounds=(np.log([10,1e-7,1]),np.log([1e8,10,1e5])),max_nfev=700)for start in [[2e5,.02,60],[5e4,.002,80]]]
 f=min(fits,key=lambda f:sum(f.fun**2));kon,koff,rm=np.exp(f.x)
 return {'kon':float(kon),'koff':float(koff),'KD':float(koff/kon),'Rmax':float(rm),'rmse':float(np.sqrt(np.mean(f.fun**2)))}
def analyze(d,out):
 d,out=Path(d),Path(out);out.mkdir(parents=True,exist_ok=True);policy=json.loads((d/'project.json').read_text())
 vials={x['sample_key']:x['vial_id']for x in read(d/'vials.csv')};compounds={x['vial_id']:x['compound_id']for x in read(d/'compounds.csv')}
 acq=list({tuple(x.items()):x for x in read(d/'acquisition.csv')}.values())
 calibration=read(d/'solvent_calibration.csv');controls=read(d/'controls.csv');blanks=read(d/'blanks.csv');raw=read(d/'measurements.csv')
 bytrace={};byblank={}
 for x in raw:bytrace.setdefault(x['trace_id'],{})[float(x['time_s'])]=x
 for x in blanks:byblank[(x['batch_id'],float(x['time_s']))]=float(x['active_RU'])-float(x['reference_RU'])
 slopes={};activity={};qc=[]
 for batch in sorted({x['batch_id']for x in acq}):
  rr=[x for x in calibration if x['batch_id']==batch];xx=np.array([float(x['delta_dmso_pct'])for x in rr]);yy=np.array([float(x['differential_RU'])for x in rr]);slopes[batch]=float(np.dot(xx,yy)/np.dot(xx,xx))
  cc=[x for x in controls if x['batch_id']==batch];activity[batch]=float(np.mean([float(x['observed_RU'])/float(x['expected_RU'])for x in cc]));qc.append({'batch_id':batch,'solvent_slope':slopes[batch],'activity_fraction':activity[batch],'valid':activity[batch]>=policy['minimum_control_activity']})
 traces=[];evidence=[]
 for x in acq:
  r=sorted(bytrace[x['trace_id']].items());t=np.array([a for a,b in r]);active=np.array([float(b['active_RU'])for a,b in r]);ref=np.array([float(b['reference_RU'])for a,b in r]);blank=np.array([byblank[(x['batch_id'],a)]for a in t]);end=float(x['association_end_s']);during=(t>=0)&(t<=end);dmso=float(x['delta_dmso_pct']);bulk=40*dmso*during
  y=active-ref-blank-slopes[x['batch_id']]*dmso*during;y-=np.mean(y[t<0]);act=activity[x['batch_id']]
  y=y/max(act,.01);reference=ref-bulk;reference-=np.mean(reference[t<0]);win=(t>=end-12)&(t<=end)
  compound=compounds[vials[x['sample_key']]];c=float(x['concentration_value'])*{'nM':1e-9,'uM':1e-6}[x['concentration_unit']]
  peak=float(np.mean(y[win]));refpeak=float(np.mean(reference[win]));valid=act>=policy['minimum_control_activity']
  item=dict(id=x['trace_id'],compound=compound,c=c,t=t,y=y,end=end,flow=x['flow_uL_min'],rep=x['replicate'],peak=peak,ref=refpeak,valid=valid)
  traces.append(item);evidence.append({'trace_id':x['trace_id'],'compound_id':compound,'concentration_M':c,'peak_corrected_RU':peak,'reference_peak_RU':refpeak,'batch_valid':valid})
 results=[];condition_fits=[]
 for compound in sorted({x['compound']for x in traces}):
  tt=[x for x in traces if x['compound']==compound];issues=[];call='supported';status='supported';params=None
  if not all(x['valid']for x in tt):call='inconclusive';status='not_applicable';issues=['invalid_control']
  else:
   high=[x for x in tt if x['c']==max(a['c']for a in tt)];signal=float(np.mean([x['peak']for x in high]));reference=float(np.mean([x['ref']for x in high]));cv=float(np.std([x['peak']for x in high])/max(abs(signal),.01))
   if reference>policy['reference_signal_limit_RU']and reference/(abs(signal)+reference)>.8:call='artifact_suspected';status='not_applicable';issues=['reference_binding']
   elif signal<policy['detection_limit_RU']:call='not_detected';status='not_applicable';issues=[]
   elif cv>policy['maximum_repeat_cv']:call='inconclusive';status='not_applicable';issues=['repeat_disagreement']
   else:
    f=[]
    for flow in sorted({x['flow']for x in tt}):
     pp=fit([x for x in tt if x['flow']==flow]);f.append(pp);condition_fits.append(dict(compound_id=compound,flow_uL_min=flow,**pp))
    if max(a['kon']for a in f)/min(a['kon']for a in f)>policy['maximum_kon_ratio']:status='condition_dependent';issues=['flow_dependence']
    elif max(a['rmse']for a in f)>policy['maximum_model_rmse_RU']:status='model_inadequate';issues=['model_mismatch']
    else:
     declines=[]
     for x in high:
      start=np.mean(x['y'][(x['t']>x['end'])&(x['t']<=x['end']+6)]);last=np.mean(x['y'][-3:]);declines.append(start-last)
     if np.mean(declines)<policy['minimum_resolved_drop_RU']:status='unresolved';issues=['unresolved_dissociation']
     else:params=fit(tt)
  results.append({'compound_id':compound,'binding_call':call,'kinetics_status':status,'issues':issues,'KD_M':params['KD']if params else None,'kon_M_inv_s_inv':params['kon']if params else None,'koff_s_inv':params['koff']if params else None,'decision':'eligible'if call=='supported'and status=='supported'else'hold'})
 eligible=sorted([x for x in results if x['decision']=='eligible'],key=lambda x:(x['KD_M'],x['compound_id']))
 selected=[x['compound_id']for x in eligible[:policy['validation_budget']]]
 for x in results:
  if x['decision']=='eligible':x['decision']='advance'if x['compound_id']in selected else'reserve'
 answer={'compounds':results,'selected':selected,'batches':qc}
 (out/'results.json').write_text(json.dumps(answer,indent=2,allow_nan=False)+'\n');writecsv(out/'trace_evidence.csv',sorted(evidence,key=lambda x:x['trace_id']),list(evidence[0]));writecsv(out/'condition_fits.csv',condition_fits,['compound_id','flow_uL_min','kon','koff','KD','Rmax','rmse'])
 (out/'provenance.json').write_text(json.dumps({'inputs':{str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(d.rglob('*'))if p.is_file()}},indent=2))
 (out/'report.md').write_text('The analysis reconstructs sample identities, calibrates solvent response, applies matched blank/reference correction and activity normalization, evaluates controls and repeat agreement, and fits eligible traces. Condition-specific estimates and trace evidence are exported. Null parameters denote unsupported estimates. Advancement follows the supplied project policy, not a claim of druglikeness.\n')
 return answer
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input-dir',required=True);p.add_argument('--output-dir',required=True);a=p.parse_args();analyze(a.input_dir,a.output_dir)
