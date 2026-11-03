# NOTES｜v18v 通告 Detail＝《明星志願》招募單 stub（A＋B）

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v18v`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18v  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish  

**對齊：**  
- `PLAN_GIG_CASTING_NOTICE_DETAIL_v1.md` §3 派生＋§4 wireframe  
- `HANDOFF_GIG_CASTING_NOTICE_DETAIL_v1.md`（A＋B only）  
- `ART_BRIEF_CASTING_NOTICE_DETAIL_v1.md`（sheet-first zone／artId）  
- `assets/ui-physical/notice/CASTING_DETAIL_WIRE.md`  
- `PLAN_GIG_CARD_PLAYER_COPY_v1`＋DS 禁詞  

---

## 本輪做咗咩

1. **通告欄**改短卡（`.gig-teaser`）→ 點「點開查看通告」開 **招募單 Detail**。  
2. **Detail** phone **sheet-first stacked**（CSS zone class＝GD artId）：  
   `notice_sheet_frame` → `notice_header_orange`（作品名＋導演 slot）→ `notice_tag_type`／`notice_tag_recruiting` → `notice_period_bar` → `notice_tab_on` → `notice_table_frame`／`notice_table_cell` → `notice_synopsis_frame`。  
3. **`#modal-inner` 豎滾**；**`#modal-btns` sticky**：`btn_leave` 離開＋約試鏡／即場試鏡（或暫未能報）。  
4. **十一欄 A＋B 派生**（唔補 gigs JSON）：見下表。  
5. `SHOW_REQ_THRESHOLD=false`（合／未合；禁 ≥／你X／差N）。  
6. `notice_poster_wall` phone **預設 display:none**（optional／開閘後）。  
7. 出圖 HOLD——**無新 PNG**；現用 CSS＋既有 `seal_*`。

---

## 十一欄 stub 派生（給 劇本／GD／tester）

| # | 欄 | 現況 | stub／缺口 |
|---|---|---|---|
| 1 | 作品名 | `workTitle`∥`《》`∥`title` | 等 C 補 `workTitle` |
| 2 | 類型 | `genreLabel`∥map(`type`) | 等 C 補細類型 `genreLabel` |
| 3 | 招募中 | 引擎派生（可報／未合仍「招募中」；consumed→已殺青） | OK 顯示層 |
| 4 | 導演 | `director`∥**組製未公開** | **缺口**：全庫未填；等用戶 OK 先批次 |
| 5 | 通告期間 | `castWindow`∥`{year}年{season}季檔 · 獲聘後 N 日內 · 約 M 個工作天` | **缺口**：無真實起迄／週數；等 `castWindow` |
| 6 | 角色 tab | MVP 單 tab「角色」；`roleHint` 放簡介下 | 等多 `roles[]` |
| 7 | 條件 | req＋聲望地板；合／未合 | OK；閾值數字唔顯示 |
| 8 | 難易度 ★ | PLAN §3.6（初+hard&lt;0.45→2；初→3；中→4；高／lead→5） | CSS ★／☆；開閘後 `notice_star_*` |
| 9 | 每週／總天 | `shootWeekdays` 去重；`shootDaysHint`／effective；唱片→錄音日 | OK |
| 10 | 片酬 | `pay[0]–pay[1]`；簽約／特殊 **—** | OK MVP |
| 11 | 劇情簡介 | `synopsis`＋可選角色說明 | OK；無展開鈕 |

---

## 點樣開 Detail（tester）

1. 硬 reload：`?v=18v`（SAVE=`starVolunteer_map_v18v`）。  
2. 地圖點音樂／電影等地點 →「只查看通告欄」。  
3. 撳短卡「點開查看通告」→ 招募單 sheet。  
4. 底 sticky：**離開**（返通告欄）／**約試鏡日**／**即場試鏡**（條件未合則暫未能報）。  
5. 抽樣建議：`gig_1988_film_01`《鐵血英雄傳》、`gig_1988_rec_star_spring`《天星序曲》。

---

## 禁詞

玩家面維持 DS：無「有板／睇板／硬鎖／唔能試／薄本」；門檻無「差N／你X／≥」。

---

## 鏡射／部署

`sv-phone-preview` → `star-volunteer-web` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。  

Soft≠PASS · 出圖 HOLD
