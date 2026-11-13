# NOTES_V20A188 — 頒獎禮獎項全部改名＋提名跟角色掛鈎

- 分支：`v20a188`（基底 main `fc76b9e`，v186；唔 rebase，落地嗰陣由統籌做）
- 拍板：用戶 2026-11-13 18:34 定電影／電視／音樂三組跟真實獎項名，廣告組由助手定；
  18:39 助手定咗廣告組 → 15 個新獎項取代舊表 10 個。
- 唔郁：SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、`?v=`（`v20a10`）、
  content pack JSON（`content/STUB_AWARDS_CEREMONY_v1.json` 等原檔零改動）、典禮名、
  提名門檻、對手加權、贏線 0.875、報紙流程。
- 接手：上一手工人 7db54ea4 中途 interrupted，**唔 resume**；本票由接手工人喺佢半成品上完成。
  上一手已落地嘅部分（已核實，唔重做）：覆寫表＋角色閘＋三處接線＋VENUE99 報紙 dek 兩行＋
  新測試兩檔＋舊測試 resync（＋225）＋drive 腳本。接手後補完嘅見 §5。

## 1. 新獎項表（15 個，覆寫表 `AWARDS188_CATEGORIES`，index.html L45438 起）

唔直改 pack JSON——覆寫表喺 index.html 載入層攞優先權（`awardsMvpCategories`／
`awardsStubCategory` 先讀呢度，冇先跌返 schema／stub；舊測試環境冇呢個 const 就行舊路）。

| 典禮 | 新獎項（id） |
|---|---|
| 維港影藝獎 `award_harbour_film` | 最佳男主角 `cat_film_lead_m`、最佳女主角 `cat_film_lead_f`、最佳男配角 `cat_film_support_m`、最佳女配角 `cat_film_support_f` |
| 星河台慶 `award_singho_tv` | 最佳男主角 `cat_tv_lead_m`、最佳女主角 `cat_tv_lead_f`、最佳男配角 `cat_tv_support_m`、最佳女配角 `cat_tv_support_f` |
| 星河金碟夜 `award_golddisc_music` | 最佳男歌手 `cat_music_singer_m`、最佳女歌手 `cat_music_singer_f`、最佳新人獎 `cat_music_newcomer` |
| 維港街招・年度廣告賞 `award_harbour_ad` | 最佳廣告男主角 `cat_ad_lead_m`、最佳廣告女主角 `cat_ad_lead_f`、最佳廣告男配角 `cat_ad_support_m`、最佳廣告女配角 `cat_ad_support_f` |

- 每格有廣東話 `winLine`／`loseLine`／`galleryLine`，唔寫數字承諾。
- 舊表 10 個拎走：年度廣告新面孔／街外最記得住嘅一鏡／最受歡迎出鏡嗓／面孔／
  影壇新面孔（臨記組）／年度票房話題綠葉／最佳電視新人（臨記組）／最受歡迎螢幕面孔／
  綜藝閃光綠葉／最佳班底／群戲／年度新人碟緣（臨記組）。舊獎項名喺工作版 index.html
  全檔 grep 零殘留（TEXTFIX55 遷移表 keys 除外，嗰啲係舊文案對照鍵，唔係玩家面獎項名）。
- 女獎項（女主角／女配角／女歌手）只係典禮獎項表嘅完整 slate——阿偉係男仔，
  永遠唔入玩家提名池（`AWARDS188_PLAYER_GENDER = "m"`）。

## 2. 角色閘判準（提名跟角色掛鈎）

- `awards188WorkRole(w)`：作品算咩位——`lead`／`support`／`singer`／`""`。
  唱片通告桶任何作品都算唱過歌（主唱／和音／MTV 都係開過聲）；綜藝／臨記／替身／武師等
  唔係 lead 亦唔係 support。
- `awards188IsLead(w)`：主角沿用遊戲既有判準 `end95IsLead`（結局梯嗰套，連替身 guard——
  roleScale 話長劇、roleLabel 話替身嗰啲唔可以當主角）＋`awards65IsLeadWork`（v65 代表作嗰套）；
  gig 搵唔到就用 wrap 紀錄本身嘅 roleLabel／作品名兜底。
