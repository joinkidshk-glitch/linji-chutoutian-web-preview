# NOTES_V20A206 — WF4 B1：重寫 v203 擴池抄襲嘅 8 對＋打散模板腔

分支 `v20a206`，基底 main `165597e`（v203 落地）。**只做 B1，唔掂 C1／C2。只做實作＋驗證，唔落地。**
C1 補喺 §6（同一分支，另一工人；上面「唔掂 C1」係 B1 工人嘅範圍）。
PixelLab 花費：**0 次**——純文案重寫，零新生成。

## 1. B1：8 對逐對重寫＋模板腔打散

### 機制說明（任務話「睇 NOTES §8 確認機制」嘅核實）

`NOTES_V20A203.md` §8 實際係 Resync（行號釘測試），唔係覆寫機制——任務嘅 §8 指針唔啱。
核實咗 v203 實際做法：WF4 新事件根本唔喺 content pack JSON 入面，佢哋係 inline 寫喺
`index.html` 嘅 `DAILY_EVENTS_WF4` 陣列入面；v203 自己嘅 B3／C1 重寫（set17／st17／st15／day15）
都係原位改陣列條目。`WF4_SCENE_OVERRIDE134` 只係場景圖覆寫表，唔覆寫文字。
所以今次跟返 v203：**原位改陣列條目，pack JSON 零掂**。`git diff` 證實：只改 `index.html`，
pack JSON／其他檔零改動。

### 8 對點改（fx／cond／loc／title 定位全部不變，只改 beats＋choices 文案）

1. **set32 vs set23（舊）＋set48 share 第二句 out——三個分身**：
   - set32「外景嗰程小巴」（瞓覺＋傾偈）→「外景小巴嗰個暈車」：半路有新臨記暈車，
     choices 變「開窗畀佢吹下風」／「讓個窗口位畀佢坐」。set23 舊單原封不動做對照。
   - set48「外景車嗰程山路」（傾偈 out 逐字相同）→「外景車半路爆胎」：山路爆胎換士啤胎，
     choices 變「幫手遞工具畀司機」／「企埋路邊睇下山景」。三單而家三個唔同場景。
2. **set35 vs set15（同 film_harbour 池，兩對 choices 全抄）**：
   set35「海邊嗰場晨戲」→ 潮水漲要搶拍：beats 改潮水追住嚟，choices 變
   「捲起褲腳行去水邊」／「幫手搬啲道具上岸」（fx 不變）。set15 舊單原封不動。
   兩單唔再係同一對掣。
3. **set30 vs set54（兩單都係新，同一前提＋逐字 beat／out）**：
   set54「收工嗰陣嗰首歌」（門口聽歌手練新歌）→「收工嗰陣嗰段對白」：隔籬廠排話劇背台詞，
   前提都唔同，choices 變「企喺度聽埋成段對白」／「跟住唸兩句先走」。
   附帶：set30 兩隻 label 都同別單撞（「企喺門口靜靜聽」撞 set41、「返去自己嗰邊開工」撞 set47），
   一併改做「企喺門口聽埋佢」／「收起心返去開工」，out 亦重寫。
4. **set42 vs set22（換餸重寫）**：set42「電視台飯堂嗰碗麵」成單重寫 →
   「電視台飯堂嗰碟排骨飯」：手寫餐牌特價豉汁蒸排骨飯，choices 變
   「嗌碟排骨飯慢慢食」／「讓個位畀後來嗰個阿叔」。set22 叉燒舊單原封不動。
5. **day27 vs set33（out「話佢識嘆，話呢度啲風，係免費嘅福利嚟」逐字相同）**：
   set33 天台兩句 out 全換（「佢哋兩個吹住水，場務指住樓下話…」／天台風景 out）；
   day27 兩句 out 亦重寫（釣魚 out 唔再「成個人鬆晒」，吹風 out 變「海風唔使錢，吹幾耐都得」），
   choice 2 label「同阿伯吹下海風」撞 st13，改做「陪阿伯吹下海風」。
   附帶：舊 set20 仲有另一寫法「呢度啲海風，係免費嘅福利嚟」獨留一處，唔係共享，保留。
6. **set31 vs set40（out「話聽日嗰場戲啲燈，幫佢打靚啲」逐字相同）**：
   set40 遞工具 out 重寫（較好燈＋企位）；set31 斟水 out 亦重寫（茶水間飲熱茶），
   兩句唔再共享。
7. **day24 vs set21（同一「認可」前提）**：day24「電視台嗰封觀眾來信」成單重寫 →
   「電視台嗰封冇名信」：信件房搵到封冇收信人嘅信，入面得張戲飛＋失物字條，
   幫手貼告示等人認／交去失物認領處。**認可 beat 成個拆走**，唔再整多個變體
   （v193 C1 要求）；cond（tierMin:1、yearMin:1992）不變。set21 點歌舊單保留。
8. **set46 vs day11（out「佢將啲消息記喺心入面…」逐字相同）**：
   set46 佈告板 choice 1 out 重寫（逐張睇＋返屋企攞紙寫低＋聽日去問下）；
   beat 2 亦重寫（「唔好淨係等電話，要周圍行下先得㗎」同 day11 共用，改做「唔好淨係坐喺度等」）。
   day11 茶樓舊單原封不動。

### 去重檢查搵到嘅額外同類問題（同一測試捉到，順手清埋，全部係新 41 單）

