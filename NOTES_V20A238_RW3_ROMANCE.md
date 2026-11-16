# v20a238: RW-3 感情線逐句重寫（R_lan／R_xu／R_hiu／R_choi）

- 範圍：`content/story_detail_romance_lan_xu.json`（lan 5＋xu 5 節點）＋`content/story_detail_romance_vera_hiu_choi.json`（hiu 5＋choi 5 節點）；R_tang_meet_stub、R_vera_* 唔郁。
- 改寫 **134 處字串**（synopsis 19、beats 57、notes 37、label 8、WF2 choiceText notes 4、setting 6、title 2、speaker 1）；全部對白行 KEEP（WF2 對白本身已係輕口語）。生效版句數 339 → 402。
- 同步：JSON 20 節點 synopsis＋beats 同步做 WF2 措辭；JSON lan 5 節點 title／setting／choices 同步做 LAN 值；LAN synopsis 5 處同步做 WF2 措辭；JSON vs 生效版差異 220 處 → 0 處。
- 用字定稿：新句一律「裏／哪裏／著」；R_choi_crisis「周刊編輯」→「週刊編輯」（title／setting／speaker／cast；sprite map 保留兩個寫法）。
- TEXTFIX55：EXACT 169→165（刪 4）、NOTE_EXACT 26→9（刪 17）；另有 4 條先刪後還原（kwan151 B3/B5/N4＋tang152 釘死：EXACT「1991年冬…」＋NOTE_EXACT「可與事業結局並存。」＋choi 兩句）；載入模擬 diffs 51→15（剩低全部 Vera／Tang）。
- 測試：`test_wf2_81_logic.js` ALL PASS（`tests/fixtures/romance_wf2_v80.json` lanPa 4 個 label 更新做新寫法，斷言本身未郁）；全套 suite **314／10**，同基線一致，零回歸。
- 工作報告：`~/workspace/linji-language-sample/RW3B_WORKLOG.md`（716 行；改寫全表 134＋保留全表 189＋10 句試讀＋防逐詞換抽查＋TEXTFIX 逐組表）。
- 未做：Live drive 實機抽檢（留待統籌安排）；WF5 mock 層舊文唔郁；TEXTFIX57「點擊」→「撳」去留（RW-5）。
