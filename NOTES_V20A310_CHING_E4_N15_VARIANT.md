# NOTES_V20A310 — Q23 程天諾 ching_e4 N15 旗變體（抉擇後對白）

- 基線：main `36b42a9`（v309 已落地，suite 372／9）
- 落地：main HEAD（見回報）、suite 373／9、Pages byte-identical（見回報）
- 檔案：`index.html` ＋10 行（47275→47285）、新測試 `tests/test_r310_ching_e4_n15.js`（27 項）、
  resync `qa310/resync310.py`、5 檔靜態測試釘行 resync（見 §4）

## §1 設計（PLAN §9 Beat 3 逐字稿）

`ching_e4`（城中四子報紙 setup，開場 8 句）兩個選擇入面，淨係「撐佢練」嗰邊按 N15 旗分流。
變體係**抉擇後對白**——玩家揀完先出現，唔做開場插入（開場插入會令程喺玩家未開口之前就提 N15，
打斷報紙 setup；heart 開場插入係另一套前例，唔適用）。

| 玩家 N15 旗 | 揀「撐佢練」之後 |
|---|---|
| `flag_vocal_train`（苦練） | 信任句行先，再接原本「今晚唔停」：玩家原句 → S「你嗰晚都係咁揀，我信你。」→ S「好！咁我今晚唔停，唱嗰課練多一個鐘，你唔准走！」 |
| `flag_vocal_polish`（修音） | 頂返句取代原本應承：玩家原句 → S「你嗰晚都係靠部機交帶㗎，咁你而家係教我練，定教我執呀？」 |
| 無旗 | 原回應 2 句唔變 |
| 任何旗＋揀「紅咗先算」 | 原回應 2 句唔變（照 PLAN，淨係撐練嗰邊有變體） |

兩旗同在（正常玩法唔會，N15 係單選）以苦練為先。

## §2 實裝（`enc79BuildScript`，舊 L40244 前插 ＋10 行）

跟 v278／v305／v309 前例——分流喺 `enc79BuildScript` 讀旗嗰陣換句，唔郁 DLG 定義：

- `beat.id==="ching_e4"` 且 `enc87StoryFlag` 在位嗰陣，讀 `flag_vocal_train`／`flag_vocal_polish`
  （`enc87StoryFlag` 讀 `S.flags` 或 `S.story.flags`，兩種存檔寫法都啱）。
- 只重建 `beatSeg100.choices[0]`（`Object.assign` 拷貝，label／flags 照抄；`lines` 換成變體）；
  `choices[1]`（紅咗先算）原樣；`beatSeg100.lines`（開場 8 句）原樣。
- 守住：開場 8 句逐字唔郁；兩個選擇 label 同授旗（`ching_back_train`／`ching_back_polish`）唔郁；
  GRANT229（撐練→`gig_1992_rec_107`《霓虹舞影》MV 男主角；紅咗先算→`gig_1992_ad_105`）唔郁；
  fav（撐練＋5／紅咗先算＋1，`enc79ChoiceFx` 按 label 對位）唔郁；`ching_e4` 註冊閘
  （tier≥1＋`enc83NewsOut("E4")`）唔郁；`ching_after_train`／`ching_after_polish` 閘唔郁；
  舊檔唔 crash。變體唔寫入 DLG 定義——同一局重播、無旗回復原樣（測試 E 段覆蓋）。

## §3 測試（`tests/test_r310_ching_e4_n15.js`，27 項全 PASS）

- A：`ching_e4` 存在（開場 8 句＋2 choices）；開場逐字；label／授旗逐字。
- B：苦練旗→播 e4、開場照舊（無開場插入）、撐練 3 句（玩家原句＋信任句＋原本「今晚唔停」，
  信任句行先）、紅咗先算嗰邊原樣。
- C：修音旗→撐練 2 句（玩家原句＋頂返句）、原本「今晚唔停」唔再出現、紅咗先算嗰邊原樣。
- D：無旗→兩邊原回應、無信任句／頂返句。
- E：變體嗰陣授旗照舊；fav＋5／＋1；GRANT229 兩邊照派；播完 `beatsDone.ching_e4` 照標；
  變體唔寫入定義（苦練 build 後定義仍係 2 句，再 build 無旗回復原樣）。
- F：舊檔（其餘 beat 已做＋N15 旗，`S.flags`／`S.story.flags` 兩種寫法）唔 crash，照播變體。
- S：`ching_e4` 註冊閘／`after_train`／`after_polish` 閘唔郁；開場無變體句；
  `gigs_new.json` 仍係 306 張。

## §4 行數漂移 resync（`qa310/resync310.py`）

本票 index.html 淨 ＋10 行，插入點舊 L40244（`pushSeg(beatSeg100, "beat:"+beat.id` 之前）。
全套 suite 首次跑出 368／14——多出嘅 5 項 FAIL 全部係靜態測試釘行漂移（已逐項核實，
5 項喺 pristine main `36b42a9` 全部 PASS，確認係本票 ＋10 行引起，唔係功能回歸）：

- `test_gift185_static.py`：總行數鏈尾 ＋v310 +10（47275→47285）。
- `test_tang171_static.py`／`test_tang173_static.py`：總行數鏈尾 ＋v310 +10、DEF 行 42484→42494、
  guard 行同步 ＋10（`len(lines) >= 42500`／`lines[42493]`）。
- `test_rom176_static.py`：4 釘各 ＋10（40716→40726、41066→41076、42369→42379、42525→42535；
  ok() 名入面嘅 L 號係歷史標籤，唔郁）。
- `test_travel114_static.py`：DEF 42484→42494、COUNT 4 處＋FREE 24 處各 ＋10；WRAPPER 29103
  喺插入點之前唔郁；插入點之前嘅 COUNT／FREE 錨點（15363–28534／6525–28375）唔郁。

`qa310/resync310.py` 用 difflib 對位核實純漂移（插入區邊界舊 L40243→新 L40243、
舊 L40244→新 L40254；新插入行 L40244–40253 在位；全部錨點內容逐字相同），
再用單次掃描 dict 查表改 5 檔（v160／v162 教訓：唔逐對 re.sub、重疊對一次過換）。
執行中捉到一個 resync 腳本本身嘅轉義 bug：`\\\\n` 字面量喺寫入檔案嗰陣變咗 8 個反斜槓，
同測試檔入面 2 個反斜槓對唔上，令總行數鏈尾第二段替換靜默失效（已改用無反斜槓寫法，
直接換鏈尾＋`== 47275`→`== 47285`，三檔再補換後覆驗 PASS）。

## §5 全套 suite

- 首次跑：368／14（5 項漂移 FAIL，見 §4）。
- resync 後重跑：**373／9**——9 項 FAIL 全部係已知 pre-existing（flash51／slot50／
  soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），
  同 v309 基線 372／9 一致；373＝372＋1（新測試 `test_r310_ching_e4_n15.js`）。
- `qa296/derive296.json` 係 suite 再生嘅衍生盤點檔，commit 前已還原，唔入版。

## §6 殘留

無。Q23 結案；下一票 v311（Q24 程 patron 閘改嚴格版三旗齊備）。
