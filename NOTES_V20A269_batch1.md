# NOTES — v20a269 第一批：支線補完 廖炳星／顧明輝／麥震東

- 工作副本：`~/workspace/linji-work269/`，分支 `v20a269`，base main `3ab2e22`（v268）。
- 任務：WORKORDER 第 ① 組第一批——只做廖／顧／麥三條線，移植舊 work158 WIP 嘅引擎＋旗＋冷版。
  舊副本 `~/workspace/linji-work158` 只讀；設計來源 `~/workspace/work158_index.diff`（759 行）＋
  `~/workspace/linji-work158/NOTES_V20A158.md` §5–§8＋`~/workspace/linji-sideline-completion/WORKORDER.md` §1–§3＋`PLAN.md` §1–§3。
- 唔改 SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`（`v20a10`）。

## 1. 做咗啲乜（index.html，+80／-7 行）

### 引擎 B+（抉擇 `flags:[...]` 欄位）
- `pushSeg`：options 映射加 `flags:c.flags||null`（`enc79NormSeg` 原樣傳遞 choices，flags 唔會被洗走）。
- 抉擇消費點（`enc79Play` render 內，`if(fx && fx.fx) enc79RunChoiceFx(fx.fx);` 之後）：
  `if(opt.flags) (opt.flags||[]).forEach(f=>{ try{ S.flags=S.flags||{}; S.flags[f]=1; }catch(_g){} });`
- 全部現有 `enc79ChoiceFx` 回傳保持不變（`gu_loan` 唔借繼續 `{fav:-2}` 無 fx，test_enc83 釘位成立）。

### `enc79ChoiceFx` 新分支只加一條
- `beat:liu_clash`：企廖炳星嗰邊 → `{fav:2}`；企導演嗰邊 → `{fav:-1}`。唔加其他。

### 廖炳星
- `liu_repay` 抉擇加 flags：多謝受落 → `enc79_liu_accepted`、推辭 → `enc79_liu_declined`（fx 照舊派 credit）。
- `liu_clash` 加新抉擇 2 選項（企廖炳星嗰邊 → `enc79_liu_clash_stand`、企導演嗰邊 → `enc79_liu_clash_script`）＋when 加 `enc83NodeDone("C13")`（N16 再開口）。
- `liu_foreshadow` when 加 `enc83NodeDone("C8")`（N9 開口）。
- 新 beat `liu_patron_cold`（6 句，T4＋declined||clash_script，無 credit，排暖版之前）＋暖版加排除式條件 `!(declined||clash_script)`。

### 顧明輝
- `gu_loan`「唔借」加 flags `enc83_gu_loan_refused`（ChoiceFx 保持 `{fav:-2}` 無 fx——test_enc83 釘位，唔准改）。
  注意：live label 係「不借，這筆錢我真的幫不了」（書面語），唔係 v148 嘅「唔借，呢筆錢我真係幫唔到」；錨點用 live 現行文字。
- `gu_n10after` 抉擇加 flags（恭喜 → `gu_n10_celebrate`、提 → `gu_n10_warned`）＋BuildScript 變體按
  `enc83_gu_loan_refused` 喺第 2 位插句（「嗰陣你話幫唔到，我唔怪你——但嗰晚我喺枱底數錢嗰陣，諗起你肯坐低，聽我講晒成件事。」）。
  live label 係「恭喜他，終於上岸」／「提醒他以後不要再碰賭」，同 task 核實一致。
- 新 beat `gu_patron_cold`（7 句，T4＋refused||warned，無登台 credit，排暖版之前）＋暖版加排除式條件 `!refused && !warned`。

### 麥震東
- `mak_respect` 抉擇加 flags（隨時候命 → `enc79_mak_accepted`、老實講會驚 → `enc79_mak_honest`，fx 照舊）。
- `mak heart` 抉擇加 flags（守秘密 → `mak_kept_secret`、勸睇醫生 → `mak_told_doctor`）＋`mak_patron` 第 2 位插句變體
  （按 `mak_kept_secret`：「嗰陣你應承幫我守秘密，你真係守到而家——呢份口密，我信得過。」）。
  live label 係「應承幫佢守秘密」，唔係 v148 嘅「應承守秘密」；錨點用 live 現行文字。
  `mak_kept_secret` 唔做閘，只做變體；`mak_told_doctor` 唔係冷路。
- `mak_intel` when 加 `enc83NodeDone("C15")`（N12 開口）。
- 新 beat `mak_patron_cold`（6 句，T4＋mak_honest，無武行 credit，排暖版之前）＋暖版加排除式條件 `!mak_honest`。

### 冷版 shadow 規則（test_enc83／test_enc84 提攜測試所逼）
- 冷版 beat 喺 registry 排喺暖版之前；暖版 when 只加排除式條件，唔加肯定式要求（測試態無旗，肯定式會 fail）。
  測試態（無旗）下冷版唔開、暖版照開，§8 提攜測試保持成立。

### Live 底同 v148 出入（已按 live 為準）
- 傳聞系統已刪（v267）：`enc79GrantFrag`／`enc79GrantRumorCard`／`enc79HasMerged` live 全部 0 命中。
  work158 diff 入面嘅傳聞 context 行（例如 `liu_repay` when 嘅 `enc79HasMerged("rumor_liao_bingxing_money")`、
  `mak_intel`／`mak_respect` 嘅 merged 閘、`liu_foreshadow` 嘅 grants）喺 live 已經唔存在，移植嗰陣無跟到——
  新加嘅閘只係 C8／C13／C15，唔掂傳聞。
- `gu_tease`／`gu_n10after` live 用 `enc83NodeDone("N10")`（N 編號），但 task 指定 C8／C13／C15 嗰三個新閘照用 C 編號
  （`enc83NodeDone` 經 `StoryOC.isDone` fallback `done_<id>`，C id 照讀；同 v158 WIP 寫法一致）。
- DLG 對白經語言重寫，個別行同 v148 唔同（例如 `liu_clash` 尾句改做書面語、mak_visit 尾句改寫）；全部編輯用 live 現行文字做 exact-match 錨點。
- `liu_repay`／`mak_respect` beat 定義無加 `grants(`（test_br89 B9 釘位，新測試有斷言釘死）。

## 2. 測試

### 新測試 `tests/test_sideline269_logic.js`：48/48 ALL PASS
- §1 靜態 12 項（flags 欄位三線、消費點、冷版 beats、clash 新抉擇、registry 閘 C8／C13／C15、暖版排除式、傳聞零殘留、B9 無 grants、BuildScript 變體在位）。
- §2 fx 6 項（clash 企邊邊＋2／−1；liu_repay／mak_respect／gu_loan 唔借無 fx 釘位；liu_accept／mak_accept 經 fx 派債權）。
- §3 節拍閘＋變體 30 項（冷版排暖版之前三線、冷版 DLG 句數 6／6／7、liu C8／C13、mak C15、patron 冷暖分流三線、
  PickBeat 揀冷／無旗揀暖、kept_secret／told_doctor／celebrate 唔係冷路、gu_n10after／mak_patron 變體正反兩面、pushSeg flags 傳遞四處）。
- 由舊 work158 嗰檔 `tests/test_sideline158_logic.js` §1–§3 改寫：刪 hiu（§4–§6）＋刪陸；sandbox 刪走已不存在嘅
  `enc79GrantFrag`／`enc79GrantRumorCard`／`enc79HasMerged`／`enc158LukAbsentTick`／`enc158PrepareNode`；
  Phase 2 陣列（`ENC79_BEATS.gu_mingfai` 等）喺 live 係 T4 區之後嘅獨立賦值，t4Region 切到 `/* ===== v20a84 ENC84` 先包到。

### 有意圖改動嘅舊測試（一處）
- `tests/test_enc83_logic.js`：`EXPECT_BEATS.gu_mingfai` 加 `'gu_patron_cold'`（`gu_n10after` 之後、`gu_patron` 之前）；
  冷版 DLG beat 7 句，滿足同檔 ≥3 句斷言。

### 相關舊測試逐個直接覆驗（全部 ALL PASS）
`test_enc79_logic.js`、`test_enc83_logic.js`（81 項）、`test_enc84_logic.js`、`test_br89_logic.js`、
`test_sideline158_logic.js`（live 嗰檔係 v158 group ② 免試鏡渠道＋GRANT229，85 項，同名唔同檔）。

### 主 script 語法
主 script 第二塊（3,714,326 bytes）抽出 `node --check` 通過（SYNTAX_OK）。

### 全套 A/B（`bash qa131/run_suite.sh`）
- 第一輪（`qa269/suite_work.txt`）：**TOTAL PASS 329 FAIL 14**——基線 333／9＋新測試 1＝334 預期，差 5 項，
  全部係釘行漂移（我淨 +73 行）：travel114（24 項）、gift185（總行數）、rom176（4 釘行）、tang171／tang173（總行數＋openLoc DEF）。
  9 項基線 FAIL 全部在列，零內容回歸。
- Resync（`qa269/resync269.py`，difflib 對位核實純漂移）：travel114 openLoc( 呼叫點序列 58 處逐字一致，
  COUNT 12 處／FREE 40 處／DEF 40549→40622／WRAPPER 28567 唔郁；rom176 4 釘行 38933→39005、39291→39363、
  40434→40507、40590→40663；gift185／tang171／tang173 總行數 45307→45380（鏈尾加 ＋v269 +73）、
  DEF 40549→40622。五檔逐個直接跑全部 PASS。注意：FREE_LINES set 內註解有 `{travelFree}`，
  regex `[^}]*` 會提前截斷，resync 腳本改用行式 parse（舊 qa158 腳本同一寫法喺而家會錯）。
- 第二輪（`qa269/suite_work2.txt`）：**TOTAL PASS 334 FAIL 9**——即基線 333／9＋新測試 1，FAIL 名單同基線逐項相同
  （flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），**零回歸**。

## 3. 唔做嘅嘢＋原因

- **陸柏言全部唔做**：頂一晚機制靠隱藏通告 `gig_intel_lu_standin`，live 已經 0 命中（v252 新庫刪咗），無錨點可移植，
  要重新設計，留跟進票。連帶 `luk_foreshadow` 新抉擇、`luk_thanks` 加閘、`luk_finale`／`luk_patron` 冷版、
  `enc158LukAbsentTick`、殺青 wrap 設 `luk_cover_night`、heart 加閘全部唔做。
- **林曉晴 ROMANCE_V158_OVERRIDES 唔郁**：v266 已落地（`9bb08fc`）。
- **CONTRA98_WHEN_FIX 唔郁**：R_hiu 兩項已喺 live。
- **任何傳聞引用唔准出現**：`enc79GrantFrag`／`enc79GrantRumorCard`／`enc79HasMerged("rumor_...")` live 全部 0 命中
  （v267 已刪傳聞系統）；work158 diff 入面嘅傳聞 context 行係 v148 舊底，錨點一律用 live 現行文字。
- **WORKORDER 1.10–1.17 即派分開＋交心新旗（`liu_heart_*`／`gu_heart_*`）唔做**：嗰啲係第二批（要新庫通告對位）。
- **攻略側項目 1.1–1.9／1.18／1.19 唔做**：parent 做。

## 4. 下一批剩低邊啲

- 第二批：WORKORDER 1.10–1.17（初遇三選／Beat 2 即派分開＋好感差異、交心新旗 `liu_heart_*`／`gu_heart_*` 讀 Beat 5 埋單變體）——要新庫通告對位。
- 陸柏言線重新設計（頂一晚機制無隱藏通告錨點；另加 `luk_finale`／`luk_patron` 冷版、`luk_thanks` 閘、heart 閘）。
- 其餘六條線（駱／魏／齊／彭／鍾／程）：WORKORDER ① 1.4–1.9 分級欄係攻略側；code 側按 PLAN §4–§9 逐線核實（大部份已 A／B 級維持，缺口見 PLAN §10 第二批以後）。
- 即派第一批 25 項（PLAN §10）：G-L1／G-G1／G-G2／G-M1／G-M2 等新通告／新兌現渠道，跟通告重寫新庫一併做，唔喺舊庫上面補。
- 實機驗證押後（Playwright 實駕未做；logic test 已覆蓋閘＋變體＋flags）。
