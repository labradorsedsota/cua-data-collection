#!/usr/bin/env python3
"""
Batch 9 排产优先级脚本
基于 Batch 1-8 历史数据分析 + SOP 硬性排除规则 + repo 特征扫描

用法：
  cd /path/to/bughunt
  python3 scripts/batch9-prioritize.py [--scan-file /tmp/batch9_repo_scan.json] [--dry-run]

输出：
  pm-template/batch9-priority-output.json
"""

import json
import os
import sys
import argparse
from collections import defaultdict

# === 配置 ===

# 硬性排除: deploy_status
EXCLUDED_DEPLOY_STATUS = {"no_script_dead", "no_script_low_roi"}

# 硬性排除: repo 大小上限 (KB)
MAX_REPO_SIZE_KB = 500_000  # 500MB

# 硬性排除: node_version 冲突模式
NODE_VERSION_CONFLICT_PATTERNS = ["<18", "<16", "<14", "8.10", "10.x", "12.x", "14.x"]

# 高风险框架 (Batch 1-8 fail rate >= 70%)
HIGH_RISK_FRAMEWORKS = {"next", "nextjs", "next.js", "gatsby", "lit"}

# 高风险 native 依赖 (Node 18+ 编译大概率失败)
HIGH_RISK_NATIVES = {"node-sass", "node-gyp"}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_high_risk_framework(framework: str) -> bool:
    fw = framework.lower().strip()
    for pattern in HIGH_RISK_FRAMEWORKS:
        if pattern in fw:
            return True
    return False


def has_node_version_conflict(node_engines: str) -> bool:
    if not node_engines or node_engines == "None":
        return False
    for pattern in NODE_VERSION_CONFLICT_PATTERNS:
        if pattern in node_engines:
            return True
    return False


def has_risky_native(native_modules: str) -> bool:
    if not native_modules:
        return False
    natives_lower = str(native_modules).lower()
    return any(mod in natives_lower for mod in HIGH_RISK_NATIVES)


def classify_task(card: dict, repo_info: dict) -> tuple:
    """
    对一张卡进行分类。
    返回 (tier, exclude_reason)
    - 如果被排除: tier=None, exclude_reason=str
    - 如果可排产: tier=str, exclude_reason=None
    """
    deploy_status = card.get("deploy_status", "")
    backend_risk = card.get("backend_risk", False)
    repo_size_kb = card.get("repo_size_kb", 0)
    framework = card.get("framework", "unknown")
    size_mb = repo_size_kb / 1024

    archived = repo_info.get("archived", False)
    node_engines = str(repo_info.get("node_engines", ""))
    native_modules = str(repo_info.get("native_modules", ""))

    # === 第一层：硬性排除 ===

    if deploy_status in EXCLUDED_DEPLOY_STATUS:
        return None, f"deploy_status={deploy_status}"

    if backend_risk is True:
        return None, "backend_risk"

    if repo_size_kb > MAX_REPO_SIZE_KB:
        return None, f"repo>{repo_size_kb // 1024}MB"

    if archived:
        return None, "archived"

    if has_node_version_conflict(node_engines):
        return None, f"node_version_conflict({node_engines})"

    # === 第二层：优先级分层 ===

    risky_fw = is_high_risk_framework(framework)
    risky_native = has_risky_native(native_modules)

    if risky_fw:
        if size_mb >= 100:
            return "P5", None
        else:
            return "P4", None

    if risky_native:
        return "P4", None

    if size_mb < 20:
        return "P1", None
    elif size_mb < 100:
        return "P2", None
    elif size_mb < 500:
        return "P3", None
    else:
        # 理论上不会到这里（>500MB 已在硬排除）
        return "P3", None


def main():
    parser = argparse.ArgumentParser(description="Batch 9 排产优先级分类")
    parser.add_argument(
        "--scan-file",
        default="/tmp/batch9_repo_scan.json",
        help="repo 特征扫描文件路径 (默认: /tmp/batch9_repo_scan.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只输出统计，不写文件",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="bughunt repo 根目录 (默认: 当前目录)",
    )
    args = parser.parse_args()

    repo_root = args.repo_root
    pool_dir = os.path.join(repo_root, "tasks", "pool")
    dispatch_log_path = os.path.join(repo_root, "pm-template", "dispatch-log.json")
    output_path = os.path.join(repo_root, "pm-template", "batch9-priority-output.json")

    # 1. 加载 dispatch-log
    print("Loading dispatch-log...")
    dispatch_log = load_json(dispatch_log_path)
    unassigned = {
        tid
        for tid, info in dispatch_log["tasks"].items()
        if info.get("status") == "unassigned"
    }
    print(f"  Unassigned tasks: {len(unassigned)}")

    # 2. 加载 repo 扫描数据
    print(f"Loading repo scan: {args.scan_file}")
    if os.path.exists(args.scan_file):
        scan_data = load_json(args.scan_file)
        print(f"  Repos in scan: {len(scan_data)}")
    else:
        print(f"  WARNING: scan file not found, proceeding without repo-level signals")
        scan_data = {}

    # 3. 分类每张卡
    print("Classifying tasks...")
    excluded = defaultdict(list)  # reason -> [task_ids]
    tiers = defaultdict(list)  # tier -> [task_ids]
    tier_repos = defaultdict(set)  # tier -> {repos}

    for tid in sorted(unassigned):
        pool_file = os.path.join(pool_dir, f"{tid}.json")
        if not os.path.exists(pool_file):
            excluded["pool_card_missing"].append(tid)
            continue

        card = load_json(pool_file)
        repo = card.get("repo", "")
        repo_info = scan_data.get(repo, {})

        tier, reason = classify_task(card, repo_info)

        if tier is None:
            excluded[reason].append(tid)
        else:
            tiers[tier].append(tid)
            tier_repos[tier].add(repo)

    # 4. 输出统计
    print("\n" + "=" * 60)
    print("硬性排除")
    print("=" * 60)
    total_excluded = 0
    for reason in sorted(excluded.keys()):
        count = len(excluded[reason])
        total_excluded += count
        print(f"  {reason}: {count} 张")
    print(f"  合计: {total_excluded} 张")

    print("\n" + "=" * 60)
    print("排产优先级")
    print("=" * 60)
    total_eligible = 0
    for tier in sorted(tiers.keys()):
        count = len(tiers[tier])
        repos_count = len(tier_repos[tier])
        total_eligible += count
        print(f"  {tier}: {count} 张 / {repos_count} 个 repo")
    print(f"  合计: {total_eligible} 张")
    print(f"\n  总计: {total_excluded + total_eligible} / {len(unassigned)} unassigned")

    # 5. 构建输出
    output = {
        "generated_at": "2026-04-23",
        "source": {
            "dispatch_log": dispatch_log_path,
            "pool_dir": pool_dir,
            "scan_file": args.scan_file,
        },
        "summary": {
            "total_unassigned": len(unassigned),
            "total_excluded": total_excluded,
            "total_eligible": total_eligible,
        },
        "excluded": {reason: tids for reason, tids in sorted(excluded.items())},
        "priority_tiers": {},
    }

    for tier in sorted(tiers.keys()):
        output["priority_tiers"][tier] = {
            "task_ids": sorted(tiers[tier]),
            "count": len(tiers[tier]),
            "repo_count": len(tier_repos[tier]),
        }

    # 6. 写入文件
    if not args.dry_run:
        print(f"\nWriting output to {output_path}...")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print("Done.")
    else:
        print("\n[dry-run] Skipping file write.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
