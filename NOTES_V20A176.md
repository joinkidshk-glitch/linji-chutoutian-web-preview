# NOTES_V20A176 — 全部人隨機撞到，連紅星都可以送禮

- **已落地：遊戲 commit `4475564`，線上核實 5,316,979 bytes、sha256 `25212cc9a458c78f22246f9808d266a80327e2023b84e3ab2052b0ca535f04df`，同 repo HEAD:index.html 完全一致（2026-11-13 約 15:58 HKT；第一次 push 斷線 egress proxy reset，重試成功；Pages 部署滯後約 2 分鐘）**
- 分支：`v20a176`（工作副本 `~/workspace/linji-work176/`），基底 main `c682cc2`（v178；三段 rebase 完成，見 §9：a618a5d→a41b789→91f264a→c682cc2）
- 設計：`DESIGN.md`（§0–§11），用戶拍板「全部人隨機撞到，連紅星都可以送禮（明星志願嗰套）」
- **本票唔落地**——落地由統籌做。**Rebase 已完成**（基底 `c682cc2`，最新 main；重驗見 §3／§9）。

## §0 摘要

六位女角＋12 紅星全部隨機巧遇；紅星可送禮，好感行 `S.stars` 0–100。女角出沒盤照抄 ENC79
機制獨立一盤（P=0.50、主場 share 0.65、保底 5 日、每日 1／每週 3／冷卻 2 日）；女角巧遇
modal 收尾：傾談／送禮／約佢出街（defensive，v159 未落地就唔出）／行開；星送禮獨立路徑
（最愛 +4／喜歡 +2／普通 +1／唔鍾意 −2，經 `enc79AddFav(starId, delta, "gift")`，週軟頂
共用 10／週）；48 條星反應句＋海媚 prefs 行 runtime 注入；地點板拎走女角傾談／送禮掣；
風聲／手帳女角版輕量。

- `index.html`：+570／−32（總行數 59341→59879，淨 +538；rebase 上 c682cc2 後總行數 59993，見 §9）
- 新測試：`tests/test_rom176_logic.js`（76/76 PASS）、`tests/test_rom176_static.py`（ALL PASS）
- Resync 舊測試 12 檔（見 §5）；rebase 上 91f264a 後再 resync 7 檔（見 §9）；第三輪上 c682cc2 後再 resync 4 檔（見 §9.4）
- 海媚退路已由 day≥335 改為 **day≥699**（rebase fix，見 §2.2／§9）；主閘 `isDone("C9")` 唔郁
- 重驗（第三輪 rebase 後）：新測試 76＋ALL PASS，反證 logic 乾淨 FAIL／static 47 FAIL；全套 pristine 241／12 vs 工作版 243／12，FAIL 清單相同零回歸；實駕重跑 5/5，0 pageerror（見 §3／§9.4）
- 紅線守住：SAVE key／softRev／`?v=` 唔郁；`content/` pack JSON 零改動；12 星唔入 `S.npcs`；
  冇自己寫排他鎖／約會系統／最愛分層。

## §1 改動對照

### 1.1 ROM176 block（`qa176/rom176_block.js`，500 行，插入點 L52919 原基底／L53012 第二輪 rebase 後／L53033 第三輪 rebase 後，`/* ---------- 殺青回望` 之前）

由 `qa176/apply176.py`（22 處替換，全部 assert 命中次數）插入。內容：

- `ROM176_WOMEN`：6 女角 key／npcId／主副場——曉晴 hiu `tvb_longmen`／`tvb_kowloon`；
  采兒 choi `rec_star`／`film_cotton`；Vera vera `ad_central`／`ad_adm`；藍 lan `tvb_longmen`／
  `tvb_kowloon`；徐 xu `ad_central`／`ad_adm`；海媚 mei `ad_adm`／`rec_hk`。
- 常數：`ROM176_P=0.50`／`ROM176_SHARE=0.65`／`ROM176_DAILY_CAP=1`／`ROM176_WEEKLY_CAP=3`／
  `ROM176_COOLDOWN=2`／`ROM176_PITY_DAYS=5`。
- `ROM176_MEET_NODES`（R meet／push1／push2／crisis／ending）、`ROM176_GREET`（每人 1 句開場白）、
  `ROM176_TEA_LINES`（6 句茶餐廳風聲線）。
- 出沒盤：`rom176EnsureDay`（日種子 `enc79Hash`／`enc79Rand`，key `"rom176:"+day+":"+key+":out"`／
  `":loc"`；lazy-init `S.romWeek`／`S.romPity`／`S.romWhispers`／`S.romLast`／`S.starGiftDay`；風聲過期清理）、
  `rom176PresenceP`（P+0.10 有未完成故事節點 offer，上限 0.85；風聲 P≥0.80／share 0.85）、
  `rom176PresenceAt`、`rom176TryIntercept`（保底用 `S.romPity[key]={days,day}` 物件形式計**不同日子**；
  觸發入帳＋設 `gift_met_<key>`／`gift_talked_<key>`／`flag_<key>_talk_met`）。
- 巧遇 modal：`rom176PlayEncounter`（肖像＋greet（NPC_LINES 優先，ROM176_GREET 後備）＋30% 種子漏風聲＋
  掣：傾談／送禮（`canGive` 通過先出）／約佢出街（只喺 `typeof rom159DateGate==="function"`，
  defensive，呼叫形 `rom159DateGate(key, L)` 係估計，見 §7）／行開；onDismiss 返 `openLoc(encDone)`）。
