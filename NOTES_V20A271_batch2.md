# NOTES_V20A271_batch2 — 支線補完第二批（WORKORDER 1.10–1.17＋陸柏言頂一晚重新設計）

- 版本：v271（分支 `v20a271`；工作副本 `~/workspace/linji-work271`）
- 底：常駐 clone main `e1bf9cc`（v269）。**注意：v270 喺我做緊期間落咗地（main 現為 `e742377`，suite 335／9 新基線）**——呢支分支係喺舊 main 上做，合併前要喺新 main 上 rebase＋重新核實行號漂移（見 §6）。
- 範圍：WORKORDER 1.10–1.17（廖／顧／麥即派分開＋交心新旗）＋陸柏言「頂一晚」機制重新設計。1.18／1.19（攻略側）唔做。
- 改動：`index.html` 淨 +91 行（+97／−6）；`tests/test_sideline271_logic.js` 新測試 71 項；`tests/test_enc83_logic.js` 1 行斷言有意圖改動（顧初遇 +3→+2，配合 E1）；`qa271/resync271.py`（resync 腳本）；`tests/test_travel114_static.py`／`test_rom176_static.py`／`test_rom159_static.py`／`test_gift185_static.py`／`test_tang171_static.py`／`test_tang173_static.py` 釘行 resync（純漂移，見 §5）。
- 唔改：SAVE key、softRev（`s107`）、產品 `?v=`（`v20a10`）。

## §1 逐項：做咗乜

### 1.10 廖初遇（Beat 1）——即派分開本身已落地，呢批只改好感數字

`GRANT229_ENC79` 嘅 `first:liu_bingxing` 三行本身已經係三張唔同通告（v229／v255 落地，`tests/test_gig229_grant.js` 釘死），呢批唔郁對位，只改 `enc79ChoiceFx` 好感（WORKORDER 建議值照做；舊值 → 新值）：

| 揀 | 即派（已落地，唔郁） | 好感 |
|---|---|---|
| 忍唔住笑出聲（key「笑出聲」） | `gig_1990_tv_217`《茶餐廳一幕》喜劇替身雜務（電視劇／臨記／1990 春） | +3 → **+2** |
| 大膽講邊句橋好笑啲（key「好笑」） | `gig_1990_tv_218`《大排檔一夜》喜劇替身雜務（電視劇／臨記／1990 春） | +1 → **+2** |
| 想攞簽名影相留念（fallback） | `gig_1990_tv_219`《片場大龍鳳》喜劇替身雜務（電視劇／臨記／1990 夏） | −2 → **+0** |

### 1.11 廖 Beat 2——已落地，唔使改

`GRANT229_CHOICE` 已有 `W3_ho_liao:W3_ho_liao_a` → `gig_1990_tv_209`《大排檔鬥氣》（電視劇／臨記／喜劇替身雜務／1990 秋，cast leadM 廖炳星）、`:b` → `gig_1990_tv_210`《街市喜宴》（同類／1990 冬，cast leadM 廖炳星）。兩張唔同，呢批 0 改動。

### 1.12 廖 Beat 4 交心——新旗＋Beat 5 變體

- 新旗（live 0 碰撞已核實）：`liu_heart_earnest`（「認真回應」）、`liu_heart_joke`（「用笑話接住」），經 v269 引擎（`pushSeg` options `flags` 欄位）落旗。
- Beat 5 好收尾（`liu_patron`）唔 inline 改原文，跟麥／v269 慣例，喺 `enc79BuildScript` 第 2 位插句變體：
  - earnest → 「你嗰日認真回我嗰句，我收到。肯頂住成班人嘅人唔多，你係其中一個。」
  - joke → 「你嗰日用笑話接我嗰句，我笑完先諗返——識笑，唔代表唔認真。」
  （WORKORDER 1.12 草稿對白，書面語化唔改意思。）

### 1.13 顧初遇（Beat 1）——即派分開已落地，只改好感數字

`first:gu_mingfai` 三行已係三張唔同和音（v229／v255 落地），只改好感：

