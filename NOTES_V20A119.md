# NOTES_V20A119 — 無名角色剪影接入（DLG119）

- 合併：分支 `v119-shadow`（rebase 後 tip `7a8cffa`，基底 main `3be1b3d` v124）→ squash 入 main **`fd4860a`**，已 push。
- 線上核實：本地 index.html **5,159,938 bytes**／sha256 `e771c824fc91fe0e…`；curl 線上 **200、5,159,938 bytes、sha `e771c824fc91fe0e…`，對上**（push 後即刻驗，Pages 無滯後）。
- 測試：全套 A/B——pristine main（`3be1b3d`）**167 PASS／12 FAIL** vs 工作版 **169 PASS／12 FAIL**，零新增回歸；新 PASS 得 2 個新守門（`test_dlg119_logic.js`、`test_dlg119_static.py`，含反證）。12 FAIL 係既有清單（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），兩邊一致。
- 實駕：Playwright 390×844、`?softPreview=1`、本地鏡像＋逐檔 byte／sha 核對，**0 pageerror**（全部 5 次驅動）。25 幕實機＋2 幕合成對照，38 名全覆蓋（見 §2）。
- 回滾：`git revert fd4860a`（squash 單一 commit；影圖檔＋測試一併還原）。

## 1. 改咗咩（index.html 淨 +152 行，23 檔）

- **DLG119 模組**（`/* ===== v20a119 DLG119 無名角色剪影 ===== */`，index.html 約 26386 行起，＋166／−14 行）：
  - 三款影：男 `shadow_male`／女 `shadow_female`／老年 `shadow_elder`，講者行 `{stem}_base.webp`、聽者行預出嘅 `{stem}_dim_base.webp`（填充 ×0.78、邊光 ×0.92 焗入圖，唔用 CSS `brightness()` 一刀切）；光暈 `{stem}_halo.png`（暖色 232,200,150、峰值 alpha 0.30）貼喺人物背後、底圖之上，講者／聽者同一層。
  - 影圖填充＋邊光行 fix1 V5 數字（填充 +14、邊光 ×1.15＋向內加粗 1px）；影唔翻轉（邊光永遠右側，GAZE `flipSafe=false`）；影唔行表情候補鏈、唔接 bust 後備。
  - **同影去重**（fix1 方案 (a)，`dlg119DedupePair`）：兩個講者解出同一個影 asset → 只留後者（當前講者），孖影永不出現。
  - **影缺失跌返舊版「影」黑卡**（`__dlg106Err` 影分支）：404 走盡候補鏈 → 原位換成 `dlg119-sil` 黑卡（唔准白屏、唔准頂替做其他角色），同場光暈一併隱藏（`visibility:hidden`）。
  - GAZE＋5 鍵（39 條）、身高表＋5 鍵（一律 1.00；老年影矮一截係圖本身人形佔比，唔另外 ×0.84）。
  - `SP_SPEAKER_LEGACY` ＋38 名解像（見 §2）；`SP_SPEAKER_REG` 舊 8 個 id 條目保留（防斷鏈），新增 `shadow_male`／`shadow_female`／`shadow_elder`／`crew_laolinji`。
- **新圖 10 張**（`assets/story/fullbody/`）：男／女／老年影 base＋_dim＋halo 各 3 張＋老臨記 `crew_laolinji_base.webp`（唯一留面嘅無名角）。
- **測試**：新守門 2 檔（logic＋static，含反證）；舊測試 8 檔期望值更新（dlg106 logic／static、dlg107、dlg108、dlg109 logic／static、map54、terms57、travel114 行號 resync——DLG119 令 index.html 淨 +152 行，44 個 `openLoc(` 呼叫點內容逐字一致、次序一致；`qa119/resync_travel114.py` 留檔）。
- **合併經過**：基底由任務原定 `dc12744` 先後變咗兩次——v120（`9eecc01`）同 v124（`3be1b3d`）期間先後入 main；分支兩次 rebase，每次唯一衝突都係 `tests/test_travel114_static.py` 行號表，兩次都用 difflib 對位重算（44 呼叫點逐字一致，COUNT 13／FREE 27 不變），冇靜靜覆蓋人哋嘅嘢。第一次 rebase 前誤讀 `HEAD`（rebase 進行中 `HEAD` 係 rebased commit 唔係 origin/main），已用明確 rev 覆核——v119 喺 rebase 前並無入 main。