- `awards188IsSupport(w)`：roleScale 含 `support` 或 roleLabel 含「配角」／「男配」；替身唔係配角。
- `awards188CatEligible(cat, ceremony, year, works)`：lead／support／singer 嗰年嗰媒介
  要做過對應角色先入圍；新人獎要唱過歌＋嗰媒介首年（之前年份冇同媒介殺青，
  用現有 wrapHistory 掃，唔新造追蹤表；舊檔 wrapHistory 截斷咗嘅話新人閘可能誤放，
  只影響獎項名，唔影響提名本身）。
- 接線三處：`awardsEvalTier`（作品數＋雙軌夠數都仲要過角色閘，否則跌返 gallery）、
  `buildAwardResultPack`（提名池只留角色啱嘅獎項；gallery 冇角色就睇全場；
  forceTier debug 嗰陣 eligible 空就跌返全表，唔留空 pack）、`awards62GateLineHtml`
  （觀禮嗰陣講明角色閘原因：「嗰年未做過主角／配角級作品，入圍唔到演員獎」／
  音樂版「嗰年未唱過歌，入圍唔到歌手獎」）。
- 唔郁提名門檻本身（嗰年嗰媒介殺青夠數＋雙軌一條達標）同贏線 0.875。

## 3. 報紙覆寫（贏獎報紙舊名）

- stub JSON `STUB_NEWSPAPER_MORNING_SOFT_v1.json` 嘅 8 款 `award_win` 模板 headline／
  dek／clipLabel 全部用舊獎項名寫——唔改 JSON，行覆寫：
  - `AWARDS188_NP_WIN`（L45636 起）：蓋晒 8 款嘅 headline／clipLabel＋其中 5 款嘅 dek，
    用通用演員／歌手獎寫法（模板唔知玩家贏邊一格，唔寫具體格名）。
  - `VENUE99_NP_DEK` 兩行 dek 修正（本票改）：`np_win_film_02`「年度票房話題綠葉」→
    「奪得演員獎」、`np_win_music_02`「最受歡迎出鏡嗓」→「憑歌聲奪獎」（`np_win_ad_02`
    dek 本身已乾淨，唔郁）。
  - `awards188ApplyNpOverlay(FW)` 喺 `loadFreeplayPacks` 尾段 textfix55＋venue99 之後行。
- 4 款 `award_nominee` 模板本身已乾淨，唔使覆寫；覆寫唔郁 nominee 模板（有測試釘死）。

## 4. Debug 入口

`window.__awards.table188()`（覆寫表）／`eligible188(ceremonyId, year)`（角色啱嘅獎項），
drive 用 `eligible188` 驗 eligible 子集。

## 5. 接手後補完嘅嘢（上一手未做完）

### 5.1 三類 drive FAIL——重跑已全部 PASS，根因如下

上一手 11:21 嗰轉 drive 係 1/18 PASS；重跑（見 §8）係 18/18 PASS。
三類 FAIL 嘅根因同處置：

1. **`newspaper_no_old: false`（6 個 won case）——真 bug，已修（上一手落咗覆寫，唔記得重跑驗）。**
   贏獎報紙 headline 行舊名（例：`維港影藝獎揭曉 阿偉 奪影壇新面孔`）——報紙模板直接讀
   newspaper stub JSON，繞過獎項覆寫表。修法就係 §3 嘅 `AWARDS188_NP_WIN` 覆寫＋
   VENUE99 兩行 dek（上一手 11:23 先寫入 index.html，11:21 嗰轉 drive 未食到）。
   重跑：6 個 won case 報紙 headline 變晒「奪演員獎」／「奪獎」等新寫法，`newspaper_no_old: true`。

2. **`stage_caption_has_label: false`（8 個 nominated case）——probe 寫得太嚴，唔係 game bug。**
   對照 won／nominated 嘅舞台 caption timeline 證實：won 揭曉字幕寫明獎項名
   （`得獎！最佳男配角：《新春大吉》`）；nominated 揭曉字幕寫得主＋玩家代表作名，
   唔寫獎項名（`陸柏言憑《歲歲平安》得獎你嘅《新春大吉》入圍到最後——差少少，下年再嚟。`）——
   獎項名喺白牌上面（`board_is_new_label`＋`board_in_pack` 兩項一路都係 true）。
   處置：修 probe，檢查點改名 `stage_caption_has_content`——won 驗字幕含 pack 任何獎項名，
   nominated 驗字幕含玩家代表作名（有實質內容，唔係空轉）。game code 一行都冇郁。

