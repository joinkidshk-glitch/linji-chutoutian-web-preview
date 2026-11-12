# v20a120 LOCFULL120：地點面板改全屏幕

## 改咗咩

**問題根源（已核實，唔使再查）**：v118 上線版沿用舊 bottom sheet 殼（`.sheet`
`max-height: min(72dvh,560px)`，場景圖只係入面一條 210px 高嘅 banner），上面一半地圖、
下面一半面板。用戶 2026-11-12 09:42 實機截圖（香江唱片）證實。Phase 1 樣本
（`linji-locpanel/sample_agency_ho/sample_agency_ho.html`）本身係全屏幕：`.stage`
390×844，場景圖全幅做底，選項卡浮喺底。

**改法（純呈現層，行為／數值／額度計數零改動）**：`index.html` 淨 +127 行。

- `#loc-sheet.locpanel118` 改全屏幕：`inset:0`＋`height:100%`＋`max-height:none`
  （選擇器帶 `#app`，2,2,0，壓得過 v17y 同 toast-up keep-sheet 嗰條
  `max-height: calc(100dvh - 176px)` 規則，後者另有專條覆寫）；`border-radius:0`、
  透明底、safe-area 底 inset 保留。
- `#loc-bg` 由 in-flow banner 變 `absolute inset:0` 全幅底（cover，`center 30%`
  跟樣本）；210px banner 規則已刪，短屏媒體查詢唔再設 150／120px banner 高，
  改收標題／pill 字。
- 標題／描述／`#loc-who` 行 in-flow 頂部，淺米字（`#f8f1de`）＋陰影＋頂部 240px
  漸變暗角（跟樣本 `.scrim-top`）；`.grab` 拖手全屏幕隱藏。
- 額度 pill 由 `absolute`（疊 banner 左上，會撞標題）改行 in-flow：flex order 排喺
  `#loc-who` 之後、地名下面（同樣本「地名→pill」次序一致），左對齊、實底不變。
  flex order 全寫死（標題 1／描述 2／`#loc-who` 3／pill 4／名牌列 5／選項卡 6／
  掣列 7），唔靠 DOM 次序（pill 喺 DOM 入面排標題前面）。
- 選項卡（`#loc-acts`）繼續 `overflow auto` 內滾，成版唔會碌走場景圖；掣列貼住卡底
  （負 margin 食咗 6px gap、去頂框、底圓角），視覺上同一塊米紙卡。
- 負責人企位：闊 120→150px（貼近樣本）；標題收窄 128→164px；`AnchorOwner`
  高度上限 230→400（貼近樣本 400px），下限 120 不變。
- 冇圖素底態（`locpanel118-nobg`）：全屏幕都要實底，唔可以透明見到地圖——還原
  米紙底＋深色字＋冇暗角。
- v118 嗰條 `[hidden]{display:none !important}` 覆寫保留；清 src 時清 alt＋
  render／hide 清名牌文字嗰兩點原封不動。

**fix1（第一輪實駕捉到，即場修好再重駕）**：

1. 選項掣拉長——`.acts` 係 grid，container 一高過內容就會將每粒掣拉長（醫院
   2 粒掣變咗兩大格空卡）。改行 `flex:0 1 auto`＋`margin-top:auto` 貼底：
   選項少嗰陣卡片內容高、上面留返場景（跟樣本）；選項多嗰陣 shrink＋overflow
   auto 照舊內滾；`align-content:start` 兜底。
2. 負責人太細——選項區貼底之後 `actsTop` 低咗，舊公式（腳收 8px 入卡）計出嚟
   得 146–225px 高。腳改收 **120px** 入卡（跟樣本腳入卡 120px 做法），個人
   可以放大、淨係頭＋身喺卡上面見到；未封頂嗰陣頂緣啱啱 y=8，唔頂穿 sheet 頂。
3. 標題換行——有負責人嗰陣「何生事務所 · 中環」喺 1.3rem＋收窄 158px 之下，
   「中／環」斷咗兩行。標題 1.3rem→**1.15rem**（letter-spacing 2px→1px），
   11 字地名＋收窄 164px 都一行過。

## 測試

- 新守門（全部 PASS；pristine main 跑新測試 FAIL，反證成立）：
  - `tests/test_locfull120_logic.js`（node 沙箱，抽真 `locpanel118AnchorOwner`，
    假 DOM）：**9 斷言**——上限 400／中間值／下限 120／腳收 120px（bottom＝
    sheet 高－actsTop－120）／封頂＋未封頂頂緣／短屏 700px 同一公式／owner
    hidden 早退。喺 pristine main 跑 **4 FAIL**。
  - `tests/test_locfull120_static.py`：**43 斷言**——sheet 全屏幕／場景圖全幅底／
    210px banner 已刪／短屏唔再設 banner 高／頂部暗角＋淺米字／pill in-flow＋
    order／選項區貼底唔拉長／負責人 150px＋收窄 164px＋標題 1.15rem／錨定
    400／120／120／素底實底／`[hidden]` 覆寫保留／v114 計數零改動／紀律
    （SAVE／softRev／`?v=`）。喺 pristine main 跑直接 throw（marker 唔存在）。
- `tests/test_locpanel118_static.py` 錨定斷言跟住改（上限 230→400、腳收
  8px→120px，v120 取代 v118 舊值）。
