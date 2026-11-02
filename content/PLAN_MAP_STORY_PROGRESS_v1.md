# PLAN_MAP_STORY_PROGRESS_v1

> **時間：** 2026-11-03（Asia/Hong_Kong）  
> **狀態：** 計劃 only — **本輪唔改 Soft／story JSON／唔出圖／唔大改 index 引擎**（hint 欄等合稿後另刀）  
> **對齊：** `QA_PLAYER_V17N_HIGHBAR_STATIC_v1.md` P0；Tester gap `QA_PLAN_GAP_vs_PLAYER_V17N_v1.md`  
> **HOLD：** 鄧節序並放、出圖暫緩、Soft≠PASS（leftover 以 `SOFT_NITS_FIX_v2.md` 為準：五項已清；鄧／出圖仍 HOLD）  
> **依據：** `PLOT_DETAIL_UNLOCK_v1.md`、`PHASE_AUTO_TABLE_v1.md`、`WIRING_OC_ENGINE_v1.md`、`WIRING_STORY_PLAY_v1.md`、`WIRING_INDEX_HOOK_v1.md`、`index.html`（`StoryOC.listOpen`／`data-m="story-play"`／`LOCS`／`mapTips`／`#loc-sheet`／劇情結算）、`story_detail_c1_to_c17.json` C1–C5  
> **修訂：** 2026-11-03 tester 補 P0；同日劇本拍板三項：C2/C4 soft loc、`playerOffer`、C5 `rel_choi_threshold=2`（見 `PLAN_BOARD_3_v1.md`）

---

## 1. 目標／非目標

### 目標
1. 玩家行地圖日常時，見到「呢度有劇情可播」體感（唔止選單「可出劇情」）。
2. C1（及主線鏈）播完／`listOpen` 只得少節或下一主線鎖住時，有**玩家可讀**「下一節未開」方向提示（唔暴露 raw `flag_*`／debug reasons）。

### 非目標
- 唔做鄧閘／鄧節序；唔出圖；唔改 Soft／story JSON（hint 欄等合稿；Soft 以 v2 為準另線）。
- **唔**用「完整劇情 UI」擋最小世界觸發：本計劃＝**最小世界觸發優先**；完整 UI 另輪仍可，但 P0 唔再延。
- 接線 debug 面板保留（建議收 `?debug=1`）；玩家入口改稱「事態」（見 §9）。
- 唔喺本週重寫 `StoryOC` 核心 token 語義；只列建議契約畀 web／iOS。
- 唔做完整日結劇情摘要長文、唔做通告板劇情側欄（後備）。

---

## 2. 優先序（必做 1–2）

| # | 方案 | 決策 | 理由（體感／成本／現有 hook） |
|---|---|---|---|
| **0a** | **教學後自動推 C1**（事態卡／`StoryPlay.start`） | **必做 P0** | 對標「看不到分別」；唔開選單都必見主線。 |
| **0b** | **開局佇列只推 C1**；平行 meet 掛地點／傾偈 | **必做 P0** | 避免 8 條 meet 同列晒冷；資料可留 `[]` 畀 debug。 |
| **0c** | **玩家 listOpen 用 `ev.ok`**（擋 phaseSoft／stub） | **必做 P0** | 開局唔應可播 Tang／stub；見 §9.3。 |
| **0d** | **phase 自動表**（`PHASE_AUTO_TABLE_v1.md`） | **必做 P0** | 播完 choice 要 `setPhase`；唔靠 Playtest。 |
| **0e** | **事態命名＋收 debug**；StoryPlay **一屏無滾** | **必做 P0** | 選單去 jargon；對白翻頁禁內層 scroll。 |
| **1** | **(A) 地點 badge／地圖 tip**（開＝可播節掛 `locId`） | **必做** | 地圖已有 `.pin.has-tip`＋`S.mapTips`；體感直達日常 loop。 |
| **2** | **(B) 播完／日結「下一節未開」玩家 hint** | **必做** | 結算／輕量日結；開局痛點。 |
| 3 | 通告板側欄（gigs board 掛 open 節） | 後備 | 易同育成鎖混淆。 |
| 4 | 完整日結劇情摘要 | 後備 | 文案量大。 |
| 5 | 完整劇情 UI（取代地圖育成殼） | **另輪** | **唔再**用「另輪」擋 0a–0e／(A)(B)。 |

**一句優先序：** 先 **0a–0e**（有分別＋時序安全）→ (A) tip／badge → (B) lockedHint；板側欄／全日結／完整 UI 後備。

---

## 3. 必做項規格

