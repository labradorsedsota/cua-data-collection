# Results CHANGELOG

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
