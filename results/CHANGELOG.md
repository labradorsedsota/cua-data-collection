# Results CHANGELOG

## 2026-04-18 12:05 — worker-07 合规修复 2 张结果卡

**操作人：** worker-07（林菡确认）
**原因：** Pichai 合规扫描发现 worker-07 提交的 43 张结果中 2 张不符合 `worker-execution-guide.md` 标准 schema（status 非法值、缺少顶层必填字段、JSON 解析失败）
**审计报告：** `reports/worker-07-audit.md`

**修复分类：**

| 类型 | 数量 | 修复方式 |
|------|------|----------|
| A: 旧格式→completed（重构为标准 schema） | 1 | 从 log 提取 sess_id/status/total_steps/last_action/last_reasoning，重构为标准 completed 格式 |
| B: JSON 控制字符修复 | 1 | 删除 \r (0x0D) 控制字符 |

**修复后 status 分布（43 张）：**

| status | 数量 |
|--------|------|
| completed | 18 |
| failed | 25 |

**影响卡清单（2 张）：**

| # | 文件 | 修复前问题 | 修复后 status | 修复方式 |
|---|------|-----------|---------------|----------|
| 1 | `angular-calendar-1396.json` | 缺少顶层字段 `sess_id`/`expected_result_used`/`duration_seconds`；status 非法值 `tool_error`（应为 completed/failed） | completed (unclear) | 从 log 提取 sess_id=`sess-20260416210830-0e98dd7e18ce46c6a6aa62da2ae829c2`；status 改 `completed`；重构 mano_cua 对象（result=unclear，3次尝试均因点击无响应失败）；补 expected_result_used=true, duration_seconds=1800 |
| 2 | `react-date-picker-110.json` | JSON 解析失败：sess_id 字符串末尾含 `\r` (0x0D) 控制字符（Invalid control character at line 6 column 67） | completed (normal) | 删除 `\r` 控制字符，内容无其他变更 |

共 2 张卡，修复后 43/43 通过合规检查。

---


## 2026-04-18 11:50 — worker-06 合规修复 5 张结果卡

**操作人：** worker-06（林菡确认）
**原因：** Pichai 合规扫描发现 worker-06 提交的 62 张结果中 5 张不符合 `worker-execution-guide.md` 标准 schema（mano_cua.result 非法值、sess_id 缺失）
**审计报告：** `reports/worker-06-audit.md`

**修复分类：**

| 类型 | 数量 | 修复方式 |
|------|------|----------|
| A: completed + result 非法值 → 修正 result 值 | 1 | mano_cua.result 从 `deploy_failed` 改为 `unclear`，更新 result_summary |
| B: completed 但 mano-cua 未执行 → failed | 4 | status 改 failed + 构建完整 failure 对象 + mano_cua 设 null |

**修复后 status 分布（62 张）：**

| status | 数量 |
|--------|------|
| completed | 36 |
| failed | 26 |

**影响卡清单（5 张）：**

| # | 文件 | 修复前问题 | 修复后 status | 修复方式 |
|---|------|-----------|---------------|----------|
| 1 | `SvelteLab-194.json` | mano_cua.result=`deploy_failed`（非法值） | completed (unclear) | result 改 `unclear`；result_summary 更新为"页面空白无法到达目标功能，无法判断bug是否存在" |
| 2 | `mini-qr-59.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式；failure.symptom: zip下载被CANCEL导致损坏；mano_cua 设 null |
| 3 | `monaco-editor-auto-typings-32.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式；failure.symptom: Node 23 ESM导致webpack require未定义；mano_cua 设 null |
| 4 | `svelteui-283.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式；failure.symptom: monorepo install失败(svelte-kit sync报错+yarn SIGKILL)；mano_cua 设 null |
| 5 | `svelteui-297.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式；failure.symptom: 同svelteui-283；mano_cua 设 null |

共 5 张卡，修复后 62/62 通过合规检查。

---


## 2026-04-18 11:45 — worker-04 合规修复 6 张结果卡

**操作人：** worker-04（林菡确认）
**原因：** Pichai 合规扫描发现 worker-04 提交的 55 张结果中 6 张不符合 `worker-execution-guide.md` 标准 schema（字段名错误、缺少顶层必填字段、mano_cua 为 null、status 虚报）
**审计报告：** `reports/worker-04-audit.md`

**修复分类：**

| 类型 | 数量 | 修复方式 |
|------|------|----------|
| A: 旧格式→completed（`session_id`→`sess_id` + 顶层散放→`mano_cua` 嵌套） | 5 | 从 log 提取 sess_id/status/total_steps/last_action/last_reasoning，重构为标准 completed 格式 |
| B: completed 但 mano-cua 未执行→failed | 1 | status 改 failed + 构建完整 failure 对象 + mano_cua 设 null |

**修复后 status 分布（55 张）：**

| status | 数量 |
|--------|------|
| completed | 46 |
| failed | 9 |

**影响卡清单（6 张）：**

