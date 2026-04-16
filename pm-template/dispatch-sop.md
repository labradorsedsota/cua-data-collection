# 派发工作 SOP（整体流程）

> 本文档描述 BugHunt 任务派发的完整工作方法、角色分工和状态管理。

---

## 一、角色与职责

| 角色 | 负责人 | 职责 |
|------|--------|------|
| **选卡排产** | Pichai | 决定哪个 Worker 跑哪些卡，更新 dispatch-log.json 状态为 `assigned` |
| **发送派发消息** | Mycroft | 读 dispatch-log.json，向 Worker 1v1 通道发送任务消息（见 dispatch-sop-mycroft.md） |
| **状态同步** | Pichai | 收到林菡通知"某群有更新"后，查看 Worker 消息，更新 dispatch-log.json |
| **异常处理** | Pichai | Worker 报异常时判断和干预 |
| **巡检** | Pichai | 监控 Worker 进度，催促无响应的 Worker |
| **Dashboard** | cron | 读 dispatch-log.json 生成统计报告 |

---

## 二、核心数据文件

| 文件 | 路径 | 用途 |
|------|------|------|
| dispatch-log.json | `pm-template/dispatch-log.json` | **唯一事实来源**，727 张卡全量在册 |
| 完整任务卡（含 ground_truth） | `tasks/pool/` | L2 抽检、FTY 终审用，**不发给 Worker** |
| 干净任务卡（无 ground_truth） | `tasks/pool-clean/` | Mycroft 发给 Worker 的卡 |
| 执行手册 | `worker-config/worker-execution-guide.md` | Worker 执行参考 |

---

## 三、整体工作流

```
Pichai 选卡 → 更新 dispatch-log.json（status: assigned）→ push
    ↓
Mycroft 读 dispatch-log.json → 找 status=assigned 的卡 → 发消息给 Worker（Mycroft 不改 dispatch-log）
    ↓
Worker ACK → 林菡通知 Pichai → Pichai 更新 status=in_progress → push
    ↓
Worker 逐 case 完成 → 林菡通知 Pichai → Pichai 更新 status=completed/failed（填 result）→ push
    ↓
批次完成 → Pichai 选下一批 → 循环
```

---

## 四、dispatch-log.json 结构

```json
{
  "version": "2.0",
  "updated_at": "2026-04-16T14:00:00+08:00",
  "summary": {
    "total": 727,
    "unassigned": 699,
    "assigned": 0,
    "in_progress": 20,
    "completed": 8,
    "failed": 0
  },
  "tasks": {
    "task_id": {
      "status": "unassigned|assigned|in_progress|completed|failed",
      "worker": "worker-02",
      "batch": 2,
      "assigned_at": "2026-04-16T12:33:00+08:00",
      "completed_at": "2026-04-16T13:20:00+08:00",
      "result": "abnormal|normal|unclear|deploy_failed|timeout|mano_cua_error",
      "note": "备注"
    }
  }
}
```

### 状态流转

```
unassigned → assigned（Pichai 选卡）→ in_progress（Worker ACK）→ completed/failed（Worker 完成）
```

所有状态变更由 Pichai 操作，Mycroft 不修改 dispatch-log。

---

## 五、Pichai 操作手册

### 5.1 选卡排产

1. `git pull` 最新 dispatch-log.json
2. 从 `status: unassigned` 的卡中选卡（规则：纯净优先、同项目同 Worker、每批 5 张）
3. **前置筛选（必须，按优先级依次检查）**：
   
   **硬性排除（直接跳过，标 failed + deploy_failed）：**
   - `backend_risk: true` 的卡
   - `repo_size_kb > 500000`（>500MB）的卡（交叉查 `tasks/pool/` 中对应卡的 `repo_size_kb` 字段）
   - `test_page` 是 `/login`、`/auth`、`/signin`、`/dashboard` 等需要认证的页面
   - 项目明显需要数据库（如看板工具、CRM、项目管理类应用）
   - 项目需要 OAuth/第三方认证（Google、GitHub 登录等）
   - `deploy_commands` 含 docker、database、prisma 关键词
   - 跳过的卡标 `status: "failed"`，`result: "deploy_failed"`，`note: "前置筛选跳过：[具体原因]"`
   
   **排产优先级（从高到低）：**
   - 优先选 `deploy_commands` 步骤 ≤3 的简单项目
   - 优先选 `repo_size_kb` 小的项目（<100MB 优先）
   - 同项目打包，每批 5 张，复用 clone + install
   - 100-200MB 的项目降优先级但不排除，视 Worker 能力分配
   
4. 更新选中卡的状态为 `assigned`，填入 `worker`、`batch`、`assigned_at`
5. 更新 `summary` 统计
6. `git push`

> **注意：** `repo_size_kb` 字段目前只在 `tasks/pool/` 的完整卡中有，`tasks/pool-clean/` 暂未同步。选卡时交叉查 pool 中对应卡获取该字段。

### 5.2 状态同步（收到林菡通知时）

1. 林菡说"worker-XX 有更新"
2. 查看对应 Worker 1v1 群的最近消息
3. 根据消息内容更新 dispatch-log.json：
   - Worker ACK → `status: in_progress`
   - Worker 完成某 case → `status: completed`，填 `result`、`completed_at`、`note`
   - Worker 报异常 → 在 `note` 中记录，判断是否干预
4. 更新 `summary` 统计
5. `git push`

### 5.3 异常处理

| 场景 | 处理 |
|------|------|
| Worker 30 分钟未 ACK | 在 1v1 通道 @Worker 催促 |
| Worker ACK 后 20 分钟无进度 | @Worker 询问状态 |
| Worker 报 deploy_failed | 建议 nvm 切版本或标 failed 跳过 |
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

1. **dispatch-log.json 是唯一事实来源** — 所有角色通过它同步状态
2. **每次修改后必须 push** — git pull → 改 → push
3. **Mycroft 只从 pool-clean/ 读卡** — pool/ 含 ground_truth，绝不发给 Worker
4. **所有 Worker 汇报必须 @Pichai** — 不带 mention 字段的消息 PM 收不到
5. **每批 5 张，同项目同 Worker** — 复用部署提效
