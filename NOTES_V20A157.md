# NOTES_V20A157 — 主線重整實裝（v20a157）

- 分支：`v20a157`，基於 main `e08a070`（v148）
- 工作副本：`~/workspace/linji-work157/`
- 設計來源：`~/workspace/linji-story-restructure/index.html`（N1–N17＋F4／G4）
- 分析目錄：`~/workspace/linji-work157-analysis/`（`SCOUT.md`／`MANIFEST.md`／`ERA.md`／`RIPPLE.md`／`AUDIT_FIX.md`／`fragments/`）
- 性質：主線 C1–C17 全幕重寫（文案＋標題＋synopsis），機制（閘／旗／stats／tags／ripple／locId／pacing）全部唔郁；另 C18／C19 輕微潤色（10 句承諾字眼）、F4／G4 新寫。
- 唔改：SAVE key `starVolunteer_map_v19w`、softRev `s107`、產品 `?v=`（`v20a10`）。

## §0 整合方法（splice 核實）

- 8 份 fragment 用 `/tmp/splice157.py` 逐表 splice（`STORY_SPINE_NODES_C6`／`BR89`／`1989`／`1990`／`STORY_SPINE_NODE_C17_410`／`CHOICE47_NODES.F4_stay_mind`／`G4_family_job`／`STORY_SPINE_NODES_WF1`），另 `ERA_M39_M22.js` 按其檔頭 manifest 執行 M39／M22 修正。
- splice 前：8 個 live 段行號對位核實＋`node --check` 全過；invariant diff（live vs fragment）只得預期差異（beats／resultBeats 數、G4 標題）。
- splice 後：逐表重新抽出再對 fragment，**實質 0 diff**（10 處字面差異全部係 NOTES 已記錄嘅刻意改寫：C6 Q1×1、C11×2、C17 synopsis×1、F4 M39×6；恢復統籌獨立再核實見 `qa131/SUITE3_AB.md` §1）；全檔 inline script `node --check` 過。
- splice bug：第一版 F4 後多咗 `},,`（live 尾逗號未食走），已直接修 index.html＋patch 咗 `/tmp/splice157.py`。
- F4／G4 格式：fragment 用鬆散格式（`id: "..."`），live CHOICE47 用緊湊格式——已 normalize 做 live 格式，否則 weave47 字串匹配會斷。
- 總改動：index.html 淨 ＋7,332 字元（splice）＋ C17 synopsis 第 2 段改寫（見 §1.7）；`content/story_detail_c1_to_c17.json` nodes[0–4]（C1–C5 pack 組）。

## §1 逐章改動對照

### 1.1 C1–C5（pack 組，`content/story_detail_c1_to_c17.json` nodes[0–4]）

- N1–N5 全幕重寫（設計稿 N1–N5），beats／choices／flags／stats／ripple 逐值對照 live——機制唔郁。
- 關鍵：C1 兩條路旗 `route_tv`／`route_film`；C2 標籤沉澱（`片場老油條`／`電視城乖仔`）＋報紙旗 `flag_network_stay`／`flag_hustle_board`；C3 高俊傑對立 `rival_gao_hard`／`rival_gao_endure`（決戰門檻 ±6，見 AUDIT_FIX §4.2）；C4_b「捱得」標籤經 registry 真・加信用 ＋2（RIPPLE §1.2，SCOUT 漏咗）；C5 三個裸名旗 `choi_honest`／`choi_spin`／`choi_dodge`（alias 斷裂，見 §7）。
- C2 閘「完成 3 次基礎通告」實現已核實（AUDIT_FIX §4.1）：stub trigger `gigCountMin:3`＋C1 done＋第 4 週起＋電視城／茶餐廳＋聽過 `tvb_rules_gossip`，計數器 `S.story.gigCount`（任何通告殺青都計）。

### 1.2 C6《角落嗰張枱》（舊：飯堂閒角）

- 標題改做「角落嗰張枱」；10 beats；synopsis／beats 重寫（N6）。
- ERA §1 修正落地：簽約形式「一簽一季，月月有糧」改寫——臨記／特約唔同電視台簽約、按日出現金；「月月有糧」只屬於經理人約藝員或全職臨記同 agent 簽底薪。fragment Beat 5 嘅引擎術語「N1 嗰條 route 旗」改做玩家面「第一日嗰個選擇」（Q1）。
- 閘不變：route_tv＋weekMin 15。

