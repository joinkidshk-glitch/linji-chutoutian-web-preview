# NOTES_CONTENT_SOFT_V20A10_PLAYTEST_COPY_v1

日期：2026-11-08（Asia/Hong_Kong）  
來源：統籌 Soft 試玩 v20a10 跟進（用戶已 OK）  
執行：Content Soft · qwen3.7-max  
狀態：**Soft≠PASS｜唔 tip LIVE｜預覽仍 ?v=20a10｜唔抬 SAVE**

## 做咗咩

1. **「噂」→「傳聞」**
   - Soft stub C2 `redStarHook`：`大明星捱出嚟傳聞；廖炳星綠葉可`
   - MOCK Phase3 alignNote：`陸柏言／廖炳星傳聞碎片`
   - PLAN／NOTES 標籤「噂碎片」順手改「傳聞碎片」

2. **C1 主場對齊金龍**
   - `story_detail`／`SANDBOX_C1_FUSION_DRAFT`：`setting`＝「金龍茶餐廳；臨記聚腳、通告情報口風」
   - 開場 beats 改金龍門／卡座；清「星河後門／附近茶餐廳；片場後巷感」做 C1 主場
   - Soft C1 `locId=cafe_cha` 結構未改；slots C1 金龍口語補強
   - **C2 後巷本身未改**

3. **C1 主對白減教科書腔（qwen-max）**
   - 何生關鍵句：「你想做演員，定係想做個連名都冇嘅臨記？」
   - 房租／手頭緊敘事港產書面；B01／何生 greet·chat 輕口語化
   - Soft slots C1–C2 清「面臨抉擇／聽取」；C5 顺手清「津津有味地／眾矢之的」
   - 人情債玩家面「賬」→「帳」；玩家面「通告板」→「通告欄」（改過檔內）

## 禁改（已守）

trigger／effects／flags／locId；經濟／休息／行為閘；LIVE tip／?v=／SAVE；唔 commit／唔開 PR。

## 改檔 sha256 前 8（preview＝權威）

- `story_detail_c1_to_c17.json`: `19adfdd5`
- `SANDBOX_C1_FUSION_DRAFT_v1.json`: `6b83255b`
- `SANDBOX_BEHAVIOR_GATE_C1_C5_SOFT_STUB_v1.json`: `feeb93d5`
- `MOCK_UI_PHASE3_STAR_CASTING_v1.json`: `783724d7`
- `STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json`: `7bf40930`
- `STUB_FAVOR_DEBT_SEASON_v1.json`: `7dd4deb7`
- `story_beats_phase1.json`: `a2ba8e52`
- `npc_lines_core.json`: `ba6732c8`

## 禁詞掃描（改過嘅玩家面 JSON）

噂｜薄本｜趕板｜看板｜通告板｜TVB → **0 hit**

## qwen raw

`content/_qwen_raw_v20a10_playtest_copy/`（constrained／fix2／slots／c5_nit）

## 備份

`content/_bak_pre_soft_v20a10_playtest_copy/`

## 同步

- `/workspace/linji-chutoutian-web-preview/content/`
- `/workspace/star-volunteer-web/content/`
- store `store-cbdfa415-74f6-4e12-8fbd-513ef31077be/`（根路徑對應檔）

## 交收

交統籌驗收後先叫 iOS Soft tip。Content Soft 停喺呢版。
