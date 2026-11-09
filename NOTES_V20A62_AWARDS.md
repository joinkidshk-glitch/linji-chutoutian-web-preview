# NOTES v20a62 — 頒獎優化包（AWARDS62）

依據：用戶 2026-11-10 05:04–05:05 要求「讓玩家追求得獎而不斷嘗試」＋頒獎禮要有動畫呈現（program 形式）；
**05:10 緊急定調改向：動畫用 8-bit 像素風**，同現有休息動畫（`assets/fx/awei-rest-sleep.mp4`）同一套語言——
原 brief 嘅「插畫場景圖＋燈光」B 方案已成段撤換（底圖常量同 CSS 冇殘留，static test 有鎖），唔兩套並存。

**硬規則遵守**：SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=` 冇郁；冇改 pack JSON；
CALIB60（v60）、CONSEQ61 後果包（v61）、結局系統冇郁；awardsLog 既有欄位語義不變（只加 `displayName` 同 `categories[].repTitle` 兩個新欄位）。
index 4,727,010 → 4,780,447 bytes（+53,437：像素底圖 base64 24,872＋AWARDS62 JS 區塊約 23.7K＋CSS 約 1.1K＋接線零碎）。

**測試**：全套 **58/58 files PASS**（基線 56＋新增 2）；新測試 `tests/test_awards62_logic.js`（34 斷言）＋`tests/test_awards62_static.py`（42 斷言），
兩套對 v20a61 index 行都 FAIL（反證成立）；全檔 script `node --check` OK。
另更新 `test_poster59_static.py` 一條全檔 WebP 總數帳：20 → 21（+1 係本版像素舞台底圖，有帳可查；總數仍然鎖死，亂加圖照爆）。

---

## A 部分：評分同追求感改版

### A1 新公式（`awards62ScoreParts` ＋重寫後嘅 `awardsScoreCategory`）

```
base  = 0.40 × normPrimary + 0.42 × worksScore + tagBonus(0.10 或 0)
score = base + taste，taste = (Math.random()*2-1) × 0.05   ← 評審口味，唔主導結果
outcome：tier=gallery → gallery；score ≥ 贏線 0.82 → won；否則 nominated（保留舊 MVP 保底語義）
```

- **normPrimary**：類別主軌值正規化——幕前聲望 stageVolume ÷ 45、業內信用 industryCredit ÷ 60（cap 1）。
  除數按 v60 校準後曲線揀：fame 60 喺慢弧第 73 週先到、屬「成名」標誌，所以聲望軌去到 45 已當滿格料；
  信用係派生值（fame×0.5＋stage×0.3＋acting×0.2＋敘事增量），1990 年勁玩家約 100+，÷60 令中段玩家約 0.7–0.9。
- **worksScore**：嗰年嗰媒介作品按質量 q 降序，`min(1, (q1 + 0.55·q2 + 0.35·q3 + 0.20·q4) / 1.6)`。
  首作權重最大、逐部遞減——質量主導，件數只係配料。
- **tagBonus**：類別 `tagBonusAny` 命中玩家標籤 → +0.10（舊制 0.15，降權令標籤唔好蓋過作品本身）。

### A2 作品質量 q（`awards62WorkQuality`，0.05–1）

主用 gig 嘅 `roleScale`（三年 gig 庫全有呢欄，最結構化）：

| roleScale | q | | roleScale | q |
|---|---|---|---|---|
| film_lead_big / tv_lead_long（擔正） | 1.00 | | film_support_small / tv_cameo_short | 0.55 |
| film_support_main / tv_support_main | 0.78 | | mtv / ad_av / variety_special | 0.48 |
| rec_album | 0.66 | | ad_print / variety_ep / photobook | 0.40 |
| *_extra_day（臨記） | 0.22 | | | |

查唔到 gig 先用片酬段兜底（history 實收 pay 或 gig pay 上限）：≥20000→0.80、≥8000→0.62、≥3000→0.48、≥1200→0.36、否則 0.25。
`stars` 微調：≥5 星 +0.04、≤1 星 −0.04。實證（logic test）：一部擔正 worksScore 0.625，四部臨記得 0.236——
**一部擔正嘅 base 貢獻（0.263）係四部閒角（0.099）嘅 2.6 倍**，「抵兩三部閒角工」達標有餘。

### A3 取消隱形壓分

舊制 `score × 0.72`（第一年／firstYearSoftBias）成段刪除；贏獎骰 `score>=0.78 && Math.random()<0.18` 成段刪除，
全檔再冇呢兩樣嘢（static test 全檔鎖）。第一年自然難贏靠嘅係作品未夠厚、聲望未夠高，唔係暗壓。

### A4 門檻推導（同 v60 校準曲線驗算）

| 玩家像 | 參數 | base | 結果 |
|---|---|---|---|
| 1988 慢弧年尾 | fame 30、電影作品 q 0.55/0.22/0.22 | 0.267＋0.196 ≈ **0.46** | 入圍級，遠離贏線——第一年自然贏唔到 |
| 散工-only | fame 30、4 部臨記 | 0.267＋0.121 ≈ **0.39** | tier 可能入到圍（件數＋dual 夠），但分數贏唔到 |
| 1989 認真谷主角線 | fame 60、一部擔正＋一部主配＋一部閒角 | 0.40＋0.42 ≈ **0.82** | 啱啱掂到贏線——第二年中後開始贏到 |
| 1990 收成期 | fame 100+、作品更厚＋標籤 | **0.92+** | 穩定得獎 |

即追求曲線係：第一年入圍 → 第二年擦邊 → 第三年收成，同三年版主幹節奏對齊。
贏線 0.82 嘅定法：要「滿格主軌（0.40）＋近滿作品分（0.42）」先穩贏，缺一瓣就要另一瓣＋標籤補，
保證贏嗰陣一定係真材實料，唔係骰出嚟。

### A5 標準透明＋代表作

- **代表作**（`awards62RepWork`）：嗰年嗰媒介 q 最高嗰部（只用 wrapHistory，同作品牆同底）；冇作品回空字串，請柬/結果唔會作故仔。
- `buildAwardResultPack` 每類別掛 `repWorkTitle`＋`weakHint62`（入圍未贏先計），pack 掛 `repWork62`＋`standing62` 快照。
- **請柬**（`renderAwardInviteHtml`）：加「你今年憑《X》爭獎」一行＋門檻行（`awards62GateLineHtml`）：
  已入圍→「入圍門檻已達標：嗰年 N 部X作品，憑《X》爭獎。今年好接近贏嗰格。」；未入圍→「今晚席位：觀禮。仲差 1 部電視作品先夠入圍（而家 1/2）；……」——全部玩家語句，冇公式。
- **結果卡**：每類別卡加「憑《X》得獎／入圍」行；入圍未贏加「差啲咩：…」弱瓣句（`awards62WeakHint` 比較代表作級數／主軌／作品量三瓣邊瓣最弱，指路點補）。

### A6 季前目標提示（`awards62SeasonHints`，接 settleWeek 既有 pushFlavor）

唔新造通知系統：喺 `settleWeek()` 嘅 CONSEQ61 段之後、`saveQ()` 之前，每週最多出一行。
規則：只睇今季（d=0，未邀請/未完成）同下季（d=1）嘅典禮；**冬→春跨年跳過**（廣告獎喺春、冬出季前版會用錯年份計作品數）；
只喺「差少少」出聲——入圍差 1–2 部作品、作品夠但 dual 未達基本盤、已入圍且中性分距贏線 ≤0.15（按弱瓣指路）、或者已過贏線（「大熱，記得出席」）。
遠離門檻一律靜默，唔嘈玩家。每行都係指路句（差咩、補咩），同 v58/v60 目標提示同一渠道同一語氣。

### A7 手帳「獎項」頁（`renderAwardsPane62`）

手帳加「獎項」tab（作品同回憶之間，`setHomeTab`／`syncHomeTabExit` 已接線），列歷年記錄：
邊個典禮（新記錄用 log 嘅 `displayName`；舊記錄 fallback 查 ceremony 表，再冇用 medium 對照「電影頒獎禮」等）、
年份季節、得獎／入圍／觀禮／推辭咗徽章、憑邊部作品（新記錄 `categories[].repTitle`；舊記錄冇呢欄就唔出嗰行，唔崩——logic test 有舊記錄樣本驗證）。

### 申報：已知上限

- **wrapHistory 全域上限 20 條**（殺青寫入點既有行為，唔係本版改動）：跨三年計，早期作品會被後期擠走。
  對頒獎嘅影響細——評分只睇「嗰年」作品，而典禮喺嗰年年尾/季尾開，嗰年作品通常仲喺 20 條內；
  但「一年殺青 >20 部」嘅極端玩家，嗰年較早嘅低質作品會先被擠走（留低嘅多數係近期作品），方向上唔會冤枉玩家。
  代表作同 worksScore 同作品牆共用呢個底，行為一致，唔另開新儲存。
- `awards62Standing.dualOk` 用 evalTier 嘅預設基本盤（聲望 ≥10 或 信用 ≥12）做展示/提示近似；schema 若改 anyOf 門檻，展示數字可能同實際 tier 有出入（tier 本身永遠行真 `awardsEvalTier`，唔受影響）。

---

## B 部分：8-bit 像素頒獎動畫（`awards62PlayCeremony`）

出席先播、播完先出結果卡；推辭/稍後完全唔經動畫。引擎係 canvas 步進器：
畫布邏輯解析度 424×240，`requestAnimationFrame` 迴圈但只喺 125ms tick 變先重畫（≈8fps 真步進感），
顯示用 CSS 放大＋`image-rendering: pixelated`（整數感放大唔糊）。全程可跳過（右上「跳過 ⏩」掣）＋撳畫面推進下一 beat；
完成回調有 guard 只行一次；成個 play 包 try/catch，出任何事即刻直入結果卡。

### 素材帳（成套 B 新增 base64 合計 24,872 字元，遠低於 150KB 目標／200KB 硬頂）

| 素材 | 形式 | 體積 | 來源 |
|---|---|---|---|
| 像素舞台底圖 `AWARDS62_STAGE_PX` | WebP data URI 424×240 q82 | binary 18,654 B／base64 24,872 字元 | 出圖管線生成（2048×1152）→ PIL 縮 424×240 |
| 像素阿偉企姿 `AWARDS62_SPR_STAND` | JS pixel map 20×32 | 約 0.7KB 字串 | 程式定義（色板跟休息 FX） |
| 像素阿偉捧杯 `AWARDS62_SPR_HOLD` | JS pixel map 20×32 | 約 0.7KB 字串 | 同上＋金杯圖樣疊胸前 |
| 觀眾/光錐/紙屑/閃光 | canvas 即時繪製 | 0 | 程式色塊 |
| 降級舞台 `awards62FallbackStage` | canvas 即時繪製 | 0 | 底圖載入失敗時自動頂上（深紫格仔＋紅幕色塊＋金邊＋光池） |

### 風格對照驗收（同休息 FX 並排睇過，先算 PASS）

- 休息 FX 實測：848×480、24fps、3 秒；抽幀（frame 30）色板＝深紫牆 `#3a2f4a` 系、深啡木、暖黃燈 `#ffd968`、月光藍。
- 底圖：深紫會場底＋紅幕金邊＋交叉暖黃光錐＋右側金杯基座＋底部觀眾席剪影＋舞台正中光池，中央留空畀精靈企位；
  縮到 424×240 再以 NEAREST 放大 2× 預覽——像素邊脆、色板同 FX 幀一致（深紫＋暖黃主調）。