3. **`seed_roles_found: false`（3 個廣告男主角 case）——probe regex 問題，上一手已修好未重跑。**
   `parse_ad_gigs` 舊版逐行搵會漏 gig36 多行定義；上一手改咗 DOTALL 撈成個 call 再抽欄，
   重跑證實抽到 8 張（7 張 ad_lead＋1 張 exodus ad_support）。
   廣告男主角 gig 喺遊戲庫入面**真係存在**——7 張 gig36 記錄（見 §6），唔係數據缺口嗰隻問題。
   3 案重跑全部 PASS：`ad_nom_lead_932` cat_ad_lead_m nominated 0.4075、
   `ad_won_att_932` cat_ad_lead_m nominated 0.7599（real-ceiling，見 §6）、
   `ad_won_synth_932` 兩隻廣告獎 won 0.89（synthetic-pay，見 §6）。

### 5.2 Resync 補 +29（上一手 +225 計少咗）

上一手 resync（10:56–10:57）按 +225 改咗 5 檔舊測試，但 index.html 其後再加咗 +29 行
（NP_WIN 覆寫＋load 呼叫＋gate 行＋debug 入口），總淨變其實係 **+254**（60155→60409 行）。
結果 5 檔舊測試逐個跑全部 FAIL（gift185 1 項／rom176 4 項／tang171 2 項／tang173 2 項／
travel114 23 項）。處置：
- `qa188/resync188_verify.py`：difflib 對位逐個錨點核實——pristine L（fc76b9e）舊行內容逐字等於
  工作版新行內容（travel114 全部 48 個錨點＋rom176 4 個＋tang DEF 2 個），插入區之前 shift +0、
  之後 shift +254，**全部純漂移**，先至准改行號。
- `qa188/resync188_fix2.py`：按驗證結果補 +29（travel114 27 處／rom176 4 處／tang171＋tang173
  各 2 處／gift185 總行數 60380→60409）。
- 5 檔重跑全部 PASS（見 §7）。上一手嘅 resync188.py／resync188_fix.py 留檔，唔刪。

### 5.3 新測試反證 guard（上一手測試本身有 crash）

`tests/test_awards188_logic.js` 對 pristine main 行會喺頂層 `extractConst` throw
（`Error: const not found: AWARDS188_CATEGORIES`＋Node stack trace），唔符合佢自己
header 寫嘅「FAIL（唔 crash）」。補咗反證守衛：開頭先檢查 10 樣 v188 嘢在唔在，
唔在就逐項印 `FAIL 反證：…唔存在` 後 exit 1，唔 throw。重驗：工作版 ALL PASS；
pristine exit 1、10 項 FAIL、零 stack trace。static 反證本身已乾淨（pristine 24 FAIL）。

### 5.4 其他

- `qa188/drive188.json`／`drive188.log` 上一手版備份咗做 `drive188_prev.json`／`drive188_prev.log`；
  重跑寫入 `drive188.json`／`drive188_rerun.log`。
- `qa188/shots188/` 9 張 `err_*.png` 睇過：11:08–11:12 舊 partial run 嘅殘留（例：
  `err_film_won_932.png` 係 new_game 流程中途停喺編輯本週行程畫面）；最終重跑 18 案
  零 ERROR、零新 err shot，呢 9 張係迭代殘留，留檔唔刪。
- 全套 suite 上一手 250/17 嗰轉係 runner 調用錯（冇傳 `<repo-root> <outfile>`，空變數
  `: > ""` 出 `line 10: : No such file or directory`）；已按正確方式重跑（見 §7）。

## 6. 數據缺口：廣告獎實玩贏唔到（跟進事項，唔喺本票修）

