# NOTES_V20A183 — v176 設計 review B1–B4＋C1–C9 一次過修

狀態：**已落地。遊戲 commit `7497c9e`（分支 `v20a183` HEAD `94caebd`，基底 main `6ed68f8`），2026-11-13 17:10 我 curl 核實：線上 5,329,880 bytes sha `9890d43e…`，同 repo HEAD:index.html 完全一致。Live 係 v183。**

- 分支 `v20a183`，基底 main `6ed68f8`（v182）。**唔落地**：呢票只做實作＋驗證＋commit＋push 分支，等統籌 squash merge。
- 來源：`~/workspace/linji-design-review-v176/REVIEW.md`（用戶 2026-11-13 16:30 拍板一次過修晒 B1–B4＋C1–C9）。
- index.html 淨 **+117 行**（60010→60127，`count('\n')`）；`qa183/apply183.py` 28 處取代，全部 assert 恰好出現一次，由 pristine 重跑同工作版 byte-for-byte 一致（已驗證 `APPLY-REPRODUCIBLE`）。
- 落地過程（統籌補記）：squash merge 後 `git push origin main` 連續 7 次喺上傳階段被 egress proxy reset（Broken pipe／remote hung up，`ls-remote` 讀取正常；空 commit 細 push 成功，證實寫入通道本身通，問題係大 pack 上傳）。解法：拆細推——文字包（index.html＋測試＋NOTES＋qa 腳本）一次成功（`7497c9e`）；10 張實駕截圖逐張推（中途又斷過 4 次，逐個 sha 重推先齊，`e3484db`→`0f90dc7`）。教訓：proxy 惡劣嗰陣大 pack 推唔到，拆細逐張推係可行出路；截圖 commit 拆散咗 10 個，之後落地唔好學。
- 紅線全部守住：SAVE key `starVolunteer_map_v19w`、softRev `s107`、`?v=v20a10` 唔郁；三份 pack JSON（`gift_react_copy.json`、`npc_lines_core.json`、`tutorial_zh_HK.json`）原封不動（static test 有紅線斷言）；鎖邏輯（`flag_romance_locked`／rel 5 鎖／rel 6 commit）唔郁；頒獎禮舞台 code 冇掂。

## 逐項修法

### B1 — 女角感情 rel 玩家面睇唔到（只顯示）
- 人脈頁（`people72Html`）女角行加 `<div class="people-next">感情：好感 X／5</div>`（`rom183RelLine183`，讀 `StoryOC.getRel("rel_"+key)`，跌返 `S.story.rel["rel_"+key]`）；巧遇 modal sub 行尾加「而家好感 X／5。」（`rom183RelText183`）。
- 實駕：人脈頁曉晴「感情：好感 2／5」、采兒「1／5」；modal 同步顯示。鎖邏輯零改動。

### B2 — 星送禮選擇器分唔開最愛＋4同喜歡＋2
- `GiftShop.prefKind` 加 `favorites` 檢查先回 `"favorite"`；`calcDelta`／`reactionEntry`／`reactionLine` 三處一併認 `favorite`（否則會跌返 +1／neutral 句）；選擇器 tag 改 `★ 最愛`／`喜`／`慎`／`普`；確認 modal 加 `kindLine183`（最愛：「★ 最愛：佢最鍾意呢樣禮物。」）。
- **注意**：`content/gift_prefs.json` 女角條目根本冇 `favorites` 欄（得 12 星先有）——女角 picker 預期冇 ★ 行，B2 目標係星 picker。實駕 star case：星 picker 有 ★ 最愛行（就係嗰粒最愛禮物），確認 modal 寫明最愛，送出＋4。
- 舊測試跟進：`test_tang167_static.py` calcDelta 字串更新（行為不變，最愛同喜歡同數）；`test_rom176_logic.js` 要抽埋 `rom183RelText183` 等（PlayEncounter 而家叫佢）。

### B3 — 行開返地點板後「在場」行講緊另一個人
- `rom176TryIntercept` 寫 `sd.doneToday[pick.key] = locId`（以前寫 `1`）；地點板在場行改行 `rom183WhoLine183(L, npcId)`——`S.romDay.doneToday[k]===L.id` 嗰位女角優先，出「在場：名（角色） · 今日已經撞過佢，聽日再嚟」，否則跌返舊行。
- 實駕：曉晴撞完行開，返去長門板，在場行寫曉晴＋「今日已經撞過佢，聽日再嚟」，唔再寫藍若曦。
- 實駕附帶發現：再入場嗰陣可能彈隨機劇情 modal（例如「飛紙仔殺到埋身」）冚住地點板——drive 要先清 modal 再讀板（已寫入 `drive183.py`）。

