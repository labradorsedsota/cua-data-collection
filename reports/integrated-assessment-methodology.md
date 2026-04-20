# Integrated Assessment 方法论与复用指南

> 版本：v1.1  
> 更新时间：2026-04-20  
> 作者：Pichai  

---

## 一、目的

对 BugHunt 项目 `results/` 目录中的所有 result 卡做全量质量评估，整合合规检查、轨迹匹配、去重信息，输出一张表，标记可交付的有效数据。

---

## 二、数据源

| 数据源 | 路径 | 说明 |
|--------|------|------|
| result 卡 | repo `results/worker-*/` | 全集，每张 JSON 一个执行结果 |
| 任务卡 | repo `tasks/pool-clean/` | 原始任务定义（含 test_description_zh, dev_url, app_name） |
| TOS 轨迹 | `/Users/mlt/Documents/code/oss/tos_trajectories/trajectories/{sess_id}/` | mano-cua 执行轨迹 |
| 脚本目录 | `/Users/mlt/.openclaw/workspace/scripts/bughunt-assessment/` | 所有评估脚本 |
| 脚本输出 | `/Users/mlt/.openclaw/workspace/scripts/bughunt-assessment/output/` | LLM 匹配结果等中间产物 |

---

## 三、评估维度（列定义）

| 列名 | 来源 | 说明 |
|------|------|------|
| task_id | result 卡 | 任务唯一标识 |
| file | result 卡 | 文件路径 worker/filename |
| worker | result 卡 | 执行 Worker |
| sess_id | result 卡 | session ID |
| status | result 卡 | completed / failed |
| mano_cua_status | result 卡 → mano_cua.status | COMPLETED / STOPPED_BY_USER / TIMEOUT 等 |
| mano_cua_result | result 卡 → mano_cua.result | normal / abnormal / unclear |
| total_steps | result 卡 → mano_cua.total_steps | 执行步数 |
| compliance | 合规检查 | pass / warn / fail |
| compliance_issues | 合规检查 | 不合规项编号（如 "#9, #10"） |
| has_trajectory | 本地轨迹 | yes / no / N/A(failed卡) |
| trajectory_match | LLM 匹配 | match / mismatch / no_data / error / N/A |
| match_confidence | LLM 匹配 | 0.0-1.0 置信度 |
| app_name_match | 强匹配 | 轨迹 task 是否包含 app_name |
| dev_url_host_match | 强匹配 | 轨迹 task 是否包含 host |
| dev_url_port_match | 强匹配 | 轨迹 task 是否包含 port |
| is_duplicate | 去重检查 | 同 task_id 是否跨 worker 出现 |
| grade | 综合评级 | A/B/C/D |
| selected | 最终筛选 | Y/N |

---

## 四、评级规则

**优先级：D > C > B > A（取最严重）**

| 等级 | 触发条件 |
|------|----------|
| D | completed 但无本地轨迹（has_trajectory=no） |
| C | 红色合规问题（#2,#3,#4,#5,#6,#7,#11）或 trajectory_match=mismatch |
| B | 黄色合规问题（#9,#10,#14,#15,#16）或 trajectory_match=error |
| A | 无问题 |

---

## 五、合规检查项

| 编号 | 含义 | 严重度 |
|------|------|--------|
| #2 | 必填字段缺失 | 🔴 C级 |
| #3 | status 值非法 | 🔴 C级 |
| #4 | completed 卡 mano_cua 不完整 | 🔴 C级 |
| #5 | mano_cua.result 值非法 | 🔴 C级 |
| #6 | sess_id 格式不合规 | 🔴 C级 |
| #7 | failed 卡 failure 不完整 | 🔴 C级 |
| #9 | task_id 跨 worker 重复 | 🟡 B级 |
| #10 | total_steps > 80 | 🟡 B级 |
| #11 | status=completed 但 result=deploy_failed | 🔴 C级 |
| #14 | timestamp 非标准 ISO 8601 | 🟡 B级 |
| #15 | failed 卡 mano_cua 非 null | 🟡 B级 |
| #16 | failed 卡 sess_id 非 null | 🟡 B级 |

---

## 六、selected 筛选标准

**selected = Y** 需同时满足全部条件：

1. status = completed
2. mano_cua_status = COMPLETED
3. has_trajectory = yes
4. trajectory_match = match
5. grade = A 或 B

---

## 七、LLM 轨迹匹配方法

