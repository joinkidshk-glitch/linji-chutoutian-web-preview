# NOTES v20a48 — 第三期實機驗收四項打磨（斜度／收紙掣黐紙／眉題去重／傳聞頁對比）

基線：v20a47（線上 4,205,962 bytes）。只改呈現層：CSS 兩處改值＋新增一段 v48 皮膚段＋`renderMorningPaperHtml` 模板一處保守去重。內容生成、edition 數據、`presentDueMorningPaper` 簽名／回傳語義、掣綁定一律冇掂。逐行 diff vs v20a47 共 65 行（改值 3 行，其餘新增）。

## 1. 報紙斜度太輕 → 加大＋掃掠補償
- 朝早報紙 `.paper-sheet`：`rotate(-1.1deg)` → **`rotate(-2.2deg)`**（v47 段內改值）。
- 剪報卡交錯輕斜同步略加（v47 段內改值）：奇卡 `-.55° → -1.1°`、偶卡 `.5° → 1°`，奇偶交錯保持。
- 補償（v48 段）：旋轉掃掠量約 (高/2)·sin2.2°，窄屏最壞約 13px 橫向／7px 縱向。`#mask.paper-on #modal-inner` 加 `padding:10px 16px 14px`——#modal-inner 係捲動盒（overflow-x:hidden 喺 padding box 邊裁），角落落喺 padding 區內唔被裁；`.modal` 底 padding 加到 20px 畀掣欄掃掠位；剪報卡左右各加 5px margin（journal-scroll 本身 padding 得 2px）。
- 證據：harness 兩款幾何（390×844／468×960）computed style 實測紙身 **−2.20°**、剪報奇卡 −1.1°／偶卡 +1.0°（matrix 分量核對）；截圖四角完整冇裁冇出界（paperInsideViewport=true）。

## 2. 收紙掣浮喺紙外 → 同紙一齊斜＋輕疊紙底邊（作用域只限 `#mask.paper-on`）
- `#mask.paper-on #modal-btns`：加 `transform:rotate(-2.2deg)`（同紙身同角度；兩者同闊、各自中心旋轉，斜向一致）；`margin-top:-7px !important`（base 規則係 +8px !important，成欄上移 15px）；`position:relative; z-index:7` 保證疊喺紙面之上。其他 modal 掣欄零影響（base `#modal-btns` 規則原封，靜態測試有守）。
- 配套：紙身 `padding-bottom` 14px → 34px，令掣疊落去嗰陣疊喺紙底留白，唔壓最底嗰行附註。
- 證據：computed style 兩款幾何掣欄均 **−2.20°**；手機版掣疊紙底（截圖：掣貼住紙左下角、附註行完整可見）；高身版（內容超高、行既有捲動）捲到最底截圖：附註行完整現身、掣只疊紙邊留白。桌面版 bounding box 層面掣頂同紙底差 3.6px，角位視覺相接（截圖為證）。

## 3. 眉題同標題重複 → 呈現層保守去重（只改 `renderMorningPaperHtml`）
- 規則：kicker = `e.clipLabel`。計 `kickNorm`（去所有空白）同 `kickTrim`；若 **`headline` 以 `kickTrim` 開頭** 或 **headline 去空白後以 `kickNorm` 為前綴**，就唔出眉題行；其他情況（唔係前綴／冇 headline／冇 clipLabel）原封不動。唔掂 edition 數據同內容生成；短訊欄嘅 paperName 眉題唔喺範圍（語義唔同，冇郁）。
- 證據：新邏輯測試 11 斷言（任務原例 suppress、全同 suppress、去空白前綴 suppress；獨立眉題／只共尾句／長過標題三個反例保留；冇 clipLabel、空 headline 行為不變；標題／dek／聲望行結構完好）。反證：同一測試行落 v20a47 舊檔，三項 suppress 斷言 FAIL、保留斷言 PASS——測試真係捉到改動。harness 亦用真函數生成：去重版日期行直落標題；「獨家直擊」反例版眉題保留（截圖）。

## 4. 傳聞頁說明文字對比 FAIL → 查明＋作用域修復
- 查明：出事嗰段係 `renderRumorPane` 嘅 `.pane-intro`。base 規則（主 style 段開首）係深啡字 `#5a4328` 配半透明金底 `rgba(201,162,39,.12)`——為淺色頁面而設；但傳聞頁 DOM 唔喺米色 `.notebook` 入面，係直接坐喺 `#v-home` 深色底（radial #3a2a22＋linear #2a1f1a→#0a1424）上，半透明底透出深底 ⇒ 深啡字配深啡底，讀唔到。傳聞卡本身有實色 `#f6e2aa` 底所以冇事；同 v20a46 嗰種「規則同情境唔夾」同類。
- 修法（v48 段，作用域只限傳聞頁）：`#home-pane-rumor .pane-intro{ background:#fff8e8; color:#3a2a18; border-color:rgba(201,162,39,.65) }`——實色米紙底＋深字，對比同傳聞卡一致。人情債頁同樣用 `.pane-intro`，唔喺今次範圍，刻意冇郁（靜態測試有守 `#home-pane-debt .pane-intro` 唔存在）。
- 證據：harness 傳聞頁截圖（390×844）——說明段米紙底深字清晰可讀，同下面 coach 行、傳聞卡同一可讀水平。

## 體積帳
- 4,205,962 → **4,209,175 bytes**（+3,213，全 CSS/JS 文字；新增內嵌素材：0）。距 4.35MB 紀律線仲有約 141KB。

## 驗證
- `node --check`：全檔 2 個 script 段 OK；主 style 段大括號平衡。
- repo tests 全套 **34/34 檔案 PASS**（原 32＋新 `test_polish48_logic.js` 11 斷言＋`test_polish48_static.py` 21 斷言）。
- 紅線 grep：SAVE key `starVolunteer_map_v19w` 10 處、`"v20a10"` 7 處、softRev 在位，同 v20a47 一致。
- Harness（證據存 `linji-work48/harness/`）：抽全份真 `<style>`＋真 `renderMorningPaperHtml` 輸出砌 DOM，Playwright Chromium 截圖＋computed-style 探針。`paper_mobile.png`／`paper_desktop.png`（斜度、掣位、冇裁角）、`paper_kicker_kept.png`（眉題保留反例）、`paper_kicker_scrolled.png`（高身版捲到最底）、`rumor_mobile.png`（傳聞說明）、`clippings_mobile.png`（剪報交錯斜＋膠紙貼）。
- Harness 教訓：第一輪剪報截圖冇斜冇膠紙——查明係 harness DOM 漏咗 `#app` 祖先，`#app …` 作用域規則冇生效；補返 #app 包裝後 computed style 核實全部規則在位。遊戲 CSS 本身冇問題。

## 已知限制
- 桌面幾何下掣頂同紙底 bounding box 差 3.6px（唔同元素旋轉盒嘅量法差異），角位視覺相接；手機版係真疊住。
- 高身報紙（內容超過 modal 上限）沿用既有捲動：未捲嗰陣掣黐住「可見紙面」底邊而非紙身真底邊，屬捲動設計嘅必然；捲到最底已核實附註唔被遮。
- 部署後建議主代理照慣例實機覆驗一次（真 edition 長短不一）。
