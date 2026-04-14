#!/usr/bin/env python3
"""
BugHunt Bug-Level Screener
For a given repo, fetches closed bug issues + linked merged PRs,
filters for UI-observable bugs, and outputs task card candidates.

Usage: python3 bug_screener.py <owner/repo> [--limit 10] [--output cards.jsonl]
"""

import subprocess
import json
import sys
import re
import time
import os

def gh_api(endpoint, jq_filter=None):
    """Call gh api and return parsed JSON."""
    cmd = ["gh", "api", endpoint]
    if jq_filter:
        cmd += ["--jq", jq_filter]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return None
        if jq_filter:
            return result.stdout.strip()
        return json.loads(result.stdout) if result.stdout.strip() else None
    except Exception:
        return None

def get_closed_bug_issues(repo, per_page=100):
    """Get closed issues labeled 'bug'."""
    issues = []
    page = 1
    while True:
        data = gh_api(f"repos/{repo}/issues?labels=bug&state=closed&per_page={per_page}&page={page}")
        if not data:
            break
        issues.extend(data)
        if len(data) < per_page:
            break
        page += 1
        time.sleep(0.5)
    return issues

def get_merged_prs_with_fixes(repo, per_page=100):
    """Get merged PRs, looking for ones that reference issues."""
    prs = []
    page = 1
    while page <= 5:  # Limit to 500 PRs
        data = gh_api(f"repos/{repo}/pulls?state=closed&per_page={per_page}&page={page}&sort=updated&direction=desc")
        if not data:
            break
        for pr in data:
            if pr.get("merged_at"):
                prs.append(pr)
        if len(data) < per_page:
            break
        page += 1
        time.sleep(0.5)
    return prs

def extract_issue_refs(text):
    """Extract issue numbers from PR body/title (closes #123, fixes #456, etc.)."""
    if not text:
        return []
    patterns = [
        r'(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)',
        r'#(\d+)',
    ]
    refs = set()
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            refs.add(int(match.group(1)))
    return list(refs)

def is_ui_observable(issue):
    """Heuristic: is this bug likely UI-observable?"""
    title = (issue.get("title") or "").lower()
    body = (issue.get("body") or "").lower()
    text = title + " " + body
    
    # Positive signals (UI-related)
    ui_keywords = [
        "display", "style", "css", "layout", "render", "visual",
        "button", "click", "hover", "modal", "dialog", "popup",
        "color", "font", "alignment", "position", "overflow",
        "responsive", "scroll", "animation", "transition",
        "missing", "disappear", "broken", "incorrect", "wrong",
        "not showing", "not visible", "not displayed", "not working",
        "ui", "ux", "screenshot", "image", "icon",
        "menu", "dropdown", "select", "input", "form",
        "page", "view", "component", "element",
        "显示", "样式", "按钮", "点击", "弹窗", "颜色", "布局",
    ]
    
    # Negative signals (not UI-observable)
    non_ui_keywords = [
        "docker", "dockerfile", "ci/cd", "pipeline", "deploy",
        "api", "endpoint", "backend", "server", "database",
        "performance", "memory leak", "cpu", "benchmark",
        "typescript error", "type error", "compile",
        "node version", "npm version", "dependency",
        "test failure", "unit test", "e2e test",
        "documentation", "readme", "typo in doc",
        "security", "vulnerability", "cve",
        "migration", "upgrade", "breaking change",
    ]
    
    ui_score = sum(1 for kw in ui_keywords if kw in text)
    non_ui_score = sum(1 for kw in non_ui_keywords if kw in text)
    
    # Has screenshot = strong positive signal
    has_screenshot = any(ext in body for ext in [".png", ".jpg", ".gif", ".jpeg", "screenshot", "image"])
    if has_screenshot:
        ui_score += 3
    
    return ui_score > non_ui_score

def generate_task_card(repo, issue, pr):
    """Generate a task card JSON from issue + PR."""
    issue_num = issue["number"]
    pr_num = pr["number"]
    
    base_sha = pr.get("base", {}).get("sha", "")[:10]
    merge_sha = pr.get("merge_commit_sha", "")[:10]
    
    task_id = f"{repo.split('/')[-1]}-{issue_num}"
    
    card = {
        "task_id": task_id,
        "repo": repo,
        "repo_url": f"https://github.com/{repo}",
        "issue_url": f"https://github.com/{repo}/issues/{issue_num}",
        "issue_title": issue.get("title", ""),
        "issue_body_preview": (issue.get("body") or "")[:300],
        "fix_pr": pr_num,
        "buggy_commit": base_sha,
        "fix_commit": merge_sha,
        "pr_changed_files": pr.get("changed_files", 0),
        "framework": "",  # To be filled
        "package_manager": "npm",
        "deploy_commands": [
            f"git clone https://github.com/{repo}.git {task_id}",
            f"cd {task_id}",
            f"git checkout {base_sha}",
            "npm install",
            "npm run dev"
        ],
        "deploy_verify": "",  # To be filled per project
        "dev_url": "http://localhost:5173",
        "test_page": "/",
        "app_name": "",  # To be filled
        "test_description_zh": "",  # To be filled by reviewer
        "expected_result_zh": "",  # To be filled by reviewer
        "timeout": 600,
        "ground_truth": {
            "bug_type": "",
            "expected_behavior": "",
            "actual_behavior": ""
        },
        "_screening": {
            "ui_observable": True,
            "has_screenshot": any(ext in (issue.get("body") or "").lower() for ext in [".png", ".jpg", ".gif"]),
            "issue_labels": [l.get("name", "") for l in issue.get("labels", [])],
        }
    }
    
    return card