## 2. 38 名解像表（全部實駕驗過）

| 影 | 顯示名（幕次） |
|---|---|
| 有面 `crew_laolinji` | 老臨記（C2、WF1 C19；C19 嗰幕同副導演男影同場，面＋影並存） |
| 男 `shadow_male`（27） | 副導演（C7、C19）、導演（C8、C13）、周刊編輯（R_choi_crisis）、院線助理（R_tang_meet，`generic_cinema_asst` 別名）、高仔（C3）、副導（C3、C13）、選角導演（C10）、武指（C15）、場務（C7、C13）、監製（C16）、唱片公司職員（C12）、老臨記昌叔（C6，名牌話係昌叔但解像行男影——拍板係咁，唔係老臨記有面圖）、助導（R_hiu_crisis）、週刊記者（C11）、後台場務（C11）、保安（C12）、處境劇副導（C6）、場務大佬根叔（C6F）、電影組副導（C6F）、老場務（C17）、助導阿森（A_hakfan_push1）、導演陸志明（A_hakfan_push2）、監製周世昌（A_hakfan_crisis）、茶餐廳伙記（C8）、編劇阿昌（C8）、酒廊伙記（C9）、藍父（detail C15） |
| 女 `shadow_female`（9） | 場務姐姐（WF3 W3_lu_pa，合成對照）、約會對象（detail C12）、助導阿玲（A_gao_crisis）、佳麗（C11）、茶水阿姐（C13）、飯堂阿姐（C6）、歌迷阿妹（C12）、服裝助手（C10）、阿媽（CHOICE47 G4，合成對照） |
| 老年 `shadow_elder`（1） | 老武師（C15） |

註：阿媽／場務姐姐嗰兩幕喺實機係播唔到對白嘅——見 §4 既有問題；合成對照將同一節點 beats 嘅 `text` 轉做 `lines` 後直播，講者解像／渲染器同一條 DLG119 路，兩人均正確出女影＋名牌＋光暈。

## 3. 實駕結果（逐幕）

驅動：`qa119/drive119.py`（主）、`drive119b.py`（補充）、`drive119c.py`（R_tang_meet＋G4／W3）、`drive119d.py`（text-beats 對照）、`qa119/analyze119.py`（深底對比量度）。Log＋截圖留喺工作副本 `qa119/`（唔入 repo）。