### 3.1 (A) 地點 badge／地圖 tip

**玩家體感一句：** 地圖針腳亮／角標「劇」→ 入地點見到「有劇情：先練／先賺」→ 一撳開 `StoryPlay`。

**驅動資料**
- 來源：`StoryOC.listOpen({ checkNodePhase:true }).open`（只 `openable`／玩家可視；pack 優先 **main C\***，其次 R／A 可選）。
- 每節需 **`locId`**（見 §3.1.1）；缺則唔掛針、仍可經選單播。
- 可選：`node.mapTipTitle`（短）／預設用 `node.title`。

**UI 掛點（web 現況）**
- `drawMap`：`S.mapTips[loc]` 已驅動 `.has-tip`；建議擴充 tip shape：`{ kind:"story"|"gig", nodeId?, title, untilDay? }`（`kind:"gig"` 維持現有情報）。
- 衝突：同 loc 同時有 gig tip + story → **story 優先**顯示（或雙標：藍 tip + 小「劇」角標）。
- `#loc-sheet`／`loc-who`：現有 `💡情報「title」` 旁加「📜 可出劇情：{title}」act 列（`act-priority` 風格）。
- `#map-hint`：可選一行「有地點亮住＝有劇情可播」。

**刷新時機**
- `StoryOC.markDone`／`applyChoice` 後；`drawMap`／`openLoc` 前；讀檔 `ensure` 後；日推進 `pruneMapTips` 時重算 story tips（story tip **唔必**跟 `untilDay` 過期，跟 open 狀態走）。

**點擊行為**
- 地圖 pin → `openLoc` → act「播事態：{title}」→ `StoryPlay.start(nodeId)`。
- **日常 loop：** 入地點／訓練／閱板時**唔**自動搶播（免打亂育成）。
- **例外（P0）：** 教學結束（或新局首次返地圖）→ **必須**自動推 C1（全屏事態卡或直接 `StoryPlay.start('C1')`）；見 §9.1。

**驗收**
- 開局：`tvb_longmen`（或 C1.locId）有 tip／badge；入 sheet 可播 C1。
- C1 done → tip 轉去 C2.locId（若有）；C1 針熄。
- 選單「可出劇情」仍可用。

#### 3.1.1 loc 映射（C1–C5；缺則待補）

| 節 | setting（摘要） | 建議 `locId` | 備註 |
|---|---|---|---|
| C1 | 星河台通告板旁／何生事務所 | **`tvb_longmen`** | 星河＝`tvb_longmen`；事務所無獨立 loc |
| C2 | 片場後巷／茶餐廳 | **soft＝`tvb_longmen`（定稿）** | **唔開新針**；茶餐廳待補 `cafe_*`（表留） |
| C3 | 星河電影組通告板前 | **`tvb_longmen`** | 同廠；高俊傑 `homes` 含此 |
| C4 | 何生事務所 | **soft＝`ad_central`（定稿）** | **唔開新針**；事務所感；待補 `agent_office`（表留） |
| C5 | 片場邊小桌 | **`tvb_longmen`**（備：`tvb_harbour` 采兒 homes） | 台慶籌備季氛圍；`rel_choi_threshold=2`（拍板） |

> iOS／web 實作前：JSON 加可選欄 `locId`（string）；未填則用上表 fallback 表（代碼內常數即可，唔使一次改晒十七節）。

---

### 3.2 (B) 播完／日結「下一節未開」hint

**玩家體感一句：** 劇情結算底下多一句：「下一幕『留人脈／趕通告』未開——多喺片場殺青後留低應酬。」（方向性，唔報 flag）。

**驅動資料**
- 播完當節後：對 **主線下一節**（C1→C2→… 固定鏈；或 `openConditions` 裡第一個未 done 嘅 C\*）跑 `StoryOC.evalNode`。
- 若下一節 **openable** → 顯示 `nextHint`／「可去 {locName} 繼續」；若 **locked** → 顯示 `lockedHint`／映射後玩家句（§4）。
- `listOpen().open` 主線空、只得 R／A：一句「主線暫時未有新幕；可繼續跑通告／見人。」
- 日結／週結：只插 **一句**（唔做長摘要）；資料同上，刷新自當日最後一次 `listOpen`。

**UI 掛點**
- **主：** `StoryPlay`「劇情結算」modal（`pickChoice` 後 body）。
- **次：** `afterDayModal`／本週結算 notes 末行（有變更先顯示，避免每日洗版）。