### 1.3 C6F（BR89，片場跟班）

- 8 beats；N6F 重寫。
- **Q2／Q3 outstanding**：昌叔題眼句「跟過三期戲，等嘅唔係近鏡，係一個名」跟設計稿刪咗（用戶未拍板，唔擅自救返），見 §7。

### 1.4 1989 表：C7／C11／C8／C9／C10

| 章 | beats | 重點 |
|---|---|---|
| C7《暴雨救場》 | 9 | 「黑雨」→「暴雨」全檔清零（另見 §1.8）；台風／救場線 |
| C11《選美後台》 | 9 | ERA §2：場務段降級做口頭提點——「唔係規矩，係呢度嘅做法。司儀企位唔好亂企，燈光就位嗰陣唔好行過」；「司儀企正中嗰塊板，燈一熄，邊個都唔准過界」刪走（查無來源，唔硬寫）；synopsis「後台規矩只有一句」→「後台得一句口頭提點」 |
| C8《茶餐廳度橋》 | 10（唔係設計稿嘅 8；多講者段落逐講者拆開所致） | |
| C9《年尾追數》 | 9 | 第三選項 `C9_c` 寫 `flag_mediate_gu_debt`（幫顧明輝爭取分期，語義唔可以改做還錢／借錢——兩處巧遇讀取文案都係講「爭取分期」） |
| C10《戲路定型》 | 8 | |

- 閘不變：C11 需 C7；C7／C11／C8／C9／C10 其餘閘不變。

### 1.5 1990 表：C15／C14／C12／C16／C13

| 章 | beats | 重點 |
|---|---|---|
| C15《高危替身》 | 7（v136 嗰陣 ≥8；v157 設計稿拍數） | 傷唔係勳章係帳；閘：需 C10＋動作標籤 |
| C14《站隊》 | 9 | 挖角潮降溫（ERA §3）：「白熱化」刪走，改做餘波／反挖角；第三選項 `C14_c` 寫 `flag_side_undecided` |
| C12《樂壇前哨》 | 12 | K 房句照用；M30 核實正確（ERA §4） |
| C16《偶像實力之爭》 | 7（v136 嗰陣 ≥8） | 修音 vs 苦練對立保留（`flag_vocal_polish`／`flag_vocal_train`，唔可以對調——程天諾兩段對白按呢個對立寫）；閘不變 |
| C13《賀歲片》 | 7（v136 嗰陣 ≥8） | 未揭盅口徑（出年年初一先上畫／票房要等出年先知）；關海媚名可出玩家面（v151 拎走禁令），但 pack C13 喺 live registry 俾 inline 主幹遮住（見 §7） |

- 閘不變：C15 需 C10；C17 需 C13（見 §1.7）。

### 1.6 C18／C19（WF1 表，輕微潤色 B1–B10）

- 主題／時間／人物／閘／旗／stats 全部唔郁；淨改 10 句扮有後續嘅承諾字眼（AUDIT_FIX §5.4）：
  - B1–B3：C18 何生「來年點排你啲工」「帶你入多啲崗位睇」→立場句（引擎從來唔兌現，無通告池讀 `flag_wf1_*`）。
  - B4：C18_a notes「將你個名寫低」→「呢句，佢記住，你自己都要記住」。
  - B5–B6：C18 `nodeRipple`／`aftermathHint` 刪「第日點收科唔同」「來年啲工就會點排」。
  - B7–B10：C19_a notes／resultBeats「圈低你個名」「下次有穩陣位，嗌佢先」「名單上一個圈」→自我確認／企得穩。
- 閘不變：C18 需 C5＋weekMin 48（1990-12-01）；C19 需 C18＋weekMin 61（1991-03-01）。
- 年份字串照舊寫舊曆（`when:"1988冬"`／`"1989春"`），運行時 `years66Walk` ＋2 變 1990 冬／1991 春，唔係穿幫。

### 1.7 C17《收科嗰晚》（`STORY_SPINE_NODE_C17_410`，15 beats）