| 幕 | 結果 |
|---|---|
| C2 留人脈／趕通告 | PASS——老臨記有面全身圖，講者 brightness(1)／聽者 0.6；旁白句兩人齊暗 0.6 無名牌。 |
| C7 暴雨救場 | PASS——場務→副導演男影（同影去重：連續兩句都係單影，唔出孖影）；阿偉句男影做聽者 `_dim`；旁白句留 `_dim` 影。 |
| C13 賀歲片 | PASS——場務／導演／副導男影；茶水阿姐女影（講者 base／廖炳星句做聽者 `_dim`）；場務→導演連續同影去重單影。 |
| C15 高危替身 | PASS——老武師老年影 vs 武指男影同場，一眼分到（老年影矮一截、闊袍、圓頭＋白髮絲；見截圖 `main_C15_step03.png`）；麥震東句武指做聽者 `_dim`。 |
| C3 對對手硬／忍 | PASS——副導／高仔男影；阿偉句男影聽者 `_dim`。 |
| C6 飯堂閒角 | PASS——飯堂阿姐女影、老臨記昌叔男影、處境劇副導男影。 |
| C6F 片場跟班 | PASS——場務大佬根叔／電影組副導男影。 |
| C8 茶餐廳度橋 | PASS——茶餐廳伙記／導演／編劇阿昌男影；最暗場景之一（見 §3.1）。 |
| C9 年尾追數 | PASS——酒廊伙記男影（同何生對答，影＋何生雙人舞台）。 |
| C10 戲路定型 | PASS——選角導演男影、服裝助手女影（講者 base／選角導演句做聽者 `_dim`）。 |
| C11 選美後台 | PASS——後台場務男影、佳麗女影、週刊記者男影（做聽者嗰陣女影 `_dim` 係佳麗，唔係記者——pair 邏輯正確）。 |
| C12 樂壇前哨（spine） | PASS——唱片公司職員／保安男影、歌迷阿妹女影；detail 版 C12（約會對象女影）另見下行。 |
| detail C12 賀歲搶位 | PASS——約會對象女影（講者 base／阿偉句做聽者 `_dim`）。 |
| C16 偶像實力之爭 | PASS——監製男影。 |
| C17 三年收科 | PASS——老場務男影。 |
| C19 賭枱邊 | PASS——副導演男影＋老臨記有面同場。 |
| R_choi_crisis 週刊會議室 | PASS——週刊編輯男影（采兒句做聽者 `_dim`）。 |
| R_tang_meet 上門談排片 | PASS——院線助理男影（講者 base／鄧麗萍句做聽者 `_dim`）；經 `__dengLine.playMeet()`（要 C5 done＋favor≥1＋身處事務所三重閘齊先開到）。 |
| R_hiu_crisis 同場搶通告 | PASS——助導男影。 |
| A_gao_crisis 賀歲檔的賭注 | PASS——助導阿玲女影。 |
| A_hakfan_push1／push2／crisis | PASS——助導阿森／導演陸志明／監製周世昌男影。 |
| R_lan_crisis | 播到，0 影——頭 6 步得藍若曦講嘢，藍父唔喺呢段；藍父已由 detail C15 覆蓋。 |
| G4 屋企有話同你講（阿媽） | 合成對照 PASS——阿媽女影＋名牌＋光暈；原裝節點見 §4。 |
| W3_lu_pa 嗰晚係你頂嗰？（場務姐姐） | 合成對照 PASS——場務姐姐女影＋名牌＋光暈，阿偉聽者 0.6；原裝節點見 §4。 |
| 404 黑卡路徑（C7，攔截 `shadow_male_base.webp`＋`_dim_base.webp`） | PASS——9 次請求全 abort，講者／聽者位原位出舊版「影」黑卡（`dlg119-sil`，左右位正確），同場光暈 `visibility:hidden`，對白繼續行，魏詠男段唔受影響；0 pageerror。 |

### 3.1 男影深底（重點殘留，已驗證——唔使調光暈）

逐個深色場景驗過，量度 110 張影截圖（`qa119/contrast119.json`）：

- 最暗實景係 **C8 茶餐廳夜景**（人物胸口高度背景亮度 bgL 67–80，影填充 70，fillVsBg 得 −9.5——數字上最貼），其次 **C13 紅棉影業**（bgL 91–98，fillVsBg −21.4～−28.3）；其餘幕 bgL 105–133。
- 但**冇一幕溶**：琥珀邊光＋光暈令每張圖至少一邊邊緣梯度 ≥36（C8：左 36.1／右 52.9；C13：右 49.3；C7：左 130.9），人眼睇截圖影輪廓清晰（C8 夜窗前頭頂光暈圈住、右側邊光成條見到；C13 淺牆前一樣）。
- **結論：光暈峰值 0.30 維持不變，唔調**——fix1「光暈先係修邊界主因」嘅判斷喺實機成立；填充／邊光亦唔郁。
- 旁白句男影聽者 `_dim`（填充 54.2）喺最暗底 C8 都仲有邊緣梯度（左 26.9／右 54.0），未溶。

### 3.2 其他實駕發現（全部 0 pageerror）