**文案來源**
- 優先節點 JSON：`lockedHint`／`nextHint`／`playerHint`（§4）。
- 後備：代碼 `reason → 玩家句` 映射表（§4.3）；再後備：通用「時機未到，先照常跑板。」

**點擊行為**
- 結算「知道了」關；若下一節已 open 可選第二鈕「去地圖」／`scrollMapPinIntoView(locId)`。

**驗收**
- C1 播完 → 見 C2 方向 hint（唔見 `need_done:C1` 字串）。
- C1 未播、開局 → 地圖 tip 夠，唔強制日結洗「去播 C1」每日（最多 tip／badge）。
- debug 面板 reasons **保留**給 tester。

---

## 4. 開局 C1 後 lockedHint 規格＋ JSON schema

### 4.1 行為規格

| 時機 | 顯示 |
|---|---|
| C1 結算完成 | 若 C2 openable：「下一幕已開：{C2.title}——可去 {loc}。」；若仍 lock（理論少見，因 oc=`["C1"]`）：不應發生；若 engine 異步，用 C2.`lockedHint` |
| listOpen 主線 open 空、locked 有 C2… | 日結／結算顯示 **最近一節主線** 嘅 `lockedHint`（玩家句） |
| 部分鎖（例 C5 要 choi／夏） | 用該節 `lockedHint`；唔列 raw `rel_choi_threshold` |
| 開局僅 C1 open | 地圖 tip 指向 C1；**唔**用「可出過少」嚇玩家——改為正面「星河廠有幕等你揀。」（C1.`playerHint`） |

**文案原則（書面港語）**
- 香港書面白話；方向性（「多留低殺青應酬」「留意通告板搶位」）。
- **禁**薄本趕板苛約口吻；**禁**對玩家露出 `flag_*`／`need_done:`／`AND …`。
- 可用節 `title`＋一句條件方向；人名用戲內名（何生、高俊傑、周采兒）。

### 4.2 建議 JSON 欄（放邊）

**檔：** `content/story_detail_c1_to_c17.json`（及 phase parts 若分載；以 wire 合併源為準）  
**節：** 至少 **C1–C5**（主線前 5）；C6+ 可後補。

```json
{
  "id": "C2",
  "locId": "tvb_longmen",
  "playerHint": "可選短句：節點已開放時地圖／sheet 用",
  "nextHint": "本節播完且下一節已開放時用（寫喺『上一節』或由引擎讀下一節 title）",
  "lockedHint": "本節未開時對玩家嘅方向提示（唔含 flag id）"
}
```

| 欄 | 誰讀 | 何時 |
|---|---|---|
| `locId` | 地圖 tip／iOS map | open 且未 done |
| `playerHint` | tip／sheet 副文 | 節 open |
| `lockedHint` | 結算／日結 | 節 locked 且為「下一主線目標」 |
| `nextHint` | 可選；否則結算組句「下一幕『{next.title}』…」 | 本節剛 done 且 next open |

**主線前 5 節建議文案（草案，實作可微調）**

| ID | lockedHint（玩家） | playerHint（已開） |
|---|---|---|
| C1 | （開局少用 locked） | 星河電視台廠景有幕等你：先練定先賺。 |
| C2 | 殺青後喺片場後巷留低——人脈同下一張通告會撞期。 | 後巷有人約飯；通告板又貼咗新單。 |
| C3 | 多去星河電影組通告板——搶位爭執快發生。 | 通告板前氣氛緊，有人睇住你嘅名牌。 |
| C4 | 何生會拎份條款含糊嘅外判通告——留意經理人事務所。 | 何生檯面有份通告紙等你表態。 |
| C5 | 同周采兒處好關係，或捱到台慶籌備季，先有小訪。 | 片場邊有小訪位，筆記本已經打開。 |

### 4.3 debug reasons → 玩家句（映射例）

| `reasons[]` 樣式（引擎） | 玩家句 |
|---|---|
| `AND need_done:C1` | 先完成上一幕「先練／先賺」。 |
| `AND need_done:C2` | 先完成「留人脈／趕通告」。 |
| `AND need_flag:flag_*`／`need_flag:…` | 用該節 `lockedHint`；無則「相關人物線未到位，先照常跑通告同傾偈。」 |
| `rel_*_need>=N` | 「同對方再熟一點再傾。」（唔報數字／鍵名） |
| `fame_need>=…` | 「聲望再累積一陣，機會先會來。」 |
| `phase_need:…`／`node_phase:…` | 「時候未到，先過完呢一季。」 |
| `season≠…`／year | 「呢幕偏某季氛圍，而家檔期未夾。」 |
| `ANY none of …` | 優先 `lockedHint`；否則「仲差一個契機（人物或季節）。」 |
| 空 open 主線 | 「主線暫時無新幕；地圖跑通告、見人就得。」 |

