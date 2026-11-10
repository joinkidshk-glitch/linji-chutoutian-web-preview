# v20a87 — WF5 觸達審計收尾包（劇情豐富化最後一包）

基底 v20a86（5,196,226 bytes）。性質係「盤點＋修死嘢」，唔加新內容。
紀律：SAVE key／softRev／`?v=` 不變；pack JSON 冇直改（變體對齊行覆寫表，同 textfix55／WF2 先例，原生移植時一齊搬）。

## 1. 全內容觸達審計（可重跑：`tests/audit_wf5.js`，輸出留底 verify87/audit_before.txt／audit_after.txt）

方法：節點宇宙 94 個（5 pack JSON＋spine／COMMIT48／CHOICE47／WF1 常量表）做旗標 fixpoint 可達分析；code／gig 生產者旗標 55 個、gig 宇宙 375 個交叉核對；巧遇 62 節拍 gate↔對白段雙向核對；鏈 A–G 情報／拼合／使用點、報紙 7 則日子、日常事件池 36 個、隱藏通告 3 個逐項查生產者。

結論：94 節點全部可達、冇死節點；主線窗口全用 yearMin（逐年重現，遲玩唔鎖死）；其餘系統接線齊全。證實死內容 2 項＋潛在同病 1 項，全部已修（見下）。

### 證實死內容（已修）

1. **程天諾專屬節拍 ching_after_train／ching_after_polish 永不開啟**：節拍 gate 讀 `S.flags.flag_vocal_train/polish`，但唯一寫入路徑係 C16 抉擇經 StoryOC.applyChoice→setFlag 寫入 `S.story.flags`——兩個旗庫永不相遇。v84 測試當年用 fixture 直設 S.flags 所以冇捉到（同 verify37 盲點同類）。
   修法：新增 `enc87StoryFlag(k)`（先查 S.flags 再查 S.story.flags，同 endingFlag410 雙庫口徑一致），三個受影響節拍（埋 chai_repay，見下）改用佢。
2. **R_choi_push1 經主線 C5 嘅替代入口永不滿足**：openConditionsAny 要求 `flag_choi_honest/spin/dodge`，C5 抉擇實際寫裸名 `choi_*`；pack 嘅 `qa.flagAlias` 同節點註文明文聲稱「wiring 讀 alias」，但 StoryOC.getFlag 根本冇 alias 解析（全檔零命中）。節點本身經 R_choi_meet 旗可達，死嘅係呢個設計替代入口。
   修法：StoryOC.getFlag 加前綴 alias 後備（原 key 查唔到時試裸名↔`flag_` 前綴另一形，三個 store 都試）。
3. **chai_repay（潛在，同病預防）**：gate 直讀 S.flags.flag_side_*（C14 抉擇旗同樣只入 story.flags），原本靠 `enc83NodeDone("C14")` 後備路先冇死；一併改用 enc87StoryFlag 正接線，零行為改變。

### 低觸達但設計如此（冇郁，逐項）

- 程天諾 1992 先解鎖；ching_rival 要未做 C16；lok_e4grudge／ching_e4 要 E4 報紙（day 1015）後；mak_visit 限定病倒／康復期；so_risk／yip_rival 要玩家級數 ≤1；luk_finale／pang_n17／chai_choice／liu_clash 係 1992 冬窗；gu_tease（1991＋未做 C9）同 gu_n10after（C9 done）互補冇空窗。
- 芬姐相識場窗口約一季（1991 年內要去 tvb_harbour 相識；送別戲有中性變體＋舊檔補播兜底）。
- 報紙 E3 喺 day 1092（早觸結局閘就見唔到）；C18／C19 時窗可錯過（只影響進度頁顯示，唔卡主線）；commit 節點要 1992 秋＋rel≥6＋crisis done；霞姐三場要累計到訪＋1991 春後。
- **鏈 G／E5 門檻可達性未獲實證**（已知 open item，唔係死內容證據）——本包冇郁，留待專門驗證。

## 2. soft 變體文本對齊（WF2 遺留）

新增覆寫表 `WF5_VARIANT_OVERRIDES87`＋`applyVariantWf5Overrides87(...)`（refreshCopyPacksFromDisk 內、loadMock 之前套用），覆寫 **7 個節點**：鄧麗萍線 R_tang_meet／push1／push2／crisis／ending（DengLine 層）＋曉晴／采兒 R_hiu_meet／R_choi_meet（DualMeet 層）。只換 synopsis／beats lines／choice label／notes；安全機制：逐節點核對 beat 數＋speaker＋行數同原稿一致先套用，對唔上成節點跳過。
- 鄧麗萍 ending 同 WF2 定版逐字咬合（紅筆圈住／「呢格，我睇好你」／百分之七／五成九／HE・BE choice 原文），舊版「跨越商業界線，承諾共同面對未來」清除。
- 采兒 meet 對齊 WF2＋M33（《星訊週刊》正字、唔抄通稿、主編催獨家、唔害人條線），兼清走原稿簡體「周刊」殘留（title 改「週刊小訪」＋setting）。
- 硬約束冇掂（測試釘死）：beat 數／行數／speaker 次序、choice id／flags／stats、chromeSeason／playerMeta、openConditions 逐一不變；廣東話標記密度 1.8→48.9／千字。

