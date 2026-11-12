# NOTES_V20A121 — 導演欄職銜關鍵字規則，取代 v117 窮舉 Set

- 分支：`v121-director-keywords`（基底 main `215b97e`＝v118；合併嗰陣 main 未郁，無 rebase）。
- 性質：純判定層。S-30 卡渲染路徑／版式／文字零改動；唔改 content pack JSON；唔郁 SAVE key／softRev／產品 `?v=`。
- 用戶拍板：唔使（執行票；設計抉擇——關鍵字清單——由執行員對住實池逐個驗定）。

## 改咗咩

### index.html（＋39／−9 行，淨 +30 行，對 main `215b97e`）
- `GIG_DIRECTOR_GENERIC117` 窮舉 Set 成個刪走，換成 `GIG_DIRECTOR_ROLE_KEYWORDS121`（25 個職銜關鍵字）＋`gigDirectorIsRoleValue121(s)`（子串命中即當職銜）。`gigDirectorRealName117(g)` 名同簽名不變，改讀新判定；`gigDirectorLabel` fallback「組製未公開」不變；`castingNoticeDetailHtml` 嘅 `directorRow117` 接線不變。
- 關鍵字清單（按工種分組，註解列明）：
  - 導演組：副導／助導／導演
  - 製作組：監製／製片／製作／組製／統籌
  - 現場組：場務／場記／武指／武術／指導
  - 技術組：攝影／燈光／收音／剪接／後期
  - 文宣組：編劇／宣傳／客戶
  - 雜項／佔位符：助理／幕後／未公開／待定
- 揀字理據（寫埋喺註解）：(1) 實池 16 個職銜值全部命中；(2) 其餘 9 個係同系合理延伸，其中「幕後／後期／製作／編劇／剪接／場記／副導／統籌」係遊戲自身幕後工種詞彙（見 `ENDING410_BACKSTAGE_KEYS`）；(3) 「未公開／待定」擋佔位符（fallback「組製未公開」同將來「導演待定」之類）。全部關鍵字 2–3 字，唔留單字通配。
- 註解同步更正咗另一處舊字：`castingNoticeDetailHtml` 頂註「濾走 8 個職銜值＋fallback」→「v121 關鍵字規則，實池 16 個值＋fallback」。

### 點解要換：v117 普查數字錯咗（實駕重驗發現）
- v117 話 live pool 183 張＝152 真名＋31 職銜值。重驗（Playwright 實駕 dump `window.GIGS`，`?softPreview=1` 新遊戲槽 3，`qa121/census_main.json`）話：**183 張＝137 真名（113 個名）＋46 職銜值（16 個值）**，0 張缺 director。
- 舊窮舉漏網嘅 15 張（舊規則下會照出導演行）：「監製」×7（`gig_1988_nat92_*` 7 張）、「導演」×2（`gig_1988_nat92_lion_sum_high`《烈日狂徒》男主角、`gig_1988_nat92_harbour_sum_high`《夜雨殺機》大反派——兩張都係高位階主角卡）、「監製助理」×1（冬季入門 `gig_1988_entry_winter_rec_chorus`）、「武指領班」×1（`gig_1988_mid35_lion_chase`）、「武術指導」×1、「客戶代表」×1、「副導阿成」×1、「宣傳部阿玲」×1（後四者皆 `gig_1988_nat92_*`）。即係話舊規則唔只將來會漏，**現行池已經漏緊 15 張**，其中兩張係主角級通告。
- 副導 ×19 嚟源：soft bridge 11＋冬季橋 6＋冬季入門戲院 1＋nat92 1。

## 183 張驗證結果（實池逐項對照，見 `tests/test_director121_logic.js` 內嵌表＋`qa121/census_main.json`）
- 16 個職銜 distinct 值（46 張）新規則全部擋到：副導 ×19、監製 ×7、副導阿標 ×4、廣告助導 ×3、導演 ×2、特輯副導／場務阿強／外景場記／平面攝影師阿忠／錄音室助導／監製助理／武指領班／武術指導／客戶代表／副導阿成／宣傳部阿玲 各 ×1；fallback「組製未公開」擋到；空值／缺 director 唔出。
- 113 個真名（137 張）**零誤殺**：逐個關鍵字做子串碰撞檢查，25 個關鍵字對 113 真名全部 0 碰撞（特別留意：「導」「監」「製」呢類字唔喺任何真名入面；「何志光」含「光」但唔含「燈光」，子串檢查分得清）。
- 假想將來新值 **29/29 擋到**（任務要求 ≥5）：執行導演、副導阿強、監製阿文、外景副導、攝影阿明、導演助理、武術指導阿強、宣傳阿珍、導演待定、場務阿文、廣告監製、製片阿強、燈光師阿輝、收音阿明、剪接阿文、編劇阿文、統籌阿強、製作部阿文、後期阿明、幕後阿強、美術指導、服裝指導、動作指導、導演未公開、監製待定、場務組阿文、副導阿成、客戶經理、宣傳部阿玲。**舊 v117 窮舉 29 個一個都擋唔到（0/29）**——反證材料；其中「副導阿成」「宣傳部阿玲」已經喺現行池，舊規則連現行值都漏。
- 每個關鍵字都有用：25 個關鍵字每一個或者命中實池值，或者命中將來值，唔留死關鍵字（logic test 逐個斷言）。
- 其他顯示路徑檢查：`gigDirectorLabel` 唯一 consumer 係 `gigDirectorRealName117`；S-30 卡經 `directorRow117` 係唯一導演顯示路（grep `director` 全量核對：其餘 `.director` 係 NPC 人情數值、`gig.director` 只入搜尋 haystack，唔顯示）。`spec.director || "副導"` 工廠預設值（4 處）照舊由 helper 濾走。