- 返程守衛：`rom176BackOpts()`（旗在就食咗佢返 `{encDone:true}`，唔在返 `{travelFree:true}`）；
  `rom176InEncounter`／`rom176SetEncounter`。
- 星送禮：`rom176StarPrefKind`（favorites→favorite）／`rom176StarDelta`（+4／+2／+1／−2，
  重複正數減半 floor）／`rom176CanGiveStarGift`（met＋今日未送＋有庫存）／
  `rom176StarReactionLine`（item-specific favorite → tier-generic `starId::liked`／`starId::dislike` →
  placeholder fallback）／`rom176DoGiveStarGift`（扣庫存、寫 `S.starGiftDay`＋
  `giftMeta.lastGiveDay[relKey]`＋`giftHist`、`enc79AddFav(starId, delta, "gift")`、結果 modal
  「送禮唔計日子」、返 `openLoc(encDone)`、唔 tickDay）。
- `rom176ApplyGiftOverrides()`（自包含，inline 字面表；定義喺檔案後段但 hoisted，喺 GIFT 賦值行呼叫，
  跟 `applyTangGift164`／167 先例）：注入 12 星 prefs（`favorites`＋`likes`=fav+like＋`dislikes`，
  `relKey="rel_<id>"`，`requireFlagsAny=[]`）＋海媚 prefs（最愛保溫瓶＋拍紙簿、喜歡咖啡豆＋卡帶、
  唔鍾意香氛＋時裝雜誌）＋48 條反應句（`FAV176` 24 條 item-specific favorite＋`GEN176` 24 條
  tier-generic liked／dislike；put 冪等，byKey＋entries 兩邊寫）＋NPC_LINES lan／xu／mei
  （每人 greet／chat／advice／intel／pressure 各 2 句）＋PORTRAITS `npc_lan`／`npc_xu`／`npc_mei`
  （fullbody base webp `?v=20a176`）。
- 海媚解鎖：`rom176MeiUnlocked`——主閘 `StoryOC.isDone("C9")`，`dayIndex ≥ 699` 只係 done-state
  讀唔到嗰陣嘅退路（1991-12-01；rebase fix，原 335＝1990-12-01 錯計 +2 年份推移，見 §2.2／§9）。

### 1.2 其餘小改動（apply176.py 逐項 assert）

| 位置 | 改動 |
|---|---|
| NPCS L6028 起（+7 行，rebase 後行號；原基底 L6018） | 加 lan／xu／mei（homes 各 [主場, 副場]，face npc_lan／npc_xu／npc_mei） |
| `giveGift` 回傳 | 刪 `costsDay:true`（殘留清理，設計 §2.3；`doGiveGift` 嘅 `spendDay` 係獨立閘，唔讀呢個回傳） |
| `enc79AddFav` 兩處條件 | 加 `|| src==="gift"`＋註釋改「enc/beat/gift」（週軟頂計數＋入帳兩處） |
| GIFT_REACT 賦值行 L31531（rebase 後；原基底 L31516） | 同行 append 呼叫 `rom176ApplyGiftOverrides()`（textfix55Walk 之前） |
| `addLocTalkGiftActs` | 女角傾談掣加 `rom176IsWomanNpc` 閘；成段 romance 送禮 try block 刪走（鄧麗萍掣唔喺度，唔郁；導演／對手／何生傾談掣保留） |
| `openLoc` | enc79 攔截之前加 rom176 攔截（`!opts.encDone` 同條件） |
| `doTalk`／`doGiveGift` 嘅 `go` | 改行 `rom176BackOpts()` |
| `doGiveGift` 頂 | 加星分支（`enc79StarDef(npcKey)` → `rom176DoGiveStarGift`） |
| `openGiftPick` | 星版副標題＋Cancel／onDismiss 返程改 `rom176BackOpts()` |
| `enc79PlayEncounter` render() 最後一步 | 加「送禮畀＋星名」掣（`rom176CanGiveStarGift` 先出；撳咗 `rom176SetEncounter({kind:"star"...})`＋`ov.remove()`＋`openGiftPick(starId, {id: locId})`） |
| `enc79TeaListen` | roll<0.50 女角風聲分支（`rom176TeaTargets`）＋toast `romwhisper` 分支＋rumorId 用 `romwind:<key>:<day>` |
| `people72Html` | 女角行加「多數喺 X 出沒」／見過後「常喺 X 出沒」（海媚鎖定嗰陣唔出呢行），sub 句改「去佢常出沒嘅地方撞佢；撞到先可以傾談／送禮。」 |
| `enc79PeopleHtml` 紅星段 | 「唔靠送禮」→「撞到嗰陣可以傾偈、送禮。」 |
| `inv72Html` 送禮提示 | 改「喺地點撞到女角／紅星嗰陣先送得（地點板冇送禮掣）」 |

### 1.3 漂移表（pristine 行號 → 工作版行號，git diff hunks 核實）

L ≤ 6016：+0；6017–52895：+7（NPCS +7）；52896–52899：+19（星巧遇送禮掣 +12）；
52900–53018：+520（ROM176 block +501）；53019–53041：+528（茶聽 roll +8）；
53042–53785：+532（茶聽 toast +4）；53786–53802：被取代區（addLoc −13）；
53803–53887：+519；53888–57855：+524（openLoc hook +5）；57856–57869：+527
（doGiveGift 星分支 +3）；57870–58028：+528（doGiveGift go +1）；≥58029：+538
（people72 haunt +10）。淨 +538，總行數 59341→59879。

