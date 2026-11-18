# NOTES_V20A304 — Q17 駱／魏／齊冷版 heart 交心（獨立寫新對白）

基線 main `3758f9f`（v302）；分支 `v20a304`；index.html 47156 → 47194 行（淨 +38）。

## 1. 做咗咩

三條線各寫一段**獨立冷版交心**（`heartCold`，跟鍾楚凝 `heartCold` 前例），有壞旗嗰陣去到交心嗰刻播冷版，唔係淨係跳過暖版、由提攜冷版承接。

| 線 | 壞旗 | 冷版位置 |
|---|---|---|
| 駱家聲 `lok_gasing` | `lok_loose_row`（Beat 2a 講出去） | `ENC83_DLG_lok_gasing.heartCold`，新 L37316 |
| 魏詠男 `ngai_wingnaam` | `ngai_rain_hold_back`（Beat 3b 企埋一邊） | `ENC83_DLG_ngai_wingnaam.heartCold`，新 L36673 |
| 齊鎮海 `chai_zanhoi` | `chai_loose_fear`（Beat 2 講兩句） | `ENC83_DLG_chai_zanhoi.heartCold`，新 L37670 |

接駁：`enc79BuildScript` 加冷版分支（新 L40173–40177），**排暖版 heart 分支之前**；閘：`tier>=3 && !heartDone && D.heartCold && 對應壞旗`。暖版 heart 閘一行都唔郁（只改咗行尾註解：「冷版由 patron 冷版承接」→「冷版 heart 見上 v20a304，提攜冷版照舊由 patron 冷版承接」）。

## 2. 三段冷版交心對白全文（各 7 句；對白廣東話，旁白書面語）

### 駱家聲——守唔住秘密（唔會彈新歌）
草稿（PLAN §4 Beat 2a／batch2 L141、L241）：「佢照彈結他，但係彈畀自己聽，唔係彈畀你聽」；守口先肯彈半首新歌。

```
N  錄音室收工之後，駱家聲一個人坐在角落，抱著結他，彈了一小段，彈到一半就停下來，沒有望向阿偉。
S  你嚟喇。坐啦，不過今日唔好問我新歌嗰啲。
A  家聲哥，我……上次嗰件事，我唔係有心講出去㗎。
S  我知你唔係有心。有心冇心，講咗出去，就係講咗出去。
S  呢首新歌，我寫咗一半，剩低嗰一半，我諗住彈畀自己聽就算，唔彈畀人聽。
N  他又掃了兩下結他，聲音很輕，像是彈給自己聽的，阿偉坐在旁邊，聽得出那段旋律沒有彈完。
S  我唔係嬲你。我只係唔敢再將未寫完嘅歌，交畀第二個人聽。
```

### 魏詠男——暴雨嗰晚冇企埋去（信任唔同咗）
草稿（PLAN §5 Beat 3b／batch2 L669）：「佢照教你兩招，但唔會話『你嗰下似返我後生』」。

```
N  武館收工之後，魏詠男一個人留在那裡練棍，見到阿偉走進來，沒有停下，只是將支棍放慢了。
S  你嚟喇。企埋嚟，今日教你兩招，學唔學得識，睇你自己。
A  詠男姐，暴雨嗰晚，我……我應該衝出去頂住個燈架㗎。
S  應該嗰啲，過咗就係過咗。你嗰晚企埋一邊，我冇怪你，武指都冇怪你。
S  不過呢，阿偉，企得穩唔係企埋一邊，係企喺應該企嘅位。呢句，你嗰晚冇做到。
N  她將支棍舞了半套，收勢那下，落地屈膝卸力，站得紋風不動，然後將支棍交回架上，沒有再望阿偉一眼。
S  返去啦。幾時你企返去應該企嘅位，我哋先再講落去。
```

### 齊鎮海——漏咗佢驚嗰句（佢唔會講「冇同第二個人講過」）
草稿（PLAN §6 Beat 2／batch2 L984、L1043）：「佢照同你傾偈，但唔會講『我驚』嗰啲」；守口先肯講「今日呢啲說話，我冇同第二個人講過」。

```
N  星河電視台古裝街，齊鎮海一個人站在那道城門前面，對著劇本，見到阿偉走過來，合上劇本，點一下頭。
S  阿偉，嚟得啱，陪我行陣，聽日嗰場古裝戲，我想再默一次。
A  齊生，上次飯堂嗰啲嘢……我唔應該同人講兩句㗎，對唔住。
S  講咗就講咗，唔使道歉。飯堂人多口雜，邊句真邊句假，聽嘅人自己會分。
S  你問我驚唔驚後生追上嚟？我話你知，我唔驚。驚嗰啲，我唔會同人講，講咗都冇用。
N  他講完就合上劇本，回到監視器後面，腳步不快不慢，像是甚麼都沒有發生過一樣。
S  返去啦。聽日嗰場，你企穩，默熟，唔好諗其他嘢。
```

