# BugHunt Cron 任务清单

> 最后更新：2026-04-22 18:16 (Pichai)
> 
> 所有 cron 任务运行在 Pichai 所在机器（机器 A），通过 OpenClaw cron 管理。
> 
> **脚本统一存放：** `~/.openclaw/workspace/scripts/bughunt/`

---

## 当前状态总览

| 任务 | 状态 | 频率 |
|------|------|------|
| bughunt-trial-patrol | ✅ 运行中 | 每 15 分钟 |
| bughunt-dashboard-sync | ✅ 运行中 | 每小时整点 |
| bughunt-pool-sync | ⏸ 已停用（近期不产卡） | 每 30 分钟 |

---

## 1. bughunt-trial-patrol（巡检）

| 项 | 值 |
|---|---|
| **ID** | `19119192-7913-489a-b9a3-d82d86b3e85d` |
| **频率** | 每 15 分钟 |
| **Session** | isolated |
| **超时** | 300 秒 |
| **类型** | 纯 agent cron（prompt 驱动，无外部脚本） |
| **状态** | ✅ 运行中 |

**功能：** 检查 10 个 Worker（worker-01~09 + Fabrice）的 1v1 工作通道最新消息，判断执行状态并生成巡检报告。

**数据源：** 各 Worker 的 DMWork 1v1 通道消息。

**报告发送到：** BugHunt 进度汇报子区（`19fe99c798914d5fac7d7de9e6fcc839____2044609885412265984`）

**报告格式：**
- 每个 Worker 一段：状态 emoji（🟢正常/🟡等待/🔴超时/🛑阻塞）+ 当前批次进度 + 最新完成的 task_id
- 底部汇总：按状态分组列出所有 Worker

**自动催促：** 如某 Worker 超过 20 分钟无新进展，自动在该 Worker 的 1v1 通道发送 @mention 催促消息。

**Worker 通道列表：**

| Worker | Channel ID | UID |
|--------|-----------|-----|
| Fabrice | 44998d9add6d40b287a38332cbaf61ca | hermes_bot |
| worker-01 | c7b092f81af944a286e1dd631038c4aa | worker01_bot |
| worker-02 | c6288de9437d4dbaa5d6a66573578b95 | worker02_bot |
| worker-03 | f72274d28dc740efb7805f70fd5bb3b3 | worker03_bot |
| worker-04 | 6d7d933c594044a688484ca815c06433 | worker04_bot |
| worker-05 | d94fe49dfeec4d52b491eb6b0479256b | worker05_bot |
| worker-06 | fcb1cd72ae25476ab713568df49fe2db | worker06_bot |
| worker-07 | 13aea54f953c4a53bac98d995a33c111 | worker07_bot |
| worker-08 | 1147ef05c926437ab28936d92fcc0590 | worker08_bot |
| worker-09 | 5c49656f14114b6285b0c32e6e6bff4e | worker09_bot |

---

## 2. dashboard-sync（Dashboard 同步）

| 项 | 值 |
|---|---|
| **ID** | `a91210a2-0cac-487f-a21c-97ae3444613f`（重建后新 ID） |
| **频率** | 每小时整点（cron `0 * * * *`，Asia/Shanghai） |
| **Session** | isolated |
| **脚本** | `~/.openclaw/workspace/scripts/bughunt/sync-dashboard.sh` |
| **状态** | ✅ 运行中 |

**功能：** 扫描 `results/` 目录所有执行结果 JSON + `tasks/pool/` 全量卡，生成 `dashboard/progress.json` 并 push 到 repo。

**数据源：** 只读 `results/` 文件和 `tasks/pool/` 总量，**不读不改 dispatch-log**。

**产出：** `dashboard/progress.json`，包含：
- summary：completed / failed / blocked / pending 统计
- tasks：每张卡的详细状态（task_id、status、worker、sess_id、duration、error）

**报告发送到：** BugHunt 进度汇报子区，格式：`📊 Dashboard Sync — completed: X | failed: X | blocked: X | pending: X | total: X`

---

## 3. pool-sync-dispatch（Pool 新卡自动同步）

| 项 | 值 |
|---|---|
| **ID** | `06f8e54f-5dce-4809-9a65-d20e58c31fef`（重建后新 ID） |
| **频率** | 每 30 分钟 |
| **Session** | isolated |
| **超时** | 120 秒 |
| **脚本** | `~/.openclaw/workspace/scripts/bughunt/sync-pool-to-dispatch.sh` |
| **状态** | ⏸ 已停用（近期智子不产卡，无需同步） |

**功能：** 扫描 `tasks/pool/`，找出不在 dispatch-log.json 中的新任务卡，自动完成：
1. 去掉 `ground_truth` 字段 → 生成 pool-clean 版本写入 `tasks/pool-clean/`
2. 以 `status: unassigned` 补录进 `pm-template/dispatch-log.json`
3. git commit + push

**作用：** 智子往 `tasks/pool/` push 新卡后，cron 自动同步到 pool-clean + dispatch-log，无需 PM 手动操作。

**报告发送到：** BugHunt 进度汇报子区，格式：`🔄 Pool 同步报告 — 新增 X 张卡（来自 Y 个项目）+ dispatch-log 总览`；无新卡时报"无新增"。

---

## 任务互补关系

```
智子 push 新卡到 tasks/pool/
    ↓
pool-sync-dispatch（每小时:30）→ 生成 pool-clean + 更新 dispatch-log
    ↓
PM 选卡排产 → Mycroft 派发 → Worker 执行
    ↓
Worker push 结果到 results/
    ↓
dashboard-sync（每小时:00）→ 扫 results/ 更新 progress.json
    ↓
bughunt-trial-patrol（每15分钟）→ 检查 Worker 通道消息 → 巡检报告 + 超时催促
```
