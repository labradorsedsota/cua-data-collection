#!/usr/bin/env python3
"""
Fix 77 non-compliant result JSON files for worker-02.
Transforms old format → worker-execution-guide.md standard schema.

Output: writes fixed files to results_fixed/ for diff review,
        then copies to results/worker-02/ on confirmation.
"""

import json
import os
import re
import glob
import shutil
from datetime import datetime

RESULTS_DIR = "results/worker-02"
LOGS_DIR = "logs"
TASKS_DIR = "tasks/pool-clean"
FIXED_DIR = "results_fixed/worker-02"
WORKER = "worker-02"

os.makedirs(FIXED_DIR, exist_ok=True)


def parse_log(task_id):
    """Extract sess_id, duration, total_steps, last_reasoning, last_action, status from log."""
    log_path = os.path.join(LOGS_DIR, f"{task_id}.log")
    if not os.path.exists(log_path):
        return None

    with open(log_path, "r", errors="replace") as f:
        content = f.read()

    info = {}

    # Extract sess_id
    m = re.search(r"Session created:\s*(sess-\S+)", content)
    if m:
        info["sess_id"] = m.group(1)

    # Extract DURATION
    m = re.search(r"DURATION:\s*(\d+)", content)
    if m:
        info["duration_seconds"] = int(m.group(1))

    # Extract total steps and status from evaluation block
    m = re.search(r"Status:\s*(COMPLETED|FAILED|TIMEOUT)", content)
    if m:
        info["mano_status"] = m.group(1)

    m = re.search(r"Total steps:\s*(\d+)", content)
    if m:
        info["total_steps"] = int(m.group(1))

    m = re.search(r"Last action:\s*(.+)", content)
    if m:
        info["last_action"] = m.group(1).strip()

    # Extract last reasoning - find the last [step N] Reasoning block
    # or the evaluation block's Last reasoning
    m = re.search(r"Last reasoning:\s*(.+?)(?:\n={10,}|\nUI window|\nDURATION)", content, re.DOTALL)
    if m:
        info["last_reasoning"] = m.group(1).strip()[:2000]
    else:
        # Fallback: find the last [step N] Reasoning
        reasonings = re.findall(r"\[step \d+\] Reasoning:\s*(.+?)(?=\n\[step|\nEvaluating|\n={5,}|\Z)", content, re.DOTALL)
        if reasonings:
            info["last_reasoning"] = reasonings[-1].strip()[:2000]

    return info if info else None