- 廣告男主角 gig 喺庫入面只得 **7 張 gig36 記錄**（1989 ×3：`g36_89_spr_adcentral_watch`／
  `g36_89_sum_adcentral_karaoke`／`g36_89_win_adm_clearance`；1990 ×4：
  `g36_90_sum_adcentral_war`／`g36_90_win_adm_newyearad`／`g36_90_win_adcentral_xmas`／
  `g36_90_aut_adcentral_preshow`）；`content/gigs_1990／1991／1992.json` 零 ad_lead，
  開局 GIGS 池亦零 ad_lead。gig36 全部 `stars: 1`。
- `mergeYearGigs36` 按遊戲曆法年注入（`GIGS36_BY_YEAR`：1991 年入 1989 批、1992 年入 1990 批；
  1990 年零 gig36）：所以 **1991 年池有 3 張 ad_lead、1992 年池有 4 張、1990 年池零張**。
  `cat_ad_lead_m` 提名喺實玩 1991／1992 年去得到（1990 年去唔到）。
  （Drive 嘅 1991 ad seed 混咗一張 1989＋一張 1990 gig——嚴格講 1990 gig 要到 1992 年先入池；
  但 1991 年池本身有 3 張 ad_lead，提名路徑喺實玩成立，gate 邏輯證明有效。）
- **贏獎到唔到**：最強現實種子（3 張 ad_lead＋2 張 film_lead，fame 45、credit 50）base
  只有 **0.7599**，低過贏線 0.875；廣告 gig pay 段（最高 [6500, 9500]）＋stars 1 係樽頸。
  `ad_won_synth_932` 用 synthetic-pay（payOverride=25000）行同一條實路徑，兩隻廣告獎贏到 0.89，
  證明贏獎渲染路徑本身正常——缺口喺數據／計分，唔喺 v188 邏輯。
  跟進方向（另開票，唔喺本票做，**唔好自己發明新通告入庫**）：加高質廣告男主角通告
  （高 pay／高 stars）或者檢討廣告計分，否則 `cat_ad_lead_m`／`cat_ad_support_m` 嘅 won
  分支喺實玩永遠見唔到。呢個缺口係舊有（贏線＋pay 段一路都係咁），v188 只係令佢浮面——
  舊獎「年度廣告新面孔」同樣要過 0.875。

## 7. 測試數字

### 新測試（全部 PASS；反證對 pristine main fc76b9e 乾淨 FAIL，唔 crash）

- `tests/test_awards188_logic.js`：**57 項 PASS**（新表 15 個逐個斷言／角色判定 17 項／
  角色閘 12 項／端到端 build 11 項／報紙覆寫 3 項）。反證：pristine exit 1、10 項 FAIL。
- `tests/test_awards188_static.py`：**35 項 PASS**（覆寫表／舊名零殘留／報紙覆寫／接線／
  唔郁嘅嘢）。反證：pristine exit 1、24 項 FAIL。

### 舊測試（逐個直接跑，全部 PASS）

- `tests/test_awards186_logic.js`：14 項 PASS（fixture 換新 label：`cat_tv_lead_m`／最佳男主角、
  `cat_tv_support_m`／最佳男配角；kicker 次序斷言跟 id 序更新：男主角先、男配角後）。
- `tests/test_awards62_logic.js`：56 項 PASS（1 行 fixture label：`最受歡迎男藝員`→`最佳男配角`）。
- `tests/test_gift185_static.py`／`test_rom176_static.py`／`test_tang171_static.py`／
  `test_tang173_static.py`／`test_travel114_static.py`：resync 補 +29 後全部 PASS
  （tang171 22/22、tang173 21/21、travel114 RESULT PASS；見 §5.2）。

### 全套 A/B（正確方式：`bash qa131/run_suite.sh <repo-root> <outfile>`，喺 repo 根目錄跑）

- Baseline（pristine main，`qa188/suite_baseline188.txt`）：**253 PASS／12 FAIL**。
- 工作版（`qa188/suite_work188c.txt`）：**255 PASS／12 FAIL**。
- FAIL 清單完全相同（12 項穩定 FAIL：flash51／giglib36／pacing35／poster59／rumor49／
  slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），
  數字差 +2 就係兩個新 v188 測試。**零回歸**。
- 上一手 `suite_work188b.txt` 嘅 250/17 係 runner 調用錯嗰轉，作廢（見 §5.4）。

## 8. 實駕結果（`qa188/drive188.py` 重跑，18/18 全 PASS，0 pageerror）