| 揀 | 即派（已落地，唔郁） | 好感 |
|---|---|---|
| 靜靜站在那裡，聽他哼完那段舊歌（key「聽」） | `gig_1990_rec_209` 劇集主題曲錄音和音歌手（唱片／初級／1990 春，主唱顧明輝） | +3 → **+2** |
| 點頭打個招呼，不打擾（key「招呼」） | `gig_1990_rec_201` 香江唱片大碟錄音和音歌手（唱片／初級／1990 春，主唱顧明輝） | +1 不變 |
| 先走，不要讓人見到我和他站在一起（fallback） | `gig_1990_rec_210`《卡拉OK影碟配唱》和音歌手（唱片／初級／1990 夏） | −2 → **+0** |

### 1.14 顧 Beat 2——抉擇本身唔喺遊戲入面，只做到 DRAFT 表層面

`gu_promise_clean`（應承佢戒賭）／`gu_ask_back`（問返佢）全 repo 0 命中——遊戲入面根本冇呢個抉擇（GRANT229_DRAFT 註解亦寫明「遊戲未有呢個抉擇」）。DRAFT 表已有兩張唔同通告：

- `gu_promise_clean` → `gig_1991_rec_201` 卡拉OK影碟和音歌手（唱片／初級／1991 春）
- `gu_ask_back` → `gig_1991_rec_207`《電視劇金曲錄音》和音歌手（唱片／初級／1991 夏）

即派分開只做到 DRAFT 表層面；**抉擇本身實裝留下一批**（要設計顧 Beat 2 抉擇喺邊度出現、點接返主線，唔係單加兩行表就得）。

### 1.15 顧 Beat 4 交心——新旗＋Beat 5 變體

- 新旗（live 0 碰撞已核實）：`gu_heart_sit`（「陪他坐到天亮，不出聲」）、`gu_heart_quit`（「勸他戒賭，重新來過」），經 v269 引擎落旗。
- Beat 5 好收尾（`gu_patron`，`ENC83_DLG_gu_mingfai.beats`）第 2 位插句變體：
  - sit → 「嗰晚你陪我坐到天光，咩都冇講——嗰種陪法，我記住。」
  - quit → 「嗰晚你話『把聲仲喺度，仲可以重新嚟過』，我返去諗咗成晚。你講得啱。」
  （WORKORDER 1.15 草稿對白，書面語化唔改意思。）

### 1.16 顧 Beat 4 恭喜／提——code 側已分開，攻略側句子留 parent

`beat:gu_n10after` 已派兩張唔同通告（code 側已分開，唔使改）：

- key「岸」（上岸）→ `gig_1992_rec_103`《齊心同行》合唱男歌手（唱片／初級／1992 秋）
- key「賭」（提佢唔好再掂賭）→ `gig_1992_rec_104`《銀幕影》主題曲配唱歌手（唱片／初級／1992 冬）

WORKORDER 要求嘅「後果段＋後果表行加即派分開一句」係**攻略側文字**，唔喺我範圍，留 parent；寫入本 NOTES 備案。

### 1.17 麥初遇（Beat 1）——即派分開已落地，只改好感數字

`first:mak_zhendong` 三行已係三張唔同動作替身（v229／v255 落地），只改好感：

| 揀 | 即派（已落地，唔郁） | 好感 |
|---|---|---|
| 放低支水喺佢身邊就走（key「放低」） | `gig_1990_film_211` 高空吊威也動作替身（電影／初級／1990 春，cast leadM 麥震東） | +3 → **+2** |
| 堅持遞到佢手（key「堅持」） | `gig_1990_film_213`《飛車場面》動作替身（電影／初級／1990 夏） | +1 不變 |
| 開口問佢傷勢（fallback） | `gig_1990_film_214`《街市追逐》動作替身（電影／初級／1990 夏） | +1 不變 |

## §2 陸柏言「頂一晚」——重新設計（舊機制已死，唔靠傳聞／唔靠已刪通告）

### 點解要重新設計

