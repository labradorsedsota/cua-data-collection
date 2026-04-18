# 轨迹下载与完整性分析报告

**生成时间：** 2026-04-18 21:36
**数据来源：** 火山云 TOS (`mano-tos` bucket, `trajectories/` prefix)

## 一、总览

| 指标 | 数量 |
|------|------|
| 有 sess_id 的 result 卡 | 463 |
| 去重 sess_id | 451 |
| TOS 下载成功 | 408 |
| TOS 未找到 | 43 |
| 下载失败 | 0 |
| completed 但无 sess_id | 10 |
| 本地轨迹总大小 | ~18 GB |

## 二、轨迹完整性分类

| 状态 | 卡数 | 说明 |
|------|------|------|
| ✅ normal | 418 | 轨迹完整（有截图、文件数合理） |
| ⚠️ warning | 2 | 轨迹可能不完整（截图少或体积小） |
| ❌ tos_not_found | 43 | TOS 上无此 session 轨迹 |
| ❌ abnormal/empty | 0 | 轨迹目录为空或无截图 |
| ❌ download_error | 0 | 下载过程出错 |
| ❌ no_sess_id | 10 | result 文件中无 sess_id |

**正常率：418/473 = 88.4%**

## 三、按 Worker 分布

| Worker | 总卡数 | 正常 | 警告 | 异常 | 异常率 |
|--------|--------|------|------|------|--------|
| worker-01 | 46 | 41 | 1 | 4 | 9% |
| worker-02 | 83 | 65 | 1 | 17 | 20% |
| worker-03 | 62 | 62 | 0 | 0 | 0% |
| worker-04 | 46 | 42 | 0 | 4 | 9% |
| worker-05 | 51 | 46 | 0 | 5 | 10% |
| worker-06 | 40 | 37 | 0 | 3 | 8% |
| worker-07 | 35 | 24 | 0 | 11 | 31% |
| worker-08 | 41 | 39 | 0 | 2 | 5% |
| worker-09 | 41 | 40 | 0 | 1 | 2% |
| worker-fabrice | 28 | 22 | 0 | 6 | 21% |

## 四、异常卡明细

### 4.1 TOS 未找到轨迹（43 张）

这些卡的 result 文件里有 sess_id，但 TOS 上没有对应的轨迹文件夹。

| task_id | worker | result_status | mc_status | sess_id |
|---------|--------|---------------|-----------|---------|
| Analog-135 | worker-05 | completed | ERROR | `sess-20260417231344-84e458ed3de8418ba305...` |
| BongoCat-437 | worker-06 | failed |  | `sess-20260417205152-4a44f3940fe24d0491de...` |
| ByteStash-156 | worker-02 | completed | COMPLETED | `sess-20260418010500-bytestash156...` |
| ByteStash-157 | worker-02 | completed | COMPLETED | `sess-20260418012900-bytestash157...` |
| ByteStash-173 | worker-02 | completed | COMPLETED | `sess-20260418012000-bytestash173...` |
| ByteStash-173 | worker-06 | failed |  | `sess-20260417225207-8445bc1cf786460f86e9...` |
| ByteStash-58 | worker-02 | completed | COMPLETED | `sess-20260418005400-bytestash58...` |
| Luckysheet-528 | worker-02 | completed | COMPLETED | `sess-20260418033000-luckysheet528...` |
| Markpad-21 | worker-02 | completed | COMPLETED | `sess-20260418035000-markpad21...` |
| Notpad-195 | worker-02 | completed | COMPLETED | `sess-20260418034000-notpad195...` |
| Notpad-268 | worker-02 | completed | COMPLETED | `sess-20260418034500-notpad268...` |
| Piped-3941 | worker-01 | completed | STOPPED_BY_USER | `sess-20260418120949-53ef91700c7547efa911...` |
| ant-design-vue-7574 | worker-07 | completed | STOPPED | `sess-20260417120628-69d872a9d67a4576b4af...` |
| beercss-558 | worker-08 | completed | TIMEOUT | `sess-20260417145720-f551653e459543d2ab13...` |
| betaflight-configurator-4700 | worker-04 | completed | STOPPED_BY_USER | `sess-20260417232902-9415bb96a012461c8431...` |
| charts-201 | worker-05 | completed | COMPLETED | `sess-20260417174013-826efc5a132d49ef818d...` |
| emoji-mart-218 | worker-02 | completed | COMPLETED | `sess-20260418022500-emoji218...` |
| emoji-mart-219 | worker-02 | completed | COMPLETED | `sess-20260418025500-emoji219...` |
| emoji-mart-220 | worker-02 | completed | COMPLETED | `sess-20260418023500-emoji220...` |
| emoji-mart-254 | worker-02 | completed | COMPLETED | `sess-20260418023422-707e7659ed2340a7b591...` |
| emoji-mart-327 | worker-02 | completed | COMPLETED | `sess-20260418031500-emoji327...` |
| emoji-mart-762 | worker-02 | completed | COMPLETED | `sess-20260418032000-emoji762...` |
| factoriolab-1327 | worker-07 | failed |  | `sess-20260417235236-23e34e5547b146d7bb98...` |
| fluid-player-486 | worker-07 | completed | KILLED | `sess-20260418132728-c1a8de70f19c4cebbbc9...` |
| gitlight-131 | worker-07 | completed | KILLED | `sess-20260418095159-bf731125227245ff9977...` |
| karakeep-2299 | worker-04 | completed | STOPPED_BY_USER | `sess-20260417221747-6a1a4aace073471aa0b8...` |
| lumen-254 | worker-09 | completed | KILLED | `sess-20260417203041-4ebc2ad18f6e4e5c9f13...` |
| mint-ui-754 | worker-07 | completed | COMPLETED | `sess-20260417160726-b60adcc2db8447c5a369...` |
| nuxt-module-220 | worker-08 | completed | TIMEOUT | `sess-20260417152758-f9903754a9d14c21ae94...` |
| nuxt-security-610 | worker-06 | completed | STOPPED_BY_USER | `sess-20260417185510-fc1a073eae634ef7873a...` |
| open5e-762 | worker-01 | completed | STOPPED_BY_USER | `sess-20260418010521-13ddabdfd56445169d91...` |
| open5e-799 | worker-02 | completed | COMPLETED | `sess-20260418073009-18a063d2b61f46ffab7c...` |
| react-date-picker-118 | worker-07 | completed | COMPLETED | `sess-20260417171621-2b99e8dafc3242aebf31...` |
| react-modern-calendar-datepicker-88 | worker-01 | completed | STOPPED_BY_USER | `sess-20260417202607-7309ec64d0b44a098999...` |
| runbox7-1279 | worker-fabrice | completed | COMPLETED | `sess-20260418113602-8309d57cf14b47d68b99...` |
| script-lab-609 | worker-04 | completed | STOPPED_BY_USER | `sess-20260417151710-d2703795a05c4f6cae6a...` |
| signature_pad-120 | worker-02 | completed | COMPLETED | `sess-20260418020100-sigpad120...` |
| signature_pad-120 | worker-05 | completed | COMPLETED | `sess-20260417135544-47e26442758849178979...` |
| signature_pad-656 | worker-02 | completed | COMPLETED | `sess-20260418021000-sigpad656...` |
| svelte-tags-input-17 | worker-04 | completed | ERROR | `sess-20260417181854-d52903bad0c041dd9e78...` |
| vue-hotel-datepicker-117 | worker-05 | completed | COMPLETED | `sess-20260417143837-636ff03ecfed4e549aaf...` |
| vue-hotel-datepicker-281 | worker-05 | completed | COMPLETED | `sess-20260417154237-6f64bc7ce6a74077966d...` |
| vue-slick-carousel-63 | worker-01 | completed | STOPPED_BY_USER | `sess-20260417230342-722981745e7d4cb1a046...` |