行號釘（本票，寫入 static test；**第三輪 rebase 後行號**，原基底值見 §9）：NPCS lan L6028、載入點 L31531、ROM176 block 起點 L53033、
rom176ApplyGiftOverrides 定義 L53398、addLocTalkGiftActs L54430、openLoc rom176 攔截 L54524。

## §2 設計落實／偏離（Step 1 核實，全部讀 code 實證）

### 2.1 星送禮接駁定案（設計 §11.2 已定）

`giveGift`／`canGive`／`openGiftPick` 唔假設 NPCS 存在——`openGiftPick` 只用 `GiftShop.prefFor`
（displayName fallback npcKey）＋`canGive`＋庫存；`reactionEntry`／`reactionLine` 只用
`GIFT_REACT.byKey`。星 id 可以直接做 npcKey，前提係注入 `GIFT_PREFS.npcs[starId]`。

但 `giveGift` 本身唔可以直接用嚟送星：① `calcDelta` 將 delta 夾到 +2／−1（設計要 +4／+2／+1／−2）；
② `giveGift` 經 `StoryOC.bumpRel(relKey)` 加 rel，會整出假 `rel_<starId>`，且有自己嘅每週 +2 軟頂；
③ `giveGift` 回傳仲有 `costsDay:true` 殘留。所以星送禮行獨立路徑 `rom176DoGiveStarGift`
（見 §1.1），共用 `openGiftPick` 揀禮物＋`GiftShop.prefKind` 分級。

### 2.2 海媚解鎖閘：設計假設同 code 閘有出入（**已解決**，rebase fix）

設計假設 N10 台慶 ≈ 1990-12-01（dayIndex 335）。但 code 閘表話：spine 寫 N10＝C9（冬，人情債觸發）；
`C9: { yearMin: 1991, seasonIn: ["冬"]}`，C10 需 C9＋dualGt 70＋1991 冬（C10 場景係星河電視台
慈善秀後台＝台慶場合）。所以可靠旗標係 `StoryOC.isDone("C9")`（S.story.done 後備）。
**本票決定：主閘用 `isDone("C9")`，dayIndex≥335 只係 done-state 讀唔到嗰陣嘅退路。**
出入寫低，落地前統籌確認邊個先啱（若 N10 實際係 1990 冬，閘要改）。
**解決（rebase，統籌拍板）**：退路已由 day≥335 改為 **day≥699**（1991-12-01，1991 年冬開始，
同 C9 閘對應；舊 335 係將主幹舊年表 1989 冬直接當咗 1990 冬，冇計 +2 年份推移）。
改咗 `index.html` 嘅 `rom176MeiUnlocked()` 退路行＋`qa176/rom176_block.js`＋B10／B11 測試
（`tests/test_rom176_logic.js`：day<699 鎖住／day≥699 解鎖；`tests/test_rom176_static.py`：
海媚閘段標題＋`'>= 699'` 斷言）。主閘 `isDone("C9")` 唔郁。DESIGN.md §3.1 已同步更正。

### 2.3 doTalk 唔加 rel（設計 §3.5「傾談（rel 少量）」喺 main 唔成立）

main 入面 `doTalk` 加嘅係 `S.npcs` 人情，唔係 `S.story.rel`——傾談對 rel 係 0 貢獻；rel 只靠送禮
（`giveGift`→`bumpRel`）＋劇情節點升。實駕 woman_talk_932 證實：傾談後 rel_hiu 仲係 0，
`S.npcs.colleague` 8→11。模擬校準只計送禮（見 §4）。設計文案若話傾談加 rel，要改文案唔係改數值。

### 2.4 其他核實（Step 1）

- 星 id 以 `ENC79_STARS` 為準（12 星：luk_baakyin、liu_bingxing、ngai_wingnaam、yip_manji、
  mak_zhendong、lok_gasing、pang_siuki、chung_choning、gu_mingfai、so_jiyan、chai_zanhoi、
  ching_tinlok；程天諾 unlockYear 1992）。
- 女角送禮現行數值（main 實測，非 v159 分層數）：`calcDelta` 喜歡 +2／普通 +1／唔鍾意 −1；
  重複第 2 次起正數減半（向下取整）；夾 delta>2→2、<−1→−1；`giveGift` 每週每 relKey 淨 +2 軟頂、
  每日每 relKey 1 份。
- `doTalk` 要求 NPCS 存在（用 `npc.face`→`PORTRAITS`、`bumpNpc`、`pickNpcLine`），所以 lan／xu／mei
  要補 NPCS 條目＋PORTRAITS face＋NPC_LINES（否則 `pickNpcLine` 回 `"……"`）。
- `canGive` 閘認 `S.flags["gift_met_"+npcKey]`——巧遇本身設咗旗，送禮掣會出，唔使預設 meet 旗。
- `enc79PlayEncounter` 內 `if(!wasMet) st.met = true;`，星巧遇一開始就設 met。
- 藍／徐 prefs pack 已有，唔使重複注入；海媚 prefs 注入（pack 冇 mei）。
- 鄧麗萍送禮掣喺 openLoc agency_ho 專屬段，唔經 `addLocTalkGiftActs`，唔郁。
- `softSocialCostsDay()` = `!softPreviewOn()`；`doGiveGift` 嘅 `spendDay` 係獨立閘，唔讀 `giveGift` 回傳。
- 星巧遇中途行 steps 嗰陣可能已經加過 fav（enc／beat 來源）：實駕 star_932 撳送禮前 fav 已係 1
  （+4 後變 5）——係 ENC79 既有行為，唔係 bug。

