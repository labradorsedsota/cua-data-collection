# Results 质量审计报告

> 生成时间：2026-04-18 10:31
> 审计范围：`results/worker-*/` 全部 JSON 文件
> 规范依据：`worker-config/worker-execution-guide.md` 第三节"结果上报"

---

## 一、总览

| 指标 | 数值 |
|------|------|
| 结果文件总数 | 697 |
| 合规文件 | 480 (68.9%) |
| 不合规文件 | 217 (31.1%) |
| 违规项总数 | 409 |

---

## 二、Status 分布

| status | 数量 | 占比 | 是否合规 |
|--------|------|------|----------|
| `completed` | 444 | 63.7% | ✅ |
| `failed` | 173 | 24.8% | ✅ |
| `None` | 40 | 5.7% | ❌ 非法值 |
| `abnormal` | 14 | 2.0% | ❌ 非法值 |
| `error` | 9 | 1.3% | ❌ 非法值 |
| `unclear` | 7 | 1.0% | ❌ 非法值 |
| `deploy_failed` | 5 | 0.7% | ❌ 非法值 |
| `normal` | 4 | 0.6% | ❌ 非法值 |
| `tool_error` | 1 | 0.1% | ❌ 非法值 |

> 规范要求 status 只能是 `completed` 或 `failed`。当前有 80 张卡使用了非法值。

---

## 三、Completed 卡分析（444 张）

### 3.1 mano_cua.result 分布

| result | 数量 | 占比 | 合规 |
|--------|------|------|------|
| `abnormal` | 186 | 41.9% | ✅ |
| `unclear` | 147 | 33.1% | ✅ |
| `normal` | 89 | 20.0% | ✅ |
| `deploy_failed` | 17 | 3.8% | ❌ |
| `MISSING` | 5 | 1.1% | ❌ |

### 3.2 mano_cua.total_steps 分布

| 指标 | 值 |
|------|-----|
| 最小值 | 1 |
| 最大值 | 216 |
| 中位数 | 38 |
| 平均值 | 42.8 |

| 步数区间 | 数量 |
|----------|------|
| 1-10 | 34 |
| 11-20 | 56 |
| 21-30 | 64 |
| 31-50 | 71 |
| 51-80 | 96 |
| >80 | 35 |

> 执行手册规定步数上限 80 步，35 张卡超标。

### 3.3 sess_id 合规性

| 状态 | 数量 |
|------|------|
| ✅ 合规格式且唯一 | 344 |
| ❌ null/缺失 | 41 |
| ❌ 空字符串 | 42 |
| ❌ 格式错误 | 5 |
| ⚠️ 重复 sess_id | 14 张（2 组） |

重复 sess_id 详情：

- `sess-20260418024444-2e21dae5022e4d2aa37d5aa8253b5042`: 10 张 — typehero-1504.json, typehero-1516.json, typehero-1541.json, typehero-1571.json, typehero-1616.json, typehero-1686.json, typehero-1688.json, typehero-1695.json, typehero-1721.json, typehero-920.json
- `sess-20260417023846-ac10ca59d6a945cc86cc6d44d9858635`: 4 张 — ha-fusion-220.json, ha-fusion-278.json, ha-fusion-476.json, ha-fusion-478.json

---

## 四、Failed 卡分析（173 张）

### 4.1 failure.type 分布

| type | 数量 |
|------|------|
| `deploy_failed` | 127 |
| `NO_FAILURE_OBJ` | 39 |
| `deploy_blocked` | 4 |
| `other` | 2 |
| `mano_cua_error` | 1 |

### 4.2 主要失败原因