- 全套回歸：pristine main 基線 **163 PASS／12 FAIL**；工作版 **165 PASS／12 FAIL**
  （＋2 新守門檔），FAIL 清單逐字一致（flash51、giglib36、pacing35、poster59、
  rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、
  wrap38）。零回歸。
- 行號漂移一處：`test_travel114_static.py` 因本包淨 +127 行要 resync
  （`qa120/resync_travel114.py` 核實 44 個 `openLoc(` 呼叫點序列逐字一致、內容逐行
  相同，純漂移；COUNT 13／FREE 27 不變，DEF 52492→52616、WRAPPER 43344→43468）。
  註：resync 腳本已改成 idempotent（舊行號由 pristine main 嘅測試檔讀，唔由工作檔讀）。
- 全檔 `node --check` 過（兩段 inline `<script>`）。

## 實駕（Playwright 真 UI 路徑，390×844，`?softPreview=1`，本地鏡像＋http.server）

Driver：`qa120/drive_locpanel120.py`（改 v118 `drive_locpanel118.py` 嚟用；新遊戲槽 3 →
地圖 → 逐個地點篤 pin → ENC79 巧遇對話逐句撳「下一句」直至 sheet 開 → 量度＋截圖）。

- **390×844：15/15 PASS，0 pageerror**。逐間量度：sheet 390×844 蓋滿 viewport、
  場景圖 390×844 全幅、地圖 6 個取樣點全部遮住、sheet 本身唔碌、pill 唔撞標題、
  負責人腳收卡內＋唔頂穿 sheet 頂＋pill 唔撞負責人、返回地圖掣喺 viewport 內。
  選項區內滾實證：rec_hk／ad_adm／rec_star 內容超高嗰陣 `scrollTop` 設定成功；
  其餘 12 間內容啱啱好唔使碌。重入計數 PASS（film_lion used 1→2）、免費返嚟
  PASS（cafe_cha 打聽 modal 後重開，pill／used 唔變）。
- **選項對照（v118 版 pristine main 逐間數一次，唔憑記憶）**：核心選項（除
  「同 X 傾談」／「送禮：X」之外全部行）三跑完全一致——pristine 跑兩次＋工作版
  一次。NPC 傾談／送禮行係逐局隨機（每日 NPC 在場位置唔係 seed 定死）：對照
  證明——pristine 第一跑 vs 第二跑本身已經喺 7 間地點唔同（同一類差異），工作版
  嘅差異全部係同一類，幅度喺對照方差之內。pill／負責人／名牌列 meta 三跑一致。
- **短屏 390×700：3/3 PASS**（agency_ho／cafe_cha／hospital）：sheet 390×700 蓋滿、
  場景圖全幅、agency_ho 負責人圖 118×325、頂緣 y=8、選項區內滾。唯一噪音係
  2 個 console 404（`liu_bingxing_shy.webp`＋`.png`，短屏嗰跑撞正廖炳星巧遇；
  已知殘留，見下，fallback 正常行，唔係 v120 回歸）。
- 截圖：`qa120/shots/`（15 間全套＋`_final.png`）、`qa120/shots_short/`（短屏 3 間）、
  `qa120/shots_pristine/`＋`qa120/shots_pristine2/`（對照兩跑）；log 喺
  `qa120/logs/`，`results.json` 每跑一份。qa 驅動腳本＋log＋截圖留喺工作副本，
  唔入 repo（跟 v121／v122 前例）。

## 合併

- 分支 `v120-locfull`（commit `83f3466`）→ squash 入 main **`a3d3cfe`**（已 push）。
- 合併手尾：第一次 squash 嗰陣工作副本本地 `main` 仲停喺舊 `215b97e`（v118），
  squash commit 錯將 v121＋v122 內容一併包入，push 嗰陣因 non-fast-forward 被拒，
  未有嘢推出去；即場 `git reset --hard origin/main`（`dc12744`）再 squash 一次，
  今次 diff 啱晒（淨 5 檔 v120：409 insertions、52 deletions），先至 push。
  教訓：合併前先確認本地 `main` 已經 fast-forward 到 `origin/main`。
- 線上核實：`curl https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/index.html?v=20a10`
  → HTTP 200、**5,147,719 bytes**、sha256 **`508539d99d3463f8306821ef4e9a0a373c53887771982a4f73df83c3c30d6310`**，
  同本地 main `index.html` 完全一致。注意：push 後即刻 curl 嗰陣線上仲係舊版
  （5,139,966 bytes，v122），等約 2 分鐘 Pages 部署完成先對上。

## 回滾

- `git revert a3d3cfe`（成包只係 `index.html` CSS＋`AnchorOwner` 一式＋2 檔新測試＋
  2 檔測試 resync／斷言更新；revert 即回復 v118 bottom sheet 行為——210px banner、
  負責人上限 230、腳收 8px）。

## 殘留缺口

- 廖炳星欠 `shy` 表情圖（短屏嗰跑撞正佢嘅巧遇，console 404 ×2，fallback 正常行；
  v114／v118 已知舊問題，補圖一票）。
- NPC 每日 在場位置逐局隨機，選項對照要扣起「同 X 傾談」／「送禮：X」行先至
  可以逐字對——將來守門測試想釘死選項清單，要先將 NPC 在場 seed 定死，另開一票。
- v119 剪影接入同時進行中（分支 `v119-shadow`，已推），本包冇掂佢啲檔；合併嗰陣
  main 仍係 `dc12744`，無衝突。