### 2.5 設計 §7 清單以外嘅新增狀態

`S.romLast`（上次觸發紀錄，返程守衛用）同 `S.romPity` 物件形式（`{days,day}` 計不同日子，唔係
設計寫嘅純計數）係實作時加嘅，設計 §7 冇列。功能已由 logic test 覆，落地唔使改，記錄在案。

## §3 測試

### 3.1 新測試

- `tests/test_rom176_logic.js`：**76/76 PASS**（工作版）；pristine 乾淨 FAIL（exit 1，
  `const not found: ROM176_WOMEN`）。覆蓋：注入（12 星 prefs＋海媚 prefs＋48 句＋冪等＋NPC_LINES＋
  PORTRAITS）、出沒盤（種子可重現、P=0.50、share 0.65、風聲 P≥0.80／share 0.85、節點 offer +0.10、
  海媚 C9 閘＋day≥699 退路＋grantWhisper）、caps／保底（每日 1／每週 3／冷卻 2 日／保底 5 日／
  主線待播優先／觸發入帳）、女角 modal（真 PlayEncounter：傾談恆出／送禮睇 canGive／冇約會掣／
  行開返 encDone／greet 用 NPC_LINES／肖像 fullbody）、星送禮（+4／+2／+1／−2、重複減半、每日限、
  週軟頂共用、級數上限、未見過唔送得、反應句、唔寫假 rel）、返程守衛。
  寫測試期間捉到兩點：①沙盒漏抽 `ENC79_WEEK_SOFT_CAP` 令 enc79AddFav try/catch 食咗返 0（已補抽）；
  ②B11 原先誤讀——day≥699 退路只喺 `S.story.done` 本身缺失先觸發（code 先讀 `S.story.done["C9"]`，
  有就直接 return），測試已改為 `delete S.story.done` 先測退路（code 唔郁）。
- `tests/test_rom176_static.py`：工作版 **ALL PASS**；pristine **47 FAIL**（乾淨反證；seg() 已加安全處理）。
  覆蓋：紅線（SAVE／softRev／?v=）、content pack 唔郁（gift_prefs npcs 只有原有 6 項、gift_react 55 條、
  items 10 樣）、ROM176 模組在位＋行號釘、地點板冇女角掣、文案、48 句、星接駁、風聲、海媚閘、
  星唔入 S.npcs、約會 defensive。

### 3.2 全套 A/B（`qa131/run_suite.sh <root> <outfile>`，兩邊同日重跑）

- 原基底（a618a5d）：
  - pristine（`~/workspace/linji-work176-pristine/`，index.html sha
    `3af45a51789cc01588a12076a0e880dae485b21539f5812c3cb84e62b6ae4932`）：**234 PASS／12 FAIL**
    （`qa176/suite_pristine176.txt`）
  - 工作版：**236 PASS／12 FAIL**（`qa176/suite_work176.txt`）
  - **FAIL 清單完全相同**（diff 零差異）：flash51、giglib36、pacing35、poster59、rumor49、slot50、
    soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38——全部係 pre-existing 12 項，
    零回歸。兩個新測試 PASS。
- 第一輪 rebase（基底 a41b789，v179）：
  - pristine **238／12**（`qa176/suite_pristine176_rebase.txt`）、工作版 **240／12**
    （`qa176/suite_work176_rebase.txt`），FAIL 清單相同。
- 第二輪 rebase（基底 **91f264a**，v175；見 §9）：
  - pristine（已更新到 91f264a，index.html sha `76c39a9f…`，總行數 59434）：
    **239 PASS／12 FAIL**（`qa176/suite_pristine176_rebase2.txt`）
  - 工作版（總行數 59972）：**241 PASS／12 FAIL**（`qa176/suite_work176_rebase2.txt`）
  - **FAIL 清單完全相同**（diff 零差異）：同上 12 項 pre-existing，零回歸。兩個新測試 PASS
    （`test_rom176_logic.js` 76/76、`test_rom176_static.py` ALL PASS）；v175 新測試
    `test_prog175_static.py`＋`test_story179_static.py` 亦 PASS。
  - 反證（rebase 後重驗）：logic 對 pristine 乾淨 FAIL（`const not found: ROM176_WOMEN`），
    static 對 pristine **47 FAIL**。
- 第三輪 rebase（基底 **c682cc2**，v178；見 §9.4）：
  - pristine（已更新到 c682cc2，index.html 總行數 59455）：**241 PASS／12 FAIL**
    （`qa176/suite_pristine176_rebase3.txt`）
  - 工作版（總行數 59993）：**243 PASS／12 FAIL**（`qa176/suite_work176_rebase3.txt`）
  - **FAIL 清單完全相同**（diff 淨差兩個新測試 PASS＋TOTAL 行）：同上 12 項 pre-existing，零回歸。
    兩個新測試 PASS（`test_rom176_logic.js` 76/76、`test_rom176_static.py` ALL PASS）；v178 新測試
    `test_awards178_logic.js` 8/8＋`test_awards178_static.py` ALL PASS（13 項）亦 PASS（v176 冇整爛佢哋）。
  - 反證（rebase 後重驗）：rom176 logic 對 pristine（c682cc2）乾淨 FAIL
    （`const not found: ROM176_WOMEN`），static 對 pristine **47 FAIL**；awards178 兩檔對
    前一版 pristine（91f264a）各 5 FAIL（乾淨反證——c682cc2 本身已有 v178 條款）。
  - 注意：第一次跑 pristine 全套嗰陣 `/tmp` 512M tmpfs 爆滿（`git archive` 展開 465M），
    suite 寫唔到 spill／OUT；清走 `/tmp/pristine178*` 後改用 `~/workspace/tmp-pristine178`
    （729M）展開＋絕對路徑 OUT 重跑，241／12 正常出爐，跑完即刪。