- 。級成句撞：day06／set51 label「打包返屋企同阿媽食」（set51 改「打包兩碗返屋企食」）。
- ，級子句（≥10 字）撞：day18 beat1 開頭抄 day12「阿偉幫阿媽去街市買餸」；
  set46 beat1「唔好淨係等電話」撞 day11；set42 beat1「阿偉排隊嗰陣」撞 set22；
  set33 beat2「唔好成日匿喺廠入面」＋out2「兩個人吹咗陣水」撞 set20；
  set44 out1「入鏡嗰陣成個人定晒…豎起手指公」抄 set13；
  set28 out1「返出去開工嗰陣」撞 set52；set50 beat2「唞陣先再開工，唔好成日企喺太陽下面」撞 set37；
  set41 out1 尾「返到屋企對住鏡練，話第日上場唔會失禮」撞 set27；
  set32 out1 尾「落車嗰陣話多謝佢」撞 st15；day25 beat2「食過就返唔到轉頭」撞 st12；
  day27 beat1「海風吹到好舒服」撞 set20；set45 out2「話呢啲嘢學多啲冇壞」撞 day19；
  set38 out2「諗起今日嗰場戲，到底邊度做得唔夠好」撞 day10／set39；set50 beat1「唞陣先再開工」撞 set37。
  全部已改寫，見 `qa206/rewrite206.py`＋`qa206/rewrite206b.py`（每句舊文 assert 全檔恰好 1 次先換；
  撞嗰句本身出現 2 次嗰幾處用埋 label／fx 定位）。
- 剩低嘅 ，級共用子句全部係 ≤9 字通用短語（「阿偉行過嗰陣」「嗰個話多謝佢」等）
  或舊池對舊池 pre-existing（例如 set15／set24「阿偉企喺碼頭邊等埋位」），唔喺 B1 範圍，留返。

### 模板腔改前／改後（新 41 單，beats＋label＋out 計數）

| 短語 | 改前 | 改後 |
|---|---|---|
| 話佢識 | 28 | **0** |
| 成個人鬆晒 | 9 | **0** |
| 聽到入晒神 | 5 | **0** |
| 識食 | 5 | **0** |
| 識做人 | 5 | **0** |
| 眉飛色舞 | 4 | **0** |

全部 ≤3（要求），實際清零。「X 話佢識 Y」預設 out 收尾已全部拆走，收尾句式多樣化
（例：set26「食得乾淨」、set38「反應快」、set47「有耐性」、set49「聽得入耳」、day28「大個仔，識心痛人」）。
全池餘數係舊池 pre-existing（話佢識 9／鬆晒 5／入晒神 4／識食 3／識做人 2／眉飛色舞 4），唔喺 B1 範圍。

### 其他核實

- fx 數值／schema 唔郁：6 單成單重寫＋全部逐句置換，fx 原封不動；新測試釘死新 41 單全合規
  （money ±5..120、stress ±8、其餘 ±1..2）。舊池有 4 例 pre-existing 例外
  （set04 stamina:3、cha03 money:-2、home01 stamina:4、day01 stamina:4），v203 前已存在，
  唔喺 B1 範圍，測試釘死數目唔多唔少。
- 禁詞零命中（全池 113 單 WF4 chunk）：VCD／互聯網／手機／狗仔隊／1989／1993／手提電話／傳呼機 全部 0。
  （全檔 grep 有命中係其他系統嘅 code／註解，唔係 WF4 文案。）
- 廣東話＋1990–92 質地不變；無真人名；文案無數字承諾。
- 陣列內零註解（v193／v203 教訓）；`index.html` 5,448,954 → 5,450,201 bytes（+1,247），
  行數不變（52 行改寫，淨 0 行）；poster85／ux68 尺寸上限測試照過。

## 2. 新測試＋反證

新檔 `tests/test_wf4_206_static.py`（48 項，工作版 TOTAL PASS）：

- (a) 。級成句去重（全池，split 。！？；＋全文，≥6 字）：**0 共享**（改前 20 撞）。
- (b) ，級子句去重（≥10 字，只計涉及新 41 單嘅對）：**0 共享**（改前 7 撞；舊池對舊池 pre-existing 唔計）。
- (c) 模板短語新 41 單每種 ≤3 次：全部 0（見上表）。
- (d) 8 對 review 引文逐句核對（每句最多 1 單）：13 句全部 ≤1——
  共享句全部清零（例：「話聽日嗰場戲啲燈，幫佢打靚啲」0、「做呢行，聽得多歌，把聲都會好啲」0）；
  舊單獨留嗰句計 1（例：set23 瞓覺 out、set15 望海 out、set21「話佢嗰場戲做得好」、day11 消息 out、
  舊 set20「係免費嘅福利嚟」）。
- (e) 8 對重寫在位＋舊單原封不動對照（set23／set15／set22／day11）。
- (f) fx 合規（新 41 全合規；舊池 4 例 pre-existing 釘死）。
- (g) 禁詞零命中（全池）。(h) 陣列內零註解。

**反證**（pristine main `165597e`，`/tmp/pristine206.html`）：**TOTAL FAIL 28**——
(a) 20 撞、(b) 7 撞、(c) 六種模板 28／9／5／5／5／4、(d) 11 句共享、(e) 8 項重寫未做。
（舊池 fx 例外嗰項喺 pristine 都 PASS，正確——嗰 4 例係 pre-existing，兩邊一樣。）
改前／改後數字見 `qa206/analyze206.py`（模板計數）＋`qa206/analyze206b.py`（。級碰撞）輸出。

## 3. 全套 A/B（`qa131/run_suite.sh <repo-root> <outfile>`，兩個參數齊）

- 工作版：**TOTAL PASS 286 FAIL 13**（299 檔；輸出 `qa206/suite_work.txt`）。
- Pristine 對照（實體 worktree `~/workspace/tmp-pristine206`，main `165597e`）：**TOTAL PASS 285 FAIL 13**
  （298 檔；輸出 `qa206/suite_pristine.txt`）。
