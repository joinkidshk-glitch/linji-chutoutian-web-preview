# v20a24 — Weave Phase 4-1：年份閘基建＋鏈 F 移民潮第 1 拍＋第 3 拍補花邊

串聯規劃進入 Phase 4（劇情內容：鏈 F／鏈 G／三年版主幹）。今票只做三樣：年份閘 helper、鏈 F 第 1 拍（1989 年起移民傳聞碎片）、鏈 F 第 3 拍補一則花邊。第 2／4／5／6 拍、人情絕響、結局回收全部唔喺今票範圍。

## 改動

1. **年份閘 helper `yearSeasonNow()`**（放 `dateObj()` 之後）
   - 年份行真日曆 `dateObj().getFullYear()`；季節行 `calendarSeason()`；回傳 `{year, season}`。
   - 刻意唔用 `displayDateObj()`：soft 預覽會改月份做顯示，年份閘失真；`dateObj()` 係真時鐘（`S.dayIndex` 自 1988-03-07 起算），跨年自然入 1989／1990。
   - 之後所有跨年內容（鏈 F 其餘節拍、N 節點年份閘）統一用呢個 helper，唔再各自計日期。

2. **鏈 F 第 1 拍：移民氛圍碎片 `EXODUS_RUMOR_SEEDS`**（6 則，`MOCK_RUMOR_SEEDS` 之後）
   - 固定 id `rumor_exodus_*`：場記全家去溫哥華／賣咗層樓／茶餐廳伙記阿成做到月底／夜晚車人去啟德送機／片場唔夠人／人人研究入籍。全部 source「金龍茶餐廳」、state normal、season 空。
   - 文案跟規劃原味（市井口吻、泛稱／虛構人物）；玩家面無真藝名；顯示經既有 `displayRumor()` 路徑（P0-3 家庭友善過濾一致，毋須改渲染）。
   - **年份閘補種**：`ensureMockJournal()` 尾段（MERGE_FRAGS 補種之後）加一段——`yearSeasonNow().year>=1989` 先逐則檢查 id 未入池先 `push` 入 `S.mockRumors`（標 `seeded:true`）。1988 年完全唔出現；舊檔跨年後自動補齊；固定 id 去重，唔重複入池、唔覆寫已存在嘅行。
   - **純氛圍**：唔入 `MERGE_PAIRS`、唔置任何情報旗、無 `fameDelta` 欄（跟一般種子形狀，唔經聲望路徑）。
   - 取捨：補種用 `push`（排池尾）而唔跟 MERGE_FRAGS 嘅 `unshift`——氛圍碎片唔應該搶教學／情報碎片嘅頭位。

3. **鏈 F 第 3 拍補花邊**（`PAPER_SIDE_ITEMS` 加 1 則，池 17→18）
   - 「某武師舉家移民，劇組筵開三席送行」（規劃原文方向），`fromYear: 1989`，行既有 `paperSideItemForDay` 年份 filter：1988 年池唔含呢則、1989 年起先出。
   - **無 id**：結構上入唔到 `SIDE_PAPER_FRAGS` 登記（登記表維持 3 條情報線），純 flavor、唔做拼合碎片，符合規劃「報紙開始寫邊個走」嘅襯底定位。

## 測試

- 新增 `tests/test_weave41_logic.js`（29/29 PASS）：行真 `dateObj`／`calendarSeason`／`yearSeasonNow` 驗邊界（dayIndex 0／116／299／300／365）；行真入口 `ensureMockJournal` 驗 1988 唔補種、跨年補齊、重複呼叫冪等、舊檔部分入池只補餘下且唔覆寫；驗移民碎片唔喺 `MERGE_PAIRS`（含 `findMergePair` 全對掃描）、唔喺 `INTEL_FLAGS`、補種唔郁 `S.intelFlags`；行真 `paperSideItemForDay` 掃 240 日驗 1988 永不出送行花邊、1989 出到；`displayRumor` 路徑驗證。
- 新增 `tests/test_weave41_static.py`（31/31 PASS）：helper 用真日曆而唔用 displayDateObj、種子表形狀、補種接線、MERGE_PAIRS／INTEL_FLAGS 無 exodus、花邊登記表維持 3 條、新文案無真藝名、SAVE key／softRev 不變。
- 既有測試更新一處：`test_weave32_logic.js` 花邊池數量斷言 17→18（今票有意加一則；1988 年 filter 後池序不變，day0／1／11 關聯斷言不受影響）。
- 全套回歸：tests/ 共 28 檔（14 邏輯＋14 靜態）全部 PASS；全檔 inline script `node --check` OK。
- 慣例不變：無改 SAVE key（`starVolunteer_map_v19w`）、softRev（s107）、`?v=`（v20a10）。

## 未做（分票）

- 鏈 F 第 2 拍（次要 NPC 離港＋人情絕響）、第 4 拍（何生「走定留」對白＋旗）、第 5 拍（移民潮通告）、第 6 拍（結局回收）——留待後續 Phase 4 分票，同三年版主幹 N 節點／結局系統一齊排。
