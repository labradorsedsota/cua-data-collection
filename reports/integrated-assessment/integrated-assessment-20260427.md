# BugHunt Result 整合评估报告

> 生成时间：2026-04-27 15:11  
> 数据源：results/ 全量 1781 张卡 × (合规检查 + 轨迹匹配 + 去重)

---

## 一、综合评级

| 评级 | 含义 | 数量 | 占比 |
|------|------|------|------|
| ✅ A级 | 可交付 | 1267 | 71.1% |
| 🟡 B级 | 有瑕疵 | 39 | 2.2% |
| 🔴 C级 | 需修复 | 258 | 14.5% |
| ⚫ D级 | 无轨迹 | 217 | 12.2% |

---

## 二、result 卡 status 分布

| status | 数量 |
|--------|------|
| completed | 941 |
| failed | 826 |
| deploy_failed | 11 |
| done | 1 |
|  | 1 |
| PARSE_ERROR | 1 |

## 三、mano_cua.status 分布（仅 completed 卡）

| mano_cua.status | 数量 |
|-----------------|------|
| COMPLETED | 662 |
| SKIPPED | 83 |
| STOPPED_BY_USER | 74 |
| ERROR | 29 |
| TIMEOUT | 26 |
| not_started | 15 |
| STOPPED | 14 |
| STOPPED_BY_TIMEOUT | 11 |
| KILLED | 8 |
| HARD_TIMEOUT | 8 |
| NOT_RUN | 8 |
| KILLED_AT_80 | 8 |
| DONE | 6 |
| SIGKILL | 4 |
| FAILED | 3 |
| SKIPPED_SAME_COMMIT | 2 |
| SKIPPED_REPO_FUSE | 2 |
| STOPPED_STEP_LIMIT | 2 |
| NOT_EXECUTED | 2 |
| TERMINATED | 1 |
| KILLED_MAX_STEPS | 1 |
| MAX_STEPS | 1 |

## 四、mano_cua.result 分布

| result | 数量 |
|--------|------|
| abnormal | 378 |
| unclear | 294 |
| normal | 204 |
| deploy_failed | 48 |
| has_bug | 14 |
| reproduced | 8 |
| no_bug | 5 |

## 五、轨迹匹配情况（completed 卡）

| 匹配结果 | 数量 |
|----------|------|
| match | 696 |
| N/A | 216 |
| mismatch | 24 |
| error | 5 |

## 六、合规性分布

| 合规状态 | 数量 |
|----------|------|
| pass | 1266 |
| fail | 393 |
| warn | 122 |

## 七、C级卡明细（需修复，共 258 张）

| task_id | worker | status | 问题 |
|---------|--------|--------|------|
| mapbox-gl-draw-1124 | worker-01 | failed | #7, #16 |
| mapbox-gl-draw-571 | worker-01 | failed | #7, #16 |
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
| editable-72 | worker-02 | failed | #2, #7 |
| editable-pr129 | worker-02 | failed | #2, #7 |
| jodit-1335 | worker-02 | done | #3 |
| kan-206 | worker-02 | failed | #9 |
| kan-23 | worker-02 | failed | #9 |
| kan-242 | worker-02 | failed | #9 |
| kan-27 | worker-02 | failed | #9 |
| kan-30 | worker-02 | failed | #9 |
| kirimase-163 | worker-02 | deploy_failed | #2, #3 |
| mavonEditor-737 | worker-02 | failed | #7 |
| medium-editor-1047 | worker-02 | completed | #9 |
| mini-media-player-784 | worker-02 | deploy_failed | #2, #3 |
| mint-ui-366 | worker-02 |  | #2, #3 |
| next-redux-wrapper-325 | worker-02 | failed | #9 |
| open5e-622 | worker-02 | completed | #9, #10 |
| open5e-721 | worker-02 | completed | #9 |
| open5e-747 | worker-02 | completed | #9 |
| open5e-803 | worker-02 | completed | #9 |
| org-chart-69 | worker-02 | completed | #9 |
| slickgpt-38 | worker-02 | completed | #9 |
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

