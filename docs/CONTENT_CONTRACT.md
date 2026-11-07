# CONTENT CONTRACT｜Freeplay 框架 v20a1

> **對象：** 之後負責豐富劇情／對白／噂文案嘅 bot（或作者）  
> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；框架＋基建對齊；**唔發明長篇粵語劇情弧**；玩家面**禁真藝名**  
> **預覽：** `?v=20a1&softBehaviorGate=1`  
> **基建筆記：** `NOTES_V20A1_INFRA.md`（取代／補充 `NOTES_V20A_FRAMEWORK.md`）

本約定義：**引擎已就緒嘅欄位**，同 **內容 bot 應填／唔應改** 嘅邊界。

---

## 0. 一句分界

| 角色 | 做 | 唔做 |
|---|---|---|
| **框架／基建 bot** | schema、stub、閘對齊、seed、弱暗紋、Soft 標籤閘、藏 `nextHint` | 長對白、長噂、完整 C6–C17 |
| **內容 bot（下一輪）** | 填 `lines`／`playerFaceLine`／噂 `text`／債 `line`／`title`／紅星短句 | 改閘公式、改 SAVE key、改 BehaviorGate parsers、加真藝名、推 tip LIVE |

---

## 1. 權威檔（讀呢啲先動手）

| 檔 | 用途 | 權威？ |
|---|---|---|
| `docs/CONTENT_CONTRACT.md` | **本約** | 是 |
| `NOTES_V20A1_INFRA.md` | v20a1 基建落地／verify | 是 |
| `content/SCHEMA_FREEPLAY_FRAMEWORK_v1.json` | 機器可讀總 schema（含 `rosterPlanned`） | 是 |
| `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` | **C1–C5 對白＋trigger 內容殼** | **對白權威**；trigger 已同 Soft 生態對齊 |
| `content/SANDBOX_BEHAVIOR_GATE_C1_C5_SOFT_STUB_v1.json` | Soft BehaviorGate 載入殼／DEV mirror | fallback；trigger 應與 slots 同步 |
| `content/STUB_RUMOR_FRAGMENTS_v1.json` | 噂碎片槽（含 Phase2 merge 對表） | 噂文案權威 |
| `content/STUB_FAVOR_DEBT_SEASON_v1.json` | 人情債×季節（`seedFreeplayFavorDebt`） | **新債文案權威** |
| `content/STUB_CASTING_TAGS_v1.json` | 選角標籤表＋雙軌 | 標籤權威 |
| `content/STUB_ERA_STARS_MVP_v1.json` | MVP 4 紅星遠觀 stub | 遠觀短句 |

內嵌 `SEASON_COLLECT`（四季示範卡）仍可玩；內容 bot **唔改** inline——改 stub，引擎會 seed 入手帳。

---

## 2. 硬規則（違反＝駁回）

1. **`nextHint` 永不顯示喺玩家面**。必須 `""`。  
2. **玩家面禁真藝名／真作品名**。DEV 靈感只可 `devOnly`。  
3. **Soft≠PASS**；唔 tip LIVE；唔改 `SAVE = starVolunteer_map_v19w`。  
4. **唔發明長篇劇情弧**喺 stub。  
5. 紅星接觸單位＝**遠觀／噂／綠葉**；MVP **無長互動對白**。  
6. **玩家面唔顯示工程標籤列表**——標籤以手帳 `weak-seals` 暗紋顯示；`?devTags=1` 先開 DEV 分頁。

---

## 3. 內容 bot 應編輯嘅欄位

### 3.1 事態節拍（Story beats）— **單一權威：slots**

**填：** `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json`

| 欄 | 必填 | 說明 |
|---|---|---|
| `playerFaceLine` | 是 | 玩家面一句鉤；填咗會 overlay Soft gate face |
| `beats[].lines` | 是 | 對白；**非「待補」** 時會 overlay `story_detail` 該節 |
| `choices[].label` | 是 | 選項字；非待補時 merge 入故事節 |
| `choices[].effects.tags` / `stats` / `flags` | 可選 | flags 只准已鎖名 |
| `redStarHook` | 可選 | 短 |
| `nextHint` | **必須 `""`** | |

