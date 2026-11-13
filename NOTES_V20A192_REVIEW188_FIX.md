# NOTES_V20A192 — 修 v188 設計 review B1＋C1–C4（一次過）

- 分支：`v20a192`（基底 main `b7ca827`，v189；唔落地，落地由統籌做）
- 拍板：用戶 2026-11-13 20:33「一次過修」B1＋C1–C4；B2 唔係呢票。
- Review 報告：`~/workspace/linji-design-review-v188/REVIEW.md`（B1／C1–C4 各節＋實測證據）。
- 唔郁：SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、`?v=`（`v20a10`）、
  content pack JSON、15 個獎項名／id、提名角色閘、報紙流程、對手加權、典禮名、
  贏線 0.875、計分、gig 庫。

## 1. 改咗乜

### B1：贏獎報紙 8 款模板，7 款舊前提一次過改晒（通用得獎寫法）

範圍係 v188 §3 報紙覆寫兩處：`AWARDS188_NP_WIN`（index.html L45665 起）＋
`VENUE99_NP_DEK`（film_02／ad_02 兩行 dek 喺嗰邊）。headline／dek 全部改寫做
「唔講具體戲份／產品／角色位」；`music_02` 唯一乾淨，唔郁；4 款 nominee 模板＋
8 款 clipLabel 唔郁。

| 模板 | 舊（矛盾） | 新 |
|---|---|---|
| film_01 dek（NP_WIN） | 阿偉憑三句對白搶鏡… | 阿偉憑實力跑出，評審讚其眼神有戲，開始有觀眾記得佢個名。 |
| film_02 headline（NP_WIN） | 影藝獎夜 阿偉茶餐廳食面戲封王 | 影藝獎夜 阿偉奪獎成焦點 |
| film_02 dek（VENUE99） | …臨記生涯添履歷。 | …街坊笑言個樣好抵死，聲望再下一城。 |
| tv_01 dek（NP_WIN） | …多謝監製不殺之恩… | 廠景熬出頭！阿偉獲獎時多謝台前幕後，而家連星河電視台高層都開始留意佢。 |
| tv_02 headline（NP_WIN） | 台慶夜 阿偉靠一句收工了贏街坊票 | 台慶夜 阿偉奪獎贏街坊票 |
| tv_02 dek（NP_WIN） | …綠葉光芒蓋不住… | …拿下演員獎，掌聲蓋不住，聲望再下一城。 |
| music_01 headline（NP_WIN） | 星河金碟夜 新人奪獎 阿偉跑出 | 星河金碟夜 阿偉奪獎跑出 |
| music_01 dek（NP_WIN） | 錄音室和音熬出頭！阿偉憑合唱單曲獲獎… | 錄音室熬出頭！阿偉憑歌聲獲獎，評審指其聲線有市井煙火味，喺行內漸漸有口碑。 |
| music_02 | （乾淨）金碟夜 阿偉奪獎 樂壇多把靚聲 | 唔郁 |
| ad_01 dek（NP_WIN） | 靠一支涼茶廣告突圍！… | 憑廣告突圍！阿偉獲評夠貼地，有街坊味，奪獎殊不容易，街坊開始記得佢個樣。 |
| ad_02 headline（NP_WIN） | 街外一鏡 阿偉憑跌低眼鏡贏掌聲 | 街外一鏡 阿偉奪獎贏掌聲 |
| ad_02 dek（VENUE99） | …奪得此特別獎，綠葉也有春天… | …奪得廣告獎，聲望穩步上揚，商戶開始留意。 |

- 「新人」只准喺新人獎嗰款出現：music_01 會喺贏最佳男歌手嗰陣出，所以 headline／dek
  兩個「新人」字都拎走；新文案逐字驗過無「新人」。
- 代表作名代入做唔到：報紙模板得 `{playerName}` 一個代位
  （`newspaperFillPlayer` 只換玩家名），寫唔到作品名——所以 film_01 dek 用「憑實力跑出」
  而唔係報告建議嘅「憑《新春大吉》跑出」。要寫作品名就要加新代位，唔喺呢票做。
- 註解入面留咗舊→新對照（`AWARDS188_NP_WIN` 上面註解），方便日後審計；舊句只喺註解
  同 TEXTFIX55 遷移表對照鍵出現，唔係玩家面（見 §6）。

