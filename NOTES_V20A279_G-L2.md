# NOTES_V20A279 — G-L2 還原收割鏈（`credit_wf3_comedy_crew` 授出路徑）

- 版本：v279（base main `4ba3078` v278）
- 拍板：用戶 2026-11-17 23:44 揀 **A：還原成條收割鏈**（唔係研究員建議嘅 B 細改；B／C 作廢）
- 範圍：廖炳星線《頂住成組人》Beat 3 中央真分叉嘅後果鏈，由頭斷咗嗰條（v267 刪傳聞系統嗰陣連收割 grant 一齊刪；抉擇掛喺已刪隱藏通告試鏡 hook 度，`liaoChoice` live 0 命中；`grudgeDue` 從來無寫入）

## 還原咗乜（逐項）

### 1. ENC79 新 beat `liu_steal`（Beat 3 搶鏡抉擇）
- DLG：`ENC79_DLG_liu_bingxing.beats.liu_steal`（插喺 `liu_tease` 之後、`liu_repay` 之前）
  - 場景：1991 年秋，紅棉影業片場，《笑住過肥年》茶樓一場；阿偉飾演茶樓新請嘅夥計，呢個位係金主讓出嚟先有嘅，成組人都知
  - 兩選項：「照劇本演，企返自己個位」（旗 `enc79_liu_steady`）／「搏一搏，自己加戲搶鏡」（旗 `enc79_liu_steal`）
  - 對白廣東話、敘述香港式書面語；無黑名單詞（新測試有斷言）
- 註冊表：`ENC79_BEATS.liu_bingxing` 插喺 `liu_tease` 之後、`liu_repay` 之前，保 PLAN 次序（Beat 3 先於 Beat 4）
  - 閘門：`ys.year===1991 && ys.season==="秋" && enc79TierOf(st.fav)>=2 && !(S.wf3 && S.wf3.liaoChoice) && enc83NodeDone("C8")`
  - 一次性（問過就唔再開）；1991 冬之後閘口關閉，`liu_repay` 照開（唔會永久 block 後面 beats）
- `enc79ChoiceFx`：`beat:liu_steal`——搶鏡 fav 1／fx `liu_steal`；照劇本演 fav 2／fx `liu_steady`
- `enc79RunChoiceFx`：`liu_steal`／`liu_steady` 只落旗 `S.wf3.liaoChoice`；結算唔喺呢度做

### 2. `wf3SettleTick` 還原兩段（照 pristine L42751–42785／L42801–42812 骨架）
- **抉擇結算**（tick 開頭，`liaoChoice && !liaoSettled`，做一次）：
  - 穩陣 → 行內信用 +2＋報紙 `wf3:liao_steady`「劇組和氣收場　新人獲讚」（聽朝刊）
  - 搶鏡 → +$800＋報紙 `wf3:liao_steal`「新人搶鏡惹不滿　劇組傳出內訌聲」（聽朝刊）＋記面子債 `debt_wf3_liao_grudge`（`dueDay = day+14`，`grudgeDue = day+14`）
- **收割完成**（`liaoHarvest && !liaoHarvestDone` 內，行喺過期分支之前）：
  - `wrapHistory` 有 `gig_1991_film_214` → `liaoHarvestDone=1`、刪債、`favorLedgerNoteSettled("debt_wf3_liao_grudge", "wf3_harvest")`、授 `credit_wf3_comedy_crew`（喜劇組場務／人情債權・喜劇組熟人／「還人情」）
  - **唔標 `redeemedBy`**：兌現留返 `gig_1992_film_202`《笑到最後》殺青嗰陣經 `br89OnGigComplete` 標；收割完成嗰陣標咗，兌現通告就永遠唔開（通用 credit 分支一見 `redeemedBy` 即 `return false`）
  - 傳聞唔還原（傳聞系統 v267 已刪）
- **過期分支唔郁**（Q13／R3：壞帳，唔計 settled，信用 −2；`favorLedgerNoteSettled(…, "wf3_harvest_expired")` 會被帳本拒絕，唔好還原返 pristine 嗰句）
- 原有開窗段唔郁：`grudgeDue` 到期 → `liaoHarvest = { gigDay: day, window: 7 }`＋toast