- **零回歸**：`comm` 比對 FAIL 清單，work-only／pristine-only 皆為空——13 項逐項相同
  （flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／
  weave43／weave44／weave49／wf5_87／wrap38），全部係 pre-existing，同 v203 落地嗰陣同一集合。
  工作版 PASS 多 1 項就係新測試 `test_wf4_206_static.py`（pristine 根本冇呢個檔）。
- 基準說明：任務講嘅基線 v203 係 285／13（v203 落地嗰陣）；今次工作版 286／13 係 285＋1 新測試，
  pristine 285／13 同基線一致。

## 4. 改動總覽

`index.html` 52 行改寫（淨 0 行）：6 單成單重寫（set32／set48／set35／set54／set42／day24）
＋41 句逐句置換（`qa206/rewrite206.py`）＋14 句補刀置換（`qa206/rewrite206b.py`）。
新檔：`tests/test_wf4_206_static.py`、`NOTES_V20A206.md`、`qa206/`（rewrite 腳本＋分析腳本＋全套 A/B 輸出）。

## 5. 殘留／跟進（唔喺呢票）

- 舊池對舊池 ，級子句共享（例：set15／set24「阿偉企喺碼頭邊等埋位」）＋舊池通用短語
  （「阿偉行過嗰陣」等）＋舊池 fx 4 例例外——全部 pre-existing，B1 唔掂，等以後票決定。
- C1／C2（迎新期保底／場景圖錯配）唔喺呢票，零掂。
- Pristine worktree `~/workspace/tmp-pristine206` 用完即清（唔留大檔）。

## 6. C1：迎新期保底機制（pity timer）

（任務話寫 §2；B1 已佔 §1–§5，C1 補喺 §6，內容齊任務要求嘅六項：機制＋config、tick 驗證、sim 新數字、實駕結果、新測試＋反證、全套數字。）

分支 `v20a206`，基底 main `165597e`（v203 落地）＋B1 commit `60f16b5`。**只做 C1，唔掂 B1／C2。只做實作＋驗證，唔落地。**
PixelLab 花費：**0 次**——純機制，零新生成。

### 機制＋config

- `WF4_CFG` 加 `pityDay:7`（數字唔寫死，等以後可調）。
- 新 helper `wf4SeenAny()`（`wf4DailyTick` 之前）：「從未見過」要穩陣計兩邊——`seen.__n > 0` 或者任何真 event id 嘅 seen 計數 `> 0` 都算見過。`__n` 係 v193 起先有，舊 save 可能有 `seen[ev.id]` 但 `__n` 係 0／undefined，兩邊計就唔會令舊 save 誤觸保底。
- `wf4DailyTick` 入面、概率擲骰之前加保底檢查，放喺已有守衛之後（pending 清理 → `if(st.pending) return;` → `if(!wf4BaseOk()) return;`）：
  `day >= (WF4_CFG.pityDay||7) && !wf4SeenAny()` → `wf4PickEvent("day", null)` 強制揀一單未見過嘅 day 事件入 pending（`st.pending`／`pendingDay`），即 return。**唔直接 fire**，行正常 pending 機制，等晨鏈＋典禮閘＋故事鎖全部照舊生效。
- 保底只會觸發一次：觸發後嗰單經晨鏈播出，seen 非空，條件永遠唔再成立。
- **唔加頻率**：`pDay`／`pLoc`／迎新曲線／池 113 單全部唔郁（新測試釘死）。
- 保底 pick（day 7、seen 空、確定性）：`wf4_ev_day09`「唱片舖試聽嗰首歌」（sim 預測，等實駕對返）。

### tick 驗證（NOTES_V20A203 §14 殘留觀察：證偽）

殘留觀察話「成週推進跳日嗰陣中間嗰幾日嘅 daily tick 似乎只跑落點日嗰次」。**證偽咗，唔係事實**：

- Code 層面：唯一推進 `dayIndex` 嘅生產路徑係 `advanceDay()`（+1，兼每次 call `wf4DailyTick()`）；直接賦值嗰兩處係 console preview（`previewJumpCalendarYear`）同 soft-preview seed（`applySoftSeedState`，flag-gated），唔係 live 玩法。→ live 玩法每日恰好一次 tick。
- 實證（drive206，見下）：`pendingDay=4`＋`lastDay=4`——day 4 有 tick（設咗 pending）兼有播出（`wf4Fire` 嗰陣 `dayIndex` 係 4），但 probe 全程從來冇喺 day 4／5／6 停低採樣過（`days_seen` 根本冇 4／5／6）。Tick 只跑落點日嘅話，day 4 唔會有 pending。
- 跳日機制：唔係跳過日子——「開始今日行程」／「過一日」之後嘅日結 modal 鏈自動連跑連續行程日，每日照樣 `tickDay → advanceDay → wf4DailyTick`。Review 嘅「約 10 次日骰」係採樣 artifact：30 日入面 probe 只係喺 10 個落點日停低（after-advance 落點：3、7、10、11、14、17、21、23、25、30），但 `advanceDay` 實際跑咗 30 次。

### Sim 新數字（`qa206/sim_wf4.js`，eval 真實引擎；輸出 `qa206/sim_output.txt`）

種子事實：日骰頭 15 日只得 day 4（roll 0.0605＜pDay 0.108）同 day 10（0.0752＜0.090）擲中；首 30 日零報紙日（`NEWS82_EVENTS` 頭 30 日冇日子），保底日唔會撞報紙閘。

