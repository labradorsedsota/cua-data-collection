#!/usr/bin/env python3
"""
Batch 1-8 unknown framework annotation fix.
Reads package.json from GitHub API for each repo, detects framework from dependencies.
Updates pool/ JSON cards with correct framework field.
"""
import json, os, sys, time
import urllib.request
import urllib.error

POOL_DIR = "tasks/pool"
BATCH9_FILE = "data/batch9_tasks.jsonl.final"

# Framework detection rules (order matters - first match wins for meta-frameworks)
FRAMEWORK_RULES = [
    # Meta-frameworks first (they imply the base framework)
    ("Next.js", ["next"]),
    ("Nuxt", ["nuxt", "nuxt3"]),
    ("Gatsby", ["gatsby"]),
    ("Remix", ["@remix-run/react"]),
    ("SvelteKit", ["@sveltejs/kit"]),
    # Base frameworks
    ("React", ["react", "react-dom", "preact"]),
    ("Vue", ["vue"]),
    ("Angular", ["@angular/core"]),
    ("Svelte", ["svelte"]),
    ("Ember", ["ember-cli", "ember-source"]),
    ("Lit", ["lit", "lit-element"]),
    ("Solid", ["solid-js"]),
    ("Alpine", ["alpinejs"]),
    ("Stimulus", ["@hotwired/stimulus", "stimulus"]),
]

def detect_framework(pkg_json):
    """Detect framework from package.json content."""
    all_deps = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        deps = pkg_json.get(key, {})
        if isinstance(deps, dict):
            all_deps.update(deps)
    
    dep_names = set(all_deps.keys())
    
    for framework_name, markers in FRAMEWORK_RULES:
        for marker in markers:
            if marker in dep_names:
                return framework_name
    
    # Fallback: check if it's a plain HTML/JS/TS project
    if any(k in dep_names for k in ("vite", "webpack", "parcel", "esbuild", "rollup")):
        return "Vanilla/Bundler"
    
    return None

def fetch_package_json(repo):
    """Fetch package.json from GitHub API."""
    url = f"https://raw.githubusercontent.com/{repo}/HEAD/package.json"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return None

def main():
    # Load batch9 ids
    batch9_ids = set()
    with open(BATCH9_FILE) as f:
        for line in f:
            batch9_ids.add(json.loads(line).get("task_id", ""))
    
    # Find all Batch 1-8 cards with unknown framework
    unknown_cards = {}  # repo -> [(filepath, card)]
    for fn in os.listdir(POOL_DIR):
        if not fn.endswith(".json"):
            continue
        fp = os.path.join(POOL_DIR, fn)
        with open(fp) as f:
            card = json.load(f)
        if card["task_id"] in batch9_ids:
            continue
        fw = (card.get("framework", "") or "").strip().lower()
        if not fw or fw in ("unknown", "none"):
            repo = card.get("repo", "")
            if repo not in unknown_cards:
                unknown_cards[repo] = []
            unknown_cards[repo].append((fp, card))
    
    print(f"Found {len(unknown_cards)} repos with {sum(len(v) for v in unknown_cards.values())} unknown cards")
    
    updated = 0
    still_unknown = 0
    errors = 0
    results = {}
    
    for i, (repo, cards) in enumerate(sorted(unknown_cards.items())):
        pkg = fetch_package_json(repo)
        if pkg is None:
            errors += 1
            results[repo] = "fetch_error"
            print(f"  [{i+1}/{len(unknown_cards)}] {repo}: fetch error")
            continue
        
        fw = detect_framework(pkg)
        if fw:
            results[repo] = fw
            for fp, card in cards:
                card["framework"] = fw
                with open(fp, "w") as f:
                    json.dump(card, f, indent=2, ensure_ascii=False)
                    f.write("\n")
                updated += 1
            print(f"  [{i+1}/{len(unknown_cards)}] {repo}: → {fw} ({len(cards)} cards)")
        else:
            still_unknown += 1
            results[repo] = "unknown"
            print(f"  [{i+1}/{len(unknown_cards)}] {repo}: still unknown ({len(cards)} cards)")
        
        # Rate limit: ~30 req/min for unauthenticated
        if (i + 1) % 20 == 0:
            time.sleep(2)
    
    print(f"\n=== Summary ===")
    print(f"Updated: {updated} cards")
    print(f"Still unknown: {still_unknown} repos")
    print(f"Fetch errors: {errors} repos")
    
    # Framework distribution of updated
    from collections import Counter
    fw_dist = Counter(v for v in results.values() if v not in ("unknown", "fetch_error"))
    print(f"\nDetected frameworks:")
    for fw, count in sorted(fw_dist.items(), key=lambda x: -x[1]):
        print(f"  {fw}: {count} repos")

if __name__ == "__main__":
    main()