### 3. 限時窗機制：新 trigger kind `wf3harvest`
- `triggerGigOn` 加 `case "wf3harvest"`：讀 `S.wf3.liaoHarvest`，窗內（`dayIndex ≤ gigDay+window`）先開；唔經 BR89／credit 規則，唔使持債權
- 直接讀 `S.wf3`，唔依賴 `ensureWf3`（測試沙盒／單獨抽取都行）
- 唔係新系統：只係現成 trigger switch 加一個 case，行返 `mergeTriggerGigs` 通知＋`gigsForLocSeasonBoard` 過濾同一條路
- 收割通告季節「秋」：stagger 有實季；板面＋通知兩處豁免季節閘（見 §4），窗開喺冬都照上板

### 4. 新庫收割通告 `gig_1991_film_214`《笑住過肥年》夜景補拍
- 電影／臨記／補拍通告／喜劇／紅棉影業（`film_cotton`）／1991／**季節秋**／1 日／`tv_cameo_short`／req 無／hard 0.4／pay [32,40]／fame [5,10]
- cast 照《笑住過肥年》班底：leadM 廖炳星、leadF 胡美琳、supportF 葉敏芝、supportM null（照 `gig_1991_film_103`）
- `storyKeys: ["wf3_liao_harvest"]`、`trigger: { kind: "wf3harvest" }`
- pay 校準：初稿 [55,65] 照抄 2 日補拍價，1 日計日薪 $60 跌出 DUR90 臨記帶（25–40）；改 [32,40]（日薪 $36，夜景補拍比平日 1 日臨記 [28,32] 略高）
- **季節改秋＋板面豁免（v279 收尾修）**：初稿季節寫「不限」想避開季節閘，結果 stagger 全庫掃描 S5 FAIL——`nat92StaggerEligible` 要求季節喺 `GIG_SEASON_SPAN88` 入面，「不限」唔係合法庫值。改返實季「秋」（拍攝季），再喺 `gigsForLocSeasonBoard` 同 `mergeTriggerGigs` 兩處加豁免：`trigger.kind==="wf3harvest"` 且已觸發嗰陣跳過 `gigSeasonHidden88`（照 NAT92 錯峰豁免嘅同一寫法）。理據：收割通告嘅檔期就係 7 日收割窗本身，唔係上映季；遲秋先搶鏡嘅玩家，窗開喺冬都照上板。其他 trigger 通告照舊跟季節窗。
- 通告庫 287 → **288 張**（1991 年 98 → 99；補拍通告 6 → 7；臨記級 26 → 27；trigger 通告 33 → 34）

### 5. BR89 map 第 14 對（兌現側小洞）
- `BR89_PATRON_OF_GIG` 加 `gig_1992_film_202: "credit_wf3_comedy_crew"`：film_202 殺青經 `br89OnGigComplete` 標 `redeemedBy`，兌現後落板
- film_202 本身（trigger credit 在位）唔郁

## 測試
- 新檔 `tests/test_wf3_279_logic.js`：**53 項全部 PASS**——收割通告靜態／DLG＋註冊表次序／fx／閘門（1991 秋開、問過唔再開、1991 冬關、1990／T1 唔開）／搶鏡全鏈（抉擇→記債→到期→開窗→殺青授債權→film_202 兌現→redeemedBy）／**板面豁免 §5b（5 項：季節秋、冬原本藏起、窗開喺冬照上板、窗未開／窗外唔見）**／穩陣（+2／好評／冇債）／過期壞帳（債銷＋信用 −2＋唔計 settled）
- `tests/test_wf3_82_logic.js` §8 休眠釘反轉（穩陣 +2／好評、搶鏡 +$800／記債／內訌、到期開窗、收割完成清債＋授債權）；鏈 A 照舊休眠；過期分支保留
- `tests/test_wf3_82_static.py` L69 改寫：試鏡 hook 唔返（「企呢個位之前」0 命中），`liaoChoice` 經 ENC79 beat 返嚟；L66／L67 保留（`WF3_LIAO_GIG`／`WF3_LIAO_HARVEST_GIG` 照舊 null，`gig_wf3_` 全檔 0 命中）
- 計數斷言同步（庫 288）：pack P0／P1／P2／P7（＋wf3harvest 1）／P8（cast 232）／每年張數 111／99／78；grant T0；dur90 A4；press94 A10（newlib 288、reshoot 7、named 155／base 133）；trigger T0／T8（BR89 14 對）／T10；br89 H1（14 對）；sideline273 (d) BR89 14 張＋G-L2（`credit_wf3_comedy_crew` code 側 3 處：結局讀位＋tick 授出＋BR89 map）；nat92 E0（MAXED 開齊 34 張，MAXED 加 `wf3.liaoHarvest` 開窗）；years A6／C0／C1（1991 年 99、288 張）；sideline158 T7／T8（14 對）；sideline274 A1（288 張／trigger 34）／D1／D2（14 對）；stagger S5（收割通告季節秋，stagger 合格）
- **釘行 resync（`qa279/resync279.py`，difflib 對位核實純漂移）**：index.html 淨 +99 行（106 加／7 刪）。gift185 總行數 46030→46129；tang171／tang173 總行數 46030→46129、openLoc DEF 41280→41377；rom176 4 釘各 +97；travel114 COUNT 12＋FREE 40＋DEF 41280→41377＋WRAPPER 28636→28693 全部按映射重寫，內容逐行核實相同。
- 全套 suite：見回報（基線 343／9）

