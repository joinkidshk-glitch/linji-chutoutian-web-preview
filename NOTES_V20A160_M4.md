# NOTES — v20a160-m4 上台領獎 GIF（贏分支 walkup beat）

- 分支：`v20a160-m4`（工作副本 `~/workspace/linji-work160-m4/`，基底 main `e08a070`＝v148）
- 狀態：code＋單元測試＋實駕已完成並驗證（drive160m4 2/2 PASS，見 §5）
- 唔開 PR、唔推 main、唔落地（落地由統籌做）。SAVE key／softRev／`?v=` 一律無郁；無直改 content pack JSON；無新生成（0 次 PixelLab 成本）。
- index.html：58,904 → **58,941 行（淨 ＋37 行）**

## 1. 落點決定

- **資產**：`assets/fx/awd_walkup_m4.gif`（`samples147/m4_walkup_fixed.gif` 原檔複製，sha256 `3d446609…0603` 兩邊一致）。fx 係動畫資產慣例位置（現有 8 條 fx 係 mp4，GIF 同目錄合理）。
- **點解用修好版**：PixelLab 匯出嘅原版 `m4_walkup.gif` 用差分幀（幀 1–8 係局部細格，tile box 如 `(44,21,106,125)`）＋disposal=0，播起嚟上一幀殘留疊埋一齊就係殘影（見 `samples147/SAMPLES147_REPORT.md` 07:14 補記）。修好版係逐格原圖 `m4_frames/` 重編：9 幀全部全幅 `(0,0,144,144)`＋disposal=2＋每幀 120ms。獎盃第 5→6 幀轉手跳位係另一回事，已知、用戶接受，唔重抽。
- **邊個 beat**：贏分支（`bestOutcome === "won"`）先有新 beat **`walkup`**，2200ms，插喺 `reveal` 之後、`glamour`／`out` 之前。贏分支全長 9350 → **11550ms**（冇海報；有海報 13350ms）。gallery／nominated 唔行。
- **點解唔直接疊喺 reveal**：reveal 嗰陣 canvas 已經畫緊玩家行前＋捧杯（`fwd64`＋`hold`），再疊 GIF 會兩個阿偉打架。獨立一個 beat，canvas 壓暗、GIF 做主角——同 v20a147 comfort 加 beat 同一模式。
- **播一次定 loop**：GIF 自帶無限 loop（NETSCAPE loop 0），一圈 9 幀 @120ms＝1080ms；2200ms 播到約兩圈。beat 完 `syncWalkup` 熄層即停；撳畫面快進／跳過掣一樣熄（同 glamour 機制）。
- **呈現**：簡單 `<img>`，唔寫播放器。`.awd62-walkup160` overlay（跟 `.awd63-glamour` 同款全幅層，`position:absolute; inset:0; z-index:2`，暗底 `rgba(10,6,18,.88)`，`pointer-events:none` 等撳掣／快進照通；GIF `width:min(72vw,300px)`、`image-rendering:pixelated`、金框＋光暈）。
- **字幕唔重複**：walkup beat 嘅 caption 係 `""`，文案「阿偉行上台，接過獎盃，高高舉起。」淨係放 overlay 層 `.cap`（跟 glamour 同款）。第一版曾經兩邊都放，實駕截圖見到金字＋台下暗字重複（v147 review B3 同類問題），已改。
- **降級**：圖載唔到，overlay 暗底＋金字照出，canvas 嗰陣 `draw()` walkup case 壓暗，唔會穿崩。

## 2. 改動一覽（index.html，＋37 行）

| 位置 | 改動 |
|---|---|
| CSS（約 L784） | `.awd62-walkup160`／`.on`／`img`／`.cap` 4 條（＋5 行） |
| `awards62CeremonyBeats`（約 L46133） | won 專屬 `walkup` beat：`{ id: "walkup", ms: 2200, caption: "" }`，reveal 之後（＋10 行，含註解） |
| `awards62PlayCeremony` | `walkupHtml`（只限 won）＋拼入 `stage.innerHTML`（＋11 行）；`walkEl`（＋1）；`syncWalkup`（＋4）；`draw()` walkup case 壓暗（＋6）；`advance()`＋初始同步各加 `syncWalkup`（＋2） |

