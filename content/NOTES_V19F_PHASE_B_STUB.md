# NOTES｜v19f MV3 Phase B label nits（內容等劇本重生 PLAN）

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v19f`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19f  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish  
**對齊：** `PLAN_GIG_MV3_ALIGN_v1` §§3–5；用戶閘（via tester）Phase B UI  
**授權／轉向：** 用戶改——全庫**重生**須先 PLAN；**唔再等**加欄 HANDOFF merge。內容等劇本交 **重生 PLAN**（交 tip／tester 後等 OK）再另開 tip。

---

## 改咗乜（UI only）

Casting Detail（`index.html`）：

| 項 | before | after |
|---|---|---|
| 類型 | pills 行只有 type／genre pill，**無「類型」字** | `.cn-pills` 前綴 `<span class="cn-lab-inline">類型</span>`＋粗 type pill；有 `genreLabel` 且 ≠ 粗則加細類 pill |
| 角色職位 | `gigRoleLineHtml` 用「角色」或「職位」 | **固定** label **「角色職位」**（值仍 `gigRoleLabelText`） |
| 特殊限制 | 空隱藏（`gigSpecialLimitsHtml`） | **不變**（唔加空 stub 行） |
| 條件／檔期欄 | v19e `1fr 1fr` | **保留** |

CSS：`.cn-pills .cn-lab-inline` 藍色粗體，同難易度 lab 語氣。

## 內容（未做／刻意唔做）

- **唔改** `content/gigs_*.json`（取消抽樣 stub；誤 bump 2.4.0 已還原 **2.3.1**）。  
- 庫現時仍 0× `genreLabel`／`roleLabel`／`limits` → UI 顯示粗 type、「角色職位」派生值、特殊限制整塊隱藏。  
- **等劇本重生 PLAN**（唔再等加欄 merge）後另開 tip 整合。

## 鏡射／部署

`sv-phone-preview` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）；commit **只** `index.html` + `NOTES_V19F_PHASE_B_STUB.md`。

Soft≠PASS · 出圖 HOLD
