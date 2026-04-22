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
   
   **硬性排除（直接跳过，不放入 dispatch-log）：**
   - `deploy_status` 为 `no_script_low_roi` 或 `no_script_dead` 的卡
   - `backend_risk: true` 的卡
   - `repo_size_kb > 500000`（>500MB）的卡
   - `test_page` 是需要认证的页面（/login、/auth、/signin、/dashboard 等）
   - 项目明显需要数据库（看板工具、CRM、项目管理类应用）
   - 项目需要 OAuth/第三方认证
   - `deploy_commands` 含 docker、database、prisma 关键词
   
   **排产优先级（从高到低）：**
   - 优先选 `deploy_commands` 步骤 ≤3 的简单项目
   - 优先选 `repo_size_kb` 小的项目（<100MB 优先）
   - 同 repo + 同 buggy_commit 的卡打包给同一个 Worker（确保熔断机制在 Worker 本地生效）
   - 同 repo 不同 buggy_commit 也尽量给同一 Worker（复用 clone + install）
   - 100-200MB 的项目降优先级但不排除
   
4. 更新选中卡的状态为 `assigned`，填入 `worker`、`batch`、`assigned_at`
5. 更新 `summary` 统计
6. `git push`
7. 通知 Mycroft 派发：**必须在「执行专用」子区（`19fe99c798914d5fac7d7de9e6fcc839____2043640961514344448`）@Mycroft 下达指令，不要发到主群**
8. 指令中必须明确写：**"用你自己的 bot token 发送，不要用 Pichai 的 token"**

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
| Worker 报 deploy_failed | Worker 按 guide 自行执行熔断（同 buggy_commit 连续 2 张 deploy_failed → 该 commit 剩余卡自动跳过），PM 不需要介入熔断判断。如 Worker 主动上报需协助的，再个案处理 |
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