| # | 文件 | 修复前问题 | 修复后 status | 修复方式 |
|---|------|-----------|---------------|----------|
| 1 | `react-content-loader-93.json` | 字段名 `session_id` 非标准；缺 `sess_id`/`expected_result_used`/`duration_seconds`；`mano_cua` 为 null（数据散落顶层） | completed (abnormal) | 从 log 提取 sess_id/last_action=DONE/last_reasoning；重构 mano_cua 嵌套对象；expected_result_used=true（日志有 Expected result 行） |
| 2 | `script-lab-609.json` | 同 #1 | completed (unclear) | 从 log 提取 sess_id/last_action/last_reasoning；STOPPED_BY_USER 128步超限；expected_result_used=true |
| 3 | `script-lab-623.json` | 同 #1 | completed (abnormal) | 从 log 提取 sess_id/last_action=DONE/last_reasoning；TS2322 编译错误；expected_result_used=true |
| 4 | `script-lab-648.json` | 同 #1 | completed (abnormal) | 从 log 提取 sess_id/last_action=DONE/last_reasoning；同 623 编译错误；expected_result_used=true |
| 5 | `svelte-tags-input-17.json` | 同 #1 | completed (abnormal) | 从 log 提取 sess_id/last_action/last_reasoning；ERROR 150步超限；mano-cua 通过源码确认 bug；expected_result_used=true |
| 6 | `website-4885.json` | `sess_id` 为 null；status=`completed` 但 mano-cua 未执行（虚报） | failed (deploy_failed) | status 改 failed；构建完整 failure 对象（symptom: Next.js 15 首次编译 >30 分钟页面空白；attempted: 基于同项目 website-4366 实测结果判定）；mano_cua 设 null |

共 6 张卡，修复后 55/55 通过合规检查。

---

## 2026-04-18 11:40 — worker-09 合规修复 29 张结果卡

**操作人：** worker-09（林菡确认）
**原因：** Pichai 合规扫描发现 worker-09 提交的 97 张结果中 29 张不符合 `worker-execution-guide.md` 标准 schema（缺少顶层必填字段、status 非法值 None、failure 为 null、sess_id 缺失）
**审计报告：** `reports/worker-09-audit.md`
**修复脚本：** `scripts/fix-worker09.py`（可复现）

**修复分类：**

| 类型 | 数量 | 修复方式 |
|------|------|----------|
| A: 旧格式→completed（有 log + mano-cua COMPLETED） | 3 | 从 log 提取 sess_id/last_action/last_reasoning，重构为标准 completed 格式 |
| A: 旧格式→failed（mano-cua 未正常完成或未执行） | 4 | 重构为标准 failed 格式，源码分析保留在 recommendation |
| B: failed 但 failure=null（非标准字段名） | 16 | failure_reason/reason/notes/error_detail→标准 failure 对象，补缺失字段 |
| C: completed 但 mano-cua 未执行→failed | 6 | status 改 failed + 构建 failure 对象 + mano_cua 设 null，源码分析保留在 recommendation |

**修复后 status 分布（97 张）：**

| status | 数量 |
|--------|------|
| completed | 65 |
| failed | 32 |

**影响卡清单（29 张）：**