*（共 258 张，仅展示前 50 张，完整列表见 CSV）*

## 八、D级卡明细（无轨迹，共 217 张）

| task_id | worker | mano_cua_status |
|---------|--------|-----------------|
| apisix-dashboard-3321 | worker-01 | STOPPED_BY_USER |
| leaflet-geoman-1348 | worker-01 | ERROR |
| mini-qr-219 | worker-01 | STOPPED_BY_USER |
| svelte-sonner-pr173 | worker-01 | STOPPED_BY_USER |
| the-graph-174 | worker-01 | STOPPED_BY_USER |
| the-graph-pr122 | worker-01 | ERROR |
| editable-81 | worker-02 | SKIPPED |
| jingo-pr189 | worker-02 | STOPPED_BY_TIMEOUT |
| mavonEditor-649 | worker-02 | STOPPED_BY_USER |
| mavonEditor-729 | worker-02 | STOPPED_BY_USER |
| mavonEditor-pr640 | worker-02 | STOPPED_BY_USER |
| mavonEditor-pr661 | worker-02 | STOPPED_BY_TIMEOUT |
| mavonEditor-pr717 | worker-02 | SKIPPED |
| mission-control-456 | worker-02 | STOPPED_BY_TIMEOUT |
| react-boilerplate-pr2810 | worker-02 | SKIPPED |
| react-slick-pr2149 | worker-02 | STOPPED_BY_TIMEOUT |
| react-slick-pr622 | worker-02 | STOPPED_BY_TIMEOUT |
| rich-markdown-editor-489 | worker-02 | ERROR |
| tikzcd-editor-pr5 | worker-02 | SKIPPED |
| vue-trix-pr18 | worker-02 | SKIPPED |
| whiteboard-13 | worker-02 | SKIPPED |
| gridsheet-pr105 | worker-03 | COMPLETED |
| mui-tiptap-334 | worker-03 | ERROR |
| ngx-infinite-scroll-40 | worker-03 | SKIPPED |
| ngx-infinite-scroll-pr235 | worker-03 | SKIPPED |
| ngx-infinite-scroll-pr262 | worker-03 | SKIPPED |
| ngx-infinite-scroll-pr282 | worker-03 | SKIPPED |
| ngx-infinite-scroll-pr369 | worker-03 | SKIPPED |
| ngx-infinite-scroll-pr386 | worker-03 | SKIPPED |
| ngx-scrollbar-674 | worker-03 | COMPLETED |
| svelte-splitpanes-3 | worker-03 | KILLED_MAX_STEPS |
| Eve-586 | worker-04 | COMPLETED |
| Eve-703 | worker-04 | SKIPPED |
| Eve-704 | worker-04 | SKIPPED |
| Eve-834 | worker-04 | SKIPPED |
| Eve-835 | worker-04 | SKIPPED |
| Eve-837 | worker-04 | SKIPPED |
| Eve-pr736 | worker-04 | SKIPPED |
| Eve-pr877 | worker-04 | SKIPPED |
| am-editor-pr245 | worker-04 | SKIPPED |
| am-editor-pr305 | worker-04 | SKIPPED |
| am-editor-pr36 | worker-04 | SKIPPED |
| apollo-pr274 | worker-04 | SKIPPED |
| apollo-pr330 | worker-04 | SKIPPED |
| apollo-pr362 | worker-04 | SKIPPED |
| axios-module-pr364 | worker-04 | SKIPPED |
| axios-module-pr414 | worker-04 | SKIPPED |
| axios-module-pr424 | worker-04 | SKIPPED |
| coracle-474 | worker-04 | ERROR |
| coracle-517 | worker-04 | SKIPPED |
| coracle-524 | worker-04 | SKIPPED |
| coracle-526 | worker-04 | SKIPPED |
| coracle-530 | worker-04 | SKIPPED |
| coracle-pr396 | worker-04 | SKIPPED |
| coracle-pr496 | worker-04 | SKIPPED |
| discord-data-package-explorer-pr11 | worker-04 | SKIPPED |
| discord-data-package-explorer-pr30 | worker-04 | SKIPPED |
| drawnix-141 | worker-04 | COMPLETED |
| drawnix-pr274 | worker-04 | COMPLETED |
| drawnix-pr318 | worker-04 | STOPPED_BY_USER |
| drawnix-pr333 | worker-04 | STOPPED_BY_USER |
| drawnix-pr368 | worker-04 | COMPLETED |
| fonts-371 | worker-04 | SKIPPED |
| fonts-382 | worker-04 | SKIPPED |
| fonts-pr274 | worker-04 | SKIPPED |
| heynote-132 | worker-04 | SKIPPED |
| heynote-195 | worker-04 | STOPPED_BY_USER |
| heynote-21 | worker-04 | ERROR |
| heynote-357 | worker-04 | TIMEOUT |
| inspira-ui-pr260 | worker-04 | SKIPPED |
| inspira-ui-pr263 | worker-04 | SKIPPED |
| inspira-ui-pr268 | worker-04 | SKIPPED |
| ngx-progressbar-66 | worker-04 | SKIPPED |
| ngx-progressbar-88 | worker-04 | SKIPPED |
| ngx-progressbar-pr119 | worker-04 | SKIPPED |
| ngx-progressbar-pr278 | worker-04 | SKIPPED |
| nuxt-95 | worker-04 | COMPLETED |
| nuxt-pr162 | worker-04 | COMPLETED |
| org-chart-215 | worker-04 | STOPPED_BY_USER |
| pwa-module-pr354 | worker-04 | SKIPPED |
| pwa-module-pr386 | worker-04 | SKIPPED |
| pwa-module-pr417 | worker-04 | SKIPPED |
| pwa-module-pr428 | worker-04 | SKIPPED |
| svelte-toast-pr52 | worker-04 | COMPLETED |
| unplugin-icons-338 | worker-04 | SKIPPED |
| unplugin-icons-pr316 | worker-04 | SKIPPED |
| unplugin-icons-pr320 | worker-04 | SKIPPED |
| unplugin-icons-pr356 | worker-04 | SKIPPED |
| vue-element-plus-admin-316 | worker-04 | HARD_TIMEOUT |
| vue-element-plus-admin-317 | worker-04 | SKIPPED_SAME_COMMIT |
| vue-element-plus-admin-318 | worker-04 | SKIPPED_SAME_COMMIT |
| vue-element-plus-admin-424 | worker-04 | SKIPPED_REPO_FUSE |
| vue-element-plus-admin-428 | worker-04 | SKIPPED_REPO_FUSE |
| vuetify-module-95 | worker-04 | SKIPPED |
| vuetify-module-pr230 | worker-04 | SKIPPED |
| vuetify-module-pr300 | worker-04 | SKIPPED |
| wuffle-142 | worker-04 | SKIPPED |
| wuffle-161 | worker-04 | SKIPPED |
| wuffle-245 | worker-04 | SKIPPED |
| OpsiMate-407 | worker-05 | COMPLETED |
| OpsiMate-408 | worker-05 | STOPPED |
| a11y.css-227 | worker-05 | STOPPED_BY_USER |
| beercss-558 | worker-05 | STOPPED_BY_USER |
| homer-pr1034 | worker-05 | COMPLETED |
| homer-pr112 | worker-05 | TIMEOUT |
| homer-pr115 | worker-05 | TIMEOUT |
| homer-pr174 | worker-05 | COMPLETED |
| react-dropzone-1449 | worker-05 | STOPPED_BY_USER |
| react-dropzone-526 | worker-05 | STOPPED_BY_USER |
| svelte-typeahead-11 | worker-05 | STOPPED_BY_USER |
| Raneto-88 | worker-06 | STOPPED_BY_USER |
| headscale-ui-pr192 | worker-06 | COMPLETED |
| muya-pr152 | worker-06 | COMPLETED |
| next-themes-85 | worker-06 | STOPPED_BY_USER |
| nuxt-social-share-175 | worker-06 | COMPLETED |
| nuxt-social-share-410 | worker-06 | TIMEOUT |
| pump.io-pr1355 | worker-06 | TIMEOUT |
| pump.io-pr1465 | worker-06 | TIMEOUT |
| pump.io-pr926 | worker-06 | TIMEOUT |
| shadcn-svelte-extras-pr361 | worker-06 | TIMEOUT |
| vue-notion-41 | worker-06 | COMPLETED |
| vue-notion-pr46 | worker-06 | COMPLETED |
| vue-notion-pr57 | worker-06 | COMPLETED |
| AlgerMusicPlayer-43 | worker-07 | STOPPED_BY_USER |
| Armoria-pr115 | worker-07 | STOPPED_BY_USER |
| Armoria-pr122 | worker-07 | STOPPED_BY_USER |
| Armoria-pr132 | worker-07 | STOPPED_BY_USER |
| Armoria-pr206 | worker-07 | STOPPED_BY_USER |
| BitFun-188 | worker-07 |  |
| open5e-622 | worker-07 | COMPLETED |
| org-chart-290 | worker-07 | COMPLETED |
| reactour-pr405 | worker-07 | STOPPED_BY_USER |
| reactour-pr448 | worker-07 | STOPPED_BY_USER |
| reactour-pr49 | worker-07 | STOPPED_BY_USER |
| reactour-pr529 | worker-07 | STOPPED_BY_USER |
| reactour-pr639 | worker-07 | STOPPED_BY_USER |
| reactour-pr660 | worker-07 | STOPPED_BY_USER |
| svelty-picker-pr156 | worker-07 | STOPPED_BY_USER |
| turnstile-250 | worker-07 | STOPPED_BY_USER |
| visual-drag-demo-pr122 | worker-07 | ERROR |
| visual-drag-demo-pr133 | worker-07 | STOPPED_BY_USER |
| visual-drag-demo-pr27 | worker-07 | STOPPED_BY_USER |
| DaybydayCRM-pr381 | worker-08 | SKIPPED |
| DaybydayCRM-pr420 | worker-08 | SKIPPED |
| TiddlyWiki5-9521 | worker-08 | TIMEOUT |
| angular-bootstrap-datetimepicker-pr426 | worker-08 | KILLED_AT_80 |
| angular-bootstrap-datetimepicker-pr49 | worker-08 | SKIPPED |
| chronoframe-92 | worker-08 | SKIPPED |
| chronoframe-pr273 | worker-08 | SKIPPED |
| evlog-160 | worker-08 | SKIPPED |
| evlog-164 | worker-08 | SKIPPED |
| github-readme-activity-graph-pr9 | worker-08 | SKIPPED |
| gitlight-131 | worker-08 | TIMEOUT |
| jsPDF-AutoTable-691 | worker-08 | COMPLETED |
| lumen-300 | worker-08 | TIMEOUT |
| medical-appointment-scheduling-131 | worker-08 | KILLED_AT_80 |
| medical-appointment-scheduling-91 | worker-08 | KILLED_AT_80 |
| mission-control-526 | worker-08 | SKIPPED |
| mission-control-529 | worker-08 | SKIPPED |
| ngx-loading-bar-40 | worker-08 | KILLED_AT_80 |
| ngx-loading-bar-43 | worker-08 | KILLED_AT_80 |
| ngx-loading-bar-65 | worker-08 | COMPLETED |
| ngx-loading-bar-85 | worker-08 | COMPLETED |
| ngx-loading-bar-pr159 | worker-08 | KILLED_AT_80 |
| nomie6-oss-23 | worker-08 | KILLED_AT_80 |
| nomie6-oss-58 | worker-08 | KILLED_AT_80 |
| nuxt-directus-144 | worker-08 | SKIPPED |
| nuxt-directus-147 | worker-08 | SKIPPED |
| nuxt-directus-157 | worker-08 | SKIPPED |
| openclaw-nerve-140 | worker-08 | TIMEOUT |
| qinglong-pr2811 | worker-08 | SKIPPED |
| qinglong-pr2833 | worker-08 | SKIPPED |
| qinglong-pr2837 | worker-08 | SKIPPED |
| react-timeline-9000-35 | worker-08 | TIMEOUT |
| vue-pdf-98 | worker-08 | TIMEOUT |
| vue-slick-carousel-63 | worker-08 | TIMEOUT |
| Markpad-21 | worker-09 | SIGKILL |
| air-datepicker-613 | worker-09 | TIMEOUT |
| air-datepicker-pr471 | worker-09 | SKIPPED |
| boardgame.io-1021 | worker-09 | COMPLETED |
| boardgame.io-782 | worker-09 | COMPLETED |
| boardgame.io-810 | worker-09 | COMPLETED |
| boardgame.io-848 | worker-09 | COMPLETED |
| boardgame.io-855 | worker-09 | COMPLETED |
| conform-454 | worker-09 | ERROR |
| conform-469 | worker-09 | STOPPED |
| hastic-grafana-app-223 | worker-09 | COMPLETED |
| hastic-grafana-app-275 | worker-09 | COMPLETED |
| hastic-grafana-app-324 | worker-09 | COMPLETED |
| laverna-351 | worker-09 | COMPLETED |
| lenis-68 | worker-09 | TIMEOUT |
| lenis-pr507 | worker-09 | SKIPPED |
| obsidian-execute-code-pr395 | worker-09 | SKIPPED |
| preact-2949 | worker-09 | COMPLETED |
| preact-4111 | worker-09 | COMPLETED |
| preact-4422 | worker-09 | COMPLETED |
| react-datetime-picker-156 | worker-09 | STOPPED |
| react-datetime-picker-40 | worker-09 | STOPPED |
| tiny-editor-108 | worker-09 | COMPLETED |
| tiny-editor-156 | worker-09 | COMPLETED |
| tiny-editor-173 | worker-09 | COMPLETED |
| tiny-editor-197 | worker-09 | COMPLETED |
| tiny-editor-201 | worker-09 | FAILED |
| tiny-editor-294 | worker-09 | FAILED |
| tiny-editor-417 | worker-09 | FAILED |
| tracktor-pr139 | worker-09 | TIMEOUT |
| vue-pdf-125 | worker-09 | KILLED |
| vuefinder-pr154 | worker-09 | STOPPED |
| vuefinder-pr49 | worker-09 | SKIPPED |
| vuefinder-pr8 | worker-09 | SKIPPED |
| vuetable-2-pr17 | worker-09 | STOPPED |
| KaibanJS-215 | worker-fabrice | COMPLETED |
| ide-9 | worker-fabrice | KILLED |
| media-chrome-697 | worker-fabrice | STOPPED |
| svelte-jsoneditor-pr184 | worker-fabrice | ERROR |
| svelte-jsoneditor-pr73 | worker-fabrice | COMPLETED |
| vuepress-theme-vdoing-pr432 | worker-fabrice | MAX_STEPS |

---

## 九、分 Worker 评级分布

| Worker | A | B | C | D | 总计 |
|--------|---|---|---|---|------|
| worker-01 | 131 | 1 | 5 | 6 | 143 |
| worker-02 | 160 | 9 | 56 | 15 | 240 |
| worker-03 | 169 | 2 | 35 | 10 | 216 |
| worker-04 | 84 | 4 | 15 | 68 | 171 |
| worker-05 | 102 | 6 | 18 | 11 | 137 |
| worker-06 | 130 | 0 | 31 | 13 | 174 |
| worker-07 | 120 | 6 | 20 | 19 | 165 |
| worker-08 | 125 | 0 | 22 | 34 | 181 |
| worker-09 | 174 | 5 | 43 | 35 | 257 |
| worker-fabrice | 72 | 6 | 13 | 6 | 97 |

---

*数据文件：*
- CSV: `reports/integrated-assessment/integrated-assessment-20260427.csv`
- JSON: `reports/integrated-assessment/integrated-assessment-20260427.json`
