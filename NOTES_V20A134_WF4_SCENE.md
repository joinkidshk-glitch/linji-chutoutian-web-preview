# NOTES_V20A134_WF4_SCENE — WF4 隨機事件灰色舞台底處理

## 背景
- v133 修好 WF4 對話框喺短 viewport 被切（舞台改 viewport-aware）。但嗰啲事件本身
  冇場景圖，舞台底係 v105 既定 fallback（米色漸變＋旁白深 scrim），一片灰。
- 用戶 2026-11-12 19:24 拍板：「灰底都一併處理」。
- 場景圖出圖硬規矩：先搵真實香港相做參照先重新生成，齋文字描述出圖唔合格；
  參照相存 DEV 留檔；相入面文字／真人樣唔抄（無字、一般化）。

## 盤點（36 單 WF4 事件）
- 18 單有 `loc`：經 `LOC_SHEET_BG` 已有場景圖，唔使郁。
- 18 單無 `loc`：全部係 `trig:"day"` 事件。`wf4Scene105` 喺地圖（`atLoc` null）
  嗰陣回空字串 → 灰底。覆寫表按事件 `setting` 映射（setting 先係正確場景，
  玩家身處地點唔代表事件發生地），優先過 `ev.loc`／`atLoc`。
- 覆寫表 `WF4_SCENE_OVERRIDE134` 覆蓋 **16／18**：
  - 屋企組 5 單（home01–04＋day01）→ 新圖 `bg_wf4_home.jpg`
  - 電話亭組 4 單（st01–03＋day02）→ 新圖 `bg_wf4_booth.jpg`
  - 街市組 5 單（st06、st07、st11、day03、day04）→ 新圖 `bg_wf4_market.jpg`
  - set08 廠房門口 → 現有圖 `bg_loc_film_lion.jpg?v=20a104`
  - st04 冰室 → 現有圖 `bg_loc_cafe_cha.jpg?v=20a104`
- 剩低 **2 單刻意留灰**（唔硬湊錯圖）：st05 卡拉OK包廂、st08 的士車廂。
  3 張新圖上限已用晒；要圖嗰陣另開票。

## 改咗乜
- `index.html` **＋28 行**（約 L40306–40354）：`wf4Scene105` 註解＋優先查覆寫表
  一行＋`WF4_SCENE_OVERRIDE134` 覆寫表。唔改 content pack JSON、唔郁 SAVE key／
  softRev／產品 `?v=`；新圖用自己嘅 cache-buster `?v=20a134`。
- 新場景圖 3 張（`assets/story/locs/`，720×1280，QC PASS，無字無人無水印）：
  `bg_wf4_booth.jpg`（292,635 bytes）、`bg_wf4_home.jpg`（197,370 bytes）、
  `bg_wf4_market.jpg`（339,156 bytes）。參照來源＋QC 見
  `~/workspace/linji-wf4scenes-refs/SOURCES.md`（美荷樓／HKFP 電話亭／1984 街頭／
  1980 廟街真實香港相）。
- 新靜態測試 `tests/test_ui134_wf4scene_static.py`（PASS；喺 pristine main 乾淨
  FAIL 8 項，反證成立）。
- 測試修訂（brittle 斷言撞正 v134 合理改動，遊戲行為無變）：
  - `tests/test_scene104_static.py`：`?v=20a104` 計數 16→18（覆寫表重用 2 張
    v104 地點圖：set08→film_lion、st04→cafe_cha）。
  - `tests/test_travel114_static.py`：插入點（約行 40319）之後嘅行號全部 ＋28
    （FREE_LINES 18 處、COUNT_LINES 6 處、DEF_LINE 53143→53171、WRAPPER_LINE
    43938→43966；已逐行實量核對）。

## 兩個呈現版式（實駕＋讀 code 核實）
`wf4PlayEvent` 按講者有冇全身圖分流（`wf4OnTableIds108`）：
- **DLG106 舞台**：講者有全身圖（阿偉）。場景圖做舞台底（`.sp-bg-layer`），
  對話框係 `.dlg106-plate`。drive 6 單入面 day02、home01 行呢個版式。