- 8 次 console.error 404 全部係既有表情候補鏈（`crew_laolinji_serious`、`yip_manji_serious`、`luk_baakyin_sad`、`ho_sang_angry`、`lin_hiu_surprise` 各 webp＋png）同缺場景圖 key（`rom_choi_crisis`、`rom_hiu_crisis`、`rom_tang_meet_soft_hold` → 行素底漸變），全部有後備、畫面無破圖；**冇一張係 DLG119 檔案**。
- 初版驅動 4 幕 `start: False`（R_choi_crisis／R_tang_meet／A_gao_crisis／C19）：根因係主驅動先播咗 C17，結局鎖 `ending78Locked()` 擋晒之後所有 `start`——新 session（C17 之前）全部播到；唔係 DLG119 問題。
- `choice47Play`／`wf3TalkPlay`／`yearSeasonNow` 唔係全域（IIFE 內），G4／W3 只能經節點物件直播（節點數據逐字抽自 index.html 原文，見 `qa119/nodes_c.json`）。

## 4. 殘留缺口（唔係 v119 引入，唔擋合併）

1. **CHOICE47／WF3 全部節點用 `text` beats，StoryPlay 只讀 `lines`／`line`——對白成段跳過**（新發現，既有 bug）：`CHOICE47_NODES` 19 句、`WF3_TALK_NODES` 67 句全部 `text` 形，無一 `lines`；`currentLine()`／`advance()`／`applyFamilySafeToNode()` 無任何 `text`→`lines` 轉換。實機對照（唔撳掣）：原裝 W3 一開即 `mode=choices`、`beatIdx=0`、行字空、得「完成這一節」掣；原裝 G4 一開即出兩個選項，四句對白零顯示。跟住 W3 完結嗰陣 `leaveStory` 會重開所在地地點，C1 未做嗰陣會自動播 C1（驅動嗰陣撞到）。即係話：阿媽 5 句、場務姐姐 5 句同其餘 CHOICE47／WF3 傾談對白，**喺玩家實機根本唔會顯示**——盤點嗰陣計咗佢哋做 live 句數，但渲染層由頭到尾冇讀過。另開一票修（轉 `text`→`lines` 或者播放器讀 `text`），唔喺 v119 改。
2. **廖炳星欠 `shy` 表情圖**（舊問題，v114 實駕已知）：C7 魏詠男段唔關事，係之前實駕撞到嘅 404，今次驅動無再撞到但檔本身未補。
3. **何生欠 `angry` 表情**（舊問題）：`ho_sang_angry.webp／.png` 404 後備行 base，今次 C9 撞到一次，畫面正常。
4. **老年影白髮去底流失**（fix1 已知）：C15 實機睇，白髮絲只剩淡淡幾根，頭偏大有光頭感；認人靠袍＋矮身形，實機分得到（§3），等用戶決定接唔接受。
5. **沈卓衡偏嚴肅、羅勁威黑恤衫變圓領 Tee**（v116 用戶已接受，唔郁）。
6. `crew_laolinji_serious` 表情檔缺失（老臨記 `serious` 候補 404 → 跌返 base，畫面正常；同第 2／3 點一類，補圖嗰陣一併做）。

## 5. 檔案清單（合併內容）

- `index.html`（＋166／−14 行，DLG119 模組＋LEGACY／REG／GAZE／身高表＋pair 去重＋黑卡後備）
- `assets/story/fullbody/`：`shadow_{male,female,elder}_{base,dim_base}.webp` ×6、`shadow_{male,female,elder}_halo.png` ×3、`crew_laolinji_base.webp`
- `tests/test_dlg119_logic.js`、`tests/test_dlg119_static.py`（新）
- `tests/test_dlg106_logic.js`、`tests/test_dlg106_static.js`、`tests/test_dlg107_static.py`、`tests/test_dlg108_static.py`、`tests/test_dlg109_height_logic.js`、`tests/test_dlg109_height_static.py`、`tests/test_map54_static.py`、`tests/test_terms57_static.py`、`tests/test_travel114_static.py`（期望值／行號更新）
- `qa119/resync_travel114.py`（行號 resync 腳本，留檔）