- 注意：第一次跑全套嗰陣冇畀參數（`run_suite.sh` 要 `<repo-root> <outfile>` 兩參），跑咗個空殼
  （log 係 `line 5/7/10: : No such file or directory`）；已 kill 咗重跑，錯嗰個 log 留喺
  `qa176/suite_work176.log` 唔好當證據。

### 3.3 實駕（`qa176/drive176.py`，`?softPreview=1`，http.server＋playwright sync，port 8971）

**5/5 PASS，0 pageerror**（`qa176/drive176_run1.log`＋`qa176/drive176.json`，截圖 `qa176/shots/` 11 張）。
**Rebase 上 91f264a 後重跑：5/5 PASS，0 pageerror**（`qa176/drive176_run2.log`＋更新咗嘅 `qa176/drive176.json`，10 張截圖重影）。
**第三輪 rebase 上 c682cc2 後重跑：5/5 PASS，0 pageerror**（`qa176/drive176_run3.log`，10 張截圖重影；`drive176.json` 冇變，唔使再更新）。

| case | checks | 關鍵證據 |
|---|---|---|
| woman_932 | 23/23 | day 0 長門即撞曉晴（modal「巧遇 · 林曉晴」，掣 傾談／送禮／行開，冇約會掣）；送保溫瓶 +2（rel 0→2、庫存 3→2、結果寫「送禮唔計日子」）；返地點板冇女角送禮／傾談掣；同日再入唔再觸發 |
| woman_talk_932 | 9/9 | 撳傾談 → doTalk modal 出現（NPC_LINES 開場白）；rel 唔郁（見 §2.3） |
| star_932 | 17/17 | day 0 茶餐廳撞廖炳星；行 12 步到收尾 → 「送禮畀廖炳星」掣；送最愛菠蘿油 +4（fav 1→5——行 steps 已 +1，見 §2.4）；`S.story.rel` 冇假 `rel_liu_bingxing`；giftHist＋starGiftDay 有紀錄；同日再送唔得 |
| whisper_932 | 7/7 | 風聲狀態寫入後，人脈頁見藍若曦＋「多數喺 X 出沒」（grant 本身由 logic test B13 覆，呢度驗 UI 消費端） |
| woman_700 | 23/23 | 同 woman_932，430×700；modal 掣全部喺 viewport 內 |

實駕方法註記：主 script 係 IIFE，page evaluate 叫唔到 rom176／enc79／openLoc 等函數，只可以讀寫
`window.S`＋撳真 UI。候選日喺 Python 用 FNV-1a 種子複製計（同 JS `enc79Hash`／`enc79Rand` 逐值
核對一致：5 個 key hash＋rand 完全相同）；逐個候選日真 UI 入場確認。第一次跑 woman_932 ERROR
（`rom176PresenceAt is not defined`）就係因為呢個 IIFE 問題，drive 已按 IIFE 重寫。

## §4 模擬校準（DESIGN §11.3）

`qa176/sim176.js`：100 次，專注追曉晴，每週去主場 3 日 Mon／Wed／Fri，撞到送喜歡禮物 +2、
每週軟頂 +2。

- 第一次跑有 bug——100 次結果完全一樣（中位數 6 週），因為種子按 dayIndex 定死、每次 run 由 day 0
  起步係同一條序列；已修正為每次 run 唔同起步日（`(i*37)%365`）。
- 修正後結果：**中位數 4 週到 rel 5，p90 6、max 10、0/100 超過 10 週**，
  分佈 {2週:6, 3週:38, 4週:31, 5週:15, 6週:6, 7週:2, 8週:1, 10週:1}。
- **結論：P(出) 0.50 維持，唔調**（DESIGN §11.3 門檻係中位數 >10 週先調上 0.60）。

## §5 Resync 紀錄（12 檔舊測試）

淨 +538 行令 12 檔靜態測試行號釘漂移＋內容檢查失效，全部按 `qa176/resync176.py`
（逐個釘行對內容，純漂移先改行號）＋單次掃描 dict 查表 resync，resync 後全套 236／12（見 §3.2）。

- kwan151：14 個 pin 一律 +7。
- tang152：3 個 pin +7（`lines()[N]` 0-index 寫法一併 +7）。
- tang171／tang173：總行數 59341→59879（`src.count('\n')`）；openLoc DEF 53860→54379。
- bust109：NPCS face 覆蓋檢查認 runtime 注入嘅 PORTRAITS 鍵（`PORTRAITS.npc_* =` 賦值），
  唔係淨係字面 7 鍵；新 face npc_lan／npc_xu／npc_mei 指向存在嘅 fullbody 圖。
- enc79_static：紅線段 `mod_seg` 分兩截掃（ENC79 起點 → ROM176 起點 ＋ 殺青回望 → 模組完），
  ROM176 內容由 test_rom176_static 覆。