| 路線 | 頭 30 日 | 首單 | 保底 |
|---|---|---|---|
| A 均衡／B 電視／C 電影／D 茶餐廳（same-day 次序，等 v203 數字可比） | A4／B5／C2／D4（同 v203 一致） | day 1／1／3／4 | 零觸發 |
| R 實玩（開局 3 日唔入場＋每日 2 地點；same-day／morning 兩種次序一樣） | **3 單**（day 3 set53、day 10 day20、day 22 set35） | day 3 | 零觸發 |
| S0 零入場（淨靠日骰） | **2 單**（day 4 day25、day 10 day18） | day 4 | 零觸發 |
| R-skip 對照變體（假設 tick 只跑落點日 0→3→7→9→…） | 1 單（day 3 set53） | day 3 | 零觸發——day 3 已經有 loc 事件，唔需要保底 |
| F 首 7 日強制日封 tick（morning 次序） | **3 單**（day 7 day09、day 10 day20、day 22 set35） | **day 7** | **派 day7:day09，播出 day 7** |
| E day 4 pending 播唔出→過期→保底補派（morning 次序；頭 7 日零入場＋day 4／5／6 強制日） | **3 單**（day 7 day09、day 10 day20、day 22 set35） | **day 7** | **派 day7:day09，播出 day 7** |

- 預期兌現：**首單一定 ≤ day 7**（保底兜底），**30 日約 2–3 單**（R 3／S0 2／F 3／E 3）。
- 保底識別方法（唔靠估）：tick 之後 pending 係新設、當日日骰擲唔中、設嗰陣 seen 空——三樣齊先記做保底派單。
- 唔會提早抽乾：三年 A 路線 **81 單，81 唔同／113，尾單 day 1075**——保底喺 A 路線零觸發；就算觸發，最多加一單（保底只係提前消耗一單 once-only 池事件，唔加任何概率；三年總數由擲骰次數決定，唔係由保底決定）。

### 實駕結果（`qa206/drive206.py`，本地鏡像 port 8996，live 模式，fresh 局；報告 `qa206/drive206_report.json`，截圖 `qa206/shots206/`）

- T 逐日（每日 2 地點＋「過一日」）＋W 成週跳日（每日 2 地點＋「開始今日行程」）：**兩條路線收斂做同一條**——同一日只會見到同一粒推進掣（地圖日「過一日」，行程日「開始今日行程」），行出同一條路徑、同一組數字。W 係 T 嘅重現，唔係獨立路線。
- **2／30 日，全部唔同**。首單真實開火 **day 4**（`wf4_ev_day25`「大排檔嗰張長枱」，`pendingDay=4`——正常日骰，唔係保底），第二單 **day 10**（`wf4_ev_day18`「街市魚檔嗰斤蝦」，`pendingDay=10`，正常日骰）。首單 ≤ day 7 ✓，2–3 單 ✓。
- **保底今次冇觸發**（day 4 已經有事件，唔需要保底）——保底開火由 sim F／E＋logic 測試證實，唔係由呢次實駕證實。
- 量度註：drive 嘅事件 stamp 寫 day 7 係 artifact（一次推進食咗幾日先 drain）；開火日以 `lastDay`／`pendingDay` 為準（day 4／day 10）。
- 實玩 2 單 vs sim R 3 單：sim 假設由 day 3 起每日入 2 地點；實玩行程日唔入場，day 3 嗰次入場實際落喺 modal 處理期間、日數已經行前咗，loc 骰唔係 sim 嗰個組合——路線 fidelity 差距，唔係機制問題。Sim S0（零入場）2 單同實玩 2 單吻合。
- 0 pageerror，0 http fail。

### 新測試＋反證

新檔 `tests/test_wf4_206c1_logic.js`（**30 項 ALL PASS**）＋`tests/test_wf4_206c1_static.py`（**22 項 ALL PASS**）：

- Logic：CFG（pityDay 7、頻率唔郁、池 113）；`wf4SeenAny` 五態（fresh／`__n`／舊 save `__n=0`／`__n` undefined／空）；day 7 觸發（pendingDay 7、day 事件、未直接 fire——seen 仲係空）；day 7 之前唔觸發（day 0／1／2／3／5／6；day 4 正常擲中做對照）；見過唔觸發（新 save `__n`＋舊 save 得 `seen[id]` 兩種）；只觸發一次（晨鏈播完之後 day 8／9／11／12 零 pending）；有 pending 唔覆蓋；base 唔 ok 唔觸發（結局鎖／強制日／病日）＋day 7 撞強制日、day 8 一解封即刻補觸發；pityDay 跟 CFG 行（改做 9 就 day 9 先觸發）；pick 合資格。關鍵種子事實：day 7／8／9 日骰全部擲唔中，出 pending 一定係保底。
- Static：CFG pityDay:7＋頻率唔郁；`wf4SeenAny` 兩邊計；保底位置（`wf4BaseOk()` 守衛之後、概率擲骰之前）；入 pending、唔直接 fire（`wf4DailyTick` 入面零 `wf4Fire`）；原有擲骰＋pending 守衛仲喺度；池 113 唔郁。
- **反證**（pristine main `9e338d6`，`/tmp/pristine206c1.html`）：logic **FAIL 14**、static **FAIL 8**，乾淨（PASS 嗰啲係應然不變嘅守衛／舊行為）。
- 附帶修復（唔修會靜默死）：`test_wf4_203_logic.js` 同 `test_wf4_193_logic.js` 抽函數清單冇 `wf4SeenAny`——佢哋 eval 嘅 `wf4DailyTick` 喺 day ≥7 嗰陣 call 唔到 helper，入 try/catch 靜默死咗（203 嗰個 A／C／D 30 日計數即刻跌）。已補抽取＋fallback stub（pristine 行為不變）。
- 附帶 resync：`index.html` 淨 **+22 行**（WF4 區頭註解＋3／`wf4SeenAny`＋10／保底檢查＋9），釘死行號嘅 5 份測試（gift185／rom176／tang171／tang173／travel114）全部漂移。`qa206/resync206.py` difflib 核實：三段改動全部喺舊 L41497 之前，淨 +22，53 處釘位內容逐字相同；已按慣例更新釘位（總行數 61400→61422、openLoc DEF 55872→55894、WRAPPER 45135→45157 等）＋補 resync 註解。