- 場景改做星河電視台會議室（setting／playerOffer／playerHint／lockedHint／`STORY_HINT_SOFT.C17` 全部「後台」→「會議室」）。
- 時間：1990 年冬末、冬台慶啱啱完、彩紙仲喺走廊掃唔切；synopsis 第 1 段「頒獎禮之後嗰晚」＋第 2 段講明今晚唔係頒獎禮之前、係收科嗰晚。
- **整合員追加修正**：fragment synopsis 第 2 段本身有 DEV 註解（「舊版文案寫『頒獎禮前夕、開場之前』……重寫將時間改返做……」）——synopsis 會經 DengLine／soft stub 上玩家面，唔可以留 DEV  meta。已改寫做玩家安全寫法：「冬台慶啱啱完——獎已經頒完，結果已經有咗。今晚唔係頒獎禮之前，係收科嗰晚……」。「頒獎禮前夕」而家全 node 只剩 1 處：何生對白否定句「唔係頒獎禮前夕——獎已經頒完」（刻意保留嘅對照句）；「開場之前」／「試咪」全 node 零命中。
- 閘不變：weekMin 153＋yearEq 1992＋needDone C13＋`awardResolved`（1992 屆冬台慶要有結果）＋backstop day 1096（1993-01-01 前一日，無條件開）。
- 靜態 choices（`C17_410_a`／`C17_410_b`，ending410Key `natural`／`quit_job`）同 v136 fixture 逐字一致；動態重建（`ending410EveNode`／`endingEveOptions410`）接駁在位。
- M22 台灣資金句照用（ERA §6 核實正確：台灣資金確係主要水喉，唔寫死精確百分比；「1992 尾收水」只寫風聲正確）；錨點註尾句已改（見 ERA_M39_M22.js manifest）。
- M39「一成」刪走（ERA §5：無可靠來源，且同長期估計約三成至一半回流不符）。

### 1.8 F4／G4（CHOICE47）

- F4 `F4_stay_mind`《何生問：走定留》：4 beats，3 抉擇各 3 resultBeats（9）。M39 趨勢句 6 處（3 beats＋3 notes 短版）由「呢年開始，都有人返嚟喇」改做「間中都會聽到，邊個邊個攞咗居留，又返嚟搵食」（零星傳聞口吻，ERA §5）。
- G4 `G4_family_job`《阿媽煲咗湯》：4 beats，G4_a 2 resultBeats、G4_b 4 resultBeats（合共 6）。**卡片標題硬編碼問題**：`choice47FamilyCardHtml` 寫死「屋企有話同你講」，唔跟節點新標題變——留返唔郁，見 §7。
- **G4 decline 旗接線另開票**：`flag_family_job_decline` 寫入點＋結局回望＋防重播已在位（見 §2）；設計稿 N17 話 decline 旗要喺結局去留段落出「主動留低」版——`endingExodusScene410` 唔讀呢支旗，呢半未兌現，另開票處理。
- **F4 第三選項純對白**：F4 第三選項係純對白（無旗／無數值），見 §7。

### 1.9 其餘細項（整合員順手做）

- Q4：`endingInserts410`「嗰季閒角」→「嗰排閒角」（同 C6「一季」修正一致）。
- 「黑雨」全檔清零：C7 node 之外三處（`STORY_HINT_SOFT.C7` hint、`STORY46_CREDIT_C7` 行、魏詠男巧遇行 L52242）由「黑雨」改「暴雨」。副作用：`test_weave46_static.py` 錨點字串要跟住改（見 §5）。
- `STORY_HINT_SOFT.C17`「後台」→「會議室」×2（見 §1.7）。

## §2 審計斷裂處理（11 支旗＋2 個 id）

來源：`~/workspace/linji-work157-analysis/AUDIT_FIX.md`（逐支 grep 全檔＋追到消費點）。**全部 11 支旗＋2 個 id 嘅寫入點（旗名／選項／stats／tags）喺重寫後原樣保留**；新測試 `test_story157_index_static.py`／`test_story157_pack_static.py` 逐支斷言旗名＋寫入選項在位。

### 2.1 真分支讀取（6 支）——已保住，重寫無斷

| # | 旗 | 寫入 | 讀取（強度） |
|---|---|---|---|
| 1 | `flag_mediate_gu_debt` | C9_c 第三選項 | 顧明輝巧遇兩處分版（`gu_loan` 前置句＋`gu_n10after` 開場句），中－強 |
| 2 | `flag_side_undecided` | C14_c 第三選項 | 齊鎮海 `chai_repay` 節拍閘 OR 四條件之一（另有 C14 done 後備路），中 |
| 3 | `flag_network_stay` | C2_a（pack） | 次日報紙 `story:C2:network`（聲望 ＋2），中－弱；讀取係 map 查 key——`STORY_FLAG_EVENT` 嗰兩行就係契約，刪咗報紙靜默停刊 |
| 4 | `flag_hustle_board` | C2_b（pack） | 次日報紙 `story:C2:hustle`（聲望 ＋1），中－弱 |
| 5 | `flag_vocal_train` | C16_b 苦練 | 程天諾 `ching_after_train`（7 句），中 |
| 6 | `flag_vocal_polish` | C16_a 修音 | 程天諾 `ching_after_polish`（7 句），中 |

