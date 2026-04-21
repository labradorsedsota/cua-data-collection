# BugHunt — CUA 轨迹数据采集（开源 Bug 复现方案）

## 一、项目定位

**项目代号：** BugHunt

**一句话目标：** 从 GitHub 开源项目的已修复 UI Bug 中大规模采集 mano-cua 操作轨迹数据，用于 CUA 模型训练和评测。

**核心逻辑：** 已修复的 Bug = ground truth（已知答案的考试）。checkout 到修复前的 buggy 版本 → 部署 → mano-cua 盲测 → 记录操作轨迹 + 是否命中 Bug。

**数据需求方：** 老傅（FTY），CUA 模型负责人。

### 与自研应用方案的区别

CUA 轨迹数据的采集有两条路径：

| 维度 | 自研应用方案（之前在做的） | 开源 Bug 复现方案（本项目） |
|------|------------------------|--------------------------|
| 应用来源 | 自己从需求到开发到部署 | GitHub 开源项目直接拿来用 |
| 测试用例来源 | 自己编写 test case | 从已修复的 Bug Issue 中提取功能点 |
| Ground Truth | 无（需要人工判断） | 有（fix PR = 答案） |
| 规模化速度 | 慢（每个应用都要走完整流程） | 快（筛选 + 部署即可批量跑） |
| 数据多样性 | 受限于自研应用的类型 | 覆盖各种技术栈、组件类型、Bug 类型 |
| 终点 | 相同：mano-cua 操作轨迹数据 | 相同 |

两条路径互补，不是替代关系。本项目聚焦开源 Bug 复现方案。

---

## 二、全链路流程

```
① 筛选项目
   GitHub 搜索 → 按标准过滤 → 确认可部署
        ↓
② 筛选 Bug
   遍历项目的 closed bug PR → 过滤出 GUI 可观测的
        ↓
③ 部署 buggy 版本
   定位 fix PR → 取 parent commit → checkout/下载 → 本地部署
        ↓
④ 构造测试任务
   基于 Bug 对应的功能点，用中文描述要验证的内容（不暴露 Bug）
        ↓
⑤ mano-cua 执行测试
   运行任务 → 采集完整轨迹
        ↓
⑥ 记录结果
   项目名称 | 测试内容 | sess-id | 是否复现
```

### 筛选标准（老傅已确认）

**选项目（3 条，来自 FTY）：**

| # | 标准 | 说明 |
|---|------|------|
| 1 | Mac 上能直接跑起来 | clone → 简单命令 → 浏览器可访问，不限纯前端 |
| 2 | UI Bug 的 PR 足够多 | 单个项目能批量产出数据，优于零散小项目 |
| 3 | 测试用例多、组件丰富 | 表单/表格/导航/弹窗/轮播/侧边栏等多类型覆盖 |

**管线自动筛选参数（2026-04-15 更新）：**