## 3. 季節標籤債（v79 遺留，全清單修正）

- **LIVE 補季節（F3a）**：spPlayerMeta 舊 regex 只認「年份＋春／秋」中文字，eraTag 係英文編碼（winter／summer）嘅節點永遠得裸年份。改為由同一來源字串以 spSoftSeasonChar 補返季節。受影響：C7（1991夏）、C9／C10（1991冬）、C13（1992冬）、C14（1992夏）、C18（1990冬）等；C6（冇季節）保持「主線 · 1990」；C1 批准標籤「主線 · 1990春」不變。
- **soft 年份（F3b）**：spPlayerMeta_softSeasonFrom 一律用死 START.y=1990 撘當前季節——改為年份跟節點 when 自帶年份。修正：C9（差一年）、C12–C17（差兩年）、C15／C19 等；seed／calendar／chrome 優先分支冇郁。
- **forced 短路（F3d，實駕新發現）**：spPlayerMeta 原本連 `spIsForcedStory`（`_sess.forced`）一齊短路做開局標籤——但 force 播係進度頁「播呢幕」嘅正規玩家路徑，任何節點經 force 開播都會標成「主線 · 1990春」（實駕 C9 內容係 1991 冬、頂欄標 1990 春）。標籤短路只保留 C1 本人；spIsForcedStory 本身（forced 鎖定行為）冇郁，gate 冇郁。
- selfCheck 期望 p3when 一項原位改版（相對期望→寫死 1988 字串，配合 F3b 新口徑）；其餘 4 項 fails（dualSeedChrome／dualNoSeed／choiSpringCal／choiAutumnCal）係 1988 stub 世界嘅既有 stale 文字期望，修前修後同樣在列，非本包引入，冇郁。

## 4. verify37 fixture 細債

`tests/test_verify37_logic.js` fixture 用錯 routes key（`{tv:true}`，真 key 係 `route_tv`，由 pack C1_a 抉擇寫入）。
結論：**對遊戲本體零影響，純測試盲點**——嗰場景 dayIndex 66＝第 10 週 < C6 閘 weekMin 15，route 有冇都出同一句「未開」，所以一直冇被發現。已修 fixture 並註明成因；C6 閘嘅正反驗證由 WF5 邏輯測試補齊（閘表＋C1_a 生產者＋routeHeld 全名查 st.routes）。
另：`tests/test_enc83_logic.js` 因 chai_repay 改用 enc87StoryFlag，抽取清單按既有 pattern 加入該函數，並加一條 story.flags 側斷言。

## 驗證

- 邏輯測試 `tests/test_wf5_87_logic.js`：work87 **59/59 PASS**；對 v86 index 行（WF5_INDEX 對照）**FAIL 18**，精準落喺 F1 alias、F2 helper、F3／F3d 標籤、變體覆寫四組——反證成立。
- 靜態測試 `tests/test_wf5_87_static.py`：PASS（SAVE／softRev／`?v=` 標記不變；8 份 pack JSON sha256 同 v86 出貨副本逐一相同，冇直改 pack）。
- 全套件 A/B：work86 基線 91 PASS／12 FAIL → work87 **93 PASS／12 FAIL**，12 個 FAIL 檔同基線逐檔一致（環境性），零回歸。
- 真 UI 實駕（verify87/drive.py，本地鏡像＋隔離 profile，v87／v86 雙跑）：**v87 21/21 PASS、pageerror 0**；v86 對照精準 9 FAIL（采兒 meet M33 口徑、鄧 meet 新文本、鄧 ending 紅圈場＋改口句、F1 getFlag alias、F2 after_train 真播、F3 函數標籤×2、F3 C9 播放頂欄標籤）。證據：verify87/evidence.json＋截圖（v87_soft_choi_meet／v87_soft_tang_meet／v87_soft_tang_ending／v87_live_c9_label／v87_live_ching_encounter）。
  - F2 實證方式：真 UI 巧遇——1992 秋冬逐日入天星音樂（rec_star），巧遇 overlay 真播程天諾 after_train 段（「半夜練唱」）；v86 同條件巧遇有觸發但 after_train 永不出現。
  - 駕駛注記：巧遇用自家 #enc79-overlay（唔係 StoryPlay）；abort 過嘅主線會變待播喺下次入地點重播（設計如此，唔係 bug）。

## 出貨

git 直推：分支 v20a87-wf5 → squash 合併 main。index.html 5,213,044 bytes（+16,818 vs v86）。