## 3. 測試

### 新測試 `tests/test_awards160_m4_static.py`（26 項，ALL PASS）
- 資產：修好版入庫、原版唔入庫（檔名唔喺 assets 任何檔案）、非空。
- **PIL 殘影回歸防線**：9 幀、144×144、逐幀 tile box 全部 `(0,0,144,144)`（全幅，唔係差分幀）、逐幀 disposal=2、逐幀 120ms。
- 接線：index.html 引用修好版、冇引用原版檔名、walkupHtml 掛 `<img src="assets/fx/awd_walkup_m4.gif">`；walkup 2200ms、只限 won、reveal 之後、beat caption 係空、overlay cap 有文案；syncWalkup／advance／draw／CSS 齊；SAVE key／softRev 冇郁。
- **反證**：同一測試檔對 pristine main（`~/workspace/pristine160m4/`，e08a070）：**17 FAIL／5 PASS，exit 1，唔 crash**。5 項 PASS 係否定式／保存式檢查（原版唔存在、冇引用原版、SAVE key、softRev）。註：PIL 段喺 pristine 因檔案唔存在行 `except` 嗰一項 FAIL，唔係 crash；逐幀子檢查喺嗰邊唔會跑（26 項入面 4 項跳過）。

### 更新咗嘅測試（行號漂移＋贏全長）
- `tests/test_awards62_logic.js` §6：won 全長窗 9–10 秒 → **約 11.5 秒（11550）**；beats 齊 walkup；walkup 2200ms、reveal 之後、caption 係空；入圍全長關係改做「得獎 −walkup 2200＋comfort 2600（即得獎＋400）」；旁聽／入圍冇 walkup。ALL PASS。
- `tests/test_awards63_logic.js` §4：won＋冇海報全長 → **約 11.5 秒**；加 walkup beat 斷言。ALL PASS。
- `tests/test_travel114_static.py`：**純行號 resync**（`qa160-m4/resync_travel114.py`，pristine vs 工作版 difflib 對位，44 個 openLoc 呼叫點內容逐字相同，0 mismatch）。淨 ＋37 行：行號 ＜46131 者 ＋5，其後者 ＋37；DEF 53562→**53599**、WRAPPER 44171→**44176**；COUNT 13／FREE 27 不變。RESULT PASS。
- `tests/test_text125_static.py`：三個釘 ＋5（27800→27805、27913→27918、33516→33521，walkup CSS 段所致）。RESULT PASS。
- 相關測試逐個直接覆驗：awards62_logic、awards63_logic、awards62_static、awards63_static、awards64_chibi_static、awards64_static、venue99_logic、fix65_logic（38 pass, 0 fail）、fix65_static、awards160_m4_static 全部 PASS。

## 4. 全套對照——零回歸（按 v151 教訓：唔齋信一次總數）

- **Pristine 基線**（`~/workspace/pristine160m4/`，e08a070，`qa160-m4/suite_baseline.txt`）：**211 PASS／12 FAIL**。12 項全部係已知 pre-existing（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38）。註：任務書話基線係 210／12 係舊數（v146 數字）；v156 已更正基線係 **211**，今次實跑證實。
- **工作版全套**（`qa160-m4/suite_work.txt`）：**212 PASS／12 FAIL**（＝基線 211＋新測試 1，FAIL 清單同基線逐項相同）。
- 中間曾經跑出 175／49（全係 .py 測試，逐個直接重跑 35 個即 PASS，剩低 14 個入面 12 個係上面穩定 12 項＋text125／travel114 兩個行號漂移——兩個已 resync 修好，見 §3）。按 AGENTS.md v151 教訓，呢啲係環境寫入波動，唔係回歸；判斷以穩定 FAIL 清單＋相關測試逐個覆驗為準。

## 5. 實駕——2/2 PASS（`qa160-m4/drive160m4.py all`，port 8974）