### 2.2 弱讀取旗（5 支）——接受現狀，寫入 NOTES，唔加強

| # | 旗 | 寫入 | 唯一讀取 |
|---|---|---|---|
| 7 | `flag_wf1_studio_dream` | C18_a | ECHO89 回望第 18／23 位（上限 3 段，典型全程排唔到——結構性邊緣化） |
| 8 | `flag_wf1_steady_craft` | C18_b | ECHO89 回望第 19／23 位，同上 |
| 9 | `flag_wf1_gamble_observe` | C19_b | ECHO89 回望第 20／23 位，同上 |
| 10 | `flag_wf1_gamble_quiet` | C19_a | ECHO89 回望第 21／23 位，同上 |
| 11 | `flag_family_job_decline` | G4_b | 結局回望句保證出（屋企 block 四揀一，唔受 ECHO89 上限限制）＋G4 防重播；唔影響判定 |

- **接受現狀理由**（AUDIT_FIX §2.3）：v157 係重寫主線文案，唔係加系統；唔郁結局判定（設計稿開宗明義話不變）；C18／C19 抉擇性質係「表態」唔係「分叉」——新 spine 要求「純對白就寫明純對白，唔呃玩家」，而唔係將每個表態升級做真分支。緩解已做：B1–B10 刪走假承諾字眼（見 §1.6）。
- **如果用戶想加強（唔喺呢票，只列選項）**：S 級——ECHO89 上限 3→5，或將 wf1 四支調前到第 5–8 位；`flag_family_job_decline` 喺 `endingExodusScene410` 去留段落加一句「主動留低」版。M 級——`flag_wf1_studio_dream` 計入 `endingE3Eligible410` 做幕後資格半格（要改結局判定，必須另行拍板）；C18／C19 各開一個中段回收節拍。唔建議將 C18／C19 升級做真分支節點。

### 2.3 兩個 id——唔係旗，唔使處理

- `ching_after_train`／`ching_after_polish` 係 `ENC79_DIALOG` 程天諾對白腳本 key（各 7 句），唔係旗；真正嘅旗係 `flag_vocal_train`／`flag_vocal_polish`（見 §2.1）。重寫 C16 嗰陣唔好將對白 id 當旗名寫入 `effects.flags`。

### 2.4 SCOUT 勘誤（3 項，已寫入本 NOTES）

1. ECHO89 排位係 **18–21／23**，唔係 SCOUT 寫嘅 19–22／22（studio_dream 18、steady_craft 19、gamble_observe 20、gamble_quiet 21；全表 23 支）。
2. SCOUT §6.1「報紙模板渲染未完全核實」——今次已追通（見 §2.1 第 3／4 行：`STUB_NEWSPAPER_STORY_SOFT_v1.json` 兩個模板在位，`choiceFlag` 同旗名一致）。
3. 審計「零讀取」判詞喺 v20a86 之後已過時：v20a87 WF5（`enc87StoryFlag` 雙 store 讀）＋v20a89 BR89（`flag_family_job_decline` 回望讀取）逐支接返。WF5 之前 `ching_after_train`／`polish` 同 `chai_repay` 嘅 `flag_side_*` 真係死讀取（gate 讀 `S.flags`，C16／C14 寫入 `S.story.flags`）；而家已活。
4. 另：`flag_wf1_*` 喺典型全程「幾乎排唔到」比 SCOUT「好少出」更弱——係排位＋上限 3 段機制決定嘅結構性邊緣化，唔係隨機少見。

### 2.5 附錄核實（兩項都搵到）