- 精靈：黑髮、膚色 `#eda87a`、深藍西裝＋白恤衫＋紅呔（跟風格錨阿偉造型），企姿同捧杯兩幀都渲染預覽驗收過
  （企喺底圖光池位、腳底 y=196、比例約佔畫面高 40%，同舞台唔打架；捧杯幀金杯喺胸前、雙耳出到）。
- 阿偉企位/光池座標係按底圖實測光池中心（x=212）定的，唔係估。

### Beat 表（總長：得獎/入圍 8.6 秒；旁聽 3.9 秒）

| # | beat | ms | 畫面 | 字幕條 |
|---|---|---|---|---|
| 1 | open | 1200 | 底圖由暗分 4 格步進亮起（或降級格仔舞台） | —— 典禮名 —— |
| 2 | enter | 1300 | 阿偉企姿由右側逐格行入光池（tick 交替 y −1 扮步行） | 你行入會場，企到台前。 |
| 3 | names | 2200 | 閃光燈白點隨 tick 換位閃爍 | 「入圍名單」＋逐行唱名：類別：《代表作》（約 0.75 秒換一行） |
| 4 | suspense | 1200 | 全場壓暗，剩光池＋阿偉企光中 | 得獎者是…… |
| 5a | reveal·won | 2100 | 捧杯幀（tick 交替彈 −2）＋46 粒像素金紙屑步進跌落 | 🏆 得獎！類別：《代表作》（金字） |
| 5b | reveal·nominated | 2100 | 燈光回暖＋觀眾席掌聲金點閃爍 | 入圍到最後一輪 《代表作》——差少少，下年再嚟。 |
| 5c | reveal·gallery | 2100 | 平實舞台（冇阿偉上台） | 今晚你坐喺觀禮席 睇住台上燈光，記住呢晚。 |
| 6 | out | 600 | 黑場 4 格步進 | （空）→ 自動入返現有結果卡（報紙/快訊/獎勵照舊） |

