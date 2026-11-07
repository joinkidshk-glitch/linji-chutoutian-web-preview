# CONTENT CONTRACT｜Freeplay 框架 v20a0

> **對象：** 之後負責豐富劇情／對白／噂文案嘅 bot（或作者）  
> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；框架 only；**唔發明長篇粵語劇情弧**；玩家面**禁真藝名**  
> **預覽：** `?v=20a0&softBehaviorGate=1`

本約定義：**框架引擎已就緒嘅欄位**，同 **內容 bot 應填／唔應改** 嘅邊界。

---

## 0. 一句分界

| 角色 | 做 | 唔做 |
|---|---|---|
| **框架 bot（本輪）** | schema、stub、UI 殼、閘鉤、藏 `nextHint`、雙軌／標籤／人情債／紅星遠觀殼 | 長對白、長噂、完整 C1–C17 劇情 |
| **內容 bot（下一輪）** | 填 `lines`／`playerFaceLine`／噂 `text`／季節鉤文案／紅星遠觀短句 | 改閘公式、改 SAVE key、改 BehaviorGate parsers、加真藝名、推 tip LIVE |

---

## 1. 權威檔（讀呢啲先動手）

| 檔 | 用途 |
|---|---|
| `docs/CONTENT_CONTRACT.md` | **本約**（內容 bot 必讀） |
| `NOTES_V20A_FRAMEWORK.md` | 框架落地筆記／verify |
| `content/SCHEMA_FREEPLAY_FRAMEWORK_v1.json` | 機器可讀總 schema |
| `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` | C1–C5 **空槽**（填對白） |
| `content/STUB_ERA_STARS_MVP_v1.json` | MVP 4 紅星遠觀 stub |
| `content/STUB_RUMOR_FRAGMENTS_v1.json` | 噂碎片槽 |
| `content/STUB_FAVOR_DEBT_SEASON_v1.json` | 人情債×季節鉤 |
| `content/STUB_CASTING_TAGS_v1.json` | 選角標籤表＋雙軌鉤 |
| 既有 LIVE／Soft | `content/story_detail_*.json`、`content/gigs_1988.json`、`content/SANDBOX_BEHAVIOR_GATE_C1_C5_SOFT_STUB_v1.json` |

計劃 thesis（用戶提供，唔入 repo 亦可）：Freeplay 生態觸發、藏 nextHint、雙軌聲量／信用、人情債×季節、紅星遠觀。

---

## 2. 硬規則（違反＝駁回）

1. **`nextHint` 永不顯示喺玩家面**（地圖 tip／事態卡／結算／手帳）。引擎欄可留空字串；UI 必須經 `BehaviorGate.nextHint_neverShow`／`storyHintPack` 清走。  
2. **玩家面禁真藝名／真作品名**。只用虛構名（陸柏言、廖炳星、魏詠男、葉敏芝…）。DEV 靈感對照只可寫喺 `devOnly` 欄，**唔入玩家 UI**。  
3. **Soft≠PASS**；唔 tip LIVE；唔改 `SAVE = starVolunteer_map_v19w`。  
4. **唔發明長篇劇情弧**喺 stub——內容 bot 填短對白／噂即可；深度支線另開 PR。  
5. 紅星接觸單位＝**遠觀／噂／綠葉**；MVP **無長互動對白**。

---

## 3. 內容 bot 應編輯嘅欄位

### 3.1 事態節拍（Story beats）

**填：** `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` → 各 `beatId` 下：

| 欄 | 型 | 必填 | 說明 |
|---|---|---|---|
| `playerFaceLine` | string | 是 | 玩家面一句鉤（茶餐廳／片場口吻；禁系統術語） |
| `beats[].lines` | string[] | 是 | 對白行；`kind`=`dialogue`\|`system` |
| `beats[].speakerId` | string\|null | dialogue 必填 | 見既有 beat schema |
| `beats[].speaker` | string | 建議 | 顯示名 |
| `beats[].emotion` | enum | 可選 | neutral/calm/tense/… |
| `beats[].expression` | enum | 可選 | default/smile/… |
| `choices[].label` | string | 是 | 選項玩家可見字 |
| `choices[].effects.flags` | string[] | 可選 | 只准用已鎖旗名（見下） |
| `choices[].effects.stats` | object | 可選 | `stageVolume`／`industryCredit`／既有能力鍵 |
| `choices[].effects.tags` | string[] | 可選 | 選角標籤 id（見 §3.4） |
| `redStarHook` | string | 可選 | 一句紅星遠觀／噂提示（短） |
| `rumorSeedIds` | string[] | 可選 | 指向噂 stub id |
| `nextHint` | string | **必須 `""`** | 內容 bot **唔好寫 pacing 長文** |

**唔好改：** `trigger.*` 閘結構（`needDone`／`weekMin`／`locIdAny`／`rumorAny`／`favorMin`／`tagAny`／`seasonAny`／`gigCountMin`）除非產品再拍板。

**已鎖旗名（C1–C5）：**  
`route_tv`／`route_film`；`flag_network_stay`／`flag_hustle_board`；`rival_gao_hard`／`rival_gao_endure`；`flag_refuse_gig_with_ho`／`flag_take_harsh_gig`；`choi_honest`／`spin`／`dodge`。

### 3.2 噂碎片（Rumor fragments）

**填：** `content/STUB_RUMOR_FRAGMENTS_v1.json` → `fragments[]`：