### 全套 A/B（`qa131/run_suite.sh <repo-root> <outfile>`，兩個參數齊）

- 工作版：**TOTAL PASS 288 FAIL 13**（301 檔；輸出 `qa206/suite_work.txt`）。
- Pristine 對照（實體 worktree `~/workspace/tmp-pristine206c1`，main `9e338d6`）：**TOTAL PASS 287 FAIL 13**（300 檔；輸出 `qa206/suite_pristine.txt`）。
- **零回歸**：`comm` 比對 FAIL 清單，work-only／pristine-only 皆為空——13 項逐項相同（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），全部係 pre-existing，同 v203／v204 落地嗰陣同一集合。工作版 PASS 多 1 項係淨數：分支多 B1＋C1 共 3 個新測試，main 多 v204 嗰 2 個（288＝287−2＋3）。
- 基準說明：B1 嗰陣工作版 286／13（基底 v203）；而家 288／13 係 286＋2 C1 新測試。

### 改動總覽

`index.html` 淨 +22 行：`WF4_CFG` 加 `pityDay:7`＋區頭註解 3 行、`wf4SeenAny()` 10 行、`wf4DailyTick` 保底檢查 9 行。
新檔：`tests/test_wf4_206c1_logic.js`、`tests/test_wf4_206c1_static.py`、`qa206/sim_wf4.js`（＋`sim_output.txt`）、`qa206/resync206.py`、`qa206/drive206.py`（＋`drive206_report.json`、`shots206/` 4 張截圖）、`NOTES_V20A206.md` §6。
改動測試檔：`tests/test_wf4_203_logic.js`、`tests/test_wf4_193_logic.js`（補抽 `wf4SeenAny`）、`tests/test_gift185_static.py`、`tests/test_rom176_static.py`、`tests/test_tang171_static.py`、`tests/test_tang173_static.py`、`tests/test_travel114_static.py`（＋22 行 resync 釘位）。

### 殘留／跟進（唔喺呢票）

- 保底喺正常 fresh 實玩未觸發過（種子日骰 day 4 已經派事件）——保底係兜底，唔係主路徑；要喺實玩見到保底開火，要撞正首週強制／病日封 tick 或者 pending 過期嗰啲局，唔使刻意追。
- T／W 收斂：drive 兩個模式實際同一條路線；以後要分開兩條路線，要改 drive 喺行程日唔跟 modal 鏈自動跑（例如每次推進後強制返地圖），唔係呢票。
- Pristine worktree `~/workspace/tmp-pristine206c1` 用完即清（唔留大檔）。

## 7. C2：7 單錯配場景圖再重映射＋全面掃描追加 2 單

分支 `v20a206`，基底 main `165597e`（v203 落地）＋B1 commit `60f16b5`＋C1 commit `b25c6d0`。**只做 C2，唔掂 B1／C1。只做實作＋驗證，唔落地。**
PixelLab 花費：**0 次**——只用現有資產重映射，零新生成。

### 揀圖方法

每單揀圖之前先用 `muse.read` 睇候選圖本身，唔係靠檔名估。核實咗：
`bg_wf4_market.jpg` 係日頭街市街景（檔口帶：菜／魚／雜貨，banner 75% 裁切位見簷篷＋檔口）；
`bg_loc_rec_hk.jpg` 係唱片舖內景本身（黑膠架＋試聽間＋咪）；`bg_loc_rec_star.jpg` 係唱片公司會客室（金唱片＋梳化）、
`bg_loc_rec_wanchai.jpg` 係錄音室控制室（混音台＋錄音間），兩者都唔係舖頭；
`bg_loc_tvb_kowloon.jpg` 係電視台辦公室（成牆電視＋打字機＋枱面成疊信件＋佈告板）；
`bg_loc_tvb_longmen.jpg` 係電視台走廊（佈告板＋門＋手推車）、`bg_loc_tvb_harbour.jpg` 係電視台大堂（錄音間＋露台海景），
兩者都冇「執信」元素；`bg_loc_film_harbour.jpg` 係片廠室內、窗外維港＋船（banner center 裁切帶正正係窗＋海＋船，菲林罐喺裁切帶下面）。

### 7 單重映射（舊圖→新圖＋理由）

| 單 | 場景 | 舊圖（錯） | 新圖 | 理由 |
|---|---|---|---|---|
| day07 | 電車上面 | `bg_wf4_taxi.jpg`（的士＋747＋啟德跑道燈，一眼認到的士） | `bg_wf4_market.jpg` | 中性街景頂住；冇電車圖，唔再用特徵太強嘅的士圖扮第二樣嘢 |
| day09 | 唱片舖 | `bg_loc_gift_shop.jpg`（廟街夜市手袋檔） | `bg_loc_rec_hk.jpg` | 唱片舖內景本身：黑膠架＋試聽間，唔係中性頂住，係啱圖 |
| st17 | 樓下士多 | `bg_loc_gift_shop.jpg`（同一張夜市檔圖） | `bg_wf4_market.jpg` | 街市街景，士多式檔口帶，近過遊客夜市 |
| day19 | 公園晨運 | `bg_wf4_home.jpg`（屋企客廳：電視＋雪櫃＋門） | `bg_wf4_market.jpg` | 戶外公共空間頂住；冇公園圖，街景係最中性嘅戶外圖 |
| day22 | 地鐵站賣唱 | `bg_wf4_taxi.jpg`（的士＋747） | `bg_wf4_market.jpg` | 中性街市街景頂住；冇地鐵站圖 |
| day24 | 電視台信件房 | `bg_wf4_home.jpg`（屋企客廳） | `bg_loc_tvb_kowloon.jpg` | 電視台辦公室內景：枱面成疊信件＋佈告板，啱「執信」；longmen 走廊／harbour 大堂冇信件元素 |
| day27 | 海邊散步 | `bg_wf4_taxi.jpg`（的士夜景） | `bg_loc_film_harbour.jpg` | 海港景：banner 見窗外維港＋船，啱黃昏海邊 |