- 環境：Playwright venv `/home/hatch/pwenv49/bin/python`、headless shell chromium、
  本地鏡像＋`python3 -m http.server`（port 18890）、播種存檔直接寫 localStorage
  （key `starVolunteer_map_v19w`，slot 1）、實路徑（唔 forceOutcome；debugForceSeasonWindow
  只接受 forceTier）、`Math.random = 0.4`。
- 18 case：932／700 × film／tv／music／ad × won／nominated，另加 ad gallery（角色閘請柬）＋
  ad synthetic-pay won。逐 case 32 項檢查（請柬今晚獎項行＝id 排序新 label／白牌＝焦點新獎項名／
  結果卡 kicker＝pack 類別＋每類 line 逐字／報紙 queue 有 award 項且無舊名／手帳獎項頁有典禮名＋
  徽章＋代表作且無舊名／全 DOM 無舊 label／0 pageerror）。
- 逐 case pack（`qa188/drive188.json`）：
  - film won：support_m＋lead_m，won 0.89／0.89；nom：0.6518／0.5873。
  - tv won：support_m＋lead_m，won 0.89／0.89；nom：0.6518／0.5873。
  - music won：newcomer＋singer_m，won 0.89／0.89；nom：0.5615／0.497。
  - ad nom sup：support_m nominated 0.4287；ad nom lead：lead_m nominated 0.4075；
    ad won att（real-ceiling）：lead_m nominated 0.7599；ad won synth（pay 25000）：
    support_m＋lead_m won 0.89／0.89；ad gallery：兩隻 gallery 0.4632。
- 截圖：`qa188/shots188/` 61 張（每 case invite／result／journal；gallery 只 invite）。
  實證例子：film_won_932 結果卡「得獎・最佳男主角」＋新 winLine「影藝獎台上念到你個名。
  燈光好光，你聽得見自己心跳同掌聲一齊嚟。」、「得獎・最佳男配角」＋「台上念到你個名。
  綠葉都有人記得——今晚，配角企到台中央。」；報紙 headline「維港影藝獎揭曉 阿偉 奪演員獎」。
- 上一手 11:21 嗰轉 1/18 PASS 嘅三類 FAIL 全部解決（根因見 §5.1）。

## 9. 殘留事項

1. **廣告獎實玩贏唔到**（§6）：`cat_ad_lead_m`／`cat_ad_support_m` won 分支實玩見唔到
   （最強現實種子 0.7599 ＜ 0.875）。跟進要另開票（加高質廣告通告或檢討計分）；本票
   唔發明新通告、唔郁贏線／計分。
2. 1990 年廣告典禮：池入面零 ad_lead gig（gig36 1990 年唔注入），`cat_ad_lead_m`
   嗰年提名都去唔到；1991／1992 先有。同 §6 同一數據缺口。
3. `qa188/shots188/` 9 張 `err_*.png` 係 11:08–11:12 舊 partial run 殘留（見 §5.4），留檔。
4. `awards188HadEarlierWork` 新人閘依賴 wrapHistory（上限 90）：舊檔截斷咗嘅話可能誤放，
   只影響獎項名，唔影響提名本身（見 §2）。
5. 本票唔落地：rebase 上新 main（v187 已落地）由統籌落地嗰陣做；設計 review 唔喺本票開。

## 10. Commit 紀錄

- 遊戲＋測試：`a117882`（index.html 淨 +259／−5 行＝+254；新測試 2 檔；
  舊測試 7 檔：awards186／awards62 fixture 換新 label＋5 檔 resync 補 +29）
- NOTES＋qa 證據：（本 commit，見 log）
- Push：`git push origin v20a188`，`git ls-remote` 核實常駐 clone 收到（見落地報告）。

## 11. Rebase 上 v187 main＋重驗（2026-11-13，rebase 工人）

- 新基底：`dcf1b72`（v187 NOTES，開工嗰陣 `git fetch origin` 核實最新 main；v189 未落地）。
  舊基底 `fc76b9e` → 新 HEAD（見 log，本 commit）。
