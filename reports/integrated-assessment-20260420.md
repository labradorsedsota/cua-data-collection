# BugHunt Result 整合评估报告

> 生成时间：2026-04-20 16:35  
> 数据源：results/ 全量 873 张卡 × (合规检查 + LLM轨迹匹配 + 去重)  
> 匹配模型：claude-haiku-4-5  

---

## 一、综合评级

| 评级 | 含义 | 数量 | 占比 |
|------|------|------|------|
| ✅ A级 | 可交付 | 709 | 81.2% |
| 🟡 B级 | 有瑕疵 | 123 | 14.1% |
| 🔴 C级 | 需修复 | 20 | 2.3% |
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

## 五、轨迹匹配情况（completed 卡，LLM 判定）

| 匹配结果 | 数量 |
|----------|------|
| match | 364 |
| no_trajectory | 19 |
| strong_match | 18 |
| mismatch | 15 |
| partial | 9 |
| error | 3 |
| no_data | 2 |

## 六、合规性分布

| 合规状态 | 数量 |
|----------|------|
| pass | 734 |
| warn | 132 |
| fail | 7 |

## 七、C级卡明细（需修复，共 20 张）

| task_id | worker | status | 问题 | 匹配结果 |
|---------|--------|--------|------|----------|
| Semantic-UI-React-3750 | worker-02 | completed |  | mismatch |
| editor.js-2084 | worker-02 | completed |  | mismatch |
| jodit-1335 | worker-02 | done | #3 | N/A |
| mint-ui-366 | worker-02 |  | #2, #3 | N/A |
| open5e-622 | worker-02 | completed | #9, #10 | mismatch |
| open5e-716 | worker-02 | completed | #10 | mismatch |
| cboard-1752 | worker-03 | completed |  | mismatch |
| emoji-mart-218 | worker-03 | completed | #10 | mismatch |
| beercss-532 | worker-05 | completed |  | mismatch |
| ebook-reader-287 | worker-05 | completed | #10 | mismatch |
| mint-ui-290 | worker-07 | failed | #7, #15 | N/A |
| mint-ui-628 | worker-07 | failed | #7, #15 | N/A |
| mint-ui-304 | worker-08 | failed | #7, #15, #16 | N/A |
| tailwindcss-987 | worker-08 | completed |  | mismatch |
| editor-542 | worker-09 | completed | #9 | mismatch |
| emoji-mart-220 | worker-09 | completed |  | mismatch |
| multiple-select-407 | worker-09 | completed |  | mismatch |
| openclaw-nerve-27 | worker-09 | completed |  | mismatch |
| website-4366 | worker-09 | completed |  | mismatch |
| vcal-350 | worker-fabrice | completed |  | mismatch |

## 八、D级卡明细（无轨迹，共 21 张）

| task_id | worker | mano_cua_status |
|---------|--------|-----------------|
| apisix-dashboard-3321 | worker-01 | STOPPED_BY_USER |
| mini-qr-219 | worker-01 | STOPPED_BY_USER |
| rich-markdown-editor-489 | worker-02 | ERROR |
| svelte-splitpanes-3 | worker-03 | KILLED_MAX_STEPS |
| org-chart-215 | worker-04 | STOPPED_BY_USER |
| a11y.css-227 | worker-05 | STOPPED_BY_USER |
| beercss-558 | worker-05 | STOPPED_BY_USER |
| svelte-typeahead-11 | worker-05 | STOPPED_BY_USER |
| open5e-622 | worker-07 | COMPLETED |
| org-chart-290 | worker-07 | COMPLETED |
| TiddlyWiki5-9521 | worker-08 | TIMEOUT |
| gitlight-131 | worker-08 | TIMEOUT |
| lumen-300 | worker-08 | TIMEOUT |
| openclaw-nerve-140 | worker-08 | TIMEOUT |
| react-timeline-9000-35 | worker-08 | TIMEOUT |
| vue-pdf-98 | worker-08 | TIMEOUT |
| vue-slick-carousel-63 | worker-08 | TIMEOUT |
| Markpad-21 | worker-09 | SIGKILL |
| vue-pdf-125 | worker-09 | KILLED |
| ide-9 | worker-fabrice | KILLED |
| media-chrome-697 | worker-fabrice | STOPPED |

## 九、轨迹不匹配卡明细（LLM 判定 mismatch，共 15 张）

