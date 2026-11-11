"""Compute the ten-task macro-average; missing tasks receive zero."""
from pathlib import Path
import argparse,json,math
from scoring import WEIGHTS

def summarize(root):
 root=Path(root);rows=[]
 for task in WEIGHTS:
  p=root/task/'scorecard.json'
  if not p.exists():rows.append({'task':task,'weight':.1,'score':0.,'status':'missing'});continue
  data=json.loads(p.read_text());score=data['score']
  if data.get('task')!=task or data.get('scoring_version')!='0.5' or type(score)not in (int,float)or not math.isfinite(score)or not 0<=score<=1:raise ValueError('Invalid or incompatible scorecard: '+str(p))
  rows.append({'task':task,'weight':.1,'score':score,'status':'scored'})
 return {'scoring_version':'0.5','fully_automatic':True,'benchmark_score':round(sum(r['score']for r in rows)/10,12),'tasks':rows,'missing_tasks':[r['task']for r in rows if r['status']=='missing']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--scorecards-root',required=True);p.add_argument('--output',required=True);a=p.parse_args();result=summarize(a.scorecards_root);Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