- 衝突：**零衝突**，`git rebase origin/main` 一次過（兩 commit：`307d6de` 遊戲＋測試、
  `eee4918` NOTES＋qa 證據）。v187 郁舞台幾何（L790／807 CSS＋L46313–46838
  awards62 播放層，淨行數 0 嘅原位替換為主），v188 郁獎項覆寫表＋角色閘
  （L45262 起，淨 +259／−5）；兩邊區域唔重疊。
- 兩邊保留核實：`git diff dcf1b72..HEAD -- index.html` 只刪 5 行，全部係 v188 自身
  故意替換（舊 np_win 模板 2 行＋舊 nominee 邏輯 3 行），無刪 v187 任何行；
  v188 標記齊全（`AWARDS188_CATEGORIES` ×8、`awardsEvalTier` ×4、
  `awardsMvpCategories` ×4、`awardsStubCategory` ×3、`AWARDS188_NP_WIN` ×3、
  `VENUE99` ×18）；v187 標記齊全（`y228` ×5、`walkup` ×10）。
- Resync：**零檔案要改**。逐個重跑全部指名測試，全部 PASS——v187 喺 awards 區係原位
  替換（淨行數 0），v188 插入點喺 L45262 之後，釘行測試用內容定位／動態範圍，
  無漂移：`test_awards188_logic.js`（57 項）、`test_awards188_static.py`（35 項）、
  awards186 logic、awards62 logic、gift185／rom176／tang171／tang173／travel114
  全部 ALL PASS；kwan151／tang152（L802 附近 v187 只做原位替換）亦 ALL PASS。
  反證唔重做（無改新測試本身）。
- `node --check`：兩段 inline script 全部 OK。
- 全套 A/B（正確調用 `bash qa131/run_suite.sh <root> <outfile>`）：
  工作分支 **257 PASS／12 FAIL**（`qa188/suite_rebase188.txt`）；
  pristine 對照 `dcf1b72` **255 PASS／12 FAIL**（`qa188/suite_pristine188.txt`，
  clone 自常駐 clone，事後已刪）；FAIL 清單 12 項完全相同（flash51／giglib36／
  pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／
  weave44／weave49／wrap38——全部 pre-existing），+2 PASS 係 v188 兩個新測試。
  註：`/tmp` 512M tmpfs 裝唔落 repo clone（單一 pack 243M，總量 2.3G），
  pristine 改放 `~/workspace/linji-pristine188`，跑完已 `rm -rf`。
- 實駕重跑：`qa188/drive188.py` **18/18 PASS、0 pageerror**
  （`qa188/drive188_rebase.log`，舊結果備份 `qa188/drive188_rebase_prev.json`）；
  v187 舞台幾何改動無整爛獎項流程（stage caption／白牌／結果卡全部 PASS）。
- 本票唔落地：squash merge／push main／設計 review 由統籌做。

## §12 第二次 rebase＋落地（統籌）
- 第二次 rebase：基底 `4283862`（v190，main 落地期間再郁）；新 HEAD `1fd1327`；零衝突（v190 只改 glamour panel CSS L805–810，淨行數 0；v188 15 個新獎項＋角色閘＋報紙覆寫在位，v190 `align-items:flex-end`／`container-type:size`／`calc(40cqh - 8px)` 在位）；resync 毋須改任何檔（index.html 行數前後同係 60409 行）；新測試 logic 57／static 35、v190 測試 32＋33、相關舊測試逐個直跑 0 FAIL；全套 A/B 工作分支 **259 PASS／12 FAIL**，pristine `4283862` **257／12**，FAIL 清單 12 項完全相同；實駕 `drive188.py` **18/18 PASS、0 pageerror**。pristine worktree `~/workspace/linji-pristine190wt` 留咗喺度未刪（跟進清理）。
- 落地：checkout main → `git merge --squash v20a188` → commit `0c29f03` → push main（一次成功）。落地前 main 係 `1029f68`（v190 NOTES，1029f68 只改 NOTES_V20A190.md，合併乾淨）。
- 線上核實：第一次 curl 仲係 v190 舊版（5,311,650 bytes sha `ba40a6a02b6c…`，Pages 部署滯後），等約 3 分鐘後重 curl：**5,330,237 bytes、sha256 `a51871c2b77f…`，同 repo `HEAD:index.html` 完全一致**。`git fsck` 乾淨（dangling commit／tree 各一，正常殘留）。