- **卡片版式**：講者冇全身圖（魚檔阿姐、臨記頭、旁白等）。場景圖做卡頂 banner
  （`.wf4-scene105` div，inline background-image），下面標題＋內文。
  st06、set08、st04 行呢個版式。v1 drive 只量舞台 selector，所以 st06 明明
  有街市圖都被判 bgOk=False——係量度盲點，唔係遊戲問題。
- 無場景圖嗰陣（st05）：兩個版式都唔出圖——舞台版式出預設漸變，卡片版式
  直頭冇 banner（淨標題＋內文）。

## 實駕驗證（drive v2，`qa134/drive134.py`）
- v2 改動：每單獨立 fresh browser context（新 game → seed → 過一日 → 呈現），
  唔再多單同一 session 串行（v1 串行喺事件之間過場卡住，set08/st04 FATAL）；
  量度雙版式（舞台＋卡片 banner）；流程照抄已驗證嘅 `qa134/probe134.py`。
- 觸發鏈實測（probe 證實）：撳「過一日」→ 確認 modal「確認過一日？」（明確撳
  「確定過一日」）→ day advance → 小休結算 modal「小休（週X）」（撳「返回地圖」）
  → 晨報／WF4 流程 → 事件呈現。盲撳 `#modal-btns` 第一個掣唔可靠（全頁文字
  搜尋會撳到 modal 背後嘅同名掣）。
- **430×700：6／6 事件 bg＋plate 雙 PASS**，failed scene requests: []：
  day02 stage／booth／plateClip −27；home01 stage／home／−25；
  st06 card-img／market；set08 card-img／film_lion；st04 card-img／cafe_cha；
  st05 card-grey（刻意留灰，無圖，對照 PASS）。
- **430×932：6／6 雙 PASS**，同一組版式／底圖／plateClip，failed scene requests: []。
- 截圖：`qa134/shots/wf4_134_*_430x700.png`、`wf4_134_*_430x932.png`（每單一張，
  已目視核對：街市／廠房／冰室 banner、屋企舞台＋阿偉企立、st05 無 banner 卡）。
- 量度檔：`qa134/measure134_430x700.json`、`qa134/measure134_430x932.json`。

## 全套測試（`qa133/run_suite.sh`，基底 632e371）
- 工作副本：**PASS 201／FAIL 12**（共 213 檔，含新測試 test_ui134）。
- Pristine main `632e371`：PASS 200／FAIL 12（共 212 檔）。
- 12 個 FAIL 兩邊完全相同（pre-existing：test_flash51、test_giglib36、test_pacing35、
  test_poster59、test_rumor49、test_slot50、test_soft_tip_111_restore、test_start53、
  test_weave43、test_weave44、test_weave49、test_wrap38），**零回歸**。

## 落地
- 基底 origin/main `632e371`（v143）。中途 main 行前兩次：4832b85（v141）→
  a1b0920（v144，巧遇頻率）→ 632e371（v143，手帳紙面化），每次 rebase＋重驗。
  v144／v143 兩次 rebase 都只係撞 `tests/test_travel114_static.py`（佢哋各自 resync
  過行號）；解法：取對方版做底，逐行實量重算（v144 版：插入點後 ＋28、≥51892
  再 ＋8；v143 版：佢嗰 +43 喺 L5347，WF4 插入點 40319→40362，之後全部 ＋28）。
  index.html 兩次都乾淨合併（WF4 區同佢哋改嘅 ENC79／手帳區無重疊）。
- （落地 commit＋線上核實結果待補）
- **已落地：main `646e16f`**（git 直接合併，冇開 PR；squash，分支 `v20a134`）。
  線上核實通過：index.html **5,202,772 bytes、sha256
  `429edf5e7e1dc5856ea6ebc1124ca58d60288231ebc5dfbec7ca462a33e8fd02`**，
  同 repo HEAD 完全一致；線上 `WF4_SCENE_OVERRIDE134` ×2、`bg_wf4_market` ×5。