實作：`StoryOC.playerReason(node|reasons) → string`（建議）；debug UI 繼續用 raw。

---

## 5. iOS 實作契約（建議欄）

| 欄位 | 說明 |
|---|---|
| **資料來源** | 同 web：`STORY_WIRE`／detail JSON；本地 `StoryOC.listOpen` 等價 API |
| **刷新時機** | map appear；loc sheet open；story dismiss；day／week settle |
| **文案來源** | `title`＋`playerHint`／`lockedHint`；禁止把 raw reasons 丟 UILabel |
| **點擊** | badge／row → present StoryPlay(nodeId)；locked 只展示 hint，唔 start |
| **Fallback** | 保留 debug／「可出劇情」列表入口 |

---

## 6. Phase（邊個做）

| Phase | 內容 | 誰 |
|---|---|---|
| **P0 本輪** | 本計劃 md＋tester P0 補丁（§9）；`PHASE_AUTO_TABLE_v1.md` | 劇本 manager 定稿／tester 對表 |
| **P1** | JSON 加 `locId`／`playerHint`／`lockedHint`（C1–C5 最少）；**等合稿**先改 JSON | 劇本 manager |
| **P2** | web：教學後推 C1、事態選單、`ok` 閘、`setPhase` 表、mapTips story、結算 hint、一屏 StoryPlay | web／iOS |
| **P3** | iOS 對齊契約 | iOS |
| **P4 後備** | 通告板側欄、全日結摘要、完整劇情 UI | 另議 |

出圖／鄧節序：**繼續 HOLD**。Soft：`SOFT_NITS_FIX_v2` 五項已清；**唔**升 PASS；唔阻塞本計劃。

---

## 7. 風險

| 風險 | 緩解 |
|---|---|
| Soft leftover 並行改 JSON | hint 欄用加欄唔改 beats；衝突時以 Soft PASS 後再 merge |
| C2／C4 soft loc | **已拍板** C2=`tvb_longmen`、C4=`ad_central`；新針（`cafe_*`／`agent_office`）後補；唔阻 tip |
| tip 同 gig 情報搶同一針 | story 優先或雙標 |
| 日結每日重複同一句 | 只在「主線目標節變更」或「剛播完」顯示 |
| 選單可出劇情 | **保留**作 fallback／無 loc 節 |

---

## 8. Tester 覆測（計劃落地後）

- [ ] 教學結束／新局返地圖：**自動**見 C1（事態卡或播放）；唔開選單  
- [ ] 開局地圖星河有劇情 tip；可播 C1；事態列表**只**見主線一條（平行 meet 未觸發前唔晒）  
- [ ] 開局玩家路徑**無** `R_tang_meet`／`R_tang_meet_stub`  
- [ ] C1→C7 只靠播放器 → phase 達 P2；C8 可播  
- [ ] C1 結算有 C2 方向句；無 raw flag／need_done  
- [ ] C2–C5 lockedHint 方向正確（含 C5：春可走采兒關係口吻）  
- [ ] StoryPlay C1（含 choice）一屏無滾  
- [ ] 預設 UI 無「接線資料」／Playtest；`?debug=1` 仍見 raw reasons  
- [ ] 出圖／鄧未動；Soft≠PASS

---

## 9. P0 補丁（tester 2026-11-03｜對齊玩家高要求）

> 補劇本原稿未寫清、但 `QA_PLAYER_V17N_HIGHBAR_STATIC_v1` 列為擋「有分別」／時序安全嘅項。實作以本節＋§2 優先序為準。

### 9.1 教學後自動推 C1

| 項 | 規格 |
|---|---|
| 時機 | 教學 7 步結束，**或**新局首次進入地圖（兩者擇一實作；建議教學結束即推） |
| UI | 全屏「有新事態」卡（人話標題，例「先練定先賺？」）→ 確認後 `StoryPlay.start('C1')`；或直接 start |
| 禁 | 要求玩家自己搵「可出劇情」jargon |
| 與 §3.1 | 日常入 loc **唔**搶播；**僅此開局例外** |
| 驗收 | 清檔新局；唔開接線選單；必見 C1 對白／二選一 |

### 9.2 開局佇列只推 C1；平行 meet 觸發（`playerOffer`｜**已拍板 2026-11-03**）

