# NOTES_V20A203 — WF4 迎新期＋Phase 2 擴池＋B3／C1／C2／C3（v193 設計 review 六項一次過）

分支 `v20a203`，基底 main `6e45cdb`（v193 NOTES 後最新）。**只做實作＋驗證，唔落地。**
PixelLab 花費：**0 次**——C2 用現有資產重映射已夠，冇新生成。

## 0. 問題來源

v193 設計 review（`~/workspace/linji-design-review-v193/REVIEW.md`，13 張截圖）：
B1 開局 52 日零事件（day 7→59）、101 日得 5 單；B2 loc 池每地點得 4–5 單（cafe_cha 11 單除外），
tvb_longmen day 125 抽乾；B3 set17／st17 近似重複；C1 點歌／銀包前提近似；C2 場景圖錯配 7 單；
C3 day 98 強制播 C6F 撞正春季廣告賞典禮，兩層疊埋（R4a，唔係穩定重現）。
用戶 2026-11-14 11:23 拍板一次過修晒六項。

## 1. B1 迎新期頻率＋B2 Phase 2 擴池（一齊設計）

### B1：開局首 30 日較高頻率，線性漸降返基線

`WF4_CFG` 加 `pDayWelcome:0.12, pLocWelcome:0.08, welcomeDays:30`（基線 `pDay:0.03, pLoc:0.03` 不變）。
新 helpers `wf4EffPDay(day)`／`wf4EffPLoc(day)`：day 0 係 0.12／0.08，線性降到 day 30 回復 0.03／0.03，
之後全程基線。`wf4DailyTick` 用 `wf4EffPDay(day)`，`wf4TryLocEvent` 用 `wf4EffPLoc(day)`。

揀值經過：先試 0.09／0.06（頭 30 日 A2／B5／C1／D3），再試 0.12／0.08（A4／B5／C2／D4），
三年總數只多 1–2 單、抽乾日唔郁，所以採用 0.12／0.08。唔齋調高頻率，連 Phase 2 擴池一齊做。

### B2：池 72→113 單

day 36→48（新 day17–28，12 單），loc 36→65（新 set26–54，29 單）。
每地點 loc 池：film_lion／film_cotton／film_harbour／tvb_longmen／tvb_harbour／tvb_kowloon 各 9 單，
cafe_cha 維持 11 單。新事件插喺 `DAILY_EVENTS_WF4` 尾（cha07 之後），全部廣東話、1990–92 質地、
冇真人名／禁詞、冇阿偉講者、fx 鍵合規（money ±80..120、stress ±8、stamina ±6、fame/pop/acting/charm/stage ±2）。
變體寫到真係唔同場景（屋邨樓梯燈／街市魚檔蝦／舊書攤雜誌／地鐵賣唱／電視台觀眾來信／年尾利是…），
唔係淨換年份數字（NOTES §8 要求）。

## 2. B3 近似重複（兩處都改）

- `wf4_ev_set17`「錄影廠門口嗰班粉絲」嗰句「你嗰場喊戲，我喊埋一份。」改寫做
  「我阿媽話你嗰場戲做得好自然，叫我一定要搵你簽個名」——唔再用「喊戲＋我喊埋一份」組合。
  核實：全 WF4 區塊「我喊埋一份」只剩 day12 一處。
- `wf4_ev_st17` 成單重寫做「樓下士多嗰支豆漿」（士多阿叔＋豆漿，唔再係涼茶舖＋阿婆＋廿四味；
  第二 choice out 特登避開舊「話梅」）。核實：「涼茶」／「廿四味」只剩 day04。

## 3. C1 前提近似（兩對）

- 點歌：`wf4_ev_st15` 改做「的士司機嗰段追星往事」（司機講自己後生追星往事，唔再係點歌）；
  `wf4_ev_set21`（廣播室電話）保留。核實：「點歌」只剩 set21 一單（內文 2 次）。
- 銀包：`wf4_ev_day15`「銀包得返幾蚊」閘由 `moneyMax:1000` 改 `moneyMax:200`，
  同 day03 嘅 ≤$1000 分層。實證：銀包 $500 → day03 出、day15 唔出；$150 → 兩單都出。

## 4. C2 場景圖錯配（零新生成，重映射）