- Seed：`seed_won` 谷爆 dual（fame 500／industryCreditDelta 500）＋1991 年高質作品（電影 lead ×4、電視劇 lead ×2、廣告 ×1，wrapHistory 條目直接帶 `roleScale`，`awards62WorkQuality` 會讀，唔使真 gig）→ film 桶 base **0.90**；`force_won` 重複 force 直到 `pack.bestOutcome==='won'`（兩 case 都係第 1 次即中；`awardsEvalTier` 只認 forceTier gallery／nominee，贏唔可以強制，要靠真分數＋taste 重骰）。
- **won_932**（430×932）：16/16——walkup 層 present、turned on、img 載到（`naturalWidth>0`）、src 係 `awd_walkup_m4.gif`、overlay cap 有「行上台」、dur **2411ms**（直接捕捉，est False）、兩張截圖齊、舞台消失、結果卡「維港影藝獎・結果」有得獎、0 pageerror、0 failed request。GIF 框像素對照：meanDiff **11.722**、**21.2%** 像素唔同（識郁，唔係靜止圖）。
- **won_700**（430×700）：16/16——同上；dur 2738ms（est True，截圖塞住 poll 嘅估算，見下）；GIF 框 meanDiff **7.485**、**18.8%** 像素唔同；0 pageerror。
- Timeline（932）：reveal「得獎！」t≈6094 → walkup t=7894（caption ""、walkupCap「阿偉行上台，接過獎盃，高高舉起。」、imgOk）→ 熄 t=10305 → 結果卡。Beat 時序同規格吻合（walkup 預計喺 open 1200＋enter 1750＋names 2400＋suspense 1400＋reveal 2100＝8850ms 附近出現，實測 7894ms 係因為 watch 喺撳「出席」後 500ms 先起錶）。
- 截圖：`qa160-m4/shots/won_932_walkup_a.png`／`won_932_walkup_b.png`（兩幀唔同：捧杯／行樓梯）、`won_932_result.png`；700 同款三張。結果 JSON：`qa160-m4/drive160m4.json`。
- Harness 備註：① Playwright locator click 喺 start 畫面會 hang（元素可見但 click 唔完成），改用 JS `el.click()`（`click_text`／`dismiss_once`）；② headless 截圖慢（~1 秒／張），poll 未必撞到 walkup→out 嗰一刻，`walkupOffMs` 有時係估算（`totalMs − 500ms out beat`），dur check 嗰陣估算窗放闊到 4500ms；直接捕捉嗰次係 2411ms，2200ms 本身由 logic test pin 死，唔靠實駕量度。

## 6. 未解決事項

- **無**。以下係已知、唔喺呢票範圍：
  - 獎盃第 5→6 幀轉手跳位（逐格先見到，用戶接受，唔重抽）。
  - 典禮舞台細／上下黑帶（v147 review B1）、報紙＋結果卡唔講賽果（B2）等，由 v149 處理；M4 唔摻。
  - M6 燕尾服／M1 會場／M9 音樂／M5 彩紙係其他 v160 工人嘅票，呢度唔掂。
- 附帶觀察（debug 強制路徑 only，唔係本票範圍）：實駕 seed 用假 gigId（`seed160_*`），`repGigId63` 係假 id → `poster59Path` 返空 → 冇 glamour beat。真實路徑（真 gigId）先有 glamour；walkup 同 glamour 順序（reveal → walkup → glamour → out）喺有海報嗰陣未實駕驗過（logic test 驗咗 beats 順序）。

## 7. 檔案

- 改動：`index.html`（＋37 行）；測試檔——`tests/test_awards62_logic.js`、`tests/test_awards63_logic.js`、`tests/test_travel114_static.py`、`tests/test_text125_static.py`。
- 新增：`assets/fx/awd_walkup_m4.gif`、`tests/test_awards160_m4_static.py`、`NOTES_V20A160_M4.md`（本檔）、`qa160-m4/drive160m4.py`、`qa160-m4/resync_travel114.py`、`qa160-m4/drive160m4.json`、`qa160-m4/shots/`（6 張 PNG）、`qa160-m4/suite_baseline.txt`、`qa160-m4/suite_work.txt`。
- `git status`：M index.html＋4 個測試檔；未追蹤 `assets/fx/awd_walkup_m4.gif`、`tests/test_awards160_m4_static.py`、`NOTES_V20A160_M4.md`、`qa160-m4/`。
