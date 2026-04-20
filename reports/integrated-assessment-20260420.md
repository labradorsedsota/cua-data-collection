# BugHunt Result 整合评估报告

> 生成时间：2026-04-20 14:55  
> 数据源：results/ 全量 873 张卡 × (合规检查 + 轨迹匹配 + 去重)

---

## 一、综合评级

| 评级 | 含义 | 数量 | 占比 |
|------|------|------|------|
| ✅ A级 | 可交付 | 722 | 82.7% |
| 🟡 B级 | 有瑕疵 | 125 | 14.3% |
| 🔴 C级 | 需修复 | 5 | 0.6% |
| ⚫ D级 | 无轨迹 | 21 | 2.4% |

---

## 二、result 卡 status 分布

| status | 数量 |
|--------|------|
| failed | 441 |
| completed | 430 |
| done | 1 |
|  | 1 |

## 三、mano_cua.status 分布（仅 completed 卡）

| mano_cua.status | 数量 |
|-----------------|------|
| COMPLETED | 380 |
| STOPPED_BY_USER | 24 |
| TIMEOUT | 9 |
| ERROR | 6 |
| SIGKILL | 4 |
| KILLED | 3 |
| STOPPED_STEP_LIMIT | 2 |
| NOT_EXECUTED | 2 |
| TERMINATED | 1 |
| KILLED_MAX_STEPS | 1 |
| STOPPED | 1 |

## 四、mano_cua.result 分布

| result | 数量 |
|--------|------|
| abnormal | 226 |
| normal | 114 |
| unclear | 93 |

## 五、轨迹匹配情况（completed 卡）

| 匹配结果 | 数量 |
|----------|------|
| strong_match | 216 |
| partial | 149 |
| mismatch | 44 |
| no_trajectory | 21 |

## 六、合规性分布

| 合规状态 | 数量 |
|----------|------|
| pass | 734 |
| fail | 91 |
| warn | 48 |

## 七、C级卡明细（需修复，共 91 张）

| task_id | worker | status | 问题 |
|---------|--------|--------|------|
| apisix-dashboard-3321 | worker-01 | completed | #6, #10 |
| mini-qr-219 | worker-01 | completed | #6 |
| open5e-721 | worker-01 | completed | #9 |
| open5e-747 | worker-01 | completed | #9, #10 |
| open5e-803 | worker-01 | completed | #9 |
| Analog-259 | worker-02 | failed | #9 |
| BongoCat-431 | worker-02 | failed | #9 |
| ByteStash-171 | worker-02 | completed | #9 |
| ByteStash-46 | worker-02 | completed | #9 |
| Dante-128 | worker-02 | failed | #9 |
| Piped-3715 | worker-02 | completed | #9 |
| cryptgeon-150 | worker-02 | failed | #9 |
| jodit-1335 | worker-02 | done | #3 |
| kan-206 | worker-02 | failed | #9 |
| kan-23 | worker-02 | failed | #9 |
| kan-242 | worker-02 | failed | #9 |
| kan-27 | worker-02 | failed | #9 |
| kan-30 | worker-02 | failed | #9 |
| medium-editor-1047 | worker-02 | completed | #9 |
| mint-ui-366 | worker-02 |  | #2, #3 |
| next-redux-wrapper-325 | worker-02 | failed | #9 |
| open5e-622 | worker-02 | completed | #9, #10 |
| open5e-721 | worker-02 | completed | #9 |
| open5e-747 | worker-02 | completed | #9 |
| open5e-803 | worker-02 | completed | #9 |
| org-chart-69 | worker-02 | completed | #9 |
| slickgpt-38 | worker-02 | completed | #9 |
| Analog-259 | worker-03 | failed | #9 |
| ByteStash-157 | worker-03 | completed | #9 |
| ByteStash-171 | worker-03 | completed | #9 |
| ByteStash-46 | worker-03 | completed | #9 |
| ByteStash-58 | worker-03 | completed | #9 |
| Nucleus-26 | worker-03 | completed | #9 |
| editor-542 | worker-03 | completed | #9 |
| editor-893 | worker-03 | completed | #9 |
| emoji-mart-219 | worker-03 | completed | #9 |
| emoji-mart-254 | worker-03 | completed | #9 |
| emoji-mart-327 | worker-03 | completed | #9 |
| emoji-mart-762 | worker-03 | completed | #9 |
| kalendar-75 | worker-03 | completed | #9 |
| next-redux-wrapper-325 | worker-03 | completed | #9 |
| svelte-splitpanes-3 | worker-03 | completed | #9 |
| org-chart-215 | worker-04 | completed | #9 |
| ByteStash-156 | worker-05 | completed | #9 |
| ByteStash-157 | worker-05 | completed | #9 |
| ByteStash-173 | worker-05 | completed | #9, #10 |
| ByteStash-46 | worker-05 | completed | #9 |
| ByteStash-58 | worker-05 | completed | #9, #10 |
| monaco-editor-auto-typings-32 | worker-05 | completed | #9 |
| shadcn-ui-expansions-171 | worker-05 | completed | #9 |