降級路徑：底圖 `Image` onerror 或未載完 → 每幀行 `awards62FallbackStage`（純色像素格仔舞台），beats/字幕/跳過完全照行；
舊存檔冇代表作欄位 → 唱名行自動用「入圍名單逐個唱出……」兜底，唔崩。

---

## 改動清單（主檔 index.html）

1. 常量 `AWARDS62_STAGE_PX`（像素底圖）插喺 v20a7 AWARDS CEREMONY 段之前。
2. CSS：手帳獎項頁（`.awd62-item`/`.awd62-badge` 等）＋卡片加行（`.psr-rep62`/`.psr-weak62`/`.psr-gate62`）＋像素舞台（`.awd62-stage`/`.awd62-canvas` pixelated/`.awd62-caption`/`.awd62-skip`）。
3. 手帳 HTML：加「獎項」tab 掣＋`home-pane-awards` pane；`setHomeTab`／`syncHomeTabExit` 接線。
4. `awardsScoreCategory` 重寫（新公式）；AWARDS62 區塊（scoreParts/quality/yearWorks/repWork/weakHint/wrapMin/standing/gateLine/renderAwardsPane62/seasonHints＋像素動畫全套）插喺 NEWSPAPER 段之前。
5. `buildAwardResultPack`：加 repWork62/standing62、類別加 repWorkTitle/weakHint62。
6. `commitAwardToLog`：entry 加 displayName、categories 加 repTitle（只加唔改）。
7. `renderAwardInviteHtml`／`renderAwardResultHtml`：加代表作行、門檻行、弱瓣行。
8. `presentAwardInvite` 出席路徑：先 `awards62PlayCeremony` 後 `presentAwardResult`（try/catch 兜底）。
9. `settleWeek`：加 AWARDS62-6 季前提示段（saveQ 之前）。
10. `window.__awards` 加 score62/standing62/rep62/hints62/beats62/play62/pane62 debug 入口。