def screen_repo(repo, max_cards=10):
    """Main screening function for a repo."""
    print(f"Screening {repo}...", file=sys.stderr)
    
    # Step 1: Get closed bug issues
    print(f"  Fetching closed bug issues...", file=sys.stderr)
    issues = get_closed_bug_issues(repo)
    print(f"  Found {len(issues)} closed bug issues", file=sys.stderr)
    
    # Step 2: Get merged PRs
    print(f"  Fetching merged PRs...", file=sys.stderr)
    prs = get_merged_prs_with_fixes(repo)
    print(f"  Found {len(prs)} merged PRs", file=sys.stderr)
    
    # Step 3: Build issue->PR mapping
    issue_to_prs = {}
    for pr in prs:
        refs = extract_issue_refs((pr.get("title") or "") + " " + (pr.get("body") or ""))
        for ref in refs:
            if ref not in issue_to_prs:
                issue_to_prs[ref] = []
            issue_to_prs[ref].append(pr)
    
    # Step 4: Filter and score
    candidates = []
    issue_map = {i["number"]: i for i in issues}
    
    for issue_num, linked_prs in issue_to_prs.items():
        if issue_num not in issue_map:
            continue
        issue = issue_map[issue_num]
        
        # Filter: UI observable
        if not is_ui_observable(issue):
            continue
        
        # Pick best PR (smallest changed_files)
        best_pr = None
        for pr in linked_prs:
            # Need to fetch changed_files count
            pr_detail = gh_api(f"repos/{repo}/pulls/{pr['number']}")
            if pr_detail and pr_detail.get("changed_files", 100) <= 10:
                if best_pr is None or pr_detail["changed_files"] < best_pr.get("changed_files", 100):
                    best_pr = pr_detail
            time.sleep(0.3)
        
        if best_pr is None:
            continue
        
        card = generate_task_card(repo, issue, best_pr)
        candidates.append(card)
        
        if len(candidates) >= max_cards:
            break
    
    # Also check PRs with fix/bug in title that might not have explicit issue refs
    if len(candidates) < max_cards:
        fix_prs = [pr for pr in prs if re.search(r'fix|bug', pr.get("title", ""), re.IGNORECASE)]
        for pr in fix_prs:
            if any(c["fix_pr"] == pr["number"] for c in candidates):
                continue
            
            pr_detail = gh_api(f"repos/{repo}/pulls/{pr['number']}")
            if not pr_detail or pr_detail.get("changed_files", 100) > 10:
                time.sleep(0.3)
                continue
            
            # Create a pseudo-issue from PR title/body
            pseudo_issue = {
                "number": pr["number"],
                "title": pr.get("title", ""),
                "body": pr.get("body", ""),
                "labels": [],
            }
            
            if is_ui_observable(pseudo_issue):
                card = generate_task_card(repo, pseudo_issue, pr_detail)
                card["task_id"] = f"{repo.split('/')[-1]}-pr{pr['number']}"
                card["issue_url"] = f"https://github.com/{repo}/pull/{pr['number']}"
                candidates.append(card)
            
            time.sleep(0.3)
            if len(candidates) >= max_cards:
                break
    
    print(f"  Found {len(candidates)} UI-observable bug candidates", file=sys.stderr)
    return candidates

def main():
    import argparse
    parser = argparse.ArgumentParser(description="BugHunt Bug-Level Screener")
    parser.add_argument("repo", help="GitHub repo (owner/name)")
    parser.add_argument("--limit", type=int, default=10, help="Max candidates per repo")
    parser.add_argument("--output", default=None, help="Output file (jsonl)")
    args = parser.parse_args()
    
    candidates = screen_repo(args.repo, max_cards=args.limit)
    
    if args.output:
        with open(args.output, "w") as f:
            for card in candidates:
                f.write(json.dumps(card, ensure_ascii=False) + "\n")
        print(f"Wrote {len(candidates)} candidates to {args.output}", file=sys.stderr)
    else:
        for card in candidates:
            print(json.dumps(card, ensure_ascii=False))

if __name__ == "__main__":
    main()
