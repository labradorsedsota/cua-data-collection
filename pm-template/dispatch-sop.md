# 派发工作 SOP（整体流程）

> 本文档描述 BugHunt 任务派发的完整工作方法、角色分工和状态管理。

---

## 一、角色与职责

| 角色 | 负责人 | 职责 |
|------|--------|------|
| **选卡排产** | Pichai | 决定哪个 Worker 跑哪些卡，更新 dispatch-log.json 状态为 `assigned` |
| **发送派发消息** | Mycroft | 读 dispatch-log.json，向 Worker 1v1 通道发送任务消息（见 dispatch-sop-mycroft.md） |
| **确认派发** | Pichai | Mycroft 报告消息已发送后，更新 dispatch-log.json 状态为 `dispatched` |
| **异常处理** | Pichai | Worker 报异常时判断和干预 |
| **巡检** | Pichai | 监控 Worker 进度，催促无响应的 Worker |
| **Dashboard** | cron | 扫 `results/` 目录生成 `dashboard/progress.json` |

---

## 二、核心数据文件

| 文件 | 路径 | 用途 | 谁写 |
|------|------|------|------|
| dispatch-log.json | `pm-template/dispatch-log.json` | **分发追踪**，只管卡从未分配到已派发 | Pichai |
| progress.json | `dashboard/progress.json` | **执行结果**，只看 result 文件 | cron 自动 |
| 完整任务卡 | `tasks/pool/` | L2 抽检、FTY 终审用，**不发给 Worker** | 智子 |
| 干净任务卡 | `tasks/pool-clean/` | Mycroft 发给 Worker 的卡 | 从 pool 清洗 |
| 执行手册 | `worker-config/worker-execution-guide.md` | Worker 执行参考 | Pichai |
| result 文件 | `results/worker-XX/*.json` | Worker 执行结果 | Worker push |

---

## 三、整体工作流

```
Pichai 选卡 → 更新 dispatch-log（status: assigned）→ push
    ↓
Mycroft 读 dispatch-log → 找 status=assigned 的卡 → 发消息给 Worker
    ↓
Mycroft 报告"已发送" → Pichai 更新 dispatch-log（status: dispatched）→ push
    ↓
（dispatch-log 的使命到此结束，不再变动）
    ↓
Worker 执行 → push result 文件到 results/worker-XX/
    ↓
cron 每小时扫 result 文件 → 更新 dashboard/progress.json
```

**两个文件完全解耦：**
- dispatch-log 只管分发（Pichai 操作）
- progress.json 只看执行结果（cron 自动扫 result 文件）

---

## 四、dispatch-log.json 结构

```json
{
  "version": "3.0",
  "updated_at": "2026-04-16T23:48:00+08:00",
  "summary": {
    "total": 727,
    "unassigned": 488,
    "assigned": 0,
    "dispatched": 239
  },
  "tasks": {
    "task_id": {
      "status": "unassigned|assigned|dispatched",
      "worker": "worker-02",
      "batch": 2,
      "assigned_at": "2026-04-16T12:33:00+08:00"
    }
  }
}
```

### 状态流转（只有 3 个状态）

```
unassigned → assigned（Pichai 选卡）→ dispatched（Mycroft 发送后 Pichai 确认）
```

所有状态变更由 Pichai 操作，Mycroft 不修改 dispatch-log。

---

## 五、Pichai 操作手册

### 5.1 选卡排产

1. `git pull` 最新 dispatch-log.json
2. 从 `status: unassigned` 的卡中选卡
3. **前置筛选（必须，按优先级依次检查）**：
   
   **硬性排除（直接跳过，不排产）：**
   - `deploy_status` 为 `no_script_low_roi` 或 `no_script_dead` 的卡
   - `backend_risk: true` 的卡
   - `repo_size_kb > 500000`（>500MB）的卡
   - `archived: true` 的 repo（Batch 1-8 历史 100% fail）
   - `node_engines` 与 Worker Node 22 严格冲突（要求 <18 或指定旧版本如 8.10.x）
   - `test_page` 是需要认证的页面（/login、/auth、/signin、/dashboard 等）
   - 项目明显需要数据库（看板工具、CRM、项目管理类应用）
   - 项目需要 OAuth/第三方认证
   - `deploy_commands` 含 docker、database、prisma 关键词
   
   **排产优先级（从高到低）：**
   
   > Batch 9 详细排产方案见 [`batch9-priority-plan.md`](batch9-priority-plan.md)，排产脚本见 [`../scripts/batch9-prioritize.py`](../scripts/batch9-prioritize.py)
   >
   > **脚本产出说明：** 脚本输出 `batch9-priority-output.json`，其中 `excluded` 和 `priority_tiers`（P1-P5）两个集合完全互斥——被硬性排除的卡不会出现在 P1-P5 中。排产时只从 `priority_tiers` 里选卡即可。
   
   | 优先级 | 条件 | 预期成功率 |
   |-------|------|-----------|
   | P1 | < 20MB，非高风险框架，无 node-sass | ~57% |
   | P2 | 20-100MB，非高风险框架，无 node-sass | ~46% |
   | P3 | 100-500MB，非高风险框架，无 node-sass | ~40% |
   | P4 | 高风险框架(Next.js/Gatsby/Lit) < 100MB，或含 node-sass | ~25% |
   | P5 | 高风险框架 ≥ 100MB | ~20% |
   
   **高风险框架**（基于 Batch 1-8 历史 fail rate ≥ 70%）：Next.js、Gatsby、Lit
   
   **其他排产规则：**
   - 同 repo + 同 buggy_commit 的卡打包给同一个 Worker（确保熔断机制在 Worker 本地生效）
   - 同 repo 不同 buggy_commit 也尽量给同一 Worker（复用 clone + install）
   
