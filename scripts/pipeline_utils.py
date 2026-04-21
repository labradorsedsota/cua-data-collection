#!/usr/bin/env python3
"""
pipeline_utils.py — BugHunt 产卡管线共用工具
2026-04-21 事故复盘后新增，覆盖项目级改造 ⑤⑥⑦

⑤ auto_commit(): 每阶段产出自动 git add + commit
⑥ write_manifest(): batch 参数持久化
⑦ generate_quality_report(): 质量报告 + 摘要写入 commit message
"""
import json, os, glob, subprocess, time
from collections import Counter
from datetime import datetime


def git_commit(message, files=None, cwd=None):
    """安全 commit：先 add 指定文件，再 commit。"""
    cwd = cwd or os.getcwd()
    if files:
        for f in (files if isinstance(files, list) else [files]):
            subprocess.run(["git", "add", f], cwd=cwd, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", message, "--quiet", "--allow-empty"],
        cwd=cwd, capture_output=True, text=True
    )
    return result.returncode == 0


def auto_commit(stage, batch_id, stats, output_file, cwd=None):
    """⑤ 阶段内定期 commit，commit message 含进度摘要。"""
    msg = f"wip: batch{batch_id} {stage} | {stats}"
    return git_commit(msg, files=output_file, cwd=cwd)


def write_manifest(batch_id, params, cwd=None):
    """⑥ batch 启动时将参数写入 manifest 并 commit。"""
    cwd = cwd or os.getcwd()
    manifest_path = os.path.join(cwd, "data", "batch_manifest.json")

    # 读取现有 manifest
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            try:
                manifest = json.load(f)
            except json.JSONDecodeError:
                manifest = {}

    # 写入本批次参数
    manifest[f"batch{batch_id}"] = {
        "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **params
    }

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    git_commit(
        f"batch{batch_id}: manifest recorded | {json.dumps(params, ensure_ascii=False)[:120]}",
        files=manifest_path, cwd=cwd
    )
    print(f"[manifest] batch{batch_id} params saved to {manifest_path}", flush=True)


def generate_quality_report(batch_id, new_cards, pool_dir, cwd=None):
    """
    ⑦ push 前生成质量报告，返回摘要字符串（写入 commit message）。
    不阻断流程，仅统计。

    Args:
        batch_id: 批次号
        new_cards: list of dict，待入库的卡
        pool_dir: 现有 pool 目录路径
    Returns:
        dict with summary string and report details
    """
    cwd = cwd or os.getcwd()
    pool_dir = os.path.join(cwd, pool_dir) if not os.path.isabs(pool_dir) else pool_dir

    # 加载现有 pool task_ids
    existing_ids = set()
    for fp in glob.glob(os.path.join(pool_dir, "*.json")):
        try:
            with open(fp) as fh:
                existing_ids.add(json.load(fh).get("task_id", ""))
        except:
            pass

    # 统计
    new_ids = {c.get("task_id", "") for c in new_cards}
    dup_ids = new_ids & existing_ids
    unique_cards = [c for c in new_cards if c.get("task_id", "") not in existing_ids]
    skipped = len(new_cards) - len(unique_cards)

    # 框架分布
    fw_dist = Counter(c.get("framework", "unknown") for c in unique_cards)

    # backend_risk 统计
    backend_risk_count = sum(
        1 for c in unique_cards
        if c.get("backend_risk") or c.get("_backend_risk")
    )
    backend_risk_pct = (backend_risk_count / max(len(unique_cards), 1)) * 100

    # Schema 校验（字段完整性）
    required_fields = ["task_id", "repo", "buggy_commit", "deploy_commands",
                       "test_description_zh"]
    schema_errors = []
    for c in unique_cards:
        missing = [f for f in required_fields if not c.get(f)]
        if missing:
            schema_errors.append({"task_id": c.get("task_id", "?"), "missing": missing})

    # 生成报告
    report = {
        "batch_id": batch_id,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_input": len(new_cards),
        "duplicates": len(dup_ids),
        "unique_new": len(unique_cards),
        "schema_errors": len(schema_errors),
        "schema_error_details": schema_errors[:20],  # 最多记录 20 条
        "backend_risk_count": backend_risk_count,
        "backend_risk_pct": round(backend_risk_pct, 1),
        "framework_distribution": dict(fw_dist.most_common()),
        "repos_covered": len(set(c.get("repo", "") for c in unique_cards)),
    }

    # 写报告文件
    report_path = os.path.join(cwd, "data", f"batch{batch_id}_quality_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # 生成 commit message 摘要
    summary = (
        f"batch{batch_id}: +{len(unique_cards)} new, "
        f"~{len(dup_ids)} dup, "
        f"={len(unique_cards) + len(existing_ids)} total | "
        f"schema {'OK' if not schema_errors else f'{len(schema_errors)} err'} | "
        f"backend_risk {backend_risk_pct:.0f}%"
    )

    print(f"[quality] {summary}", flush=True)
    if schema_errors:
        print(f"[quality] ⚠️ {len(schema_errors)} cards with missing fields (see report)", flush=True)

    return {
        "summary": summary,
        "report": report,
        "report_path": report_path,
        "unique_cards": unique_cards,
    }