- tang164：庫存提示檢查 `'或者喺事務所見過鄧麗萍之後'` → 新文案 `'喺事務所見過鄧麗萍之後'`。
- tang167：giveGift 回傳檢查字串拎走 `, costsDay:true`（殘留清理，delta:applied 意圖不變）。
- text125：3 個錨點 +7（27672→27679、27801→27808、33494→33501），註解鏈一併更新。
- text55：KHM 檢查將 ROM176 block 段排除出掃描範圍＋context 關鍵字加 `'npc_mei'`／`'id:"mei"'`
  （NPCS 註冊條目；+30 窗口啱啱截斷 `npc_mei`，要加 `id:"mei"` 先認到）。
- travel114：COUNT 13 個 pin 重寫；FREE 27→33（舊 2 條 go 改行 back176 守衛，拎出 FREE_LINES，
  另加 back176 規則；新 8 處 encDone 返程入 FREE）；DEF 53860→54379；WRAPPER 44235→44242。
  呼叫點總數 44→52（免費 33＋計數 13＋back176 2＋定義／wrapper／測試區 4），
  `grep -c "openLoc(" index.html` = 52，對數。
- weave46：藍若曦檢查容許 ROM176 block 內嘅行＋`'name:"藍若曦"'`（註冊條目）＋GREET 前綴
  `lan:"藍若曦`＋通告牌（由「撳住個通告牌」放寬到「通告牌」，PA 線內容）；「零歌手向」嗰半保留不變。

## §6 Rebase／落地注意

- **Rebase 已完成（見 §9）**：三段——a618a5d→a41b789（第一輪，中斷工人做咗一半，接手工人完成）→91f264a
  （第二輪，v175）→c682cc2（第三輪，v178）。基底而家係最新 main `c682cc2`。落地唔使再 rebase（除非 main 再郁）。
- `git rebase --continue` 要設 `GIT_EDITOR=true`，唔好 pipe 去 head；resync 用單次掃描 dict 查表。
- 落地流程（統籌）：分支做好 → checkout main → `git merge --squash v20a176` → commit → push main
  （經 deploy key，唔使 approve；唔開 PR）。

## §7 未解決／交接

1. **海媚解鎖閘年份出入**（見 §2.2）：設計話 N10 台慶 ≈ 1990-12-01（day 335），code 閘話 C9 開
   1991 冬（約 day 700）。本票主閘 `isDone("C9")`＋day≥335 退路。落地前統籌確認邊個先啱；
   若 N10 實際係 1990 冬，閘要改返 day 335 為主。
   **已解決（rebase，見 §9）**：統籌拍板退路改 **day≥699**（1991-12-01），主閘唔郁；本票已改。
2. **約會入口簽名待對**：`rom176PlayEncounter` 嘅約會掣 defensive check 係
   `typeof rom159DateGate === "function"`，呼叫形 `rom159DateGate(key, L)` 係估計——v159 未落地，
   落地嗰陣要對返 v159 實際簽名（若簽名唔同，掣會靜默唔出，唔會爆錯）。
3. **doTalk 唔加 rel**（見 §2.3）：設計 §3.5「傾談（rel 少量）」喺 main 唔成立；若設計堅持傾談要加 rel，
   要另開票改 `doTalk`（影響全部 NPC 傾談，唔係 v176 範圍）。
4. **S.romLast／S.romPity 物件形式**（見 §2.5）：設計 §7 清單以外，功能已覆，記錄在案。
5. **星巧遇中途 fav**（見 §2.4）：行 steps 嗰陣 enc／beat 來源可能先加 fav，送禮 +4 係疊加上去；
   週軟頂共用 10 點，實駕 fav 1→5 正常。
6. **RIPPLE／v159 衝突**：v159 未落地；v176 冇寫排他鎖／約會／最愛分層，v159 落地嗰陣約會掣會自動出現
   （defensive check），但 v159 嘅 `rom159ApplyGiftOverrides` 同 ROM176 注入有重疊位（海媚 prefs、
   GIFT 賦值行呼叫點）——合併嗰陣要對一次，唔好雙重注入。

## §8 Commit

- Commit 1（遊戲＋測試）：`index.html`＋`tests/test_rom176_logic.js`＋`tests/test_rom176_static.py`＋
  12 檔 resync 舊測試。
- Commit 2（NOTES＋qa 證據）：`NOTES_V20A176.md`＋`qa176/`（`rom176_block.js`、`apply176.py`、
  `drive176.py`、`sim176.js`、`resync176.py`、`drive176.json`、suite 兩份 log、drive log、shots 11 張）。
- Rebase 後新 commit（見 §9）：699 fix（`c079b0b`，rebase 後 `39db47d`）＋rebase resync＋重驗
  （NOTES §9＋`qa176/resync176_rebase.py`＋suite rebase2 兩份 log＋drive run2 log／json＋10 張重影截圖）。
- 第三輪 rebase 後新 commit（見 §9.4–9.6）：釘行 resync＋重驗（NOTES §9.4–9.6＋
  `qa176/resync176_rebase3.py`＋suite rebase3 兩份 log＋drive run3 log＋10 張重影截圖＋新測試反證 log）。
- Push 去常駐 clone：`git push --force-with-lease origin v20a176`（clone 式副本 origin 係常駐 clone 本地路徑；**唔 push 去 github.com**）。
- `DESIGN.md` 留喺工作副本，唔入分支。

## §9 Rebase 紀錄（接手工人，2026-11-13）

### 9.1 兩段 rebase

