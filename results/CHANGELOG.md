# Results CHANGELOG

## 2026-04-19 17:35 — Batch 14: 48 张卡重做

**原因：** 合规性检查 + 数据质量分类后，以下卡需重做：
- 不合规卡 26 张（completed缺sess_id / status异常 / 字段缺失等）
- C类 14 张（共享sess_id，多卡共用一条轨迹）
- D类 4 张（COMPLETED但TOS无轨迹）
- E类 4 张（mc_status=KILLED）
- H类 2 张（无任何result）
- 去重后 48 张

**操作：**
1. 87 个 result 文件（含重复副本）移入 `results_archive/trash/`
2. dispatch-log 重置为 unassigned → 重新分配（避开原 worker）→ dispatched
3. 通过 Pichai bot 向 9 个 worker 1v1 通道派发任务

**分配：**
- worker-01: 6 张（Analog-135, Notpad-268, jodit-1327, mint-ui-318, nuxt-security-494, react-virtualized-1375）
- worker-02: 5 张（BongoCat-437, RapidRAW-658, jodit-1335, mint-ui-366, open5e-655）
- worker-03: 4 张（Taskosaur-62, mint-ui-490, open5e-762, svelte-highlight-258）
- worker-05: 6 张（BongoCat-438, calendar-401, minimal-chat-74, mint-ui-531, open5e-775, svelte-tags-input-17）
- worker-06: 6 张（BongoCat-499, docz-965, mint-ui-285, mint-ui-577, open5e-799, svelte-tags-input-26）
- worker-07: 5 张（BongoCat-509, mint-ui-290, mint-ui-628, org-chart-290, vue-hotel-datepicker-281）
- worker-08: 6 张（BongoCat-592, docz-984, mint-ui-304, mint-ui-644, org-chart-306, vue-pdf-98）
- worker-09: 5 张（BongoCat-777, emoji-mart-220, mint-ui-305, mint-ui-754, planka-1350）
- worker-fabrice: 5 张（Notpad-195, ide-9, mint-ui-307, mint-ui-776, react-modern-calendar-datepicker-88）

---

## 2026-04-19 11:30 — 回滚 10:05 的状态修改

**操作：** 回滚 5 张卡的 status 改动，恢复为原始 completed 状态

| 卡 | 回滚内容 |
|---|---|
| BongoCat-437 | status: failed → completed，移除 failure.type |
| BongoCat-509 | 同上 |
| BongoCat-592 | 同上 |
| BongoCat-777 | 同上 |
| Analog-135 | 同上 |

**原因：** Emily 指示先不修改任务状态，林菡确认回滚。
**open5e-762 文字备注同时撤销。**

## 2026-04-19 11:20 — 旧结果归档

**操作：** 将 `results/trash/` 下 143 张回收卡的旧 result JSON 移至 `results_archive/trash/`

**原因：** 这 143 张卡已于 2026-04-18 22:51 从 `results/worker-xx/` 移入 `results/trash/`（详见下方记录），现统一归档到 `results_archive/`，保持 `results/` 目录干净，仅存放当前有效结果。

**变更摘要：**
- 移动文件：143 张（`results/trash/` → `results_archive/trash/`）
- `results/trash/` 已清空
- 原始数据未丢失，可在 `results_archive/trash/` 中查阅

## 2026-04-19 10:05 — ~~不可测卡状态修正（5 张）~~ **已回滚**

> 原操作：5 张卡 status completed→failed。因在 Emily 叫停前已执行，现按林菡指示回滚。

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