### C1：電視男主角 loseLine 一字改

- `AWARDS188_CATEGORIES` cat_tv_lead_m loseLine：「名單滑過你個名——入圍咗，未抱盃。
  還有下一場。」→「…仲有下一場。」全表 15 格 45 行再無「還有」。

### C2：音樂版角色閘句刪走（死文案）

- `awards62GateLineHtml` 刪走 music 分支「嗰年未唱過歌，入圍唔到歌手獎」——
  任何唱片通告作品都算唱過歌，庫入面零 `rec_extra_day` gig，呢句永遠湊唔齊觸發條件。
  修法係加 `medium !== "music"` 守衛：音樂嗰陣唔再推角色閘句，跌返「坐觀禮席睇全場」；
  電影／電視版閘句「嗰年未做過主角／配角級作品，入圍唔到演員獎」一字唔郁。
  唔為一句文案加數據；留返無害死 code 唔如刪走乾淨。

### C3：結果卡第一行跟舞台 focus

- `renderAwardResultHtml`：先用 v184 `awardsCatsSorted184`（id 序）排，再將舞台 focus
  格（`awards63FocusCat(pack)`：pack 內第一個 won／nominated，即係白牌＋揭曉演嗰格）
  移去第一行；其餘格維持 id 固定排序。
- 協調 v184：跨類別穩定排序維持（其餘格照 id 序）；「同屆提名」行取第一個有 fellows63
  嘅類別（各類共用同一份名單），唔受卡序影響；單 focus 舞台設計本身唔郁（唔改舞台演幾格）。
- 實測對照（見 §5）：雙格 won／nom 嗰陣 board＝男配角／新人獎，第一行 kicker 同樣係嗰格；
  舊版係男主角行先。

### C4：旁聽請柬列全 slate

- `renderAwardInviteHtml`：`pack.tier === "gallery"` 嗰陣，「今晚獎項」行改列
  `AWARDS188_CATEGORIES[ceremonyId]` 成個獎項表（表內次序），行尾加「（觀禮）」：
  電影／電視「最佳男主角、最佳女主角、最佳男配角、最佳女配角（觀禮）」；
  音樂「最佳男歌手、最佳女歌手、最佳新人獎（觀禮）」；廣告同電影。
- 女獎只係列名，唔寫「你爭」——阿偉唔會爭女獎；nominee 請柬唔郁（淨列你爭嗰啲）。
  舊環境冇覆寫表就跌返原來寫法（`typeof` 守衛）。

## 2. 測試數字

### 新測試（全部 PASS；反證對 pristine main `b7ca827` 乾淨 FAIL，唔 crash）

- `tests/test_awards192_logic.js`：**31 項 PASS**（B1 生效後 8 款模板逐款斷言——
  templateId 對準＋headline／dek 逐字＋禁字掃描＋music_01 無「新人」＋music_02 唔郁＋
  nominee 唔郁；C1 loseLine 逐字＋全表無「還有」；C2 三種 medium 閘句＋nominee 分支；
  C3 雙格 won focus 行先＋次序反轉跟 focus 走＋單格不變；C4 三典禮全 slate＋nominee 唔郁）。
  反證：pristine exit 1、3 項 FAIL（`阿偉憑實力跑出`／`阿偉奪獎贏街坊票`／`（觀禮）`
  唔存在；「仲有下一場」喺 pristine 其他 loseLine 已有，唔計入反證）。
- `tests/test_awards192_static.py`：**26 項 PASS**（B1 兩表禁字掃描＋music_01 無新人＋
  music_02 唔郁＋nominee 唔入表；C1／C2／C3／C4 結構斷言；唔郁嘅嘢 7 項）。
  反證：pristine exit 1、2 項 FAIL。

### 舊測試更新（行為改動令舊斷言過時，唔係回歸）

- `tests/test_awards186_logic.js`：雙格 kicker 斷言由「id 序男主角先」改做
  「跟舞台 focus（pack 次序面孔先 → 男配角先）」；fixture 嗰行 loseLine
  「還有下一場」→「仲有下一場」（同 game 新文案對齊）；header 註解一併改。
  14 項 PASS。