| # | 文件 | 修复前问题 | 修复后 status | 修复方式 |
|---|------|-----------|---------------|----------|
| 1 | `openclaw-nerve-27.json` | status=None, 缺必填字段, 旧格式 | completed (abnormal) | 从 log 提取 last_action=DONE/last_reasoning; sess_id 取最后 COMPLETED session |
| 2 | `shadcn-solid-77.json` | status=None, 缺必填字段, 旧格式 | completed (abnormal) | 从 log 提取 last_action=DONE/last_reasoning; mano-cua COMPLETED 26步 |
| 3 | `shadcn-solid-122.json` | status=None, 缺必填字段, 旧格式 | completed (abnormal) | 从 log 提取 last_action=DONE/last_reasoning; mano-cua COMPLETED 6步 |
| 4 | `Luckysheet-528.json` | status=None, 缺必填字段, 旧格式 | failed (mano_cua_error) | 72步 SIGKILL→failed; 源码分析保留在 symptom/recommendation |
| 5 | `Starkiller-5.json` | status=None, 缺必填字段, 旧格式 | failed (deploy_failed) | 需 Empire C2 后端; 源码分析保留在 recommendation |
| 6 | `Task-Board-608.json` | status=None, 缺必填字段, 旧格式 | failed (deploy_failed) | Obsidian 插件无法浏览器运行; 源码分析保留在 recommendation |
| 7 | `openclaw-nerve-64.json` | status=None, 缺必填字段, 旧格式 | failed (deploy_failed) | STT 后端不可用→deploy_failed; 源码分析保留在 recommendation |
| 8 | `kaneo-1066.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | failure_reason/notes→标准 failure 对象; 补缺失字段 |
| 9 | `kaneo-1081.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #8 |
| 10 | `kaneo-1087.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #8 |
| 11 | `kaneo-1131.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #8 |
| 12 | `kaneo-1140.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #8 |
| 13 | `megadraft-283.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | reason/error_detail→标准 failure 对象; 补缺失字段 |
| 14 | `megadraft-286.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #13 |
| 15 | `megadraft-288.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #13 |
| 16 | `megadraft-302.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #13 |
| 17 | `megadraft-319.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #13 |
| 18 | `megadraft-324.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #13 |
| 19 | `react-hot-toast-10.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #13 |
| 20 | `react-hot-toast-27.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #13 |
| 21 | `react-hot-toast-45.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #13 |
| 22 | `react-hot-toast-50.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #13 |
| 23 | `react-hot-toast-101.json` | failure=null, 缺 sess_id/expected_result_used/duration_seconds | failed (deploy_failed) | 同 #13 |
| 24 | `devtools-598.json` | sess_id=null (completed 但 mano-cua 未执行) | failed (deploy_failed) | completed→failed; 源码分析保留在 recommendation |
| 25 | `maker.js-556.json` | sess_id=null (completed 但 mano-cua 未执行) | failed (deploy_failed) | 同 #24 |
| 26 | `ngx-datatable-1702.json` | sess_id=null (completed 但 mano-cua 未执行) | failed (deploy_failed) | 同 #24 |
| 27 | `ngx-page-scroll-2.json` | sess_id=null (completed 但 mano-cua 未执行) | failed (deploy_failed) | 同 #24 |
| 28 | `react-grid-layout-918.json` | sess_id=null (completed 但 mano-cua 未执行) | failed (deploy_failed) | 同 #24 |
| 29 | `shikwasa-44.json` | sess_id=null (completed 但 mano-cua 未执行) | failed (deploy_failed) | 同 #24 |

共 29 张卡，修复后 97/97 通过合规检查。

---

## 2026-04-18 11:30 — worker-03 合规修复 27 张结果卡

**操作人：** worker-03（林菡确认）
**原因：** Pichai 合规扫描发现 worker-03 提交的 90 张结果中 27 张不符合 `worker-execution-guide.md` 标准 schema（缺少顶层必填字段、sess_id 问题、mano_cua 缺字段、failure 为 null、JSON 解析失败）
**审计报告：** `reports/worker-03-audit.md`
**修复脚本：** `scripts/fix-worker03.py`（可复现）

**修复分类：**

| 类型 | 数量 | 修复方式 |
|------|------|----------|
| A: 有 log 可提取真实数据 | 2 | 从 log 提取正确 sess_id / 修复 JSON 转义 |
| B: 信息存在但格式非标准 | 4 | 重组为标准 failure 对象 |
| C: completed 但 mano_cua 未启动 → failed | 21 | status 改 failed + 构建 failure 对象 + mano_cua 设 null |

**修复后 status 分布（90 张）：**

| status | 数量 |
|--------|------|
| completed | 60 |
| failed | 30 |

**影响卡清单（27 张）：**

| # | 文件 | 修复前问题 | 修复后 status | 修复方式 |
|---|------|-----------|---------------|----------|
| 1 | `cboard-1752.json` | sess_id 格式错误：`sess-20260418000125-placeholder` | completed | 从 log 提取真实 sess_id：`sess-20260418000150-452ee47d7c8141999938126b5add74c7` |
| 2 | `open5e-622.json` | JSON 解析失败：last_reasoning 中 CSS content 转义错误 | completed | JSON 重建 + 从 log 提取 total_steps(90)/last_action/last_reasoning |
| 3 | `cloudinary-179.json` | status=failed 但 failure 为 null，使用非标字段 failure_reason/failure_detail | failed (deploy_failed) | 重组为标准 failure 对象 + 补 sess_id=null/expected_result_used |
| 4 | `open5e-783.json` | status=failed 但 failure 为 null | failed (deploy_failed) | 从 mano_cua.result_summary 构建 failure 对象，mano_cua 设 null |
| 5 | `saltcorn-3596.json` | status=failed 但 failure 为 null | failed (deploy_failed) | 从 mano_cua.result_summary 构建 failure 对象，mano_cua 设 null |
| 6 | `saltcorn-3859.json` | status=failed 但 failure 为 null | failed (deploy_failed) | 从 mano_cua.result_summary 构建 failure 对象，mano_cua 设 null |
| 7 | `VueTorrent-2391.json` | status=completed 但 mano_cua 未启动，缺 sess_id/duration_seconds，mano_cua 缺 total_steps/last_action/last_reasoning | failed (deploy_failed) | completed→failed，构建标准 failure 对象（需 qBittorrent 后端），mano_cua 设 null |
| 8 | `VueTorrent-2413.json` | 同 #7 | failed (deploy_failed) | 同 #7 |
| 9 | `VueTorrent-2433.json` | 同 #7 | failed (deploy_failed) | 同 #7 |
| 10 | `VueTorrent-2440.json` | 同 #7 | failed (deploy_failed) | 同 #7 |
| 11 | `VueTorrent-2489.json` | 同 #7 | failed (deploy_failed) | 同 #7 |
| 12 | `VueTorrent-2492.json` | 同 #7 | failed (deploy_failed) | 同 #7 |
| 13 | `VueTorrent-2570.json` | 同 #7 | failed (deploy_failed) | 同 #7 |
| 14 | `VueTorrent-2573.json` | 同 #7 | failed (deploy_failed) | 同 #7 |
| 15 | `VueTorrent-2587.json` | 同 #7 | failed (deploy_failed) | 同 #7 |
| 16 | `VueTorrent-2657.json` | 同 #7 | failed (deploy_failed) | 同 #7 |
| 17 | `VueTorrent-2676.json` | 同 #7 | failed (deploy_failed) | 同 #7 |
| 18 | `CopilotKit-3263.json` | 同 #7（需 LLM API 后端） | failed (deploy_failed) | completed→failed，构建 failure 对象（需 OpenAI API key） |
| 19 | `cboard-2039.json` | 同 #7（需登录+ElevenLabs API Key） | failed (deploy_failed) | completed→failed，构建 failure 对象（需账号+API key） |
| 20 | `console-2604.json` | 同 #7（需 Appwrite 后端） | failed (deploy_failed) | completed→failed，构建 failure 对象（需 Appwrite 后端服务） |
| 21 | `devhub-107.json` | 同 #7（需 GitHub OAuth） | failed (deploy_failed) | completed→failed，构建 failure 对象（需 GitHub OAuth 认证） |
| 22 | `pluely-153.json` | 同 #7（Tauri 桌面应用+需 LLM API） | failed (deploy_failed) | completed→failed，构建 failure 对象（需 LLM API key） |
| 23 | `saleor-dashboard-5985.json` | 同 #7（需 Saleor GraphQL 后端） | failed (deploy_failed) | completed→failed，构建 failure 对象（需电商后端） |
| 24 | `shopify-268.json` | 同 #7（需 Shopify API 凭证） | failed (deploy_failed) | completed→failed，构建 failure 对象（需 Storefront API Token） |
| 25 | `sim-3922.json` | 同 #7（需外部 AI 后端） | failed (deploy_failed) | completed→failed，构建 failure 对象（需 MCP/Ollama 服务） |
| 26 | `sim-3974.json` | 同 #7（需外部 AI 后端） | failed (deploy_failed) | completed→failed，构建 failure 对象（需 MCP/Ollama 服务） |
| 27 | `wanderlust-392.json` | 同 #7（需 MongoDB 后端） | failed (deploy_failed) | completed→failed，构建 failure 对象（需 MongoDB 服务） |

共 27 张卡，修复后 90/90 通过合规检查。

---

## 2026-04-18 11:15 — worker-01 合规修复 16 张结果卡

**操作人：** worker-01（林菡确认）
**原因：** Pichai 合规扫描发现 worker-01 提交的 57 张结果中 16 张不符合 `worker-execution-guide.md` 标准 schema（failure.type 非法值、status/结构错误、sess_id 格式错误）
**审计报告：** `reports/worker-01-audit.md`

**修复分类：**

| 类型 | 数量 | 修复方式 |
|------|------|----------|
| failure.type `deploy_blocked` → `deploy_failed` | 4 | 字段值替换 |
| completed+mano_cua.result=deploy_failed → failed 格式 | 11 | 重构为 status=failed + failure 对象，mano_cua=null |
| sess_id 格式错误（多段拼接） | 1 | 从原始 log 提取正确 sess_id |

**修复后 status 分布（57 张）：**

| status | 数量 |
|--------|------|
| completed | 38 |
| failed | 19 |

**影响卡清单（16 张）：**

| # | 文件 | 修复前问题 | 修复后 status | 修复方式 |
|---|------|-----------|---------------|----------|
| 1 | `Semantic-UI-React-3502.json` | failure.type=`deploy_blocked`（非法值） | failed (deploy_failed) | `deploy_blocked` → `deploy_failed` |
| 2 | `Semantic-UI-React-3552.json` | failure.type=`deploy_blocked`（非法值） | failed (deploy_failed) | `deploy_blocked` → `deploy_failed` |
| 3 | `Semantic-UI-React-3581.json` | failure.type=`deploy_blocked`（非法值） | failed (deploy_failed) | `deploy_blocked` → `deploy_failed` |
| 4 | `Semantic-UI-React-3669.json` | failure.type=`deploy_blocked`（非法值） | failed (deploy_failed) | `deploy_blocked` → `deploy_failed` |
| 5 | `animate-ui-129.json` | sess_id 格式错误：多了一段时间戳拼接 | completed (abnormal) | 从 log 提取正确 sess_id：`sess-20260417183909-4fe90955a8a841be8809c20c50b9bc63` |
| 6 | `devhub-17.json` | status=completed + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式，symptom/attempted/recommendation 从原 result_summary 迁移 |
| 7 | `docz-985.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式 |
| 8 | `photon-330.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式 |
| 9 | `photon-526.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式 |
| 10 | `shopify-223.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式 |
| 11 | `shopify-259.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式 |
| 12 | `shopify-264.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式 |
| 13 | `shopify-267.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式 |
| 14 | `shopify-269.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式 |
| 15 | `shopify-274.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式 |
| 16 | `shopify-293.json` | sess_id 为空 + mano_cua.result=`deploy_failed`（非法值） | failed (deploy_failed) | 重构为 failed 格式 |