| task_id | worker | confidence | reason |
|---------|--------|------------|--------|
| Semantic-UI-React-3750 | worker-02 | 0.85 | 任务卡重点测试嵌套shorthand props设置input ref的属性保留行为，而轨迹任务重点测试搜索功能的完整流程，两者测试焦点和验证目标不同。 |
| editor.js-2084 | worker-02 | 0.00 | N/A |
| open5e-622 | worker-02 | 0.85 | 轨迹中的任务在第5步额外增加了'用DevTools检查逗号元素的CSS属性'的要求，而任务卡描述中明确禁止打开Terminal或其他应用程序，DevTools检查违反了此约束。 |
| open5e-716 | worker-02 | 0.85 | 任务卡禁止打开DevTools，但轨迹中第4步要求打开DevTools检查Console错误，这是核心差异。 |
| cboard-1752 | worker-03 | 0.85 | 任务卡要求验证开关状态持久化（切换后离开再重新进入应显示相同状态），而轨迹任务仅要求验证切换时的即时状态变更，两者验证重点不同。 |
| emoji-mart-218 | worker-03 | 0.00 | N/A |
| beercss-532 | worker-05 | 0.85 | 轨迹描述中button测试目标是'观察是否保持高亮'，与任务卡要求的'恢复到正常未聚焦外观'存在矛盾，说明两者测试预期结果不一致。 |
| ebook-reader-287 | worker-05 | 0.00 | N/A |
| tailwindcss-987 | worker-08 | 0.85 | 轨迹中要求按F12打开Console检查安全策略错误，与任务卡禁止打开Terminal或其他应用程序的要求存在矛盾，表明两者对测试方法的理解存在偏差。 |
| editor-542 | worker-09 | 0.00 | N/A |
| emoji-mart-220 | worker-09 | 0.00 | N/A |
| multiple-select-407 | worker-09 | 0.85 | 任务卡仅要求测试Basic example的多选功能，而轨迹中的实际任务扩展了测试范围，额外包含了With OptGroups和Single Select部分的测试，超出了原始任务描述的范围。 |
| openclaw-nerve-27 | worker-09 | 0.92 | 任务卡要求测试Memory查看功能的基本流程（导航、查看列表、点击查看详情），而轨迹任务额外要求执行DevTools Console命令修改DOM状态，这是完全不同的操作路径和测试目标。 |
| website-4366 | worker-09 | 0.99 | 两段文本描述的是完全不同的功能测试：任务卡描述的是Newsletter邮件订阅功能，而轨迹中的实际任务是搜索功能测试，两者在测试目标、操作步骤和验证点上都没有重叠。 |
| vcal-350 | worker-fabrice | 0.85 | 任务卡要求检查选中和悬停两种状态的高亮效果，而轨迹中的实际任务仅描述了选中状态的检查，缺少悬停状态的验证要求。 |

## 十、分 Worker 评级分布

| Worker | A | B | C | D | 总计 |
|--------|---|---|---|---|------|
| worker-01 | 69 | 4 | 0 | 2 | 75 |
| worker-02 | 92 | 28 | 6 | 1 | 127 |
| worker-03 | 80 | 15 | 2 | 1 | 98 |
| worker-04 | 31 | 17 | 0 | 1 | 49 |
| worker-05 | 62 | 15 | 2 | 3 | 82 |
| worker-06 | 69 | 11 | 0 | 0 | 80 |
| worker-07 | 58 | 6 | 2 | 2 | 68 |
| worker-08 | 88 | 4 | 2 | 7 | 101 |
| worker-09 | 110 | 12 | 5 | 2 | 129 |
| worker-fabrice | 50 | 11 | 1 | 2 | 64 |

---

## 附录：compliance_issues 编号对照表

| 编号 | 含义 | 严重度 |
|------|------|--------|
| #2 | 必填字段缺失 | 🔴 C级 |
| #3 | status 值非法（不是 completed/failed） | 🔴 C级 |
| #4 | completed 卡 mano_cua 不完整 | 🔴 C级 |
| #5 | mano_cua.result 值非法 | 🔴 C级 |
| #6 | sess_id 格式不合规 | 🔴 C级 |
| #7 | failed 卡 failure 字段不完整 | 🔴 C级 |
| #9 | task_id 跨 worker 重复 | 🟡 B级 |
| #10 | total_steps > 80 | 🟡 B级 |
| #11 | status=completed 但 result=deploy_failed（逻辑矛盾） | 🔴 C级 |
| #14 | timestamp 非标准 ISO 8601 | 🟡 B级 |
| #15 | failed 卡 mano_cua 非 null | 🟡 B级 |
| #16 | failed 卡 sess_id 非 null | 🟡 B级 |

> 评级优先级：D > C > B > A（取最严重等级）

---

*数据文件：*
- CSV: reports/integrated-assessment-20260420.csv
- JSON: reports/integrated-assessment-20260420.json
- LLM匹配详情: reports/llm-match-report-20260420.json