- `tests/test_awards188_static.py`：閘句接線斷言由「電影／電視＋音樂句齊」改做
  「電影／電視句在位＋音樂句唔再出現」（C2）。35 項 PASS。
- `tests/test_awards186_static.py`：C1 斷言 label 改做「focus 格行先、其餘格維持固定
  id 排序」（檢查字串本身唔變）。PASS。

### Resync（index.html 淨 +32 行，5 檔行號釘）

- 6 個 hunks 全部喺 L45296–46530（VENUE99 dek 0／C1 0／NP_WIN 註解 +7／C4 請柬 +11／
  C3 結果卡 +11／C2 閘句 +3）；總行數 60443→60475。
- `qa192/resync192_verify.py`：difflib 對位核實 **55 個錨點全部純漂移**
  （22 個 +0：插入點前；33 個 +32：插入點後；WRAPPER L44387＋tang173 CSS L4887
  喺插入點前，唔郁；非 equal 區只係 6 個 v192 hunks）。
- `qa192/resync192_fix.py` 執行：travel114 COUNT／FREE dict 插入點後者 +32（26 處）＋
  DEF 54939→54971；rom176 4 處 +32；tang171／tang173 總行數 60443→60475＋DEF 行
  54940→54972／lines[54938]→lines[54970]；gift185 總行數 60443→60475。
  只改數字參數，label／歷史註解唔郁；各檔加咗一行 v192 resync 註解。
- 5 檔重跑全部 PASS（travel114 RESULT PASS／gift185 ALL PASS／rom176 ALL PASS／
  tang171 22/22／tang173 21/21）。

### 全套 A/B（`bash qa131/run_suite.sh <repo-root> <outfile>`，絕對路徑 outfile）

- Baseline（pristine main `b7ca827`，`qa192/suite_pristine192.txt`）：**261 PASS／12 FAIL**。
- 工作版（`qa192/suite_work192.txt`）：**263 PASS／12 FAIL**。
- FAIL 清單完全相同（12 項穩定 FAIL：flash51／giglib36／pacing35／poster59／rumor49／
  slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），
  數字差 +2 就係兩個新 v192 測試。**零回歸**。
- 注意：第一次工作版 suite 跑出 258/17——多出 5 FAIL 全部係上面 resync 嘅 5 檔
  （未 resync 之前）；resync 後重跑即係 263/12。

### Rebase 上 main `f2a6b0c`（v191，統籌做）

- 驗證期間 main 行前咗：v191（C6F 幕號，`f2a6b0c`）落咗地，live 5,336,448 bytes
  sha `9eb1980d…`；分支基底由 `b7ca827` rebase 上 `f2a6b0c` 先落地。
- Rebase 衝突只係 5 檔 resync 舊測試（index.html＋awards 測試乾淨套用）：
  第一次 `git rebase --continue` 撞到 todo 重複 pick（720f112 出現兩次，v153 已知
  現象），`GIT_EDITOR=true git rebase --continue` 之後先見到衝突。
- 解法：5 檔取 HEAD 版（v191 嘅 resync，啱 `f2a6b0c`），再用 difflib 重新對位
  `f2a6b0c` → 工作版（淨 +32，6 個 v192 hunks；腳本 `qa192/resync192_rebase.py`／
  `resync192_rebase2.py`）。第 1 輪腳本有 3 個 bug（rom176 `zip` 錯配多出嘅 2 個
  `line()`、tang DEF off-by-one、tang173 CSS 錨點 4887 應為 4889），第 2 輪修正後
  全部錨點核實純漂移：travel114（46 錨點）DEF 54986→55018、WRAPPER 44434 唔郁；
  rom176 4 處 +32（53416→53448、53784→53816、54923→54955、55017→55049）；
  tang171／173 總行數 60490→60522＋DEF 54986→55018；gift185 總行數 60490→60522；
  tang173 CSS lines[4888] 唔郁。10 檔測試 rebase 後重跑全部 PASS。
- Rebase 後全套 A/B 重跑（`qa192/suite_pristine192_rebase.txt`／
  `suite_work192_rebase.txt`）：Baseline（pristine `f2a6b0c`）**263 PASS／12 FAIL**；
  工作版 **265 PASS／12 FAIL**；FAIL 清單完全相同（12 項穩定 FAIL 同上），
  數字差 +2 就係兩個新 v192 測試。**零回歸**。上面 261／263 係 rebase 前舊基底數字，
  以呢節為準。

