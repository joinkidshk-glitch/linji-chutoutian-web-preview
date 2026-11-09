# NOTES v20a19 — Weave Phase 3-1：報紙連載口吻＋點名門檻

串聯規劃 §3.3「報紙連載規則」落地：報紙要記得自己寫過啲乜（連載口吻），同埋點名玩家要有門檻（唔好第一日就大名見報）。

## 研究結論（現有報紙系統）

- 組版：`buildNewspaperEdition(batch, day)` 將到期佇列按 |fameDelta| 排序，最高嗰則做主新聞（headline／dek），其餘做短訊（最多 3 則＋「同日還有 N 則」），尾加花邊短訊（Phase 1-1）；edition 有 id／dayIndex／eventKeys／fameDelta 等欄。
- 歷史：有——`S.newspaperClippings`（`commitMorningPaper` 收報時 unshift 入去，上限 40 份），欄位有 headline／dek／eventKeys／fameDelta 等，即係「上一份報紙」嘅可靠來源；去重就靠佇列 item 嘅 `eventKey`＋剪報 eventKeys。
- 玩家稱呼（改之前）：主新聞 headline 永遠用泛稱「臨記飾演…」（唔點名）；但 dek 由第一日就直書「阿偉」——無門檻、唔一致。story／award 模板嘅 `{playerName}` 亦寫死換成「阿偉」（今次唔郁嗰條路徑，見下）。

## 今次改動

### 點名門檻（按幕前聲望 S.fame＝幕前聲量分級）

- 新增 `newspaperNameTier(fame)`／`newspaperPlayerRef(tier)`，門檻跟現有 fame 尺度：
  - **anon（fame < 15）**：泛稱「一名臨記」（標題用「臨記」），唔點名——門檻同 #104 淡紙（fame < 15）一致，淡紙期同時係匿名期。
  - **named（15 ≤ fame < 40）**：開始點名「阿偉」（標題、dek、傳聞回音一致）。
  - **titled（fame ≥ 40）**：稱號式「人氣新人阿偉」。
- 套落 `newspaperWrapFaceLines` 嘅標題／dek／rumorEcho 稱呼位；回傳多 `nameTier` 欄。連帶修口徑矛盾：anon 期電視版 dek 唔再寫「名字見諸內頁」、搶眼版唔再寫「副導記低咗佢個名／名字上了內頁」。
- 角度（Phase 1-2 穩陣／搶眼）判定同文案骨架不變，只換稱呼層；淡紙路徑（fame < 15）自動行 anon，同既有行為咬合。

### 連載口吻（報紙記得上一份主話題）

- 新增 `newspaperTopicKey(item)`：關聯鍵優先序——①劇情 C3 高俊傑競爭線（eventKey `story:C3:*` → `rival:gao`）②通告 `starHint.name` 紅星（由 eventKey 解出 gigId 查通告）→ `star:<名>` ③標題／dek／作品名出現嘅紅星名（池 `PAPER_TOPIC_STARS`，全虛構）④作品名 → `work:<名>`。
- 新增 `newspaperPrevTopicKey()`：讀剪報列第一份（最近一份）嘅 `topicKey`；舊檔剪報無此欄，就由 eventKeys／標題／dek 即場推斷（舊存檔兼容）。
- `buildNewspaperEdition`：今期主新聞 topicKey 同上一份相同，先喺主新聞 dek 尾加一句跟進句（`newspaperSerialLine`：「本報早前曾報道 X 的消息，今期再有跟進，讀者可對照前文。」／爭位版／作品版）；唔同鍵或者無上一份就唔加，唔硬砌；dek 本身已有「本報早前」就唔疊加。
- edition 新增 `topicKey` 欄；`commitMorningPaper` 將 `topicKey` 存入剪報記錄，接住下一份用。

## 冇改

- SAVE key、softRev、`?v=`；殺青角度判定；花邊短訊；story／award 報紙模板（`{playerName}` 仍寫死「阿偉」——嗰啲係事件報，唔係每日主新聞，留待日後如要統一再開一票）。

## 測試

- 新增 `tests/test_weave31_logic.js`（41 項：門檻邊界／三級稱呼落標題・dek・rumor／anon 口徑矛盾修復／角度不變／關聯鍵四級優先序／連載句／舊檔剪報推斷／edition 整合＋唔疊加）全過。
- 新增 `tests/test_weave31_static.py`（17 項）全過。
- 舊測試全套回歸（P0、P0-3、Weave 1-1／1-2／1-3、2-1／2-2／2-3）無回歸；全檔 script `node --check` 通過。
