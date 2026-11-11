"""Scientific outcome verification against generating truth and measured observations."""
import csv,json,math,hashlib,sys,os,tempfile,shutil,subprocess,signal
from pathlib import Path
from scoring import case_score,aggregate

def read(p):
 with p.open()as f:return list(csv.DictReader(f))
def load(p):
 def pairs(items):
  out={}
  for k,v in items:
   if k in out:raise ValueError('Duplicate key')
   out[k]=v
  return out
 if p.is_symlink() or not p.is_file() or p.stat().st_size>20_000_000:raise ValueError('Invalid output file')
 return json.loads(p.read_text(),object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('Nonfinite value')))
def num(a,b,rtol=.25,atol=0):return type(a)in (int,float)and math.isfinite(a)and abs(a-b)<=atol+rtol*abs(b)
def indexed(rows,key):
 result={x[key]:x for x in rows}
 if len(result)!=len(rows):raise ValueError('Duplicate record')
 return result
def check(out,case):
 out,case=Path(out),Path(case);checks=[]
 def record(name,ok):checks.append({'name':name,'passed':bool(ok)})
 try:
  a=load(out/'results.json');g=load(case/'truth.json');ar=indexed(a['compounds'],'compound_id');gr=indexed(g['compounds'],'compound_id');record('compound_coverage',set(ar)==set(gr))
  for key,y in gr.items():
   x=ar.get(key,{})
   record(key+'/scientific_call',all(x.get(k)==y[k]for k in ['binding_call','kinetics_status']))
   issues=x.get('issues');record(key+'/issues',isinstance(issues,list)and len(issues)==len(set(issues))and set(issues)==set(y['issues']))
   record(key+'/decision',x.get('decision')==('advance'if key in a.get('selected',[])else'reserve'if y['kinetics_status']=='supported'and y['binding_call']=='supported'else'hold'))
   for k in ['KD_M','kon_M_inv_s_inv','koff_s_inv']:
    record(key+'/'+k,k in x and (x[k]is None if y[k]is None else num(x[k],y[k])))
  selected=a.get('selected',[]);eligible=sorted([x for x in g['compounds']if x['kinetics_status']=='supported'],key=lambda x:x['KD_M']);required=min(3,len(eligible));allowed={x['compound_id']for x in eligible if not required or x['KD_M']<=1.1*eligible[required-1]['KD_M']}
  record('selection',isinstance(selected,list)and len(selected)==required and len(set(selected))==required and set(selected)<=allowed)
  record('selection_order',all(cid in gr and gr[cid]['KD_M']is not None for cid in selected)and all(gr[selected[i]]['KD_M']<=1.1*gr[selected[i+1]]['KD_M']for i in range(len(selected)-1)))
  ab=indexed(a['batches'],'batch_id');gb=indexed(g['batches'],'batch_id');record('batch_coverage',set(ab)==set(gb))
  for b,y in gb.items():
   x=ab.get(b,{});record(b+'/calibration',num(x.get('solvent_slope'),y['solvent_slope'],.002,.01));record(b+'/activity',num(x.get('activity_fraction'),y['activity_fraction'],.002,.0001));record(b+'/validity',type(x.get('valid'))is bool and x['valid']==y['valid'])
  aa=indexed(read(out/'trace_evidence.csv'),'trace_id');gg=indexed(read(case/'trace_truth.csv'),'trace_id');record('trace_coverage',set(aa)==set(gg))
  for tid,y in gg.items():
   x=aa.get(tid,{})
   try:ok=x['compound_id']==y['compound_id']and x['batch_valid'].lower()==y['batch_valid'].lower()and num(float(x['concentration_M']),float(y['concentration_M']),1e-8,1e-15)and all(num(float(x[k]),float(y[k]),.01,.1)for k in ['peak_corrected_RU','reference_peak_RU'])
   except (ValueError,KeyError):ok=False
   record(tid+'/corrected_evidence',ok)
   record(tid+'/mapping',x.get('compound_id')==y['compound_id'])
   for field,suffix,rel,absolute in [('concentration_M','concentration',1e-8,1e-15),('peak_corrected_RU','corrected_response',.01,.1),('reference_peak_RU','reference_response',.01,.1)]:
    try:valid=num(float(x[field]),float(y[field]),rel,absolute)
    except (ValueError,KeyError):valid=False
    record(tid+'/'+suffix,valid)
   record(tid+'/batch_flag',x.get('batch_valid','').lower()==y['batch_valid'].lower())
  # Check that reported fits actually reproduce the observations. No optimizer identity is required.
  fits=read(out/'condition_fits.csv');fi={(x['compound_id'],x['flow_uL_min']):x for x in fits};record('unique_condition_fits',len(fi)==len(fits))
  d=case/'data';v={x['sample_key']:x['vial_id']for x in read(d/'vials.csv')};c={x['vial_id']:x['compound_id']for x in read(d/'compounds.csv')};acq=indexed(list({tuple(x.items()):x for x in read(d/'acquisition.csv')}.values()),'trace_id');raw={}
  for row in read(d/'measurements.csv'):raw.setdefault(row['trace_id'],{})[float(row['time_s'])]=row
  blanks={(x['batch_id'],float(x['time_s'])):float(x['active_RU'])-float(x['reference_RU'])for x in read(d/'blanks.csv')}
  residuals={};needed=set()
  for tid,x in acq.items():
   cid=c[v[x['sample_key']]]
   if gr[cid]['binding_call']!='supported':continue
   key=(cid,x['flow_uL_min']);needed.add(key)
   if key not in fi:continue
   pp=fi[key]
   try:
    kon,koff,rm=[float(pp[k])for k in ['kon','koff','Rmax']]
    if not all(math.isfinite(z)and z>0 for z in [kon,koff,rm]):raise ValueError()
    b=gb[x['batch_id']];end=float(x['association_end_s']);cc=float(x['concentration_value'])*{'nM':1e-9,'uM':1e-6}[x['concentration_unit']];yy=[]
    for t,row in sorted(raw[tid].items()):
     value=(float(row['active_RU'])-float(row['reference_RU'])-blanks[(x['batch_id'],t)]-b['solvent_slope']*float(x['delta_dmso_pct'])*(0<=t<=end))/b['activity_fraction'];yy.append((t,value))
    baseline=sum(z for t,z in yy if t<0)/sum(t<0 for t,z in yy)
    for t,y in yy:
     if t<0:continue
     rate=kon*cc+koff;pred=rm*kon*cc/rate*(1-math.exp(-rate*min(t,end)))*math.exp(-koff*max(0,t-end));residuals.setdefault(key,[]).append((pred-(y-baseline))**2)
   except (ValueError,OverflowError):record(cid+'/finite_condition_parameters',False)
  record('condition_fit_coverage',set(fi)==needed)
  for key,squares in residuals.items():
   actual=math.sqrt(sum(squares)/len(squares));limit=5 if gr[key[0]]['kinetics_status']=='model_inadequate'else .3
   record('/'.join(key)+'/fit_reproduction',actual<=limit and num(float(fi[key]['rmse']),actual,.01,.02)and num(float(fi[key]['KD']),float(fi[key]['koff'])/float(fi[key]['kon']),.001))
  manifest={'inputs':{str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(d.rglob('*'))if p.is_file()}}
  record('input_provenance',load(out/'provenance.json')==manifest)
  # Narrative reports are optional and never affect the score.
 except Exception as e:record('output_contract/'+str(e),False)
 result={'passed':bool(checks)and all(x['passed']for x in checks),'checks':checks}
 result['score_details']=case_score(out,case,result)
 return result

