> 狀態更正：本規格嘅 FX→GD 移交已由 #24 收口。教學步 5–6 copy Done Soft（#23 `8a63e477`）；FX assets＋wire Done Soft（#24 `ff1d5eed`，`artHold:false`）。下文「缺 FX／交 GD」係 copy 規格當時範圍，唔再當 FX HOLD。Soft≠PASS｜唔 tip LIVE｜`?v=` 仍 19w。

Soft≠PASS｜教學 Phase2 步5–6 Soft overlay｜經 qwen3.7-max｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜FX→GD｜唔改 tutorial_zh_HK.json 主教學1–7（另線 Phase2 overlay）

# PLAN_TUTORIAL_PHASE2_STEPS_5_6_COPY_SOFT_v1

## 1. 範圍與 Soft overlay 說明

本檔為《臨記出頭天》教學 Phase2 步5至步6之 Soft overlay 規格草案。
- **Soft≠PASS**：本檔僅為邏輯與文案槽位對齊之 Soft 規格，不等於最終實裝通過（PASS）。
- **獨立覆蓋**：本 overlay 僅針對 Phase2 步5（手帳傳聞拖曳）與步6（拼合結算）進行擴充，**絕對唔改 `tutorial_zh_HK.json` 主教學1–7**，主線教學維持原檔不動。
- **玩家面長句**：本檔提供之玩家面文案僅為語意範例（Placeholder），最終長句與潤飾交 DeepSeek 另產。

---

## 2. 步5規格表：打開手帳／傳聞碎片槽／拖曳引導

| 規格維度 | 說明與對齊 |
| :--- | :--- |
| **觸發條件** | 玩家於手帳介面點擊「傳聞」分頁，且擁有 ≥2 塊可拼合之傳聞碎片。 |
| **畫面焦點** | 傳聞碎片槽、拖曳引導指示（缺 FX，實作交由 GD）。 |
| **Coach 文案槽** | 引導玩家將兩塊相關碎片拖曳靠近，觸發拼合預覽。 |
| **字數上限** | Coach 提示 ≤ 25 字；碎片狀態描述 ≤ 15 字。 |
| **禁寫事項** | 禁工程詞入玩家面、禁真藝名、禁「Ho 哥」（須用「何生」）、禁 tip LIVE。 |
| **對齊 MOCK 鍵** | `MOCK_UI_PHASE2_LOC_NOTEBOOK_v1.json`：<br>• `notebook.tabs.rumors` (傳聞分頁)<br>• `rumors.state.normal` (一般碎片)<br>• `rumors.state.teased` (拖曳靠近時之高亮狀態) |
| **玩家面長句** | **待 DeepSeek**（見 `MOCK_TUTORIAL_PHASE2_STEPS_5_6_COPY_SOFT_v1.json`） |

---

## 3. 步6規格表：拼合確認／成功／失敗／人情債結算

| 規格維度 | 說明與對齊 |
| :--- | :--- |
| **觸發條件** | 兩塊碎片拖曳重疊達判定閾值，或點擊「拼合」按鈕。 |
| **畫面焦點** | 拼合確認彈窗 → 成功蓋章 (Stamp) / 失敗提示 (Toast) → 人情債結算浮層。 |
| **字數上限** | 確認/失敗 Toast ≤ 20 字；成功 Stamp 線 ≤ 30 字；人情債結算 ≤ 25 字。 |
| **禁寫事項** | 禁工程詞入玩家面、禁真藝名、禁「Ho 哥」（須用「何生」）、禁 89-92 數值。 |
| **對齊 MOCK 鍵** | `MOCK_UI_PHASE2_DEEPEN_v1.json`：<br>• `mergeFlow.confirmLabel` / `cancelLabel`<br>• `mergeFlow.successStampLine`<br>• `mergeFlow.failToast` / `noPairHint` / `emptyState`<br>• `toasts.mergeGlow` (狀態標記) |
| **玩家面長句** | **待 DeepSeek**（確認／stamp／fail／人情債結算 → MOCK JSON） |

---

## 4. 按鈕標籤規格

按鈕標籤沿用 `MOCK_UI_PHASE2_DEEPEN_v1.json` 之 deepen 鍵，確保 UI 組件一致性。

| 按鈕動作 | 對齊 MOCK 鍵 | 玩家面短標籤範例 | 備註 |
| :--- | :--- | :--- | :--- |
| **確認拼合** | `mergeFlow.confirmLabel` | 確認拼合 | 玩家面長句/動態文案待 DeepSeek 另產 |
| **取消拼合** | `mergeFlow.cancelLabel` | 取消 | 玩家面長句/動態文案待 DeepSeek 另產 |
| **關閉結算** | `mergeFlow.closeSettle` | 知道了 | 人情債結算後關閉浮層 |

---

## 5. Acceptance Checklist

- [ ] **Soft≠PASS**：已標識本檔為 Soft 規格，非最終實裝。
- [ ] **主檔隔離**：確認無修改 `tutorial_zh_HK.json` 主教學 1-7 邏輯。
- [ ] **稱呼替換**：全文已將「Ho 哥」替換為「何生」，無遺漏。
- [ ] **禁真藝名**：玩家面範例僅使用「何生」或虛構代稱，無真實藝名。
- [ ] **禁工程詞**：玩家面文案範例純淨，無 `locId`、`req key` 等工程詞彙。
- [ ] **硬閘 HOLD**：確認無涉及 LIVE 提示、出圖流程、89-92 相關內容。
- [ ] **FX 移交**：確認所有動畫、特效、音效實作已列入 Out of scope 並標記交 GD。

---

## 6. Out of Scope

以下項目**不在**本 Soft overlay 規格範圍內，需交由對應團隊或另開規格處理：

1. **FX／動畫／音效實作**：拖曳光效、拼合蓋章動畫、成功/失敗音效 → **交 GD (Graphics/Game Designer)**。
2. **改 LIVE**：不涉及任何 LIVE 直播相關邏輯或提示（唔 tip LIVE）。
3. **出圖流程**：不涉及出圖相關判定與 UI（出圖 HOLD）。
4. **89–92 相關**：不涉及 89-92 之數值、劇情或特殊狀態（89-92 HOLD）。
5. **改 gigs**：不修改 gig（通告/工作）系統底層邏輯。
6. **改主檔**：嚴禁修改 `tutorial_zh_HK.json` 主教學 1-7 內容。

---

## 7. 擬交 iOS 路徑約定

本輪 Soft 產物（content＋store 雙寫；交 iOS 用 overlay，唔改主教學）：

- `content/PLAN_TUTORIAL_PHASE2_STEPS_5_6_COPY_SOFT_v1.md`（本規格）
- `content/MOCK_TUTORIAL_PHASE2_STEPS_5_6_COPY_SOFT_v1.json`（玩家面經 DeepSeek）
- `content/MOCK_TUTORIAL_PHASE2_STEPS_5_6_COPY_SOFT_v1.md`（人讀表）
- 對齊參照：`MOCK_UI_PHASE2_DEEPEN_v1.json`、`MOCK_UI_PHASE2_LOC_NOTEBOOK_v1.json`、`PLAN_TUTORIAL_PHASE2_WALKTHROUGH_SOFT_v1.md`