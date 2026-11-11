from pathlib import Path
import sys,shutil,tempfile,json,subprocess,time
from harbor.models.task.config import TaskConfig
from verifier import evaluate
ROOT=Path(__file__).resolve().parents[1];summary=[]
for p in sorted((ROOT/'tasks').iterdir()):
 shutil.copyfile(ROOT/'tools'/'verifier.py',p/'tests'/'verifier.py');shutil.copyfile(ROOT/'tools'/'scoring.py',p/'tests'/'scoring.py');(p/'tests'/'scoring_config.json').write_text(json.dumps({'task':p.name}));TaskConfig.model_validate_toml((p/'task.toml').read_text())
 for sh in [p/'tests'/'test.sh',p/'solution'/'solve.sh']:subprocess.run(['bash','-n',str(sh)],check=True)
 with tempfile.TemporaryDirectory()as tmp:
  start=time.time();r=evaluate(p/'solution'/'run.py',p/'tests',Path(tmp)/'logs',isolate=False)
  bad=[(c['case'],[x['name']for x in c['checks']if not x['passed']])for c in r['cases']if not c['passed']]
  print(p.name,'PASS'if r['reward']==1 else'FAIL',round(time.time()-start,2),bad,flush=True)
  summary.append({'task':p.name,'reward':r['reward'],'failures':bad})
(ROOT/'validation.json').write_text(json.dumps({'tasks':summary,'docker_e2e':'not run: Docker unavailable','privilege_isolation':'not run','actual_llm_trials':'not run'},indent=2));assert all(x['reward']==1 for x in summary)
