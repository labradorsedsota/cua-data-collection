# Results CHANGELOG

## 2026-04-18 22:51 — 异常卡清理（143 张）

**操作：** 将以下 143 张 result 文件从 `results/{worker}/` 移至 `results/trash/`，dispatch-log 状态改为 `unassigned`。

**原因分类：**

### mc_status=STOPPED_BY_USER（54 张）

- Luckysheet-409
- Piped-3762
- Piped-3969
- Piped-4072
- TiddlyWiki5-763
- TiddlyWiki5-9521
- accounts-ui-173
- alpine-theme-95
- angular-calendar-1396
- angular-datepicker-267
- animate-ui-129
- ebook-reader-287
- elements-1062
- factoriolab-1332
- fluid-player-452
- ide-9
- maplibre-gl-js-4853
- maplibre-gl-js-7185
- media-chrome-1017
- media-chrome-697
- media-chrome-750
- media-chrome-772
- medium-editor-702
- medium-editor-711
- medium-editor-748
- medium-editor-757
- mini-qr-219
- nuxt-security-494
- open5e-775
- planka-1350
- react-bootstrap-6842
- react-timeline-9000-35
- react-virtualized-1375
- rich-markdown-editor-350
- rich-markdown-editor-4
- rich-markdown-editor-408
- rich-markdown-editor-489
- svelte-splitpanes-3
- svelte-typeahead-11
- trix-77
- typehero-1504
- typehero-1516
- typehero-1541
- typehero-1571
- typehero-1616
- typehero-1682
- typehero-1686
- typehero-1688
- typehero-1695
- typehero-1721
- typehero-920
- vue-pdf-98
- vue-pdf-99
- website-4366

### TOS未找到轨迹（41 张）

- Analog-135
- BongoCat-437
- ByteStash-156
- ByteStash-157
- ByteStash-173
- ByteStash-58
- Luckysheet-528
- Markpad-21
- Notpad-195
- Notpad-268
- Piped-3941
- ant-design-vue-7574
- beercss-558
- betaflight-configurator-4700
- charts-201
- emoji-mart-218
- emoji-mart-219
- emoji-mart-220
- emoji-mart-254
- emoji-mart-327
- emoji-mart-762
- factoriolab-1327
- fluid-player-486
- gitlight-131
- karakeep-2299
- lumen-254
- mint-ui-754
- nuxt-module-220
- nuxt-security-610
- open5e-762
- open5e-799
- react-date-picker-118
- react-modern-calendar-datepicker-88
- runbox7-1279
- script-lab-609
- signature_pad-120
- signature_pad-656
- svelte-tags-input-17
- vue-hotel-datepicker-117
- vue-hotel-datepicker-281
- vue-slick-carousel-63

### mc_status=TIMEOUT（17 张）

- Analog-259
- VyManager-169
- apisix-dashboard-3321
- calendar-401
- editor-1842
- editor.js-2084
- open5e-622
- open5e-655
- org-chart-215
- reactgrid-302
- rich-markdown-editor-302
- rich-markdown-editor-323
- static-cms-809
- static-cms-994
- vaadin-grid-2055
- vue-pdf-125
- vue-pdf-168

### result无sess_id（10 张）

- mint-ui-490
- mint-ui-531
- mint-ui-577
- mint-ui-628
- mint-ui-644
- openclaw-nerve-140
- openclaw-nerve-184
- openclaw-nerve-194
- openclaw-nerve-25
- openclaw-nerve-34

### mc_status=ERROR（6 张）

- BongoCat-509
- editor.js-2089
- factoriolab-1295
- learn.svelte.dev-392
- multiple-select-355
- svelte-highlight-258

### mc_status=KILLED（4 张）

- a11y.css-227
- beercss-532
- beercss-539
- medium-editor-959

### mc_status=空（3 张）

- BongoCat-592
- ByteStash-46
- rich-markdown-editor-165

### mc_status=TIMEOUT_KILL（3 张）

- Semantic-UI-React-3833
- jodit-1327
- jodit-1335

### mc_status=SKIPPED（3 张）

- ha-fusion-278
- ha-fusion-476
- ha-fusion-478

### mc_status=SIGKILL（2 张）

- lumen-300
- lumen-473

---

**变更摘要：**
- 移动文件：143 张
- dispatch-log 更新：143 张 → unassigned
- dispatch-log 新状态：unassigned=143, dispatched=689