day05 冰室→`bg_loc_cafe_cha.jpg`、day07 電車→`bg_wf4_taxi.jpg`、day09 唱片舖→`bg_loc_gift_shop.jpg`、
day11 茶樓→`bg_loc_cafe_cha.jpg`、day14 片場休息區→`bg_loc_film_lion.jpg`、
day15 茶餐廳門口→`bg_loc_cafe_cha.jpg`、st17 士多→`bg_loc_gift_shop.jpg`；
新 day17–28 全部入 `WF4_SCENE_OVERRIDE134`（day17／19／24／28 home、day18／23／25 market、
day20／21 gift、day22／26／27 taxi）。覆寫表 36→48 行，全部檔案存在已驗。
下一批新圖優先補冰室／電車／茶樓／唱片舖四個場景（參照相先行，跟場景圖硬規矩）——
重映射已夠，呢票唔生成，PixelLab 0 次。

## 5. C3 強制播撞典禮（調查結論＋防禦性修法）

調查（機制已查明，見 `index.html` 內 `morningChain196`／`awards62PlayCeremony`／`story165CanPlay`）：

- 晨鏈 `morningChain196` 順序行（請柬→典禮播完→cont→強制播），唔會撞。
- 典禮 `awards62PlayCeremony` 係掛 `document.body` 嘅全屏 overlay（`.awd62-stage`，
  `position:fixed;inset:0;z-index:9990`），唔經 StoryPlay、唔設 `_storyPlayLocked`，
  所以 `story165CanPlay` 原本唔知佢存在。
- 只有晨鏈之外嘅掛點（`#loc-close`／`book70ExitHome` → `story165TryForcedPlay`）喺典禮進行中
  被觸發（例如探針 JS click 穿透 overlay）先會兩層疊埋，故事掣俾典禮層冚住撳唔到，
  播完 `isDone('C6F')` 返 false（review R4a，day 98 C6F 撞春季廣告賞）。
- **真人玩家撳唔穿全屏典禮層**，所以唔係 live bug，係防禦性閘。
- 會唔會食出行額度：唔會——`#loc-close` 路徑本身唔計出行額度。

修法：新 `awards62CeremonyActive()`（`document.querySelector(".awd62-stage")`，有 `typeof document` 守衛），
`story165CanPlay()` 加一行閘（排喺 `isStoryPlayActive`／`_storyPlayLocked` 檢查之後、`story165NextOpen()` 之前）。
典禮播完（stage 拆走）後下次返地圖晨鏈尾段強制播照常行，故事唔會唔見。

## 6. 頻率模擬（`qa203/sim_wf4.js`，用遊戲本身 WF4 code eval）

頭 30 日迎新期（工作版）：A4／B5／C2／D4（合共 15 單）；pristine 基線 A2／B3／C1／D1（合共 7 單）。
迎新曲線實測：`wf4EffPDay(0/15/29/30)` = 0.120／0.075／0.033／0.030；
`wf4EffPLoc` = 0.080／0.055／0.032／0.030。
三年 1095 日：A 81／B 58／C 57／D 50（pristine 62／47／41／42），重複率全部 0%，每單最多見 1 次。
抽乾：tvb_longmen（B 路線）由 day 125 推遲到 day 750；day 池抽乾日 1075（約三年尾）；
cafe_cha B 路線維持 day 771。
（輸出 `qa203/sim_output.txt`；pristine 對照 `qa203/sim_output_pristine.txt`。）

## 7. 測試（新＋更新，全部 PASS；反證對 pristine 乾淨 FAIL）

新：
- `tests/test_wf4_203_logic.js`（42 項 ALL PASS）：迎新曲線準確值、頭 30 日 inline sim（A4／B5／C2／D4）、
  三年四路線重複率 0%、B3／C1 文案去重＋分層實證、C2 7 單重映射＋12 單新 day 入表、C3 典禮閘
  （有 stage → CanPlay null；冇 stage → 返 C6F）。
- `tests/test_wf4_203_static.py`（TOTAL PASS）：CFG 欄位、helpers 接線、B3／C1 逐單 chunk 計數、
  覆寫表 48 行、典禮閘排位、`.awd62-stage` 全屏 overlay。

更新（池 113／day 48／loc 65／每地點 9／覆寫表 48）：
`test_wf4_193_logic.js`、`test_wf4_86_logic.js`、`test_wf4_193_static.py`、`test_wf4_86_static.py`、
`test_ui134_wf4scene_static.py`、`test_wf4dlg108_logic.js`、`test_wf4dlg108_static.py`、
`test_story198_logic.js`（extract list 加 `wf4EffPLoc`）——全部 ALL PASS／TOTAL PASS／RESULT PASS。

