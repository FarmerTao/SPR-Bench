"""Generate ten integrated synthetic research campaigns and independent truth."""
import csv,json,math,random,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def js(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
def csvout(p,headers,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='')as f:w=csv.writer(f);w.writerow(headers);w.writerows(rows)
def response(t,c,kon,koff,rm,end):
 t=max(t,0);rate=kon*c+koff
 return rm*kon*c/rate*(1-math.exp(-rate*min(t,end)))*math.exp(-koff*max(t-end,0))
SPECS=[
('campaign-adjudication','Adjudicate an SPR Screening Campaign','Deliver an evidence-supported hit assessment for a screening campaign assembled from several acquisition batches. Reconcile the sample records, determine which experiments can support a conclusion, and distinguish interpretable binding from apparent hits that do not survive the campaign controls. Produce a defensible follow-up shortlist.',['clean','negative','reference','invalid','discordant']*3),
('solvent-reference-recovery','Recover Binding Evidence from Solvent-Affected Runs','The screening team reports strong responses that change between solvent conditions. Determine which compounds retain credible binding evidence after defensible calibration and correction. Quantify the recovered responses and identify cases that should not be advanced.',['clean','negative','reference']*5),
('kinetic-evidence-audit','Audit the Reportability of Binding Kinetics','Audit the kinetic characterization campaign. Decide which compounds support numerical rate constants, which show binding but do not support the proposed kinetic interpretation, and which require a repeat. Supply condition-specific fits and explain the limits of the reportable estimates.',['clean','slow','heterogeneous','discordant']*4),
('condition-consistency','Assess Flow-Dependent Binding Evidence','Evaluate whether the characterization results are stable across flow conditions. Determine which compounds admit a common intrinsic-rate interpretation and which should be held for a condition-dependence investigation. Do not infer a unique transport mechanism from disagreement alone.',['clean','flow','reference','negative']*4),
('model-adequacy','Resolve Model Inadequacy in a Binding Campaign','A previous campaign report presented every response as a single-site kinetic interaction. Reassess whether that description is supported across concentration and replicate series. Identify compounds for which a simple model is an adequate reporting model and those requiring a more cautious interpretation.',['clean','heterogeneous','slow','negative']*4),
('surface-activity-drift','Recover a Campaign with Changing Surface Activity','Recover the campaign interpretation across changing surface activity and invalid acquisitions. Use the supplied control measurements to determine whether normalization is supported. Distinguish declining assay performance from genuine differences between compounds, and report which conclusions remain usable.',['clean','invalid','negative','clean','reference']*3),
('replicate-adjudication','Reconcile Conflicting Replicate Measurements','Resolve disagreement between independent replicate series. Distinguish stable evidence from compounds whose apparent affinity cannot be responsibly summarized by a single estimate. Preserve every measurement in the audit trail and do not discard disagreeing repeats merely to improve a fit.',['clean','discordant','reference','slow']*4),
('campaign-reconstruction','Reconstruct and Analyze an Acquisition Archive','Reconstruct the compound identities and concentrations in the acquisition archive, then complete a scientific hit assessment. The archive contains repeated exports, unsorted observations, mixed declared concentration units, and indirect sample identifiers. Demonstrate that the recovered mapping supports the reported conclusions.',['clean','negative','reference','invalid','discordant']*3),
('pipeline-repair','Repair a Faulty SPR Analysis Pipeline','Repair or replace the supplied legacy analysis pipeline so that it produces scientifically defensible results for this campaign and new campaigns using the documented file contract. The current output is not a reference answer. Diagnose the scientific and software defects, deliver a corrected implementation, and include a regression-test explanation in the report.',['clean','negative','reference','slow','heterogeneous','discordant']*3),
('budgeted-validation','Prioritize Orthogonal Validation from Campaign Evidence','Choose a shortlist for the next orthogonal-validation round under the project budget. Decisions must follow from the supplied raw measurements, run validity, replicate consistency, and reportable binding parameters. Make the scientific exclusions auditable; an attractive fitted affinity alone is insufficient.',['clean','clean','negative','reference','invalid','discordant','flow','slow']*3)]
POLICY={'minimum_control_activity':.2,'detection_limit_RU':3.,'reference_signal_limit_RU':10.,'maximum_repeat_cv':.25,'maximum_kon_ratio':1.6,'maximum_model_rmse_RU':.8,'minimum_resolved_drop_RU':.6,'validation_budget':3}
NOTE='''# Acquisition and assay notes

All measurements are synthetic. Response units are RU and time is seconds. Each trace has its own acquisition clock, with negative times preceding injection. Association end times are recorded per injection. Concentration units are declared per injection; sample identifiers resolve through vials.csv and compounds.csv. Repeated exports may contain identical rows. They are not additional experimental replicates.

Solvent calibration gives differential active-minus-reference response against the sample-minus-running-buffer DMSO percentage-point difference. Use the zero-intercept linear calibration for this instrument. The common solvent bulk contribution in each channel is 40 RU per percentage point during injection. It cancels in differential correction but must be removed when evaluating reference-surface response. No persistent solvent contribution remains after injection.

blanks.csv contains matched batch/time blank active and reference measurements. Controls are independent corrected endpoint measurements of a reference interaction with a documented expected response. Within a batch, the control activity ratio acts multiplicatively on target-specific response, not on solvent or reference-surface adsorption. An activity below the project minimum invalidates the batch; division by a very small control value does not rescue it. Control activity is stable within each batch.

Baseline offsets can be estimated from negative times. The last 12 seconds of association define the campaign endpoint statistic. Technical measurement noise is additive, approximately Gaussian, and small compared with the control acceptance limits. Independent replicate numbers must remain distinct.

For reportable simple kinetics the initial response is zero; fit all nonnegative times across concentrations with shared positive kon, koff and Rmax, separately by flow condition. A blank-corrected 1:1 model with no additional intercept is the campaign reporting model. The campaign policy specifies the model-adequacy, replicate-consistency and parameter-reportability gates; these are project conventions, not universal biological laws. Flow-dependent estimates are apparent estimates; they do not establish a unique mechanism.
'''
SPEC='''# Deliverable contract

Implement `/app/submission/run.py` with `--input-dir DIRECTORY --output-dir DIRECTORY`. Keep helpers under /app/submission. Read only the supplied campaign directory for task data. Create the output directory, write all persistent outputs there, and support repeated invocations with fresh paths. No network or precomputed results are available in evaluation. Each invocation has 180 seconds, 2 CPUs, 4 GB RAM, and one BLAS thread.

## results.json
Top-level keys: compounds (one record per compound), selected (ordered compound IDs), batches (one record per acquired batch).
Each compound record contains compound_id, binding_call (supported / not_detected / artifact_suspected / inconclusive), kinetics_status (supported / not_applicable / unresolved / condition_dependent / model_inadequate), issues (list from invalid_control, reference_binding, repeat_disagreement, flow_dependence, model_mismatch, unresolved_dissociation), KD_M, kon_M_inv_s_inv, koff_s_inv, and decision (advance / reserve / hold). Unsupported numeric estimates must be JSON null.
Batch records contain batch_id, solvent_slope (RU per DMSO percentage point), activity_fraction, and valid (boolean).

## Campaign policy
Apply the documented controls before making negative or positive claims. A compound with any invalid acquired batch is inconclusive with invalid_control. Otherwise compare the highest-concentration endpoints across repeats and conditions. An endpoint reference response above reference_signal_limit_RU and reference/(abs(corrected)+reference)>0.8 indicates reference_binding. Corrected response below detection_limit_RU is not_detected under the tested conditions. Excessive endpoint population CV indicates repeat_disagreement. These unresolved/invalid/artifact cases do not admit rate estimates.

For the remaining compounds, compare fitted conditions: kon ratio above maximum_kon_ratio gives condition_dependent; otherwise any condition RMSE above maximum_model_rmse_RU gives model_inadequate. If neither applies, assess the mean highest-concentration dissociation drop from the first three post-switch observations to the last three observations. A drop below minimum_resolved_drop_RU is unresolved. Only compounds passing all gates receive globally fitted numerical rate constants and KD. This ordering defines the project's adjudication convention where issues coexist. These rules determine reportability, not molecular mechanism.

Only binding_call=supported and kinetics_status=supported are eligible. Rank eligible compounds by ascending KD, using compound_id to break exact ties; advance up to validation_budget, reserve other eligible compounds, and hold the rest. Advancement means justified follow-up under this project's policy, not established druglikeness.

## trace_evidence.csv
Columns: trace_id,compound_id,concentration_M,peak_corrected_RU,reference_peak_RU,batch_valid. Include each distinct acquired trace once. Corrected peaks are activity-normalized endpoint means after solvent, matched blank, reference, and baseline correction. Reference peaks remove common solvent response and pre-injection baseline, without activity normalization. Row order is arbitrary; IDs define alignment.

## condition_fits.csv
Columns: compound_id,flow_uL_min,kon,koff,KD,Rmax,rmse. Include a fit for each compound/flow combination reaching model assessment. Records are numerical evidence for the adequacy and condition-consistency decisions; they must not be represented as intrinsic kinetic estimates for failed cases.

## provenance.json and report.md
provenance.json is {"inputs": {"relative/path": "sha256hex", ...}} for all files under input-dir. report.md is optional and is never scored, including its presence or absence. No human or LLM judge participates in scoring.

## Evaluation
The submitted program is rerun on three campaign fixtures. Each task receives a fully automatic score from 0 to 1, using the task-specific weights, submetrics, tolerances and critical-error caps in `/app/spec/SCORING.md`. The same value is written to Harbor reward.txt and scorecard.json. The benchmark score is the arithmetic mean of the ten task scores; each task contributes 10%. Numeric reference values come from independent generating truth. Nonidentifiable parameters must be null. Correct alternative implementations are allowed. Selection permits a 10% generating-affinity equivalence band. Returned files are inspected in a separate verifier.
'''
def campaign(d,n,variant):
 rng=random.Random(46000+n*100+variant);kinds=SPECS[n-1][3][:];rng.shuffle(kinds)
 ids=[f'C{variant}{i:03d}'for i in rng.sample(range(100,999),len(kinds))];times=list(range(-18,421,2));acq=[];measure=[];vials=[];comp=[];truth=[];ev=[];batches={'B1':1.,'B2':.65,'B3':.35,'BX':.04};slopes={b:rng.uniform(100,300)for b in batches}
 for i,(cid,kind)in enumerate(zip(ids,kinds)):
  key=f'P{rng.randrange(10000,99999)}';vial=f'V{rng.randrange(10000,99999)}';vials.append([key,vial]);comp.append([vial,cid]);kon=rng.uniform(1.2e5,3e5);kd=2.5e-8*(1.65**(i%6))*rng.uniform(.94,1.06);koff=kd*kon;rm=rng.uniform(50,80)
  if kind=='slow':koff=1e-5;kd=koff/kon
  batch='BX'if kind=='invalid'else ['B1','B2','B3'][i%3];act=batches[batch];flows=[10,30,100]if n==4 or kind=='flow'else[30]
  call={'negative':'not_detected','reference':'artifact_suspected','invalid':'inconclusive','discordant':'inconclusive'}.get(kind,'supported');status={'negative':'not_applicable','reference':'not_applicable','invalid':'not_applicable','discordant':'not_applicable','slow':'unresolved','flow':'condition_dependent','heterogeneous':'model_inadequate'}.get(kind,'supported');issue={'reference':'reference_binding','invalid':'invalid_control','discordant':'repeat_disagreement','slow':'unresolved_dissociation','flow':'flow_dependence','heterogeneous':'model_mismatch'}.get(kind)
  truth.append({'compound_id':cid,'binding_call':call,'kinetics_status':status,'issues':[issue]if issue else[],'KD_M':kd if kind=='clean'else None,'kon_M_inv_s_inv':kon if kind=='clean'else None,'koff_s_inv':koff if kind=='clean'else None,'decision':'eligible'if kind=='clean'else'hold'})
  for flow in flows:
   for rep in [1,2]:
    for j,c in enumerate([5e-9,2e-8,8e-8,3.2e-7,1.28e-6]):
     tid=f'T{variant}{len(acq):05d}';end=120;tt=times if kind!='slow'else list(range(-18,133,2));dmso=rng.uniform(-.25,.25);unit='nM'if (i+j+rep)%2 else'uM';value=c/(1e-9 if unit=='nM'else 1e-6);acq.append([tid,key,batch,rep,flow,value,unit,end,dmso]);yy=[];rr=[]
     for t in tt:
      gate=0<=t<=end;bulk=40*dmso*gate;blank=.015*t+1.7
      kk=kon*({10:.25,30:.5,100:1}[flow]if kind=='flow'else 1)
      signal=response(t,c,kk,koff,rm,end)
      reference=0.
      if kind=='negative':signal=0.
      if kind=='reference':reference=response(t,c,kon,.02,60,end);signal=.015*reference
      if kind=='heterogeneous':signal=.5*response(t,c,kon,.035,rm,end)+.5*response(t,c,kon,.001,rm,end)
      if kind=='discordant'and rep==2:signal*=.25
      noise=rng.gauss(0,.025);ref=2+bulk+reference;active=ref+blank+slopes[batch]*dmso*gate+act*signal+noise
      measure.append([tid,t,active,ref]);yy.append(signal+noise/act);rr.append(reference)
     base=sum(y for t,y in zip(tt,yy)if t<0)/sum(t<0 for t in tt);peak=sum(y-base for t,y in zip(tt,yy)if end-12<=t<=end)/7;refpeak=sum(y for t,y in zip(tt,rr)if end-12<=t<=end)/7
     ev.append([tid,cid,c,peak,refpeak,act>=.2])
 if n in [8,9]:acq+=acq[2:7];measure+=measure[10:30];rng.shuffle(acq);rng.shuffle(measure)
 csvout(d/'acquisition.csv',['trace_id','sample_key','batch_id','replicate','flow_uL_min','concentration_value','concentration_unit','association_end_s','delta_dmso_pct'],acq);csvout(d/'measurements.csv',['trace_id','time_s','active_RU','reference_RU'],measure);csvout(d/'vials.csv',['sample_key','vial_id'],vials);csvout(d/'compounds.csv',['vial_id','compound_id'],comp)
 csvout(d/'blanks.csv',['batch_id','time_s','active_RU','reference_RU'],[[b,t,.015*t+3.7,2.]for b in batches for t in times]);csvout(d/'solvent_calibration.csv',['batch_id','delta_dmso_pct','differential_RU'],[[b,x,slopes[b]*x]for b in batches for x in [-.3,-.15,0,.15,.3]]);csvout(d/'controls.csv',['batch_id','control_replicate','expected_RU','observed_RU'],[[b,r,50,50*a*factor]for b,a in batches.items()for r,factor in [(1,.98),(2,1.02)]])
 js(d/'project.json',POLICY);(d/'RUN_NOTES.md').write_text(NOTE)
 eligible=sorted([x for x in truth if x['decision']=='eligible'],key=lambda x:x['KD_M']);selected=[x['compound_id']for x in eligible[:3]]
 for x in truth:
  if x['decision']=='eligible':x['decision']='advance'if x['compound_id']in selected else'reserve'
 acquired={r[2]for r in acq}
 return {'compounds':truth,'selected':selected,'batches':[{'batch_id':b,'solvent_slope':slopes[b],'activity_fraction':a,'valid':a>=.2}for b,a in batches.items()if b in acquired]},ev

catalog=[]
for n,(slug,title,objective,kinds)in enumerate(SPECS,1):
 p=ROOT/'tasks'/slug
 for variant in [0,1,2]:
  case=p/'tests'/'cases'/str(variant);d=case/'data';d.mkdir(parents=True,exist_ok=True);truth,evidence=campaign(d,n,variant);js(case/'truth.json',truth);csvout(case/'trace_truth.csv',['trace_id','compound_id','concentration_M','peak_corrected_RU','reference_peak_RU','batch_valid'],evidence)
 env=p/'environment';shutil.copytree(p/'tests'/'cases'/'0'/'data',env/'data',dirs_exist_ok=True);(env/'spec').mkdir(exist_ok=True);(env/'spec'/'CONTRACT.md').write_text(SPEC)
 if n==9:
  (env/'legacy').mkdir(exist_ok=True)
  legacy=(ROOT/'tools'/'engine.py').read_text().replace('Research workflow reference; reads only supplied experimental files.','Legacy campaign processor retained for reproducibility; requires scientific audit.')
  legacy=legacy.replace("-blank-slopes[x['batch_id']]","-blank-0*slopes[x['batch_id']]").replace("{'nM':1e-9,'uM':1e-6}","{'nM':1e-6,'uM':1e-6}").replace("elif cv>policy['maximum_repeat_cv']:","elif cv>100:").replace("key=lambda x:(x['KD_M'],x['compound_id'])","key=lambda x:(-x['KD_M'],x['compound_id'])")
  (env/'legacy'/'analyze.py').write_text(legacy)
 instruction=f'''# {title}

{objective}

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.
'''
 if n==9:instruction+='\nThe legacy implementation is under `/app/legacy/`; its outputs are not ground truth. Your submission may repair it or replace it with a justified implementation.\n'
 (p/'instruction.md').write_text(instruction)
 (env/'requirements.txt').write_text('numpy==2.2.6\nscipy==1.15.3\npandas==2.2.3\nmatplotlib==3.10.3\n')
 (env/'Dockerfile').write_text('FROM python:3.12.10-slim\nWORKDIR /app\nCOPY requirements.txt /tmp/requirements.txt\nRUN pip install --no-cache-dir -r /tmp/requirements.txt\nCOPY data /app/data\nCOPY spec /app/spec\n'+('COPY legacy /app/legacy\n'if n==9 else'')+'RUN mkdir -p /app/submission /app/output\nCMD ["bash"]\n')
 (p/'task.toml').write_text('''schema_version = "1.4"
artifacts = ["/app/submission"]
[task]
name = "spr-research/'''+slug+'''"
description = "'''+title+'''"
[metadata]
author_name = "SPR research pilot"
difficulty = "hard"
category = "scientific-data-analysis"
tags = ["spr", "campaign-analysis", "synthetic"]
[agent]
timeout_sec = 3600.0
[verifier]
timeout_sec = 600.0
environment_mode = "separate"
[verifier.environment]
network_mode = "no-network"
cpus = 2
memory_mb = 4096
storage_mb = 10240
[environment]
network_mode = "no-network"
cpus = 2
memory_mb = 4096
storage_mb = 10240
build_timeout_sec = 600.0
''')
 sol=p/'solution';sol.mkdir(exist_ok=True);shutil.copyfile(ROOT/'tools'/'engine.py',sol/'run.py');(sol/'solve.sh').write_text('#!/bin/bash\nset -eu\nmkdir -p /app/submission\ncp /solution/run.py /app/submission/run.py\npython3 /app/submission/run.py --input-dir /app/data --output-dir /app/output\n')
 (p/'tests'/'Dockerfile').write_text('FROM python:3.12.10-slim\nRUN pip install --no-cache-dir numpy==2.2.6 scipy==1.15.3 pandas==2.2.3 matplotlib==3.10.3\nCOPY . /tests\nWORKDIR /app\nRUN mkdir -p /logs/verifier\nCMD ["bash"]\n')
 (p/'tests'/'test.sh').write_text('#!/bin/bash\nset -eu\nmkdir -p /logs/verifier\nprintf "0\\n" > /logs/verifier/reward.txt\npython3 /tests/verifier.py\n')
 for f in [sol/'solve.sh',p/'tests'/'test.sh']:f.chmod(0o755)
 catalog.append({'id':n,'slug':slug,'title':title,'objective':objective,'compounds_per_case':len(kinds),'cases':3})
js(ROOT/'task_catalog.json',catalog)
print('Generated ten research campaigns')
