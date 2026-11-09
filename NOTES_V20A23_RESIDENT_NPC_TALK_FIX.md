# NOTES v20a23 — 駐場 NPC：事務所傾談掣斷鏈修復

背景：v20a22 已喺 openLoc hub 分支加傾談掣（條件：S.locNpc 有 NPC 在場先呼叫
addLocTalkGiftActs），路徑級測試通過；但實機覆檢（真遊戲、新存檔）發現事務所
面板仍然無「同何生傾談」掣（3/7、3/14 兩次皆無），其他 NPC（如林曉晴喺九龍
電視台）就有。

## 診斷根因（行號以 v20a22 版計）

- `refreshNpc()`（22438–22446）係唯一填 `S.locNpc` 嘅函數：新檔（33877）、
  每日 `advanceDay()`（24192）、讀檔缺欄（33919）都係呼叫佢。佢將每個 NPC 以
  70% 機會隨機派去其 `homes` 其中一處，每地點只存一個 NPC。
- `NPCS`（4078–4091）：`agent.homes=[ad_central, tvb_kowloon, film_cotton,
  rec_wanchai]`、`reporter.homes=[rec_star, film_cotton, tvb_harbour, ad_adm]`。
  **agency_ho 同 cafe_cha 唔喺任何 NPC 嘅 homes 入面**，所以
  `S.locNpc["agency_ho"]`／`S.locNpc["cafe_cha"]` 永遠係 undefined——唔係
  「嗰日唔好彩」，係結構上永遠唔成立。
- v20a22 喺 openLoc（31457）攞 `npcId=S.locNpc[id]` 傳入 hub 分支嘅
  addLocTalkGiftActs；agency_ho 永遠 undefined → 傾談／送禮掣永遠唔出。
- 對照組：tvb_kowloon 喺 colleague.homes 入面，林曉晴有被派去嗰度嘅日子，
  所以嗰度有傾談掣。分別純粹係數據：個地點喺唔喺 homes 名單上。
- v20a22 測試假象：test_weave34 嘅 freshS 人手寫死 `locNpc:{agency_ho:'agent'}`，
  測咗一個真派位永遠產生唔到嘅狀態。

## 修法（數據驅動，唔改派位層）

駐場關係寫入 LOCS 數據（新欄 `residentNpc`，同 NPCS.homes 同一哲學）：

- LOCS `agency_ho` 加 `residentNpc:"agent"`。何生係事務所駐場嘅證據本身就喺
  現有設計入面：地點以佢命名、openLoc 入場每日 `bumpNpc("agent",+2)`、
  loc-who 硬寫「何生提醒：…」、C1 主線播點係 agency_ho。
- 新增 `locResidentNpcId(L)`（驗證 NPCS 存在先認）＋`locPanelNpcId(L)`
  （派位 locNpc 優先、無先攞駐場兜底）。
- openLoc 面板 npcId 改行 `locPanelNpcId(L)`——hub／非 hub 同一解析，
  非 hub 行為不變（嗰啲地點無 residentNpc，解析結果同舊版逐日一致，
  有測試逐次對齊驗證）。
- cafe_cha 唔設 residentNpc：現有數據入面采兒（reporter）嘅 homes 同
  STORY_MEET_SOFT meet 地點都唔包茶餐廳，茶餐廳社交層係 MOCK_ASK 嘅無名
  伙記／老闆娘／隔籬枱；采兒傾談掣喺佢自己 4 個出沒地點本身運作正常，
  唔係斷鏈。唔擅自指派駐場（屬設計決定）——日後要加，只改 LOCS 一行。
- 送禮掣跟 helper 本來邏輯：何生唔喺 MAP_NPC_TO_KEY（romance 送禮對象係
  Vera／曉晴／采兒），所以事務所只有傾談掣、無送禮掣，屬原有設計。
- 派位層（refreshNpc／homes／地圖針 hasNpc）原封不動；地圖針「熟人在場」
  語義維持係派位相遇，唔因駐場而恆亮。

## 測試（吸取教訓：唔准人手 set locNpc）

- 新增 `tests/test_weave35_logic.js`（14 項）：行**真 refreshNpc＋真 LOCS／
  NPCS 數據＋真 openLoc**（假 DOM），locNpc 一律由真派位產生：
  300 次派位斷言 hub 永遠無 locNpc（診斷鎖）＋曉晴有被派去九龍電視台（對照）；
  100 次派位後面板解析恆為何生；連續 14 日真 openLoc 事務所日日有
  「同何生傾談」掣；茶餐廳無傾談掣＋MOCK_ASK 在（現況鎖）；非 hub 九龍
  電視台傾談掣出現與否同真派位逐次一致。新測試對 v20a22 舊檔會直接出錯
  （缺 locPanelNpcId），證明測得到個 bug。
- 新增 `tests/test_weave35_static.py`（19 項）：鎖死 LOCS residentNpc 數據、
  helper 接線、openLoc 唔准退返淨讀 S.locNpc、refreshNpc／homes 原封不動、
  SAVE key／softRev 不變。
- test_weave34_logic.js harness 補 eval 兩個新 helper（佢抽函數清單要跟新
  接線，斷言本身無改）。
- 舊測試全套（P0、P0-3、Weave 1-1／1-2／1-3、2-1／2-2／2-3、3-1／3-2／3-3、
  v20a22 批次，邏輯＋靜態共 24 檔）全部通過、零回歸；全檔 script
  `node --check` 通過。無改 SAVE key／softRev／?v=。
