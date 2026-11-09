# NOTES v20a49 — 傳聞頁提示行（.rumor-hint）對比修復

基線：v20a48（線上 4,209,175 bytes）。只改呈現層 CSS：主 style 段尾新增一段 v49 皮膚段（純新增 18 行，逐行 diff vs v20a48 只有呢段，冇改任何既有行）。模板、JS、內容生成一律冇掂。

## 出事元素同根因（查證，非估）
- 出事行：手帳「傳聞」頁（`#home-pane-rumor`）`.pane-intro` 下面嗰行提示「點兩張剛聽聞，拉埋再確認。」——元素係 `renderRumorPane()` 生成嘅 `<p class="rumor-hint">`。
- 顏色來源：`.rumor-hint` 全檔得一條 base 規則（主 style 段行 3288）：`color:#6b4e2e`（深啡字）、**冇 background**（全透明），冇其他 cascade 對手、冇 !important。
- 底色來源：hint 坐喺 `#rumor-list` 內、直接喺 `#v-home` 上面；`#v-home` 最終生效背景係深色漸變（radial #3a2a22 ＋ linear #2a1f1a→#0a1424）。透明底透出深底 ＋ 深啡字 ＝ 低對比。同 v20a48 修嘅 `.pane-intro` 同類病，仲要更差一級——intro 至少有半透明金底，hint 連底都冇。

## 同 class 全部實例核對（只限傳聞頁）
- `.rumor-hint` 全檔只出現喺 `renderRumorPane()` 兩個分支：(a) 揀齊兩張（mergeOn）時嘅 glow 提示行；(b) 未揀齊、剛聽聞 ≥2 時嘅操作提示行（任務點名嗰句）。兩處都寫入 `#rumor-list`，即傳聞頁範圍之內；其他頁面冇用呢個 class。所以作用域 `#home-pane-rumor .rumor-hint` 一次覆蓋晒兩個分支，唔會波及其他頁。
- 同頁其他次要行順手核對：`.tut-phase2-coach`（實色 #fff8e8 底＋深字）同 `.rumor-card`（實色 #f6e2aa 底）本身可讀，冇事。
- **申報（冇改）**：同頁底部 `.weak-whisper`（行 3279 base 規則）同樣係深啡字 #6b4e2e 配深底、仲加 opacity:.45，客觀對比比 hint 更低；但佢唔係同 class，而且設計上就係「whisper」——一句刻意淡嘅氣氛句（街坊讚美 flavor text，唔係操作指示），改唔改屬設計取捨，留畀主代理／用戶決定，今次唔擅自擴大範圍（靜態測試有守佢原封不動）。

## 修法（同 v20a48 .pane-intro 同一語言，作用域只限傳聞頁）
```css
#home-pane-rumor .rumor-hint{
  background:#fff8e8;
  color:#3a2a18;
  border:1px solid rgba(201,162,39,.65);
  border-radius:8px;
  padding:6px 8px;
}
```
實色米紙底 #fff8e8 ＋ 深字 #3a2a18 ＋ 金邊 rgba(201,162,39,.65)，同 v48 `.pane-intro` 修法逐值一致；padding／radius 跟返 `.pane-intro` base 幾何；hint 嘅 margin／字款由 base 規則保留。特異度 (1,1,0) 勝 base (0,1,0)，base 規則原封不動，其他情境（若日後有）唔受影響。

## 證據
- Computed-style 探針（harness，抽全份真 `<style>` ＋跟真 render 順序砌嘅傳聞頁 DOM，Playwright Chromium 390×844）：
  - 修復前：color `rgb(107,78,46)`（#6b4e2e）、background `rgba(0,0,0,0)`（透明）——深啡字直坐深底。
  - 修復後：color `rgb(58,42,24)`（#3a2a18）、background `rgb(255,248,232)`（#fff8e8），字底對比 **13.02:1**。
- 截圖前後對照（`harness/rumor_hint_before.png`／`rumor_hint_after.png`）：前——hint 一行深啡字浮喺深底、幾乎溶入背景（同實機症狀吻合）；後——hint 成為米紙金邊小紙條，同上面 intro／coach 同一可讀水平同視覺語言；其餘版面逐像素級一致。
- Harness 檔：`harness/build_harness49.js`（同一 DOM 分別抽 v48／v49 index 嘅真 style 砌頁）、`harness/shot49.py`（截圖＋探針；本機 playwright 模組要另開 venv `/home/hatch/pwenv49`，browser binary 沿用 `/home/hatch/pw-browsers` 嘅 headless shell，以 executable_path 指過去）。

## 體積帳
- 4,209,175 → **4,210,205 bytes**（+1,030，全 CSS 文字；新增內嵌素材：0）。距 4.35MB 紀律線仲有約 140KB。

## 驗證
- `node --check`：全檔 2 個 script 段 OK。
- repo tests 全套 **35/35 檔案 PASS**（原 34 ＋ 新 `tests/test_rumor49_static.py` 17 斷言：作用域規則齊值、base 原樣、scoped 只出現一次、其他頁冇份、whisper 原封、紅線）。
- 反證：新靜態測試行落 v20a48 舊檔，7 項作用域斷言 FAIL、其餘 PASS——測試真係捉到今次改動。
- 紅線 grep：SAVE key `starVolunteer_map_v19w` 10 處、`"v20a10"` 7 處、softRev 在位，同 v20a48 一致；主 style 段大括號平衡。