**Trigger（`trigger.*`）：** 已同 sandbox 生態對齊（含 C3 `rumorAny`/`fameMin`、C4 `favorMin`/`favorTarget`、C5 噂＋季節）。  
內容 bot **預設唔改 trigger**——只填對白。引擎 Soft 路徑：`applyFreeplaySlotsToSoftGate()` 用 slots trigger 覆寫 BehaviorGate。

占位對白（含「待補」）→ **唔覆蓋**既有 Soft stub／`story_detail` 對白（遊戲唔崩）。

**已鎖旗名（C1–C5）：**  
`route_tv`／`route_film`；`flag_network_stay`／`flag_hustle_board`；`rival_gao_hard`／`rival_gao_endure`；`flag_refuse_gig_with_ho`／`flag_take_harsh_gig`；`choi_honest`／`spin`／`dodge`。

### 3.2 噂碎片

**填：** `content/STUB_RUMOR_FRAGMENTS_v1.json` → `text`（同 `title`）

- **空 `text` = 唔自動入手帳**（防洗版）。  
- 非空＋`seasonAny` 空或匹配 `calendarSeason()` → `seedFreeplayRumorShells` 種入噂 pane。  
- **Phase2 merge 對表**（`mergeGroup`／`phase2PairId`）：

| phase2PairId | fragment ids |
|---|---|
| `pair_lu_baiyan_breakdown` | `rumor_lu_baiyan_angry` + `rumor_lu_baiyan_drunk` |
| `pair_liao_bingxing_money` | `rumor_liao_bingxing_talk` + `rumor_liao_bingxing_recast` |
| `pair_mai_zhendong_hide_injury` | `rumor_mai_zhendong_hurt` + `rumor_mai_zhendong_refuse_doc` |

教學 `MERGE_FRAGS` 已預置上述 id；內容 bot 填 stub `text` 可豐富同 id（已存在則唔重複種）。

### 3.3 人情債 × 季節 — **單一權威：stub**

**填：** `content/STUB_FAVOR_DEBT_SEASON_v1.json` → `debts[]`／`hooks[]` 嘅 `line`／`title`

引擎：`seedFreeplayFavorDebt()`  
- 登記全部 stub id；當季匹配 → 入 `S.mockDebts`  
- 空 `line` → 顯示「（文案待補）」殼，唔崩  
- `SEASON_COLLECT` 內嵌四季卡仍可玩（示範）；**新文案只改 stub**

狀態詞：`未到期`／`就嚟到期`／`已逾期`／`已清`（`未催` 會 map 做 `未到期`）。

### 3.4 選角標籤＋雙軌

**填：** `content/STUB_CASTING_TAGS_v1.json`

玩家面：earned `S.castingTags` → 手帳 **weak-seals**（~8% opacity）。  
DEV 列表：`?devTags=1` 或 `localStorage.starVolunteer_devTags=1`。  
`__freeplay.tags()` 永遠可用。

**Soft 通告閘（唔 tip LIVE）：** 通告 JSON 可加：

| 欄 | 說明 |
|---|---|
| `requiresCastingTagAny` | 玩家需有其中一個標籤（id 或 label）先可試鏡 |
| `blocksCastingTagAny` | 有其中一個則暫未能報 |

無呢兩個欄 → Soft／LIVE 行為同舊。

### 3.5 時代紅星

MVP 4 權威 id：`luk_baakyin`／`liu_bingxing`／`ngai_wingnaam`／`yip_manji`（`yip_manzi`→`yip_manji`）。  
`rosterPlanned`（schema）：其餘名冊 id（麥震東／駱家聲／彭少祺／鍾楚凝／顧明輝／蘇芷茵 `so_jiyan`／齊鎮海…）— **無地圖釘**；`so_jiyan` 有剪影資產但無釘＝**故意 HOLD**。

---

## 4. 內容 bot 點自檢

瀏覽器 console（Soft 預覽）：

```js
await __freeplay.load();
__freeplay.check();          // ok:true；infra:"v20a1"
__freeplay.slots();          // C1–C5
__freeplay.favorDebt();
__freeplay.rosterPlanned();  // length ≥ 8
__freeplay.tags();
```

預覽：`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a1&softBehaviorGate=1`

---

## 5. Explicit HOLD

- 出圖／31 人 LOOKS；bust preferFile 後排  
- 紅星長互動／romance／鄧線完整；89–92  
- LIVE tip／抬 SAVE  
- C6–C17 生態槽；齊鎮海上地圖  
- 催收罰鎖 gigs；拼合音效  
