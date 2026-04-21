#!/usr/bin/env python3
"""
push_to_pool.py — 将 Stage 2 最终产出推入 tasks/pool/
含自动质量报告 + 摘要 commit message（项目级改造 ⑦）

用法:
    python scripts/push_to_pool.py --batch 9 --input data/batch9_tasks.jsonl.final
    python scripts/push_to_pool.py --batch 10 --input data/batch10_tasks.jsonl.final --dry-run
"""
import json, os, sys, argparse, glob, shutil
from pipeline_utils import generate_quality_report, git_commit

def main():
    parser = argparse.ArgumentParser(description="Push task cards to pool with quality report")
    parser.add_argument("--batch", required=True, type=int, help="Batch number")
    parser.add_argument("--input", required=True, help="Final task cards JSONL file")
    parser.add_argument("--pool", default="tasks/pool", help="Pool directory")
    parser.add_argument("--dry-run", action="store_true", help="Report only, don't copy or commit")
    args = parser.parse_args()

    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(cwd)

    input_path = args.input
    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)

    # 加载新卡
    with open(input_path) as f:
        new_cards = [json.loads(line) for line in f if line.strip()]

    print(f"[push] Batch {args.batch}: {len(new_cards)} cards from {input_path}")

    # ⑦ 生成质量报告
    qr = generate_quality_report(args.batch, new_cards, args.pool, cwd=cwd)
    unique_cards = qr["unique_cards"]

    print(f"\n{'='*60}")
    print(f"Quality Report Summary:")
    print(f"  Input:         {len(new_cards)}")
    print(f"  Duplicates:    {qr['report']['duplicates']}")
    print(f"  Unique new:    {len(unique_cards)}")
    print(f"  Schema errors: {qr['report']['schema_errors']}")
    print(f"  Backend risk:  {qr['report']['backend_risk_pct']}%")
    print(f"  Repos:         {qr['report']['repos_covered']}")
    print(f"  Frameworks:    {qr['report']['framework_distribution']}")
    print(f"{'='*60}\n")

    if args.dry_run:
        print("[dry-run] No files copied, no commits made.")
        return

    # 复制到 pool
    copied = 0
    for card in unique_cards:
        tid = card.get("task_id", "")
        if not tid:
            continue
        dest = os.path.join(args.pool, f"{tid}.json")
        if os.path.exists(dest):
            continue
        with open(dest, "w") as f:
            json.dump(card, f, indent=2, ensure_ascii=False)
        copied += 1

    print(f"[push] Copied {copied} cards to {args.pool}/")

    # Commit: 质量报告 + pool 新卡，摘要写入 commit message
    files_to_add = [args.pool, qr["report_path"]]
    git_commit(qr["summary"], files=files_to_add, cwd=cwd)

    # Push to remote
    import subprocess
    result = subprocess.run(["git", "push"], cwd=cwd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[push] ✅ Pushed to remote")
    else:
        print(f"[push] ❌ Push failed: {result.stderr[:200]}")

    print(f"\n[DONE] {qr['summary']}")


if __name__ == "__main__":
    main()