| 原因 | 数量 |
|------|------|
| 需要数据库/外部服务 | 22 |
| repo 下载超时 | 17 |
| 端口问题 | 15 |
| 需要认证/OAuth | 11 |
| node-sass/node-gyp 编译错误 | 10 |
| TresJS monorepo部署失败。pnpm postinstall中vite build失败(Node 23不兼容 | 6 |
| mano-cua 屏幕录制权限异常，Chrome 窗口不可见，系统级阻塞 | 4 |
| Python 依赖问题 | 4 |
| Node 版本兼容问题 | 3 |
| Tauri桌面应用（依赖@tauri-apps/api, @tauri-apps/plugin-*），vite dev  | 3 |
| Requires Zesty.io backend API. Bug confirmed via source code | 3 |
| npm install 失败：核心依赖 mono-svelte@^1.5.14 于 2025-07-16 从 npm 注 | 2 |
| Podverse Web是播客平台，backend_risk:true。核心功能（播客搜索/播放/订阅）需要外部API后 | 2 |
| mano-cua 屏幕录制权限异常，Chrome 窗口在 CUA 截图中不可见。screencapture 命令报 'c | 1 |
| npm install / yarn install 反复被系统 SIGKILL（内存不足），Gatsby monore | 1 |

---

## 五、各 Worker 违规汇总

| Worker | 结果数 | 不合规数 | 不合规率 |
|--------|--------|----------|----------|
| worker-01 | 52 | 12 | 23% |
| worker-02 | 127 | 77 | 61% |
| worker-03 | 89 | 27 | 30% |
| worker-04 | 55 | 6 | 11% |
| worker-05 | 50 | 8 | 16% |
| worker-06 | 62 | 5 | 8% |
| worker-07 | 42 | 2 | 5% |
| worker-08 | 72 | 31 | 43% |
| worker-09 | 97 | 29 | 30% |
| worker-fabrice | 51 | 20 | 39% |

---

## 六、不合规卡完整清单（217 张）

### worker-01（12 张）

| 文件 | 问题 |
|------|------|
| Semantic-UI-React-3502.json | failure.type 非法值: `deploy_blocked` |
| Semantic-UI-React-3552.json | failure.type 非法值: `deploy_blocked` |
| Semantic-UI-React-3581.json | failure.type 非法值: `deploy_blocked` |
| Semantic-UI-React-3669.json | failure.type 非法值: `deploy_blocked` |
| animate-ui-129.json | sess_id 格式错误: `sess-20260417184505-417183909-4fe90955a8a841be8809c20c50b9bc63` |
| shopify-223.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| shopify-259.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| shopify-264.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| shopify-267.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| shopify-269.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| shopify-274.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| shopify-293.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |

### worker-02（77 张）

| 文件 | 问题 |
|------|------|
| Analog-259.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `error` |
| BongoCat-431.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `error` |
| BongoCat-437.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `error` |
| BongoCat-438.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `error` |
| BongoCat-499.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `error` |
| BongoCat-509.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `error` |
| BongoCat-592.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `error` |
| BongoCat-777.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `error` |
| ByteStash-156.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| ByteStash-157.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| ByteStash-171.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| ByteStash-173.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| ByteStash-46.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| ByteStash-58.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| Dante-128.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `error` |
| Luckysheet-528.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `unclear` |
| Markpad-21.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `unclear` |
| Notpad-195.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| Notpad-268.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| Semantic-UI-React-3864.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `normal` |
| Semantic-UI-React-3994.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `normal` |
| Semantic-UI-React-4005.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| Semantic-UI-React-4083.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `unclear` |
| Semantic-UI-React-4110.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `unclear` |
| Silex-743.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| Silex-843.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| angular-datatables-1605.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| angular-datatables-1723.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| angular-datepicker-112.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| angular-gridster2-377.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| angular-gridster2-529.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| cryptgeon-150.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| emoji-mart-218.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| emoji-mart-219.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| emoji-mart-220.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `unclear` |
| emoji-mart-254.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `normal` |
| emoji-mart-327.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| emoji-mart-762.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `unclear` |
| flitter-68.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| kan-206.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| kan-23.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| kan-242.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| kan-27.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| kan-30.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| kan-35.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| kan-70.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| karakeep-2395.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `deploy_failed` |
| karakeep-2396.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `deploy_failed` |
| karakeep-2493.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `deploy_failed` |
| next-redux-wrapper-325.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| onlook-2587.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| onlook-2908.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| open5e-622.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| open5e-655.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| open5e-694.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| open5e-695.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| open5e-716.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| open5e-721.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| open5e-747.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| open5e-775.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| open5e-799.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| open5e-803.json | 缺少顶层字段: repo, status, expected_result_used, duration_seconds; status 非法值: `None` |
| padloc-427.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| padloc-638.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| script-lab-667.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| script-lab-672.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| script-lab-732.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `abnormal` |
| shopware-pwa-1537.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `deploy_failed` |
| shopware-pwa-1665.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `deploy_failed` |
| signature_pad-120.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `normal` |
| signature_pad-656.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `unclear` |
| slickgpt-38.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| vue-pdf-179.json | sess_id 格式错误: `N/A-code-review`; mano_cua 缺字段: last_reasoning |
| vue-pdf-189.json | sess_id 格式错误: `N/A-code-review`; mano_cua 缺字段: last_reasoning |
| website-4566.json | failure 为 null |
| website-4776.json | failure 为 null |
| website-4780.json | failure 为 null |

### worker-03（27 张）

| 文件 | 问题 |
|------|------|
| CopilotKit-3263.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| VueTorrent-2391.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| VueTorrent-2413.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| VueTorrent-2433.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| VueTorrent-2440.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| VueTorrent-2489.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| VueTorrent-2492.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| VueTorrent-2570.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| VueTorrent-2573.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| VueTorrent-2587.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| VueTorrent-2657.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| VueTorrent-2676.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| cboard-1752.json | sess_id 格式错误: `sess-20260418000125-placeholder` |
| cboard-2039.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| cloudinary-179.json | 缺少顶层字段: sess_id, expected_result_used; failure 为 null |
| console-2604.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| devhub-107.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| open5e-622.json | JSON 解析失败: Expecting property name enclosed in double quotes: line 16 column 137 (char 792) |
| open5e-783.json | 缺少顶层字段: sess_id, duration_seconds; failure 为 null |
| pluely-153.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| saleor-dashboard-5985.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| saltcorn-3596.json | 缺少顶层字段: sess_id, duration_seconds; failure 为 null |
| saltcorn-3859.json | 缺少顶层字段: sess_id, duration_seconds; failure 为 null |
| shopify-268.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| sim-3922.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| sim-3974.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |
| wanderlust-392.json | 缺少顶层字段: sess_id, duration_seconds; sess_id 缺失或为空; mano_cua 缺字段: total_steps, last_action, last_reasoning |

### worker-04（6 张）

| 文件 | 问题 |
|------|------|
| react-content-loader-93.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; sess_id 缺失或为空; mano_cua 为 null |
| script-lab-609.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; sess_id 缺失或为空; mano_cua 为 null |
| script-lab-623.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; sess_id 缺失或为空; mano_cua 为 null |
| script-lab-648.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; sess_id 缺失或为空; mano_cua 为 null |
| svelte-tags-input-17.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; sess_id 缺失或为空; mano_cua 为 null |
| website-4885.json | sess_id 缺失或为空 |

### worker-05（8 张）

| 文件 | 问题 |
|------|------|
| codeimage-420.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| codeimage-445.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| codeimage-641.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| lms-1931.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| lms-1932.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| lms-2098.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| svelte-splitpanes-3.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| think-83.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |

### worker-06（5 张）

| 文件 | 问题 |
|------|------|
| SvelteLab-194.json | mano_cua.result 非法值: `deploy_failed` |
| mini-qr-59.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| monaco-editor-auto-typings-32.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| svelteui-283.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |
| svelteui-297.json | sess_id 缺失或为空; mano_cua.result 非法值: `deploy_failed` |

### worker-07（2 张）

| 文件 | 问题 |
|------|------|
| angular-calendar-1396.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; status 非法值: `tool_error` |
| react-date-picker-110.json | JSON 解析失败: Invalid control character at: line 6 column 67 (char 197) |

### worker-08（31 张）

| 文件 | 问题 |
|------|------|
| Task-Board-516.json | sess_id 缺失或为空 |
| clappr-1868.json | sess_id 缺失或为空 |
| devtools-768.json | sess_id 缺失或为空 |
| elements-936.json | sess_id 缺失或为空 |
| epicenter-1637.json | sess_id 缺失或为空 |
| freespeech-21.json | sess_id 缺失或为空 |
| frontend-3712.json | sess_id 缺失或为空 |
| gitlight-56.json | sess_id 缺失或为空 |
| hls-downloader-491.json | sess_id 缺失或为空 |
| kan-320.json | sess_id 缺失或为空 |
| karakeep-2511.json | sess_id 缺失或为空 |
| karakeep-2569.json | sess_id 缺失或为空 |
| karakeep-2640.json | sess_id 缺失或为空 |
| lms-1583.json | sess_id 缺失或为空 |
| marble-296.json | sess_id 缺失或为空 |
| minimal-chat-99.json | sess_id 缺失或为空 |
| misskey-hub-next-101.json | sess_id 缺失或为空 |
| plot-2274.json | sess_id 缺失或为空 |
| rawgraphs-app-113.json | sess_id 缺失或为空 |
| react-design-editor-244.json | sess_id 缺失或为空 |
| react-native-web-2794.json | sess_id 缺失或为空 |
| react-pdf-1530.json | sess_id 缺失或为空 |
| shopify-261.json | sess_id 缺失或为空 |
| sorry-cypress-228.json | sess_id 缺失或为空 |
| sorry-cypress-392.json | sess_id 缺失或为空 |
| sorry-cypress-849.json | sess_id 缺失或为空 |
| static-cms-790.json | sess_id 缺失或为空 |
| suneditor-1205.json | sess_id 缺失或为空 |
| tui.editor-1806.json | sess_id 缺失或为空 |
| website-v2-1887.json | sess_id 缺失或为空 |
| win11React-658.json | sess_id 缺失或为空 |

### worker-09（29 张）

| 文件 | 问题 |
|------|------|
| Luckysheet-528.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds, timestamp; status 非法值: `None` |
| Starkiller-5.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds, timestamp; status 非法值: `None` |
| Task-Board-608.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds, timestamp; status 非法值: `None` |
| devtools-598.json | sess_id 缺失或为空 |
| kaneo-1066.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| kaneo-1081.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| kaneo-1087.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| kaneo-1131.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| kaneo-1140.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| maker.js-556.json | sess_id 缺失或为空 |
| megadraft-283.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| megadraft-286.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| megadraft-288.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| megadraft-302.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| megadraft-319.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| megadraft-324.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| ngx-datatable-1702.json | sess_id 缺失或为空 |
| ngx-page-scroll-2.json | sess_id 缺失或为空 |
| openclaw-nerve-27.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| openclaw-nerve-64.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| react-grid-layout-918.json | sess_id 缺失或为空 |
| react-hot-toast-10.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| react-hot-toast-101.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| react-hot-toast-27.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| react-hot-toast-45.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| react-hot-toast-50.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| shadcn-solid-122.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| shadcn-solid-77.json | 缺少顶层字段: status, sess_id, expected_result_used, duration_seconds; status 非法值: `None` |
| shikwasa-44.json | sess_id 缺失或为空 |

### worker-fabrice（20 张）

| 文件 | 问题 |
|------|------|
| Notpad-195.json | mano_cua 缺字段: status, last_action, last_reasoning |
| PeaNUT-35.json | mano_cua 缺字段: status, last_action, last_reasoning |
| Piped-3715.json | mano_cua 缺字段: status, last_action, last_reasoning |
| accounts-ui-173.json | sess_id 格式错误: `sess-accounts-ui-173` |
| accounts-ui-191.json | 缺少顶层字段: sess_id; sess_id 缺失或为空; mano_cua 缺字段: last_action, last_reasoning |
| accounts-ui-203.json | 缺少顶层字段: sess_id; sess_id 缺失或为空; mano_cua 缺字段: last_action, last_reasoning |
| accounts-ui-204.json | 缺少顶层字段: sess_id; sess_id 缺失或为空; mano_cua 缺字段: last_action, last_reasoning |
| commercejs-nextjs-demo-store-130.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| commercejs-nextjs-demo-store-156.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| commercejs-nextjs-demo-store-175.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| commercejs-nextjs-demo-store-221.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| commercejs-nextjs-demo-store-40.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| commercejs-nextjs-demo-store-59.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| commercejs-nextjs-demo-store-85.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| commercejs-nextjs-demo-store-88.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| commercejs-nextjs-demo-store-93.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| nuxt-studio-149.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| nuxt-studio-81.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| photon-342.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |
| photon-478.json | 缺少顶层字段: sess_id, expected_result_used, duration_seconds; failure 为 null |

---

## 七、建议

1. **worker-02 需全面返工**：77 张不合规卡，主要问题是使用了完全不同的 JSON schema（把 mano_cua.result 值直接当 status 用）
2. **worker-09 需补 failure 对象**：failed 卡缺少 failure 对象
3. **worker-01 修正 shopify 系列**：mano_cua.result 用了 `deploy_failed`（应为 `unclear` 或改 status 为 `failed`）
4. **sess_id 重复**：worker-04 的 typehero 10 张卡共用一个 sess_id，需确认是否真的是同一个 mano-cua session
5. **超过 80 步的卡**（35 张）需复查

---

*报告由 Pichai 自动生成，数据截至 2026-04-18 10:31*
