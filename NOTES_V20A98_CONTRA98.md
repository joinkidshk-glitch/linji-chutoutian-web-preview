# v20a98 CONTRA98 — 劇情矛盾全面檢查＋硬矛盾修復

用戶收尾清單第一條線。三路系統性審計（時間線／人物狀態＋因果／地點＋數字稱謂＋禁用詞），
共 34 項：硬矛盾 9（本包全修）、輕微唔順 14、存疑待判 11（冇擅改，綜合報告
`~/workspace/linji-contradiction-audit.md` 交用戶判斷；分部報告 linji-contra-parts/）。
判定口徑：玩家實際見到嘅有效文本（pack × 覆寫／清洗／年份推移合併後）。
全部改動喺 index.html（覆寫／正規化／顯示層／對白底稿），冇直改 content pack JSON；
冇改 SAVE key／softRev／?v=。

## 硬矛盾修復（9 項）

- **A-01/A-02 支線節點頁首年份超出日曆**：支線 P5 結局節點（12 個）經 years66 全域 +2 後
  頁首標「1994」、P4 節點（11 個）標「1993」，但兩批戲實際只喺 1992 年內播（P5＝1992 年
  12 月、C17 後劇情封鎖）。新增載入正規化 `contra98FixNodeWhen`＋`CONTRA98_WHEN_FIX` 表，
  喺 years66Walk 之前行（跟藍 PA 覆寫先例用舊曆值）：P5 一律「1990冬／era_1990_winter_finale」，
  P4 按內容季節（賀歲片開鏡／冬日八卦＝冬，其餘秋；eraTag 保留 promo/anni/gossip/capital 後綴）
  → 有效顯示「1992冬／1992秋」。
- **A-03 C1 頁首「1990春」**：`spPlayerMeta` 硬編碼同開局曆法打架（START=1990-01-01・冬、
  開始按鈕寫「1990 年冬」、JAN67 已改 C1 when 做冬，唯獨呢行漏改）→ 改「冬」。
  連帶更新 test_wf5_87_logic 兩條舊期望（F3／F3d）——標籤格式不變、季節跟返曆法，註明理由。
- **B-01 commit 互斥缺口**：COMMIT48 互斥只守 CMT offer；pack R_hiu_ending／R_choi_ending
  嘅 HE choice 照寫 commit 旗、冇查對方旗，同一局可同兩人「講明」。StoryPlay.start 加
  預備鉤 `contra98PrepareNode`（跟 wf3PrepareNode82 先例，淺拷貝唔改 pack）：對方 commit
  已立而自己未立時，HE choice 換「坦白心意」差一步變體（只寫自己線 BE 旗，notes 明寫差一步）。
- **B-02 Vera 危機幕打歌前提**：WF2 R_vera_crisis 覆寫用新字串重寫「去電台打歌」前提，
  TEXTFIX55 exact-key 洗唔走 → synopsis／首句改返電視台錄影版（對齊 TEXTFIX55 既定目標措辭）。
- **C-01 C4 地點三方打架**：pack locId＋beats 係事務所，但 `STORY_LOC_SOFT.C4` 寫 ad_central，
  CALIB60 時窗提示會錯掛中環廣告 → 改 agency_ho；STORY_HINT_SOFT C3 nextHint／C4 lockedHint
  兩句「中環廣告」改返事務所。
- **C-02 巧遇初遇劇本副場穿幫（系統性）**：`enc79BuildScript` 加 locId 參數（caller 傳入），
  新增 `ENC79_FIRST_ALT98`——11 星副場版場景句精確替換（葉敏芝係反向：主場 rec_hk 先係錯位，
  alt 喺主場套用）；STAR_SIGHTINGS 葉敏芝行 distanceLook／locHint 由「訓練班」改「唱片公司舞蹈房」。
- **C-03 麥震東初遇地點**：底稿「清水灣片場邊」主副場都唔啱 → 改「紅棉影業片場邊」（主場），
  副場獅子山版入 ALT 表。
- **C-04 通告自稱星河但掛海港廣播**：《渡輪燈火》《商場歲月》TEXTFIX55_GIG_EXACT 兩條
  synopsis 修正值「星河電視台長篇」→「海港廣播長篇」；blurb 模板加一條 EXACT 修正
  （已查證呢句 blurb 全部 4 次出現 loc 都係 tvb_harbour）。

## 測試

- 新增 `tests/test_contra98_logic.js`（真函數抽取：23 節點 fix+walk+spPlayerMeta 全鏈、
  四 pack 全域年份 ≤1992 守門、commit 鉤四態、ALT 表 12 星替換）＋`tests/test_contra98_static.py`；
  兩者對 v97 index 行均 FAIL（反證）。
- 全套 A/B（逐檔 exit）：基線 v97 89 PASS／37 FAIL（環境性、逐檔已知）→ v98 91 PASS／37 FAIL，
  FAIL 集逐檔一致，唯一差異係兩個新測試 PASS——零回歸。
- 實駕（Playwright 本地鏡像）22/22 PASS：真開播 C1 頁首「主線 · 1990冬」、R_xu_ending 頁首
  「主線 · 1992冬」；spPlayerMeta 對真載入節點（R_vera_crisis 1992秋、A_ko_ending 1992冬、
  R_tang_crisis 1992秋）；B-01 真節點＋真旗標四態；C-02 六個副場／主場初遇旁白對位。

## 冇改（交用戶判斷）

輕微 14＋存疑 11 項全列喺綜合審計報告：包括兩位「芬姐」係咪同一人（B-10）、鍾楚凝 farewell
後冇離場旗（B-05）、E5/GH 結局回望引用冇系統出處嘅經歷（B-07/B-09）、「偉翔」稱呼分界
（B-12/C-05）、NEWS82 挖角則同 C14 嘅關係（A-09）、C18/C19 章戳同季節閘唔對齊（A-12）等。
