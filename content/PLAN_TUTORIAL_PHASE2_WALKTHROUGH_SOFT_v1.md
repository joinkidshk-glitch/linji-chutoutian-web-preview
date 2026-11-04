Soft≠PASS｜教學 Phase2 走查｜未接行為閘｜經 qwen3.7-max｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜鄧 push1+ HOLD｜Soft A/B 唔使

經 Qwen qwen3.7-max 處理

# PLAN_TUTORIAL_PHASE2_WALKTHROUGH_SOFT_v1

## 狀態欄
- **文件**：PLAN_TUTORIAL_PHASE2_WALKTHROUGH_SOFT_v1
- **階段**：Phase 2 教學走查 (Soft)
- **狀態**：Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜鄧 push1+ HOLD

## 走查目標
- 驗證 Phase 2 教學流程嘅敘事與數據連貫性。
- 確認「金龍茶餐廳 (cafe_cha)」與「何生事務所 (agency_ho)」嘅場景切換與對話觸發條件。
- 檢查「手帳傳聞拼合」機制嘅 UI 反饋與邏輯。
- 梳理「人情債」數值變動與對應劇情節點。
- 確保玩家面顯示「何生」，絕不出現「Ho 哥」或真藝名，且無工程詞彙外露。

## 觸發順序總圖
1. 玩家進入「金龍茶餐廳 (cafe_cha)」，觸發茶記閒聊，獲取初始傳聞碎片。
2. 轉移至「何生事務所 (agency_ho)」，何生交代新任務，解鎖「手帳」系統。
3. 打開手帳，進行「傳聞拼合」教學，完成第一次拼圖。
4. 拼合成功後，觸發「人情債」結算畫面，數值更新。
5. 何生給出下一步指示，Phase 2 教學結束，準備進入主線。

## Checklist

| 步序 | 觸發 | 期望畫面 | 齊／缺 | 對照檔 | 備註 |
|---|---|---|---|---|---|
| 1 | 進入金龍茶餐廳 | 茶記全景，NPC 對話彈出 | 齊 | MOCK_UI_PHASE2_LOC_NOTEBOOK_v1.json | 確認場景名顯示正確 |
| 2 | 與茶記老闆對話 | 獲取傳聞碎片，彈出物品獲得提示 | 齊 | TUTORIAL_COPY_PLAN_v1.md | 文案需符合香港書面語（對齊 TUTORIAL_COPY_PLAN） |
| 3 | 前往何生事務所 | 事務所內景，何生站立等待 | 齊 | MOCK_UI_PHASE2_LOC_NOTEBOOK_v1.json | 玩家面必須顯示「何生」 |
| 4 | 何生交代任務 | 對話框顯示任務目標，解鎖手帳 | 齊 | TUTORIAL_COPY_PLAN_v1.md | 禁用任何工程詞彙 |
| 5 | 打開手帳系統 | 手帳 UI 展開，顯示傳聞碎片槽 | 缺 | MOCK_UI_PHASE2_DEEPEN_v1.json | 缺少碎片拖曳引導動畫 |
| 6 | 傳聞拼合教學 | 高亮提示玩家拖曳碎片至拼合區 | 缺 | MOCK_UI_PHASE2_DEEPEN_v1.json | 需補充拼合成功特效 |
| 7 | 拼合成功結算 | 彈出「人情債」數值變動面板 | 齊 | TUTORIAL_COPY_PLAN_v1.md | 數值增減需清晰 |
| 8 | 何生總結 | 何生對話收尾，關閉教學引導 | 齊 | TUTORIAL_COPY_PLAN_v1.md | 確認無多餘按鍵殘留 |

## 缺漏清單
- 手帳 UI 嘅碎片拖曳引導動畫未實裝（對應步序 5）。
- 傳聞拼合成功時嘅視覺特效與音效未配置（對應步序 6）。
- 「人情債」數值變動面板嘅停留時間需微調，避免遮擋何生後續對話。

## Acceptance
- 所有 Checklist 項目必須達到「齊」嘅狀態，且缺漏清單項目已修復。
- 玩家面所有文本與 UI 嚴格遵守命名規範（何生、無真藝名、無工程詞）。
- 教學流程順暢，無卡死或邏輯斷層，符合 Phase 2 敘事節奏。

## Out of scope
- 接行為閘 LIVE
- tip
- 出圖
- 89–92
- 鄧 push1+
- 改 gigs favor

## 擬轉統籌
- 待缺漏清單修復後，進行內部第二次走查。
- 確認無誤後，將 Phase 2 教學模組移交至 QA 團隊進行完整回歸測試。
- 統籌需跟進美術團隊補齊手帳 UI 動畫與拼合特效。
