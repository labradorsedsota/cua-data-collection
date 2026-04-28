# BugHunt Result 整合评估报告

> 生成时间：2026-04-28 14:57  
> 数据源：results/ 全量 1825 张卡 × (合规检查 + 轨迹匹配 + 去重)

---

## 一、综合评级

| 评级 | 含义 | 数量 | 占比 |
|------|------|------|------|
| ✅ A级 | 可交付 | 1478 | 81.0% |
| 🟡 B级 | 有瑕疵 | 54 | 3.0% |
| 🔴 C级 | 需修复 | 193 | 10.6% |
| ⚫ D级 | 无轨迹 | 100 | 5.5% |

---

## 二、result 卡 status 分布

| status | 数量 |
|--------|------|
| completed | 913 |
| failed | 882 |
| deploy_failed | 28 |
| done | 1 |
|  | 1 |

## 三、mano_cua.status 分布（仅 completed 卡）

| mano_cua.status | 数量 |
|-----------------|------|
| COMPLETED | 706 |
| STOPPED_BY_USER | 59 |
| SKIPPED | 38 |
| TIMEOUT | 24 |
| ERROR | 21 |
| NOT_RUN | 18 |
| not_started | 15 |
| KILLED | 14 |
| STOPPED | 13 |
| HARD_TIMEOUT | 7 |
| DONE | 6 |
| STOPPED_BY_TIMEOUT | 4 |
| SIGKILL | 4 |
| STOPPED_STEP_LIMIT | 2 |
| NOT_EXECUTED | 2 |
| MAX_STEPS_REACHED | 2 |
| TERMINATED | 1 |
| KILLED_MAX_STEPS | 1 |
| DEPLOY_FAILED_SOURCE_VERIFIED | 1 |
| KILLED_AT_135 | 1 |
| KILLED_AT_105 | 1 |
| KILLED_AT_127 | 1 |
| KILLED_AT_133 | 1 |

## 四、mano_cua.result 分布

| result | 数量 |
|--------|------|
| abnormal | 431 |
| unclear | 280 |
| normal | 207 |
| deploy_failed | 16 |
| has_bug | 6 |
| no_bug | 2 |

## 五、轨迹匹配情况（completed 卡）

| 匹配结果 | 数量 |
|----------|------|
| match | 776 |
| N/A | 100 |
| mismatch | 25 |
| error | 10 |
| no_data | 2 |

## 六、合规性分布

| 合规状态 | 数量 |
|----------|------|
| pass | 1475 |
| fail | 230 |
| warn | 120 |

## 七、C级卡明细（需修复，共 193 张）

| task_id | worker | status | 问题 |
|---------|--------|--------|------|
| heynote-434 | worker-01 | completed |  |
| mapbox-gl-draw-1124 | worker-01 | failed | #7, #16 |
| mapbox-gl-draw-571 | worker-01 | failed | #7, #16 |
| Semantic-UI-React-3750 | worker-02 | completed |  |
| editable-72 | worker-02 | failed | #2, #7 |
| editable-pr129 | worker-02 | failed | #2, #7 |
| jodit-1335 | worker-02 | done | #3 |
| kirimase-163 | worker-02 | deploy_failed | #2, #3 |
| mavonEditor-737 | worker-02 | failed | #7 |
| mini-media-player-784 | worker-02 | deploy_failed | #2, #3 |
| mint-ui-366 | worker-02 |  | #2, #3 |
| open5e-622 | worker-02 | completed | #9, #10 |
| open5e-716 | worker-02 | completed | #10 |
| react-boilerplate-126 | worker-02 | completed |  |
| react-boilerplate-pr2810 | worker-02 | completed |  |
| react-slick-1881 | worker-02 | completed |  |
| teleport-code-generators-209 | worker-02 | failed | #2, #7 |
| teleport-code-generators-213 | worker-02 | failed | #2, #7 |
| teleport-code-generators-245 | worker-02 | failed | #2, #7 |
| teleport-code-generators-266 | worker-02 | failed | #2, #7 |
| twin.macro-528 | worker-02 | failed | #2, #7 |
| twin.macro-576 | worker-02 | failed | #2, #7 |
| twin.macro-pr252 | worker-02 | failed | #2, #7 |
| twin.macro-pr692 | worker-02 | failed | #2, #7 |
| uimix-pr134 | worker-02 | failed | #2, #7 |
| uimix-pr164 | worker-02 | failed | #2, #7 |
| uimix-pr17 | worker-02 | failed | #2, #7 |
| uimix-pr178 | worker-02 | failed | #2, #7 |
| uimix-pr41 | worker-02 | failed | #2, #7 |
| uimix-pr50 | worker-02 | failed | #2, #7 |
| uimix-pr95 | worker-02 | failed | #2, #7 |
| webmail-189 | worker-02 | failed | #2, #7 |
| webmail-192 | worker-02 | failed | #2, #7 |
| webmail-196 | worker-02 | failed | #2, #7 |
| webmail-207 | worker-02 | failed | #2, #7 |
| webmail-84 | worker-02 | failed | #2, #7 |
| webmail-pr169 | worker-02 | failed | #2, #7 |
| x-render-597 | worker-02 | failed | #2, #7 |
| x-render-934 | worker-02 | failed | #2, #7 |
| x-render-pr1572 | worker-02 | failed | #2, #7 |
| x-render-pr1582 | worker-02 | failed | #2, #7 |
| x-render-pr1666 | worker-02 | failed | #2, #7 |
| x-render-pr1677 | worker-02 | failed | #2, #7 |
| x-render-pr1686 | worker-02 | failed | #2, #7 |
| DocFlow-306 | worker-03 | failed | #2, #7 |
| DocFlow-pr245 | worker-03 | failed | #2, #7 |
| DocFlow-pr280 | worker-03 | failed | #2, #7 |
| DocFlow-pr281 | worker-03 | failed | #2, #7 |
| DocFlow-pr284 | worker-03 | failed | #2, #7 |
| cboard-1752 | worker-03 | completed |  |