| 参数 | 值 | 说明 |
|------|------|------|
| deploy | Easy（有 dev 脚本） | Mac 可直接跑 |
| bugs | ≥5 且 ≤500 | 有足够 bug 但不是超大 mono repo |
| stars | ≥100 | 项目质量下限 |
| ui_score | ≥2 | 正向词 82 个 - 排除词 32 个，截图+5 |
| PR changed_files | ≤10 | 排除大重构类 PR |
| 框架/库排除 | Stars > 50K 排除 | 超大 repo 几乎都是框架/平台，非可测试应用 |
| 框架/库排除 | 已知名单 16 个 | angular/angular, preactjs/preact, TanStack/query 等 |
| 框架/库排除 | 描述关键词 17 个 | framework/compiler/runtime/state management 等 |
| 后端依赖排除 | 黑名单检测 | home-assistant-js-websocket, docker-compose 等 |
| 候选池 | **711 个项目** | 944 → FRAMEWORK_REPOS(-30) → FRAMEWORK_KEYWORDS(-198) → stars>50K(-5)（来源：phase2_results.jsonl 实跑，2026-04-20 确认）|
| 前置过滤拦截 | ~200 个项目 | 后端依赖/桌面应用（electron/express/django 等）|
| 实际可产卡项目 | ~674 个 | Batch 1-9 合计产卡项目（来源：tasks/pool/ 去重 repo count）|
| 线上总量 | **3,373 张卡** | Batch 1-8: 832 + Batch 9: 2,541（来源：ls tasks/pool/*.json \| wc -l, 2026-04-21）|

> ⚠️ **FRAMEWORK_KEYWORDS 子串匹配问题（2026-04-21 确认）**：Batch 1-8 使用的 FRAMEWORK_KEYWORDS 列表中包含 `orm`（原意过滤 ORM 框架），但因子串匹配导致 `form`、`platform`、`formatter`、`transformer` 等描述中含 `orm` 的项目被误杀。Batch 9 跳过了预过滤步骤，不受此影响。详见下方 6.5 节分析。

**任务卡描述规范（2026-04-15 更新）：**

| 规范 | 说明 |
|------|------|
| test_page 提取 | Level A: 从 issue body 正则提取 URL 路径（覆盖约 10-15%） |
| 反逃逸约束 | Level B: test_page="/" 时自动追加「始终在浏览器内操作，禁止打开 Terminal，找不到报 unclear」 |
| deploy_commands | 强制 npm run dev（不用 dist 部署） |
| 端口推断 | 从框架自动检测（next→3000, vite→5173, cra→3000, angular→4200） |
| app_name | 从 package.json name 字段自动填充 |

**选 Bug（3 条）：**

| # | 标准 | 说明 |
|---|------|------|
| 4 | GUI 可观测 | 排除纯后端/性能/并发类，保留所有 UI 可见异常 |
| 5 | 不排除动态类 | 动画跳动、过渡异常等都算在内 |
| 6 | Fix commit 可追溯 | 能定位到修复前的代码版本 |

### 执行规范

| 项 | 规范 |
|----|------|
| 任务描述语言 | **中文** |
| 任务描述内容 | 只描述要验证的功能点，**不暴露 Bug 本身** |
| 轨迹要求 | 完整（非中途中断） |
| 评测流程 | 完整（从打开页面到结论） |
| 产出格式 | `项目名称 \| 测试内容 \| sess-id \| 观测结果(abnormal/normal/unclear)` |

### 任务卡格式（JSON）

智子产出、Pichai 分发。每个任务卡包含以下字段：

```json
{
  "task_id": "luxesite-253",
  "repo": "ivegamsft/luxesite",
  "repo_url": "https://github.com/ivegamsft/luxesite",
  "buggy_commit": "39a6e117de7046abb5cd2d5d1ed62547138be8f1",
  "deploy_commands": ["npm install", "npm run dev"],
  "deploy_verify": {
    "method": "curl",
    "check": "curl -s -o /dev/null -w '%{http_code}' http://localhost:3000",
    "expect": "200",
    "timeout_seconds": 120
  },
  "app_name": "Aurora Luxe",
  "dev_url": "http://localhost:3000",
  "test_page": "/",
  "test_description_zh": "滚动到推荐评价区域，点击翻页按钮逐页浏览，检查切换过程是否正常流畅。",
  "expected_result_zh": "点击翻页按钮后，评价卡片应平滑过渡到下一组，无跳动或闪烁",
  "framework": "nextjs",
  "timeout": {"max_steps": 100, "max_minutes": 15},
  "ground_truth": {
    "bug_issue": "#253",
    "bug_description": "404页面缺返回首页链接",
    "visibility": "仅限智子+Pichai，不发给执行agent"
  }
}
```

**字段说明：**
- `task_id`：命名规则为 `{repo短名}-{issue号}`（如 `luxesite-253`），全局唯一，由智子统一分配
- `app_name`：应用名称，用于拼接 mano-cua 任务描述
- `deploy_verify`：结构化部署验证，执行 agent 确认服务跑起来后再开测
- `test_page`：Chrome 打开的初始页面路由
- `test_description_zh`：具体在哪个页面操作，由智子在描述中包含
- `expected_result_zh`：**可选增强**，描述功能的正确行为（从 issue/fix commit 提取），供 mano-cua `--expected-result` 参数使用。evaluation 数据沉淀备用，4/28 前不进训练集（FTY 2026-04-14 确认）。该参数导致 mano-cua 报错时去掉重跑，不阻塞采集
- `ground_truth`：仅供智子+Pichai 比对，**不下发给执行 agent**
- 重试结果文件加后缀区分：`luxesite-253-retry1.json`

### mano-cua 测试执行规范（SOP）

> 详细 SOP 见 [`worker-execution-guide.md`](worker-execution-guide.md)（Pichai 维护）。以下为概要。

**三阶段执行：**
1. **启动前**：部署验证（curl 200）→ Chrome 打开目标页面 → 窗口最大化
2. **执行中**：拼接任务描述执行 mano-cua → 首步 URL 校验 → 双层超时（软 10min / 硬 15min）
3. **完成后**：提取 sess-id → 日志完整性确认（行数>20、含 Session ID）→ 复现判定（必须引用观测事实）→ 关闭测试标签页

**关键规则：**
- 任务描述拼接：`"当前Chrome浏览器已打开{app_name}网站，地址是{dev_url}。{test_description_zh}"`
- `--expected-result` 为可选增强参数，报错时去掉重跑
- `test_page` 只用于 Chrome 打开初始页面，不拼进任务描述
- 关闭标签页时 matchPath 用 `"localhost"`（不限端口，不同项目端口不同）
- BLOCKED 必须附诊断（现象 + 根因 + ≥2 方案）

---

## 三、角色分工

| 角色 | 负责人 | 职责 |
|------|--------|------|
| **数据需求方** | 老傅（FTY） | 定义筛选标准、数据质量标准、验收产出 |
| **决策层** | Emily | 资源协调、方向把控 |
| **项目管理** | Pichai | 任务分发、进度汇总、质量把控、异常升级 |
| **筛选 & 任务设计** | 智子（consultant_bot） | 项目筛选、Bug 筛选、测试任务描述编写、先导验证 |
| **执行 Agent × N** | 待分配 | 部署 buggy 版本 + 执行 mano-cua 测试 + 上报结果 |

---

## 四、任务编排

### 4.1 六步流程分析

| 步骤 | 内容 | 需要 Mac mini？ | 需要 AI 判断力？ | 可提前准备？ |
|------|------|:-:|:-:|:-:|
| ① 筛选项目 | GitHub 搜索 → 过滤 → 确认可部署 | ❌ | ✅ 高 | ✅ |
| ② 筛选 Bug | 遍历 closed PR → 过滤 GUI 可观测的 | ❌ | ✅ 高 | ✅ |
| ③ 部署 buggy 版本 | clone → checkout → install → 启动服务 | ✅ | ⚠️ 看情况 | ❌ |
| ④ 构造测试任务 | 根据 Bug 功能点写中文描述 | ❌ | ✅ 高 | ✅ |
| ⑤ 执行 mano-cua | 传入 URL + 描述 → mano-cua 跑 | ✅ | ❌ 机械 | ❌ |
| ⑥ 记录结果 | 收集 sess-id、是否复现 → 上报 | ✅ | ❌ 机械 | ❌ |

**关键发现：** 前半段（①②④）和后半段（③⑤⑥）天然分离：
- **①②④ 不需要 Mac mini，需要 AI 判断力，可以提前做**
- **③⑤⑥ 必须在 Mac mini 上，且⑤⑥是纯机械操作**

唯一的"灰色地带"是 **③ 部署**：它必须在 Mac mini 上做，但如果遇到依赖报错、环境不兼容，就需要排查能力。这是选择智能 Worker（方案 A，全部装 OpenClaw）的核心原因——Worker 自身有排错能力，部署失败不会卡住等人。

### 4.2 编排方案

```
┌─ 准备阶段（周一~周三）─────────────────────────────┐
│                                                    │
│  智子：①筛选项目 → ②筛选Bug → ④写测试任务描述     │
│        ↓                                           │
│  智子：在现有机器上预验证部署命令（降低踩坑率）      │
│        ↓                                           │
│  产出：完整任务包                                   │
│        ↓                                           │
│  PM：审核任务包质量                                 │
│                                                    │
│  ── 同步进行 ──                                    │
│                                                    │
│  周二：用现有 bot 端到端跑通全流程                   │
│  周三：新机器到货 → 装机 → 验收                     │
│                                                    │
└────────────────────────────────────────────────────┘

┌─ 执行阶段（周四~周日）─────────────────────────────┐
│                                                    │
│  PM 分发任务包给 10 个 Worker                       │
│        ↓                                           │
│  Worker（智能，有 OpenClaw）：                       │
│    ③ 部署 buggy 版本                               │
│      → 正常：继续                                   │
│      → 失败：自行排查，连续失败3次 → 上报PM，跳过   │
│    ⑤ 执行 mano-cua                                 │
│      → 正常：继续                                   │
│      → 超时/崩溃：重试1次，仍失败 → 记录异常，跳过  │
│    ⑥ 上报结果                                      │
│        ↓                                           │
│  PM：实时监控 + 半日报（12:00 / 18:00）             │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 4.3 角色与步骤对应

| 步骤 | 负责人 | 阶段 | 说明 |
|------|--------|------|------|
| ① 筛选项目 | 智子 | 准备阶段 | 周一~周三提前完成 |
| ② 筛选 Bug | 智子 | 准备阶段 | 和①连续完成 |
| ④ 构造测试任务 | 智子 | 准备阶段 | 和②连续完成，产出任务包 |
| 任务包审核 | PM（Pichai） | 准备阶段 | 抽检质量，确认不暴露 Bug |
| 预验证部署 | 智子 | 准备阶段 | POC 阶段已完成 5 个项目验证，批量执行改为排产侧过滤（backend_risk）|
| ③ 部署 buggy 版本 | Worker | 执行阶段 | 在 Mac mini 上，失败可自行排查 |
| ⑤ 执行 mano-cua | Worker | 执行阶段 | 机械执行 |
| ⑥ 记录结果上报 | Worker | 执行阶段 | 按格式上报 PM |
| 实时监控 + 半日报 | PM（Pichai） | 执行阶段 | 异常发现 + 进度汇总 |

---

## 五、质量控制

### 5.1 数据质量标准

| 维度 | 标准 |
|------|------|
| 轨迹完整性 | mano-cua session 正常结束（非中断/超时） |
| 任务描述质量 | 中文、不暴露 bug、只描述要验证的功能点 |
| 复现判定 | Worker 标注观测结果：`abnormal`（观测到异常）/ `normal`（看起来正常）/ `unclear`（无法判断）。**必须引用至少一条具体观测事实**。L2 阶段映射为 FTY 交付术语（abnormal→复现 / unclear→部分复现 / normal→无法复现） |
| 产出格式 | 项目名称 \| 测试内容 \| sess-id \| 观测结果（abnormal/normal/unclear） |

### 5.2 质量保障（实际执行方案）

> 原设计为三层人工闸门（L1 格式检查 → L2 人工抽检 → L3 FTY 终审）。实际执行中 L1/L2 被自动化替代，效率更高：

| 层级 | 原设计 | 实际执行 | 工具 |
|------|--------|---------|------|
| **L1 合规检查** | Pichai 人工 100% 格式检查 | 自动化全量扫描 | `scripts/check-compliance.py` |
| **L2 轨迹匹配** | 智子人工抽检 50%→20% | LLM 全量自动判定（match/mismatch/partial） | claude-haiku-4-5 批量推理 |
| **整合评估** | — | 合规 + 轨迹匹配 + 去重 → ABCD 四级评定 | `reports/integrated-assessment/` |
| **L3 FTY 终审** | 按需 | 待执行（FTY 尚未正式验收） | — |

**整合评估结果（873 张卡）：** A 级 709（81.2%）/ B 级 123（14.1%）/ C 级 20（2.3%）/ D 级 21（2.4%）

### 5.3 异常监控（实际执行方案）

> 原设计为 PM 每天半日报（12:00/18:00）。实际改为 cron 自动巡检，频率更高、异常发现更及时。

**巡检机制（每 15 分钟）：**
1. Worker 失联检测——最后信号超 20 分钟 → 1v1 群询问
2. 连续失败——同一 Worker 连续 3 个 failed → 暂停 + 要求诊断
3. 速率预警——实际完成速率 < 目标 80% → 广播群预警
4. 质量预警——unclear 占比 > 30% → 抽查原因

详见 `patrol-plan.md`、`patrol-lessons.md`

### 5.4 错误处理规则（实际执行方案）

| 场景 | 处理方式 |
|------|----------|
| 部署失败 | Worker 自行排查一次（改端口、重装依赖），仍失败 → 整项目标 `deploy_failed`，全部卡跳过 |
| 需要数据库/认证/OAuth | 立即标 `deploy_failed`，不花时间绕过 |
| mano-cua 软超时（>10 分钟） | 标 WARN，继续等待 |
| mano-cua 硬超时（>15 分钟） | 强制终止（`mano-cua stop`），标 failed |
| mano-cua 异常退出 | 重试 1 次，仍失败则记录异常跳过 |
| 首步 URL 偏离 | 终止重启，连续 3 次 → 标 failed |
| 同一个 bug 重试 | 结果文件加后缀（如 `luxesite-253-retry1.json`） |

> 原设计中「同项目连续 3 个 case 部署失败 → PROJECT_BLOCKED + 强制诊断」在实际执行中未触发。原因：部署是项目级判定，一次失败即整项目所有卡失败，不存在「连续 3 个 case」的场景。

**BLOCKED 强制诊断（可选升级路径）：** 仅适用于部署成功但 mano-cua 反复异常的场景（如 URL 持续偏离、连续超时）。标记 BLOCKED 时建议附：
1. 失败现象 — 具体报错信息或截图
2. 根因判断 — 初步分析原因
3. 建议方案 — 推荐处理方式

BLOCKED 后立即通知 PM，PM 决定是否升级或调整任务分配。

---

## 六、先导实验（智子已完成）

| 项目名称 | Bug Issue | 测试内容 | sess-id | 是否复现 |
|---------|-----------|---------|---------|---------|
| ivegamsft/luxesite | #258 | 轮播区域翻页切换是否流畅 | sess-20260413125759-a8c220d54e9b4f3fbe6d1613c2564e11 | ⚠️ 部分复现 |
| ivegamsft/luxesite | #253 | 404 页面功能是否完善、能否返回首页 | sess-20260413144132-473fa240e8df45f7ad94571d27c138d0 | ✅ 复现 |

**先导结论：**
- 全链路可行：GitHub 搜索 → checkout buggy → 部署 → CUA 测试 → 产出 sess-id ✅
- 功能缺失类 Bug 命中率高，轨迹清晰
- 动态过程类 Bug 可检测但不如静态 Bug 直观

---

## 6.5 项目筛选方法论与进度（智子负责）

### 自动化筛选管线

```
Phase 1: 广搜（已完成）
  70 组 GitHub 搜索查询 × 30+ 应用品类
  → 9,542 个候选 repo（去重后）

Phase 2: 精筛（已完成）
  Web 语言过滤（TS/JS/Vue/Svelte/HTML/Dart）→ 7,066 个
  ↓ 逐个检查
  ├── package.json 可部署性（有 dev/start 脚本、无重型依赖）→ Easy 3,884
  ├── Stars ≥100 → 2,702
  ├── Bugs 5-500 → 944（来源：phase2_results.jsonl 实跑，2026-04-20 确认）
  ├── FRAMEWORK_REPOS 黑名单 → -30 → 914
  ├── FRAMEWORK_KEYWORDS 描述匹配 → -198 → 716
  └── Stars >50K → -5 → 711
  ↓
  最终产出：Batch 1-8 从 711 中产卡，Batch 9 从原始 944 中产卡（跳过预过滤）
```

### 当前进度（2026-04-17 17:00 更新）

| 阶段 | 进度 | 数据 |
|------|------|------|
| Phase 1 广搜 | ✅ 完成 | 9,542 → 7,066（Web 语言过滤）|
| Phase 2 粗筛 | ✅ 完成 | 7,066 → Easy 3,884 → stars≥100: 2,702 → bugs 5-500: **944** → FRAMEWORK_REPOS: 914 → FRAMEWORK_KEYWORDS: 716 → stars>50K: **711**（phase2_results.jsonl 实跑）|
| 框架/库过滤 | ✅ 完成 | 三层过滤：已知框架名单 + 描述关键词 + Stars>50K |
| 后端依赖前置过滤 | ✅ 完成 | BACKEND_DEP_BLACKLIST 扩充（django/flask/rails/frappe/electron 等）|
| Bug 级精筛脚本 | ✅ 完成 | `bug_screener.py` + `batch_card_generator.py`，关键词已优化 |
| POC 任务卡 | ✅ 完成 | 25 张卡（5 项目），已 push |
| Batch 1（100 项目）| ✅ 完成 | Stage 1 唯一跑完的批次，产出主要卡源 |
| Batch 2-3（LLM 补跑）| ✅ 完成 | 参数调整 + LLM 描述补跑 |
| Batch 4（200 项目，min-bugs=5）| ✅ 完成 | 扩量批次 |
| **线上总量** | **3,373 张卡** | **674 个项目**（Batch 1-8: 832/229 + Batch 9: 2,541/445，来源：tasks/pool/ count, 2026-04-21）|

### 执行进度（2026-04-17 17:00）

| 指标 | 数值 | 说明 |
|------|------|------|
| 总卡量 | 3,373 | Batch 1-8: 832 + Batch 9: 2,541（pool/ count, 2026-04-21）|
| Batch 1-8 已执行 | 873 | results/ JSON count，含 41 个重跑 |
| 其中 completed | 430 | 49.3% |
| 其中 failed | 441 | 50.5%（其中 98% 为 deploy_failed）|
| Batch 9 待执行 | 2,541 | 尚未开始 |
| 执行 Worker | 10 | worker-01~09 + Fabrice |

> ⚠️ **历史数据纠正（2026-04-16 发现，2026-04-20 实跑确认）**：之前报的「869 候选、扫了 450 个（60%）」为错误数据。869 来自早期子集 `final_candidates.jsonl`，450 来自 Batch 1-3 的 max-repos 参数之和（非去重实际值）。实际候选池经实跑确认为 944（bugs 5-500）→ 711（框架过滤后）。Batch 1-8 产卡来自 711 中的 229 个项目，Batch 9 从原始 944 中重新扫描产卡（跳过预过滤）。
>
> **教训**：凡是量级判断，必须用生产脚本实跑验证，不能自己另起近似计算。

### 数据源真实漏斗（经脚本实跑验证）

```
Phase 1 原始搜索          9,542 个 repo
Phase 2 全量              7,066 个 repo
  ↓ deploy=easy            3,884
  ↓ stars≥100              2,702
  ↓ bugs 5-500               944  ← 实跑确认（phase2_results.jsonl, 2026-04-20）
  ↓ FRAMEWORK_REPOS          -30 → 914
  ↓ FRAMEWORK_KEYWORDS      -198 → 716
  ↓ stars>50K                 -5 → 711
  ↓
  Batch 1-8 从 711 中产卡    229 个项目 / 832 张卡
  Batch 9 从 944 中产卡      445 个项目 / 2,541 张卡（跳过预过滤）
  ═══════════════════
  合计                     674 个项目 / 3,373 张卡
```

### 正式筛选参数（FTY 2026-04-14 22:00 确认）

**项目级筛选：**

| 参数 | 值 | 说明 |
|------|------|------|
| 部署难度 | Easy | 有 dev 脚本，`npm run dev` 可启动 |
| 最低 bugs | ≥5 | 恢复原参数，扩大池子 |
| 最低 stars | ≥100 | 保证项目质量和 issue 规范度 |
| 最大 bugs | ≤500 | 跳过超大 repo，节省 API 配额 |
| 非 GUI 过滤 | 是 | 剥离 API/CLI/后端框架类项目（~20%） |

→ **944 个候选项目**（phase2_results.jsonl 实跑，经 FRAMEWORK 过滤后 711）

**Bug 级筛选：**

| 参数 | 值 | 说明 |
|------|------|------|
| issue 状态 | closed + label:bug | 已修复的 bug |
| PR 关联 | 有 merged PR | 通过 closes/fixes #xxx 匹配 |
| PR 改动文件数 | ≤10 | 单一 bug，checkout 干净 |
| UI 可观测性 | ui_score ≥2 | 正向词(82个) - 排除词(32个)，截图+5分 |
| 测试页面 | 按需指定 | 子页面功能类bug需指定 test_page，首页类保持 / |

**UI 关键词概要（v2.4 优化后）：**
- 英文正向词 57 个：display/style/button/click/modal/table/tab/sidebar/toast/carousel/upload/drag/...
- 中文正向词 25 个：显示/样式/按钮/圆角/边框/悬停/暗色/深色/主题/导航/侧边栏/轮播/卡片/...
- 排除词 32 个：docker/api/backend/performance/compile/dependency/security/migration/...
- 截图加分：+5分

### 产量预估（2026-04-17 基于实测数据修正）

| 步骤 | 数量 | 说明 |
|------|------|------|
| 候选项目池 | 944 | phase2_results.jsonl 实跑确认（bugs 5-500, stars≥100, deploy=easy）|
| Batch 1-8 预过滤后 | 711 | FRAMEWORK_REPOS + KEYWORDS + stars>50K |
| Batch 1-8 已产卡 | 229 个项目 / 832 张 | 含 POC 25 张 |
| Batch 9 产卡（跳过预过滤）| 445 个项目 / 2,541 张 | 从 944 中去除已有项目后产卡 |
| **合计** | **674 个项目 / 3,373 张卡** | tasks/pool/ count, 2026-04-21 |

> ℹ️ 剩余项目集中在 bugs 5-49 区间，LLM 通过率可能低于前几批（高 bug 项目已扫完）。Batch 6 实测通过率较低（高 bug 大型项目后端依赖占比高），后续 Batch 以中小项目为主，预计更健康。

### 管线关键修正（2026-04-15）

| 修正项 | 原值 | 新值 | 原因 |
|--------|------|------|------|
| 级联跳过逻辑 | 1 张拒绝就跳过整个项目 | 需 2 张都拒绝才跳过 | 避免误杀可测项目（实测后确认被拒项目确实不可测）|
| LLM max-cards | 50 | 500 | 原默认值导致大量候选未处理 |
| ui_score 门槛 | ≥8 | ≥3 | 扩大候选覆盖 |
| TPL 卡计入 | 是 | 否 | TPL 卡无实质描述，不计入有效产出 |
| 后端依赖过滤 | 基础名单 | 扩充名单（+django/flask/rails/frappe/electron） | Batch 2+3 拦截 100+ 后端/桌面项目 |

### 各批次执行记录

| 批次 | 扫描项目 | 参数 | 实际状态 |
|------|---------|------|----------|
| POC | 5 个项目 | Easy + Medium 对照 | ✅ 25 张卡 |
| Batch 1 | 100 个项目 | min-bugs=10, stars≥100 | ✅ Stage 1 唯一完整批次，主要卡源 |
| Batch 2 | 150 个项目 | 同上 | ✅ LLM 补跑完成（Stage 1 output 已丢失）|
| Batch 3 | 200 个项目 | min-bugs=5 | ✅ LLM 补跑完成（Stage 1 output 已丢失）|
| Batch 4 | 200 个项目 | min-bugs=5 | ✅ 扩量完成 |
| **Batch 1-4 合计** | | | **771 张卡 / 223 个项目** |
| Batch 5 | 补量 | 同上 | ✅ 合并入后续批次 |
| Batch 6 | 100 个项目 | bugs 高→低排序 | ✅ 完成（发现高 bug 项目后端依赖占比高）|
| Batch 7 | Stage 1 补扫 | 加强 description 前置过滤 | ✅ 完成 |
| Batch 8 | 最后一批预过滤候选 | 同上 | ✅ 完成（711 候选全部扫完）|
| **Batch 1-8 合计** | 229 个项目 | | **832 张卡**（含 POC 25）|
| Batch 9 | 445 个项目 | 跳过预过滤，从 944 中重新扫描 | ✅ 入库完成，**2,541 张卡**，待执行 |
| **Batch 1-9 合计** | **674 个项目** | | **3,373 张卡** |

> ⚠️ Batch 1-8 使用 FRAMEWORK_KEYWORDS 预过滤（候选池 711），其中 `orm` 子串匹配误杀了含 form/platform/formatter 的纯前端项目。Batch 9 跳过预过滤步骤，从原始 944 中重新扫描，补回了被误杀项目。详见上方框架分布分析。

---

## 6.6 协作与交付流程

### 任务流转

```
智子 push 任务卡到 tasks/pool/
        ↓
Pichai pull → pool-clean/ 去除 ground_truth → dispatch-log 记录派发 → Worker 执行 → results/worker-xx/ 提交
        ↓
Worker 执行（部署 → mano-cua → 结果）
        ↓
Worker 将结果 JSON 写入本地 results/{worker名}/{task_id}.json
        ↓
Worker 在执行群发状态信号（✅/❌/⚠️）
        ↓
Pichai 收集结果 → push 到 repo results/ 目录
        ↓
智子 L2 抽检（初期 50%，稳定后 20-30%）
        ↓
FTY L3 按需终审
```

### Repo 目录结构

```
bughunt/
├── README.md                    # 项目全景文档（唯一权威源）
├── SUMMARY.md                   # Batch 1-9 全景与执行结果摘要
├── PENDING.md                   # 归档：历史待确认事项
├── POC-REPORT.md               # POC 阶段报告
├── patrol-plan.md               # 巡检方案
├── patrol-lessons.md            # 巡检教训
├── data/
│   ├── candidates.jsonl         # Phase 1 广搜（13,207 条）
│   ├── phase2_results.jsonl     # Phase 2 精筛（7,066 条）
│   ├── batch9_tasks.jsonl       # Batch 9 Stage 1 原始输出
│   ├── batch9_tasks.jsonl.final # Batch 9 最终版（2,541 张）
│   ├── batch9_manifest.json     # Batch 9 清单
│   └── archive/                 # 中间过程文件归档
├── tasks/
│   ├── pool/                    # 全量任务卡 JSON（智子 push，3,373 张）
│   └── pool-clean/              # 去除 ground_truth 后的派发版（Pichai 管理）
├── results/                     # 执行结果（873 条，Worker push）
│   ├── CHANGELOG.md             # 清洗变更记录
│   ├── worker-01/ ~ worker-09/  # 各 Worker 结果
│   └── worker-fabrice/
├── reports/                     # 报告
│   ├── integrated-assessment/   # 整合评估报告
│   └── worker-audit-*.md        # Worker 审计报告
├── dashboard/                   # 进度看板
│   ├── index.html
│   └── progress.json
├── scripts/                     # 自动化脚本
│   ├── batch9_stage1.py
│   ├── batch9_stage2_llm.py
│   ├── bug_screener.py
│   ├── validate_cards.py
│   ├── verify_pool.py
│   └── archive/                 # 一次性修补脚本
├── worker-config/               # Worker 配置模板
│   ├── worker-execution-guide.md
│   ├── worker-setup.md
│   ├── worker-agents.md
│   ├── worker-soul.md
│   ├── worker-tools.md
│   └── worker-user.md
├── group-md-templates/          # 群聊 GROUP.md 模板
├── logs/                        # mano-cua 执行日志
└── pm-template/                 # PM 巡检模板
```

### 写权限规则

| 目录 | 写权限 | 说明 |
|------|--------|------|
| `tasks/pool/` | 智子 | 任务卡只由智子产出 |
| `tasks/pool-clean/` | Pichai | 去除 ground_truth 后的派发版，Pichai 管理 |
| `results/` | Worker / Pichai | Worker push 执行结果，Pichai 审核 |
| `data/` | 智子 | 筛选数据由智子维护 |
| `reports/` | 智子 | 质量报告、审计报告 |
| `README.md` | 智子（方案层）/ Pichai（执行层）| 改前 pull，改完 push，互相 review |
| `worker-config/` | Pichai（执行文档）/ 智子（方案文档）| 各管各的 section |

### 结果 JSON 格式

Worker 每个 case 完成后产出：

```json
{
  "task_id": "vcal-350",
  "worker": "fabrice",
  "timestamp": "2026-04-14T18:30:00+08:00",
  "deploy": {
    "status": "success",
    "duration_seconds": 45
  },
  "mano_cua": {
    "sess_id": "sess-20260414183045-xxxxx",
    "status": "COMPLETED",
    "total_steps": 17,
    "last_action": "DONE",
    "last_reasoning": "...",
    "duration_seconds": 180
  },
  "result": "abnormal",
  "result_summary": "第 7 步截图中选中日期后无高亮样式变化，连续 3 次点击不同日期均无视觉反馈",
  "log_file": "logs/vcal-350.log",
  "log_lines": 142
}
```

### FTY 交付格式

> ℹ️ **原材料已齐，待 FTY 确认格式后批处理导出。**

result JSON 中已有全部原始数据：

| 字段 | 说明 | 覆盖率 |
|------|------|--------|
| `repo` | 项目名称（如 `uvarov-frontend/vanilla-calendar-pro`） | 100% |
| `mano_cua.result_summary` | mano-cua 的观测描述（中/英文） | 421/430 completed |
| `sess_id` | mano-cua session ID | 430/430 |
| `mano_cua.result` | `abnormal` / `normal` / `unclear` | 430/430 |

**待 FTY 确认：**
1. 是否需要术语映射（abnormal→复现 / unclear→部分复现 / normal→无法复现），还是直接用原始值
2. 交付格式（CSV / JSONL / 其他）
3. 是否需要 `result_summary`
4. 是否需要轨迹文件下载路径/方式（Pichai 补充）
5. 除以上字段外还需要什么

### 状态信号规范

Worker 每个 case 完成后在执行群发一行状态信号：

```
✅ worker-fabrice | vcal-350 | 4m12s          # 正常完成
❌ worker-fabrice | vcal-352 | 2m05s | deploy  # 部署失败
⚠️ BLOCKED worker-moss | ms-511 | 15m | 诊断见群消息  # 需要介入
```

### POC 简化流程（当前生效）

POC 阶段不做 `tasks/pool-clean/` 的文件移动，Pichai 通过 DMWork 消息直接指派。结果 Worker 在群里回报，Pichai 手动收集写入 repo。正式流程待 POC 验证后确定。

---

## 七、待确认事项

### 已明确

| # | 问题 | 结论 | 来源 |
|---|------|------|------|
| 1 | 规模目标 | **近期：采完已制卡的 3,373 张任务。远期：10,000 条轨迹** | 林菡 |
| 2 | 时间节点 | **周四(4/17)~周日(4/20) 完成执行**，之前为 setup 阶段 | 林菡 |
| 3 | 轨迹数据存储 | 云端存储，包含描述文件 + 截图文件，有代码可下载 | 林菡 |
| 4 | Worker 机器 | **10 台新 Mac mini**，预计周三(4/16)到货 | 林菡 |
| 5 | Worker 方案 | **方案 A：每台装 OpenClaw + DMWork 插件 + mano-cua**，智能 Worker 可自主排查部署问题 | 林菡 |

### 待讨论

| # | 问题 | 决策者 | 状态 |
|---|------|--------|------|
| 6 | ~~候选项目列表是否需要老傅确认？~~ | ~~Emily / 老傅~~ | ✅ 已确认：FTY 看过 POC 任务卡，确认筛选逻辑和格式（补充：需指明具体测试页面） |
| 7 | ~~数据有效性标准~~ | ~~老傅~~ | ✅ 已确认：复现状态三级（复现/部分复现/无法复现），部分复现有价值；超时重跑一次，再超时丢弃 |
| 8 | ~~测试任务描述由谁编写？~~ | ~~全员讨论~~ | ✅ 已确认：智子编写（Proposal A 生效）|
| 9 | ~~共享通道~~ | ~~Emily~~ | ✅ 已确认：GitHub repo（bughunt）|
| 10 | `--expected-result` 是否用于训练？ | 老傅 | ✅ 已确认：evaluation 数据有用，4/28 前沉淀备用，优先操作轨迹 |

### Proposal A：测试任务描述编写分工

**建议：智子在筛选 Bug 时一并编写任务描述，打包成完整任务包交给 Worker 直接执行。**

理由：
1. **筛选和描述是同一个阅读过程** — 智子筛选 Bug 时已经看过 Issue 详情、理解了功能点，顺手就能写出任务描述。如果让 Worker 来写，需要重新读一遍 Issue，重复劳动。
2. **"不暴露 Bug"有技巧门槛** — 先导实验中智子已摸出分寸（如 #253 写「检查 404 页面功能是否完善」而非「检查有没有返回链接」）。分散给多个 Worker 各自写，质量可能参差不齐。
3. **Worker 保持纯执行** — 拿到任务包（commit + 部署命令 + 任务描述 + URL）直接跑，不需要理解 Bug，流程最简、出错率最低、可替换性最强。

建议分工：

| 环节 | 负责人 | 产出 |
|------|--------|------|
| 筛选项目 + 筛选 Bug + 编写任务描述 | 智子 | 完整任务包（task list） |
| 抽检任务描述质量 | PM（Pichai） | 确认不暴露 Bug、描述清晰 |
| 部署 + 执行 + 收集结果 | Worker | sess-id + 是否复现 |

> ⚠️ 此为 PM 建议方案，待全员讨论确认。

### Proposal B：汇总与监控机制

#### 产能实绩与目标

> 原推算：10 Worker × 4 天 × 250 条/天 = 10,000 条。假设单 case 5 分钟。
> 实际：Batch 1-8 产出 873 条 result，其中 completed 430。部署失败率 50% + 任务卡不足是主因。
>
> **近期目标**：采完已制卡的 3,373 张任务。**远期目标**：10,000 条轨迹。
> Batch 9 排产优化（backend_risk 过滤 + 同 repo 连续失败暂停）预期可显著提升部署成功率。

#### PM 内部监控（实时）

我会维护一个实时统计文件，每个 Worker 上报结果后立即更新：

```
统计维度：
- 总完成数 / 目标数（进度百分比）
- 每个 Worker 的完成数、成功率、平均耗时
- 异常 case 数（超时/中断/部署失败）
- 复现率（✅ / ⚠️ / ❌ 分布）
- 当前速率 vs 目标速率（是否能按时完成）
```

异常触发规则：
- Worker 连续 30 分钟无产出 → 主动排查
- 单 Worker 超时率 > 30% → 暂停该 Worker，分析原因
- 整体速率低于目标 20% 以上 → 升级到林菡

#### 对外汇报（半日报）

每天 **12:00** 和 **18:00** 各发一次进度报告到群里：

```
📊 BugHunt 进度报告（4/17 午间）
━━━━━━━━━━━━━━━━━━━━━━━
总进度：1,250 / 10,000（12.5%）
今日完成：620 条
活跃 Worker：10/10
复现率：✅ 45% | ⚠️ 20% | ❌ 35%
异常：Worker-3 部署失败 2 次，已恢复
预计完成时间：4/20 16:00（按当前速率）
━━━━━━━━━━━━━━━━━━━━━━━
```

#### Dashboard（如果条件允许）

在 repo 中维护一个 `dashboard.md` 或 `progress.json`，Worker 上报后自动更新，随时可查。如果有 GitHub Pages 可以做成可视化页面。

> ⚠️ 此为 PM 建议方案，待确认。

---

## 八、时间表

### Setup 阶段

| 日期 | 目标 | 具体任务 |
|------|------|---------|
| **周一 4/14** | 方案定稿 | ① 完成项目文档 ② 待讨论事项推动确认 ③ 智子继续筛选项目+Bug+写任务描述 |
| **周二 4/15** | **用现有 bot 跑通全流程** | ① 在现有机器上端到端跑通：任务包 → 部署 → mano-cua 执行 → 结果上报 → PM 汇总 ② 验证超时处理机制 ③ 验证汇报流程 ④ 验证异常 case 兜底策略 ⑤ 记录 Worker 需要的完整配置清单 |
| **周三 4/16** | **装机就绪** | ① 新 Mac mini 到货 ② 按配置清单装机（OpenClaw + DMWork + mano-cua + 环境依赖）③ 每台跑 1 个 case 验收 ④ 任务包定稿，分配到 Worker |

### 执行阶段

| 日期 | 目标 | 具体任务 |
|------|------|---------|
| **周四 4/17** | 正式开跑 | 10 台并行执行，PM 实时监控，午间/晚间半日报 |
| **周五 4/18** | 持续执行 | 同上，根据前一天数据调优（任务分配/超时策略） |
| **周六 4/19** | 持续执行 | 同上 |
| **周日 4/20** | 完成 + 交付 | 收尾 → 最终汇总 → 交付老傅 |

### 周二验证清单（必须全部跑通）

- [ ] **端到端流程**：任务包 → clone → checkout → 部署 → mano-cua 执行 → sess-id 产出 → 结果上报 → PM 汇总
- [ ] **超时处理**：mano-cua 单 case 超时多久算失败？超时后自动 kill？是否重试？重试几次？
- [ ] **部署失败处理**：install 报错 / 服务启动失败时 Worker 怎么做？跳过？自行排查？上报？
- [ ] **汇报流程**：Worker 完成一个 case 后如何上报？格式？发到哪？
- [ ] **任务切换**：同项目多个 Bug 之间如何切换（可能共享部署）？不同项目之间如何切换（需要重新部署）？
- [ ] **Worker 配置清单**：软件版本、环境变量、OpenClaw 配置、SOUL/AGENTS 模板、mano-cua 参数——全部文档化
- [ ] **产能基准**：实测单 case 平均耗时，验证 10 Worker × 4 天能否达成 10,000 条

---

## 九、相关链接

- Repo: https://github.com/labradorsedsota/bughunt
- 群聊「从github找CUA数据」：智子 + 老傅 + Emily + 林菡 + Pichai
- mano-cua 版本：v1.0.6

---

*文档版本：v3.1 | 2026-04-21 | 智子（质量控制改为实际执行方案：L1/L2自动化替代人工、异常监控改cron巡检、错误处理对齐实际流程、BLOCKED降为可选、FTY交付标注待确认、目标拆分近期/远期、产能推算改为实绩）*
*文档版本：v2.5 | 2026-04-14 | 智子（SOP 去重指向 worker-execution-guide.md、matchPath 修正、result 字段保持 abnormal/normal/unclear + L2 映射说明、result_summary 统一字段名）*
*文档版本：v2.4 | 2026-04-14 | 智子（FTY 确认正式筛选参数、产量预估 2,500-2,700、关键词优化 v2.4、周三三批次计划）*
*文档版本：v2.3 | 2026-04-14 | 智子（FTY 数据需求确认 7 项、粗筛完成 1,124 候选、精筛脚本验证、POC 25 张卡、候选池统计、Bug 精筛逻辑、test_page 补充、待决事项关闭）*
*文档版本：v2.2 | 2026-04-14 | Pichai（SOP 升级：窗口最大化、日志 tee、双层超时、首步 URL 校验、BLOCKED 强制诊断、日志完整性、判定引用观测、任务间关标签页、Worker Checklist）*
*文档版本：v2.1 | 2026-04-14 | 智子（新增：expected_result_zh 字段、筛选方法论与进度、待决事项更新）*
*文档版本：v2.0 | 2026-04-13 | Pichai*