### B4 — 海媚「去找 · 金鐘創意」掣 day 0 已生效
- `goBit` 前加 `lockedMeiGo183`（mei＋`rom176MeiUnlocked()` false）：未解鎖出純文字 div「主線再行前啲先撞到佢」，冇掣、唔扣額度；已解鎖／其他人照舊有掣。
- **TDZ 教訓**：`lockedMeiGo183` 原本插喺 `rk176` 宣告之前，直接讀 `rk176` 會 `ReferenceError: Cannot access 'rk176' before initialization`（`test_menu72_logic.js` 捉到）。修正：將 `rk176` 宣告行搬去 `home` 行之前，行數不變。`apply183.py` 已同步呢個修正。
- 實駕：day 0 人脈頁海媚行有鎖定句、冇金鐘創意掣；其餘 8 行掣齊。

### C1 — 舊三女角開場白係書面語
- `ROM183_PACK_GREET` 粵語版＋`rom183ApplyLineOverrides()` runtime 覆寫 `NPC_LINES` greet[0]（colleague／stylist／reporter），喺 `textfix55SimplePack(d)` 之後呼叫；pack JSON 唔郁。
- 實駕：曉晴 modal bubble 係「咁啱嘅，喺呢度撞到你。」（Vera／采兒同款粵語版經 logic test 覆）。

### C2 — 徐寶珊初遇預設咗未發生嘅春茗相遇
- `ROM176_GREET.xu` 改初遇版「後生仔，行路望路呀。咦，係你——啱啱先撞到，唔好意思。」；見過版搬去 `ROM183_GREET_MET.xu`（「…上次春茗撞過嗰個。」）；`rom176TryIntercept` 設旗前先記 `metBefore183 = rom176WomanMet(pick.key)`，傳入 `rom176PlayEncounter(key, locId, metBefore183)` 分版（無傳入就查 `R_xu_meet` done）。
- 實駕：首次撞徐寶珊無「春茗」；播種 `gift_met_xu` 後再撞有「春茗」。

### C3 — 女角送禮結果句混普通話口吻
- `rom183ApplyGiftReactFix()`：10 句逐字覆寫（EXACT183，post-TEXTFIX55 形——見下）＋通用 fallback（`是不是→係咪`／`什麼→咩`），同時改 `byKey`＋`entries` 兩份，冪等；喺 `textfix55Walk(giftReact, …)` 之後呼叫。
- 實駕：送保溫瓶畀曉晴，結果句「保溫瓶？你係咪見到我冬天抱住紙杯震？真係實用。」——零「是不是」／「什麼」，55 條全部過 filter（logic test 讀真 pack 驗）。
- **注意**：EXACT183 鍵要用 TEXTFIX55 之後嘅字串（例如 pack 原文「太實用了」經 TEXTFIX55 變「真係實用」）；用 pack 原文做鍵會對唔上，淨係得 fallback 生效。呢點已喺實作入面處理好。

### C4 — 海媚開場白有舞台指示
- `ROM176_GREET.mei` 刪括號：「關海媚：「咁啱，喺呢度撞到你。」」；NL176 mei greet[1] 淨留「有嘢搵我？」。
- 實駕（播種 `S.story.done.C9=1` 解鎖）：海媚 modal 無括號敘述句。

### C5 — 人脈頁「去找」掣金字對比度 1.87:1
- `.people-go` 字色 `#c9a227`→`#5a4328`；底 `rgba(201,162,39,.12)`→`.28`；邊 `rgba(201,162,39,.55)`→`rgba(90,67,40,.65)`。
- 靜態實計 **6.47:1**；實駕 live 逐層 alpha 合成實計 **6.26:1**（字 #5a4328／合成底 rgb(231,211,155)），≥4.5:1。
- 附帶：drive 初版 contrast 計法錯兩次（第一次忽略 alpha 當實金計 3.83；第二次 fg object 傳入 lum() 變 NaN）——已修正做逐層合成，唔係遊戲問題。

### C6 — 教學完全唔提隨機巧遇
- **修正教訓（實駕捉到）**：第一版淨係 patch 咗 TUT_NPC，但 live 教學只行 `TUT_MAIN_IDS` 四步（WELCOME／MAP／BOARD／DONE），TUT_NPC 根本唔顯示，drive C6 FAIL。修正：巧遇句「去佢哋常出沒嘅地方，有機會撞到佢哋——撞到先可以傾談／送禮。」落喺 **TUT_MAP body 第三句**（inline fallback＋`rom183ApplyLineOverrides` runtime 覆寫 live pack，冪等）；TUT_NPC 嗰句保留（覆蓋重看／其他路徑）。
- 實駕：行晒 4 步教學，TUT_MAP 嗰頁有撞到句。

### C7 — 700 禮物選擇器尾 3 件要碌
- `@media (max-height:720px)`：`#gift-pick-list` 兩欄 grid（10 行變 5 行）；「取消」掣 pinned 不變。
- 實駕 430×700：10 行 bottom 全部 ≤700，取消掣 bottom ≤700 唔使碌。

