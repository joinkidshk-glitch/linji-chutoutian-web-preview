# NOTES_V20A300_PANG_STAGE_HALF.md — Q13：彭少祺人情渠道司儀通告台風要求減半

## 任務
Q13：用彭少祺人情渠道（慈善騷頂班）入場嗰陣，5 張司儀通告嘅台風要求減半。
基線 main `e588b05`（v299，suite 363／9）。工作副本 `~/workspace/linji-work300`，分支 `v20a300`。

## 減半計法（拍板寫低）
**`Math.ceil`（向上取整）**。對照表：

| 通告 | 原台風要求 | 減半後 | charm 要求（唔郁） | 級別／聲望 floor |
|---|---|---|---|---|
| gig_1990_variety_101《今夜歡笑》 | 15 | **8** | 12 | 初級／0 |
| gig_1990_variety_105《歡笑滿堂》 | 25 | **13** | 20 | 初級／0 |
| gig_1991_variety_104《歡樂大綜藝》 | 30 | **15** | 25 | 初級／0 |
| gig_1991_variety_103《樂善之夜》 | 45 | **23** | 30 | 中級／16 |
| gig_1992_variety_102《銀禧同歡夜》 | 80 | **40** | 55 | 稀有／32 |

邊界說明：開局台風 14。15→8（唔係 7）之後，開局過到最低嗰張《今夜歡笑》（charm 12／floor 0 都過到），其餘四張仍要練台風。揀 ceil 係刻意：減半係放寬，唔係送——15→7 會令開局台風 14 過到之餘仲有 7 點水位，太鬆；ceil 保留「要啱啱好先過到」嘅門檻感。

## 核心設計發現（改動前核實）
渠道原本只喺 `canAudition(gig).ok` 嗰陣先提供——即玩家本身要過齊**全數**台風要求，減半先有意義。所以放寬必須喺**渠道資格判定嗰層**用減半後嘅要求計，唔係淨係改提示字。

## 改動（index.html 淨 +44 行，總行數 47093→47137）
兩處插入：
1. 詳情頁 `openCastingNoticeDetail` 鎖定分支 ＋7（舊 L18723 後）：`ch158Locked` 金色提示＋「用人情免試鏡」掣（正常試鏡掣照樣鎖住；下面「差幾多達標」係正常路線嘅數，唔郁）。
2. v20a158 區 ＋37（舊 L45245 後）：新 helper 三個＋`favor158ChannelForGig` 重寫＋頭註解更新。
   - `pangHalvedStageReq158(stage)`：`Math.ceil(stage / 2)`。
   - `pangEffectiveGig158(gig)`：只改 stage 一項嘅 copy，原 gig 唔郁（庫 req 唔郁）。
   - `pangChannelReady158(gig)`：啱類別（`isPangCharityGig158`：type 綜藝＋roleLabel 含「主持」）＋持有彭債權＋用減半台風計嘅 `canAudition` 過關。
   - `favor158ChannelForGig`：武指分支維持原狀（全數 `canAudition` 先提供）；彭分支改用 `pangChannelReady158`；提示寫明減半前後數字（例：「人情可用：慈善騷頂班——彭少祺開聲引薦，台風要求 15→8，此司儀通告無須試鏡，直接獲聘。」）。
   - v20a158 頭註解：「台風放寬」未定 → 已定（v20a300 Q13）。
   - `promptAudition` 係死 code（全 repo 淨定義＋註解引用，冇 live caller），唔郁。`doAudition`／`canAudition` 本身唔郁。

## 唔郁嘅嘢
- charm 要求、聲望 floor、其他硬閘照舊；通告庫 req 唔郁（放寬只適用經彭渠道入場嗰陣）。
- F1／其他 158 渠道（武指照應）唔郁。
- SAVE key／softRev／產品 `?v=` 唔郁。

## 測試
- 新 `tests/test_r300_pang_stage_half.js` **37 項，ALL PASS**：減半表（15→8／25→13／30→15／45→23／80→40）、effective gig 不變性（原 gig stage／charm／其他 req 唔郁）、開局邊界（台風 14 過 101、`canAudition` 全數唔過 101）、7 唔過／8 過、charm 閘（charm 唔夠照擋）、聲望 floor 閘、五張掃描（全部係 `isPangCharityGig158`、減半表齊全）、武指唔郁、非主持唔入（綜藝非主持／非綜藝主持都唔入）、詳情頁鎖定分支靜態斷言（金色提示＋免試鏡掣＋正常試鏡掣照鎖）。
- 舊 `test_sideline158_logic.js` ALL PASS（補抽三個新 helper＋T2 註解更新）。
- `test_sideline273_logic.js` 曾經新 FAIL（(d) G-PANG-1）：佢抽 `favor158ChannelForGig` 但冇抽三個新 helper，`typeof` 守衛令渠道靜靜回 null（唔係真回歸）。修法：將三個 helper 加入抽取清單。同樣補咗 `test_sideline278_logic.js`、`test_sideline280_logic.js` 兩檔抽取清單（佢哋今次冇爆，但抽出嚟嘅函數已經係殘缺版）。三檔重跑全部 ALL PASS。
- 釘行 resync（`qa300/resync300.py`）：6 檔靜態測試——gift185（總行數鏈尾 ＋v300 +44）、tang171／tang173（總鏈 ＋44；openLoc DEF 鏈 ＋7：DEF 42339→42346，guard 42345→42352，index 42338→42345）、rom159（3 釘＋全佳行各 ＋7：25459→25466／26307→26314／26208→26215／25487→25494）、rom176（4 釘各 ＋7：40574→40581／40924→40931／42224→42231／42380→42387）、travel114（DEF 42339→42346、WRAPPER 29096→29103、COUNT 12 處、FREE 40 處；FREE 45500 嗰對重疊 45456→45500／45500→45544 用單次掃描 dict 查表一次過換）。全部錨點先對 pristine main 用 difflib 對位核實內容逐字相同（純漂移），再改。6 檔重跑全部 PASS（gift185 ALL PASS／tang171 22 PASS／tang173 22 PASS／rom159 156 checks 0 FAIL／rom176 ALL PASS／travel114 RESULT PASS；分類：免費 40＋計數 12＋back176 2＋定義／wrapper／測試區 4）。
- 全套 suite：見下面。

## Suite
全套 `bash qa131/run_suite.sh`（outfile `~/workspace/suite_v300_final.txt`）：**TOTAL PASS 364 FAIL 9**。
364＝v299 基線 363＋新檔 `test_r300_pang_stage_half.js` 1 檔。9 項 FAIL 全部係已知 pre-existing，同 v299 基線一字不差：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38。零新增回歸。

## 落地
（待填：main HEAD、Pages md5／bytes。）
