# DeepSeek 文案計劃理解檢查

- HTTP: 200
- model: deepseek-flash

---

a) 五點摘要

1. Phase1 以 1988 年春開局（1988-03-07）為起點，建議涵蓋 W1–12（約三個月，春至入夏），主線目標是「臨記出頭半步」：穩定有薪加上初步人脈。
2. 主線節拍為 B01–B10，涵蓋何生放手、通告板初見、首次報名與訓練、charm 軟解鎖、首次試鏡、首單殺青、人脈三角、對手壓力、記者曝光、春夏小結。
3. 章節切法為四章 × 三週：Ch1 開局鎖與訓練；Ch2 首試鏡／首通告；Ch3 人脈與對手；Ch4 春夏小結；季節標籤春 W1–6、夏 W7–12。
4. Phase1 文案交付重點為 HTML 六人 NPC 對話池（改寫為書面語）、事件模板變體、主線短對白、章標題與訓練解鎖句；1988 通告庫以 QA／補洞為主。
5. 1989–1992 僅作輕映射標籤，Phase2+ 暫不產 detail；畫風／UI 另線進行，不在本文範圍。

b) 語域規則

已批方案 C：通告、NPC 對話、事件模板、主角對白及計劃文件全文一律採繁體書面語；可保留少量港產行業詞（如通告、殺青、龍套），但禁止以粵語口語文法作為主幹。原方案 A（通告書面語＋其餘粵語）與方案 B（全面粵語口語）均不採用。HTML 原型現有粵語口語 NPC 池須整池改寫為書面語，機制與 bucket 結構不變；主角生成線對齊書面語短句；DeepSeek 四殼一律以書面語為輸出主幹。既有 `gigs_1988` 本為書面語，不因語域重寫年庫。

c) 會做／不會做

會做：
- 依計劃規格確認 Phase1 主線節拍、週／章結構、通告庫規格、NPC 對話池規格、事件模板與欄位對齊。
- Phase1 只加深 HTML 六人（何生、Vera、林曉晴、張子駿、高俊傑、周采兒），對話池改寫為書面語，每人約 30 句、六人合計約 180 句（規格目標）。
- 1988 通告庫只做 QA／潤飾／補洞，上限 ≤8 則，並整理春／夏「優先上板」標註表。
- 事件模板變體約 50–60 句、主線 B01–B10 短對白（每 beat ≤3 句）、章標題與開結、訓練／解鎖句約 20 句。
- 在用戶確認 §9 其餘開放問題後，才由 tester 按 Prompt A/B/C/D 分批呼叫 DeepSeek 產出 detail。

不會做：
- 不重產 1988 三十則通告年庫（預設新產 0 則）。
- Phase1 不為 `cast_main.json` 十二人各產完整 lines，也不將其當作已上線。
- 不跑完整 detail、不填滿 Prompt B/C/D 變體正文，除非另有用戶指令。
- 不發明衝突 schema、不改數值公式、不新增未經批准的欄位。
- 不產 1989–1992 年庫、不寫長篇劇本、不重寫 UI 文案系統（除非擋玩）。
- 不生成完整對話池、不寫出三十則通告、不填滿變體正文。

d) 對齊的資料檔案名稱

- `worldview.json`（`content/worldview.json`）
- `protagonist.json`（`content/protagonist.json`）
- `gigs_1988.json`（`content/gigs_1988.json`；往後為 `gigs_YEAR`，如 `gigs_1989`、`gigs_1990`、`gigs_1991`、`gigs_1992`）
- `cast_main.json`（`content/cast_main.json`）
- `index.html`（含 `NPCS`、`doTalk`、settle／shoot／audition 字串）
- `content/prompts/prompt4_gigs.md`
- 構想路徑（待批）：`content/npc_lines_core.json`、`events_zh_HK.json`

e) 三個仍不清楚、需要用戶澄清的問題

1. 雙 cast 決策：Phase1 是否確定只深 HTML-6、Phase2 再以 `legacyId`／別名表 merge 入 `cast_main`？
2. 一期長度：Phase1 是否確定為 W1–12，抑或改為 W1–8 或延至秋季？
3. 對話外置：是否批准新增 `npc_lines_core.json` 與 `events_zh_HK.json`（只搬字串、不改欄位語義）？另 1988 年庫是否維持「只 QA、不重產」？