舊 work158 設計全部錨點都係 `gig_intel_lu_standin`（v252 新庫刪咗，live 0 命中）＋傳聞 `enc79HasMerged("rumor_lu_baiyan_breakdown")`（傳聞系統 v267 成個刪）。兩樣都死咗，舊機制無論點都接唔返。新機制改用新庫真實通告＋現成 GRANT229 即派＋殺青 wrap hook＋每日 tick，唔開新通告、唔復活傳聞。

### 揀咗邊張通告做替工，點解

**`gig_1991_tv_203`《星夜迷離》臨時替工**（電視劇／初級／1991 冬／1 日／替身；cast leadM 陸柏言、leadF 鍾楚凝）。理由：

1. 通告本身 blurb／synopsis 明寫「陸柏言親自點名要你做臨時替工」「陸柏言與你的交情足夠，才有這一日臨時替工」——即係話，佢本身就係「陸柏言點名要你頂」嘅替工，唔使改通告文案都夾。
2. 時點夾：`luk_tease` 限 1991 年播出，替工係 1991 冬——tease 播完嗰季就係替工嗰季，時序順。
3. 佢已有 rel 觸發（`trigger: {kind:"rel", npcId:"luk_baakyin", relMin:25}`，v267 歸宿）：兩條路（rel 夠 25／陸線 tease 即派）指向同一張通告，完成佢就立 `luk_cover_night`，唔理邊條路拎到。
4. 排除過嘅候選：`gig_1990_tv_102`《街頭快跑》（leadM 係麥震東，陸只係 supportM，唔係陸點名）；`gig_1991_tv_201`《碼頭茶餐廳》夜更侍應（有 `storyKeys: ["N7"]`，同主線 N7 糾纏）；`gig_1990_tv_105`《夜半來客》武師（角色係武師唔係替身）。

### 成條鏈（時序）

```
1990        luk_foreshadow（tier 1 嗰陣撞到陸發脾氣）
              ├─ 守口如瓶 → luk_kept_secret（fav +2）
              └─ 同人講兩句 → luk_loose_talk（fav −2）
              （舊 v158 草稿原文；live 寫法修正「邊個都唔敢埋身」）
              另：初遇 first 抉擇落 luk_first_quiet／luk_first_pushy
                  （「雙手遞返，唔多口」／「趁機介紹自己」；第三選無旗）
tier≥2      luk_intel（v267 已處理：live 已無傳聞閘，只讀 tier≥2）
1991        luk_tease（新 registry beat；tier≥2＋1991 年＋未 cover＋未 absent）
              → 播出嗰晚經 grant229Record 記低 gig_1991_tv_203
              → 第二朝何生電話派（grant229DeliverOne 直接獲聘，唔受通告季節閘限制）
1991 冬     完成替工（殺青 wrap hook：done_gig_1991_tv_203 → 立 luk_cover_night，
              清 luk_absent_night；遲做都補救）
              28 日內唔接／唔做 → 每日 tick enc271LukAbsentTick 立 luk_absent_night
              （已 cover／已 done_／已 fail_shoot／shoots 排緊 → 唔立）
頂過嗰晚    luk_thanks（新 registry beat；閘 luk_cover_night——頂過先有句唔該）
1992 冬     luk_finale 冷暖分流：
              冷版 luk_finale_cold（T4＋absent／loose，排暖版之前；無 credit）
              暖版 luk_finale 加排除式閘 !(luk_absent_night || luk_loose_talk)
T4          luk_patron 冷暖分流：冷版 luk_patron_cold push 排暖版之前（無 credit）；
              暖版 luk_patron 加排除式閘
T3          heart 加閘：T3＋luk_kept_secret 先有交心（守口先開；講兩句 → heart 唔開）
              heart「靜靜聽落去」落 luk_confidant
luk_foreshadow 變體：按 luk_first_quiet／luk_first_pushy 喺開頭 prepend 一句
              （enc79BuildScript 第 2 位插句，唔 inline 改原文）
```

### 舊組件移植對照