### C8 — 「去找」掣名同新機制打架
- 人脈頁掣名全站改「去 X 行下」（揀「行下」唔揀「碰下」）；連埋 C5 嗰掣一齊改。
- 舊測試唔驗字面（`test_menu72_logic.js:118`／`test_menu72_static.py:79` 只驗 `data-loc`＋`people-go`），唔使改佢哋；實駕：8 個掣全部「去 X 行下」，零「去找」。

### C9 — 出行額度同撞人機制疊加
- 開局 intro 入場 `openLoc(locId)` → `openLoc(locId, {travelFree:true})`（加註解說明係系統引導入場）；travel114 上限／計數本身唔郁。
- 實駕：新遊戲後 pill「仲可以去 2 個地方」；撳 intro「去睇劇情」掣入場後仍然 2 個；之後手動入茶餐廳變 1 個。
- travel114 釘同步：COUNT 13→12／FREE 33→34；舊 59358 intro 行由 COUNT 移去 FREE，新行 59475。

## 漂移帳（淨 +117 行，difflib 核實）
C7 CSS +2（舊 L3849）／prefKind +1（舊 L30519）／TryIntercept +1（舊 L53246）／PlayEncounter +2（舊 L53279）／ROM183 block +107（舊 L53549）／openGiftPick 確認 modal +3（舊 L58500／58502）／goBit +1（舊 L58684）。其餘取代全部原地改。C6 修正零行數漂移。

## 測試
- 新：`tests/test_rom183_logic.js`（33 項 PASS）＋`tests/test_rom183_static.py`（60 項 PASS）；pristine 反證：logic FAIL「const not found: ROM183_GREET_MET」，static 41 項 FAIL——乾淨。
- 舊測試跟進（全部 PASS）：kwan151／tang152／rom176（static＋logic）／travel114（static＋logic）／tang171／tang173／menu72（logic＋static）／text125／tang167／weave46（static＋logic）／weave48／dlg106。
- **resync 引入問題（已修）**：`qa183/resync183.py` 升序取代撞號，kwan151 A7（原 `line(25961)`）錯變 `line(25965)`，已改返 `line(25963)`；其餘檔案號碼互不重疊，經檢查無同類碰撞。
- **resync 漏咗嘅釘（已修）**：rom176 static NPCS lan `line(6030)`→`line(6032)`（C7 +2）；text125 三粒釘 27696→27698、27825→27827、33518→33521。
- **weave46（全套唯一新增 FAIL，已修）**：C3 EXACT183 覆寫表多咗一行「藍若曦」字面，觸發全檔核實 allowlist。修法：test 准許 ROM183 block 入面嘅行（註解 `/* 殺青回望` 喺 `nocomment` 入面已剝走，end marker 要用 `function enc79OnWrap`——第一版用註解做界搵唔到，j=-1，block 係空，修咗先過）。

## 全套
`bash qa131/run_suite.sh`：pristine **244／12** vs 工作版最終 **246／12**，FAIL 清單逐項相同（12 項穩定 pre-existing），＋2 係新測試。零回歸。

## 實駕（`qa183/drive183.py`，Playwright，本地鏡像，0 pageerror）
8 case、78 項檢查全部 PASS，截圖 `qa183/shots183/`（10 張），結果 `qa183/drive183.json`：
- `c6c9_932` 7/7（C6 教學＋C9 pill 2→2→1）
- `people_932` 9/9（B1 rel 行、B4 海媚鎖定、C5 live 6.26:1、C8 行下）
- `woman_932` 15/15（C1 粵語開場白、B1 modal rel、送禮 picker、B2 喜歡確認句、C3 保溫瓶粵語句、rel 2→4）
- `woman_700` 17/17（C7 10 行全部見到＋取消掣 pinned）
- `star_b2_932` 12/12（B2 星 picker ★ 最愛行＋確認 modal＋送出 +4）
- `b3_932` 8/8（B3 在場行跟巧遇盤）
- `xu_932` 6/6（C2 初遇／見過兩版）
- `mei_932` 4/4（C4 無括號開場白）

## 殘留／交接
- `rom159DateGate` 估計形：呢票冇掂到，冇嘢交代。
- v159 重疊位：B1 只係顯示，讀現行 `S.story.rel`；v159 落地嗰陣如果感情顯示搬去新 UI，`rom183RelLine183`／`rom183RelText183` 要跟住搬或者刪，唔好兩邊並存。
- B2 女角 picker 冇 ★ 係數據現實（`gift_prefs.json` 女角無 `favorites` 欄），唔係 bug；如果日後想女角都有最愛，要補 pack 數據（唔准直改 pack 嗰陣記得行覆寫表）。
- C3 EXACT183 鍵係 post-TEXTFIX55 形——日後 TEXTFIX55 改 mapping，呢 10 條鍵可能又要對位。
- C6 嘅 TUT_NPC patch 保留咗但 live 唔顯示；如果日後 `TUT_MAIN_IDS` 加返 NPC 步，兩句唔會重複（冪等檢查 `indexOf("撞到")<0`）。