| 項 | 規格 |
|---|---|
| 玩家事態列表 | 開局（phase=P1、空 done）**只展示 C1**（及之後已 unlock 主線） |
| **`playerOffer`** | 平行 meet（Vera／曉晴／采兒／高／子駿／方／何…）JSON 寫 **`playerOffer: false`**；主線 `C*` **省略或 `true`** |
| 觸發（定稿） | 首次入對應 **`locId`** **或** 首次 **`doTalk`** 該 NPC → 引擎 runtime／save 開 offer（然後玩家 list 可見） |
| Debug | 資料可保留 `openConditions=[]`；debug 列表仍可睇全部 |
| 驗收 | 事態預設只見主線；去對應 loc／傾偈後先出現 meet |

### 9.3 phase soft 玩家閘／stub 隔離

| 項 | 規格 |
|---|---|
| `listOpen`／`StoryPlay.start`（玩家） | 必須 `ev.ok`（`openable && !phaseSoft`）；`force:true` 僅 debug |
| Picker | 「可播」vs「時候未到（灰）」分開；灰項顯示 `lockedHint`／phase 玩家句 |
| stub | `R_tang_meet_stub` **永不**入玩家 open（`openConditions=['__debug']` 或 iter 過濾 `supersededBy`） |
| Soft | stub flags_written 等已見 `SOFT_NITS_FIX_v2`；本節只要求**玩家路徑隔離**，唔當 Soft PASS |

### 9.4 phase 自動推進

- 權威表：`PHASE_AUTO_TABLE_v1.md`  
- `markDone`／年曆跨入後 `setPhase`；刷新 map tip／事態  
- 驗收：唔撳「phase→P2」亦可入 C8 時序

### 9.5 事態命名＋收 debug

| 正式 UI | Debug（`?debug=1` 或長按版號） |
|---|---|
| 選單「**事態**」（原「可出劇情」） | 「接線資料」、Playtest、`標記 C1`、`phase→P2`、Console 句 |
| 列標題用人話（`title`） | code id 細字可留 debug |
| 結算人話（路線／關係） | 禁 `flags_written`／「Tang 雙閘」工程句 |

### 9.6 StoryPlay 一屏無滾（零容忍）

| 項 | 規格 |
|---|---|
| 佈局 | 每次 1 speaker＋1～2 短句；選項固定底；「下一句」翻頁 |
| CSS | 禁 `.story-play{overflow:auto}` 內層滾；外層 modal 播劇情時亦唔滾 |
| 文案 | 超長句劇本側截斷（合稿）；本輪計劃只定驗收 |
| 驗收 | iPhone 預覽播 C1 全程（含 2 choice）無捲動條／內層滑動 |

### 9.7 C5 春開局（對齊 P1 資料張力｜**已拍板 2026-11-03**）

- ANY：`rel_choi_threshold` **OR** `season_1988_summer_anni_prep`  
- **春開局政策（定稿）：** 季節肢未到時，走 **采兒關係** 肢；`lockedHint` 已寫「同周采兒處好關係，或捱到台慶籌備季」。  
- **`thresholds.rel_choi_threshold = 2`**（同 Tang 小刻度 +1/+2；**否決** 10／25／40；**取消** null-skip）  
- 夏肢：`season_1988_summer_anni_prep` OR 仍在  
- JSON 寫入等劇本下刀；本檔只定計劃。

### 9.8 BEATS vs C1–C17（雙軌）

- 過渡：`story_beats_phase1`＝教學／週章節氛圍；**C1–C17＝重大抉擇權威**（事態／map tip 只掛 C／R／A）。  
- 同一週唔播兩套矛盾開場白；BEATS 與 C 文案衝突時以 **C** 為準。  
- deprecated 時間表另議（唔阻 P0）。

---

## 10. Cross-link

| 檔 | 關係 |
|---|---|
| `QA_PLAN_GAP_vs_PLAYER_V17N_v1.md` | 對表遺漏總表 |
| `QA_PLAYER_V17N_HIGHBAR_STATIC_v1.md` | 玩家 FAIL 來源 |
| `PHASE_AUTO_TABLE_v1.md` | phase 自動推進 |
| `PLOT_DETAIL_UNLOCK_v1.md` | 解鎖方向＋玩家可讀未開 |
| `WIRING_*_v1.md` | 引擎／播放／hook；「完整 UI 另輪」→ 改以本計劃 P0 為最小世界觸發 |
| `SOFT_NITS_FIX_v2.md` | Soft leftover 現況權威 |

---

*完 — PLAN_MAP_STORY_PROGRESS_v1（含 tester P0 補丁）*
