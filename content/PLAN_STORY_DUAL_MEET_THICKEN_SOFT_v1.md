Soft≠PASS｜雙女 meet Soft 加厚重開票｜嚴格綁 C3/C4 FULL Soft A｜經 qwen3.7-max｜對白經 DeepSeek｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜鄧 push1+ HOLD

[經 Qwen qwen3.7-max 處理]

# PLAN_STORY_DUAL_MEET_THICKEN_SOFT_v1

**核心標記**：Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜鄧 push1+ HOLD

## 1. 背景／停因對照
- **背景**：《臨記出頭天》雙女主（曉晴、采兒）初遇劇情需要加厚，以提升角色立體感與敘事張力。
- **停因對照**：早前 sandbox 階段曾暫停加厚，主因是當時未跟足 FULL 規格，且行為閘 Soft 門檻鬆、未嚴格綁定 C3/C4。
- **重開原則**：而家重開必須嚴格跟足 FULL Soft A 規格，並落實行為閘 Soft 綁定，確保劇情觸發與玩家進度完全同步。

## 2. 閘綁定
嚴格綁定 FULL Soft A 規格，確保劇情解鎖與主線章節掛鉤：
- **曉晴初遇 (`R_hiu_meet`)**：掛於 **C3 後**。內部觸發條件（openGate）設定為 `hiu = needDone C3`。
- **采兒初遇 (`R_choi_meet`)**：掛於 **C4 後**。內部觸發條件（openGate）設定為 `choi = needDone C4`。
- **玩家面展示**：絕對禁止出現工程詞（如 flag、gate、week-gate、SHA 等），統一以「主線進度」、「章節解鎖」等自然語言描述。經理人對外統一稱呼為「何生」（內部 favor target 仍用 `agency_ho`），禁用「Ho 哥」及真藝名。

## 3. 加厚範圍
- **敘事維度**：深化曉晴與采兒的初遇背景、性格衝突與潛在動機。
- **數據預留**：
  - 預留 `chromeSeason` 與 `playerMeta` 欄位。
  - 跟隨 chrome Soft A 規格：主線 · 1988{{季}}。
  - 季節變數以 `seed.season` 為優先讀取來源，確保場景描述與當前遊戲季節一致。

## 4. 節拍規格表（hiu／choi）
### 曉晴 (`R_hiu_meet`) - 綁定 C3 後
| 節拍 (Beat) | 敘事目標 | 內部條件 / 數據 | 玩家面描述 |
|---|---|---|---|
| B1 | 場景鋪墊與氛圍 | `seed.season` 讀取 | 根據當前季節顯示環境描述 |
| B2 | 曉晴登場與初步互動 | `openGate: needDone C3` | 完成第三章後解鎖 |
| B3 | 核心對話與性格展現 | `agency_ho` 關聯 | 提及經理人何生的安排 |

### 采兒 (`R_choi_meet`) - 綁定 C4 後
| 節拍 (Beat) | 敘事目標 | 內部條件 / 數據 | 玩家面描述 |
|---|---|---|---|
| B1 | 衝突前置與懸念 | `seed.season` 讀取 | 根據當前季節顯示環境描述 |
| B2 | 采兒登場與張力建立 | `openGate: needDone C4` | 完成第四章後解鎖 |
| B3 | 利益交織與後續伏筆 | `agency_ho` 關聯 | 提及經理人何生的態度 |

## 5. Mock 交付
以下為劇情骨架（Skeleton），對白暫以 stub 形式標示，後續交由 DeepSeek 深化。

**曉晴初遇 (`R_hiu_meet`)**
```text
[Scene: 片場外 / 季節: {{seed.season}}]
曉晴: (看著通告單) [pendingDeepSeek: 表達對目前處境的無奈與對演戲的堅持]
玩家: [pendingDeepSeek: 回應選項 A/B]
曉晴: 何生那邊... [pendingDeepSeek: 提及經理人何生的壓力，帶出性格]
```

**采兒初遇 (`R_choi_meet`)**
```text
[Scene: 化妝間 / 季節: {{seed.season}}]
采兒: (補妝，透過鏡子看玩家) [pendingDeepSeek: 帶出防備心與競爭意識]
玩家: [pendingDeepSeek: 回應選項 A/B]
采兒: 以為何生捧你... [pendingDeepSeek: 點出經理人何生的資源分配，建立衝突]
```

## 6. Soft A/B
為方便統籌抽樣與測試，提供兩種加厚深度方案：
- **Soft A（輕量加厚）**：+1–2 beat。側重背景加厚，對白微延，不改變主線節奏。**（建議採用，方便 Soft 抽樣測試）**
- **Soft B（重量加厚）**：+3–4 beat。加入額外衝突軸與支線互動，大幅增加文本量與演出時間。
- **決策**：目前預設推行 Soft A，最終方案待統籌拍板。

## 7. Acceptance
- 曉晴劇情嚴格在 C3 完成後觸發，采兒劇情嚴格在 C4 完成後觸發。
- 玩家介面（UI/UX）及對話中，絕無「Ho 哥」、真藝名及任何工程詞。
- 經理人稱呼對外統一為「何生」，內部數據 `agency_ho` 運作正常。
- `chromeSeason` 與 `playerMeta` 正確讀取 `seed.season`，季節描述無誤。
- 所有核心標記（Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜鄧 push1+ HOLD）已落實並限制相關流程。

## 8. Out of scope
- 不涉及 C3/C4 主線核心劇情的改寫。
- 不包含 Soft B（重量加厚）的完整實作（除非統籌後續要求）。
- 不包含美術出圖（出圖 HOLD）及 89–92 相關內容（89–92 HOLD）。
- 不涉及 LIVE 營運活動提示（唔 tip LIVE）。

## 9. 擬轉統籌
- 本計劃及規格表確認後，將連同 Mock skeleton 轉交統籌團隊。
- 統籌需拍板 Soft A/B 選擇，並協調 DeepSeek 進行對白深化（處理 pendingDeepSeek 部分）。
- 跟進鄧 push1+ 進度（鄧 push1+ HOLD 狀態解除後推進）。
