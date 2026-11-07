# CONTENT CONTRACT｜Freeplay 框架 v20a3

> **對象：** 之後負責豐富劇情／對白／噂文案嘅 bot（或作者）  
> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；結構殼齊＋**殺青獎勵／傳媒反響**；**唔發明長篇粵語劇情弧**；玩家面**禁真藝名**  
> **預覽：** `?v=20a3&softBehaviorGate=1`  
> **基建筆記：** `NOTES_V20A3_POST_SHOOT_REWARD.md`（亦見 `NOTES_V20A2_STRUCTURE.md`）

本約定義：**引擎已就緒嘅欄位**，同 **內容 bot 應填／唔應改** 嘅邊界。

---

## 0. 一句分界

| 角色 | 做 | 唔做 |
|---|---|---|
| **框架／結構 bot** | schema、C1–C17 slots 殼、名冊遠觀釘、Soft 信用／催收鎖、bust preferFile、**殺青獎勵引擎**、藏 `nextHint` | 長對白、長噂、LIVE tip |
| **內容 bot（下一輪）** | 填 `lines`／`playerFaceLine`／噂 `text`／債 `line`／`title`／紅星短句／choice labels／**殺青獎勵 stub 文案** | 改閘公式、改 SAVE key、改 BehaviorGate parsers、加真藝名、推 tip LIVE、擅自改 trigger（除非 re-board） |

---

## 1. 權威檔

| 檔 | 用途 | 權威？ |
|---|---|---|
| `docs/CONTENT_CONTRACT.md` | **本約** | 是 |
| `NOTES_V20A2_STRUCTURE.md` | v20a2 結構落地／verify | 是 |
| `content/SCHEMA_FREEPLAY_FRAMEWORK_v1.json` | 機器可讀總 schema | 是 |
| `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` | **C1–C17 對白＋trigger 殼** | **對白權威**；C6–C17 Soft 可用性以 slots 為準 |
| `content/SANDBOX_BEHAVIOR_GATE_C1_C5_SOFT_STUB_v1.json` | Soft BehaviorGate 載入殼／DEV mirror | C1–C5 fallback；C6–C17 由 slots create |
| `content/STUB_RUMOR_FRAGMENTS_v1.json` | 噂碎片 | 噂文案權威 |
| `content/STUB_FAVOR_DEBT_SEASON_v1.json` | 人情債×季節 | 新債文案權威 |
| `content/STUB_CASTING_TAGS_v1.json` | 選角標籤表＋雙軌 | 標籤權威 |
| `content/STUB_ERA_STARS_MVP_v1.json` | 紅星遠觀 stub（MVP4＋6 擴展） | 遠觀短句 |
| `content/SCHEMA_POST_SHOOT_REWARD_v1.json` | 殺青獎勵 schema | 是 |
| `content/STUB_POST_SHOOT_REWARDS_v1.json` | 殺青獎勵文案 stub | **獎勵文案權威** |
| `NOTES_V20A3_POST_SHOOT_REWARD.md` | v20a3 獎勵落地／verify | 是 |

---

## 2. 硬規則（違反＝駁回）

1. **`nextHint` 永不顯示喺玩家面**。必須 `""`。  
2. **玩家面禁真藝名／真作品名**。DEV 靈感只可 `devOnly`。  
3. **Soft≠PASS**；唔 tip LIVE；唔改 `SAVE = starVolunteer_map_v19w`。  
4. **唔發明長篇劇情弧**喺 stub。  
5. 紅星接觸單位＝**遠觀／噂／綠葉**；**無長互動對白**。  
6. **玩家面唔顯示工程標籤列表**——標籤以手帳 `weak-seals` 暗紋顯示；`?devTags=1` 先開 DEV 分頁。  
7. **齊鎮海 `chai_zanhoi`／`placeholder_era_08` 唔上地圖**。

---

## 3. 內容 bot 應編輯嘅欄位

### 3.1 事態節拍 — **slots C1–C17**

**填：** `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json`

| 欄 | 必填 | 說明 |
|---|---|---|
| `playerFaceLine` | 是 | 玩家面一句鉤 |
| `beats[].lines` | 是 | 對白；非「待補」時 overlay |
| `choices[].label` | 是 | 選項字 |
| `choices[].effects.flags/stats/tags` | 可選 | flags 只准已鎖／已預留名 |
| `redStarHook` | 可選 | 短 |
| `nextHint` | **必須 `""`** | |

**Trigger：** 框架擁有。內容 bot **預設唔改**。C6–C17 Soft 閘由 slots create／overlay；sandbox 可能只有 C1–C5。

占位對白（含「待補」）→ **唔覆蓋**既有 Soft stub／`story_detail`（遊戲唔崩）。

### 3.2 噂／人情債／標籤

同 v20a1：噂填 `text`（空＝唔自動種）；債填 `line`／`title`；標籤表見 `STUB_CASTING_TAGS`。  
**催收罰鎖：** 只有狀態 **`已逾期`** 會 Soft 鎖「接通告」；清數後放行。教學債保持 `未到期`。

### 3.3 Soft 通告欄（內容／數據可選）

| 欄 | 說明 |
|---|---|
| `requiresCastingTagAny` / `blocksCastingTagAny` | Soft 標籤閘 |
| `industryCreditMin` | Soft 業內信用下限；**缺欄＝唔閘** |


### 3.5 殺青獎勵／傳媒反響（v20a3）

**觸發：** 拍攝成功殺青（`finished`）一次一包。  
**填：** `content/STUB_POST_SHOOT_REWARDS_v1.json`

| 頻道 | 填欄 | 說明 |
|---|---|---|
| `press` | `headline`／`dek`／`paperName` | 報紙娛樂版短卡 |
| `news` | `line`／`outlet` | 電視／電台一句 |
| `streetFans` | `line`／`place`／可選 `stageVolumeDelta` | 街上突發 fans |
| `metrics` | `label`／`valueLine`／`blurb` | 電影→票房；電視／綜藝→收視；唱片→銷量；其他→關注度 |

空字或「待補」→ 引擎用 fallback 短句（遊戲唔崩）。  
**唔改** matchTypes／metricKind 映射除非 re-board。玩家面禁真藝名。

### 3.4 時代紅星遠觀

地圖遠觀 id：`luk_baakyin`／`liu_bingxing`／`ngai_wingnaam`／`yip_manji`／`mak_zhendong`／`lok_gasing`／`pang_siuki`／`chung_choning`／`gu_mingfai`／**`so_jiyan`**。  
內容 bot 可改 stub 短句（`silhouetteDesc`／`distanceLine`／`rumorTeaser`）。**唔寫長互動樹。**

bust preferFile（引擎）：`assets/story/era_stars/{id}_bust_*.png`＋silhouette（MVP4＋so_jiyan）。

---

## 4. 內容 bot 點自檢

```js
await __freeplay.load();
__freeplay.check();          // ok:true；infra:"v20a3"；slotsCount:17；postShootReward:true
__reward.check();            // ok:true
__freeplay.slots().nodes.length; // 17
__freeplay.softIndustryCreditGate({ industryCreditMin: 1 });
__freeplay.softOverdueFavorDebtLock({});
```

預覽：`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a3&softBehaviorGate=1`

---

## 5. Explicit HOLD

- 出圖／31 人 LOOKS  
- 紅星長互動／romance／鄧線完整；89–92  
- LIVE tip／抬 SAVE  
- 齊鎮海上地圖；拼合音效  
- 填晒 C1–C17 粵語長對白（本輪只留殼）
- 真實報紙排版／音效；長篇傳媒劇情弧（獎勵只係短卡）
