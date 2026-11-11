"""Test scientific defects, static replay, and an alternative optimizer."""
from pathlib import Path
import tempfile,subprocess,sys,json
from verifier import evaluate
ROOT=Path(__file__).resolve().parents[1];source=(ROOT/'tools'/'engine.py').read_text();checks=[]
def trial(name,code,task,expected):
 with tempfile.TemporaryDirectory()as tmp:
  tmp=Path(tmp);p=tmp/'run.py';p.write_text(code);r=evaluate(p,ROOT/'tasks'/task/'tests',tmp/'logs',timeout=30,isolate=False)
  assert (r['reward']==1 if expected==1 else r['reward']<1),(name,r)
  checks.append({'test':name,'task':task,'reward':r['reward']});print(name,task,'PASS',flush=True)
mutants=[('omit_solvent',"slopes[batch]=float(np.dot(xx,yy)/np.dot(xx,xx))","slopes[batch]=0.0",'solvent-reference-recovery'),('omit_blank',"-blank-slopes[x['batch_id']]","-0*blank-slopes[x['batch_id']]",'campaign-adjudication'),('omit_activity',"y=y/max(act,.01)","y=y",'surface-activity-drift'),('accept_invalid_control',"valid=act>=policy['minimum_control_activity']","valid=True",'campaign-adjudication'),('wrong_concentration_units',"{'nM':1e-9,'uM':1e-6}","{'nM':1e-6,'uM':1e-6}",'campaign-reconstruction'),('ignore_replicate_conflict',"elif cv>policy['maximum_repeat_cv']:","elif cv>100:",'replicate-adjudication')]
for name,old,new,task in mutants:
 assert old in source;trial(name,source.replace(old,new),task,0)
trial('legacy_pipeline',(ROOT/'tasks'/'pipeline-repair'/'environment'/'legacy'/'analyze.py').read_text(),'pipeline-repair',0)
trial('no_output','pass\n','campaign-adjudication',0)
trial('crashing_program','raise SystemExit(2)\n','campaign-adjudication',0)
with tempfile.TemporaryDirectory()as tmp:
 tmp=Path(tmp);frozen=tmp/'frozen';subprocess.run([sys.executable,str(ROOT/'tools'/'engine.py'),'--input-dir',str(ROOT/'tasks'/'campaign-adjudication'/'environment'/'data'),'--output-dir',str(frozen)],check=True)
 code='import argparse,shutil\nfrom pathlib import Path\np=argparse.ArgumentParser();p.add_argument("--input-dir");p.add_argument("--output-dir");a=p.parse_args()\nfor f in Path('+repr(str(frozen))+').iterdir():\n if f.is_file():shutil.copyfile(f,Path(a.output_dir)/f.name)\n'
 trial('static_replay',code,'campaign-adjudication',0)
alternative=source.replace('max_nfev=700','max_nfev=1200,method="dogbox"').replace('[[2e5,.02,60],[5e4,.002,80]]','[[1e5,.01,100],[3e5,.03,45]]')
for p in sorted((ROOT/'tasks').iterdir()):trial('alternative_optimizer',alternative,p.name,1)
(ROOT/'robustness.json').write_text(json.dumps({'checks':checks,'note':'Alternative optimizer shares preprocessing; this is not an independently authored scientific reference or expert review.'},indent=2))
