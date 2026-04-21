#!/usr/bin/env python3
"""
Phase 2: Fix remaining unknown frameworks using repo name heuristics + GitHub topics API.
"""
import json, os, urllib.request, urllib.error, time

POOL_DIR = "tasks/pool"
BATCH9_FILE = "data/batch9_tasks.jsonl.final"

# Manual mapping for well-known repos
MANUAL_MAP = {
    "CopilotKit/CopilotKit": "React",
    "DevCloudFE/vue-devui": "Vue",
    "TaTo30/vue-pdf": "Vue",
    "Tresjs/tres": "Vue",
    "necolas/react-native-web": "React",
    "wojtekmaj/react-calendar": "React",
    "wojtekmaj/react-date-picker": "React",
    "wojtekmaj/react-pdf": "React",
    "nuxt/website-v2": "Nuxt",
    "vuetifyjs/nuxt-module": "Nuxt",
    "KUN1007/kun-galgame-nuxt4": "Nuxt",
    "juice-shop/juice-shop": "Angular",
    "analogdotnow/Analog": "Angular",
    "typehero/typehero": "Next.js",
    "krishnaacharyaa/wanderlust": "React",
    "avitorio/outstatic": "Next.js",
    "kirill-konshin/next-redux-wrapper": "Next.js",
    "blinkospace/blinko": "Next.js",
    "sorry-cypress/sorry-cypress": "React",
    "kanbn/kan": "React",
    "jordan-dalby/ByteStash": "React",
    "onlook-dev/onlook": "React",
    "karakeep-app/karakeep": "Next.js",
    "simstudioai/sim": "Next.js",
    "devhubapp/devhub": "React",
    "fantasticit/think": "React",
    "doocs/md": "Vue",
    "padloc/padloc": "Lit",
    "puemos/hls-downloader": "React",
    "hngngn/shadcn-solid": "Solid",
    "imskyleen/animate-ui": "React",
    "nicoespeon/trello-kanban-analysis-tool": "React",
    "plankanban/planka": "React",
    "iam4x/bobarr": "React",
    "usemarble/marble": "React",
    "usesend/useSend": "React",
    "meursyphus/flitter": "Vanilla/Bundler",
    "lukasbach/monaco-editor-auto-typings": "React",
    "jxnblk/mdx-deck": "React",
    "frappe/builder": "Vue",
    "frappe/helpdesk": "Vue",
    "frappe/insights": "Vue",
    "frappe/lms": "Vue",
    "silexlabs/Silex": "Vanilla/Bundler",
    "saltcorn/saltcorn": "Vanilla/Bundler",
    "overlayeddev/overlayed": "React",
    "OfficeDev/script-lab": "React",
    "crowi/crowi": "React",
    "cupcakearmy/cryptgeon": "Svelte",
}

# Name-based heuristics
NAME_HINTS = [
    ("react", "React"),
    ("vue", "Vue"),
    ("angular", "Angular"),
    ("svelte", "Svelte"),
    ("nuxt", "Nuxt"),
    ("next", "Next.js"),
    ("solid", "Solid"),
    ("lit-", "Lit"),
    ("ember", "Ember"),
]

def detect_from_name(repo):
    """Detect framework from repo name."""
    name = repo.lower().split("/")[-1]
    for hint, fw in NAME_HINTS:
        if hint in name:
            return fw
    return None

def fetch_topics(repo):
    """Fetch repo topics from GitHub API."""
    url = f"https://api.github.com/repos/{repo}/topics"
    try:
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Mozilla/5.0"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("names", [])
    except:
        return []

def detect_from_topics(topics):
    """Detect framework from GitHub topics."""
    topics_lower = [t.lower() for t in topics]
    for topic, fw in [("nextjs", "Next.js"), ("nuxtjs", "Nuxt"), ("nuxt", "Nuxt"),
                       ("gatsby", "Gatsby"), ("remix", "Remix"), ("sveltekit", "SvelteKit"),
                       ("reactjs", "React"), ("react", "React"),
                       ("vuejs", "Vue"), ("vue", "Vue"),
                       ("angular", "Angular"),
                       ("svelte", "Svelte"), ("solidjs", "Solid"), ("lit", "Lit")]:
        if topic in topics_lower:
            return fw
    return None

def main():
    batch9_ids = set()
    with open(BATCH9_FILE) as f:
        for line in f:
            batch9_ids.add(json.loads(line).get("task_id", ""))
    
    unknown_cards = {}
    for fn in os.listdir(POOL_DIR):
        if not fn.endswith(".json"):
            continue
        fp = os.path.join(POOL_DIR, fn)
        with open(fp) as f:
            card = json.load(f)
        if card["task_id"] in batch9_ids:
            continue
        fw = (card.get("framework", "") or "").strip().lower()
        if not fw or fw in ("unknown", "none", "vanilla/bundler"):
            repo = card.get("repo", "")
            if repo not in unknown_cards:
                unknown_cards[repo] = []
            unknown_cards[repo].append((fp, card))
    
    print(f"Phase 2: {len(unknown_cards)} repos, {sum(len(v) for v in unknown_cards.values())} cards still unknown")
    
    updated = 0
    still_unknown = []
    
    for i, (repo, cards) in enumerate(sorted(unknown_cards.items())):
        fw = None
        source = ""
        
        # 1. Manual map
        if repo in MANUAL_MAP:
            fw = MANUAL_MAP[repo]
            source = "manual"
        
        # 2. Name heuristic
        if not fw:
            fw = detect_from_name(repo)
            if fw:
                source = "name"
        
        # 3. GitHub topics (only for remaining)
        if not fw:
            topics = fetch_topics(repo)
            if topics:
                fw = detect_from_topics(topics)
                if fw:
                    source = f"topics({','.join(topics[:3])})"
            time.sleep(0.5)
        
        if fw:
            for fp, card in cards:
                card["framework"] = fw
                with open(fp, "w") as f:
                    json.dump(card, f, indent=2, ensure_ascii=False)
                    f.write("\n")
                updated += 1
            print(f"  [{i+1}/{len(unknown_cards)}] {repo}: → {fw} [{source}] ({len(cards)} cards)")
        else:
            still_unknown.append((repo, len(cards)))
            print(f"  [{i+1}/{len(unknown_cards)}] {repo}: still unknown ({len(cards)} cards)")
    
    print(f"\n=== Phase 2 Summary ===")
    print(f"Updated: {updated} cards")
    print(f"Still unknown: {len(still_unknown)} repos, {sum(c for _, c in still_unknown)} cards")
    if still_unknown:
        print(f"\nRemaining unknown repos:")
        for repo, cnt in still_unknown:
            print(f"  {repo} ({cnt} cards)")

if __name__ == "__main__":
    main()
