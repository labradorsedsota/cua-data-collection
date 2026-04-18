#!/usr/bin/env python3
"""
Batch 9 Stage 1: Screen untouched candidates via bug_screener.py.
Commits output every 20 repos for safety.
"""
import json, subprocess, sys, os, time, glob
from collections import Counter

CANDIDATES = "data/batch9_candidates.jsonl"
OUTPUT = "data/batch9_raw.jsonl"
POOL_DIR = "tasks/pool"
MAX_BUGS_PER_REPO = 15
COMMIT_INTERVAL = 20

with open(CANDIDATES) as f:
    candidates = [json.loads(line) for line in f]

pool_tasks = set()
for fp in glob.glob(f"{POOL_DIR}/*.json"):
    try:
        with open(fp) as fh:
            pool_tasks.add(json.load(fh).get("task_id", ""))
    except: pass

print(f"[batch9-s1] {len(candidates)} candidates, {len(pool_tasks)} existing tasks", flush=True)

total_raw = 0
processed = 0
errors = 0
repos_with_cards = 0

outf = open(OUTPUT, "a" if os.path.exists(OUTPUT) else "w")

# Resume support
existing_repos = set()
if os.path.exists(OUTPUT):
    with open(OUTPUT) as f:
        for line in f:
            try: existing_repos.add(json.loads(line).get("repo", ""))
            except: pass
    if existing_repos:
        print(f"  Resuming: {len(existing_repos)} repos already processed", flush=True)

for i, cand in enumerate(candidates):
    repo = cand["name"]
    if repo in existing_repos:
        continue

    processed += 1

    if processed % 5 == 1:
        print(f"[{processed}/{len(candidates)}] {repo} (raw: {total_raw}, repos_ok: {repos_with_cards}, err: {errors})", flush=True)

    try:
        result = subprocess.run(
            [sys.executable, "scripts/bug_screener.py", repo, "--limit", str(MAX_BUGS_PER_REPO)],
            capture_output=True, text=True, timeout=120,
            cwd=os.getcwd()
        )

        if result.returncode != 0:
            errors += 1
            continue

        repo_cards = 0
        for line in result.stdout.strip().split("\n"):
            if not line.strip(): continue
            try:
                card = json.loads(line)
                if card.get("task_id", "") in pool_tasks:
                    continue
                outf.write(json.dumps(card, ensure_ascii=False) + "\n")
                outf.flush()
                total_raw += 1
                repo_cards += 1
            except json.JSONDecodeError:
                continue

        if repo_cards > 0:
            repos_with_cards += 1

    except subprocess.TimeoutExpired:
        errors += 1
        print(f"  TIMEOUT: {repo}", flush=True)
    except Exception as e:
        errors += 1

    # Auto-commit every COMMIT_INTERVAL repos
    if processed % COMMIT_INTERVAL == 0 and total_raw > 0:
        outf.flush()
        os.system(f'cd {os.getcwd()} && git add {OUTPUT} && git commit -m "batch9-s1: {processed} repos scanned, {total_raw} raw candidates" --quiet')
        print(f"  [committed at {processed} repos]", flush=True)

    time.sleep(1)

outf.close()

# Final commit
os.system(f'cd {os.getcwd()} && git add {OUTPUT} && git commit -m "batch9-s1 COMPLETE: {processed} repos, {total_raw} raw, {repos_with_cards} producing, {errors} errors" --quiet')

print(f"\n[batch9 Stage 1 COMPLETE]", flush=True)
print(f"  Processed: {processed}/{len(candidates)}")
print(f"  Raw candidates: {total_raw}")
print(f"  Repos with cards: {repos_with_cards}")
print(f"  Errors/timeouts: {errors}")
print(f"  Output: {OUTPUT}")
