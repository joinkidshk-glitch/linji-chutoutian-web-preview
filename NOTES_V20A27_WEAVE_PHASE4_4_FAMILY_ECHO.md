# NOTES v20a27 — Weave Phase 4-4：鏈 G 第 2 拍（報紙首次點名 → 屋企回音）＋ 4-3 覆檢跟進（屋企卡排序）

版本：v20a27（soft 預覽；SAVE key `starVolunteer_map_v19w`、softRev `s107`、`?v=` 不變）

## 一、鏈 G 第 2 拍：報紙首次點名 → 屋企回音

規劃原文（weave plan 鏈 G 第 2 拍）：「當報紙第一次點名寫玩家，觸發屋企事件：屋企人剪低份報紙／打嚟茶餐廳搵人（嗰年代無手提電話，打去茶餐廳／事務所留言）——阿偉第一次覺得自己『似返個人』。」

### 偵測（掛點＋狀態）
- 新函數 `familyPaperEchoTick()`，掛喺 `commitMorningPaper` 主流程尾、`saveQ()` 之前呼叫一次（`familyPaperEchoTick` 全檔只此一個呼叫點）。放在 saveQ 前，`paperTier`／`echoNote` 狀態同今期剪報同一次落盤；`edition.fameApplied===true` 嘅重入路徑行唔到呢度，唔會重複計同一期。
- 狀態存 `S.familyHome`（接 4-3 同一個 state 物件，`ensureFamilyHomeState` 擴欄＋正規化，舊檔安全）：
  - `paperTier`：上一次 commit 觀察到嘅點名級別（`""`＝未觀察過；`"anon"`／`"named"`／`"titled"`）。
  - `echoNote`：觸發後寫入嘅常駐字條（空字串＝未觸發，同時係一次性旗）。
  - `echoDay`：觸發日（dayIndex）。
- 規則（逐期 commit 計一次 `newspaperNameTier()`，用 commit 當刻 `S.fame`——即嗰期 fameDelta 落帳之後嘅級別）：
  - **首次觀察只初始化、永不觸發**：任何存檔第一次行到呢段（`paperTier===""`），只記低當刻級別。舊檔就算 fame 已過 named/titled 門檻都**唔補觸發**——事件屬於「第一次見報紙寫你名嗰一刻」，過咗就唔扮返（決定，唔係限制）。
  - **首次跨級先觸發**：`paperTier==="anon"` 且今期係 `named` 或 `titled`（直跳 titled 都算）嗰期觸發；`named→titled` 唔係首次跨級，唔觸發。
  - 一次性：`echoNote` 寫入後，之後任何跨級都唔再觸發。
- 冇改 `newspaperNameTier` 本體、冇改報紙內容生成；今票只加偵測＋呈現。

### 呈現（三樣齊，文案原文）
1. **toast（兩段式，跟 favor toast 先例避 40 字截斷）**：
   - 主句：`茶餐廳伙記轉告：你阿媽打嚟，話喺報紙見到你個名。`
   - 副句：`佢問嗰個係咪真係你，又囑你記得食飯。嗰版報紙佢剪低收好咗——手帳剪報頁有得睇返。`（尾句即剪報收藏提示：嗰期報紙喺 commit 時已入 `S.newspaperClippings`，輕量文字提示，冇改剪報系統。）
2. **屋企卡常駐回音字條**（`renderDebtPane` 屋企卡內、`family-attitude` 態度字條之後另一行，class `family-echo`，由 `familyEchoNoteText()` 讀 `echoNote`）：
   - `屋企回音：阿媽將嗰版寫住你名嘅報紙剪咗落嚟，夾喺本電話簿入面，摺得整整齊齊。嗰句冇講出口嘅驕傲，佢用把較剪講晒。`
3. 剪報提示：見 toast 副句尾（冇另加 UI）。

### 文案口徑出入（決定）
- 規劃原文寫點名「陳偉翔」（全名），但 LIVE 報紙點名一律用「阿偉」（`newspaperPlayerRef`：named＝「阿偉」、titled＝「人氣新人阿偉」；全名只喺標題畫面介紹出現）。今票跟 LIVE，唔改口徑；觸發條件亦只認 tier 跨級，唔認字串。

### 邊界（誠實記錄）
- 回音字條寄居喺屋企債卡：若觸發嗰陣屋企債啱啱還清、未到下期補種，卡暫時唔喺債頁，字條要等下期屋企卡返嚟先見到（狀態常駐 `echoNote`，唔會唔見）；toast 係即時主呈現，唔受影響。

## 二、4-3 覆檢跟進：屋企卡顯示排序

- 背景：Phase 4-3 實機抽查發現，新檔人情債頁有 3 張卡，屋企嗰張（`debt_family_home`）排第 3（前面係春季季節卡「何生春季數」「老張開春器材數」）。但鏈 G 第 1 拍原意係「開局手帳第一筆唔係圈內債，係屋企」，屋企卡應該排第一。
- 修法（**只改顯示次序，唔郁數據**）：`renderDebtPane` 將債卡生成改為 `{id, html}` 陣列，輸出時抽出屋企卡（`famCardsHtml`）排喺 banner 之後、季節卡／債權卡／其餘債卡之前；其餘卡保持現有相對次序。`S.mockDebts` 陣列本身一字不動，還款、壓力、帳本等邏輯零影響。冇債冇卡時嘅「清晒」空狀態行為不變（改為獨立 `emptyHtml`，條件等值）。

## 三、測試

- 新增 `tests/test_weave44_logic.js`（29 項，全過）：行真 `commitMorningPaper`＋真 `renderDebtPane`＋真 `ensureFamilyHomeDebt`：
  - (a) 首次觀察三種舊檔形狀（anon/named/titled）都只初始化、唔觸發；
  - (b) anon→named 嗰期觸發一次（包括靠嗰期 fameDelta 14+2 推過門檻嗰期）、之後再出報紙／再升 titled 都唔重複，toast 兩段式＋文案＋嗰期入剪報齊驗；
  - (c) anon→titled 直跳觸發；(d) named→titled 唔觸發；
  - (e) 觸發後真渲染屋企卡有 `family-echo` 字條（喺態度字條之後、重渲染常駐）；(f) 觸發前冇字條；
  - 排序（新檔形狀：春季季節卡 2 張＋債 3 筆、屋企債數據排中間）：屋企卡係輸出第一張卡、喺季節卡之前、其餘債相對次序不變、`S.mockDebts` 數據次序渲染後冇變。
- 新增 `tests/test_weave44_static.py`（27 項，全過）：接線、狀態預設／正規化、跨級條件原文、saveQ 前掛點、字條位置、排序接線、點名門檻不變、全名只留 2 處、慣例不變。
- 全套回歸：tests/ 共 34 檔（17 邏輯＋17 靜態）全部 PASS，零回退；全檔 inline script `node --check` OK。

## 四、取捨／未做
- 偵測用 commit 當刻 fame 計 tier（唔係報紙生成嗰刻）：嗰期 fameDelta 推過門檻嗰期即算「首次點名嗰期」，同玩家感受一致（朝早攞起份報紙嗰陣聲望已升）。
- 唔做回音專屬 modal／動畫：鏈 G 定位係「細額長流」嘅個人勾，toast＋常駐字條已經夠，唔搶主線呈現。
