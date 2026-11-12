# NOTES_V20A131 — UI 風格統一 B 批（B1–B4）

## 拍板
用戶 2026-11-12 17:12 話「好，跟你意見」：B1 畫 2 張企立圖（霞姐＋禮品老闆娘，
地點面板規格要負責人企側邊）／B2 統一做筆記紙／B3 統一米色／B4 維持固定高＋文字
垂直置中。次序 B3→B2→B1→B4。基底 v128 main `259fe1c`。**新制落地，唔開 PR**
（git squash merge → push main，經 deploy key）。

## 改動（index.html 55 行）
- **B3 殺青第三卡統一米色**：`.psr-card.psr-news` 藍底刪除，統一返 `.psr-card`
  預設米色漸變（粉卡 psr-streetFans 唔喺 B3 範圍，唔郁）。
- **B2 事業 tab 筆記紙**：works／awards／memory 三頁 `.journal-scroll` 改筆記紙
  （#f3e6c8＋金邊 #c4a574）；拍攝簿 `.req` 列由深藍盒改紙卡；v76 深底淺字覆寫
  喺事業頁範圍內還原返紙面墨色（其他頁唔郁；`.work-csscard59` 海報代用卡同
  `.gig-card` 內 `.req` 唔郁）。
- **B4 對話框維持固定高＋文字垂直置中**：主線 `.dlg106-plate` 改 flex 縱向＋
  `.sp-line` margin-top/bottom:auto（短句垂直置中，長文溢出嗰陣 auto margin 歸零
  唔裁頂）；巧遇 `.e79-line` display:flex＋align-items:safe center（短句置中，
  超長句跌返 flex-start）。固定高一律唔郁（主線 118px／巧遇 4.65em）。
- **B1 霞姐＋禮品老闆娘企立圖**：`locpanel118OwnerFor` cafe_cha 回
  `xia_jie_base.webp?v=20a131`、gift_shop 回 `gift_lady_base.webp?v=20a131`，
  企位＋名牌（霞姐 · 金龍茶餐廳老闆娘／老闆娘 · 廟街禮品檔，唔憑空起名）；
  noFig 分支留做後備。兩張圖 gen1 即中、QC pass、米白光邊已焗（美術筆記
  `qa131/art/B1_ART_NOTES.md`）。

## 新資產
- `assets/story/fullbody/xia_jie_base.webp`（104,362 bytes，508×1387）
- `assets/story/fullbody/gift_lady_base.webp`（151,314 bytes，563×1825）
- 全身圖庫 146→**148 張**；真檔數目 121→**123 張**。

## 測試（零回歸）
- **新鮮 pristine baseline**（worktree `pristine131-worktree`，259fe1c）：**184 PASS／12 FAIL**，
  同 v128 上線基線一致。
- **Work**：**188 PASS／12 FAIL**（+4＝4 個新 ui131 測試全部 PASS）。
- **FAIL 列表同 baseline 完全一致**（12 個環境性 static FAIL：flash51／giglib36／
  pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／
  weave43／weave44／weave49／wrap38）。
- 新測試：`tests/test_ui131b1–b4_static.py`（4 個，全部 PASS；pristine 反證 FAIL 成立）。
- Resync（11 個）：dlg107／dlg108／dlg109／dlg119／dlg123／dlg126、
  locpanel118_static＋logic（B1 計數／斷言更新，見下）、map54／text125／travel114
  （上一手已做）。
- **Baseline 疑點結論**：上一手 `suite_baseline131.txt` 嘅 177 PASS／20 FAIL 係受污染
  baseline——佢係喺工作副本入面、B1 改動已經存在嗰陣跑嘅，唔係乾淨 pristine。
  正確基線係上面嘅 184／12（新鮮 worktree 重跑證實）。
- **8 個額外 FAIL 嘅原因**（全部係 B1 加 2 張圖嘅預期後果，唔係 bug，已 resync）：
  5 個計數斷言（dlg107／119／123／126 fullbody 146→148；dlg109 真檔 121→123）；
  dlg108 兩個（真檔 121→123；低淨空配對 110→120——實測 pre-B1 121 張／820 對／
  n_shrink 110；加 B1 後 123 張／903 對／n_shrink 120，自動收細機制本身冇問題）；
  locpanel118 兩個（霞姐／禮品檔由 noFig 改做有圖＋名牌；`locpanel118OwnerFor`
  入面已經完全冇 noFig，只剩 `locpanel118Render` 嘅後備分支）。

## 實駕（Playwright 390×844，?softPreview=1，本地鏡像）
- **B1**（`qa131/drive131_b1.py`，`qa131/drive131_b1.json`）：金龍茶餐廳 sheet 開、
  霞姐圖 `xia_jie_base.webp?v=20a131` loaded（nat 508×1387）、名牌「霞姐 ·
  金龍茶餐廳老闆娘」；廟街禮品 sheet 開、老闆娘圖 `gift_lady_base.webp?v=20a131`
  loaded（nat 563×1825）、名牌「老闆娘 · 廟街禮品檔」。**0 pageerror／0 http404**。
  截圖 `qa131/shots/b1_cafe_cha.png`／`b1_gift_shop.png`（兩位負責人企面板側邊＋
  名牌，米白光邊清晰）。注意：入地點可能先觸發巧遇（今次係廖炳星喺茶餐廳），
  要播完 ENC79 先開板；drive 檢測改用 `.e79-line` 有文字為準（唔靠 'on' class，
  實測 overlay class 可能係空但內容已出）。
- **B2／B3／B4**（`qa131/drive131.py`，新鮮重跑，`qa131/drive131.json`）：
  B2 事業 tab 三頁全部 bg rgb(243,230,200)＝#f3e6c8、金邊 #c4a574；
  B3 殺青三卡 metrics／news／streetFans 齊，psr-metrics 米色漸變；
  B4 主線 plateH 118、display flex、column、line margin 上下 26.39px（置中）；
  B4 巧遇 lineH 74、display flex、alignItems safe center、centerGap 上 25／下 27。
- **404 全部 pre-existing**（drive131.json 14 個）：`arc_fong_push1`（jpg／png／webp，
  經 `drive131_pristine404.json` 證實 pristine 同樣有）＋`pang_siuki_sad`（png／webp
  ?v=20a106；`pang_siuki_sad.webp` 喺工作副本同 main 入面都唔存在，係 v127 表情補圖
  批嘅目標——彭少祺 sad 3 句——唔係 v131 引入）。

## 紅線
- SAVE key（`starVolunteer_map_v19w`）、softRev（s107）、產品 `?v=`（v20a10）全部唔郁
  （diff 零出現）；`content/` 零改動；index.html 註解冇寫其他測試硬計嘅版本字串。

## 殘留（唔喺 B 批範圍）
- 巧遇攔截間歇性靜默吞點擊（pre-existing，v126 一樣）：有星在場撳 pin 嗰陣
  intercept 觸發但 overlay 唔出現、板又唔開，額度照扣——要設計決定先修。
- `pang_siuki_sad.webp` 欠圖（v127 表情補圖批）；`arc_fong_push1` 欠圖（pre-existing）。
- D-7 抉擇屏唔出 meta／synopsis（v128 取捨，留返）。

## 出貨
新制：分支 `v20a131` → 常駐 clone checkout main → `git merge --squash v20a131`
→ commit → push main（經 deploy key，唔使 approve；唔開 PR）。
