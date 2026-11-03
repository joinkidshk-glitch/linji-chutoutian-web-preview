# NOTES｜v19g 劇情簡介滾盡＋作品名固定

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v19g`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19g  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish

**對齊：** tester ?v=19f PASS soft nits（都市梟雄錄 synopsis 裁尾／sheet 標題入 scroller）

---

## 本輪改動

### 1) Synopsis clip／滾唔到尾（都市梟雄錄「桶。」）

**根因：** `.notice_synopsis_frame` `max-height:min(28vh,9.5rem)`＋`overflow:hidden`，內層 `.cn-syn-scroll` `flex:1 1 auto` 喺 max-height flex 下未形成確定高度 → 內滾唔生效，尾字被父層裁掉。

**修法：**
- 簡介框 **取消 max-height 裁切**（`max-height:none`；`overflow:visible`；`.cn-syn-scroll` 唔再獨立 overflow）
- 長文改由 **`.notice_sheet_body` 豎滾** 睇晒（含「垃圾桶。」）
- 保留簡介紙框視覺；`p` 加極短 `padding-bottom` 避免末字貼邊

### 2) Sheet 作品名（橙頭）唔跟身滾走

**根因：** 整張 `.notice_sheet_frame`（含 `h2.cn-work`）喺 `#modal-inner` scroller 內；父層 `overflow:hidden` 亦令 sticky 無效。

**修法：**
- HTML：橙頭下包 `<div class="notice_sheet_body">`（pills→簡介）
- `#mask.casting-sheet-on`：`#modal-inner` 改 `overflow:hidden`＋column flex；`.notice_sheet_frame` 撐滿；**橙頭 `flex:0`**；**`.notice_sheet_body` `flex:1; overflow-y:auto`**
- sticky `#modal-btns` 不變

### 刻意唔改

- v19e 兩欄 `1fr 1fr`
- v19f「類型」「角色職位」／limits 空隱藏
- exact 片酬／違約金／`>N` 色樣
- 「通告期間」中點斷行（可讀 nit）
- **唔** merge gigs JSON／重生／物理切圖 LIVE

---

## 鏡射／部署

`sv-phone-preview` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。  
Commit：`index.html`＋本 NOTES。

Soft≠PASS · 出圖 HOLD
