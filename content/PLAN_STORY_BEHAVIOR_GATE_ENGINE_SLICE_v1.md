> Soft≠PASS｜行為閘引擎切片｜經 qwen3.7-max｜唔 tip｜LIVE week-gate 仍 active（liveWeekGateStillActive）｜89–92 HOLD

# 行為閘引擎切片計劃（PLAN_STORY_BEHAVIOR_GATE_ENGINE_SLICE_v1）

## 1. 目的與範圍
本檔為《臨記出頭天》行為閘（Behavior Gate）的 **引擎切片（Engine Slice）接線規格**，主要受眾為 iOS Soft 實作與統籌抽樣人員。文件旨在說明 iOS Soft 端如何讀取 stub 的 `nodes[].trigger` 欄位、執行評估順序，並與現有的 LIVE week-gate 機制並存。

**核心原則**：
- 本輪 **唔 tip LIVE**，LIVE 路徑暫仍維持 week-gate only。
- **唔改** 89–92 節點；出圖流程 HOLD。
- 引擎切片只負責讀取 stub 並評估，**唔改** 已拍板的 trigger 數值。

## 2. Soft A/B 鎖一覽
以下為已拍板的 Soft A/B 鎖，實作時必須 **一字不差** 對齊：

- C1：`cafe_cha`
- weekMin：**保留**（各節現有 weekMin 仍作 Soft 地板；LIVE **暫仍 week-gate only** 直至 tip）
- C3：聲量 **>15** → stub `fameMin:16`／`fameCompare:'>'`／tag `fameMin_16`
- C4：`favor≥1` @ 事務所 → `favorMin:1`＋`favorTarget:'agency_ho'`＋`locIdAny` 含 `agency_ho`＋`softLogic:'AND'`（favor∧loc）
- C5：季節＋loc＋rumor **軟**（`rumorSoftPriority`／季節 autumn|winter；rumor 種子軟優先）
- `rival_gao`：**唔混入 C5**（HOLD；只留 C3 選擇旗 `rival_gao_hard`／`rival_gao_endure`）
- 89–92：**唔改**
- Soft≠PASS；**唔 tip LIVE** 直至 tester OK
- `liveWeekGateStillActive:true`；`tipForbidden:true`

## 3. trigger 欄位字典
iOS Soft 讀取 `nodes[].trigger` 時，需支援以下欄位解析：

| 欄位 | 說明 |
|---|---|
| `needDone` | 前置節點完成清單（如 `["C1"]`）。 |
| `minDaysAfterPrev` | 距離上一節點完成的最少日數。 |
| `weekMin` | 週數地板（Soft 評估用，LIVE 暫不依賴）。 |
| `locIdAny` | 地點白名單（如 `["cafe_cha", "tvb_longmen"]`）。 |
| `rumorAny` | 觸發所需的傳聞種子清單。 |
| `favorMin` | 最低好感度門檻。 |
| `favorTarget` | 好感度計算對象（如 `agency_ho`，即何生）。 |
| `softLogic` | 複合條件邏輯（如 `AND` 代表 favor 與 loc 必須同時滿足）。 |
| `fameMin` | 聲量最低門檻數值。 |
| `fameCompare` | 聲量比較運算子（如 `'>'`）。 |
| `tagAny` | 必須具備的標籤清單（如 `fameMin_16`）。 |
| `seasonAny` | 季節白名單（如 `["autumn", "winter"]`）。 |
| `gigCountMin` | 最低接 job 次數。 |
| `rumorSoftPriority` | 布爾值，啟用傳聞軟優先邏輯。 |
| `rumorSeedsRequired` | 布爾值，強制要求傳聞種子必須存在。 |
| `relAny` | 關係網絡白名單。 |

## 4. 評估順序（evalOrder）
為確保效能與邏輯一致性，建議 iOS Soft 依以下順序執行 trigger 評估（短路求值）：

1. `needDone`（前置節點檢查）
2. `minDaysAfterPrev`（冷卻日數檢查）
3. `weekMin` 地板（週數下限檢查）
4. `loc` / `locIdAny`（地點檢查）
5. `favor` / `softLogic:'AND'`（好感度與複合邏輯檢查）
6. `fame` / `fameMin` / `fameCompare`（聲量檢查）
7. `gigCountMin`（接 job 次數檢查）
8. `seasonAny`（季節檢查）
9. `rumor` 軟邏輯（`rumorSoftPriority` / `rumorSeedsRequired`）
10. `tagAny` / `flags`（標籤與旗標檢查）

## 5. 專節實作備註

