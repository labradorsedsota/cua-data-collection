# BugHunt PM 巡检方案

## 通信拓扑

```
广播群（汇报）──── PM (Pichai)
                      ├── 1v1 群: Fabrice
                      └── 1v1 群: Moss
                      └── ... (扩展到 10 Worker)
```

## 群 Session 配置

| 群 | channel_id | 用途 |
|----|------------|------|
| 广播群 | `__BROADCAST_CHANNEL_ID__` | 巡检汇总、里程碑播报 |
| Fabrice 工作群 | `__FABRICE_CHANNEL_ID__` | 任务分发、状态收集 |
| Moss 工作群 | `__MOSS_CHANNEL_ID__` | 任务分发、状态收集 |

> ⚠️ 建群后由 PM 填入实际 channel_id

## 巡检频率

- POC：每 15 分钟
- 10 Worker：每 15 分钟（cron 自动化）

## 巡检数据源

**patrol-status.json**（PM 本地维护）

每次收到 Worker 在 1v1 群的状态信号时，PM 更新此文件。
巡检时读取此文件检查规则。

```json
{
  "workers": {
    "worker-fabrice": {
      "last_signal_time": "2026-04-14T16:05:00+08:00",
      "last_task_id": "luxesite-253",
      "last_result": "abnormal",
      "completed": 3,
      "failed": 1,
      "total_assigned": 5,
      "consecutive_failures": 0,
      "results": {
        "normal": 1,
        "abnormal": 2,
        "unclear": 0
      }
    },
    "worker-moss": {
      "last_signal_time": "2026-04-14T16:02:00+08:00",
      "last_task_id": "lumen-253",
      "last_result": "normal",
      "completed": 2,
      "failed": 0,
      "total_assigned": 5,
      "consecutive_failures": 0,
      "results": {
        "normal": 2,
        "abnormal": 0,
        "unclear": 0
      }
    }
  },
  "last_patrol": "2026-04-14T16:10:00+08:00",
  "patrol_count": 5
}
```

## 巡检规则（4 条）

### 规则 1：失联检测
- **触发**：Worker 最后信号超过 20 分钟
- **动作**：在该 Worker 的 1v1 群发询问："20 分钟没收到状态，当前情况？"
- **升级**：询问后 5 分钟无响应 → 在广播群标红预警

### 规则 2：连续失败
- **触发**：同一 Worker 连续 3 个 failed
- **动作**：在 1v1 群发暂停指令 + 要求诊断汇总
- **升级**：汇报到广播群

### 规则 3：速率预警
- **触发**：实际完成速率 < 目标速率的 80%
- **计算**：目标速率 = total_assigned / 预估总时间，实际速率 = completed / 已用时间
- **动作**：分析瓶颈（部署慢？mano-cua 超时多？），在广播群预警

### 规则 4：质量预警
- **触发**：unclear 比例 > 30%
- **动作**：抽查 unclear case 的 result_summary，判断是任务描述问题还是 mano-cua 问题
- **升级**：如果是任务描述问题 → 通知智子修正

## 巡检输出

每次巡检在**广播群**发汇总：

```
🔍 巡检 16:30
worker-fabrice: ✅ 3/5 | abnormal | 最后信号 3min 前
worker-moss: ⚠️ 2/5 | normal | 22min 无信号 → 已询问
整体: 5/10 (50%) | 速率正常 | 预计 17:30 完成
异常: 无
```

有异常时：
```
🔍 巡检 16:45
worker-fabrice: 🔴 3/5 | 连续 3 个 failed → 已暂停
worker-moss: ✅ 4/5 | normal | 最后信号 1min 前
整体: 7/10 (70%) | ⚠️ fabrice 暂停中
异常: fabrice 连续失败，疑似 ha-fusion 项目部署问题，已要求诊断
```

## 巡检流程（每次执行）

1. 读取 `patrol-status.json`
2. 计算各 Worker 距上次信号的时间
3. 逐条检查 4 条规则
4. 有触发 → 在对应 1v1 群发干预消息
5. 生成汇总 → 发到广播群
6. 更新 `patrol-status.json` 的 `last_patrol` 时间

## Worker 状态信号更新流程

Worker 在 1v1 群发状态信号时，PM 立即更新 patrol-status.json：

收到 `✅ luxesite-253 | 4m32s | abnormal | 404页面无返回链接`
→ 更新:
  - last_signal_time = now
  - last_task_id = luxesite-253
  - last_result = abnormal
  - completed += 1
  - results.abnormal += 1
  - consecutive_failures = 0

收到 `❌ cleaningsvc-18 | deploy_failed | npm install 编译错误`
→ 更新:
  - last_signal_time = now
  - last_task_id = cleaningsvc-18
  - failed += 1
  - consecutive_failures += 1

## POC → 10 Worker 扩展

| 项目 | POC (2 Worker) | 10 Worker |
|------|---------------|-----------|
| 巡检方式 | PM 手动（cron 提醒） | cron 自动执行脚本 |
| 状态文件 | 本地 JSON | 同（或 repo） |
| 巡检输出 | 广播群 | 同 |
| 干预方式 | PM 手动在 1v1 群发 | 同（自动化待评估） |