- C2「完成 3 次基礎通告」閘：行 stub trigger（見 §1.1），`BehaviorGate.selfCheck` 邊界自檢齊（gigCount:3 過、2 唔過）。
- N3 rival 決戰門檻 ±6：`RIVAL_CFG`＋`rivalryWinThreshold`＋註解三方吻合——門檻 40；hard ＋6（46，激嬲對手更難贏）、endure −6（34）；重寫唔好寫反。贏：信用 ＋3＋報紙點名（聲望 ＋2）＋高俊傑好感 ＋3；輸：人氣 −1＋好感 −1。結局專屬段落 `endingCareerScene410` 有 hard／endure 兩版。

## §3 時代細節核實結果（ERA §1–§7）

來源：`~/workspace/linji-work157-analysis/ERA.md`（每項鎖定設計稿主張再 web research 查真實來源）。

| # | 項目 | 結論 | 實裝處理 |
|---|---|---|---|
| 1 | N6 簽約形式「一簽一季，月月有糧」 | 要修正 | 已改寫（見 §1.2）：臨記按日出現金、唔同電視台簽約 |
| 2 | N8 選美後台規矩 | 核實唔到 | 降級做口頭提點（見 §1.4）；司儀企位句刪走（查無來源） |
| 3 | N13 挖角潮延續到 1992 夏 | 要修正 | 「白熱化」刪走，改餘波／反挖角（1992 年已有重量級幕後回流 TVB） |
| 4 | M30 K 房首間年份 | 核實正確 | 照用：1990 年已有連鎖喺銅鑼灣開房間式 lounge，Big Echo 1991 年來港 |
| 5 | M39 回流比例「約一成」 | 要修正 | 「一成」刪走；1992 年夏寫回流只宜零星傳聞（F4 6 處改做「間中都會聽到」） |
| 6 | M22 台灣資金幅度 | 核實正確 | 照用：台灣資金確係主要水喉，唔寫死精確百分比；「1992 尾收水」只寫風聲正確 |
| 7 | M23 產量部數（1990／91／92） | 要修正 | 票房 12.4 億核實正確；逐年產量數字核實唔到（口徑不一：上映約 200–242 部 vs 製作／送檢 300–426 部；產量峰值有來源指係 1993 唔係 1992）——**本票無逐年產量句要改；數字唔寫入玩家面**，留待之後內容批次處理 |

## §4 Ripple 量化（C1–C5）＋建議——等拍板，唔實作

來源：`~/workspace/linji-work157-analysis/RIPPLE.md`（數字全部實計：真 `dualTrackNumbers` 函數＋fresh 初始值＋逐段讀 code＋94 張開局板面重計）。

- **頭號結論**：信用擺幅係 **5 點**，唔係 SCOUT 寫嘅 3 點——SCOUT 漏咗 C4_b「捱得」標籤經 registry 真・加信用 ＋2。最差組合（C3_a −1＋C4_a −1）雙軌 13；最好組合（C3_b +1＋C4_b +2）雙軌 18；開局雙軌 15，Y1 評核地板 45／警告線 65——擺幅只係地板嘅 11.1%。
- 開局可接通告數零影響：體能 75→70 重計 94 張板面，可接數 20→20（20 張入面冇一張有體能要求）。
- C4_b ＋8 壓力唔會整病跟健康節奏玩嘅玩家（每週休息一次最高掂 80 一日，翌日清零；`sickStreak:2` 掂唔到）；唔休息連谷先會將病倒日由第 9 日提早到第 8 日。但有即時隱藏代價：壓力跨過 70 試鏡成功率 ×0.78。
- C4_a 嗰筆人情債對 E4／E5 係「幾乎零」：E4 數嘅係 `S.mockCredits`（人哋欠玩家），唔係 `S.mockDebts`；E5 同理；只係還清後經 `favorLedgerNoteSettled` 計 `settled` +1／6。未還唯一作用係結局回望多一句「仲欠何生一筆」。
- 標籤沉澱對 C8／C15 閘零影響，但對「軌跡分類」有影響：C2 兩個標籤＋C4_b「捱得」全部入 `TRAJ49_TAG_SETS.support`，任揀 C2_a／C2_b 再加 C4_b 即有 2 個甘草組標籤 → 軌跡定型做 support（甘草）；軌跡只影響何生介紹句／殺青評語／報紙稱呼，`resolveEnding410` 明文唔用佢判結局。
- **S1–S10 唔做**（等用戶拍板）：C5_a 唔加 `rel_choi:+1`；C4_b「捱得」標籤照保留。RIPPLE 報告全文見分析目錄，建議等用戶拍板先實作。

## §5 測試

