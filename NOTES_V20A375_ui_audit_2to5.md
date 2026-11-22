# v375 全畫面檢視優先序 ②–⑤ 改版（2026-11-22）

## 範圍
全畫面雙檢視報告（`~/workspace/linji-ui-audit-2026-11-22/REPORT.md`）優先序第二至五項：
劇情對話／開場、結局總結可讀性、作品牆海報化、手帳週行程。
只改呈現，唔改任何邏輯／數值／判定。GPT-6.2-sol 先出規格（原稿 `~/workspace/linji-drive375/gpt_plan375.txt`＋`.md`），
Gemini 設計圖只作方向；原則：遮字跟 GPT 必修、氛圍跟 Gemini 從嚴。

## 改動（只改 index.html，淨 +116 行）
1. **劇情對話（GPT 判 C：對白被掣遮）**
   - 對話牌高度改跟內容：`height:auto; min-height:170px; max-height:60dvh`，唔再固定高度壓字。
   - 掣列分區：名字牌（role g）做小吊牌排左（order:1），翻頁掣（role p）改摺角樣式
     （`linear-gradient(to top left, transparent 0 12px, #FBF7EE 12px)` 摺角＋朱紅字，order:2 靠右），
     對白文字唔再被任何掣遮住。
2. **結局總結可讀性（雙模型判 C）**
   - 結局內容包一張暖白紙（`.ending375-sheet`，底 `#FBF7EE`）；事業結局名做朱印
     （`.ending375-stamp`，rotate -2deg）；段落加 `.e375-grp` 分隔線；標題卡加 `.ending375-tag`；
     遮罩內掣色跟紙面對比調整。判定邏輯（endingSummaryHtml410 嘅計算）冇郁。
3. **作品牆海報化**
   - 作品卡（`workCard59Html`）海報區右下加「殺青」印（`.work-stamp375`），卡頂加膠紙（`.work-card59::before`）。
   - 履歷行（`jobs72SectionHtml`）加媒介色左邊（`.wrap-clip375`，電影 #8A3028／電視 #365344／
     綜藝 #7C3346／唱片 #6C4F70／廣告 #765017）＋殺青小印（`.clip-stamp375`）。
4. **手帳週行程**
   - 七日格改 3 欄 grid 直式格仔（`#nb-days`，格仔紙背景，第七格跨欄橫排）；
     今日紅圈（`.is-today.wd`）、鎖定日底色（`.locked`）；壓力改溫度計管
     （`.stress-scale363`，12px 圓角管，末端點 #2C6260）。
   - `prefers-reduced-motion` 停新動畫。

## GPT 取捨（冇跟嘅部分）
- 海報區保留 3/4 比例，唔跟 GPT 建議嘅 5:4（現有海報圖資產係 3/4，改比例會裁圖）。
- 確定掣保留 v363 紅墨式，唔跟 GPT 實底掣（同全站手帳語言一致）。
- Gemini 設計圖入面嘅 AI 瑕疵字冇抄，文字一律 app 排字。

## 測試
- JS 語法：node parse 2 個 script block，0 bad。
- Suite 首跑 380 PASS／29 FAIL，逐項分類：
  - 12 項逐個跑 PASS（suite 波動）：awei199、awei201、bust109、delete268、dlg107、dlg119、
    dlg123、dlg126、dlg127、dlg138、home272、travel114。
  - 7 項行號釘漂移已 resync 並逐個覆驗 PASS：gift185、tang171、tang173、rom159、rom176、
    text125、tang152（新總行數 48601；CSS 插入舊 L6501 淨 +115，作品卡 +1 行，規則：舊行
    >6501 且 <16186 → +115，>16186 → +116；錨點內容逐字核實純漂移）。
  - r296_expression_dead_files.js：工作副本環境損壞（qa296 檔 0-byte，clone checkout 中途
    寫入預算被擋，derive296.json 寫唔入），合併後喺常駐 clone 單跑覆驗。
- 相關邏輯測試逐個 PASS：weave410、conseq61、cast252、poster59、menu72、ladder95、
  favor259、gig229、qa101。
- Playwright 實駕截圖四屏：見證據目錄（劇情對話、結局總結、作品牆、手帳週行程）。

## 環境事故
clone checkout 中途 exec 寫入預算被擋（EPERM on write），工作副本大量 qa*/samples* 證據檔
0-byte（唔影響 build／suite）；commit 只 add 指定路徑，唔用 `git add -u`。
Chromium 亦因寫入預算開唔到 profile 而 SIGTRAP，截圖等預算回復後補跑。