共 16 张卡，修复后 57/57 通过合规检查。

---

## 2026-04-18 11:10 — worker-02 合规修复 77 张结果卡

**操作人：** worker-02（林菡确认）
**原因：** Pichai 合规扫描发现 worker-02 提交的 127 张结果中 77 张不符合 `worker-execution-guide.md` 标准 schema（缺少顶层必填字段、status 非法值、failure 为 null、sess_id 格式错误等）
**操作：** 就地修复 77 张 JSON 文件，将旧格式字段映射为标准 schema，修复后全部通过合规检查（127/127）

**修复脚本：** `scripts/fix-compliance.py`（可复现）
**验证脚本：** `scripts/check-compliance.py`（修复后 127/127 通过）

**修复分类：**

| 类型 | 数量 | 修复方式 |
|------|------|----------|
| 旧格式+有log→completed | 33 | 从 log 解析 sess_id/duration/last_reasoning，status 映射为 completed，重构 mano_cua 对象 |
| 旧格式+无session→failed | 21 | 转 status=failed + failure 对象，sess_id=null, mano_cua=null, duration_seconds=0 |
| 旧格式+有log+缺字段→completed/failed | 18 | 从 log/任务卡补字段（repo 等），按是否有 mano-cua session 分 completed/failed |
| sess_id 格式错误（vue-pdf-179/189） | 2 | 转 status=failed + failure.type=other（未跑 mano-cua） |
| failure 为 null（website-4566/4776/4780） | 3 | 重构 failure_reason/failure_detail 为标准 failure 对象，sess_id N/A→null |