def evaluate(code,tests,logs,timeout=180,isolate=True):
 code,tests,logs=map(lambda p:Path(p).resolve(),[code,tests,logs]);logs.mkdir(parents=True,exist_ok=True);(logs/'reward.txt').write_text('0\n');reports=[];isolated=isolate and os.geteuid()==0
 if isolated:
  os.chmod(tests,0o700);os.chmod(logs,0o700)
  for p in [code.parent,*code.parent.rglob('*')]:
   if not p.is_symlink():os.chmod(p,0o755 if p.is_dir()else 0o644)
 for case in sorted((tests/'cases').iterdir()):
  with tempfile.TemporaryDirectory(prefix='spr-campaign-')as temp:
   temp=Path(temp);data=temp/'data';out=temp/'output';shutil.copytree(case/'data',data);out.mkdir()
   if isolated:
    os.chmod(temp,0o755)
    for p in [data,*data.rglob('*')]:os.chmod(p,0o755 if p.is_dir()else 0o644)
    os.chown(out,65534,65534)
   def drop():os.setgroups([]);os.setgid(65534);os.setuid(65534)
   try:
    with (logs/(case.name+'.log')).open('w')as stream:
     proc=subprocess.Popen([sys.executable,str(code),'--input-dir',str(data),'--output-dir',str(out)],cwd=out,stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True,preexec_fn=drop if isolated else None,env={'PATH':'/usr/local/bin:/usr/bin:/bin','HOME':str(out),'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MPLCONFIGDIR':str(out/'.mpl')})
     try:ret=proc.wait(timeout=timeout)
     except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait();raise RuntimeError('timeout')
    try:os.killpg(proc.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    if ret:raise RuntimeError(f'program exit {ret}')
    r=check(out,case)
   except Exception as e:r={'passed':False,'checks':[{'name':'execution/'+str(e),'passed':False}]}
   reports.append({'case':case.name,**r})
 task=json.loads((tests/'scoring_config.json').read_text())['task'];scorecard=aggregate(task,reports);(logs/'scorecard.json').write_text(json.dumps(scorecard,indent=2));reward=scorecard['score'];(logs/'reward.txt').write_text(str(reward)+'\n');report={'reward':reward,'all_checks_passed':all(x['passed']for x in reports)and len(reports)==3,'scorecard':scorecard,'cases':reports,'privilege_isolation':isolated};(logs/'metrics.json').write_text(json.dumps(report,indent=2))
 testslist=[{'name':r['case']+'/'+x['name'],'status':'passed'if x['passed']else'failed','duration':0}for r in reports for x in r['checks']];passed=sum(x['status']=='passed'for x in testslist)
 (logs/'ctrf.json').write_text(json.dumps({'results':{'tool':{'name':'spr-campaign-verifier'},'summary':{'tests':len(testslist),'passed':passed,'failed':len(testslist)-passed,'skipped':0,'pending':0,'other':0,'start':0,'stop':0},'tests':testslist}},indent=2));return report
if __name__=='__main__':
 try:evaluate('/app/submission/run.py','/tests','/logs/verifier')
 except Exception as e:
  p=Path('/logs/verifier');p.mkdir(parents=True,exist_ok=True);(p/'reward.txt').write_text('0\n');(p/'metrics.json').write_text(json.dumps({'error':str(e),'reward':0}))
