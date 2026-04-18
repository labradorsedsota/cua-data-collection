#!/usr/bin/env python3
"""Fix 20 non-compliant result JSONs for worker-fabrice."""
import json
import os

RESULTS_DIR = "/Users/mlt/.openclaw/workspace/bughunt/results/worker-fabrice"

def load(fname):
    with open(os.path.join(RESULTS_DIR, fname)) as f:
        return json.load(f)

def save(fname, data):
    with open(os.path.join(RESULTS_DIR, fname), 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ {fname}")

# ============================================================
# A类: mano_cua 补字段 (3张)
# ============================================================
print("=== A类: mano_cua 补字段 ===")

a_fixes = {
    "Notpad-195.json": {
        "status": "COMPLETED",
        "last_action": "DONE",
        "last_reasoning": "The test is now complete. Here is a comprehensive summary of the findings:"
    },
    "PeaNUT-35.json": {
        "status": "COMPLETED",
        "last_action": "DONE",
        "last_reasoning": "**完美！最终确认结果非常清晰！**"
    },
    "Piped-3715.json": {
        "status": "COMPLETED",
        "last_action": "DONE",
        "last_reasoning": "The DevTools is now closed and I can clearly see the video page in its final state:"
    },
}

for fname, fields in a_fixes.items():
    d = load(fname)
    for k, v in fields.items():
        d["mano_cua"][k] = v
    save(fname, d)

# ============================================================
# B类-1: accounts-ui-173 sess_id 修正 (1张)
# ============================================================
print("\n=== B类-1: accounts-ui-173 sess_id 修正 ===")

d = load("accounts-ui-173.json")
d["sess_id"] = "sess-20260418000814-4fddf69768d24fcc9176ea4ffbf0451f"
save("accounts-ui-173.json", d)

# ============================================================
# B类-2: accounts-ui-191/203/204 重建为 failed (3张)
# ============================================================
print("\n=== B类-2: accounts-ui 批量跳过 → failed ===")

for task_id in ["accounts-ui-191", "accounts-ui-203", "accounts-ui-204"]:
    fname = f"{task_id}.json"
    d = load(fname)
    d["status"] = "failed"
    d["sess_id"] = None
    d["expected_result_used"] = False
    d["duration_seconds"] = 0
    d["mano_cua"] = None
    d["failure"] = {
        "type": "other",
        "symptom": "认证墙，同仓库 accounts-ui-173 已确认需 Zesty.io 后端登录（auth.api.dev.zesty.io），本地部署只有登录页面",
        "attempted": [
            "accounts-ui-173 跑了 71 步 mano-cua 确认需 Zesty.io OAuth 后端认证，无法绕过"
        ],
        "recommendation": "同仓库同部署流程，批量跳过"
    }
    # remove old keys if any
    d.pop("failure_reason", None)
    d.pop("failure_detail", None)
    save(fname, d)

# ============================================================
# C类: failed 结构重组 (13张)
# ============================================================
print("\n=== C类: failed 结构重组 ===")

# commercejs x9
commercejs_ids = [40, 59, 85, 88, 93, 130, 156, 175, 221]
for num in commercejs_ids:
    fname = f"commercejs-nextjs-demo-store-{num}.json"
    d = load(fname)
    old_detail = d.get("failure_detail", "")
    d["status"] = "failed"
    d["sess_id"] = None
    d["expected_result_used"] = False
    d["duration_seconds"] = 0
    d["mano_cua"] = None
    d["failure"] = {
        "type": "deploy_failed",
        "symptom": "node-sass 原生编译失败：node-gyp 3.8.0 + node-sass 在 macOS ARM64 (Darwin 23.4.0) 上无法编译 libsass",
        "attempted": [
            "Node 24 npm install — node-gyp rebuild 失败",
            "Node 18 npm install — 同样 node-gyp rebuild 失败",
            "设置 Python 环境变量 — 仍报错"
        ],
        "recommendation": "跳过，node-sass 需要降级到极老版本 Node 或换 dart-sass"
    }
    d.pop("failure_reason", None)
    d.pop("failure_detail", None)
    save(fname, d)

# nuxt-studio x2
for num in [81, 149]:
    fname = f"nuxt-studio-{num}.json"
    d = load(fname)
    old_detail = d.get("failure_detail", "")
    symptom = "EMFILE: too many open files — nuxt-studio monorepo pnpm 嵌套过深，chokidar watch 触发文件描述符耗尽" if num == 149 else "同 nuxt-studio-149：EMFILE + OOM 导致 nuxt-studio 服务无法启动"
    d["status"] = "failed"
    d["sess_id"] = None
    d["expected_result_used"] = False
    d["duration_seconds"] = 0
    d["mano_cua"] = None
    d["failure"] = {
        "type": "deploy_failed",
        "symptom": symptom,
        "attempted": [
            "Node 18 — 缺 oxc-parser native binding",
            "Node 24 — OOM（2GB 堆内存不够）",
            "Node 24 + 4GB heap — 仍 EMFILE crash",
            "ulimit -n 1048575 — 仍不够"
        ],
        "recommendation": "跳过，monorepo 结构导致文件描述符耗尽，非本地可解决"
    }
    d.pop("failure_reason", None)
    d.pop("failure_detail", None)
    save(fname, d)

# photon x2
for num in [342, 478]:
    fname = f"photon-{num}.json"
    d = load(fname)
    d["status"] = "failed"
    d["sess_id"] = None
    d["expected_result_used"] = False
    d["duration_seconds"] = 0
    d["mano_cua"] = None
    d["failure"] = {
        "type": "deploy_failed",
        "symptom": "依赖 mono-svelte@^1.5.14 在 npm 上不存在（No versions available），疑似已 unpublish",
        "attempted": [
            "npm install — ENOVERSIONS mono-svelte",
            "pnpm install — 同样找不到包"
        ],
        "recommendation": "跳过，第三方依赖已从 npm 删除，无法安装"
    }
    d.pop("failure_reason", None)
    d.pop("failure_detail", None)
    save(fname, d)

print("\n=== 修复完成，共 20 张 ===")