### 5.1 新增測試（全部 PASS；反證對 pristine `e08a070` 乾淨 FAIL，唔 crash）

- `tests/test_story157_index_static.py`（115＋2 斷言）：每表 key 數目／次序、beats 數（C8=10 唔係設計稿嘅 8；C15／C16／C13＝7；C17＝15）、關鍵句、閘（C6／C6F route＋weekMin 15；C11 需 C7；C15 需 C10；C17 weekMin 153／yearEq 1992／需 C13；C18 需 C5＋weekMin 48；C19 需 C18＋weekMin 61）、全部 choice 旗／stats、ERA 修正句、舊句消失、年份規則（內容段零 1991／1992／1993，WF1 單一 legacy `openConditionsNote`「1991 春」除外；`STORY_GATE_3Y` 年份欄合法使用 game 年）、`effects.notes` 零數字承諾、零「聲量」／「Ho哥」／真人名、SAVE／softRev／`?v=` 不變、C17 synopsis 無 DEV 註解。反證：27 FAIL。
- `tests/test_story157_pack_static.py`（124 斷言，pack 組）：C1–C5 nodes[0–4] 逐值核對。反證：26 FAIL。

### 5.2 四個舊守衛窄化豁免（已拍板，寫明 v157 brief＋SCOUT §3.1）

- `test_aud91fix122_static.py`、`test_aud91fix124_static.py`、`test_gigreq110_static.py`、`test_wf5_87_static.py`：因為本票授權直改 pack nodes[0–4] 而 FAIL，已窄化為只豁免 `content/story_detail_c1_to_c17.json` nodes[0–4] 呢次改動（gigreq110：git-status／diff 檢查只准呢個檔；wf5_87：nodes[5:] sha 對照 linji-work86 基線，證明死 pack C6–C17 唔郁；其餘 7 個 pack 仍全 sha）。唔准放寬其他 pack 守衛。

### 5.3 本票授權改動而要更新期望嘅舊測試（期望 only，機制斷言無放寬）

| 測試 | 改動 | 原因 |
|---|---|---|
| `test_gate136_static.py` | C17「頒獎禮前夕」斷言改做「只剩對白否定句 ×1」；1990 冬斷言改用新字（冬台慶啱啱完／星河電視台會議室／頒獎禮散場） | C17 場景改會議室＋synopsis 改寫 |
| `test_weave47_static.py` | G4 標題 → 阿媽煲咗湯 | 新標題 |
| `test_weave48_static.py`＋`test_weave48_logic.js` | C6 標題 → 角落嗰張枱（3 處） | 新標題（`STORY_TITLE_SOFT.C6`／C5 nextHint 殘留舊標題，係 fallback 表，留返唔郁——見 §7） |
| `test_wf1_80_logic.js` | beats 下限 C15／C16／C13 由 ≥8 改 ≥7；v136 fixture 文本子序列／前綴檢查改做機制等價檢查（choices id 順序＋每抉擇 flags／stats／tags 同 fixture 一致＋flags_written 只增不減） | C15／C16／C13 重寫做 7 拍；C6–C17 全幕文本已由設計稿取代（新文本斷言由 test_story157_index_static.py 承接） |
| `test_text125_static.py` | CHOICE47 resultBeats 普查 11→15（F4 3×3=9＋G4 2+4=6）；currentLine／advance／applyFamilySafeToNode 行號 resync（27800→27824、27913→27937、33516→33582） | F4／G4 新寫＋splice 行號漂移 |
| `test_weave46_static.py` | 錨點字串「黑雨殺到」→「暴雨殺到」 | §1.9 黑雨清零 |
| `test_travel114_static.py` | 44 個 openLoc 呼叫點＋DEF／WRAPPER 行號 resync（difflib 對位，內容逐行相同，純漂移；DEF 53562→53632、WRAPPER 44171→44241） | splice 行號漂移 |

### 5.4 全套 A/B（suite3，已填）