| 舊 work158 組件 | 新機制 |
|---|---|
| 殺青 wrap hook（完成 `gig_intel_lu_standin` → `luk_cover_night`） | 同一位置（`resolvePlannedDay`，`done_` 寫入點之後），監察 `gig_1991_tv_203`；**一行寫法**（awei195 S4 釘住 done_ 行之後 3 行內要有 `enc195RecordTierMax`，兩行寫法會頂走佢——見 §5） |
| `luk_foreshadow` 守口／講兩句 → `luk_kept_secret`／`luk_loose_talk`（fav +2／−2） | 照搬，經 `enc79ChoiceFx` 新分支 `beat:luk_foreshadow` |
| `luk_thanks` 加閘 `luk_cover_night` | 新 registry beat `{ id:"luk_thanks", when: tier>=2 && luk_cover_night }`（舊 `luk_thanks`／`luk_tease` 係孤兒 DLG，live 從來唔播——呢批正式接入 registry） |
| `luk_finale`／`luk_patron` 冷暖分流 | 冷版 DLG（v158 草稿原文）＋暖版排除式閘＋冷版排暖版之前（v269 shadow 規則） |
| 28 日唔接偵測 tick（`enc158LukAbsentTick` 模式） | `enc271LukAbsentTick()`，監察 `gig_1991_tv_203`；每日 `advanceDay` 呼叫（`enc83GuLoanTick()` 之後） |
| heart 加閘（T3＋`luk_kept_secret`） | 照搬 |
| `luk_first_quiet`／`luk_first_pushy`／`luk_confidant` 初遇旗 | 照搬，經 DLG flags 欄位 |
| `luk_intel` 傳聞閘 | **唔使改**——v267 已處理，live 只讀 tier≥2 |

## §3 唔做／留下一批

- **顧 Beat 2 抉擇本身**（`gu_promise_clean`／`gu_ask_back`）：遊戲入面冇呢個抉擇，DRAFT 表已分開兩張（見 §1 1.14）；抉擇實裝要另設計，留下一批。
- **1.16 攻略側句子**：後果段＋後果表行加「即派分開」一句，留 parent（攻略側）。
- **陸 heart 錯過 foreshadow 邊緣情況**：`luk_foreshadow` 只喺 tier 1 播出；如果玩家 1990 年錯過（tier 升穿 1 先撞到陸），永遠攞唔到 `luk_kept_secret` → 陸 heart 永遠唔開。v158 原設計一樣係咁，留跟進票決定係咪放寬（例如 tier 2 都畀一次守口機會）。
- **新發現未修（唔喺 1.10–1.17 範圍，唔好喺呢票順手改）**：`heart:gu_mingfai` fx 關鍵字 `天光` 對唔上 live label「陪他坐到天亮，不出聲」（語言重寫改咗 label，fx 關鍵字漏改；live 揀呢個選項得 fav +1 唔係 +3；`tests/test_enc83_logic.js` 入面嗰個斷言用嘅係舊廣東話 label「陪佢坐到天光，唔出聲」，同 live DLG 已經唔一致）。留下一批／統籌決定。
- **其餘六條線**（駱／魏／齊／彭／鍾／程）：code 側按 PLAN §4–§9 逐線核實；即派第一批 25 項（PLAN §10）新通告／新兌現渠道跟通告重寫新庫一併做。
- **實機驗證押後**：Playwright 實駕未做；logic test 已覆蓋閘＋變體＋flags（見 §4）。

## §4 測試