反證（pristine main `6e45cdb`）：203 logic 31 FAIL、193 logic 7 FAIL、86 logic 3 FAIL、
dlg108 logic 3 FAIL、203 static TOTAL FAIL 35、193 static TOTAL FAIL 10、86 static FAIL、
ui134 TOTAL FAIL 44、dlg108 static RESULT FAIL (3)——全部乾淨 FAIL，唔 crash。
（註：86 logic 嘅 (7) 讀 pack JSON 係跟 html 所在目錄搵 `content/`，對 `/tmp/pristine203.html`
跑會 ENOENT crash——pre-existing 測試設計限制；將 pristine 檔擺入 repo 目錄再跑就乾淨 FAIL 3 項。
193／86／203 logic 嘅 helpers 抽取已加 try/catch stub，pristine 冇嗰啲函數嗰陣斷言乾淨 FAIL 唔 crash。
story198 logic 喺 pristine ALL PASS——正確，佢驗嘅係 v198 行為，pristine 已經有。）

教訓（兩次）：**唔可以喺 `DAILY_EVENTS_WF4` 陣列入面放任何註解**（block comment 同 `//` 行尾註解都會整爛
dlg108_static 嘅 naive JS→JSON 轉換；v193 已有同一教訓）。Phase 2 說明註解已搬去陣列外；
day15 嗰行 `// v20a203 C1` 尾註已刪除。陣列內現時零註解已驗。

## 8. Resync（行號釘測試，純漂移）

index.html 淨增 +233 行（61167→61400）。`qa203/resync203.py`（difflib 對位 pristine `6e45cdb` vs 工作版）：
全部釘行內容逐字相同，BAD: none。
- rom176：54069→54302、54437→54670、55576→55809、55670→55903（6134／31695 唔郁）。
- tang171／173：總行數 61167→61400、openLoc DEF 55639→55872。
- travel114：DEF 55639→55872、WRAPPER 44902→45135、COUNT 12 行＋FREE 33 行逐行對位。
- gift185：總行數 61167→61400。
五檔 resync 後全部 PASS。

## 9. 全套 A/B（`qa131/run_suite.sh`）

- 工作版：**TOTAL PASS 282 FAIL 16**（298 檔）。
- Pristine 對照（同一套測試，symlink 樹）：TOTAL PASS 273 FAIL 25。
  差額 9 項＝5 項 v203 更新測試喺 pristine 正確 FAIL（gift185／rom176／ui134／wf4_193_static／wf4_203_static）
  ＋4 項 NOTES 路徑 artifact（aud91／dayend189／dayflow196／verify37 驗 `NOTES_*.md` 喺 index.html 隔籬，
  symlink 樹入面冇嗰啲檔——唔係遊戲問題）。
  （註：pristine symlink run 嘅 node 測試經 `__dirname` 讀返工作版 index.html，嗰部分結果唔準；
  node 反證已逐檔用明確路徑參數跑過，見 §7。）
- **零回歸**：工作版 16 個 FAIL 全部都喺 pristine FAIL 清單入面（`comm` 比對為空），
  即係全部係 pre-existing。任務講嘅基線 283／13 係 v193 落地嗰陣嘅數字；今次 298 檔入面
  pre-existing FAIL 集合係 16 項，兩邊一致。

## 10. 實駕（Playwright，`qa203/drive203.py`，本地鏡像＋`http.server`，LIVE 裸 URL）

0 pageerror、0 console error、0 http fail（全程）。報告 `qa203/drive203_report.json`，截圖 `qa203/shots203/`（28 張）。

- **A 場景巡迴（pending-seed 即彈，R5 手法）：15/15 PASS。**逐單 seed pending（seen 清空、pendingDay＝當日、
  按 cond 補 day／money／fame／stress），reload＋讀檔＋返地圖即彈 modal；標題＋場景圖 URL 全部啱，
  圖檔經 HTTP 驗 200。day05 冰室→`bg_loc_cafe_cha.jpg`、day07 電車→`bg_wf4_taxi.jpg`、
  day09 唱片舖→`bg_loc_gift_shop.jpg`、day11 茶樓→`bg_loc_cafe_cha.jpg`、
  day14 片場休息區→`bg_loc_film_lion.jpg`、day15 茶餐廳門口→`bg_loc_cafe_cha.jpg`、
  st15 的士追星往事→`bg_wf4_taxi.jpg`、st17 士多豆漿→`bg_loc_gift_shop.jpg`、
  day17／day24→`bg_wf4_home.jpg`、day18→`bg_wf4_market.jpg`、day20→`bg_loc_gift_shop.jpg`、
  set17→`bg_loc_tvb_longmen.jpg`、set26→`bg_loc_film_lion.jpg`、set54→`bg_loc_tvb_kowloon.jpg`。
  （set54 第一輪 FAIL 係 drive 時序問題，唔係遊戲 bug：day 730 載入撞星河台慶典禮，drive 未等典禮播完就讀 modal；
  加咗 ceremony-wait 之後重跑 PASS。見 §12。）
