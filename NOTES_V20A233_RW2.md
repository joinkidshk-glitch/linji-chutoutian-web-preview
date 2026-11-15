# NOTES_V20A233_RW2 — 語言重寫 RW-2 Phase 1（v233）

## 做咗乜
- 內嵌表主線 N6–N19 逐句重寫（輕口語對白＋香港式書面語旁白，第三人稱），共 **134 個內嵌表葉片**改寫；句數 1,426 → 1,424（只係 N6 −2：synopsis 刪 DEV 枚舉 −3，beats[9] 修復 ＋1）。
- 動態 N17 選項（`endingEveOptions410`）13 個 label／note＋E4 crisis beat 2 行＋F4 `actHint`＋G4 卡 `debt-note` 一併重寫（17 個函數／卡片字串）。
- `STORY_HINT_SOFT` 4 個逐字重複嘅 playerHint 同步做新版（後備表，正常唔會顯示；舊廣東話版已清走）。
- 同步返 `content/story_detail_n1_to_n17.json`：N6–N17 以內嵌正本取代死 pack 節點，新增 N18／N19（pack 由 17 個 nodes 變 19 個）；機器核對逐葉比對 **1,190 葉 0 出入**（`artId` 除外）。
- N1–N5 一字未郁；新庫／引擎區零改動。

## 分章改動（葉片數）
N6 12／N7 8／N8 11／N9 8／N10 11／N11 4／N12 8／N13 12／N14 14／N15 9／N16 11／N17 6／N18 4／N19 5／F4 5／G4 6。

## 關鍵核實結果
- **N17 結構：唔使改。** 靜態節點得 2 個抉擇（順其自然／收山想想，保底）；播出時 `ending410EveNode` 經 `endingEveOptions410` 動態重建 2–6 個（至多六個，id a–f）。六個意向係方向，唔係六個掣。淨逐句重寫。
- **F4／G4：玩家可見，一併重寫。** 喺 `CHOICE47_NODES`（F4 3 抉擇、G4 2 抉擇）＋卡片字串。
- **`when` 年份唔手改。** N17 `when` '1990冬'、F4 '1990秋起'、G4 '1990冬起' 係舊曆寫法，YEARS66 載入 +2 變 1992；手改會 double-shift。N17 `lockedHint` 保留「1990 年冬」（410 陷阱測試釘死）。
- **TEXTFIX55 實測：改前 0 命中。** EXACT 171／NOTE_EXACT 36／PHRASES 14／TEXTFIX57_EXACT 9／TEXTFIX57_PHRASES 4——範圍內 896 句 0 命中，唔使拆任何條目。改後載入模擬（`textfix55StoryPack` 行 1,321 葉）：3 處 diff，全部係通用 `textfix55Note` 清洗器喺「。」／「）」後補句尾「。」——改前同一 3 處一樣有，pre-existing，唔係本批引入。
- **禁詞掃描：** 附錄 A 避免清單 0 新命中。「直播」1 處係 N11 synopsis 原有（1990 慈善騷電視直播，年代啱，保留並記錄理據）；「回去」1 處係我新寫嘅 G4 debt-note，已改做「返去」。新句簡體字 0 命中。
- **JS 語法：** `vm.Script` 編譯全部 2 個 inline script block（3,779,851 字元）通過；JSON `python3 -m json.tool` 通過。
- **Suite：312／10，零回歸。** FAIL 清單同 pristine main（b90bbd6）即場跑出嚟嘅 10 項已知 pre-existing 完全一致。中途曾經多 7 項 FAIL，全部處理好（見下）。

## Suite 中途 7 項 FAIL 嘅處理
- **2 項係我改錯，要修內容：**① N6 beats[9].lines[1] 重寫嗰陣漏咗「第一天那個選擇決定的，那個才是真分支。這裡不假裝有分叉。」幾句，已補返。② N17 `lockedHint` 唔可以刪「1990 年冬」（410 陷阱），已還原原文。
- **5 項係有意改動失效嘅錨點，更新測試＋註明原因：** story157_pack（pack 17→19 nodes；nodes[5:] sha 重算 `1be6aa08…`）、story157_index（N8「後台的人看他的眼神」、G4「表叔在銀行那邊」）、cleanup100（珍姐糖水句「給他」）、gate136（動態選項 note「頒獎禮散場，他站回他站慣的那個位置。」；pack N17 when／pacing 跟內嵌正本 1990冬／weekMin 153／prevMain N16）、weave410（退圈後果字眼「不再是這一行的人」「不再回這一行」）、wf1_80 fixture（N17 choices notes 兩句）。
- **JSON 同步刪咗嘅死欄：** N17 舊十檔 `endings_catalog`（E01–E10）＋`orientation_hint`——內嵌表無此欄，`index.html` 全檔 0 讀取；`qa.phase5.endings_names_lock` 頂層 metadata 未郁（歷史記錄，見工作報告）。

## 未做／押後
- **Live 實駕押後**（瀏覽器死）：開局→第 39 週第一張配角、頒獎禮全程、引薦／即派實機、新庫真載入、1990 板面、報紙分類、忠告卡。
- **Phase 2 另開**（唔喺呢票）：刪內嵌表，JSON 做唯一來源。留意：JSON N17 `when` 而家係舊曆 '1990冬'（跟內嵌正本），Phase 2 要裁定 JSON 節點載入嗰陣係咪行 YEARS66，唔可以靜默當顯示年。
- `STORY_HINT_SOFT` 內 N6–N17 嘅釋義版 lockedHint（同節點版唔同字，死後備）未重寫——正常唔顯示，Phase 2 清內嵌表嗰陣一併處理。
- N15 beats[1]「一身怎樣都不肯停的汗」係原有寫法，試讀嗰陣覺得略拗，留原樣（唔喺本批範圍改措辭）。

## 驗收證據（詳見 `~/workspace/linji-language-sample/RW2A_WORKLOG.md`）
改動葉片分章計、TEXTFIX55 載入模擬、禁詞掃描、JS 編譯、JSON 同步逐葉核對（1,190 葉 0 出入）、suite 312／10（FAIL 清單同 baseline 一致）、read-aloud 10 句試讀 0 停低重讀、防逐詞換抽查 5 組。