- 新測試 `tests/test_sideline271_logic.js`：**71／71 ALL PASS**（§1 靜態對位＋旗＋閘、§2 fx、§3 節拍閘、§4 absent tick、§5 變體＋pushSeg flags；用 v269 harness 模式，sandbox 另加 `ENC79_DLG_luk_baakyin`、stub `grant229Record`（照 live 語義：dueDay+1、一生一次）、`enc271LukAbsentTick`；對位檢查直接 require `content/gigs_new.json`）。
- 相關舊測試逐個直接跑全部 ALL PASS：`test_sideline269_logic.js`、`test_enc79_logic.js`、`test_enc83_logic.js`（81 項）、`test_enc84_logic.js`、`test_br89_logic.js`、`test_gig229_grant.js`。
- 主 script 語法：第二塊 script（3,720,108 bytes）抽出 `node --check` 通過（SYNTAX_OK）。
- 全套第一輪（`qa271/suite_work.txt`）：**TOTAL PASS 328 FAIL 16**——9 項基線 FAIL 全部在列；新 FAIL 7 項（awei195／gift185／rom159／rom176／tang171／tang173／travel114），全部係釘行漂移（見 §5）。
- 全套第二輪（`qa271/suite_work2.txt`，resync 後）：**TOTAL PASS 335 FAIL 9**——FAIL 名單同 v269 基線逐項相同（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），0 新 FAIL。

## §5 Resync（`qa271/resync271.py`）

- index.html 淨 +91 行（45380→45471）；全部改動喺舊 L19690–39960 之間。
- **awei195 S4 唔係純漂移**：wrap hook 最初插咗 2 行喺 `done_` 寫入點同 `enc195RecordTierMax` 之間，頂出咗測試釘住嘅 3 行窗。修法：hook 改一行寫法（註解做同一行嘅尾註），record call 仲喺 3 行內；production 行為不變。修完 awei195 直接跑 ALL PASS，唔使改測試。
- 其餘 6 項純漂移，difflib 對位核實內容逐字相同先改期望值（`qa271/resync271.py`，單次掃描 dict 查表；重疊 pair 分開兩輪）：
  - travel114：openLoc( 序列 58 處逐字一致；COUNT 12 處、FREE 40 處、DEF 40622→40713、WRAPPER 28567→28570。
  - rom176：4 釘行 39005→39079、39363→39437、40507→40598、40663→40754。
  - rom159：4 釘行 25195→25198、26029→26032、25944→25947、全佳註解行 25223→25226（「全佳」全檔只出現 1 次不變）。
  - gift185／tang171／tang173：總行數 45380→45471（鏈尾加 ＋v271 +91）；openLoc DEF 40622→40713。
  - rom159／rom176 ok() 名內歷史行號係標籤，唔郁。

## §6 合併前要做（統籌）

- **Rebase**：v270 喺我做緊期間落咗地（main `e1bf9cc` → `e742377`）。呢支分支要喺新 main 上 rebase＋重新核實行號漂移。預期影響好細：v270 係刪檔尾第一個 `</html>` 之後重複嘅 8 行（檔尾，喺全部釘行之後），理論上只影響總行數（45471→45463）同 gift185／tang171／tang173 嘅總行數鏈（＋v270 −8）；其餘釘行唔郁——但一定要喺新 main 上重跑 difflib 核實，唔好憑理論估。
- 合併＋推 main＋Pages 核實＋刪工作副本由統籌做（我唔合併／唔 push main）。

## §7 統籌 rebase 記錄（2026-11-17）

- Rebase 上新 main `8d7cf8a`（v270 落地後：`e742377`＋NOTES commit `8d7cf8a`，suite 335／9）。Rebase 乾淨，唯三檔總行數鏈衝突（gift185／tang171／tang173）：v270 −8（檔尾）＋v271 +91，合併後總行數 **45463**（鏈 `…＋v269 +73＋v270 −8＋v271 +91`）；tang171／tang173 嘅 openLoc DEF 行維持 **40713**（v270 刪行喺 DEF 之後，唔影響 DEF；resolver 最初誤將 `＋v270 −8` 寫入 DEF 鏈，統籌已修正返）。
- Rebase 後全套重跑（`qa271/suite_rebased.txt`）：**TOTAL PASS 336 FAIL 9**——即新 main 335／9＋新測試 1，FAIL 名單同 v270 基線逐項相同，零回歸。新測試 71／71、相關舊測試逐個直接跑全部 PASS（travel114 印 `RESULT PASS`，唔係 `ALL PASS`，唔係 fail）。
- 合併：squash merge v271 → main，Pages 核實後刪工作副本。