## 測試
- 新守門（全部 PASS；pristine main 跑新測試 FAIL，反證成立）：
  - `tests/test_director121_logic.js`（node 沙箱，讀真關鍵字表＋真函數）：108 斷言——16 職銜值、113 真名逐個＋逐關鍵字零碰撞、fallback／空值、29 將來值＋舊規則 0/29 反證、每關鍵字有用。喺 pristine main 跑即 throw（`const not found: GIG_DIRECTOR_ROLE_KEYWORDS121`，exit 1）。
  - `tests/test_director121_static.py`：20 斷言——舊 Set 已刪、新表＋判定在、25 關鍵字齊、註解有分組／揀字理據／更正數字／檢查方法／已知限制、S-30 卡接線不變、紅線（SAVE／softRev／?v=）不變。喺 pristine main 跑 FAIL（exit 1）。
- 舊 `tests/test_s30dedup117_static.py` 全部繼續 PASS（35 斷言，零修改——佢嘅 9 個字面值檢查靠內嵌通告數據＋fallback return 照舊存在，唔係靠已刪嘅 Set；helper 名 `gigDirectorRealName117` 保留）。
- 因 v121 改動而要修嘅現成測試（全部再 PASS，唔係放寬）：`test_travel114_static.py`（行號純漂移：index.html 淨 +30 行；`qa121/resync_travel114.py` 順序對齊 44 行 `openLoc(` 呼叫點，逐行內容逐字相同，確認純漂移；COUNT 13 處／FREE 27 處／DEF_LINE 52487／WRAPPER_LINE 43341）。
- 全套回歸：pristine main `215b97e` 基線 **159 PASS／12 FAIL**；工作版 **161 PASS／12 FAIL**（＋2 新守門檔），FAIL 清單逐字一致（flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38）。零回歸。註：任務書話基線 160/12，實量係 159/12（171 檔；FAIL 清單同 v118 一致，差額係基線數，唔係回歸）。

## 實駕（390×844，`?softPreview=1`，Playwright；工作版，`qa121/drive_verify121.py`＋`verify_work.json`＋`qa121/shots/`）
- 全池 in-page 複算：183 張＝137 出／46 隱，113 個真名 distinct、16 個職銜值，分布同 census 逐項對上。
- 通告卡（全部行真 UI：入地點→通告欄→撳卡；Day1 兩個地點，額度 2/2 用完）：
  - 職銜 ×2：星河電視台《賀歲特輯》cny（副導）、維港電影《戲院人潮》cinema（副導）——兩張都**無導演行**，同 v117 一致（截圖確認）。
  - 真名 ×2：星河電視台《瑞氣盈門賀新歲》var_05——導演行「何偉龍」；《賀歲喜劇笑滿堂》tv_06——導演行「高志明」（截圖確認）。
  - 注入 ×3（同板改 `window.GIGS` director 值再重撳 teaser，唔入 content pack）：var_05→「監製阿文」、tv_06→「執行導演」、cinema→「執行導演」——三張都**無導演行**。
  - 過日持久性：cinema 注入值過咗一日之後仍然係「執行導演」（池冇 reload 沖走）。
- **7/7 PASS，0 pageerror，0 console error。**
- 途中修好三個腳本問題（唔入 repo）：「暫未能報」係 stay 掣（撳極唔閂，離開要用 `.btn_leave`）；板 modal 喺 detail 閂咗之後仲開緊，要經「返地點選單」先閂得乾淨，否則「返回地圖」／「過一日」撳掣會俾 overlay 攔住（Day3 額度假死就係咁嚟）；翌日晨早故事 modal「休息（週二）」嘅「下一句」有打字機延遲，唔好搶撳「開始今日行程」。最終流程改晒做 Day1 兩板驗晒，唔使過日入場。
- 途中撞到嘅非 v121 問題：無。廖炳星 shy 404 今次冇撞到。

## 合併紀錄
- Squash 合併入 main：`3bc0061`（基底 `215b97e`＝v118）。
- 本地 main index.html：5,139,404 bytes，sha256 `266bd83750e402d7613ea04a981bc9775b36a8a13a42de3d9fef998bc2009e70`。
- 線上初檢（合併後即刻）：5,137,219 bytes，sha `af6b43db0911b34a…`——舊版，Pages 部署滯後；推呢個 NOTES commit 重觸發部署，之後再核實。
- 線上覆檢（NOTES 重觸發後）：（待補）

## 回滾方法
- 成段還原即可：`git revert 3bc0061`（squash 單一 commit；只掂 index.html＋3 個測試檔，無 content pack、無 SAVE key、無資產）。舊 `GIG_DIRECTOR_GENERIC117` Set 會返嚟，但留意還原即係還原埋漏網 15 張（監製／導演等會重新出導演行）——回滾只適用於新規則本身出問題（例如誤殺真名），唔係無代價。
- 單點修正（唔使成段 revert）：加／減關鍵字只係改 `GIG_DIRECTOR_ROLE_KEYWORDS121` 一行表；改完跑 `node tests/test_director121_logic.js`（佢會即刻驗 113 真名零碰撞＋29 將來值）。

## 殘留缺口
- 已知限制（寫埋喺註解）：值預期係「淨人名」或「淨職銜」二揀一；「導演陳大文」呢類混合值會被成個濾走（實池 0 張；內容側應直接填淨人名，唔好加前綴）。
- 關鍵字表係靜態表：將來新職銜詞（例如全新工種）要人手加字；加字前先對住實池真名做子串碰撞檢查（logic test 內嵌 113 真名表就係檢查工具）。
- v117 NOTES 嘅「152 真名／31 職銜值」數字錯咗，呢份 NOTES 已更正；v117 份 NOTES 本身保留原貌唔改。
