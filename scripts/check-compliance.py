#!/usr/bin/env python3
"""Compliance checker - validates all result JSON files against the spec."""
import json, os, sys

FIXED_DIR = "results_fixed/worker-02"
passed = 0
failed = 0
issues = []

for f in sorted(os.listdir(FIXED_DIR)):
    if not f.endswith('.json'): continue
    tid = f.replace('.json','')
    d = json.load(open(os.path.join(FIXED_DIR, f)))
    errs = []
    
    # Required top-level fields
    for req in ["task_id","repo","worker","status","sess_id","expected_result_used","duration_seconds","timestamp"]:
        if req not in d:
            errs.append(f"missing field: {req}")
    
    status = d.get("status")
    if status not in ("completed","failed"):
        errs.append(f"invalid status: {status}")
    
    if status == "completed":
        mc = d.get("mano_cua")
        if mc is None:
            errs.append("completed but mano_cua is null")
        elif not isinstance(mc, dict):
            errs.append("mano_cua is not a dict")
        else:
            for mf in ["status","total_steps","last_action","result","result_summary","last_reasoning"]:
                if mf not in mc:
                    errs.append(f"mano_cua missing: {mf}")
            r = mc.get("result")
            if r not in ("normal","abnormal","unclear"):
                errs.append(f"invalid mano_cua.result: {r}")
        
        sid = d.get("sess_id")
        if sid is not None and not str(sid).startswith("sess-"):
            errs.append(f"invalid sess_id format: {sid}")
    
    if status == "failed":
        fail = d.get("failure")
        if fail is None:
            errs.append("failed but failure is null")
        elif not isinstance(fail, dict):
            errs.append("failure is not a dict")
        else:
            for ff in ["type","symptom","attempted","recommendation"]:
                if ff not in fail:
                    errs.append(f"failure missing: {ff}")
            ft = fail.get("type")
            if ft not in ("deploy_failed","timeout","mano_cua_error","url_deviation","other"):
                errs.append(f"invalid failure.type: {ft}")
    
    if errs:
        failed += 1
        issues.append((tid, errs))
    else:
        passed += 1

print(f"=== Compliance Check ===")
print(f"Passed: {passed}/{passed+failed}")
print(f"Failed: {failed}/{passed+failed}")
if issues:
    print(f"\nIssues:")
    for tid, errs in issues:
        for e in errs:
            print(f"  {tid}: {e}")
