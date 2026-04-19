#!/usr/bin/env python3
"""
Batch 9 post-processing: fix dev_url, exclude >50K stars, add backend_risk/repo_size_kb.
"""
import json, os, sys, time
import urllib.request
import urllib.error
from collections import Counter

INPUT = "data/batch9_tasks.jsonl.final"
OUTPUT = "data/batch9_tasks.jsonl.fixed"
MANIFEST = "data/batch9_manifest.json"
REPO_META_CACHE = "data/batch9_repo_meta.json"

# Port mapping
PORT_MAP = {
    "angular": 4200,
    "react": 3000,      # default for CRA; Vite overrides below
    "nextjs": 3000,
    "nuxt": 3000,
    "vue": 5173,         # Vue+Vite default
    "svelte": 5173,
    "preact": 5173,
    "vite": 5173,
    "other": 5173,
    "unknown": 5173,
    "nestjs": 3000,
}

# Backend risk keywords in deploy_commands
BACKEND_KEYWORDS = [
    "docker", "postgres", "mysql", "mongodb", "redis", "supabase",
    "prisma migrate", "db:seed", "db:create", "database",
    "flask", "django", "rails", "laravel", "express",
    "docker-compose", "docker compose",
]

def detect_port(card):
    fw = card.get("framework", "unknown")
    port = PORT_MAP.get(fw, 5173)
    
    # For react: check if Vite-based
    deploy = " ".join(card.get("deploy_commands", []))
    if fw == "react":
        if "vite" in deploy.lower() or "@vitejs" in deploy.lower():
            port = 5173
        else:
            port = 3000
    
    # For vue: check if CLI-based (8080) vs Vite (5173)
    if fw == "vue":
        if "vue-cli-service" in deploy.lower() or "@vue/cli" in deploy.lower():
            port = 8080
    
    return port

def detect_backend_risk(card):
    deploy = " ".join(card.get("deploy_commands", [])).lower()
    for kw in BACKEND_KEYWORDS:
        if kw in deploy:
            return True
    return False

# Step 1: Load cards
with open(INPUT) as f:
    cards = [json.loads(line) for line in f]
print(f"Loaded {len(cards)} cards from {INPUT}")

# Step 2: Query GitHub API for stars + size
repos = list(set(c.get("repo", "") for c in cards))
print(f"Querying GitHub API for {len(repos)} repos...")

repo_meta = {}
if os.path.exists(REPO_META_CACHE):
    with open(REPO_META_CACHE) as f:
        repo_meta = json.load(f)
    print(f"  Loaded {len(repo_meta)} from cache")

for i, repo in enumerate(repos):
    if repo in repo_meta:
        continue
    if i % 50 == 0 and i > 0:
        print(f"  [{i}/{len(repos)}] queried...")
        # Save cache periodically
        with open(REPO_META_CACHE, "w") as f:
            json.dump(repo_meta, f)
    
    try:
        url = f"https://api.github.com/repos/{repo}"
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {os.environ.get('GITHUB_TOKEN', '')}",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            repo_meta[repo] = {
                "stars": data.get("stargazers_count", 0),
                "size_kb": data.get("size", 0),
            }
    except Exception as e:
        repo_meta[repo] = {"stars": 0, "size_kb": 0, "error": str(e)}
    time.sleep(0.3)  # Rate limit

# Save final cache
with open(REPO_META_CACHE, "w") as f:
    json.dump(repo_meta, f, indent=2)
print(f"  Done. {len(repo_meta)} repos queried.")

# Step 3: Exclude >50K stars
excluded_stars = {r for r, m in repo_meta.items() if m.get("stars", 0) > 50000}
if excluded_stars:
    print(f"\nExcluding {len(excluded_stars)} repos with >50K stars:")
    for r in sorted(excluded_stars):
        stars = repo_meta[r].get("stars", 0)
        cnt = sum(1 for c in cards if c.get("repo") == r)
        print(f"  {r}: {stars:,} stars, {cnt} cards")

before_count = len(cards)
cards = [c for c in cards if c.get("repo", "") not in excluded_stars]
print(f"  Removed {before_count - len(cards)} cards")

# Step 4: Fix dev_url
port_changes = Counter()
for card in cards:
    port = detect_port(card)
    old_url = card.get("dev_url", "")
    card["dev_url"] = f"http://localhost:{port}"
    if old_url != card["dev_url"]:
        port_changes[f"{old_url} → {card['dev_url']}"] += 1

print(f"\nPort fixes:")
for change, cnt in port_changes.most_common():
    print(f"  {change}: {cnt}")

# Step 5: Add backend_risk + repo_size_kb
risk_count = 0
for card in cards:
    repo = card.get("repo", "")
    card["backend_risk"] = detect_backend_risk(card)
    card["repo_size_kb"] = repo_meta.get(repo, {}).get("size_kb", 0)
    if card["backend_risk"]:
        risk_count += 1

print(f"\nbackend_risk=True: {risk_count}/{len(cards)} ({risk_count*100/len(cards):.1f}%)")

# Step 6: Write output
with open(OUTPUT, "w") as f:
    for c in cards:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")
print(f"\nWritten {len(cards)} cards to {OUTPUT}")

# Step 7: Generate manifest
fw_dist = Counter(c.get("framework", "") for c in cards)
score_dist = Counter(c.get("_ui_score", 0) for c in cards)
manifest = {
    "batch": "batch9",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "input": {
        "stage1_raw": "data/batch9_raw.jsonl",
        "stage1_count": 5027,
        "stage1_repos": 477,
    },
    "stage2": {
        "total_processed": 5027,
        "valid": 3374,
        "rejected": 1492,
        "errors": 161,
        "pass_rate": "67.1%",
    },
    "post_processing": {
        "per_repo_cap": 8,
        "after_cap": 2563,
        "excluded_high_stars": list(excluded_stars),
        "excluded_card_count": before_count - len([c for c in cards]),
        "port_fixes": dict(port_changes.most_common()),
        "backend_risk_count": risk_count,
        "backend_risk_pct": f"{risk_count*100/len(cards):.1f}%",
    },
    "final": {
        "total_cards": len(cards),
        "unique_repos": len(set(c.get("repo","") for c in cards)),
        "framework_distribution": dict(fw_dist.most_common()),
        "ui_score_distribution": {str(k): v for k, v in sorted(score_dist.items())},
    }
}

with open(MANIFEST, "w") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print(f"Manifest written to {MANIFEST}")

# Summary
print(f"\n=== FINAL SUMMARY ===")
print(f"Total cards: {len(cards)}")
print(f"Unique repos: {manifest['final']['unique_repos']}")
print(f"Framework: {dict(fw_dist.most_common(10))}")
print(f"Backend risk: {risk_count} ({risk_count*100/len(cards):.1f}%)")
print(f"Avg repo_size_kb: {sum(c.get('repo_size_kb',0) for c in cards)/len(cards):.0f}")
