# Dashboard 技术文档

> BugHunt 任务看板的数据源、计算逻辑和同步机制。

---

## 一、文件结构

| 文件 | 用途 | 生成方式 |
|------|------|----------|
| `dashboard/index.html` | 看板前端页面 | 手动维护 |
| `dashboard/progress.json` | 执行结果数据 | cron 自动生成 |
| `dashboard/overall.json` | 全局统计数据 | cron 自动生成 |

**部署方式：** GitHub Pages，访问 `index.html` 即可查看看板。

---

## 二、数据源

Dashboard 依赖两个上游数据源，**只读不写**：

| 数据源 | 路径 | 维护者 | 包含信息 |
|--------|------|--------|----------|
| result 文件 | `results/worker-XX/*.json` | Worker push | 每张任务卡的执行结果 |
| dispatch-log | `pm-template/dispatch-log.json` | Pichai（PM） | 每张卡的分发状态 |

两个数据源完全解耦：
- dispatch-log 只管分发（unassigned → assigned → dispatched）
- result 文件只记录执行结果（completed / failed）

---

## 三、progress.json

### 职责

只读 `results/` 目录和 `tasks/pool/`，生成每张任务卡的执行结果。**不读 dispatch-log。**

### 数据结构

```json
{
  "last_updated": "2026-04-23 15:00:00",
  "summary": {
    "total": 3373,
    "completed": 454,
    "failed": 466,
    "blocked": 0,
    "pending": 2453
  },
  "tasks": [
    {
      "task_id": "repo-123",
      "status": "completed",
      "worker": "worker-01",
      "result": "abnormal",
      "sess_id": "...",
      "repo": "owner/repo",
      "duration_seconds": 120,
      "error": "",
      "result_summary": "..."
    }
  ]
}
```

### 计算逻辑

1. 扫 `tasks/pool/*.json` → 获取全部 task_id（总量）
2. 扫 `results/**/*.json` → 获取执行结果
3. **去重规则**（同一 task_id 有多条 result 时）：
   - 优先级：completed+COMPLETED > completed > failed > blocked > 其他
   - 同优先级按时间降序，取最新
4. 状态判定：
   - `blocked`：status=blocked 或 mano_status=BLOCKED
   - `failed`：status=failed 或 deploy_status=failed 或 mano_status=FAILED
   - `completed`：其他有结果的
   - `pending`：无 result 的卡

---

## 四、overall.json

### 职责

综合 `progress.json` 和 `dispatch-log.json`，生成全局统计数字。用于 Dashboard 顶部统计卡片。

### 数据结构

```json
{
  "last_updated": "2026-04-23 15:36:15",
  "overall": {
    "total": 3373,
    "unassigned": 2451,
    "dispatched": 922,
    "running": 2,
    "completed": 454,
    "failed": 466
  }
}
```

### 字段定义与计算逻辑

| 字段 | 含义 | 计算方式 |
|------|------|----------|
| `total` | 总任务数 | `tasks/pool/` 中的卡总量 |
| `unassigned` | 未分配 | total - dispatched |
| `dispatched` | 已派发（累计） | dispatch-log 中 status=dispatched 的总数（含已出结果的） |
| `running` | 执行中 | dispatched - completed - failed（已派发但还没出结果的） |
| `completed` | 已完成 | progress.json 中 status=completed 的数量 |
| `failed` | 失败 | progress.json 中 status=failed 或 blocked 的数量 |

### 数学关系

```
total = unassigned + dispatched
dispatched = running + completed + failed
```

两个等式始终成立，保证数据自洽。

---

## 五、同步机制（cron job）

| 配置项 | 值 |
|--------|---|
| Job 名称 | `bughunt-dashboard-sync` |
| 触发频率 | 每小时整点（`0 * * * *`，Asia/Shanghai） |
| 执行脚本 | `scripts/bughunt/sync-dashboard.sh` |
| Session 模式 | isolated（独立 session，不影响主 session） |
| Delivery | none（脚本内部自行 curl 发报告） |

### 执行流程

```
git pull（增量同步）
    ↓
扫 results/ + tasks/pool/ → 生成 progress.json
    ↓
读 dispatch-log + progress.json → 生成 overall.json
    ↓
git add + commit + push
    ↓
curl 发送简报到「BugHunt 进度汇报子区」
```

### 报告格式

发送到进度汇报子区（channel_type: 5）：
```
📊 Dashboard Sync (2026-04-23 15:36:15)

✅ 完成 454 | ❌ 失败 466 | 🔄 执行中 2 | 🚀 已派发 922 | ⏳ 未分配 2451 | 📊 总计 3373
```

---

## 六、前端展示逻辑

### 统计卡片（顶部 6 张）

从 `overall.json` 读取，展示 6 个维度：

| 卡片 | 字段 | 颜色 |
|------|------|------|
| 总任务 | total | 白色 |
| 未分配 | unassigned | 灰色 |
| 已派发 | dispatched | 蓝色 |
| 执行中 | running | 黄色 |
| 已完成 | completed | 绿色 |
| 失败 | failed | 红色 |

**降级策略：** overall.json 加载失败时，从 progress.json 统计（只能展示 pending/completed/failed 三态）。

### Worker 概览

从 `progress.json` 统计每个 Worker 的完成数、成功率、平均耗时。

### 任务列表

从 `progress.json` 读取完整任务列表，支持：
- 搜索（task_id / 项目名）
- 按状态、Worker、结果筛选
- 列排序

### 数据加载

- 并行 fetch `progress.json` 和 `overall.json`
- 优先尝试相对路径（GitHub Pages），失败回退 GitHub API
- 自动刷新间隔：60 秒

---

## 七、变更记录

| 日期 | 变更 |
|------|------|
| 2026-04-20 | 初版 Dashboard：progress.json + index.html |
| 2026-04-23 | 新增 overall.json，统计卡片改为 5 态展示（未分配/已派发/执行中/已完成/失败） |
