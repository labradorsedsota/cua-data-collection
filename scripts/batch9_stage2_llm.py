#!/usr/bin/env python3
"""
Batch 9 Stage 2: LLM description generation via API.
Commits output every 100 cards for safety.
"""
import json, os, sys, glob, time, re
import urllib.request
import urllib.error
from collections import Counter

RAW_INPUT = "data/batch9_raw.jsonl"
OUTPUT = "data/batch9_tasks.jsonl"
POOL_DIR = "tasks/pool"
COMMIT_INTERVAL = 100
PER_REPO_CAP = 8
UI_SCORE_MIN = 5

# API config - read from openclaw config
import pathlib
config_path = pathlib.Path.home() / ".openclaw" / "openclaw.json"
with open(config_path) as f:
    cfg = json.load(f)
provider = cfg["models"]["providers"]["mininglamp"]
API_URL = provider["baseUrl"] + "/v1/messages"
API_KEY = provider["apiKey"]
MODEL = provider["models"][0]["id"]

SYSTEM_PROMPT = """你是一个 GUI 测试任务卡质量评审员。给定一个 GitHub issue/PR 的信息，你需要：

1. 判断这个 bug 是否是 GUI/UI 可观测的（用户在浏览器中能直接看到或交互到的视觉/行为问题）
2. 如果是，生成中文测试描述和预期结果
3. 识别前端框架

严格输出 JSON（不要 markdown code block）：
{"ui_observable":true,"ui_score":8,"framework":"react","test_description_zh":"...","expected_result_zh":"..."}

或拒绝：
{"ui_observable":false,"ui_score":2,"reject_reason":"纯 TypeScript 类型定义修复，无 UI 表现"}

评分标准：
- 10: 明确的视觉bug（元素消失/错位/颜色错误/图标异常）
- 8: 交互bug（点击无响应/拖拽失效/表单状态错误）
- 6: 间接UI影响（数据不显示/状态不更新/路由异常）
- 4: 可能有UI影响但不确定
- 2: 纯后端/API/构建/类型/测试
- 1: 文档/CI/配置

规则：
- test_description_zh: 只描述要验证的操作步骤和观察点，不暴露 bug 本身
- expected_result_zh: 描述功能的正确行为
- framework: react/vue/angular/svelte/nextjs/nuxt/preact/vite/other/unknown
- ui_score < 5 的一律拒绝"""

def call_api(prompt, retries=2):
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 400,
        "messages": [{"role": "user", "content": f"{SYSTEM_PROMPT}\n\n{prompt}"}]
    }).encode()
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
    }
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(API_URL, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                text = data.get("content", [{}])[0].get("text", "")
                text = text.strip()
                if text.startswith("```"):
                    text = re.sub(r"```json?\n?", "", text)
                    text = re.sub(r"```\s*$", "", text)
                try: return json.loads(text)
                except:
                    match = re.search(r'\{[^{}]*("ui_observable"|"ui_score")[^{}]*\}', text, re.DOTALL)
                    if match: return json.loads(match.group())
                    return None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(min(30, 5 * (attempt + 1)))
            elif e.code >= 500:
                time.sleep(3)
            else: return None
        except: 
            if attempt < retries: time.sleep(2)
            else: return None
    return None

# Load pool for dedup
pool_tasks = set()
for fp in glob.glob(f"{POOL_DIR}/*.json"):
    try:
        with open(fp) as fh:
            pool_tasks.add(json.load(fh).get("task_id", ""))
    except: pass

with open(RAW_INPUT) as f:
    raw = [json.loads(line) for line in f]
raw = [c for c in raw if c.get("task_id", "") not in pool_tasks]

print(f"[stage2-llm] {len(raw)} cards to process", flush=True)

# Resume support
existing = set()
if os.path.exists(OUTPUT):
    with open(OUTPUT) as f:
        for line in f:
            try: existing.add(json.loads(line).get("task_id", ""))
            except: pass
    if existing:
        print(f"  Resuming: {len(existing)} already done", flush=True)

valid_count = len(existing)
rejected = 0
errors = 0
processed = 0

outf = open(OUTPUT, "a")

for i, card in enumerate(raw):
    tid = card.get("task_id", "")
    if tid in existing: continue
    processed += 1

    if processed % 20 == 1:
        print(f"[{processed}/{len(raw)}] {tid} (valid: {valid_count}, rej: {rejected}, err: {errors})", flush=True)

    prompt = f"""项目: {card.get('repo', '')}
Issue/PR 标题: {card.get('issue_title', '')}
Issue 内容摘要: {card.get('issue_body_preview', '')[:400]}
修复 PR 改动文件数: {card.get('pr_changed_files', '?')}
test_page: {card.get('test_page', '/')}

请判断并输出 JSON。"""

    result = call_api(prompt)
    if result is None:
        errors += 1
        continue

    if not result.get("ui_observable", False) or result.get("ui_score", 0) < UI_SCORE_MIN:
        rejected += 1
        continue

    desc = result.get("test_description_zh", "")
    if not desc or len(desc) < 10:
        rejected += 1
        continue

    card["test_description_zh"] = desc
    card["expected_result_zh"] = result.get("expected_result_zh", "")
    card["framework"] = result.get("framework", "unknown")
    card["_ui_score"] = result.get("ui_score", 5)
    card["_description_source"] = "llm_api_batch9"

    outf.write(json.dumps(card, ensure_ascii=False) + "\n")
    outf.flush()
    valid_count += 1

    # Auto-commit
    if processed % COMMIT_INTERVAL == 0:
        outf.flush()
        os.system(f'cd {os.getcwd()} && git add {OUTPUT} && git commit -m "batch9-s2: {processed} processed, {valid_count} valid" --quiet')
        print(f"  [committed at {processed}]", flush=True)

    time.sleep(0.5)

outf.close()

# Per-repo cap + final output
all_valid = []
with open(OUTPUT) as f:
    all_valid = [json.loads(line) for line in f]

repo_count = Counter()
capped = []
for c in sorted(all_valid, key=lambda x: -x.get("_ui_score", 0)):
    repo = c.get("repo", "")
    if repo_count[repo] < PER_REPO_CAP:
        capped.append(c)
        repo_count[repo] += 1

with open(OUTPUT + ".final", "w") as f:
    for c in capped:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

os.system(f'cd {os.getcwd()} && git add {OUTPUT} {OUTPUT}.final && git commit -m "batch9-s2 COMPLETE: {len(all_valid)} valid, {len(capped)} after cap, {rejected} rejected, {errors} errors" --quiet')

fw_dist = Counter(c.get("framework","") for c in capped)
print(f"\n[Stage 2 LLM COMPLETE]", flush=True)
print(f"  Processed: {processed}")
print(f"  Valid: {len(all_valid)}")
print(f"  After cap (8/repo): {len(capped)}")
print(f"  Rejected: {rejected}")
print(f"  Errors: {errors}")
print(f"  Pass rate: {len(all_valid)*100/max(processed,1):.1f}%")
print(f"  Framework: {dict(fw_dist.most_common())}")
