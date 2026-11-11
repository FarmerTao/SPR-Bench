"""Regression tests for fully automatic score semantics, including report independence."""
from pathlib import Path
import tempfile,json,math,sys
from scoring import WEIGHTS,GROUPS,parameter_credit,aggregate
from summarize_scores import summarize
from engine import analyze
from verifier import check
ROOT=Path(__file__).resolve().parents[1]
assert all(math.isclose(sum(x),1)for x in WEIGHTS.values())
assert parameter_credit(101,100)==1
assert abs(parameter_credit(113,100)-.5)<1e-12
assert parameter_credit(125,100)==0
assert parameter_credit(float('nan'),100)==0
case=ROOT/'tasks'/'campaign-adjudication'/'tests'/'cases'/'0'
with tempfile.TemporaryDirectory()as temp:
 out=Path(temp)/'output';analyze(case/'data',out)
 result=check(out,case);score=aggregate('campaign-adjudication',[result]*3);assert score['score']==1
 (out/'report.md').unlink();assert aggregate('campaign-adjudication',[check(out,case)]*3)==score
 (out/'report.md').write_text('Nonsense narrative that must not change scoring.');assert aggregate('campaign-adjudication',[check(out,case)]*3)==score
 a=json.loads((out/'results.json').read_text());g=json.loads((case/'truth.json').read_text());truth={x['compound_id']:x for x in g['compounds']};x=next(x for x in a['compounds']if x['kinetics_status']=='supported');x['KD_M']=truth[x['compound_id']]['KD_M']*1.13;(out/'results.json').write_text(json.dumps(a));partial=aggregate('campaign-adjudication',[check(out,case)]*3);assert 0<partial['score']<1
 x=next(x for x in a['compounds']if x['kinetics_status']!='supported');x['KD_M']=1e-9;(out/'results.json').write_text(json.dumps(a));assert check(out,case)['score_details']['total_cap']==.69
 a['selected'][0]=x['compound_id'];(out/'results.json').write_text(json.dumps(a));assert check(out,case)['score_details']['total_cap']==.49
 a['selected'][0]='UNKNOWN';(out/'results.json').write_text(json.dumps(a));assert check(out,case)['score_details']['total_cap']==.49
 (out/'results.json').write_text('invalid');assert aggregate('campaign-adjudication',[check(out,case)]*3)['score']==0
 assert aggregate('campaign-adjudication',[{'passed':False}]*3)['score']==0
 cards=Path(temp)/'cards';cards.mkdir()
 for i,task in enumerate(WEIGHTS):
  d=cards/task;d.mkdir();(d/'scorecard.json').write_text(json.dumps({'task':task,'scoring_version':'0.5','score':.88 if i==0 else .92}))
 assert summarize(cards)['benchmark_score']==.916
 (cards/next(iter(WEIGHTS))/'scorecard.json').unlink();assert summarize(cards)['benchmark_score']==.828
(ROOT/'scoring_validation.json').write_text(json.dumps({'version':'0.5','passed':True,'checks':['all weight rows sum to 1','parameter partial-credit boundaries','report absence has no effect','report content has no effect','perfect score is 1','parameter perturbation earns partial credit','critical-error caps .69 and .49','unknown advancement cap','invalid required output zero','failed execution zero','ten-task mean .916','missing task zero without reweighting'],'docker_e2e':'not run'},indent=2))
print('Fully automatic scoring regression tests passed.')