- **B 迎新期密度（fresh 局，行到 day 30）：實測 2 單，全部唔同（`ok: false` 對自設 ≥3 斷言——見下）。**
  路線：每日入 tvb_longmen＋cafe_cha 各一次＋過日；三輪重跑結果完全一致（deterministic roll）：
  「大排檔嗰張長枱」（day25）＋「街市魚檔嗰斤蝦」（day18），0 pageerror。
  對照：v193 實玩係開局 52 日零事件（day 7→59）——**0／52 日 → 2／30 日，迎新期實玩密度確實有改善**，
  但未到 sim A 路線預測嘅 4 單。差距原因（drive 路線 artifact，唔係遊戲 bug）：
  sim 係逐日 tick＋每日輪入 7 個地點；實玩行程係撳「開始今日行程」跑成週計劃，每次推進跳 3–4 日，
  中間嗰啲日冇入場擲骰（每日得返落點日嗰次 tick＋兩次入場）。即係話 sim 係頻率設計嘅證據，
  實玩數字係呢條路線下嘅量度——兩者路線唔同，唔可以直接對數字。
  另一個待跟進觀察（未證實）：成週計劃一次推進幾日嗰陣，中間嗰幾日嘅 daily tick 似乎只跑落點日嗰次；
  要證實要另開探針，唔喺呢票做。
- **C 典禮撞強制播（R4a 播種，day 98）：PASS。**晨鏈請柬→典禮舞台出現（`ceremony_seen: true`，
  冇請柬 modal 要撳，直接入典禮）；典禮進行中用 JS click 穿透（入地點＋閂 sheet）→**故事零開**
  （`story_during_ceremony: false`，典禮層仲喺度）；穿透前後狀態零變化（day 98、money／stress／fame／
  locTries 0／pending set17 全部唔郁——唔食出行額度）；撳跳過→典禮完→晨鏈先呈現 WF4 pending set17
  （要撳埋佢先輪到強制播）→C6F 強制播（act191「第 6 幕・電影線：片場跟班」）→播完 `isDone('C6F')` True。
  即係話：R4a 嗰個兩層疊埋喺 v203 唔再出現，故事亦唔會唔見。
- **D 地點抽乾（film_lion）：PASS。**seed seen＝全部 113 單除咗 set26；每日入 film_lion 兩次，
  attempt 16 彈 set26「片場門口嗰個飯盒」（唯一未見過嗰單）；抽乾後再入 film_lion 3 次（跨日）→零 WF4 modal。
  （註：loc roll 係 deterministic hash，`film_lion` try 1 喺 day 0–59 系統性偏高零中；
  每日入兩次用埋 try 2 先中。見 §12。）
- **E 700 smoke：PASS。**fresh 局＋pending-seed day05，標題「冰室門口嗰張櫈」＋場景圖
  `bg_loc_cafe_cha.jpg`＋圖 200，地圖正常。

## 11. 改動總覽（`git diff --stat`，未計新檔）

14 檔改動，354 insertions(+)，102 deletions(-)。`index.html` +254／−21（淨 +233 行，61167→61400）：
迎新期 CFG＋helpers（~15 行）、41 單新事件（~183 行）、覆寫表＋19 行、7 單重映射、set17／st17／st15／
day15 文案＋閘改動、C3 `awards62CeremonyActive`＋`story165CanPlay` 一行閘。
新檔：`tests/test_wf4_203_logic.js`（218 行，42 項）、`tests/test_wf4_203_static.py`（98 行）、
`NOTES_V20A203.md`、`qa203/`（sim＋resync＋drive＋probe_set54＋報告＋25 張截圖）。
其餘 13 檔測試改動全部係池數／行號 resync／extract list（見 §7／§8）。

## 12. 殘留／跟進