4. 更新选中卡的状态为 `assigned`，填入 `worker`、`batch`、`assigned_at`
5. 更新 `summary` 统计
6. `git push`
7. 通知 Mycroft 派发：在「执行专用」子区 @Mycroft 下达指令（见附录 A 指令模板）

### 5.2 确认派发

1. Mycroft 报告"X/X 全部派发到位"
2. 把对应卡从 `assigned` → `dispatched`
3. 更新 `summary`
4. `git push`

### 5.3 选卡时避免重复分配

- dispatch-log 里 `assigned` 或 `dispatched` 的跳过
- `results/` 目录下已有 result 文件的跳过

### 5.4 异常处理

| 场景 | 处理 |
|------|------|
| Worker 30 分钟未 ACK | 在 1v1 通道 @Worker 催促 |
| Worker ACK 后 20 分钟无进度 | @Worker 询问状态 |
| Worker 报 deploy_failed | 建议 nvm 切版本或跳过 |
| Worker 完成批次 | 选下一批卡，走选卡排产流程 |

---

## 六、Worker 通道表

| Worker | Channel ID | UID |
|--------|-----------|-----|
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

## 七、关键规则

1. **dispatch-log 只管分发** — unassigned → assigned → dispatched，不跟踪执行结果
2. **progress.json 只看 result 文件** — completed/failed/blocked/pending，不读 dispatch-log
3. **每次修改 dispatch-log 后必须 push**
4. **Mycroft 只从 pool-clean/ 读卡** — pool/ 含 ground_truth，绝不发给 Worker
5. **所有 Worker 汇报必须 @Pichai** — 不带 mention 字段的消息 PM 收不到
6. **同 repo + 同 buggy_commit 同 Worker** — 确保 Worker 本地熔断生效；同 repo 不同 commit 也尽量同 Worker 以复用部署

---

## 附录 A：通知 Mycroft 派发（指令模板）

在「执行专用」子区 @Mycroft 发送以下指令（替换 `{变量}` 后发送）：

```
@Mycroft 派发指令：

**请严格按照你的操作手册 `pm-template/dispatch-sop-mycroft.md` 执行。**

1. 拉取 repo（按手册§三步骤 1）
2. 读取 `pm-template/dispatch-log.json`，找出所有 `status: "assigned"` 的卡，按 worker 分组
3. 对每个有 assigned 卡的 Worker，向其 1v1 通道发送 2 条消息（按手册§三的模板，严格按顺序，间隔 200-300ms）：
   - 消息 1：派发指令（任务 ID 列表 + 执行手册位置 + pool-clean 路径），不需要 mention
   - 消息 2：汇报规则，必须 @Worker（payload 带 mention 字段）
4. Worker 通道表见手册§四
5. 用你自己的 bot token 发送，不要用 Pichai 的 token
6. 不需要逐张发任务卡 JSON，Worker 自行从 repo 的 tasks/pool-clean/ 读取
7. batch 号为 {BATCH_NUM}
8. {EXTRA_NOTE}
9. 完成后清理临时目录，回报派发结果（成功/失败的 Worker 列表）
```

**使用说明：**
- `{BATCH_NUM}`：替换为当前批次号
- `{EXTRA_NOTE}`：如有特殊提醒（如执行手册版本变更）写在这里，无则删除此行
- 不需要手动指定 Worker 列表，Mycroft 从 dispatch-log 中自动识别有 assigned 卡的 Worker
