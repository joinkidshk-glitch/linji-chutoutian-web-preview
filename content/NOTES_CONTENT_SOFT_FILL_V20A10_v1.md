# NOTES｜Content Soft Fill v20a10（qwen3.7-max）

> **時間：** 2026-11-08（Asia/Hong_Kong）  
> **基線：** main `f318917`／預覽 `?v=20a10&softBehaviorGate=1`  
> **閘：** Soft≠PASS｜唔 tip LIVE｜SAVE `starVolunteer_map_v19w`｜唔抬 ?v=｜89–92 HOLD  
> **模型：** qwen3.7-max（DashScope token-plan APAC · `compatible-mode/v1/chat/completions`）  
> **禁止：** 本地自由起草對白／傳聞／選項（本輪文案均經 qwen）

## 改檔

| 檔 | sha256 前 8 | 填咗咩 |
|---|---|---|
| `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` | `cd0bea4f` | **只 C1–C5**：`playerFaceLine`／`beats[0].lines`／`choices[].label`／`redStarHook`（可空）；`nextHint` 全 `""`；trigger／effects／flags **未改**；C6–C17 文案欄未動 |
| `content/STUB_RUMOR_FRAGMENTS_v1.json` | `a22cfc17` | 既有 12 條 `title`＋`text`；**新增 4 閘傳聞** `tvb_rules_gossip`／`gao_steal_spotlight`／`choi_recent_news`／`hau_ching_recent_news`（fragments 總 16） |
| `content/STUB_FAVOR_DEBT_SEASON_v1.json` | `40789bfe` | 4 hooks `title`＋`line`；2 debts `title`＋`line` |

備份：`content/_bak_pre_content_soft_v20a10/`  
Qwen raw：`content/_qwen_raw_v20a10/`（batch1b C1–C5；batch2b 傳聞；batch3b favor）

## 合入方式

1. 分三批呼叫 qwen3.7-max（C1–C5 → 傳聞 → favor／debt）；temperature 0.45–0.55  
2. 第一批簡體→重跑繁體；傳聞口語批→重跑書面語  
3. Python merge：只覆寫允許文案欄；trigger 深比較＝備份；閘傳聞 `starId=null`；`json.tool` 驗過  
4. 禁詞掃描（薄本｜趕板｜看板｜噂｜真藝名常見表｜通告板｜TVB／無線）：**0 hit**（meta.note 未掃）

## qwen 出稿摘要

- **C1–C5：** 金龍茶餐廳入行分岔（電視台／電影）；傳聞規矩下留人脈 vs 趕通告；高仔搶鏡硬／忍；何生苛刻通告拒／接；采兒曉晴傳聞老實／圓場／迴避。短手帳句＋1–2 句系統敘事。  
- **傳聞：** 12 槽改書面娛樂版短訊；閘用四條覆蓋電視城規矩、高仔搶鏡、采兒／曉晴近期（虛構）。  
- **人情債：** 夏碼頭避雨、冬事務所清貨、春茶餐廳開年、秋電視城台慶；何生 200 人情、魏詠男過氣人情。

## Soft 試玩驗收點（建議）

1. Soft 預覽 `?v=20a10&softBehaviorGate=1`（唔 tip LIVE）  
2. **C1** cafe_cha：見 playerFaceLine＋兩選（電視台／電影）；flags `route_tv`／`route_film`  
3. 手帳／傳聞種到 **`tvb_rules_gossip`** → **C2** 可觸；選留人脈／趕通告  
4. 種 **`gao_steal_spotlight`**＋fame 閘 → **C3** 硬／忍  
5. agency_ho favor → **C4** 拒／接苛刻  
6. 秋／冬＋ **`choi_recent_news`／`hau_ching_recent_news`** → **C5** 三選  
7. 人情債 pane：hooks／debts 有 line；玩家面無「噂／薄本／趕板／看板」

## 未做

- 唔 commit／唔開 PR／唔 tip LIVE／唔抬 SAVE／?v=  
- 唔改 BehaviorGate／經濟／休息／C6–C17 文案  
