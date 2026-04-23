# Batch 9 排产优先级方案

> 版本：v1.0 | 日期：2026-04-23 | 作者：Pichai
> 基于 Batch 1-8 共 942 张执行结果的数据分析

## 一、数据基础

- Batch 9 未排产（unassigned）：2,451 张
- 数据源：`tasks/pool/*.json` 卡字段 + `/tmp/batch9_repo_scan.json` repo 特征扫描
- 历史参照：Batch 1-8 共 942 张（466 completed / 476 failed）

## 二、硬性排除规则

以下条件命中即不排产，共排除 **481 张**：

| # | 规则 | 字段/来源 | 数量 | 数据依据 |
|---|------|----------|------|---------|
| 1 | deploy_status = no_script_dead | pool 卡 `deploy_status` | 97 张 | SOP §5.1 现有规则 |
| 2 | deploy_status = no_script_low_roi | pool 卡 `deploy_status` | 69 张 | SOP §5.1 现有规则 |
| 3 | repo > 500MB | pool 卡 `repo_size_kb` | 98 张 | SOP §5.1 现有规则 |
| 4 | backend_risk = True | pool 卡 `backend_risk` | 24 张 | SOP 现有规则，历史 79% fail |
| 5 | **archived = true**（新增） | repo 扫描 `archived` | 177 张 | Batch 1-8 中 8 张全 failed（100%） |
| 6 | **node_version 严格冲突**（新增） | repo 扫描 `node_engines` | 16 张 | 要求 <18 或指定旧版本，Worker Node 22 必 fail |

> 注：规则按顺序匹配，一张卡只计入首次命中的规则。实际有重叠（如 backend_risk + archived）。

### node_version 严格冲突判定条件

`node_engines` 包含以下模式之一：`<18`、`<16`、`<14`、`8.10`、`10.x`、`12.x`、`14.x`

## 三、排产优先级

排除后剩余 **1,970 张 / 360 个 repo**，按以下优先级排产：

| 优先级 | 条件 | 卡数 | repo 数 | 预期成功率 | 排产理由 |
|-------|------|------|---------|-----------|---------|
| **P1** | < 20MB，非高风险框架，无 node-sass | 809 张 | 154 个 | ~57% | 体积小、clone/install 快，历史成功率最高 |
| **P2** | 20-100MB，非高风险框架，无 node-sass | 594 张 | 101 个 | ~46% | 中等体量，成功率接近均值 |
| **P3** | 100-500MB，非高风险框架，无 node-sass | 322 张 | 51 个 | ~40% | 体量大但无其他风险因素 |
| **P4** | Next.js/Gatsby/Lit < 100MB，或含 node-sass | 236 张 | 49 个 | ~25% | Next.js 历史 75% fail；node-sass Node 18+ 编译大概率失败 |
| **P5** | Next.js/Gatsby/Lit ≥ 100MB | 9 张 | 5 个 | ~20% | 高风险框架 + 大体积，双重负面 |

### 高风险框架定义

基于 Batch 1-8 失败率：
- **Next.js**：75% fail（92 张中 69 张 failed）— SSR 天然依赖后端
- **Gatsby**：75% fail（4 张中 3 张 failed，样本少）
- **Lit**：100% fail（5 张全 failed）

### 优先级判定因素（按权重）

1. **repo 大小**：< 20MB（57% 成功）→ 20-100MB（46%）→ 100-200MB（45%）→ 200MB+（33%）
2. **框架**：Vanilla/Nuxt 最安全（25% fail），React/Vue/Angular 中等（~52%），Next.js/Lit 最危险（75%+）
3. **native 依赖**：node-sass 高危（Node 18+ 编译失败），sharp/puppeteer 相对安全

### 不作为排产因素的条件

| 条件 | 原因 |
|------|------|
| monorepo | Batch 1-8 失败率 33%，低于均值 50%，不应降优先级 |
| sharp/puppeteer/playwright | macOS 编译成功率高，历史仅 5 次失败 |
| 宽松 node_version（如 >=8.0.0） | Worker Node 22 完全满足 |

## 四、排产约束

- **同 repo + 同 buggy_commit 打包同一 Worker**（熔断依赖）
- 每个 repo 平均 5.7 张卡

## 五、执行节奏估算

按 8 个活跃 Worker、每人每天 ~20 张：

| 阶段 | 累计卡数 | 预计天数 | 预期累计 completed |
|------|---------|---------|-------------------|
| P1 | 809 张 | ~5 天 | ~460 张 |
| P1+P2 | 1,403 张 | ~9 天 | ~730 张 |
| P1-P3 | 1,725 张 | ~11 天 | ~860 张 |
| P1-P5 | 1,970 张 | ~12.5 天 | ~910 张 |

## 六、执行脚本

排产脚本：`scripts/batch9-prioritize.py`

用法：
```bash
cd /path/to/bughunt
python3 scripts/batch9-prioritize.py
```

输出：按优先级排序的 task_id 列表 + 统计摘要，写入 `pm-template/batch9-priority-output.json`

## 七、Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-23 | 初始版本 |