### 5.1 C3：聲量 >15 實作
- **數值對齊**：聲量大於 15，實作上設定 `fameMin: 16` 且 `fameCompare: '>'`（或等價邏輯 `fame > 15`）。
- **標籤綁定**：必須同時檢查 `tagAny` 包含 `fameMin_16`。
- **選擇旗**：C3_a 綁定 `rival_gao_hard`；C3_b 綁定 `rival_gao_endure`。

### 5.2 C4：AND 邏輯（favor∧loc）
- **複合條件**：`favorMin: 1` 且 `favorTarget: 'agency_ho'`，同時 `locIdAny` 包含 `agency_ho`。
- **邏輯運算**：`softLogic: 'AND'` 確保好感度與地點條件必須 **同時成立**。
- **稱呼規範**：經理人統一稱為「何生」，**嚴禁** 使用「Ho 哥」。
- **選擇旗**：C4_a 綁定 `flag_refuse_gig_with_ho`；C4_b 綁定 `flag_take_harsh_gig`。

### 5.3 C5：季節與 rumor 軟優先
- **季節限制**：`seasonAny` 限定為 `autumn` 或 `winter`。
- **軟優先邏輯**：啟用 `rumorSoftPriority: true` 與 `rumorSeedsRequired: true`，確保傳聞種子（`choi_recent_news`, `hau_ching_recent_news`）在評估時享有軟優先權。
- **選擇旗**：C5_a 綁定 `choi_honest`；C5_b 綁定 `choi_spin`；C5_c 綁定 `choi_dodge`。

### 5.4 rival_gao HOLD
- `rival_gao` 相關邏輯 **唔混入 C5**（HOLD 狀態）。
- 僅保留 C3 的選擇旗（`rival_gao_hard` / `rival_gao_endure`）作為後續分支依據。

## 6. 與 LIVE week-gate 並存策略
- **LIVE 路徑**：維持現狀，只認可 `week-gate`（`liveWeekGateStillActive: true`）。
- **Soft 路徑**：透過 feature flag 或 `#if Soft` 編譯宏，啟用 Soft preview 路徑，讀取 stub 的 `nodes[].trigger` 行為欄位。
- **合流時機**：在 tester 確認 OK 且正式 tip 之前，兩條路徑 **唔合流**。`tipForbidden: true` 必須嚴格執行。

## 7. iOS Soft hooks 建議
為方便除錯與擴充，建議在 `stub.engineSlice.iosSoftHooks` 實作以下 hook 點：

- `hook_preEvaluate(nodeId)`: 進入節點評估前觸發，用於 log 當前狀態。
- `hook_softLogicAND_resolve(favorResult, locResult)`: 專門處理 C4 的 AND 邏輯結果。
- `hook_rumorSoftPriority_check(rumorSeeds)`: 處理 C5 傳聞種子軟優先權的解析。
- `hook_fameCompare_eval(currentFame, fameMin, operator)`: 處理 C3 聲量比較運算。
- `hook_postEvaluate(nodeId, isPass)`: 評估結束後觸發，記錄通過與否。

## 8. 玩家面禁寫門檻工程詞
- **禁用詞彙**：玩家介面與文案中，嚴禁出現 `trigger`、`loc`、`flag`、`fameMin`、`need_done`、`weekMin` 等工程詞彙。
- **鎖因書面語**：當條件未滿足導致節點鎖定時，必須使用通順的書面語解釋（例如：「暫未能報」、「離開」、「時機未到」），而非顯示工程變數。
- **nextHint**：保持為空或 **唔顯示**，避免洩露底層邏輯。

## 9. 驗收清單
- [ ] 頁眉與 `liveWeekGateStillActive` 狀態確認無誤。
- [ ] Soft A/B 鎖一覽已 **一字不差** 寫入並對齊 stub。
- [ ] C3 `fameMin:16` / `fameCompare:'>'` / `fameMin_16` 實作正確。
- [ ] C4 `softLogic:'AND'` 與 `favorTarget:'agency_ho'` 邏輯通過測試。
- [ ] C5 `rumorSoftPriority` 與季節 `autumn|winter` 評估正常。
- [ ] `rival_gao` 確認 **唔混入 C5**，僅存於 C3 選擇旗。
- [ ] LIVE 路徑仍為 week-gate only，Soft 路徑透過 feature flag 隔離。
- [ ] 玩家面文案已清除所有門檻工程詞，經理人統一稱呼「何生」。
- [ ] choice/flags id 沿用 LIVE 規範（`route_tv` / `route_film` / `flag_network_stay` / `flag_hustle_board` 等），無擅自更改。

## 10. Out of scope
- 89–92 節點修改。
- 正式 tip LIVE（本輪 `tipForbidden`）。
- 出圖流程（HOLD）。
- 更改 LIVE 現有 week-gate 邏輯。
- 更改 choice id。
- 更改已拍板的 trigger 數值與結構。