- 下一批新圖優先補冰室／電車／茶樓／唱片舖四個場景（C2 註，參照相先行）。
- v193 NOTES §5 eventLine 重複（唔入呢票，沿用）。
- 實駕發現（drive 流程問題，唔係遊戲 bug）：① day 730 載入會撞星河台慶典禮（晨鏈請柬→典禮→結果卡），
  pending-seed 巡迴要等典禮播完先讀 modal——drive 已加 ceremony-wait；② `saveQ` 係 IIFE 內部，
  頁面 evaluate 叫唔到——drive 改用直寫 localStorage（R4a 手法）播種；③ loc roll 係 deterministic hash，
  `film_lion` try 1 喺 day 0–59 系統性偏高（零中），D case 要每日入兩次（用埋 try 2，day 4 中）；
  ④ `#map-end-day` 有兩個（重複 id），drive 改用可見嗰粒；⑤ B 迎新期實測 2／30 日（自設 ≥3 斷言未達，
  見 §10——v193 係 0／52 日，有改善但未到 sim 預測 4 單；差距係 drive 路線唔同 sim 路線所致）。
- B 迎新期實測未達自設 ≥3：唔係回歸，係量度路線差異；要更貼近 sim 嘅數字就要改 drive 路線
  （逐日推進＋輪入 7 個地點），留返統籌決定係咪重跑。

## 13. 補修：三個舊測試期望過期（統籌獨立重驗發現，唔係遊戲回歸）

獨立重驗發現三個舊測試嘅期望值俾 v203 有意增長追過，遊戲本身冇問題；只更新測試期望，
**index.html 零改動**。三個原因全部已核實：

- `tests/test_poster85_static.py`：斷言主檔 `< 5,386,704 + 40,000 = 5,426,704`。
  v203 有意增長約 40KB（41 單新事件＋迎新期 code），主檔實測 5,448,954 bytes，
  所以超標。跟返呢個測試歷次慣例（v89／v92／v95 有意增長嗰陣上限跟住原位更新）：
  基數改做 5,448,954，保留 +40,000 slack，即上限 **5,488,954**。
- `tests/test_ux68_static.py`：斷言主檔總量 `< 5,430,000 bytes`，同一原因超標。
  上限改做 **5,490,000**（現尺寸 5,448,954 ＋約 41,000 slack）。
- `tests/test_scene104_static.py`：斷言 `src.count('?v=20a104') == 18`。
  工作版實測 26 處（pristine 18 處）。+8 係 v203 C2 重映射喺 WF4 覆寫表入面重用
  `?v=20a104`——檔案本身冇變，cache-buster 重用係正確嘅。
  組成更新：builder 1＋LOC_SHEET_BG 15＋WF4 覆寫表重用 10（v134 2＋v203 8）。
  期望計數 18→**26**。

逐個重跑三個測試，全部 PASS（poster85 11/11、ux68 26/26、scene104 58/58）。

全套重跑（`qa131/run_suite.sh`，2026-11-14 13:0x）：

- 工作版：**TOTAL PASS 285 FAIL 13**（298 檔）。
- Pristine 對照：**TOTAL PASS 283 FAIL 13**——今次用 `~/workspace/tmp-pristine203/`
  實體 worktree（main `6e45cdb`），**唔再用 symlink 樹**（上一手 symlink 樹令 pristine
  虛增 9 個 FAIL：5 項 v203 更新測試＋4 項 NOTES 路徑 artifact，見 §9）。
- **零回歸**：`comm` 比對工作版 FAIL 清單 vs pristine FAIL 清單，work-only 為空——
  13 個 FAIL 兩邊完全相同（flash51／giglib36／pacing35／poster59／rumor49／slot50／
  soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），
  全部係 pre-existing。工作版 PASS 多 2 項（285 vs 283）係 v203 新測試喺工作版 PASS、
  喺 pristine 正確 FAIL。
- 對 §9 數字嘅說明：§9 工作版 282／16 vs 今次 285／13——差 3 項就係呢三個期望更新後
  由 FAIL 轉 PASS，一一對應。Pristine §9 係 273／25（symlink 樹，298 檔）vs 今次 283／13
  （實體 worktree，296 檔）：檔數少 2 係 v203 新加嘅兩個測試檔（`test_wf4_203_logic.js`、
  `test_wf4_203_static.py`）喺 main `6e45cdb` 根本唔存在；FAIL 少 12 項入面，§9 已列明
  9 項係 symlink 樹虛增（5 項 v203 更新測試＋4 項 NOTES 路徑 artifact），其餘 3 項
  （含嗰兩個新測試檔喺 symlink 樹入面跑出嚟嘅 FAIL）冇舊輸出留底對唔返逐項——
  但唔影響結論：今次實體 worktree 嘅 pristine FAIL 清單同工作版 FAIL 清單逐項相同。
  註：三個測試喺 pristine 全部 PASS（pristine 主檔 5,409,025 bytes，未超舊上限；
  scene104 計數 18 啱啱好），喺工作版更新期望後亦全部 PASS；兩邊 FAIL 清單相同＝零回歸，
  結論不變。