- Pristine baseline（`e08a070`，`~/workspace/linji-pristine155`）：**211 PASS／12 FAIL**（FAIL：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38——全部 pre-existing；weave44 係 `CHK101_PAYEE = "陳偉翔"` 第三處出現令 count 3≠2，pristine 一樣 FAIL，唔係 v157 引起；soft_tip_111_restore 同理 pristine 一樣 FAIL）。
- 工作副本（未更新測試前）：205 PASS／20 FAIL——多出嘅 8 項正正係 §5.3 嗰 8 個測試。
- 工作副本（更新測試後，suite3）：**213 PASS／12 FAIL**（`qa131/suite3_workA.txt`，225 檔）；pristine 同期 **211 PASS／12 FAIL**（`qa131/suite3_pristineA.txt`，223 檔）。總數差 ＋2＝正好 2 份新測試；FAIL 清單兩邊逐項相同（diff 零差異），多出 FAIL 0 項。**結論：零回歸。**
- 逐個直接跑相關測試 15/15 PASS：兩份新測試＋§5.3 7 個更新測試＋4 個守衛窄化測試＋weave48_logic／travel114_logic 兩個配對檔（詳見 `qa131/SUITE3_AB.md` §2）。
- 注意：套件數字會波動（同一 repo 連續跑出唔同總數，失敗項每次唔同、全部係 .py、逐個直接跑全部 PASS；每次都出現嘅只有 12 項 pre-existing FAIL）。判斷回歸睇「12 項穩定 FAIL＋相關測試逐個直接覆驗」，唔好齋信一次 suite 總數。本次兩邊總數差完全由新測試數解釋，無大幅波動跡象，按任務條件無跑第二次工作版確認 run。

## §6 實駕驗證（drive2：6 phase 全部 PASS）

- 腳本：`qa131/drive157.py`（本地鏡像 port 8971，390×844，`?softPreview=1`；Playwright venv `/home/hatch/pwenv49/bin/python`）。正本跑次 run5，550 秒，EXIT=0，**0 pageerror、0 HTTP404**。詳見 `qa131/DRIVE2.md`。
- 第一輪 drive 死喺 Phase B：`awardsSetFlag` 唔係 global（IIFE 內部函數），seed 嗰陣 `ReferenceError`。修正：改行 `S.awardsFlags["1992/award_singho_tv"]` 直寫（gate 用 game year 1992 做 key）。第一輪已驗到：A 全程＋B 前半（C18／C11／C15 閘）＋C15 播放，0 pageerror（截至 crash）。
- **Phase A N1–N5 全程 PASS**：C1 ui 16 句（首句「何生事務所嘅冷氣夠凍…」）、C2 force 11、C3 force 14、**C4 ui 8 句**（今輪第一次經 UI 攞到 offer）、C5 force 12；全部 done=true。抉擇同 run2f 一致；C1 `route_tv: false`。
- **Phase B 關鍵閘 PASS（8 項）**：C18 day300 唔開／day334（1990-12-01）開 15 句；C11 無 C7 唔開／有 C7 開 15 句；C15 無 tag 唔開／有 tag 開 11 句；C17 day1065 無獎唔開／有獎開／backstop day1096 無獎都開。
- **Phase C 審計斷裂 PASS（13 項）**：C16 train 旗＋`ching_after_train` when()=true、`ching_after_polish`=false（互斥正確）、C9 調停旗、gu_loan／chai_repay when()=true、C14 未定旗、人脈網 live `{stay:true, hustle:false}`、WF1 回響 3 句（第 4 支俾 3 行上限截，設計原意）、C5 `flag_choi_honest` 寫入＋讀取。
- **Phase D 程天諾真觸發 PASS**：掃 day 973–1000，day 974 觸發，overlay「巧遇 · 程天諾」，首句「喂，你哋睇住呀，我程天諾唔會一世靠部機㗎…」；10 句 after_train 對白；`when_live: true`。
- **Phase E F4／G4 PASS**（run2f／run3 兩次唔完整之後 run5 全通）：F4 day 900 事務所 sheet 見卡「何生有句說話想同你講」，播 4 句，揀「唔走」→ `flag_stay_mind: true`；G4 ☰選單→手帳→人情頁→「返屋企講清楚」，播 4 句，揀「繼續做落去」→ `flag_family_job_decline: true`。根因：F4 seed 日要 ≥882（1992-06-01 夏，唔係 881）；屋企唔係地圖地點，G4 正確路徑係手帳人情頁；enc79 攔截要清走 overlay 先見到 sheet。
- **Phase F C17 全程 PASS**：fresh page，day 1065＋C13 done＋獎 done，22 句，2 抉擇，揀「順其自然」→ `S.ending410 = {career: "E0", eveKey: "natural"}`，結局畫面「三年收科」E0 正文出現。首句「1992 年冬末，星河電視台會議室。冬台慶啱啱完，彩紙仲喺走廊掃唔切…」；`meeting_room: true`、`taiwan: true`。
- 附帶觀察（drive 層面，唔係遊戲 bug 定論）：C2／C3／C5 仍然 via=force（sheet 無對應「播劇情：」offer，疑似 stale-sheet／導航問題，留待跟進）；C17 句數三跑 36／23／22 係 `step_story` 逐字 reveal 重複計數，內容一致唔係回歸。
- 證據：`qa131/drive157.json`（run5）、`qa131/drive157_run5.log`、截圖 `qa131/shots157/`（15 張：c1–c5、c11、c15、c18、ching_enc、f4_mid、g4_mid、c17_mid、c17_after_choice）。