### 4.3 Result 文件无 sess_id（10 张）

这些卡 status=completed 但 result JSON 里没有 sess_id 字段。

| task_id | worker |
|---------|--------|
| mint-ui-490 | worker-07 |
| mint-ui-531 | worker-07 |
| mint-ui-577 | worker-07 |
| mint-ui-628 | worker-07 |
| mint-ui-644 | worker-07 |
| openclaw-nerve-140 | worker-fabrice |
| openclaw-nerve-184 | worker-fabrice |
| openclaw-nerve-194 | worker-fabrice |
| openclaw-nerve-25 | worker-fabrice |
| openclaw-nerve-34 | worker-fabrice |

### 4.4 轨迹可能不完整（2 张）

| task_id | worker | mc_status | 截图数 | 文件数 | 大小(MB) | 原因 |
|---------|--------|-----------|--------|--------|----------|------|
| ByteStash-171 | worker-02 | COMPLETED | 2 | 3 | 0.9 | 截图数过少(2张)，可能不完整 |
| open5e-884 | worker-01 | COMPLETED | 2 | 3 | 0.5 | 截图数过少(2张)，可能不完整 |

## 五、正常卡列表

<details>
<summary>展开查看全部正常卡（点击展开）</summary>

| task_id | worker | mc_status | steps | 截图数 | 文件数 | 大小(MB) |
|---------|--------|-----------|-------|--------|--------|----------|
| Analog-259 | worker-03 | TIMEOUT | 65 | 188 | 189 | 92.1 |
| BongoCat-431 | worker-09 | COMPLETED | 25 | 50 | 51 | 20.3 |
| BongoCat-431 | worker-fabrice | COMPLETED | 11 | 22 | 23 | 5.8 |
| BongoCat-438 | worker-03 | COMPLETED | 29 | 58 | 59 | 22.0 |
| BongoCat-499 | worker-08 | COMPLETED | 24 | 90 | 91 | 36.5 |
| BongoCat-509 | worker-05 | ERROR | 16 | 36 | 37 | 111.8 |
| BongoCat-592 | worker-07 |  | 0 | 54 | 55 | 20.2 |
| ByteStash-156 | worker-09 | COMPLETED | 63 | 126 | 127 | 25.5 |
| ByteStash-157 | worker-03 | COMPLETED | 5 | 10 | 11 | 3.7 |
| ByteStash-171 | worker-03 | COMPLETED | 17 | 34 | 35 | 12.9 |
| ByteStash-46 | worker-02 | COMPLETED | 27 | 54 | 55 | 26.0 |
| ByteStash-46 | worker-03 | COMPLETED | 19 | 38 | 39 | 16.2 |
| ByteStash-46 | worker-fabrice |  | 0 | 412 | 413 | 135.0 |
| ByteStash-58 | worker-03 | COMPLETED | 63 | 126 | 127 | 48.9 |
| Luckysheet-409 | worker-01 | STOPPED_BY_USER | 67 | 134 | 135 | 32.6 |
| Markpad-21 | worker-fabrice |  | 22 | 45 | 46 | 12.5 |
| Notpad-195 | worker-fabrice | COMPLETED | 7 | 14 | 15 | 3.7 |
| Nucleus-26 | worker-03 | COMPLETED | 26 | 52 | 53 | 20.8 |
| PeaNUT-35 | worker-fabrice | COMPLETED | 43 | 86 | 87 | 30.0 |
| Piped-3715 | worker-02 | COMPLETED | 47 | 94 | 95 | 39.5 |
| Piped-3715 | worker-fabrice | COMPLETED | 48 | 96 | 97 | 29.2 |
| Piped-3762 | worker-01 | STOPPED_BY_USER | 86 | 174 | 175 | 27.2 |
| Piped-3821 | worker-01 | COMPLETED | 8 | 16 | 17 | 2.4 |
| Piped-3969 | worker-01 | STOPPED_BY_USER | 73 | 164 | 165 | 33.0 |
| Piped-4059 | worker-01 | COMPLETED | 15 | 30 | 31 | 11.5 |
| Piped-4072 | worker-01 | STOPPED_BY_USER | 56 | 150 | 151 | 48.4 |
| SandDance-546 | worker-08 | COMPLETED | 35 | 62 | 63 | 42.4 |
| Semantic-UI-React-3683 | worker-02 | COMPLETED | 70 | 164 | 165 | 83.9 |
| Semantic-UI-React-3750 | worker-02 | COMPLETED | 32 | 64 | 65 | 33.1 |
| Semantic-UI-React-3833 | worker-02 | TIMEOUT_KILL | 80 | 166 | 167 | 89.1 |
| Semantic-UI-React-3864 | worker-02 | COMPLETED | 87 | 174 | 175 | 87.5 |
| Semantic-UI-React-3994 | worker-02 | COMPLETED | 18 | 36 | 37 | 22.0 |
| Semantic-UI-React-4005 | worker-02 | COMPLETED | 10 | 20 | 21 | 12.4 |
| Semantic-UI-React-4083 | worker-02 | COMPLETED | 51 | 102 | 103 | 60.9 |
| Semantic-UI-React-4110 | worker-02 | COMPLETED | 49 | 98 | 99 | 55.2 |
| SvelteLab-194 | worker-06 | COMPLETED | 25 | 50 | 51 | 20.8 |
| SvelteLab-265 | worker-01 | COMPLETED | 51 | 102 | 103 | 39.6 |
| TiddlyWiki5-763 | worker-01 | STOPPED_BY_USER | 80 | 162 | 163 | 119.8 |
| TiddlyWiki5-8092 | worker-08 | COMPLETED | 30 | 60 | 61 | 29.5 |
| TiddlyWiki5-8507 | worker-08 | COMPLETED | 10 | 20 | 21 | 13.0 |
| TiddlyWiki5-9467 | worker-08 | COMPLETED | 15 | 30 | 31 | 18.7 |
| TiddlyWiki5-9521 | worker-01 | STOPPED_BY_USER | 83 | 168 | 169 | 103.8 |
| TiddlyWiki5-9555 | worker-08 | COMPLETED | 31 | 62 | 63 | 32.6 |
| TiddlyWiki5-9592 | worker-08 | COMPLETED | 7 | 14 | 15 | 8.7 |
| TiddlyWiki5-9629 | worker-08 | COMPLETED | 10 | 20 | 21 | 12.3 |
| TiddlyWiki5-9647 | worker-08 | COMPLETED | 41 | 82 | 83 | 50.4 |
| TiddlyWiki5-9788 | worker-02 | COMPLETED | 24 | 48 | 49 | 28.2 |
| VueTorrent-2097 | worker-03 | COMPLETED | 17 | 34 | 35 | 2.9 |
| VyManager-169 | worker-03 | TIMEOUT | 57 | 214 | 215 | 136.7 |
| a11y.css-227 | worker-09 | KILLED | 73 | 180 | 181 | 114.8 |
| accounts-ui-173 | worker-fabrice | STOPPED_BY_USER | 71 | 144 | 145 | 45.2 |
| alpine-theme-57 | worker-04 | COMPLETED | 66 | 132 | 133 | 84.2 |
| alpine-theme-95 | worker-01 | STOPPED_BY_USER | 80 | 160 | 161 | 121.9 |
| angular-calendar-1396 | worker-07 | STOPPED_BY_USER | 23 | 48 | 49 | 24.9 |
| angular-datatables-1605 | worker-02 | COMPLETED | 9 | 18 | 19 | 9.1 |
| angular-datatables-1723 | worker-02 | COMPLETED | 110 | 220 | 221 | 101.2 |
| angular-datepicker-112 | worker-02 | COMPLETED | 88 | 176 | 177 | 99.3 |
| angular-datepicker-163 | worker-04 | COMPLETED | 27 | 54 | 55 | 32.6 |
| angular-datepicker-167 | worker-03 | COMPLETED | 22 | 44 | 45 | 22.9 |
| angular-datepicker-189 | worker-04 | COMPLETED | 68 | 136 | 137 | 71.3 |
| angular-datepicker-225 | worker-04 | COMPLETED | 9 | 18 | 19 | 9.8 |
| angular-datepicker-235 | worker-04 | COMPLETED | 51 | 102 | 103 | 58.4 |
| angular-datepicker-245 | worker-01 | COMPLETED | 72 | 144 | 145 | 79.4 |
| angular-datepicker-267 | worker-01 | STOPPED_BY_USER | 80 | 160 | 161 | 89.4 |
| angular-datepicker-278 | worker-01 | COMPLETED | 11 | 22 | 23 | 12.3 |
| angular-grid-layout-6 | worker-03 | COMPLETED | 24 | 48 | 49 | 21.8 |
| animate-ui-129 | worker-01 | STOPPED_BY_USER | 81 | 162 | 163 | 28.7 |
| ant-design-vue-7540 | worker-05 | COMPLETED | 6 | 12 | 13 | 5.8 |
| ant-design-vue-7590 | worker-07 | COMPLETED | 28 | 56 | 57 | 27.6 |
| ant-design-vue-7819 | worker-07 | COMPLETED | 13 | 26 | 27 | 13.3 |
| apisix-dashboard-3321 | worker-08 | TIMEOUT | 70 | 172 | 173 | 71.3 |
| auto-2015 | worker-08 | COMPLETED | 6 | 12 | 13 | 5.1 |
| batnoter-65 | worker-fabrice | COMPLETED | 67 | 64 | 65 | 21.4 |
| batnoter-87 | worker-08 | COMPLETED | 19 | 38 | 39 | 26.1 |
| batnoter-89 | worker-fabrice | COMPLETED | 216 | 215 | 216 | 94.8 |
| beercss-532 | worker-02 | KILLED | 65 | 170 | 171 | 82.2 |
| beercss-539 | worker-02 | KILLED | 70 | 198 | 200 | 101.4 |
| beercss-549 | worker-08 | COMPLETED | 45 | 100 | 101 | 40.6 |
| betaflight-configurator-4900 | worker-fabrice | COMPLETED | 114 | 228 | 229 | 75.6 |
| calendar-401 | worker-03 | TIMEOUT | 42 | 144 | 145 | 59.3 |
| cboard-1109 | worker-03 | COMPLETED | 76 | 152 | 153 | 78.0 |
| cboard-1454 | worker-03 | COMPLETED | 45 | 90 | 91 | 41.3 |
| cboard-1482 | worker-03 | COMPLETED | 23 | 46 | 47 | 32.2 |
| cboard-1589 | worker-03 | COMPLETED | 28 | 56 | 57 | 31.4 |
| cboard-1745 | worker-03 | COMPLETED | 40 | 108 | 109 | 58.7 |
| cboard-1752 | worker-03 | COMPLETED | 24 | 48 | 49 | 11.2 |
| cboard-1892 | worker-03 | COMPLETED | 18 | 36 | 37 | 9.4 |
| cboard-2026 | worker-03 | COMPLETED | 29 | 58 | 59 | 5.5 |
| cboard-2040 | worker-03 | COMPLETED | 18 | 36 | 37 | 5.1 |
| codejar-95 | worker-03 | COMPLETED | 7 | 14 | 15 | 5.1 |
| devops-daily-859 | worker-05 | COMPLETED | 30 | 60 | 61 | 57.3 |
| docs-3351 | worker-08 | COMPLETED | 9 | 18 | 19 | 9.7 |
| docz-1691 | worker-07 | COMPLETED | 14 | 28 | 29 | 12.3 |
| ebook-reader-258 | worker-04 | COMPLETED | 33 | 66 | 67 | 24.7 |
| ebook-reader-287 | worker-04 | STOPPED_BY_USER | 44 | 90 | 91 | 35.0 |
| editor-1842 | worker-08 | TIMEOUT | 55 | 178 | 179 | 80.7 |
| editor-542 | worker-03 | COMPLETED | 37 | 74 | 75 | 29.5 |
| editor-619 | worker-03 | COMPLETED | 16 | 32 | 33 | 14.4 |
| editor-706 | worker-03 | COMPLETED | 44 | 88 | 89 | 40.8 |
| editor-721 | worker-03 | COMPLETED | 31 | 62 | 63 | 28.8 |
| editor-893 | worker-03 | COMPLETED | 24 | 48 | 49 | 22.0 |
| editor.js-2084 | worker-03 | TIMEOUT | 113 | 336 | 337 | 180.1 |
| editor.js-2089 | worker-03 | ERROR | 20 | 41 | 42 | 18.6 |
| editor.js-2208 | worker-03 | COMPLETED | 27 | 54 | 55 | 31.4 |
| editor.js-2261 | worker-03 | COMPLETED | 35 | 70 | 71 | 34.5 |
| editor.js-2297 | worker-03 | COMPLETED | 15 | 30 | 31 | 14.2 |
| editor.js-2386 | worker-05 | COMPLETED | 7 | 14 | 15 | 5.4 |
| editor.js-2499 | worker-05 | COMPLETED | 9 | 18 | 19 | 7.1 |
| editor.js-2518 | worker-05 | COMPLETED | 10 | 22 | 23 | 9.4 |
| editor.js-2536 | worker-06 | COMPLETED | 58 | 116 | 117 | 58.1 |
| editor.js-2689 | worker-05 | COMPLETED | 11 | 22 | 23 | 9.2 |
| elements-1062 | worker-01 | STOPPED_BY_USER | 80 | 162 | 163 | 298.0 |
| emoji-mart-218 | worker-03 | COMPLETED | 95 | 190 | 191 | 115.2 |
| etherpad-lite-6471 | worker-08 | COMPLETED | 51 | 102 | 103 | 39.5 |
| etherpad-lite-6811 | worker-03 | COMPLETED | 51 | 102 | 103 | 22.0 |
| etherpad-lite-7137 | worker-08 | COMPLETED | 33 | 90 | 91 | 51.5 |
| factoriolab-1295 | worker-01 | ERROR | 90 | 181 | 182 | 104.2 |
| factoriolab-1332 | worker-01 | STOPPED_BY_USER | 116 | 232 | 233 | 132.5 |
| factoriolab-1494 | worker-01 | COMPLETED | 11 | 22 | 23 | 10.0 |
| factoriolab-1585 | worker-01 | COMPLETED | 45 | 90 | 91 | 47.0 |
| factoriolab-1601 | worker-01 | COMPLETED | 30 | 60 | 61 | 29.4 |
| factoriolab-1693 | worker-01 | COMPLETED | 37 | 74 | 75 | 41.5 |
| flitter-68 | worker-02 | COMPLETED | 99 | 200 | 201 | 92.7 |
| fluid-player-452 | worker-06 | STOPPED_BY_USER | 4 | 8 | 9 | 3.3 |
| fluid-player-465 | worker-06 | COMPLETED | 56 | 112 | 113 | 45.6 |
| fluid-player-530 | worker-06 | COMPLETED | 16 | 32 | 33 | 13.1 |
| fluid-player-613 | worker-06 | COMPLETED | 11 | 22 | 23 | 9.0 |
| gitlight-66 | worker-fabrice | COMPLETED | 6 | 12 | 13 | 4.5 |
| graphviz-visual-editor-215 | worker-01 | COMPLETED | 18 | 36 | 37 | 3.2 |
| ha-fusion-220 | worker-03 | COMPLETED | 48 | 100 | 101 | 96.0 |
| ha-fusion-278 | worker-03 | SKIPPED | 0 | 100 | 101 | 96.0 |
| ha-fusion-476 | worker-03 | SKIPPED | 0 | 100 | 101 | 96.0 |
| ha-fusion-478 | worker-03 | SKIPPED | 0 | 100 | 101 | 96.0 |
| ha-fusion-62 | worker-01 | COMPLETED | 29 | 58 | 59 | 43.0 |
| ide-9 | worker-01 | STOPPED_BY_USER | 92 | 186 | 187 | 13.9 |
| ionic-823 | worker-05 | COMPLETED | 39 | 80 | 81 | 34.4 |
| it-tools-1110 | worker-03 | COMPLETED | 24 | 70 | 71 | 38.5 |
| it-tools-555 | worker-03 | COMPLETED | 9 | 18 | 19 | 11.1 |
| it-tools-652 | worker-03 | COMPLETED | 35 | 70 | 71 | 33.4 |
| jodit-1327 | worker-03 | TIMEOUT_KILL | 73 | 200 | 201 | 93.4 |
| jodit-1335 | worker-03 | TIMEOUT_KILL | 58 | 150 | 151 | 68.0 |
| jodit-514 | worker-03 | COMPLETED | 14 | 28 | 29 | 10.3 |
| kalendar-75 | worker-03 | COMPLETED | 68 | 212 | 213 | 89.5 |
| kan-206 | worker-08 | COMPLETED | 55 | 28 | 29 | 15.8 |
| kan-242 | worker-08 | COMPLETED | 18 | 36 | 37 | 16.3 |
| karakeep-1669 | worker-04 | COMPLETED | 42 | 162 | 163 | 70.9 |
| karakeep-2242 | worker-04 | COMPLETED | 42 | 92 | 93 | 37.1 |
| karakeep-2395 | worker-02 | COMPLETED | 74 | 150 | 151 | 58.7 |
| kepler.gl-2305 | worker-09 | COMPLETED | 13 | 26 | 27 | 45.2 |
| kepler.gl-2369 | worker-fabrice | COMPLETED | 19 | 38 | 39 | 15.8 |
| kepler.gl-3346 | worker-fabrice | COMPLETED | 23 | 46 | 47 | 21.0 |
| learn.svelte.dev-164 | worker-02 | COMPLETED | 78 | 156 | 157 | 80.4 |
| learn.svelte.dev-360 | worker-02 | COMPLETED | 86 | 194 | 195 | 107.7 |
| learn.svelte.dev-392 | worker-02 | ERROR | 40 | 80 | 81 | 42.3 |
| lokus-15 | worker-05 | COMPLETED | 25 | 50 | 51 | 17.5 |
| lumen-253 | worker-09 | COMPLETED | 46 | 92 | 93 | 44.7 |
| lumen-300 | worker-09 | SIGKILL | 68 | 188 | 189 | 88.4 |
| lumen-451 | worker-09 | COMPLETED | 52 | 104 | 105 | 46.2 |
| lumen-473 | worker-09 | SIGKILL | 54 | 176 | 177 | 80.4 |
| maplibre-gl-js-4853 | worker-04 | STOPPED_BY_USER | 29 | 60 | 61 | 36.6 |
| maplibre-gl-js-7185 | worker-04 | STOPPED_BY_USER | 30 | 60 | 61 | 56.0 |
| maplibre-gl-js-7277 | worker-04 | COMPLETED | 21 | 42 | 43 | 45.1 |
| maplibre-gl-js-7314 | worker-04 | COMPLETED | 31 | 62 | 63 | 32.7 |
| maputnik-871 | worker-07 | COMPLETED | 18 | 36 | 37 | 25.5 |
| maskito-2445 | worker-05 | COMPLETED | 46 | 92 | 93 | 44.7 |
| maskito-2448 | worker-05 | COMPLETED | 38 | 76 | 77 | 36.9 |
| maskito-2534 | worker-05 | COMPLETED | 50 | 100 | 101 | 46.7 |
| maskito-804 | worker-05 | COMPLETED | 41 | 82 | 83 | 37.8 |
| mathlive-2479 | worker-09 | COMPLETED | 28 | 56 | 57 | 24.0 |
| mathlive-2482 | worker-09 | COMPLETED | 33 | 66 | 67 | 29.3 |
| mathlive-2584 | worker-08 | COMPLETED | 34 | 68 | 69 | 27.2 |
| mathlive-2638 | worker-09 | COMPLETED | 27 | 54 | 55 | 22.2 |
| md-1126 | worker-08 | COMPLETED | 31 | 62 | 63 | 30.4 |
| media-chrome-1017 | worker-06 | STOPPED_BY_USER | 39 | 78 | 79 | 55.9 |
| media-chrome-697 | worker-06 | STOPPED_BY_USER | 39 | 80 | 81 | 41.2 |
| media-chrome-750 | worker-06 | STOPPED_BY_USER | 41 | 84 | 85 | 28.7 |
| media-chrome-772 | worker-06 | STOPPED_BY_USER | 41 | 84 | 85 | 30.1 |
| media-chrome-792 | worker-05 | COMPLETED | 109 | 204 | 205 | 151.5 |
| media-chrome-823 | worker-05 | COMPLETED | 60 | 102 | 103 | 88.9 |
| media-chrome-986 | worker-05 | COMPLETED | 39 | 78 | 79 | 43.9 |
| media-chrome-991 | worker-05 | COMPLETED | 31 | 62 | 63 | 36.5 |
| medium-editor-1047 | worker-02 | COMPLETED | 16 | 32 | 33 | 22.8 |
| medium-editor-1047 | worker-fabrice | COMPLETED | 39 | 78 | 79 | 40.8 |
| medium-editor-1057 | worker-02 | COMPLETED | 26 | 52 | 53 | 37.2 |
| medium-editor-1156 | worker-02 | COMPLETED | 52 | 104 | 105 | 57.8 |
| medium-editor-1216 | worker-02 | COMPLETED | 89 | 178 | 179 | 111.1 |
| medium-editor-234 | worker-02 | COMPLETED | 37 | 74 | 75 | 40.8 |
| medium-editor-702 | worker-06 | STOPPED_BY_USER | 77 | 156 | 157 | 91.8 |
| medium-editor-711 | worker-06 | STOPPED_BY_USER | 13 | 26 | 27 | 9.9 |
| medium-editor-748 | worker-06 | STOPPED_BY_USER | 16 | 32 | 33 | 15.2 |
| medium-editor-751 | worker-06 | COMPLETED | 55 | 110 | 111 | 70.1 |
| medium-editor-757 | worker-06 | STOPPED_BY_USER | 29 | 58 | 59 | 38.4 |
| medium-editor-783 | worker-06 | COMPLETED | 48 | 96 | 97 | 56.4 |
| medium-editor-935 | worker-06 | COMPLETED | 16 | 32 | 33 | 20.7 |
| medium-editor-942 | worker-09 | COMPLETED | 57 | 114 | 115 | 68.1 |
| medium-editor-959 | worker-09 | KILLED | 70 | 210 | 211 | 129.6 |
| medium-editor-994 | worker-09 | COMPLETED | 77 | 154 | 155 | 62.9 |
| meilisearch-ui-163 | worker-08 | COMPLETED | 16 | 32 | 33 | 12.9 |
| mini-qr-219 | worker-06 | STOPPED_BY_USER | 63 | 364 | 365 | 193.4 |
| minimal-chat-74 | worker-03 | COMPLETED | 58 | 116 | 117 | 59.6 |
| mint-ui-285 | worker-05 | COMPLETED | 29 | 58 | 59 | 24.1 |
| mint-ui-290 | worker-05 | COMPLETED | 21 | 38 | 39 | 14.6 |
| mint-ui-304 | worker-05 | COMPLETED | 9 | 18 | 19 | 7.6 |
| mint-ui-305 | worker-05 | COMPLETED | 31 | 60 | 61 | 24.3 |
| mint-ui-307 | worker-05 | COMPLETED | 63 | 102 | 103 | 38.6 |
| mint-ui-318 | worker-07 | COMPLETED | 44 | 88 | 89 | 29.7 |
| mint-ui-366 | worker-07 | COMPLETED | 41 | 82 | 83 | 30.0 |
| mint-ui-776 | worker-07 | COMPLETED | 17 | 34 | 35 | 12.0 |
| monaco-editor-auto-typings-32 | worker-05 | COMPLETED | 33 | 68 | 69 | 36.5 |
| multiple-select-257 | worker-09 | COMPLETED | 60 | 120 | 121 | 23.6 |
| multiple-select-302 | worker-09 | COMPLETED | 13 | 26 | 27 | 2.0 |
| multiple-select-308 | worker-04 | COMPLETED | 10 | 20 | 21 | 7.8 |
| multiple-select-350 | worker-09 | COMPLETED | 20 | 40 | 41 | 3.1 |
| multiple-select-355 | worker-09 | ERROR | 14 | 29 | 30 | 2.4 |
| multiple-select-407 | worker-09 | COMPLETED | 21 | 42 | 43 | 4.0 |
| multiple-select-434 | worker-05 | COMPLETED | 6 | 12 | 13 | 4.1 |
| multiple-select-450 | worker-05 | COMPLETED | 8 | 16 | 17 | 5.7 |
| multiple-select-465 | worker-05 | COMPLETED | 6 | 12 | 13 | 4.4 |
| multiple-select-487 | worker-05 | COMPLETED | 14 | 28 | 29 | 10.8 |
| multiple-select-507 | worker-05 | COMPLETED | 16 | 32 | 33 | 11.2 |
| multiple-select-511 | worker-fabrice | COMPLETED | 57 | 114 | 115 | 36.4 |
| multiple-select-515 | worker-05 | COMPLETED | 18 | 36 | 37 | 13.0 |
| next-redux-wrapper-325 | worker-03 | COMPLETED | 15 | 30 | 31 | 12.5 |
| ng-select-2475 | worker-02 | COMPLETED | 18 | 36 | 37 | 16.0 |
| ng-select-2498 | worker-02 | COMPLETED | 59 | 118 | 119 | 58.0 |
| ng-select-2515 | worker-02 | COMPLETED | 8 | 16 | 17 | 7.3 |
| ng-select-2576 | worker-07 | COMPLETED | 33 | 66 | 67 | 32.3 |
| ng-select-2594 | worker-02 | COMPLETED | 43 | 86 | 87 | 45.0 |
| ng-select-2738 | worker-02 | COMPLETED | 21 | 42 | 43 | 19.5 |
| ng-select-2759 | worker-02 | COMPLETED | 55 | 110 | 111 | 53.4 |
| ngx-clipboard-147 | worker-03 | COMPLETED | 46 | 92 | 93 | 38.9 |
| ngx-markdown-185 | worker-08 | COMPLETED | 45 | 140 | 141 | 67.6 |
| nuxt-21 | worker-fabrice | COMPLETED | 26 | 52 | 53 | 20.4 |
| nuxt-33 | worker-fabrice | COMPLETED | 108 | 106 | 107 | 31.6 |
| nuxt-46 | worker-fabrice | COMPLETED | 27 | 54 | 55 | 17.2 |
| nuxt-api-party-49 | worker-06 | COMPLETED | 55 | 110 | 111 | 52.7 |
| nuxt-api-party-98 | worker-06 | COMPLETED | 25 | 50 | 51 | 33.5 |
| nuxt-module-222 | worker-08 | COMPLETED | 22 | 50 | 51 | 23.1 |
| nuxt-security-332 | worker-06 | COMPLETED | 20 | 40 | 41 | 17.8 |
| nuxt-security-494 | worker-06 | STOPPED_BY_USER | 86 | 174 | 175 | 83.0 |
| nuxt-security-610 | worker-05 | COMPLETED | 37 | 76 | 77 | 44.6 |
| octo-101 | worker-07 | COMPLETED | 56 | 112 | 113 | 22.6 |
| octo-213 | worker-07 | COMPLETED | 37 | 74 | 75 | 30.2 |
| octo-76 | worker-07 | COMPLETED | 109 | 218 | 219 | 101.9 |
| open5e-622 | worker-02 | COMPLETED | 97 | 196 | 197 | 101.0 |
| open5e-622 | worker-03 | TIMEOUT | 90 | 180 | 181 | 88.3 |
| open5e-655 | worker-02 | COMPLETED | 25 | 50 | 51 | 22.3 |
| open5e-655 | worker-03 | TIMEOUT | 59 | 162 | 163 | 78.6 |
| open5e-695 | worker-02 | COMPLETED | 14 | 28 | 29 | 13.3 |
| open5e-716 | worker-02 | COMPLETED | 90 | 180 | 181 | 84.6 |
| open5e-721 | worker-01 | COMPLETED | 6 | 12 | 13 | 1.7 |
| open5e-721 | worker-02 | COMPLETED | 42 | 84 | 85 | 38.0 |
| open5e-737 | worker-03 | COMPLETED | 57 | 138 | 139 | 85.2 |
| open5e-747 | worker-01 | COMPLETED | 82 | 164 | 165 | 82.7 |
| open5e-747 | worker-02 | COMPLETED | 27 | 54 | 55 | 31.3 |
| open5e-775 | worker-01 | STOPPED_BY_USER | 94 | 188 | 189 | 38.1 |
| open5e-775 | worker-02 | COMPLETED | 59 | 118 | 119 | 60.3 |
| open5e-799 | worker-01 | COMPLETED | 48 | 96 | 97 | 37.5 |
| open5e-803 | worker-01 | COMPLETED | 43 | 86 | 87 | 26.4 |
| open5e-803 | worker-02 | COMPLETED | 40 | 80 | 81 | 45.7 |
| open5e-869 | worker-01 | COMPLETED | 30 | 60 | 61 | 9.7 |
| openclaw-nerve-23 | worker-fabrice | COMPLETED | 12 | 24 | 25 | 6.7 |
| openclaw-nerve-27 | worker-09 | COMPLETED | 25 | 50 | 51 | 23.5 |
| org-chart-215 | worker-02 | TIMEOUT | 70 | 196 | 197 | 98.0 |
| org-chart-290 | worker-02 | COMPLETED | 41 | 82 | 83 | 37.7 |
| org-chart-306 | worker-02 | COMPLETED | 17 | 34 | 35 | 15.5 |
| org-chart-69 | worker-02 | COMPLETED | 44 | 88 | 89 | 38.7 |
| overlayed-87 | worker-08 | COMPLETED | 26 | 52 | 53 | 19.7 |
| paperbits-demo-138 | worker-08 | COMPLETED | 40 | 80 | 81 | 42.1 |
| paperbits-demo-74 | worker-08 | COMPLETED | 15 | 40 | 41 | 23.3 |
| planka-1350 | worker-04 | STOPPED_BY_USER | 32 | 66 | 67 | 24.0 |
| react-bootstrap-6314 | worker-03 | COMPLETED | 25 | 50 | 51 | 27.3 |
| react-bootstrap-6393 | worker-03 | COMPLETED | 66 | 132 | 133 | 86.1 |
| react-bootstrap-6421 | worker-03 | COMPLETED | 64 | 128 | 129 | 85.1 |
| react-bootstrap-6491 | worker-03 | COMPLETED | 6 | 12 | 13 | 7.0 |
| react-bootstrap-6507 | worker-03 | COMPLETED | 44 | 88 | 89 | 64.9 |
| react-bootstrap-6528 | worker-02 | COMPLETED | 12 | 24 | 25 | 14.1 |
| react-bootstrap-6637 | worker-02 | COMPLETED | 15 | 30 | 31 | 15.1 |
| react-bootstrap-6671 | worker-02 | COMPLETED | 22 | 44 | 45 | 25.0 |
| react-bootstrap-6712 | worker-02 | COMPLETED | 21 | 42 | 43 | 24.9 |
| react-bootstrap-6764 | worker-02 | COMPLETED | 28 | 56 | 57 | 34.5 |
| react-bootstrap-6827 | worker-08 | COMPLETED | 11 | 22 | 23 | 11.8 |
| react-bootstrap-6842 | worker-05 | STOPPED_BY_USER | 62 | 162 | 163 | 78.3 |
| react-bootstrap-6860 | worker-08 | COMPLETED | 18 | 48 | 49 | 25.6 |
| react-bootstrap-6866 | worker-08 | COMPLETED | 77 | 154 | 155 | 85.9 |
| react-bootstrap-6991 | worker-08 | COMPLETED | 15 | 30 | 31 | 17.4 |
| react-calendar-343 | worker-05 | COMPLETED | 7 | 14 | 15 | 6.0 |
| react-content-loader-110 | worker-06 | COMPLETED | 60 | 120 | 121 | 56.0 |
| react-content-loader-93 | worker-04 | COMPLETED | 35 | 70 | 71 | 29.1 |
| react-datasheet-grid-204 | worker-05 | COMPLETED | 19 | 38 | 39 | 13.2 |
| react-date-picker-110 | worker-07 | COMPLETED | 4 | 8 | 9 | 2.8 |
| react-native-web-2560 | worker-06 | COMPLETED | 9 | 18 | 19 | 6.7 |
| react-native-web-2704 | worker-06 | COMPLETED | 26 | 52 | 53 | 20.0 |
| react-page-838 | worker-09 | COMPLETED | 25 | 52 | 53 | 95.5 |
| react-player-1957 | worker-01 | COMPLETED | 11 | 22 | 23 | 3.9 |
| react-rainbow-1485 | worker-08 | COMPLETED | 15 | 38 | 39 | 16.8 |
| react-timeline-9000-104 | worker-01 | COMPLETED | 22 | 44 | 45 | 20.2 |
| react-timeline-9000-144 | worker-05 | COMPLETED | 66 | 116 | 117 | 54.6 |
| react-timeline-9000-200 | worker-05 | COMPLETED | 88 | 176 | 177 | 89.2 |
| react-timeline-9000-35 | worker-05 | STOPPED_BY_USER | 78 | 158 | 159 | 83.6 |
| react-timeline-9000-62 | worker-05 | COMPLETED | 54 | 108 | 109 | 55.1 |
| react-toastify-577 | worker-09 | COMPLETED | 31 | 62 | 63 | 39.9 |
| react-virtualized-1375 | worker-06 | STOPPED_BY_USER | 59 | 174 | 175 | 104.8 |
| react-virtualized-1577 | worker-06 | COMPLETED | 63 | 126 | 127 | 59.8 |
| react-virtualized-866 | worker-08 | COMPLETED | 79 | 162 | 163 | 76.8 |
| reactgrid-104 | worker-06 | COMPLETED | 25 | 50 | 51 | 27.0 |
| reactgrid-205 | worker-08 | COMPLETED | 15 | 36 | 37 | 18.2 |
| reactgrid-229 | worker-08 | COMPLETED | 25 | 50 | 51 | 21.7 |
| reactgrid-302 | worker-06 | TIMEOUT | 48 | 117 | 118 | 68.2 |
| reactstrap-1070 | worker-05 | COMPLETED | 89 | 180 | 181 | 84.3 |
| rich-markdown-editor-165 | worker-07 |  | 0 | 59 | 60 | 21.9 |
| rich-markdown-editor-176 | worker-05 | COMPLETED | 18 | 36 | 37 | 13.6 |
| rich-markdown-editor-208 | worker-01 | COMPLETED | 76 | 152 | 153 | 36.2 |
| rich-markdown-editor-296 | worker-07 | COMPLETED | 64 | 128 | 129 | 144.4 |
| rich-markdown-editor-302 | worker-07 | TIMEOUT | 49 | 108 | 109 | 121.0 |
| rich-markdown-editor-323 | worker-07 | TIMEOUT | 53 | 268 | 269 | 301.3 |
| rich-markdown-editor-350 | worker-01 | STOPPED_BY_USER | 81 | 162 | 163 | 11.4 |
| rich-markdown-editor-4 | worker-01 | STOPPED_BY_USER | 80 | 162 | 163 | 9.7 |
| rich-markdown-editor-408 | worker-01 | STOPPED_BY_USER | 81 | 162 | 163 | 17.0 |
| rich-markdown-editor-416 | worker-09 | COMPLETED | 64 | 128 | 129 | 207.3 |
| rich-markdown-editor-440 | worker-09 | COMPLETED | 61 | 122 | 123 | 188.7 |
| rich-markdown-editor-447 | worker-01 | COMPLETED | 45 | 90 | 91 | 10.7 |
| rich-markdown-editor-462 | worker-09 | COMPLETED | 26 | 52 | 53 | 80.8 |
| rich-markdown-editor-489 | worker-05 | STOPPED_BY_USER | 89 | 180 | 181 | 84.1 |
| script-lab-623 | worker-04 | COMPLETED | 12 | 24 | 25 | 10.4 |
| script-lab-648 | worker-04 | COMPLETED | 6 | 12 | 13 | 5.8 |
| script-lab-667 | worker-02 | COMPLETED | 13 | 26 | 27 | 2.6 |
| script-lab-672 | worker-02 | COMPLETED | 63 | 126 | 127 | 13.2 |
| script-lab-732 | worker-02 | COMPLETED | 66 | 30 | 31 | 13.2 |
| shadcn-admin-134 | worker-06 | COMPLETED | 24 | 48 | 49 | 23.5 |
| shadcn-admin-136 | worker-06 | COMPLETED | 65 | 166 | 167 | 85.4 |
| shadcn-solid-122 | worker-09 | COMPLETED | 6 | 12 | 13 | 5.6 |
| shadcn-solid-77 | worker-09 | COMPLETED | 26 | 52 | 53 | 24.5 |
| shadcn-ui-expansions-171 | worker-05 | COMPLETED | 18 | 36 | 37 | 18.3 |
| shadcn-ui-expansions-205 | worker-05 | COMPLETED | 11 | 22 | 23 | 11.2 |
| signature_pad-656 | worker-05 | COMPLETED | 27 | 54 | 55 | 41.0 |
| slickgpt-38 | worker-02 | COMPLETED | 15 | 30 | 31 | 11.3 |
| sorry-cypress-310 | worker-05 | COMPLETED | 23 | 48 | 49 | 20.2 |
| static-cms-1069 | worker-09 | COMPLETED | 18 | 36 | 37 | 3.5 |
| static-cms-781 | worker-09 | COMPLETED | 24 | 48 | 49 | 46.4 |
| static-cms-809 | worker-09 | TIMEOUT | 55 | 162 | 163 | 171.4 |
| static-cms-815 | worker-09 | COMPLETED | 22 | 44 | 45 | 36.0 |
| static-cms-844 | worker-09 | COMPLETED | 15 | 30 | 31 | 5.2 |
| static-cms-853 | worker-09 | COMPLETED | 61 | 122 | 123 | 29.8 |
| static-cms-854 | worker-09 | COMPLETED | 53 | 106 | 107 | 118.7 |
| static-cms-879 | worker-09 | COMPLETED | 48 | 96 | 97 | 140.6 |
| static-cms-905 | worker-05 | COMPLETED | 59 | 118 | 119 | 78.7 |
| static-cms-926 | worker-09 | COMPLETED | 18 | 36 | 37 | 62.4 |
| static-cms-931 | worker-09 | COMPLETED | 6 | 12 | 13 | 19.6 |
| static-cms-937 | worker-09 | COMPLETED | 21 | 42 | 43 | 67.4 |
| static-cms-943 | worker-09 | COMPLETED | 10 | 20 | 21 | 32.8 |
| static-cms-994 | worker-09 | TIMEOUT | 39 | 146 | 147 | 353.1 |
| svelte-highlight-258 | worker-01 | ERROR | 85 | 170 | 171 | 16.5 |
| svelte-splitpanes-3 | worker-06 | STOPPED_BY_USER | 51 | 164 | 165 | 74.4 |
| svelte-tags-input-26 | worker-04 | COMPLETED | 10 | 20 | 21 | 7.7 |
| svelte-typeahead-11 | worker-03 | STOPPED_BY_USER | 119 | 240 | 241 | 106.8 |
| svelte-typeahead-34 | worker-03 | COMPLETED | 39 | 78 | 79 | 34.2 |
| svelte-typeahead-47 | worker-03 | COMPLETED | 59 | 118 | 119 | 48.4 |
| svelte-typeahead-56 | worker-03 | COMPLETED | 15 | 30 | 31 | 12.9 |
| svelte-typeahead-66 | worker-03 | COMPLETED | 62 | 124 | 125 | 55.6 |
| svelteui-179 | worker-02 | COMPLETED | 59 | 118 | 119 | 57.3 |
| svelteui-189 | worker-02 | COMPLETED | 42 | 84 | 85 | 40.7 |
| svelteui-202 | worker-02 | COMPLETED | 26 | 52 | 53 | 27.4 |
| tabler-react-125 | worker-02 | COMPLETED | 80 | 160 | 161 | 75.3 |
| tabler-react-134 | worker-02 | COMPLETED | 90 | 214 | 215 | 105.4 |
| tabler-react-136 | worker-02 | COMPLETED | 72 | 144 | 145 | 72.9 |
| tabler-react-165 | worker-02 | COMPLETED | 18 | 36 | 37 | 17.3 |
| tabler-react-174 | worker-06 | COMPLETED | 23 | 46 | 47 | 22.5 |
| tailwindcss-960 | worker-01 | COMPLETED | 34 | 102 | 103 | 32.3 |
| tailwindcss-987 | worker-08 | COMPLETED | 31 | 62 | 63 | 32.5 |
| trello-kanban-analysis-tool-32 | worker-03 | COMPLETED | 27 | 54 | 55 | 8.8 |
| trix-265 | worker-04 | COMPLETED | 5 | 10 | 11 | 3.6 |
| trix-554 | worker-04 | COMPLETED | 13 | 26 | 27 | 17.8 |
| trix-77 | worker-04 | STOPPED_BY_USER | 96 | 194 | 195 | 77.8 |
| typehero-1504 | worker-04 | STOPPED_BY_USER | 28 | 56 | 57 | 27.1 |
| typehero-1510 | worker-06 | COMPLETED | 13 | 26 | 27 | 22.5 |
| typehero-1516 | worker-04 | STOPPED_BY_USER | 28 | 56 | 57 | 27.1 |
| typehero-1541 | worker-04 | STOPPED_BY_USER | 28 | 56 | 57 | 27.1 |
| typehero-1571 | worker-04 | STOPPED_BY_USER | 28 | 56 | 57 | 27.1 |
| typehero-1616 | worker-04 | STOPPED_BY_USER | 28 | 56 | 57 | 27.1 |
| typehero-1682 | worker-06 | STOPPED_BY_USER | 73 | 146 | 147 | 70.7 |
| typehero-1686 | worker-04 | STOPPED_BY_USER | 28 | 56 | 57 | 27.1 |
| typehero-1688 | worker-04 | STOPPED_BY_USER | 28 | 56 | 57 | 27.1 |
| typehero-1695 | worker-04 | STOPPED_BY_USER | 28 | 56 | 57 | 27.1 |
| typehero-1721 | worker-04 | STOPPED_BY_USER | 28 | 56 | 57 | 27.1 |
| typehero-920 | worker-04 | STOPPED_BY_USER | 28 | 56 | 57 | 27.1 |
| vaadin-grid-1176 | worker-07 | COMPLETED | 67 | 134 | 135 | 72.4 |
| vaadin-grid-1577 | worker-07 | COMPLETED | 47 | 94 | 95 | 48.4 |
| vaadin-grid-1645 | worker-07 | COMPLETED | 42 | 84 | 85 | 47.0 |
| vaadin-grid-1723 | worker-07 | COMPLETED | 83 | 394 | 395 | 225.8 |
| vaadin-grid-1726 | worker-07 | COMPLETED | 75 | 150 | 151 | 75.3 |
| vaadin-grid-1737 | worker-07 | COMPLETED | 85 | 170 | 171 | 85.6 |
| vaadin-grid-2055 | worker-08 | TIMEOUT | 71 | 182 | 183 | 71.2 |
| vcal-340 | worker-fabrice | COMPLETED | 98 | 196 | 197 | 97.6 |
| vcal-342 | worker-02 | COMPLETED | 57 | 114 | 115 | 78.8 |
| vcal-344 | worker-fabrice | COMPLETED | 25 | 50 | 51 | 15.3 |
| vcal-350 | worker-fabrice | COMPLETED | 76 | 152 | 153 | 60.0 |
| vcal-352 | worker-02 | COMPLETED | 65 | 130 | 131 | 91.4 |
| vue-devui-1567 | worker-01 | COMPLETED | 62 | 124 | 125 | 31.1 |
| vue-hotel-datepicker-202 | worker-05 | COMPLETED | 56 | 114 | 115 | 46.9 |
| vue-pdf-125 | worker-08 | TIMEOUT | 70 | 142 | 143 | 83.9 |
| vue-pdf-168 | worker-08 | TIMEOUT | 63 | 144 | 145 | 75.5 |
| vue-pdf-172 | worker-02 | COMPLETED | 46 | 92 | 93 | 52.3 |
| vue-pdf-215 | worker-02 | COMPLETED | 61 | 158 | 159 | 92.0 |
| vue-pdf-224 | worker-02 | COMPLETED | 53 | 106 | 107 | 80.3 |
| vue-pdf-98 | worker-06 | STOPPED_BY_USER | 16 | 32 | 33 | 17.3 |
| vue-pdf-99 | worker-06 | STOPPED_BY_USER | 62 | 180 | 181 | 103.0 |
| wanderlust-193 | worker-04 | COMPLETED | 5 | 10 | 11 | 4.6 |
| website-4366 | worker-04 | STOPPED_BY_USER | 60 | 120 | 121 | 42.3 |
| website-4788 | worker-04 | COMPLETED | 16 | 32 | 33 | 20.5 |
| website-4794 | worker-04 | COMPLETED | 3 | 6 | 7 | 4.0 |
| website-4805 | worker-04 | COMPLETED | 8 | 16 | 17 | 8.4 |
| website-4893 | worker-04 | COMPLETED | 30 | 60 | 61 | 37.4 |
| website-5102 | worker-04 | COMPLETED | 91 | 182 | 183 | 148.8 |
| website-5139 | worker-04 | COMPLETED | 14 | 28 | 29 | 13.5 |
| website-5158 | worker-04 | COMPLETED | 5 | 10 | 11 | 4.5 |
| website-5189 | worker-04 | COMPLETED | 16 | 32 | 33 | 15.8 |
| whitebophir-48 | worker-01 | COMPLETED | 28 | 56 | 57 | 3.8 |

</details>

---
*报告由 Pichai 自动生成，轨迹文件存储在本地 `/tmp/tos_trajectories/`，未上传到 GitHub。*