之後：`bg_loc_gift_shop.jpg` 淨返 day20／day21（唔再一圖四用，嗰兩單 review 話勉強可接受，唔郁）；
`bg_wf4_taxi.jpg` 淨返 st08／st15／day26（全部的士／車廂感，review 話 day26 勉強可接受，唔郁）；
`bg_wf4_market.jpg` 一圖 15 用（原 11＋今次 4 單）——通用街景，任務指明「冇啱圖就寧願用 market 呢啲較中性嘅圖頂住」；
`bg_loc_film_harbour.jpg` 一圖 3 用（day10／st13／day27，全部海主題，同 cafe_cha 一圖三用 day05／11／15 同級）。

### 全面掃描（48 行逐單文案 vs 圖，review 冇點名嘅再執到 2 單）

逐單對過成個覆寫表 48 行（文案 beats＋setting 對圖本身）。除咗上面 7 單，仲有 2 單明顯錯配，一併修埋：

- **day10 巴士上層望住個海**（`bg_wf4_taxi.jpg` → `bg_loc_film_harbour.jpg`）：文案重點係「望住個海」，的士圖係 747＋跑道燈，零海景；海港圖 banner 正正係維港＋船。day26 巴士站留返的士圖（review 話車廂感勉強可接受；day26 文案冇提海）。
- **st13 渡輪上面嗰陣海風**（`bg_wf4_taxi.jpg` → `bg_loc_film_harbour.jpg`）：文案係渡輪望兩岸樓＋海風，的士圖零海；海港圖啱「海＋兩岸」。

其餘 39 行掃過無其他明顯錯配（留低嘅勉強項全部有原因，唔郁）：
home 組（home01–04／day01／day08 天台晾衫／day16 天台數星／day17／day28）——天台兩單係屋企範圍延伸，冇天台圖，home 已經係最中性；
booth 組（st01–03／day02／day13）電話亭啱；market 組（st06 魚檔／st07 LD舖／st11 大排檔／day03 士多罐頭／day04 涼茶舖／day06 大排檔／day12 街市／st12 廟街夜市／day18 街市／day23 雨天街角／day25 大排檔）街市／街景啱或中性可接受；
karaoke 組（st05／st14）啱；taxi 餘下（st08 的士／st15 的士／day26 巴士站）啱或勉強可接受；
cafe_cha（st04 冰室／day05 冰室／day11 茶樓／day15 茶餐廳）review 話修好／可接受；film_lion（set08 派錯更去錯廠／day14 片場休息區）啱；
gift 餘下（day20 舊書攤／day21 洗衣舖）review 話勉強可接受，唔郁。

### 逐單截圖證據（`qa206/drive206c2.py`，本地鏡像 port 8997，live 模式，pending-seed 即彈）

9／9 ok（標題＋場景圖 URL 全部啱預期），0 pageerror、0 http fail。報告 `qa206/drive206c2_report.json`，截圖 `qa206/shots206c2/`：

| 單 | seed 日 | 截圖目視 |
|---|---|---|
| day07 | 10 | 街市檔口帶，冇的士／747 ✓ |
| day09 | 11 | 黑膠架＋試聽間，唱片舖本身 ✓ |
| st17 | 12 | 街市街景，士多式檔口 ✓ |
| day19 | 13 | 戶外街市街景，唔再係客廳 ✓ |
| day22 | 14 | 街市街景，唔再係的士 ✓ |
| day24 | 731（cond yearMin:1992） | 成牆電視＋枱面信件，電視台辦公室 ✓ |
| day27 | 15 | 窗外維港＋船 ✓（banner 左緣見少少佈告板，片廠室內殘留，唔影響海港主讀） |
| day10 | 16 | 窗外維港＋船，「望住個海」✓ |
| st13 | 17 | 窗外維港＋船，渡輪望海 ✓ |

載入日全部避開頒獎日（100／365／730）；day24 用 731 滿足 yearMin:1992。典禮等待照 review R1B 手法（見 `.awd62-stage` 就等）。
探針時序 artifact（同 review R1B §4 同類，唔係遊戲 bug）：day09／day19／day22／day10 四張截圖頂部見到「行程已定」週計劃卡殘留、day24 嗰張頂部見到「星河台慶・年度頒獎夜・結果」卡殘留——截圖嗰刻晨鏈仲過渡緊，WF4 modal 本身完整正確；正常行鏈 WF4 彈出嗰刻得 1 個 modal（review R1D2 已證）。

### 新測試＋反證

冇開新測試檔——期望入咗三份現有測試（任務指明 `test_ui134_wf4scene_static.py` 為主）：

