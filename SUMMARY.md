# BugHunt 项目全景摘要

> 生成时间：2026-04-21
> 统计来源：tasks/pool/ JSON count, results/ JSON count, reports/integrated-assessment/

---

## 一、数据规模

| 指标 | 数值 | 来源 |
|------|------|------|
| 候选项目池 | 944（bugs 5-500, stars≥100, deploy=easy） | phase2_results.jsonl 实跑 |
| 预过滤后候选（Batch 1-8 用） | 711 | FRAMEWORK_REPOS + KEYWORDS + stars>50K |
| Batch 1-8 产卡 | 832 张 / 229 个项目 | tasks/pool/ 匹配 |
| Batch 9 产卡 | 2,541 张 / 445 个项目 | data/batch9_tasks.jsonl.final |
| **合计** | **3,373 张 / 674 个项目** | tasks/pool/ JSON count |

## 二、各批次参数与状态

| 批次 | 扫描项目 | 参数 | 卡量 | 状态 |
|------|---------|------|------|------|
| POC | 5 | Easy + Medium 对照 | 25 | ✅ 完成 |
| Batch 1 | 100 | min-bugs=10, stars≥100, bugs≤500 | 主要卡源 | ✅ 完成 |
| Batch 2 | 150 | 同上 | LLM 补跑 | ✅ 完成（Stage 1 output 已丢失）|
| Batch 3 | 200 | min-bugs=5 | LLM 补跑 | ✅ 完成（Stage 1 output 已丢失）|
| Batch 4 | 200 | min-bugs=5 | 扩量 | ✅ 完成 |
| Batch 5-8 | 补扫+修正 | 加强前置过滤 | 补量 | ✅ 完成（711 候选全部扫完）|
| **Batch 1-8 合计** | 229 项目 | | **832 张** | 已执行 |
| Batch 9 | 445 项目 | 跳过预过滤，从 944 重新扫 | **2,541 张** | ✅ 入库，待执行 |

## 三、Batch 1-8 执行结果（results/ 统计）

| 指标 | 数值 | 说明 |
|------|------|------|
| result JSON 总数 | 873 | 含 41 个可能的重跑 |
| completed | 430（49.3%） | |
| failed | 441（50.5%） | 其中 98% 为 deploy_failed |
| 其他（done/空） | 2 | |

### mano-cua 判定（430 completed）

| 判定 | 数量 | 占比 |
|------|------|------|
| abnormal（发现 bug） | 224 | 52.1% |
| normal（未发现） | 114 | 26.5% |
| unclear（无法判断） | 92 | 21.4% |

**有效发现率**：832 → 430 completed → 224 abnormal = **26.9%**

### deploy_failed 根因（432 张）

| 原因 | 数量 | 占比 |
|------|------|------|
| 需要后端/数据库 | 138 | 31.9% |
| 版本/依赖兼容性 | 72 | 16.7% |
| monorepo/特殊包管理 | 37 | 8.6% |
| OOM/内存不足 | 27 | 6.2% |
| 其他（API 密钥/npm 等） | 158 | 36.6% |

### backend_risk 标记效果

| 分组 | 卡数 | 失败率 |
|------|------|--------|
| backend_risk=True | 263 | **82.9%** |
| 无 backend_risk | 567 | **37.2%** |

> Batch 1-8 有 264 张 backend_risk=True（31.8%），排产时未使用该标记。如排产前跳过，部署失败率可从 50.5% 降至约 37%。Batch 9 仅 39 张 backend_risk=True（1.5%）。

### 各 Worker 产出

| Worker | 总结果 | completed | 完成率 |
|--------|--------|-----------|--------|
| worker-01 | 75 | 30 | 40.0% |
| worker-02 | 127 | 66 | 52.0% |
| worker-03 | 98 | 56 | 57.1% |
| worker-04 | 49 | 28 | 57.1% |
| worker-05 | 82 | 55 | 67.1% |
| worker-06 | 80 | 38 | 47.5% |
| worker-07 | 68 | 22 | 32.4% |
| worker-08 | 101 | 44 | 43.6% |
| worker-09 | 129 | 58 | 45.0% |
| worker-fabrice | 64 | 33 | 51.6% |

## 四、整合评估（reports/integrated-assessment/）

| 评级 | 含义 | 数量 | 占比 |
|------|------|------|------|
| ✅ A级 | 可交付 | 709 | 81.2% |
| 🟡 B级 | 有瑕疵 | 123 | 14.1% |
| 🔴 C级 | 需修复 | 20 | 2.3% |
| ⚫ D级 | 无轨迹 | 21 | 2.4% |

## 五、框架分布（Batch 1-9 合并）

| 框架 | Batch 1-8 | Batch 9 | 合并 | 合并占比（已分类） | 生态参考 | 偏差 |
|------|----------|---------|------|------|------|------|
| React | 158（19.0%）| 893（35.1%）| 1,051 | 43.7% | ~40% | +3.7pp ✅ |
| Vue | 103（12.4%）| 363（14.3%）| 466 | 19.4% | ~15% | +4.4pp ✅ |
| Angular | 55（6.6%）| 272（10.7%）| 327 | 13.6% | ~12% | +1.6pp ✅ |
| Svelte | 63（7.6%）| 135（5.3%）| 198 | 8.2% | ~5% | +3.2pp ✅ |
| Next.js | 44（5.3%）| 142（5.6%）| 186 | 7.7% | ~15% | -7.3pp ⚠️ |
| Nuxt | 39（4.7%）| 140（5.5%）| 179 | 7.4% | ~5% | +2.4pp ✅ |

> Batch 1-8 的 FRAMEWORK_KEYWORDS 中 `orm` 子串匹配误杀了含 form/platform/formatter 的纯前端项目（React 占被误杀项目的 43.8%）。Batch 9 跳过预过滤，已修正此偏差。
>
> 合并后六大框架中五个偏差在 ±5pp 内。唯一残留偏差是 Next.js 偏低 7pp（SSR 项目后端依赖多，被 backend_risk 拦截比例高）。
>
> Batch 1-8 React 实际占比 19.0%（含 unknown 中 react-bootstrap 等重标注 73 张），raw 字段仅 10.2%（53.7% 标为 unknown）。

## 六、已知问题与待办

| 项 | 状态 | 说明 |
|---|---|---|
| 交付 CSV 给 FTY | ⏸ 待定 | 需先与 FTY 确认当前所需字段 |
| Batch 1-8 unknown 卡框架补标注 | ⏸ 待定 | 345 张 unknown 待补跑框架检测 |
| Next.js 偏低 | 📋 已知 | 如 FTY 关注 SSR 场景，后续定向补充 |
| Batch 9 排产优化 | 📋 Pichai | backend_risk=True 默认不排产 + 同 repo 连续 2 张 deploy_failed 暂停 |

---

*统计口径说明：*
- *卡量 = tasks/pool/*.json 文件数*
- *项目数 = pool/ 内去重 repo 数*
- *执行结果 = results/worker-*/*.json 文件数*
- *框架分布中 Batch 1-8 React 含 CRA(32) + 重标注 unknown(73)*
- *所有百分比基于对应分母四舍五入至一位小数*