## 3. 實駕結果（`qa192/drive192.py`，15/15 全 PASS，0 pageerror）

- 環境：Playwright venv `/home/hatch/pwenv49/bin/python`、headless shell chromium、
  本地鏡像＋`python3 -m http.server`（port 19290，serve 工作副本）、viewport 430×932／430×700、
  LIVE 模式（唔用 `?softPreview=1`）、播種存檔直接寫 localStorage
  （key `starVolunteer_map_v19w`，slot 1）、實路徑（唔 forceOutcome；
  `debugForceSeasonWindow` 只接受 forceTier）、`Math.random` 常數。
- 方法照抄獨立 review（`drive_review188.py`／`b`／`c`）：B1 每媒介 won ×
  `Math.random = 0.4`（模板 _01）／`0.7`（模板 _02，`floor(0.7*2) = 1`），
  用報紙 queue 項 `templateId` 對準模板 id 再逐字對 headline／dek；
  C3 用舞台白牌（boards）對結果卡第一行 kicker。
- 逐 case JSON：`qa192/drive192.json`；截圖：`qa192/shots192/` 24 張
  （每 case invite＋won／nom 結果卡）；log：`qa192/drive192.log`。

| Case | 驗咩 | 結果 |
|---|---|---|
| b1_film_01_932 | np_win_film_01 逐字 | PASS（headline「維港影藝獎揭曉 阿偉 奪演員獎」＋dek「阿偉憑實力跑出…」） |
| b1_film_02_932 | np_win_film_02 逐字 | PASS（「影藝獎夜 阿偉奪獎成焦點」＋dek「…奪得演員獎…」） |
| b1_tv_01_932 | np_win_tv_01 逐字 | PASS（「星河台慶夜 演員獎爆冷由阿偉奪得」＋dek「…多謝台前幕後…」） |
| b1_tv_02_932 | np_win_tv_02 逐字 | PASS（「台慶夜 阿偉奪獎贏街坊票」＋dek「…掌聲蓋不住…」） |
| b1_music_01_932 | np_win_music_01 逐字 | PASS（「星河金碟夜 阿偉奪獎跑出」＋dek「…憑歌聲獲獎…」，無「新人」） |
| b1_music_02_700 | np_win_music_02 逐字（700px） | PASS（「金碟夜 阿偉奪獎 樂壇多把靚聲」＋dek「…憑歌聲奪獎…」） |
| b1_ad_01_932 | np_win_ad_01 逐字（synthetic-pay 25000） | PASS（「維港街招賞 阿偉跑出」＋dek「憑廣告突圍！…」） |
| b1_ad_02_932 | np_win_ad_02 逐字（synthetic-pay 25000） | PASS（「街外一鏡 阿偉奪獎贏掌聲」＋dek「…奪得廣告獎…」） |
| c1_tv_lose_932 | tv lead_m loseLine 逐字＋C3 | PASS（「名單滑過你個名——入圍咗，未抱盃。仲有下一場。」；board 男配角＝第一行男配角） |
| c2_film_gate_932 | 電影角色閘句逐字 | PASS（「嗰年未做過主角／配角級作品，入圍唔到演員獎」） |
| c2_tv_gate_932 | 電視角色閘句逐字 | PASS（同上句） |
| c2_music_gate_932 | 音樂 gallery 無死句 | PASS（請柬零「未唱過歌」） |
| c4_film_gal_932 | 電影 gallery 全 slate | PASS（「今晚獎項：最佳男主角、最佳女主角、最佳男配角、最佳女配角（觀禮）」） |
| c4_music_gal_932 | 音樂 gallery 全 slate | PASS（「今晚獎項：最佳男歌手、最佳女歌手、最佳新人獎（觀禮）」） |
| c4_tv_gal_932 | 電視 gallery 全 slate | PASS（同電影行，單格 pack 都出全 slate） |

- C3 逐案（board vs 結果卡第一行）：film won 男配角＝男配角、tv won 男配角＝男配角、
  music won 新人獎＝新人獎、ad won 廣告男配角＝廣告男配角、tv nom 男配角＝男配角；
  單格 r=0.7 won（男主角／男歌手／廣告男主角）board＝第一行同樣一致。