def load_task_card(task_id):
    """Load task card to get repo field."""
    path = os.path.join(TASKS_DIR, f"{task_id}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    # Also check tasks/pool/
    path2 = os.path.join("tasks/pool", f"{task_id}.json")
    if os.path.exists(path2):
        with open(path2) as f:
            return json.load(f)
    return None


def determine_failure_type(d):
    """Determine failure.type from old format data."""
    summary = (d.get("reasoning_summary", "") + " " + d.get("notes", "")).lower()
    status = d.get("status", "")
    error_type = d.get("error_type", "")

    if "deploy_failed" in summary or "deploy_failed" in str(error_type) or status == "deploy_failed":
        return "deploy_failed"
    if "tauri" in summary:
        return "deploy_failed"
    if "timeout" in summary:
        return "timeout"
    return "deploy_failed"


def build_failure_object(d):
    """Build a failure object from old format data."""
    summary = d.get("reasoning_summary", "")
    notes = d.get("notes", "")
    symptom = summary if summary else notes
    if not symptom:
        symptom = f"status was '{d.get('status', 'unknown')}' with no details"

    return {
        "type": determine_failure_type(d),
        "symptom": symptom[:500],
        "attempted": [],
        "recommendation": notes[:200] if notes and notes != summary else "跳过"
    }


def fix_file(task_id):
    """Fix a single result file. Returns (fixed_data, change_description) or None if already compliant."""
    path = os.path.join(RESULTS_DIR, f"{task_id}.json")
    with open(path) as f:
        d = json.load(f)

    # Check if already compliant
    status = d.get("status")
    if status in ("completed", "failed"):
        has_sess = "sess_id" in d
        has_exp = "expected_result_used" in d
        has_dur = "duration_seconds" in d
        if status == "completed" and has_sess and has_exp and has_dur:
            mc = d.get("mano_cua")
            if mc and all(k in mc for k in ["status", "total_steps", "last_action", "result", "result_summary", "last_reasoning"]):
                return None  # Already compliant
        if status == "failed" and has_sess and has_exp and has_dur and d.get("failure") is not None:
            return None  # Already compliant

    # Parse log if available
    log_info = parse_log(task_id)

    # Load task card for repo
    task_card = load_task_card(task_id)
    repo = d.get("repo") or (task_card.get("repo") if task_card else None) or "unknown/unknown"

    # Determine old session_id
    old_sess_id = d.get("session_id") or d.get("sess_id") or ""
    old_result = d.get("result") or d.get("status") or ""
    old_total_steps = d.get("total_steps", 0)
    old_reasoning = d.get("reasoning_summary", "")

    # Special case: vue-pdf-179/189 (sess_id format error)
    if task_id in ("vue-pdf-179", "vue-pdf-189"):
        fixed = {
            "task_id": task_id,
            "repo": repo,
            "worker": WORKER,
            "status": "failed",
            "sess_id": None,
            "expected_result_used": False,
            "duration_seconds": 0,
            "timestamp": d.get("timestamp", ""),
            "mano_cua": None,
            "failure": {
                "type": "other",
                "symptom": d.get("mano_cua", {}).get("result_summary", "页面无目标功能入口"),
                "attempted": ["代码审查确认 App.vue 未实现目标功能 UI"],
                "recommendation": "跳过，页面无目标功能按钮"
            }
        }
        return fixed, "sess_id格式修复→failed+failure对象"

    # Special case: website-4566/4776/4780 (failure is null)
    if task_id.startswith("website-") and d.get("status") == "failed" and d.get("failure") is None:
        detail = d.get("failure_detail", "") or d.get("failure_reason", "")
        fixed = dict(d)
        # Remove non-standard fields
        for k in ["failure_reason", "failure_detail"]:
            fixed.pop(k, None)
        # Fix sess_id for failed cases
        if fixed.get("sess_id") == "N/A":
            fixed["sess_id"] = None
        fixed["failure"] = {
            "type": "deploy_failed",
            "symptom": detail[:500] if detail else "git clone timeout",
            "attempted": ["proxy clone", "直连 clone", "gh cli clone", "blob filter clone"],
            "recommendation": "跳过，asyncapi/website 仓库过大无法 clone"
        }
        fixed["mano_cua"] = None
        return fixed, "failure字段重构"

    # Determine if this case actually ran mano-cua successfully
    has_session = bool(old_sess_id) or (log_info and "sess_id" in log_info)
    ran_mano = has_session or old_total_steps > 0

    # Override: if original status was error/deploy_failed and total_steps=0,
    # treat as failed even if log has a sess_id (mano-cua started but app broken)
    if old_result in ("error",) and old_total_steps == 0:
        ran_mano = False
    if d.get("error_type") == "DEPLOY_FAILED" and old_total_steps == 0:
        ran_mano = False
    # sess_id like "inferred-from-*" means mano-cua was NOT actually run
    if old_sess_id and old_sess_id.startswith("inferred-"):
        ran_mano = False

    if ran_mano:
        # Case ran mano-cua → status: completed
        sess_id = old_sess_id or (log_info.get("sess_id") if log_info else None) or ""
        duration = d.get("duration_seconds") or (log_info.get("duration_seconds") if log_info else 0) or 0
        total_steps = (log_info.get("total_steps") if log_info else None) or old_total_steps or 0
        last_action = (log_info.get("last_action") if log_info else None) or "DONE"
        last_reasoning = ""
        if log_info and "last_reasoning" in log_info:
            last_reasoning = log_info["last_reasoning"]
        elif old_reasoning:
            last_reasoning = old_reasoning

        # Map old result to mano_cua.result
        result_map = {
            "abnormal": "abnormal",
            "normal": "normal",
            "unclear": "unclear",
            "error": "unclear",
        }
        mc_result = result_map.get(old_result, "unclear")
        result_summary = old_reasoning or d.get("notes", "") or ""

        fixed = {
            "task_id": task_id,
            "repo": repo,
            "worker": WORKER,
            "status": "completed",
            "sess_id": sess_id,
            "expected_result_used": False,
            "duration_seconds": duration,
            "timestamp": d.get("timestamp", ""),
            "mano_cua": {
                "status": (log_info.get("mano_status") if log_info else None) or "COMPLETED",
                "total_steps": total_steps,
                "last_action": last_action,
                "result": mc_result,
                "result_summary": result_summary[:500],
                "last_reasoning": last_reasoning[:2000] if last_reasoning else result_summary[:500]
            }
        }
        return fixed, f"旧格式→completed, result={mc_result}"

    else:
        # Case did NOT run mano-cua → status: failed
        failure_obj = build_failure_object(d)
        # For old format that have result_summary with details
        if d.get("result_summary") and failure_obj["symptom"].startswith("status was"):
            failure_obj["symptom"] = d["result_summary"][:500]
        fixed = {
            "task_id": task_id,
            "repo": repo,
            "worker": WORKER,
            "status": "failed",
            "sess_id": None,
            "expected_result_used": False,
            "duration_seconds": 0,
            "timestamp": d.get("timestamp", ""),
            "mano_cua": None,
            "failure": failure_obj
        }
        return fixed, f"旧格式→failed, type={fixed['failure']['type']}"


def main():
    files = sorted([f.replace(".json", "") for f in os.listdir(RESULTS_DIR) if f.endswith(".json")])

    fixed_count = 0
    skip_count = 0
    errors = []
    changes = []

    for task_id in files:
        try:
            result = fix_file(task_id)
            if result is None:
                skip_count += 1
                # Copy as-is to fixed dir
                shutil.copy(
                    os.path.join(RESULTS_DIR, f"{task_id}.json"),
                    os.path.join(FIXED_DIR, f"{task_id}.json")
                )
            else:
                fixed_data, desc = result
                with open(os.path.join(FIXED_DIR, f"{task_id}.json"), "w") as f:
                    json.dump(fixed_data, f, indent=2, ensure_ascii=False)
                fixed_count += 1
                changes.append((task_id, desc))
        except Exception as e:
            errors.append((task_id, str(e)))

    print(f"\n=== Fix Summary ===")
    print(f"Total files: {len(files)}")
    print(f"Already compliant (skipped): {skip_count}")
    print(f"Fixed: {fixed_count}")
    print(f"Errors: {len(errors)}")

    if errors:
        print(f"\nErrors:")
        for tid, err in errors:
            print(f"  {tid}: {err}")

    print(f"\nChanges:")
    for tid, desc in changes:
        print(f"  {tid}: {desc}")


if __name__ == "__main__":
    main()