*（共 193 张，仅展示前 50 张，完整列表见 CSV）*

## 八、D级卡明细（无轨迹，共 100 张）

| task_id | worker | mano_cua_status |
|---------|--------|-----------------|
| apisix-dashboard-3321 | worker-01 | STOPPED_BY_USER |
| leaflet-geoman-1521 | worker-01 | STOPPED_BY_USER |
| mini-qr-219 | worker-01 | STOPPED_BY_USER |
| ngx-progressbar-88 | worker-01 | SKIPPED |
| nuxt-95 | worker-01 | STOPPED_BY_USER |
| pwa-module-pr354 | worker-01 | SKIPPED |
| pwa-module-pr428 | worker-01 | SKIPPED |
| sanity-690 | worker-01 | SKIPPED |
| svelte-sonner-pr173 | worker-01 | STOPPED_BY_USER |
| the-graph-174 | worker-01 | STOPPED_BY_USER |
| the-graph-pr122 | worker-01 | SKIPPED |
| tiny-editor-417 | worker-01 | STOPPED_BY_USER |
| vuetify-module-pr300 | worker-01 | SKIPPED |
| mavonEditor-pr667 | worker-02 | TIMEOUT |
| mavonEditor-pr717 | worker-02 | SKIPPED |
| react-dropzone-911 | worker-02 | TIMEOUT |
| rich-markdown-editor-489 | worker-02 | ERROR |
| tikzcd-editor-pr5 | worker-02 | SKIPPED |
| tracktor-pr139 | worker-02 | TIMEOUT |
| vue-trix-pr18 | worker-02 | SKIPPED |
| vuefinder-pr8 | worker-02 | SKIPPED |
| wuffle-142 | worker-02 | SKIPPED |
| qinglong-pr2811 | worker-03 | COMPLETED |
| svelte-splitpanes-3 | worker-03 | KILLED_MAX_STEPS |
| unplugin-icons-338 | worker-03 | SKIPPED |
| wuffle-161 | worker-03 | SKIPPED |
| coracle-517 | worker-04 | SKIPPED |
| coracle-524 | worker-04 | SKIPPED |
| coracle-526 | worker-04 | SKIPPED |
| coracle-530 | worker-04 | SKIPPED |
| coracle-pr396 | worker-04 | SKIPPED |
| coracle-pr496 | worker-04 | SKIPPED |
| discord-data-package-explorer-pr11 | worker-04 | SKIPPED |
| org-chart-215 | worker-04 | STOPPED_BY_USER |
| a11y.css-227 | worker-05 | STOPPED_BY_USER |
| beercss-558 | worker-05 | STOPPED_BY_USER |
| inspira-ui-pr260 | worker-05 | COMPLETED |
| react-dropzone-1449 | worker-05 | COMPLETED |
| react-dropzone-526 | worker-05 | SKIPPED |
| svelte-typeahead-11 | worker-05 | STOPPED_BY_USER |
| wuffle-245 | worker-05 | SKIPPED |
| BongoCat-437 | worker-06 | COMPLETED |
| nuxtr-vscode-106 | worker-06 | STOPPED_BY_USER |
| nuxtr-vscode-119 | worker-06 | SKIPPED |
| nuxtr-vscode-128 | worker-06 | SKIPPED |
| nuxtr-vscode-62 | worker-06 | SKIPPED |
| obsidian-annotator-70 | worker-06 | SKIPPED |
| obsidian-annotator-pr220 | worker-06 | SKIPPED |
| obsidian-annotator-pr231 | worker-06 | SKIPPED |
| obsidian-annotator-pr268 | worker-06 | SKIPPED |
| pump.io-pr926 | worker-06 | TIMEOUT |
| vue-notion-pr46 | worker-06 | SKIPPED |
| vue-notion-pr57 | worker-06 | SKIPPED |
| AlgerMusicPlayer-43 | worker-07 | STOPPED |
| Armoria-pr132 | worker-07 | STOPPED |
| open5e-622 | worker-07 | COMPLETED |
| org-chart-290 | worker-07 | COMPLETED |
| pixel-editor-pr70 | worker-07 | COMPLETED |
| pixel-editor-pr77 | worker-07 | COMPLETED |
| reactour-pr405 | worker-07 | COMPLETED |
| reactour-pr529 | worker-07 | COMPLETED |
| svelty-picker-pr156 | worker-07 | DEPLOY_FAILED_SOURCE_VERIFIED |
| tiny-editor-294 | worker-07 | MAX_STEPS_REACHED |
| viewtube-2312 | worker-07 | COMPLETED |
| visual-drag-demo-pr133 | worker-07 | MAX_STEPS_REACHED |
| TiddlyWiki5-9521 | worker-08 | TIMEOUT |
| chronoframe-pr273 | worker-08 | TIMEOUT |
| gitlight-131 | worker-08 | TIMEOUT |
| lumen-300 | worker-08 | TIMEOUT |
| ngx-loading-bar-40 | worker-08 | KILLED_AT_135 |
| ngx-loading-bar-85 | worker-08 | KILLED_AT_105 |
| ngx-loading-bar-pr159 | worker-08 | KILLED_AT_127 |
| nomie6-oss-58 | worker-08 | KILLED_AT_133 |
| openclaw-nerve-140 | worker-08 | TIMEOUT |
| react-timeline-9000-35 | worker-08 | TIMEOUT |
| vue-pdf-98 | worker-08 | TIMEOUT |
| vue-slick-carousel-63 | worker-08 | TIMEOUT |
| Markpad-21 | worker-09 | SIGKILL |
| boardgame.io-810 | worker-09 | STOPPED |
| conform-469 | worker-09 | STOPPED |
| hastic-grafana-app-223 | worker-09 |  |
| hastic-grafana-app-275 | worker-09 |  |
| hastic-grafana-app-324 | worker-09 |  |
| lenis-pr507 | worker-09 |  |
| preact-2949 | worker-09 |  |
| preact-4111 | worker-09 |  |
| preact-4422 | worker-09 |  |
| react-charts-pr29 | worker-09 |  |
| react-datetime-picker-180 | worker-09 |  |
| reui-pr17 | worker-09 |  |
| reui-pr18 | worker-09 |  |
| reui-pr38 | worker-09 |  |
| reui-pr5 | worker-09 |  |
| reui-pr82 | worker-09 |  |
| vue-pdf-125 | worker-09 | KILLED |
| CodeFlask-pr35 | worker-fabrice | COMPLETED |
| CodeFlask-pr38 | worker-fabrice | COMPLETED |
| CodeFlask-pr41 | worker-fabrice | COMPLETED |
| ide-9 | worker-fabrice | KILLED |
| media-chrome-697 | worker-fabrice | STOPPED |

---

## 九、分 Worker 评级分布

| Worker | A | B | C | D | 总计 |
|--------|---|---|---|---|------|
| worker-01 | 145 | 2 | 3 | 13 | 163 |
| worker-02 | 192 | 10 | 41 | 9 | 252 |
| worker-03 | 189 | 4 | 34 | 4 | 231 |
| worker-04 | 98 | 4 | 15 | 8 | 125 |
| worker-05 | 125 | 11 | 11 | 7 | 154 |
| worker-06 | 155 | 2 | 19 | 12 | 188 |
| worker-07 | 141 | 7 | 19 | 12 | 179 |
| worker-08 | 157 | 1 | 7 | 12 | 177 |
| worker-09 | 191 | 6 | 35 | 18 | 250 |
| worker-fabrice | 85 | 7 | 9 | 5 | 106 |

---

*数据文件：*
- CSV: `reports/integrated-assessment/integrated-assessment-20260428.csv`
- JSON: `reports/integrated-assessment/integrated-assessment-20260428.json`