- C2 音樂分支 live 驗唔到觸發條件本身（按設計永遠觸發唔到）——刪句後音樂 gallery
  請柬零死句＋電影／電視閘句逐字對照，邏輯測試補埋個分支（見 §2）。

### 實駕途中兩單 probe 問題（唔係 game bug，全部已解決）

1. 第一轉 0/15 ERROR：`new_game` 係由 review 腳本 import 返嚟，硬編 port 18892，
   我自己 serve 喺 19290——`ERR_CONNECTION_REFUSED`。修法：drive192.py 自備
   `new_game`（同一流程，指去 19290）。15 張 `err_*.png` 殘留已刪。
2. 第一轉 film gate 兩案 FAIL（`seed_roles_found: false`）：gig 池本身得 1 部 film extra，
   SEED2 播唔齊 2 部，數目閘先行（「仲差 1 部電影作品」）——同 review 自己 b-run
   一樣（佢哋嗰轉都係 1 部）。修法：照抄 review c 腳本 SEED3 literal 播種
   （動作組臨記＋替身，2 部），重跑 PASS。c4_tv_gal 初版閘句預期亦錯：
   得 1 部電視作品嗰陣數目閘先行係正確（review tv_suponly 同一道理），
   閘句斷言改為只喺 c2 專案驗。

## 4. 殘留事項

1. **B2 廣告 won 缺口唔喺呢票**：`cat_ad_lead_m`／`cat_ad_support_m` won 分支實玩
   見唔到（最強現實種子 0.7599 ＜ 0.875），另開票。呢票 ad win 報紙用 synthetic-pay
   （payOverride＝25000）驗渲染路徑，同 v188 做法一致。
2. TEXTFIX55 遷移表對照鍵入面仲有舊 win 模板句（例：「臨記組跑出！阿偉憑三句對白搶鏡」）——
   嗰啲係舊文案→新文案對照鍵，唔係玩家面；v188 已定留返做舊檔遷移，唔郁。
   同理，`AWARDS188_NP_WIN` 上面註解留咗舊→新對照，方便審計。
3. C4 nominee 請柬「今晚獎項」行維持列你爭嗰啲（按任務指示唔郁）——行字本身話係
   「今晚獎項」但淨列 2 格，嚴格講同 C4 原問題同一類；要改行字（例：「你爭嘅獎項」）
   定連 nominee 都列全 slate，等下一票拍板。
4. 實駕用 `debugForceSeasonWindow` 強制路徑驗證——live 玩家頒獎禮本身仲鎖喺 soft 閘後面
   （調查報告 `~/workspace/linji-work-awards-missing/INVESTIGATION.md`；用戶已拍板
   等 v192 落地先開，v194 待派）。呢票改嘅文案／次序／slate 經強制路徑驗證無誤，
   自然觸發要等 v194 拆閘＋全弧 LIVE 重跑先再驗。
5. `qa192/drive192.json` 曾經俾 3 案重跑覆寫過一次（得返 3 案），之後完整重跑
   15 案還原；最終檔係完整版（15 案，`drive192_rerun3.log` 留低做重跑紀錄）。

## 5. Commit 紀錄

- 遊戲＋測試：`720f112`（index.html ＋32 行淨增；11 檔，+423／−59）
- NOTES＋qa 證據：（本 commit，見 log）
- Push：唔 push origin（worktree 式副本 origin 係 github.com；分支本身已經喺常駐 clone，
  commit 喺工作副本就得，統籌會喺常駐 clone 合併）。
- Pristine 對照 clone `~/workspace/linji-pristine192`（b7ca827）事後已刪；
  反證＋baseline suite 已做完，留低 `qa192/suite_pristine192.txt` 做紀錄。

## 落地紀錄（統籌）

- 遊戲 commit `6cfcfbf`（squash merge `v20a192`，基底 rebase 後 `f2a6b0c`）；線上親自 curl
  核實 **5,339,072 bytes、sha256 `df05fdd3740c…`**，同 repo `6cfcfbf:index.html` 完全一致。
- Push main 一次成功；`git fsck --strict` 乾淨（淨係正常 dangling）。
- Rebase 期間 main 由 `b7ca827` 行前到 `f2a6b0c`（v191 落地），詳見上節。
