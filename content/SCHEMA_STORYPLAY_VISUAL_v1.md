# SCHEMA_STORYPLAY_VISUAL_v1

**權威計劃：** `PLAN_STORY_UI_BEAT_SCHEMA_v1.md`（本檔＝引擎落地摘要）  
**引擎：** v18g StoryPlay  
**HOLD：** Soft≠PASS；全量出圖未開；**C1 UI test art gate** 允許 GD 交最小 bust／`bg_loc_tvb_longmen`（見 `ART_BRIEF_C1_UI_TEST_v1.md`）  
**相容：** 舊 beat `{ speaker, lines }` 仍可播。

## Beat（additive）

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

| 鍵 | 說明 |
|---|---|
| `kind` | `dialogue` \| `system` |
| `speakerId` | dialogue 必填；system＝`null` |
| `speaker` | 顯示名（可選） |
| `emotion` | enum；缺→`neutral` |
| `expression` | enum；缺→`default` |
| `lines` | `string[]` |
| `locId` / `bg` | 可選；覆蓋 node 環境 |

**禁止 beat 鍵 `portrait`。** Bust＝`speakerId`→registry→`artId`→檔名。

### 規則

1. **dialogue：** bust 經 speakerId；讀 emotion＋expression。  
2. **system：** 置中、無 bust；legacy `系統`／`旁白`／`""` 相容。  
3. **BG 優先：** beat.`bg` → beat.`locId`→`bg_loc_{locId}` → node.`locId`→`bg_loc_*` → `bg_generic_interior`。  
4. `node.setting`＝文案 only；`node.artId`＝章卡（≠bust／≠bg）。

### emotion v1

`neutral|calm|tense|angry|warm|tired|smirk|worried|soft|firm`

### expression v1（PLAN）

`default|smile|frown|raise_brow|eyes_down|look_aside`  
（別名：`serious`→`frown`）

## Bust 資產槽（drop-in）

優先序（引擎）：

1. `assets/npc/{artId}_bust_{expression}.(png|jpg|webp)`  
2. `assets/story/{artId}_bust_{expression}.*`  
3. `assets/npc/{artId}_bust.*`（無表情後綴）  
4. 同路径 `…_bust_default.*`（表情缺檔時）  
5. `PORTRAITS[portraitsKey]`／`assets/{face}.jpg`／`assets/dialog/{face}.jpg`  
6. 剪影 `sp-bust-sil`

**C1 UI test artIds：** `char_hero`（awi）· `char_ho` · `char_cheung`  
例：`assets/npc/char_hero_bust_default.png`

主表 speakerId→artId 見 PLAN §B（awi→`char_hero` 等）。

## BG 資產槽（drop-in）

1. `assets/bg/{bgKey}.(jpg|png|webp)`  
2. `assets/story/{bgKey}.*`  
3. `assets/{bgKey}.*`  
4. CSS gradient class（`bg_loc_*`／`bg_generic_interior`／`bg_c1_tea_restaurant`）

例：`assets/bg/bg_loc_tvb_longmen.jpg`

11 loc → `bg_loc_{locId}` 全表見 PLAN §C.1。

## UX

- 字在 `sp-plate`／`sp-plate-center`（唔壓裝飾線）  
- Phone；progress＋下一句／跳至選項可見  
- Soft≠PASS · 全量出圖 HOLD（C1 測閘另計）