**模型：** claude-haiku-4-5（via mininglamp gateway）

**API：**
```
POST https://llm-gateway.mlamp.cn/v1/chat/completions
Authorization: Bearer {API_KEY}
Model: claude-haiku-4-5
```

**Prompt 模板：**
```
你是一个数据质量审核员。请判断以下两段文本是否描述的是同一个测试任务。

【任务卡描述 (test_description_zh)】
{test_description_zh from tasks/pool-clean/{task_id}.json}

【轨迹中的实际任务描述 (trajectory task)】
{task field from trajectories/{sess_id}/result.json}

请回答：
1. same_task: true 或 false
2. confidence: 0.0-1.0
3. reason: 简短说明

严格按 JSON 格式回复：
{"same_task": true/false, "confidence": 0.95, "reason": "..."}
```

**范围：** 所有 status=completed 且 mano_cua.status=COMPLETED 的卡

**输出：** same_task + confidence + reason

---

## 八、强匹配检查方法

从任务卡取 `app_name` 和 `dev_url`，从轨迹 `result.json` 取 `task` 字段：

- **app_name_match：** `app_name.lower()` 是否出现在 `task.lower()` 中
- **dev_url_host_match：** URL 的 hostname 是否出现在 task 中
- **dev_url_port_match：** URL 的 port 是否出现在 task 中

---

## 九、执行步骤（下次复用）

### 前置准备

```bash
# 1. Clone repo (sparse checkout)
git clone --filter=blob:none --sparse https://github.com/labradorsedsota/bughunt.git /tmp/bughunt-check
cd /tmp/bughunt-check
git sparse-checkout set results tasks/pool-clean reports

# 2. 确认轨迹目录
TRAJ_DIR="/Users/mlt/Documents/code/oss/tos_trajectories/trajectories"
ls $TRAJ_DIR | wc -l  # 应有 520+

# 3. 如有新增 result 卡的 sess_id 缺轨迹，先补下载
python3 ~/.openclaw/workspace/scripts/bughunt-assessment/download_missing_batch.py
```

### 执行评估

```bash
SCRIPTS=~/.openclaw/workspace/scripts/bughunt-assessment

# 4. 运行 LLM 匹配（后台，约 20 分钟）
# 注意：脚本中 RESULTS_DIR/TASKS_DIR 仍指向 /tmp/bughunt-check，需要先 clone repo
python3 $SCRIPTS/llm_match_check.py &

# 5. 运行整合报告
python3 $SCRIPTS/integrate_report.py

# 6. 推到线上
cd /tmp/bughunt-check
git add reports/integrated-assessment-*.{csv,json,md}
git commit -m "update: integrated assessment YYYY-MM-DD"
git push origin main
```

---

## 十、文件位置总览

| 文件 | 持久化路径 | 说明 |
|------|-----------|------|
| LLM 匹配脚本 | `~/.openclaw/workspace/scripts/bughunt-assessment/llm_match_check.py` | 调 claude-haiku-4-5 |
| 整合报告脚本 | `~/.openclaw/workspace/scripts/bughunt-assessment/integrate_report.py` | 合并数据源 |
| 合规检查脚本 | `~/.openclaw/workspace/scripts/bughunt-assessment/compliance_check.py` | 18 项检查 |
| TOS 下载脚本 | `~/.openclaw/workspace/scripts/bughunt-assessment/download_missing_batch.py` | 批量下载 |
| 脚本输出目录 | `~/.openclaw/workspace/scripts/bughunt-assessment/output/` | LLM 结果、日志 |
| 轨迹数据 | `/Users/mlt/Documents/code/oss/tos_trajectories/trajectories/` | 520 session, 24GB |
| 原始下载脚本 | `~/.openclaw/workspace/download_sess.py` | 单个 sess_id 下载 |

---

## 十一、注意事项

1. **repo 每次用 sparse clone 到 /tmp/bughunt-check** — 这是临时工作目录，脚本中 RESULTS_DIR/TASKS_DIR 指向这里
2. **轨迹已在持久化路径** — 不会因重启丢失
3. **LLM API budget** — 本地 proxy (127.0.0.1:18792) 已超 budget，用 mininglamp gateway 直连
4. **app_name 命名不一致是正常的** — npm 包名 vs 产品名，LLM 能正确判定
5. **重复卡（#9）是 B 级** — 不影响 selected，但标记提醒去重

---

*本文档随项目迭代更新。*