- **第一段（a618a5d→a41b789，v179）**：上一任 rebase 工人（d9235cd1）中途 interrupted，約 15:25。
  接手嗰陣分支本地 HEAD 已係 `78a8e1f`（NOTES）← `843921b`（遊戲＋測試）← `a41b789`，
  即第一段 rebase 已經做完，但未 push（常駐 clone 嘅 `v20a176` 仲係舊 `e302e91`）。
  工作樹有未 commit 改動——正係第一段收尾未做完嘅嘢：海媚退路 335→699（一行 code＋
  `rom176_block.js`＋B10／B11 測試）＋rom176 static 釘行 resync（原基底值→a41b789 基底值）。
  接手工人核實咗呢啲改動啱晒（`grep` 對返 index.html 實行：GIFT_REACT L31521、ROM176 block L52934
  等全部吻合），原樣 commit 做 `c079b0b`，再做第二段。
- **第二段（a41b789→91f264a，v175）**：`git fetch origin`（origin/main→91f264a）→
  `GIT_EDITOR=true git rebase 91f264a`（冇 pipe 去 head）。`index.html` 自動合併乾淨；
  6 檔測試衝突（kwan151／tang152／tang171／tang173／text125／travel114——全部係 v175 同 v176
  各自 resync 咗同一批釘行）。解法：6 檔全部取 v176 嗰邊（theirs，內容改動啱），再用 difflib
  對位重寫釘行（見 §9.2）；tang173 補返 v175 嗰行 rebase 歷史註解。`git rebase --continue` 後
  三個 commit 全部順利套用：`4bf1b00`（遊戲＋測試）← `f2e809b`（NOTES＋qa）← `39db47d`
  （699 fix＋resync，全套 240／12 係第一段基底數字，見 §3.2）。
- v175 改動對照（`a41b789..91f264a`，`index.html` 79＋／1－，淨 ＋78）：CSS ＋10（L4954，
  `.prog175-banner`）、toast ＋15（L33718，進度頁 banner 分流）、prog175 函數 ＋51（L44154，
  `prog175ShowBanner`／`prog175AdoptToast`）、render ＋2（L44296，`prog175AdoptToast()` 呼叫）、
  openBody 文案 1 行改（刪「已經開放——」）。ROM176 冇掂 toast／openBody，唔使對文案；
  淨係行號漂移。

### 9.2 第二段 resync（`qa176/resync176_rebase.py`）

- 方法：difflib `SequenceMatcher` 單次掃描建舊→新行號映射，逐個釘行核實舊內容同新內容逐字相同
  先改行號；唔 blanket `txt.replace` 改 prose 數字（v153 教訓）。兩個映射：map1＝c079b0b→合併後
  （v176 嗰邊 13 檔）、map2＝91f264a→合併後（v175 嗰邊 prog175／story179）。
- 結果：**全部釘行內容逐字相同，純漂移，零 DIFF**。改咗 7 檔：
  rom176_static（6 釘：6018→6028、31521→31531、52934→53012、53299→53377、54331→54409、
  54425→54503）、kwan151（13 釘，一律 ＋10）、tang152（3 釘：25765→25775、31448→31458、
  31592→31602）、tang171／tang173（總行數 59894→59972、DEF 54394→54472）、text125
  （3 錨點 ＋10）、travel114（COUNT 13＋FREE 33＋DEF 54394→54472＋WRAPPER 44257→44335）。
  唔使改：bust109／enc79／tang164／tang167／text55／weave46（內容檢查為主，釘行唔受影響）、
  prog175／story179（map2，釘行喺 v176 插入點之前／內容檢查）。
- 漂移規律（v175 淨 ＋78）：L4954 之前 ＋0、4954–33718 ＋10、33718–44154 ＋25、44154–44296
  ＋76、44296 之後 ＋78。合併後總行數 59434＋538＝**59972**。
- 手修標籤（script 唔掂 cosmetic 數字）：tang171／tang173 總行數標籤 59894→59972＋DEF 標籤
  54394→54472（連同「v175 ＋78」歷史），travel114／tang171／tang173 各加一行 rebase 歷史註解。

### 9.3 重驗（第二段 rebase 後）

- 新測試：logic **76/76 PASS**、static **ALL PASS**；反證：logic 對 pristine（91f264a）
  乾淨 FAIL（`const not found: ROM176_WOMEN`）、static 對 pristine **47 FAIL**。
- 相關測試逐個直接覆驗：kwan151／tang152／tang171（22/22）／tang173（21/21）／text125／
  travel114／bust109／enc79／tang164／tang167／text55／weave46／prog175／story179——全部 PASS。
- 全套 A/B：pristine **239／12**、工作版 **241／12**，FAIL 清單完全相同（12 項 pre-existing，
  見 §3.2），零回歸。
- 實駕重跑（`drive176_run2.log`，pwenv49＋headless shell）：**5/5 PASS，0 pageerror**——
  woman_932（day 0 撞曉晴、送保溫瓶 ＋2、rel 0→2、地點板冇女角掣、同日唔再觸發）、
  woman_talk_932（傾談後 rel 唔郁，npcs 8→13）、star_932（撞廖炳星、送最愛菠蘿油 ＋4、
  fav 1→5、冇假 `rel_liu_bingxing`）、whisper_932（人脈頁風聲）、woman_700（modal 掣全部喺
  viewport 內）。10 張截圖重影。
- 模擬校準唔使重跑（冇改機率相關 code；P(出) 0.50 維持，見 §4）。
- 環境：git identity（Muse／muse@localhost）＋core.sshCommand（`gh_tunnel.py`＋UserKnownHostsFile）
  開工已核實齊全；rebase／suite／實駕期間冇 EPERM／SIGTRAP 故障。

### 9.4 第三段 rebase（91f264a→c682cc2，v178）

