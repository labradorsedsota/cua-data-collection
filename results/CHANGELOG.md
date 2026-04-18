# Results CHANGELOG

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