| 欄 | 說明 |
|---|---|
| `id` | 穩定 snake_case |
| `source` | 來源標籤（茶餐廳／報攤／茶水間…） |
| `title` | 短標題 |
| `text` | **玩家面噂文**（「聽講／好似」口吻） |
| `seasonAny` | `["春","夏","秋","冬"]` 或空＝全年 |
| `locIdAny` | 可觸發地點 |
| `starId` | 可選；MVP 四 id 之一 |
| `mergeGroup` | 可選；同組可拼合 |
| `devOnly` | 可選；**唔顯示** |

空槽用 `"text": ""`；引擎會顯示「（文案待補）」殼，唔崩。

### 3.3 人情債 × 季節（Favor-debt season）

**填：** `content/STUB_FAVOR_DEBT_SEASON_v1.json` → `hooks[]`／`debts[]`：

| 欄 | 說明 |
|---|---|
| `id` | 穩定 id |
| `creditorId`／`creditorName` | 債主 |
| `title`／`line` | 玩家面債條文案 |
| `season` | 催收季節 |
| `amount` | 建議金額（可空） |
| `status` | `未催`／`催收中`／`已逾期`／`已清` |
| `locHint` | 還債地點（通常 `agency_ho`） |

### 3.4 選角標籤（Casting tags）＋雙軌

**填／擴：** `content/STUB_CASTING_TAGS_v1.json` → `tags[]`：

| 欄 | 說明 |
|---|---|
| `id` | snake_case（如 `tag_endure`） |
| `label` | 玩家可見（如「捱得」） |
| `hidden` | true＝只經 NPC 口風暗示（預設 false＝手帳可見名） |
| `stageVolumeDelta`／`industryCreditDelta` | 沉澱時雙軌修正（可 0） |
| `blocksCastingTagAny`／`requiresCastingTagAny` | 通告閘鉤（內容可填；引擎已留位） |

通告 JSON 既有 `tagOnComplete: ["捱得",…]`——殺青時引擎會寫入 `S.castingTags`（label 或 id）。

雙軌已存在：`stageVolume`（鏡像 fame）／`industryCredit`（`S.industryCreditDelta`）。內容 bot 喺 choice `effects.stats` 用呢兩個鍵即可。

### 3.5 時代紅星遠觀（Era-star landmarks）

**填短句：** `content/STUB_ERA_STARS_MVP_v1.json`（同 `MOCK_UI_PHASE3_STAR_CASTING_v1.json` 對齊）：

| 欄 | 說明 |
|---|---|
| `starId` | **權威 id**（見下） |
| `displayName` | 虛構名 |
| `silhouetteDesc`／`distanceLine`／`rumorTeaser`／`locHint` | 遠觀短文（**無長對話**） |
| `locs` | 地圖 loc id |
| `devOnly.inspiration` | DEV only；**禁玩家面** |

**MVP 4 權威 id（引擎／資產）：**

| starId | 顯示名 |
|---|---|
| `luk_baakyin` | 陸柏言 |
| `liu_bingxing` | 廖炳星 |
| `ngai_wingnaam` | 魏詠男 |
| `yip_manji` | 葉敏芝 |

> **別名：** 規劃文件有時寫 `yip_manzi` → 一律正規化為 **`yip_manji`**（資產檔名／既有 stub）。內容 bot 唔好新開 `yip_manzi` id。

### 3.6 地點 stub

已存在於 `LOCS`（唔使再建）：

| locId | 名 |
|---|---|
| `cafe_cha` | 金龍茶餐廳 |
| `agency_ho` | 何生事務所 |

內容 bot 可喺 beat／噂 `locIdAny` 引用；可改 `desc` 氛圍句（短），唔改座標／id。

---

## 4. 內容 bot **唔應**改

- `index.html` BehaviorGate parsers／`featureFlag_softBehaviorGatePreview`／`gatePath`／`nextHint_neverShow`
- `SAVE` key、LIVE week-gate 數字（除非另開產品 PR）
- 出圖資產 bulk（出圖 HOLD）；遠觀剪影路徑可留空
- 真藝名寫入任何玩家面字串
- 長 romance／紅星深度支線（HOLD）

---

## 5. Beat 視覺 schema（既有）

沿用 `content/SCHEMA_STORYPLAY_VISUAL_v1.md`／`PLAN_STORY_UI_BEAT_SCHEMA_v1.md`：

```json
{
  "kind": "dialogue",
  "speakerId": "ho_sang",
  "speaker": "何生",
  "emotion": "firm",
  "expression": "default",
  "lines": ["…"],
  "locId": null,
  "bg": null
}
```

---

## 6. 驗收清單（內容 PR）

- [ ] 所有新玩家面字串無真藝名  
- [ ] 所有 beat `nextHint === ""`  
- [ ] C1–C5 旗名只用不在本約以外嘅新旗（或先更新本約）  
- [ ] 紅星只遠觀短句；無長對話樹  
- [ ] Soft≠PASS；verify URL 帶 `?v=…&softBehaviorGate=1`  
- [ ] 噂／債／標籤空槽唔令 UI 崩（空態殼仍在）

---

## 7. 建議工作流（內容 bot）

1. 讀本約 + `STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json`  
2. 先填 C1 `playerFaceLine` + 2–4 行對白 + 2 choices（短）  
3. 加 1–2 條噂碎片掛 `cafe_cha`  
4. 可選：改 MVP 紅星 `rumorTeaser`  
5. 開 PR；**唔改閘**；框架 bot／主理人再合