- `tests/test_ui134_wf4scene_static.py`（v20a206 C2 新 block，13 項）：9 單重映射逐單釘死＋gift 淨返 day20／21＋taxi 淨返 st08／st15／day26＋home 唔再配 day19／day24＋review 話可接受／勉強嗰 7 單（day11／20／21／23／25／26／28）唔郁。
- `tests/test_wf4_203_static.py`（C2 期望更新＋v206 block，9 項）：7 單舊期望改新值（day07→market、day09→rec_hk、st17→market）＋day19／22／24／27／day10／st13 新期望＋gift／taxi 用途集合＋7 單舊錯圖唔再出現。
- `tests/test_wf4_203_logic.js`（C2 期望更新，`wf4Scene105` 實讀）：day07／day09／st17／day19／22／24／27／day10／st13 逐單斷言＋`expectNew` 12 單新 day 地圖更新＋gift 淨返 day20／21。唔更新呢兩份，佢哋會釘死舊 v203 映射而 FAIL——呢個係期望更新，唔係測試放水。
- 三份全部 TOTAL／ALL PASS（見下）。

**反證**（pristine main `a426947`，v203 舊映射）：ui134 嘅 v206 block 會 FAIL 13 項（9 單映射＋gift／taxi／home／唔郁 4 項集合斷言）；203 static／logic 嘅 C2 期望會 FAIL（day07／day09／st17／day19／22／24／27／day10／st13 共 9 單舊值）。新期望只喺重映射後嘅工作版成立。

### 附帶 resync（淨 +3 行漂移，唔係 C2 本身，係表頭註解加咗 3 行）

`index.html` 61422→**61425 行**（淨 +3：覆寫表頭註解加 v20a206 C2 三行；9 行重映射原位替換，淨 0）。頭一版全套即刻多 6 項 FAIL
（gift185／rom176／tang171／tang173／travel114／scene104）——全部係釘行漂移／計數，唔係回歸：
`qa206/resync206c2.py` difflib 核實 PASS——非 equal 段全部喺舊 L41269–41322（表頭＋覆寫表）之內，
9 個 replace（1 個＋3＋8 個淨 0，合共 9 行換圖），53 處釘位內容逐字相同，`?v=20a104` 26→29 處。
跟住更新 6 份測試嘅釘位／計數（慣例，同 C1 resync 一樣）：
gift185 總行數 61422→61425；rom176 4 處各 +3（54324→54327、54692→54695、55831→55834、55925→55928）；
tang171／tang173 總行數＋DEF 55894→55897；travel114 COUNT／FREE 兩個 set 入面＞41271 者各 +3（DEF 55894→55897、WRAPPER 45157→45160，歷史註解唔郁）；
scene104 `?v=20a104` 26→29（WF4 覆寫表重用 10→13：v134 2＋v203 8＋v206 淨 +3——rec_hk 1＋tvb_kowloon 1＋film_harbour 3 減 gift 2）。
6 份重跑全部 PASS。

### 全套 A/B（`qa131/run_suite.sh <repo-root> <outfile>`，兩個參數齊）

- 工作版：**TOTAL PASS 288 FAIL 13**（301 檔；輸出 `qa206/suite_work_c2.txt`）。
- Pristine 對照（實體 worktree `~/workspace/tmp-pristine206c2`，main `a426947`＝v205 落地）：**TOTAL PASS 287 FAIL 13**
  （300 檔；輸出 `qa206/suite_pristine_c2.txt`）。
- **零回歸**：`comm` 比對 FAIL 清單，work-only／pristine-only 皆為空——13 項逐項相同
  （flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／
  weave43／weave44／weave49／wf5_87／wrap38），全部係 pre-existing，同 v203／v204／v205 落地嗰陣同一集合。
  工作版 PASS 多 1 項係淨數：分支多 B1＋C1 共 3 個新測試，main 多 v204 嗰 2 個（288＝287−2＋3）；C2 冇開新測試檔。
- 基準說明：任務講嘅基線 v203 係 285／13；C1 嗰陣工作版 288／13（基底 v203＋B1＋C1）；今次工作版 288／13 同 C1 一致，
  pristine 287／13 同 C1 嗰陣 main `9e338d6` 一致（v205 冇加新測試檔）。

### 改動總覽

`index.html` 淨 +3 行：覆寫表頭註解＋3 行＋9 行原位換圖（淨 0）。
改動測試檔 9 份：`tests/test_ui134_wf4scene_static.py`、`tests/test_wf4_203_static.py`、`tests/test_wf4_203_logic.js`
（C2 期望）＋`tests/test_gift185_static.py`、`tests/test_rom176_static.py`、`tests/test_scene104_static.py`、
`tests/test_tang171_static.py`、`tests/test_tang173_static.py`、`tests/test_travel114_static.py`（＋3 行 resync）。
新檔：`qa206/drive206c2.py`（＋`drive206c2_report.json`、`shots206c2/` 9 張截圖）、`qa206/resync206c2.py`、
`qa206/suite_work_c2.txt`、`qa206/suite_pristine_c2.txt`。
唔掂：B1 文案、`tests/test_wf4_206_static.py`、C1 機制、事件文案／fx／任何 code。

### 殘留／跟進（唔喺呢票）

- 下一批新圖優先補電車／唱片舖／士多／公園／地鐵站／海邊／信件房 7 個場景（review C2 修法方向；今次只係用現有圖頂住，
  day07／day19／day22 嗰三單尤其係「中性街景頂住」唔係啱圖；film_harbour banner 左緣有佈告板殘留）。
  參照相先行，跟場景圖硬規矩——NOTES_V20A203 §4 已經排咗頭 4 個（冰室／電車／茶樓／唱片舖），呢度加埋後 3 個（公園／地鐵站／海邊／信件房計 4 個，連士多共 7 個）。