**修复后 status 分布：**

| status | 数量 | mano_cua.result / failure.type 分布 |
|--------|------|-------------------------------------|
| completed | 78 | abnormal: 47, unclear: 20, normal: 11 |
| failed | 49 | deploy_failed: 47, other: 2 |

**影响卡清单（77 张）：**

| # | 文件 | 修复前问题 | 修复后 status | 修复方式 |
|---|------|-----------|---------------|----------|
| 1 | `Analog-259.json` | status=error, 缺 sess_id/expected_result_used/duration_seconds/mano_cua/failure 顶层字段 | failed (deploy_failed) | 从 reasoning_summary 构建 failure 对象；补 sess_id=null, expected_result_used=false, duration_seconds=0, mano_cua=null |
| 2 | `BongoCat-431.json` | status=error, 缺 sess_id/expected_result_used/duration_seconds/mano_cua/failure 顶层字段 | failed (deploy_failed) | 从 reasoning_summary 构建 failure 对象（Tauri 桌面应用）；补 sess_id=null, mano_cua=null |
| 3 | `BongoCat-437.json` | status=error, 缺必填顶层字段 | failed (deploy_failed) | 同 #2，Tauri 桌面应用无法浏览器测试 |
| 4 | `BongoCat-438.json` | status=error, 缺必填顶层字段 | failed (deploy_failed) | 同 #2 |
| 5 | `BongoCat-499.json` | status=error, 缺必填顶层字段 | failed (deploy_failed) | 同 #2 |
| 6 | `BongoCat-509.json` | status=error, 缺必填顶层字段 | failed (deploy_failed) | 同 #2 |
| 7 | `BongoCat-592.json` | status=error, 缺必填顶层字段 | failed (deploy_failed) | 同 #2 |
| 8 | `BongoCat-777.json` | status=error, 缺必填顶层字段 | failed (deploy_failed) | 同 #2 |
| 9 | `ByteStash-46.json` | status=abnormal, 缺 sess_id/expected_result_used/duration_seconds/mano_cua 顶层字段 | completed (abnormal) | 从 log 解析 sess_id + duration；从 reasoning_summary 构建 mano_cua 对象（含 last_reasoning）；status abnormal→completed + mano_cua.result=abnormal |
| 10 | `ByteStash-58.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 同 #9，从 log 解析 sess_id/duration/last_reasoning |
| 11 | `ByteStash-156.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 同 #9 |
| 12 | `ByteStash-157.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 同 #9 |
| 13 | `ByteStash-171.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 同 #9 |
| 14 | `ByteStash-173.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 同 #9 |
| 15 | `Dante-128.json` | status=error, 缺必填顶层字段 | failed (deploy_failed) | 从 reasoning_summary 构建 failure 对象（buggy commit 是 Ruby 版本）；补 sess_id=null, mano_cua=null |
| 16 | `Luckysheet-528.json` | status=unclear, 缺必填顶层字段 | completed (unclear) | 从 log 解析 sess_id/duration/last_reasoning；status unclear→completed + mano_cua.result=unclear |
| 17 | `Markpad-21.json` | status=unclear, 缺必填顶层字段 | completed (unclear) | 同 #16 |
| 18 | `Notpad-195.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 从 log 解析 sess_id/duration/last_reasoning；status→completed + mano_cua.result=abnormal |
| 19 | `Notpad-268.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 同 #18 |
| 20 | `Semantic-UI-React-3864.json` | status=normal, 缺 sess_id/expected_result_used/duration_seconds/mano_cua 顶层字段 | completed (normal) | 从 log 解析 sess_id/duration/last_reasoning；status normal→completed + mano_cua.result=normal |
| 21 | `Semantic-UI-React-3994.json` | status=normal, 缺必填顶层字段 | completed (normal) | 同 #20 |
| 22 | `Semantic-UI-React-4005.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 从 log 解析 sess_id/duration/last_reasoning；status→completed + mano_cua.result=abnormal |
| 23 | `Semantic-UI-React-4083.json` | status=unclear, 缺必填顶层字段 | completed (unclear) | 从 log 解析 sess_id/duration/last_reasoning；status→completed + mano_cua.result=unclear |
| 24 | `Semantic-UI-React-4110.json` | status=unclear, 缺必填顶层字段 | completed (unclear) | 同 #23 |
| 25 | `Silex-743.json` | status=None, 缺 status/sess_id/expected_result_used/duration_seconds/failure 字段 | failed (deploy_failed) | 从 reasoning_summary 构建 failure 对象；补 sess_id=null, mano_cua=null, duration_seconds=0 |
| 26 | `Silex-843.json` | status=None, 缺必填字段 | failed (deploy_failed) | 同 #25 |
| 27 | `angular-datatables-1605.json` | status=None, 缺 status/sess_id/expected_result_used/duration_seconds/mano_cua 字段 | completed (abnormal) | 从 log 解析 sess_id/duration/last_reasoning；从任务卡补 repo；构建 mano_cua 对象 |
| 28 | `angular-datatables-1723.json` | status=None, 缺必填字段 | completed (abnormal) | 同 #27 |
| 29 | `angular-datepicker-112.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 从 log 解析 sess_id/duration/last_reasoning；status→completed + mano_cua.result=abnormal |
| 30 | `angular-gridster2-377.json` | status=None, 缺必填字段 | failed (deploy_failed) | 从 reasoning_summary 构建 failure 对象；补 sess_id=null, mano_cua=null |
| 31 | `angular-gridster2-529.json` | status=None, 缺必填字段 | failed (deploy_failed) | 同 #30 |
| 32 | `cryptgeon-150.json` | status=None, 缺必填字段 | failed (deploy_failed) | 从 reasoning_summary 构建 failure 对象（需 Rust 后端）；补 sess_id=null, mano_cua=null |
| 33 | `emoji-mart-218.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 从 log 解析 sess_id/duration/last_reasoning；status→completed + mano_cua.result=abnormal |
| 34 | `emoji-mart-219.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 同 #33 |
| 35 | `emoji-mart-220.json` | status=unclear, 缺必填顶层字段 | completed (unclear) | 从 log 解析 sess_id/duration/last_reasoning；status→completed + mano_cua.result=unclear |
| 36 | `emoji-mart-254.json` | status=normal, 缺必填顶层字段 | completed (normal) | 从 log 解析 sess_id/duration/last_reasoning；status→completed + mano_cua.result=normal |
| 37 | `emoji-mart-327.json` | status=abnormal, 缺必填顶层字段 | completed (abnormal) | 同 #33 |
| 38 | `emoji-mart-762.json` | status=unclear, 缺必填顶层字段 | completed (unclear) | 从 log 解析 sess_id/duration/last_reasoning；status→completed + mano_cua.result=unclear |
| 39 | `flitter-68.json` | status=None, 缺 repo/status/expected_result_used/duration_seconds/mano_cua 字段 | completed (unclear) | 从 log 解析 sess_id/duration/last_reasoning；从任务卡补 repo；构建 mano_cua 对象 |
| 40 | `kan-23.json` | status=None, 缺 repo/status/expected_result_used/duration_seconds 字段 | failed (deploy_failed) | 从 result_summary 构建 failure 对象（需 PostgreSQL+OAuth+S3）；从任务卡补 repo；补 sess_id=null, mano_cua=null |
| 41 | `kan-27.json` | status=None, 缺 repo/必填字段 | failed (deploy_failed) | 同 #40 |
| 42 | `kan-30.json` | status=None, 缺 repo/必填字段 | failed (deploy_failed) | 同 #40 |
| 43 | `kan-35.json` | status=None, 缺 repo/必填字段 | failed (deploy_failed) | 同 #40 |
| 44 | `kan-70.json` | status=None, 缺 repo/必填字段 | failed (deploy_failed) | 同 #40 |
| 45 | `kan-206.json` | status=None, 缺 repo/必填字段 | failed (deploy_failed) | 同 #40 |
| 46 | `kan-242.json` | status=None, 缺 repo/必填字段 | failed (deploy_failed) | 同 #40 |
| 47 | `karakeep-2395.json` | status=deploy_failed（非法值）, 缺必填顶层字段 | completed (unclear) | 从 log 解析 sess_id/duration/last_reasoning；实际跑了 mano-cua，status 纠正为 completed |
| 48 | `karakeep-2396.json` | status=deploy_failed（非法值）, 缺必填顶层字段 | failed (deploy_failed) | 从 reasoning_summary 构建 failure 对象；补 sess_id=null, mano_cua=null |
| 49 | `karakeep-2493.json` | status=deploy_failed（非法值）, 缺必填顶层字段 | failed (deploy_failed) | 同 #48 |
| 50 | `next-redux-wrapper-325.json` | status=None, 缺必填字段 | failed (deploy_failed) | 从 reasoning_summary 构建 failure 对象；补 sess_id=null, mano_cua=null |
| 51 | `onlook-2587.json` | status=None, 缺必填字段 | failed (deploy_failed) | 同 #50 |
| 52 | `onlook-2908.json` | status=None, 缺必填字段 | failed (deploy_failed) | 同 #50 |
| 53 | `open5e-622.json` | status=None, 缺 repo/status/expected_result_used/duration_seconds/mano_cua 字段 | completed (abnormal) | 从 log 解析 sess_id/duration/last_reasoning；从任务卡补 repo；构建 mano_cua 对象 |
| 54 | `open5e-655.json` | status=None, 缺 repo/必填字段 | completed (abnormal) | 同 #53 |
| 55 | `open5e-694.json` | sess_id=inferred-from-open5e-695（格式非法）, total_steps=0 | failed (deploy_failed) | 未实际运行 mano-cua（推断结果）；转 status=failed + failure 对象；sess_id=null, mano_cua=null |
| 56 | `open5e-695.json` | status=None, 缺 repo/必填字段 | completed (abnormal) | 从 log 解析 sess_id/duration/last_reasoning；从任务卡补 repo；构建 mano_cua 对象 |
| 57 | `open5e-716.json` | status=None, 缺 repo/必填字段 | completed (abnormal) | 同 #53 |
| 58 | `open5e-721.json` | status=None, 缺 repo/必填字段 | completed (abnormal) | 同 #53 |
| 59 | `open5e-747.json` | status=None, 缺 repo/必填字段 | completed (abnormal) | 同 #53 |
| 60 | `open5e-775.json` | status=None, 缺 repo/必填字段 | completed (abnormal) | 同 #53 |
| 61 | `open5e-799.json` | status=None, 缺 repo/必填字段 | completed (unclear) | 从 log 解析 sess_id/duration/last_reasoning；从任务卡补 repo；构建 mano_cua 对象 |
| 62 | `open5e-803.json` | status=None, 缺 repo/必填字段 | completed (abnormal) | 同 #53 |
| 63 | `padloc-427.json` | status=None, 缺必填字段 | failed (deploy_failed) | 从 reasoning_summary 构建 failure 对象；补 sess_id=null, mano_cua=null |
| 64 | `padloc-638.json` | status=None, 缺必填字段 | failed (deploy_failed) | 同 #63 |
| 65 | `script-lab-667.json` | status=None, 缺 status/sess_id/expected_result_used/duration_seconds/mano_cua 字段 | completed (normal) | 从 log 解析 sess_id/duration/last_reasoning；从任务卡补 repo；构建 mano_cua 对象 |
| 66 | `script-lab-672.json` | status=None, 缺必填字段 | completed (abnormal) | 同 #65 |
| 67 | `script-lab-732.json` | status=abnormal, 缺 sess_id/expected_result_used/duration_seconds/mano_cua 顶层字段 | completed (abnormal) | 从 log 解析 sess_id/duration/last_reasoning；status→completed + mano_cua.result=abnormal |
| 68 | `shopware-pwa-1537.json` | status=deploy_failed（非法值）, 缺必填顶层字段 | failed (deploy_failed) | 从 reasoning_summary 构建 failure 对象；补 sess_id=null, mano_cua=null |
| 69 | `shopware-pwa-1665.json` | status=deploy_failed（非法值）, 缺必填顶层字段 | failed (deploy_failed) | 同 #68 |
| 70 | `signature_pad-120.json` | status=normal, 缺 sess_id/expected_result_used/duration_seconds/mano_cua 顶层字段 | completed (normal) | 从 log 解析 sess_id/duration/last_reasoning；status normal→completed + mano_cua.result=normal |
| 71 | `signature_pad-656.json` | status=unclear, 缺必填顶层字段 | completed (unclear) | 从 log 解析 sess_id/duration/last_reasoning；status unclear→completed + mano_cua.result=unclear |
| 72 | `slickgpt-38.json` | status=None, 缺必填字段 | completed (unclear) | 从 log 解析 sess_id/duration/last_reasoning；从任务卡补 repo；构建 mano_cua 对象 |
| 73 | `vue-pdf-179.json` | sess_id=N/A-code-review（格式非法）, mano_cua 缺 last_reasoning | failed (other) | 未实际运行 mano-cua（代码审查）；转 status=failed + failure.type=other；sess_id=null, mano_cua=null |
| 74 | `vue-pdf-189.json` | sess_id=N/A-code-review（格式非法）, mano_cua 缺 last_reasoning | failed (other) | 同 #73 |
| 75 | `website-4566.json` | status=failed 正确，但 failure 为 null（用了非标准 failure_reason/failure_detail 字段） | failed (deploy_failed) | 将 failure_reason+failure_detail 重构为标准 failure 对象（含 type/symptom/attempted/recommendation）；sess_id N/A→null |
| 76 | `website-4776.json` | status=failed 正确，但 failure 为 null（同上） | failed (deploy_failed) | 同 #75 |
| 77 | `website-4780.json` | status=failed 正确，但 failure 为 null（同上） | failed (deploy_failed) | 同 #75 |

共 77 张卡。

## 2026-04-17 16:07 — 移除 25 张非标准 schema 结果卡

**操作人：** Pichai（林菡确认）
**原因：** 这 25 张卡的 result JSON 不符合标准 schema（缺少 status 字段、status 值非标准如 deploy_failed/unclear）
**操作：** 从 results/{workerXX}/ 移至 results_archive/trash/，dispatch-log 状态改回 unassigned，后续重新派发

**影响卡列表：**

| # | task_id | 原 Worker | 问题 |
|---|---------|-----------|------|
| 1 | Semantic-UI-React-3864 | worker-02 | missing status field (non-standard schema) |
| 2 | Semantic-UI-React-3994 | worker-02 | missing status field (non-standard schema) |
| 3 | Semantic-UI-React-4005 | worker-02 | missing status field (non-standard schema) |
| 4 | Semantic-UI-React-4083 | worker-02 | missing status field (non-standard schema) |
| 5 | Semantic-UI-React-4110 | worker-02 | missing status field (non-standard schema) |
| 6 | react-content-loader-110 | worker-02 | missing status field (non-standard schema) |
| 7 | emoji-mart-219 | worker-03 | missing status field (non-standard schema) |
| 8 | emoji-mart-220 | worker-03 | missing status field (non-standard schema) |
| 9 | emoji-mart-254 | worker-03 | missing status field (non-standard schema) |
| 10 | emoji-mart-327 | worker-03 | missing status field (non-standard schema) |
| 11 | emoji-mart-762 | worker-03 | missing status field (non-standard schema) |
| 12 | open5e-694 | worker-03 | non-standard status: deploy_failed |
| 13 | open5e-695 | worker-03 | non-standard status: deploy_failed |
| 14 | open5e-716 | worker-03 | non-standard status: deploy_failed |
| 15 | blinko-1068 | worker-09 | non-standard status: deploy_failed |
| 16 | blinko-1138 | worker-09 | non-standard status: deploy_failed |
| 17 | blinko-427 | worker-09 | non-standard status: deploy_failed |
| 18 | blinko-444 | worker-09 | non-standard status: deploy_failed |
| 19 | blinko-802 | worker-09 | non-standard status: deploy_failed |
| 20 | organice-1001 | worker-09 | non-standard status: deploy_failed |
| 21 | organice-1006 | worker-09 | non-standard status: deploy_failed |
| 22 | organice-779 | worker-09 | non-standard status: deploy_failed |
| 23 | organice-784 | worker-09 | non-standard status: deploy_failed |
| 24 | organice-988 | worker-09 | non-standard status: deploy_failed |
| 25 | rich-markdown-editor-489 | worker-09 | non-standard status: unclear |

共 25 张卡。

## 2026-04-17 16:23 — 移除 24 张 mano_cua.result 非标准结果卡

**操作人：** Pichai（林菡确认）
**原因：** status=completed 但 mano_cua.result 不在 {normal, abnormal, unclear} 标准值范围内
**操作：** 从 results/{workerXX}/ 移至 results_archive/trash/，dispatch-log 状态改回 unassigned

**影响卡列表：**

| # | task_id | 原 Worker | 问题 |
|---|---------|-----------|------|
| 1 | lokus-15 | worker-02 | mano_cua.result=deploy_failed |
| 2 | lokus-255 | worker-02 | mano_cua.result=deploy_failed |
| 3 | lokus-259 | worker-02 | mano_cua.result=deploy_failed |
| 4 | lokus-261 | worker-02 | mano_cua.result=deploy_failed |
| 5 | lokus-283 | worker-02 | mano_cua.result=deploy_failed |
| 6 | website-4776 | worker-04 | mano_cua.result=bug_found |
| 7 | SvelteLab-194 | worker-06 | mano_cua.result=deploy_failed |
| 8 | SvelteLab-289 | worker-06 | mano_cua.result=deploy_failed |
| 9 | github-profile-readme-generator-249 | worker-06 | mano_cua.result=deploy_failed |
| 10 | github-profile-readme-generator-382 | worker-06 | mano_cua.result=deploy_failed |
| 11 | github-profile-readme-generator-93 | worker-06 | mano_cua.result=deploy_failed |
| 12 | hermes-ide-75 | worker-06 | mano_cua.result=deploy_failed |
| 13 | hermes-ide-78 | worker-06 | mano_cua.result=deploy_failed |
| 14 | hermes-ide-87 | worker-06 | mano_cua.result=deploy_failed |
| 15 | kan-35 | worker-06 | mano_cua.result=deploy_failed |
| 16 | kan-376 | worker-06 | mano_cua.result=deploy_failed |
| 17 | kan-70 | worker-06 | mano_cua.result=deploy_failed |
| 18 | kan-71 | worker-06 | mano_cua.result=deploy_failed |
| 19 | photon-345 | worker-06 | mano_cua.result=deploy_failed |
| 20 | photon-543 | worker-06 | mano_cua.result=deploy_failed |
| 21 | tabler-react-226 | worker-06 | mano_cua.result=deploy_failed |
| 22 | tabler-react-238 | worker-06 | mano_cua.result=deploy_failed |
| 23 | tabler-react-353 | worker-06 | mano_cua.result=deploy_failed |
| 24 | rich-markdown-editor-538 | worker-09 | mano_cua.result=__MISSING__ |

共 24 张卡。

## 2026-04-17 16:27 — 移除 2 张 sess_id 不合规结果卡

**操作人：** Pichai（林菡确认）
**原因：** status=completed 但 sess_id 为 N/A（Tauri 桌面应用，浏览器不兼容，无有效 mano-cua session）
**操作：** 移至 results_archive/trash/，dispatch-log 改回 unassigned

| # | task_id | 原 Worker | 问题 |
|---|---------|-----------|------|
| 1 | BongoCat-509 | worker-08 | sess_id=N/A-tauri-app-browser-incompatible |
| 2 | BongoCat-777 | worker-08 | sess_id=N/A-tauri-app-browser-incompatible |

共 2 张卡。

## 2026-04-17 — Round 4: TOS 无数据清理（32 张）

**原因：** Emily/智子排查 TOS 发现 32 个 session ID 在 TOS 上无数据（轨迹未上传）
**操作：** 对应 32 张 result JSON 从 results/ 移入 trash，dispatch-log 改回 unassigned
**影响：** 31 个 task_id（Analog-135 有两份），32 个文件
**涉及 Worker：** worker-01(3), worker-03(1), worker-04(2), worker-05(3), worker-06(3), worker-07(1), worker-08(14), worker-09(2), worker-fabrice(4) — 注 Analog-135 同时在 worker-09 和 worker-fabrice
