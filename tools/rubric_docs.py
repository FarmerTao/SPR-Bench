"""Generate ten task-specific atomic rubrics from the executable scoring weights."""
from pathlib import Path
import json
from scoring import GROUPS,WEIGHTS
ROOT=Path(__file__).resolve().parents[1]
FOCUS={
'campaign-adjudication':'Assess supported binding and follow-up eligibility across an entire campaign; a smooth or high-response trace alone is insufficient.',
'solvent-reference-recovery':'Recover solvent- and reference-corrected evidence; distinguish apparent responses that disappear after justified correction.',
'kinetic-evidence-audit':'Distinguish binding evidence from permission to report precise kinetic parameters; preserve unresolved and model-inadequate outcomes.',
'condition-consistency':'Preserve flow-condition identities, reproduce condition-specific fits, and reject unsupported pooling of apparent rates.',
'model-adequacy':'Identify when the campaign single-site reporting model is inadequate; better numerical fitting is not proof of a biological mechanism.',
'surface-activity-drift':'Recover control activity and normalized response across batches without rescuing invalid batches by numerical division.',
'replicate-adjudication':'Retain conflicting repeats and correctly withhold unsupported numerical estimates instead of selecting convenient measurements.',
'campaign-reconstruction':'Recover unique traces, indirect compound mappings and declared concentration units before scientific interpretation.',
'pipeline-repair':'Correct the behavior of the supplied faulty pipeline across new cases; equivalent replacement code is acceptable.',
'budgeted-validation':'Prioritize only scientifically eligible candidates under the fixed budget, with consistent advance/reserve/hold dispositions.'}
ATOMS={
'mapping':[('compound_coverage','Exact compound-ID set; missing or extra IDs fail.'),('batch_coverage','Exact acquired-batch set.'),('trace_coverage','Exact distinct acquired-trace set.'),('mapping','Correct trace-to-compound joins, averaged over expected traces.'),('concentration','Correct molar concentration per trace; tolerance 1e-15 M + 1e-8 relative.')],
'correction':[('calibration','Batch solvent slopes match generating calibration; tolerance 0.01 + 0.002 relative.'),('corrected_response','Corrected, baseline-adjusted and activity-normalized endpoint means; tolerance 0.1 RU + 0.01 relative.'),('reference_response','Reference endpoints remove common solvent/baseline without target-activity normalization; tolerance 0.1 RU + 0.01 relative.')],
'qc':[('issues','Exact issue sets per compound; no duplicate reasons.'),('activity','Control activity recovery per batch; tolerance 0.0001 + 0.002 relative.'),('validity','Correct boolean validity for every acquired batch.'),('batch_flag','Every trace carries its batch validity correctly.')],
'fit_consistency':[('condition_fit_coverage','Exactly the required compound/flow fit pairs, including inadequate-model cases that reach assessment.'),('unique_condition_fits','No duplicate compound/flow fit records.'),('fit_reproduction','Each fit reproduces the corrected observations, reports consistent RMSE, and satisfies KD=koff/kon. All three must hold for that condition.')],
'execution':[('input_provenance','Exact SHA-256 manifest of actual inputs, from a successful fresh invocation.'),('structured_output','Nonempty structured compound results, produced by the submitted program.')]
}
LABELS={'mapping':'Identity and units','correction':'Signal correction','qc':'Quality control','binding':'Binding evidence classification','reportability':'Parameter reportability','quantification':'Parameter accuracy','fit_consistency':'Condition-fit consistency','decisions':'Follow-up decisions','execution':'Executable output and provenance'}
index=['# Task-Specific Rubrics','', 'These ten English rubrics expand the implemented v0.5 scoring rules into atomic criteria. Each task totals 1.0; all scoring is automatic. They share verifier primitives but have independent weights and campaign-specific scientific emphasis. They do not introduce unimplemented tests or new deductions.','', 'The administrator-facing rubric files live outside environment/ and are not copied into the agent image. Public task specifications still disclose the required outputs, measurement conventions, execution limits, graded metrics and project decision policies. Generating truth, case labels and private fixtures remain verifier-only during a correctly configured run. Do not hide information necessary for an unambiguous scientific decision.','', '| Task | Main scientific emphasis | Rubric |','|---|---|---|']
for task,weights in WEIGHTS.items():
 rows=[];items=[]
 for i,(group,w)in enumerate(zip(GROUPS,weights),1):
  atoms=[]
  if group in ATOMS:
   for name,requirement in ATOMS[group]:atoms.append({'id':name,'max_score':w/len(ATOMS[group]),'requirement':requirement})
   detail='; '.join(f"**{a['max_score']:.6g} ({100*a['max_score']:.6g}%)**: {a['requirement']}"for a in atoms)
  elif group=='binding':
   detail=f"Split {w:g} equally among the K truth classes present. Each class earns its share times correct predictions / expected members. All-negative output cannot earn the supported-binder share. Missing compounds count as incorrect."
  elif group=='reportability':
   detail=f"Each of N correct kinetic-status labels and 3U correctly withheld parameters earns {w:g}/(N+3U). N is compound count; U is unreportable-compound count. A missing field is not null. A precise unsupported value loses credit and can activate the cap."
  elif group=='quantification':
   detail=f"Split {w:g} over 3P identifiable parameters, where P is the reportable-compound count. Multiply each share by credit(e): 1 for relative error <=1%; (0.25-e)/0.24 for 1%-25%; 0 at >=25% or for invalid values. Unreportable nulls earn no points here."
  else:
   atoms=[{'id':'dispositions','max_score':w*.5,'requirement':'Correct advance/reserve/hold assignment per expected compound, averaged across compounds.'},{'id':'selection','max_score':w*.25,'requirement':'Correct shortlist size, unique eligible members and the declared 10% affinity-equivalence allowance.'},{'id':'selection_order','max_score':w*.25,'requirement':'Correct order under the declared adjacent 10% affinity-equivalence allowance.'}]
   detail='; '.join(f"**{a['max_score']:.6g} ({100*a['max_score']:.6g}%)**: {a['requirement']}"for a in atoms)
  items.append({'id':group,'max_score':w,'weight_percent':100*w,'subcriteria':atoms,'rule':detail})
  rows.append(f"| {i}. {LABELS[group]} | {w:g} | {100*w:g}% | {detail} |")
 text='# '+task+' — Official Automatic Rubric\n\n'+FOCUS[task]+'\n\n**Maximum score: 1.0. No report, human judgment, or LLM judge is scored.**\n\n| Criterion | Max | Weight | Requirements and subcredit |\n|---|---:|---:|---|\n'+'\n'.join(rows)
 text+='''

## Application rules

Evaluate each category on all three campaign fixtures; average the three category achievements equally, multiply by this task's category weight, and sum. Missing expected subcategories receive zero without denominator reweighting. Row order is ignored where IDs establish correspondence. Each expected trace or compound, not arbitrary lines of narrative, is the unit of checking.

A nonzero process exit, missing executable or timeout earns zero for that execution. A required-output contract exception activates the documented zero cap. Unsupported advancement caps the entire task at 0.49; unsupported precise parameters cap it at 0.69; otherwise the cap is 1.0. Keep uncapped submetrics for diagnosis. Reports have no effect, even if absent or misleading.

Fit reproduction uses independently reconstructed observed RMSE <=0.3 RU for ordinary assessed conditions or <=5 RU for model-inadequate cases. Reported RMSE must agree within 0.02 RU + 1% relative, and reported KD must agree with koff/kon within 0.1% relative. These are project-specific synthetic-pilot settings.

See ../SCORING.md for the complete shared numerical contract and tools/scoring.py plus tools/verifier.py for the executable implementation. Expected labels, references and private cases are not defined by text matching. Merely mentioning a correction, uncertainty or diagnosis earns no credit.

## Scope of this rubric

This is a task-specific weighting and atomic expansion of the current shared computational checks, not a claim that ten independent scientific test engines have been implemented. In particular, model adequacy is assessed through the declared reporting model and its evidence; a separate unseen-concentration prediction challenge is not currently scored. Pipeline repair is judged by corrected behavior, not edit count, diagnosis prose, or a newly invented regression-test submission requirement.
'''
 d=ROOT/'rubrics';d.mkdir(exist_ok=True);(d/(task+'.md')).write_text(text);data={'version':'0.5-rubric-detail-1','task':task,'max_score':1.,'focus':FOCUS[task],'criteria':items};(d/(task+'.json')).write_text(json.dumps(data,indent=2)+'\n')
 assert abs(sum(x['max_score']for x in items)-1)<1e-12
 for item in items:
  if item['subcriteria']:assert abs(sum(x['max_score']for x in item['subcriteria'])-item['max_score'])<1e-12
 index.append(f"| {task} | {FOCUS[task]} | [{task}](rubrics/{task}.md) |")
(ROOT/'RUBRICS.md').write_text('\n'.join(index)+'\n')
print('Ten rubric tables generated; all category and fixed subcriterion weights verified.')