- `bg_wf4_market.jpg` 而家一圖 15 用——通用街景頂住嘅代價，新圖補齊之後應該逐單換返啱圖。
- Pristine worktree `~/workspace/tmp-pristine206c2` 用完即清（唔留大檔）。

## 8. Rebase 上 main a426947（v205）＋重驗紀錄（落地統籌）

分支基底由 main `3768c90`（v203）rebase 上 `a426947`（v205 落地）。`index.html` diff 內容逐字不變
（前後 diff ±行 sort 後 md5 一致，155 行；`pityDay`／`wf4SeenAny`／`v20a206 C2` 全部在位）。

### Rebase 衝突：兩輪，全部純行號漂移

- **C1 commit（`b25c6d0`）**：5 份 static 測試（gift185／rom176／tang171／tang173／travel114）衝突——
  v204 亦 resync 過同一批（總行數 61400→61432，v204 +32）。解法：逐個錨點按公式
  `rebased = HEAD + (v206 − v203)` 重算，再逐行 grep 核實內容（例如 rom176：54302→54356、
  54670→54724、55809→55863、55903→55957；travel114 COUNT／FREE／DEF 55926／WRAPPER 45158；
  總行數 61454）。一度寫錯 `count('\\n')`（雙斜槓，total 斷言 FAIL），已修正，5 份全部 PASS 後先繼續。
- **C2 commit（`8b30101`）**：同一批 5 份衝突——C2 覆寫表頭註解 +3 行（插入點 ~L41271，之後者各 +3）。
  總行數 61457；DEF 55929／WRAPPER 45161；rom176 54359／54727／55866／55960；travel114
  COUNT／FREE 按段 +0／+3 重算，逐行 grep 核實（39583 不變、41535／44592 係 +3 後嘅值）。5 份全部 PASS 後先繼續。
- Rebase 後分支 HEAD `8f1f37f`（B1 `5970165` → C1 `4f9d6c6` → C2 `8f1f37f`）。

### 重驗（rebase 後最終樹）

- 相關測試逐個重跑，全部 PASS：`test_wf4_206_static.py`、`test_wf4_206c1_logic.js`、
  `test_wf4_206c1_static.py`、`test_ui134_wf4scene_static.py`、`test_wf4_203_static.py`、
  `test_wf4_203_logic.js`、`test_wf4_193_logic.js`、`test_scene104_static.py`、
  `test_gift185_static.py`、`test_rom176_static.py`、`test_tang171_static.py`、
  `test_tang173_static.py`、`test_travel114_static.py`。
- **全套 A/B**（`qa131/run_suite.sh`，兩個參數齊；輸出 `qa206/suite_work_rebase.txt`／
  `qa206/suite_pristine_rebase.txt`）：工作版 **TOTAL PASS 290 FAIL 13**、pristine（main `a426947`
  worktree `~/workspace/tmp-pristine206`）**TOTAL PASS 287 FAIL 13**；`comm` 比對 FAIL 清單，
  work-only／pristine-only 皆為空——13 項逐項相同，全部係 pre-existing（同 v203／v204／v205 同一集合）。
  工作版 PASS 多 3 項就係 3 個新 v206 測試。**零回歸**。
  （教訓：pristine 嗰次 outfile 用相對路徑 `qa206/...` 會 fail——main 根本冇 `qa206/` 目錄；
  改用絕對路徑先寫到。第一次跑嘅 work 290／13 不變，pristine 重跑 287／13。）
- **實駕重跑**（本地鏡像，live 模式；rebase 後最終樹）：
  - C1 `qa206/drive206.py`（exit 0）：T＋W 兩條路線收斂，全部 **2／30 日、唔同**——首單 day 4
    `wf4_ev_day25`「大排檔嗰張長枱」（pendingDay=4，正常日骰，唔係保底）、第二單 day 10
    `wf4_ev_day18`「街市魚檔嗰斤蝦」（pendingDay=10）；pendingDay=4 證實 day 4 有 tick
    （v203 §14 殘留觀察繼續證偽）；0 pageerror、0 http fail。結果同 rebase 前逐字一致。
  - C2 `qa206/drive206c2.py`（exit 0）：**9／9 ok**（標題＋場景圖 URL 全部啱預期），0 pageerror、0 http fail。
    day24 新標題「電視台嗰封冇名信」＋tvb_kowloon 辦公室圖已上台。
  - B1 新 probe `qa206/probe206b1.py`（exit 0）：seed set32／set35，**2／2 ok**——新標題
    「外景小巴嗰個暈車」＋beat「暈車」、「海邊嗰場晨戲」＋beat「潮水一路漲」全部上台；
    0 pageerror、0 http fail。截圖 `qa206/shots206b1/`。
- Pristine worktree `~/workspace/tmp-pristine206` 落地後即清（唔留大檔）。

## 9. 落地紀錄（v20a206 上線）

- 遊戲 commit `8b5c460`（squash merge `v20a206`，4 粒分支 commit：B1 `5970165` → C1 `4f9d6c6` → C2 `8f1f37f` → rebase 重驗 `1fc1f74`）。
- 線上親自 curl 核實：`index.html` 5,455,174 bytes，sha256 `bff57aeb7ed26671…`，同 repo HEAD 逐字一致。
- 全套 A/B（rebase 後最終樹）：工作版 290／13 vs pristine main `a426947` 287／13，FAIL 清單逐項相同，零回歸。
- 實駕重跑（rebase 後最終樹）：C1 drive T＋W 全部 2／30（首單 day 4、次單 day 10）、C2 drive 9／9、B1 probe 2／2；0 pageerror、0 http fail。
- 工作副本 `linji-work206`＋pristine worktree `tmp-pristine206` 落地＋review 完即清；分支 `v20a206` 留喺常駐 clone（`1fc1f74`）。