## §7 未解決問題（outstanding，等拍板／另開票）

1. **Q2／Q3 C6F 昌叔題眼句**：「跟過三期戲，等嘅唔係近鏡，係一個名」跟設計稿刪咗；用戶未拍板，唔擅自救返。等用戶決定要唔要加返。
2. **C5 alias 斷裂**：保留裸名 `choi_honest`／`choi_spin`／`choi_dodge`，唔加 `flag_choi_honest`。`enc87StoryFlag`／`endingFlag410` 雙 store 讀唔會自動對應裸名；要拍板先至加 alias。
3. **E06「走」選項缺口**：設計稿 E06 段落嘅「走」選項未有對應實裝接線（留待跟進票具體化）。
4. **G4 decline 旗接線**：`endingExodusScene410` 去留段落未讀 `flag_family_job_decline`（見 §1.8）；另開票加一句「主動留低」版。
5. **F4 第三選項純對白**：F4 第三選項無旗／無數值，純對白——按新 spine「純對白就寫明純對白」原則接受現狀；如要升級做真分支另開票。
6. **結局梯換名另案**：結局梯／稱號換名唔喺呢票，另案處理。
7. **G4 卡片標題硬編碼**：`choice47FamilyCardHtml` 寫死「屋企有話同你講」，唔跟節點新標題「阿媽煲咗湯」變。留返唔郁（改佢要郁卡片渲染，另開票）。
8. **殘留舊標題（fallback 表）**：`STORY_TITLE_SOFT.C6` 仍係「飯堂閒角」、C5 nextHint 仍講「行電視線有『飯堂閒角』」——節點標題優先，fallback 表未跟住改；要唔要一併改，另開票決定。
9. **C13 俾 inline 主幹遮住**：pack C13 喺 live registry 俾 inline 主幹遮住（`applyStorySpineOverrides48()` 換做「賀歲片」）——關海媚個名要真係喺 live 見到，等 v157／v158 或另開票處理 C13 被遮住。
10. **Ripple S1–S10**：唔實作，等用戶拍板（見 §4）。
11. **C17 synopsis 第 2 段**：整合員已改寫做玩家安全寫法（見 §1.7）；如設計組想保留「舊版」對照說明，請改放 DEV 註解，唔好放 synopsis。

## §8 落地記錄（已落地）

- Rebase：分支 `v20a157` 由 `e08a070` rebase 上 `origin/main` `60b0a8f`（v166 NOTES）。6 個測試檔衝突（aud91fix122／124、gigreq110、text125、travel114、wf5_87），其中 wf5_87 手動合併（保留 main 嘅 v151 DENG 例外＋v157 嘅 nodes[5:] 檢查——v157 原版喺 rebase 後樹會誤判 DENG 兩檔）；rebase 後 HEAD `171829a`；resync commit `22900ab`（travel114 42 錨點／text125 3 錨點／kwan151 13 錨點／tang152 3 錨點，difflib 核實全部純漂移；全套 rebase 後 225／12 零回歸）。期間修好 SSH host key 查錯地方問題（`core.sshCommand` 加 `-o UserKnownHostsFile=/home/hatch/.ssh/known_hosts`，見 AGENTS.md）。
- Squash merge：main `807440f`（44 檔，+4431/−647），push `60b0a8f..807440f` 上 GitHub。合併前核對常駐 clone 分支 HEAD＝`22900ab`（v160 教訓）＋兩邊 tree sha 一致。
- 線上核實：5,238,462 bytes、sha `bd62ff94…`，同 repo `main:index.html` 逐字一致（curl 核實，HTTP 200）。
- 設計 review：`~/workspace/linji-design-review-v157/REVIEW.md`（已派，待報告）。