- `git fetch origin`（origin/main→c682cc2）→ `GIT_EDITOR=true git rebase c682cc2`（冇 pipe 去 head）。
  `index.html` 自動合併乾淨；3 檔測試衝突（tang171／tang173／travel114——全部係 v178 同 v176
  各自 resync 咗同一批釘行）。解法：3 檔全部取 v176 嗰邊（theirs，內容改動啱），再用 difflib
  對位重寫釘行（見 §9.5）；v178 嗰兩行 rebase 歷史註解＋v175 嗰行（tang171／travel114 第二輪
  嗰陣跌咗，tang173 有保留）事後手補返。`git rebase --continue` 後四個 commit 全部順利套用：
  `7d7ea0f`（遊戲＋測試）← `5375fdf`（NOTES＋qa）← `cf303c3`（699 fix＋resync）← `5f6db74`
  （第二輪 rebase commit 本身）。
- v178 改動對照（`91f264a..c682cc2`，`index.html` 22＋／1－，淨 **＋21**）：AWARDS64 註解＋1／
  ko sprite＋3／awards63Fellows 特別名額＋21（L46847 附近，`ko_chunkit` 1991 年起入池），再 strip
  刪返註解＋1／sprite＋3（淨 ＋21 全部係 fellows 條款）。ROM176 冇掂頒獎禮，唔使對邏輯；淨係行號漂移。
  v178 新測試 21 項（`test_awards178_logic.js` 8 項＋`test_awards178_static.py` 13 項）全部內容斷言，
  冇釘行，唔使 resync。
- 海媚退路核實：合併後 `>= 699` 仲喺度（L53095，舊 L53074＋21），B10／B11 測試照舊（rom176
  static／logic 已覆），唔使重做。

### 9.5 第三段 resync（`qa176/resync176_rebase3.py`）

- 方法：同第二段——difflib `SequenceMatcher` 單次掃描建舊→新行號映射，逐個釘行核實舊內容同新內容逐字相同
  先改行號；唔 blanket `txt.replace` 改 prose 數字（v153 教訓）。兩個映射：map1＝1367de3→合併後
  （v176 嗰邊 14 檔）、map2＝c682cc2→合併後（v178 嗰邊 prog175／story179）。
- 結果：**全部釘行內容逐字相同，純漂移，零 DIFF**（`--check` 35 個 OK remap）。改咗 4 檔：
  rom176_static（4 釘，一律 ＋21：53012→53033、53377→53398、54409→54430、54503→54524；
  6028／31531 喺 v178 插入點之前，唔郁）、tang171／tang173（總行數 59972→59993、DEF 54472→54493）、
  travel114（COUNT 13＋FREE 33 不變，DEF 54472→54493、WRAPPER 44335 唔郁；27 個釘行一律 ＋21）。
  唔使改：kwan151／tang152／text125／bust109／enc79／tang164／tang167／text55／weave46
  （內容檢查為主，釘行唔受影響）、prog175／story179（map2，釘行喺 v178 插入點之前／內容檢查）。
- 漂移規律（v178 淨 ＋21）：L46847 之前 ＋0、之後 ＋21。合併後總行數 59972＋21＝**59993**。
- 手修標籤（script 唔掂 cosmetic 數字）：tang171／tang173 總行數 prose 59972→59993＋DEF prose
  54472→54493（連同「v178 ＋21」歷史鏈）；tang171／tang173／travel114 各補返 v178 兩行＋v175 一行
  rebase 歷史註解＋一行第三輪 rebase 註解。

### 9.6 重驗（第三段 rebase 後）

- 新測試：logic **76/76 PASS**、static **ALL PASS**；反證：logic 對 pristine（c682cc2）
  乾淨 FAIL（`const not found: ROM176_WOMEN`）、static 對 pristine **47 FAIL**。
- 相關測試逐個直接覆驗：kwan151／tang152／tang171（22/22）／tang173（21/21）／text125／
  travel114／bust109／enc79／tang164／tang167／text55／weave46／prog175／story179／awards63／
  awards64_chibi——全部 PASS；v178 新測試 logic 8/8＋static ALL PASS（13 項）亦 PASS（v176 冇整爛佢哋）。
- 全套 A/B：pristine **241／12**、工作版 **243／12**，FAIL 清單逐項相同（12 項 pre-existing，
  見 §3.2），零回歸；suite diff 淨差兩個新測試 PASS＋TOTAL 行。
- 實駕重跑（`drive176_run3.log`，pwenv49＋headless shell）：**5/5 PASS，0 pageerror**——
  woman_932（day 0 撞曉晴、送保溫瓶 ＋2、rel 0→2、地點板冇女角掣、同日唔再觸發）、
  woman_talk_932（傾談後 rel 唔郁，npcs 8→13）、star_932（撞廖炳星、送最愛菠蘿油 ＋4、
  fav 1→5、冇假 `rel_liu_bingxing`）、whisper_932（人脈頁風聲）、woman_700（modal 掣全部喺
  viewport 內）。10 張截圖重影。
- 模擬校準唔使重跑（冇改機率相關 code；P(出) 0.50 維持，見 §4）。
- 環境：git identity（Muse／muse@localhost）＋core.sshCommand（`gh_tunnel.py`＋UserKnownHostsFile）
  開工已核實齊全；rebase／suite／實駕期間冇 EPERM／SIGTRAP 故障；唯一環境問題係 `/tmp` tmpfs
  爆滿（見 §3.2），已清走，唔影響結果。