## 同原設計出入（有意圖，唔係漏做）
1. **轉平台**：原 Beat 3 係試鏡前 modal（掛喺已刪隱藏通告 `gig_wf3_liao_stage` 嘅試鏡 hook 度）；而家係 ENC79 beat `liu_steal`。抉擇本身、兩邊後果、14 日＋7 日窗全部照原設計。
2. **結算時機**：原 v82 係殺青結算（揀完去拍戲，殺青嗰陣先結算）；而家無戲可殺青，改為抉擇後翌日 tick 結算一次。`dueDay` 由結算日＋14 計，live 實際係抉擇日＋15（翌日 tick＋14）；窗本身 7 日，1 日差唔影響可完成性。
3. **年份**：原鏈係 1990 年（舞台＋收割通告都係 `year:1990`）；新 beat 係 1991 秋（跟《笑住過肥年》賀歲片 1991 冬上映、秋拍嘅時序＋N9 已完成錨點 C8），收割通告跟 1991 年。1990 年嗰條舊鏈唔返。
4. **傳聞唔還原**：原完成分支另授 `rumor_wf3_comedy_crew`；傳聞系統 v267 已刪，唔還原。
5. **穩陣報紙標題**：原「劇組和氣收場　新人識分寸獲讚」；「識分寸」係黑名單詞，改「劇組和氣收場　新人獲讚」，dek 照寫。
6. **+2／+$800 保留**：PLAN §1 只寫報紙＋記債，冇提呢兩項；但 pristine（NOTES_V20A82＋pristine L42751–42785）同休眠釘（L173／L182）都有，照原設計還原。
7. **舊 id 唔復用**：收割通告用新庫 id `gig_1991_film_214`，唔用舊 `gig_wf3_liao_harvest`（避開舊 id 斷言＋新庫 id 格式）；`WF3_LIAO_GIG`／`WF3_LIAO_HARVEST_GIG` 常數照舊 null。
8. **Beat 5 冷版未接**：WORKORDER 1.1 話搶鏡嗰邊「冷版開」，但 `liu_patron`／`liu_patron_cold` 閘門現時只讀 `enc79_liu_declined`／`enc79_liu_clash_script`，唔讀 `liaoChoice`。本票唔郁 patron 閘（v269 已測行為，唔想順手改）；留跟進票：搶鏡後 Beat 5 行冷版要讀 `liaoChoice==="steal"`。
9. **窗內接咗、窗外先殺青**：過期分支喺 tick 行先（完成分支只喺 `!liaoHarvestDone` 嗰陣行）；即係話，窗尾日之後先殺青唔計完成，照 Q13 當壞帳。收割通告 1 日工，窗內接即日／翌日做得完，邊緣情況極少。

## 驗收（code 側）
- `liaoChoice` 全檔出現：tick 結算＋完成分支讀、RunChoiceFx 寫、beat 閘讀、測試
- `credit_wf3_comedy_crew` code 側 3 處：結局鏈 B 讀位（L12914）＋tick 授出＋BR89 map 值
- 結局鏈 B 而家完成得到：`liaoHarvestDone` 經收割完成設 1（以前只喺過期分支設，永遠到唔到）

## 落地記錄（post-merge）
- main HEAD `b243f2a`（squash merge v279，2026-11-18）
- 全套 suite：**344／9**（9 項全部係已知 pre-existing FAIL：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38；基線 343／9＋新測試檔 1 個）
- GitHub Pages 核實：主頁 200、4,674,100 bytes、與本地 index.html byte-identical
- 工作副本 `linji-work279` 已刪