*（共 91 张，仅展示前 50 张，完整列表见 CSV）*

## 八、D级卡明细（无轨迹，共 15 张）

| task_id | worker | mano_cua_status |
|---------|--------|-----------------|
| rich-markdown-editor-489 | worker-02 | ERROR |
| a11y.css-227 | worker-05 | STOPPED_BY_USER |
| beercss-558 | worker-05 | STOPPED_BY_USER |
| svelte-typeahead-11 | worker-05 | STOPPED_BY_USER |
| org-chart-290 | worker-07 | COMPLETED |
| TiddlyWiki5-9521 | worker-08 | TIMEOUT |
| gitlight-131 | worker-08 | TIMEOUT |
| lumen-300 | worker-08 | TIMEOUT |
| openclaw-nerve-140 | worker-08 | TIMEOUT |
| react-timeline-9000-35 | worker-08 | TIMEOUT |
| vue-pdf-98 | worker-08 | TIMEOUT |
| vue-slick-carousel-63 | worker-08 | TIMEOUT |
| vue-pdf-125 | worker-09 | KILLED |
| ide-9 | worker-fabrice | KILLED |
| media-chrome-697 | worker-fabrice | STOPPED |

---

## 九、分 Worker 评级分布

| Worker | A | B | C | D | 总计 |
|--------|---|---|---|---|------|
| worker-01 | 69 | 1 | 5 | 0 | 75 |
| worker-02 | 96 | 8 | 22 | 1 | 127 |
| worker-03 | 81 | 2 | 15 | 0 | 98 |
| worker-04 | 44 | 4 | 1 | 0 | 49 |
| worker-05 | 64 | 6 | 9 | 3 | 82 |
| worker-06 | 70 | 0 | 10 | 0 | 80 |
| worker-07 | 58 | 4 | 5 | 1 | 68 |
| worker-08 | 89 | 0 | 5 | 7 | 101 |
| worker-09 | 114 | 0 | 14 | 1 | 129 |
| worker-fabrice | 51 | 6 | 5 | 2 | 64 |

---

## 附录：compliance_issues 编号对照表

| 编号 | 含义 | 严重度 |
|------|------|--------|
| #2 | 必填字段缺失 | 🔴 |
| #3 | status 值非法（不是 completed/failed） | 🔴 |
| #4 | completed 卡 mano_cua 不完整 | 🔴 |
| #5 | mano_cua.result 值非法 | 🔴 |
| #6 | sess_id 格式不合规 | 🔴 |
| #7 | failed 卡 failure 字段不完整 | 🔴 |
| #9 | task_id 跨 worker 重复 | 🟡 |
| #10 | total_steps > 80 | 🟡 |
| #11 | status=completed 但 result=deploy_failed（逻辑矛盾） | 🔴 |
| #14 | timestamp 非标准 ISO 8601 | 🟡 |
| #15 | failed 卡 mano_cua 非 null | 🟡 |
| #16 | failed 卡 sess_id 非 null | 🟡 |

> 🔴 = 触发 C 级评级，🟡 = 触发 B 级评级

---

*数据文件：*
- CSV: `reports/integrated-assessment-20260420.csv`
- JSON: `reports/integrated-assessment-20260420.json`