**唔抄暖版**：三段同暖版 heart 逐句零重用（測試逐句對位斷言）；暖版關鍵句全部避開——駱唔用「肯由頭聽到尾／想彈畀你聽下」、魏唔用「你嗰下似返我後生／留三分力／眼要先到」、齊唔用「你覺得我應該點行／一哥呢兩個字／冇同第二個人講過」。

## 3. 接駁決定（播完之後點行）

- **heartDone 照標**：冷版回調設 `heartDone = true`＋記旗（`lok_heart_cold`／`ngai_heart_cold`／`chai_heart_cold`）。理由：冷版就係嗰次交心，唔重播；測試證實再撞一次行 pool，唔會重播。
- **好感 ＋1，唔係暖版 ＋2**：有裂痕嘅交心，值同一次普通 pool 傾偈（＋1）一樣，唔值得暖版信任交心嗰個 ＋2。暖版對照測試：45→47；冷版：45→46。
- **唔派暖版收尾獎勵**：冷版回調**唔叫** `sideline280GrantCompletion`。雙重保障：①回調根本無呢個 call；②就算叫咗，predicate 都唔會過——駱要 `lok_calm_truth`（冷版無抉擇，設唔到）、魏要「唔係 `rain_hold_back`」（壞旗本身即唔啱）、齊要 `truth_change＋try_new`（`truth_change` 只由暖版 heart 抉擇落）。測試證實冷版播完 `sideline280_*` 未落、聲望／信用唔郁。
- **提攜（T4 patron_cold）照去得到，唔死局**：提攜閘只睇 tier＋壞旗，唔靠 `heartDone`（`enc79PickBeat` 只睇 `beatsDone`＋`when()`）。測試證實：播完冷版 heart 再升 T4，`lok／ngai／chai_patron_cold` 照播；冷版 heart 嗰次亦唔會順便播埋提攜冷版——兩個獨立 beat。
- **heart 抉擇即派（GRANT229_ENC79）冷版無、派唔到**：冷版 `heartCold` **無 `choices`**（跟鍾 `heartCold` 前例），所以無抉擇、無抉擇旗、唔經 `grant229RecordFromEnc79`；seg 係 `"heartCold:<starId>"`，GRANT229_ENC79 全部行都係 `"heart:<starId>"`，無對應行。測試直接 call `grant229RecordFromEnc79('heartCold:…')` 回 false、queue 唔郁。
- **唔郁清單**：暖版 heart 閘、暖版 heart 對白、三個 `patron_cold` 對白、鍾 `heartCold`（4 句）、`gigs_new.json`（302 張）全部唔郁；`enc79ChoiceFx` 唔使加冷版分支（無抉擇）。

## 4. 測試

- 新檔 `tests/test_r304_cold_heart.js`（ALL PASS）：(A) 形狀＋裂痕關鍵句＋零抄暖版＋旁白書面語；(B) 三線暖／冷對照；(C) 冷版 heart 同提攜冷版獨立＋播完升 T4 照去到；(D) 播完 heartDone／＋1／唔派收尾獎勵／唔重播＋暖版 ＋2 對照；(E) GRANT229 唔派；(F) 舊檔（得 fav／met、有壞旗）唔 crash 照播冷版；(S) 靜態 guard。
- 釘行漂移：`qa304/resync304.py`（difflib 對位＋單次掃描 dict 查表）。66 處錨點逐字核實純漂移；漂移帶：＜36673 ＋0、36673–37304 ＋11、37305–37647 ＋22、37648–40139 ＋33、≥40140 ＋38。改咗 5 檔：gift185（總行數）、tang171／tang173（總行數＋openLoc DEF 42365→42403＋guard）、rom176（4 釘 ＋38）、travel114（DEF 42365→42403＋COUNT 4 處＋FREE 24 處，各 ＋38；WRAPPER 29103 唔郁）。
- 全套 suite：`bash qa131/run_suite.sh` → **TOTAL PASS 367 FAIL 9**（`~/workspace/suite304.log`）。9 項 FAIL 全部係 pre-existing——已喺 pristine HEAD（`git checkout HEAD -- index.html`，47156 行）逐個覆驗一樣 FAIL：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38（softRev／文案舊問題）＋wf5_87（搵唔到另一個 worktree `linji-work86` 嘅檔，環境問題）。v302 基線 366／9；今次 367／9＝基線＋1 個新測試，零回歸。

## 5. 附帶發現（唔喺 Q17 範圍，留畀統籌）

- 工作副本入面 `qa296/derive296.json` 有未提交修改，唔係今次改動（今次 commit 唔包佢）。
- 舊版暖版 heart 註解話「冷版由 patron 冷版承接」已隨今次改咗註解；如有其他文件／攻略重複呢句舊講法，值得跟進同步（今次無改攻略）。
