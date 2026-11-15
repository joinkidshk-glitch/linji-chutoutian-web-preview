# v20a217 NOTES：語言審核遊戲側改動票

- 基底：v216 NOTES `2e5a298`（遊戲 `65b4b3e`＝live v216）。來源：`~/workspace/linji-language-audit/AUDIT.md`（§1 共 35 項）、`~/workspace/linji-language-audit/GAME_FIXES.md`（26 項遊戲側已裁定改法）、`~/workspace/linji-language-audit/DECISIONS-2026-11-15.md`（9 項用戶決定，凌駕 AUDIT）。**只做遊戲，唔郁攻略**（攻略由統籌另外做）。
- 紀律：唔改 SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`；新檔案用 `git add <path>` 明確加；唔開 PR（git 直接合併落地）；唔開下一票。
- YEARS66 硬規則：遊戲有 runtime 年份推移層（`index.html` L31622 起，SHIFT=2），source 寫舊曆、載入自動 +2，玩家見新曆。**絕對唔可以直接手改 source 年份 +2**，D7／D8 指定改動除外，NPC／PHASE1 重寫嗰陣對白入面嘅年份字串唔郁。

## 1. 改咗乜（逐項＋改前／改後數）

### 9 項用戶決定
- **D1 收科→埋單**：`index.html` 99 次／76 行全數→埋單（玩家面＋註解一併改；76 行入面無 TEXTFIX55 fixture、無 code identifier；「煞科」係另一個詞，唔受影響）。C17 章名「三年收科」→「三年埋單」；文案「收科嗰晚」→「埋單嗰晚」。改後 `埋單` 109 次（99＋原有 10）、`收科` 0。
- **D2 高仔 B——全部改全名**：live 57 處（`index.html` 10＋content 47：story_detail 23、STUB 14、SOFT_RUMOR 6、STUB_RUMOR 2、SANDBOX 2）全部→「高俊傑」，連 key 都改（剪影對照 `"高仔":"shadow_male"`→`"高俊傑"`，否則講者改名後查唔到）。改後 `高仔` 0、`高俊傑` index 110 次。AUDIT 話 61，差額 4 個喺 content/*.md dev 文件，唔係 live，唔郁。
- **D3 N13 章名確認〈企邊〉**：即站隊→企邊，見下。
- **D4 識分寸 W2——全部改**：11 處＋標籤 id 1 處，逐句選擇如下（全部→「識做人」，除咗報紙頭條用「知分寸」）：
  - L20638 notes「導演記得你識分寸。」→「導演記得你識做人。」
  - L20683 nodeRipple「導演記得你識分寸，信用微升」→「導演記得你識做人，信用微升」
  - L21670／L21682 notes「職員幫你擋咗一句：「佢識分寸。」」→「佢識做人。」
  - L43524 何生「只會話你唔識做，唔識分寸。」→「只會話你唔識做，唔識做人。」
  - L43528 label「「記住喇，何生，我識分寸。」」→「我識做人。」
  - L43531 阿偉「我識分寸，企返我個位，做我嗰份，唔會亂嚟。」→「我識做人，企返我個位，做我嗰份，唔會亂嚟。」
  - L43873 報紙頭條「劇組和氣收場　新人識分寸獲讚」→「新人知分寸獲讚」（頭條用「知分寸」較啱）
  - L43875 rumorEcho「話有個新人好識分寸。」→「好識做人。」
  - L58556 roleHint「講數同落手都要識分寸。」→「都要識做人。」
  - L43249 標籤 id `tagOnComplete:["識分寸"]`→`["識做人"]`（所屬通告 `gig_wf3_liao_stage`）。
  - **標籤 id 處理**：標籤存喺 `S.castingTags`；`STUB_CASTING_TAGS_v1.json` registry 得 10 粒，無「識分寸」條目，改 id 後 fallback label＝"識做人"，顯示無問題。舊存檔已有「識分寸」嗰粒會斷——已喺 `ensureCastingTagsState()`（L45472）加 migration，沿用 v20a57 先例，每次讀取冪等正規化：字串 `"識分寸"`→`"識做人"`、object `.label`／`.id` 同樣改；註解加「v20a217 加識分寸→識做人」。改後 `識分寸` 剩 4 次，全部係 migration code 本身（註解＋3 處比對）。無其他 code 讀 "識分寸" id；E1／SS 唔靠呢粒（靠八卦＋高冷）。
- **D5 抄通稿→攞稿照登**：3 處（index L20303、L24266、story_detail L910）。改後 0。
- **D6 「對齊」**：遊戲 grep 有 **113 次**，全部唔係目標句：版式「左對齊」、音樂「對齊聲部」（gig roleHint／blurb／synopsis，正確用法）、dev 註解（「通告級別 vs 要求對齊」等）、TEXTFIX55 鍵、L23044 註解「對齊返差一步，名實相符」。用戶原話句「先由內容判斷…再對齊另一邊」喺遊戲入面**唔存在**（嗰句係攻略附錄）。**遊戲側 0 改動**，等統籌確認。
- **D7 移民空位 1990 秋（顯示值）**：只改 `mergeExodusGigs` 嘅 L43010：`choice47SeasonReached(1992, "秋")`→`(1990, "秋")`；5 張 EXODUS gig discoverNote source「移民空位：1990 年秋先出現」→「移民空位：1988 年秋先出現」（`year:1990` 欄唔郁）。**唔改 L42697** `commit48Available` 嗰個 `(1992, "秋")`——嗰個係感情線 commit 窗口（N15–N17，顯示 1992 秋先啱）。已追蹤核實：`years66GigRemap` 經 `normalizeGigRecord` 喺 `mergeExodusGigs` 嗰陣行，`__y66w` 冪等，唔會 double-shift；source 1988 秋→顯示 1990 秋正確。EXODUS gigs `season:"不限"`，`g.year` 唔影響板面可見窗同 release 行。L42767 註解同步改做 (1990, "秋")。改後 `choice47SeasonReached(1992, "秋")` 剩 1（commit48）、`(1990, "秋")` 2（閘＋註解）；「移民空位：1988 年秋」5 處。行為改變（用戶已拍板）：移民空位通告由 1992 秋提早到 1990 秋上板——測試期望已跟住改（見 §2）。
- **D8 F4 場面改秋天**：4 處（CHOICE47_NODES `F4_stay_mind`）：`when:"1990夏起"`→`"1990秋起"`、setting「1990 年夏天，黃昏收工時分」→「1990 年秋，黃昏收工時分」、synopsis「1990 年夏天，移民顧問公司門口日日排長龍。」→「1990 年秋，…」、beats[0]「1990 年夏，黃昏收工時分。」→「1990 年秋，…」。年份 1990 絕對唔郁（經 walk 顯示 1992 年秋）。其餘 5 處「1990 年夏」全部係 N13〈企邊〉高爾夫球會所節點（lockedHint／setting／beats），唔係 F4，唔郁。**閘唔郁**：`CHOICE47_DEFS` 嘅 `F4_stay_mind: { year:1992, season:"夏"}` 維持不變——任務只叫改場面文字，改閘係玩法行為改動，未獲指示（見 §5 第 2 項）。
- **D9 年份引文 B 已完成，唔關遊戲事**：遊戲 source 年份一律唔郁（D7／D8 除外）。

### GAME_FIXES §1 第 1–26 項
1. 高仔句→「哼，算你夠薑。我記住你呀阿偉，等住睇。」：story_detail L601＋L584（notes `高仔話行著瞧`→`高俊傑話等住睇`）／L614／L658（系統句）＋STUB L627–628（拆兩行）。改後 `行著瞧` 0、`算你狠` 0、`打哈哈` 0。
2. 采兒句→「你唔好同我笑住帶過啦。」：story_detail L949＋STUB L949（STUB 版較短，淨改首句）。
3. 留咗道門→留返條路：story_detail L1058。改後 0。
4. 站隊→企邊：index 16 處玩家面（章名、label、lockedHint／nextHint、C17 回望、結局句、巧遇對白、標題表、synopsis）＋gigs_1989.json L155（`你的角色不站隊喊口號`→`你的角色唔企邊喊口號`）。註解 2 行（L21292、L58283，共 4 次）唔改。改後 `站隊` 剩 4（註解）、`企邊` 41。
5. 派工→派通告：index 5 處＋story_detail L44。改後 0。
6. 認橋→認自己度唔到／認返嗰兩句係人哋諗嘅：index C8 4 行／5 次，按 GAME_FIXES 建議寫法。改後 0。
7. 唔好帶口→唔好多嘴：index 3 處（L20276 ×2、L20295）。改後 0。
8. 係帳→係一筆數：L21178 對白＋L21210／L21246 notes 引句。改後 0。
9. 搞砸→搞衰：L53320 label、L53322 對白、L56583 阿偉句。改後 0。
10. 粉絲→歌迷：**實數係 WF4 5 處／3 行**，唔係 AUDIT 話嘅 2 處：L41157 標題、L41159 beats＋speaker「粉絲女仔」→「歌迷女仔」、L41160 choices ×2。改後 index `粉絲` 剩 3（TEXTFIX55_PHRASES／GIG_PHRASES `["粉絲","歌迷"]` ×2＋L60053 dev 註解）；gigs_1989.json 1 處（`帶粉絲排隊`）由 TEXTFIX55 GIG_PHRASES 兜底，顯示已係歌迷，source 唔郁；`protagonist.json` 1 處唔係 live（index 0 引用）。
11. 應援：L21537「應援牌」→「打氣牌」、L21740「應援升聲望」→「幫歌迷打氣升聲望」、L21504 註解「幫粉絲應援／避開狂熱粉」→「幫歌迷打氣／避開狂熱歌迷」。改後 0。
12. 爆料給記者→爆料畀記者：L20397 label＋L20260 註解。改後 0。
13. 老實說出所知→老實講出所知：story_detail L985＋STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json L985 label（後者係全檔掃出，GAME_FIXES 表漏咗；STUB 係 live，經 storySlots 載入）。改後 0。
14. 零死角→點睇都咁穩：L51740（刪咗重複嘅「企邊度都咁穩」分句，否則「咁穩」重複兩次）。改後 0。
15. 人情帳→人情簿：7 處（「人情帳本」→「人情簿」4 處註解先，再「人情帳」→「人情簿」3 處）。改後 0。
16. 忠誠帳→何生記低呢筆：L20915 nodeRipple「追數入何生嘅忠誠帳；…」→「追數就係何生記低呢筆；…」。改後 0。
17. 錄像→錄影：index.html 36 次＋`content/gigs_1988.json` 36 次（10 張通告）。舊版 soft 備份（6 檔 ×36）＋`NOTES_SOFT_PHASE_D_VOCAL_MAP_v1.json` 唔係 live（只 fetch `gigs_1988.json`／`gigs_1989.json`），唔郁。改後 live 0。
18. 龍套→臨記／做臨記：NPC_LINES_CORE 5 處（連第 24 項一併重寫）、EVENTS WEEK_OK 1 處（inline L19860＋`content/events_zh_HK.json` 兩邊）、story_detail L293／L347＋STUB L370、gigs_1989.json L1794 標題、**gigs_1991.json 3 處**（L99 標題／L102 blurb／L107 discoverNote，全檔掃出，GAME_FIXES 表漏咗；gigs_1991 係 live）、index L35326 code regex `/龍套開工$/,"龍套開拍"`→`/臨記開工$/,"臨記開拍"`（死 code，但唔改就做唔到龍套 0 命中）。`cast_main.json`／`protagonist.json`／`worldview.json` 共 4 處唔係 live（index 0 引用），唔郁。改後 live 0。
19. 怎麼／為什麼→點樣／點解：12 句，按 GAME_FIXES 表逐句改（story_detail 4 句、rival_mentor 6 句、romance_vera_hiu_choi R_hiu_meet 1 句、index L61548 1 句；L61548 兼改鸽→鴿＋「被放鸽子」→「俾人放飛機」）。改後呢 12 句 0 命中；L31376 TEXTFIX55 fixture 舊樣本唔郁（特登留低嘅「改前」樣本）。其餘 怎麼／為什麼 喺 `gift_react_copy.json`（8 次／4 句）同已停載嘅 `story_detail_romance_tang.json`（3 次），見 §5 第 3 項。
20. 簡體字：index L43063／L43073／L43083 傳聞 echo「个」5 次→「個」；L61548 鸽（見第 19 項）；L31757 DEV 註解「处理」→「處理」。改後 live 0。
21. 網絡短片→電視短片：index L6331 地點 `ad_adm` desc。改後 0。
22. 休息睡覺→休息瞓覺：index 6 處（label 3＋註解 3）＋**gigs_1988.json 1 處（shootHint）、gigs_1990.json 1 處（synopsis）、gift_react_copy.json 4 處（2 句 ×2）**——後三檔係全檔掃出，GAME_FIXES 表只列 index。DS filter 文件（3 處）唔係 live，唔郁。改後 live 0。
23. 喝水→飲水：index L12780 shootHint「記得多喝水，」→「記得多飲水，」＋同上三檔（gigs_1988 shootHint「記得多喝水，保持體能…」／gigs_1990 synopsis「你衝刺、急停、喝水。」／gift_react 4 處）。TEXTFIX55 無 喝水 key，顯示唔會自動轉，一定要改 source。舊 soft 備份 6 檔唔郁。改後 live 0。
24. NPC_LINES_CORE 成批重寫做廣東話：**180 句入面改 174 句**（map 176 項，2 項 sync 不變：agent greet/3、chat/5 嘅 JSON 本身已係廣東話；其餘 4 句原本已係廣東話，唔在 map：stylist advice/0、advice/1、intel/0、reporter chat/5）。base＝`content/npc_lines_core.json`（live，經 fetch 載入），inline const L19859 成個換做同一個重寫後嘅 object，兩邊驗證完全一致（inline＝＝JSON）。龍套 5 處兼改（director chat/2、intel/3；rival advice/4；reporter chat/6、intel/4）。`edits` 註解同 `name` 欄唔郁；stylist 仲叫 Vera（見 §5 第 4 項）。`locale:"zh-Hant-written"` 唔郁（見 §5 第 5 項）。
25. STORY_BEATS_PHASE1 成批重寫做廣東話：**43 項入面改 40 項**（3 項 sync 不變：B01/1、B01/2、B02/0 嘅 JSON 本身已係廣東話／新版內容）；章題 2 處（「記數簿與名片冊」→「記數簿同名片冊」、「人脈與對手」→「人脈同對手」）。base＝`content/story_beats_phase1.json`，inline L19860 嘅 PHASE1 const 成個換做同一個 object，兩邊驗證完全一致。**Ch1 open[0]「1988 年春，阿偉在黃大仙屋邨起步。」一字唔郁**——`JAN67_OPENING_TEXT_MAP`（L31784）用正則 match 呢句先換做「1990 年初…」，改一隻字都會令顯示變「1990 年春」（1 月開局應係「年初」）；walk 覆蓋已核實（BEATS 喺 L31893 walked＋L31955 jan67 fix）。重寫順手修埋 inline 同 JSON 嘅漂移（NPC 6 處、PHASE1 12 處，例如 B02／B04 內容完全唔同、B09／B10「（未達）／（已達）」前綴）。
26. 高仔方案 A 作廢，改行決定 2（B）。

### 測試期望更新（25 檔，全部只改期望字串／釘行，冇刪斷言、冇削弱）
- 舊詞斷言跟新寫法：`test_conseq61_logic.js`／`test_conseq61_static.py`／`test_weave410_logic.js`／`test_weave410_static.py`（收科→埋單）、`test_dlg119_static.py`（38 名表 高仔→高俊傑）、`test_story157_pack_static.py`（C3 標題「高俊傑搶鏡」、ALLOWED_SPEAKERS、ripple 兩值；nodes[5:] sha pin 重算 `5b464d60…`→`fa95df5f…`）、`test_story157_index_static.py`（C15 係一筆數）、`test_weave48_logic.js`／`test_weave48_static.py`（C14 企邊）、`test_wf4_203_logic.js`（set17 標題「錄影廠門口嗰班歌迷」）、`test_rest58_static.py`（休息瞓覺）、`test_gate136_static.py`（F4 1990 秋）、`test_years66_static.py`（結局閘「1992 年冬 · 三年埋單」＋choice47 窗口分拆：commit 仲係 1992 秋 ×1、移民空位閘 1990 秋 ×2）。
- 行為改變跟 D7：`test_weave47_logic.js` seg4（1990 夏唔注入／1990 秋注入 5／1991 注入／1992 春夏注入）、`test_giglib36_logic.js`（1991 有 exodus；新增 1990 夏之前無 exodus 下限檢查）。
- Scope guard 豁免擴充（v157 precedent）：`test_aud91fix122_static.py`／`test_aud91fix124_static.py`／`test_gigreq110_static.py`／`test_newspaper214_award_static.py`——v217 15 個 content JSON 列入豁免（同 `git status` 實際改動檔完全一致）；其餘 content JSON 一律唔准郁。
- `test_rom183_static.py`：npc_lines_core.json 斷言由「唔郁」改做「已粵語化」（colleague greet[0] 新值）；gift_react 嗰個「唔郁」斷言照舊 PASS（v217 只改咗 喝水 4 處，唔掂 是不是／什麼 計數）。
- 盤點 CSV（repo 外）：`~/workspace/linji-noportrait-audit/speakers_by_display.csv` L32 `extra_unknown,高仔,3`→`高俊傑`（③級顯示名跟遊戲改名；唔入 repo，dlg119 測試讀佢）。

## 2. 全套 suite A／B

- A（pristine，常駐 clone main v216）：**309／13**。
- B（工作副本）第一跑：**284／38**——25 項新 FAIL，全部係舊詞斷言／釘行／scope guard（見 §1 測試期望更新），逐個修復。
- B 第二跑：**307／15**——剩 `test_dlg119_static.py`（盤點 CSV 仲係高仔）＋`test_rest58_static.py`（我改測試嗰陣多咗個引號，SyntaxError）。兩項修好後各自 ALL PASS。
- B 第三跑：**309／13**——FAIL 清單同 A **一模一樣**（13 項穩定 pre-existing FAIL：flash51／giglib36_static／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。零回歸。
- 紅線核實：SAVE key `starVolunteer_map_v19w` 10 處、`"v20a10"` 7 處、`s107` 在位；舊詞全檔掃描（index.html＋content/*.json）：收科／高仔／派工／認橋／帶口／係帳／搞砸／零死角／忠誠帳／人情帳／錄像／打哈哈／行著瞧／算你狠／留咗道門／爆料給記者／老實說出所知／應援／抄通稿／網絡短片 全部 0（剩低例外全部有記低：站隊 4＝註解、粉絲 3＝TEXTFIX 映射 ×2＋註解、識分寸 4＝migration code、錄像／龍套／睡覺／喝水 剩低嘅全部喺非 live 檔）。

## 3. 釘行 resync（v217 淨 +3 行）

- 插入點：`ensureCastingTagsState()` 標籤遷移（舊 L45472 之後），淨 +3 行；其後釘行各 +3。
- `test_gift185_static.py`：總行數 62755→62758。
- `test_tang171_static.py`／`test_tang173_static.py`：總行數 62755→62758、openLoc DEF 行 57227→57230。
- `test_rom176_static.py`：四釘 55657→55660、56025→56028、57164→57167、57258→57261（實際行號已 grep 核實）。
- `test_travel114_static.py`：COUNT／FREE／DEF／WRAPPER 48 個釘行逐行核實內容同 pristine 一致（純漂移）：27 處 ≥45472 者 +3（COUNT 61308／61486／61632／61653、FREE 55480 之後 22 處、DEF 57227→57230）；WRAPPER 45430 唔郁（喺插入點之前）。

## 4. 殘留／跟進（唔喺呢票）

1. **story_detail 有 3 句 synopsis 年份會顯示 1993**（pre-existing display bug）：L1957「1991年夏，賀歲檔與台慶級位置開搶。…」、L2218「1991年秋，資本場宴會上，…」、L2355「1991年春，藍家在宴會側廳…」。機制：main pack 經 `years66Walk`，1991→1993；TEXTFIX55_EXACT 只覆蓋咗「1991年冬」同「1992年收束」兩句，呢 3 句無覆蓋。任務話 source 年份唔郁，只匯報，等統籌定（可能修法：加 TEXTFIX55_EXACT 條目，但係設計決定）。
2. **F4 閘 vs 文字**：場面改咗 1990 秋，但 `CHOICE47_DEFS` 嘅 `F4_stay_mind: { year:1992, season:"夏"}` 維持不變（顯示 1992 夏開），窗口註解話「N15 秋末至 N17 冬末」，三者未完全對齊，等統籌定。
3. **gift_react_copy.json 怎麼 ×8（4 句 ×2，byKey＋entries 兩份）**：Vera「你怎麼知道我想看這期的剪裁專題？」／「別人怎麼處理肩膀和領口。」、林曉晴「我聽都未聽過怎麼站。」、藍若曦「你怎麼找到這卷卡帶的？」。TEXTFIX55 無覆蓋，係 live（經 fetch 載入）。要成句重寫先啱（淨換 怎麼→點樣／點解會留低半句書面語），審核冇提供寫法，唔擅自改，等統籌定。`story_detail_romance_tang.json` 為什麼 ×3 唔使理（v20a152 已停載，鄧麗萍感情線取消）。
4. **NPC stylist 仲叫 Vera**（`NPC_LINES_CORE` stylist＋B07 句），Vera 刪除收尾係 v159 範圍，唔喺呢票。
5. **PHASE1 `locale:"zh-Hant-written"`**：內容已改粵語，metadata 未郁（唔敢郁，驚整斷測試），等統籌定。
6. **D6 對齊 113 次**：遊戲有命中但全部唔係目標句，0 改動，等統籌確認。
7. 審核漏數（已一併修，見 §1）：粉絲 WF4 實數 5 處唔係 AUDIT 嘅 2 處；高仔 61 vs 57（4 個喺 .md dev 文件）；龍套／喝水／老實說出所知喺其他 live JSON 有漏網（gigs_1991、gigs_1988／1990、gift_react、STUB）。

## 5. 改動檔清單

- `index.html`（+209／−206，淨 +3 行；5,554,079 bytes；blob `c983e7f`）
- content 15 檔：`SANDBOX_BEHAVIOR_GATE_C1_C5_SOFT_STUB_v1.json`、`SOFT_RUMOR_BEHAVIOR_GATE_PLAYTEST_FIX_v1.json`、`STUB_RUMOR_FRAGMENTS_v1.json`、`STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json`、`events_zh_HK.json`、`gift_react_copy.json`、`gigs_1988.json`、`gigs_1989.json`、`gigs_1990.json`、`gigs_1991.json`、`npc_lines_core.json`（174 句改）、`story_beats_phase1.json`（40 項改）、`story_detail_c1_to_c17.json`、`story_detail_rival_mentor.json`、`story_detail_romance_vera_hiu_choi.json`
- tests 25 檔：`test_aud91fix122_static.py`、`test_aud91fix124_static.py`、`test_conseq61_logic.js`、`test_conseq61_static.py`、`test_dlg119_static.py`、`test_gate136_static.py`、`test_gift185_static.py`、`test_giglib36_logic.js`、`test_gigreq110_static.py`、`test_newspaper214_award_static.py`、`test_rest58_static.py`、`test_rom176_static.py`、`test_rom183_static.py`、`test_story157_index_static.py`、`test_story157_pack_static.py`、`test_tang171_static.py`、`test_tang173_static.py`、`test_travel114_static.py`、`test_weave410_logic.js`、`test_weave410_static.py`、`test_weave47_logic.js`、`test_weave48_logic.js`、`test_weave48_static.py`、`test_wf4_203_logic.js`、`test_years66_static.py`
- repo 外：`~/workspace/linji-noportrait-audit/speakers_by_display.csv` L32（唔入 repo）
- 本檔 `NOTES_V20A217.md`
- 合計 41 檔，+691／−620。腳本留檔（唔入 repo）：`~/workspace/v217_edit.py`、`v217_edit2.py`、`v217_edit3.py`、`v217_testfix4a.py`。

## 6. 落地紀錄

- （待落地後補）
