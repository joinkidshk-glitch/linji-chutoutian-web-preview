Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜禁「Ho 哥」→「何生」／favor `agency_ho`｜經 qwen3.7-max｜玩家面禁真藝名／禁工程詞

# PLAN_TUTORIAL_PHASE2_NITS_MODAL_SCROLL_SOFT_v1

## 繼承走查 73602f5a 缺漏
- 步序 5：缺拖曳引導動畫。
- 步序 6：缺拼合特效。
- 未接行為閘。

## 新增 modal 豎滾 nit
- **問題**：狀態／教學／StoryPlay／Casting 等 modal 內容過長時，底欄被頂走或無法滾動。
- **對照精神**：
  - v17w：`#modal-btns` sticky／flex:0 釘底。
  - v17x：`#modal-inner` flex:1 1 0% + min-height:0 + overflow-y:auto。
- **要求**：`#modal-inner`（或同等容器）可豎滾；底欄／CTA `#modal-btns` sticky 可見、唔被內容頂走。
- **限制**：唔改 LIVE tip／唔抬 `?v=`。

## Soft 驗點 checklist
1. [ ] 步序 5 拖曳引導動畫觸發與顯示。
2. [ ] 步序 6 拼合特效播放與結束回調。
3. [ ] 長內容 modal（如 Casting 詳情）滾動時，`#modal-inner` 正常豎滾。
4. [ ] 長內容 modal 滾動時，`#modal-btns` 保持釘底可見，無被遮擋。
5. [ ] 確認未接行為閘無引發 crash 或死鎖。

## 範圍與狀態
- **Soft A/B**：唔使。
- **未接行為閘**：保持現狀，唔 tip LIVE。
- **出圖 HOLD**：美術資源暫不更新。
- **89–92 HOLD**：時代深度鎖原樣。

## Acceptance
- 教學步序 5/6 動畫特效還原。
- Modal 豎滾與釘底 CTA 符合 v17w/v17x 精神。

## Out of scope
- LIVE tip 改動。
- `?v=` 版本號提升。
- 行為閘底層重構。

## 擬轉統籌
- 驗收通過後，將 modal 滾動規範與教學特效缺漏修復轉交統籌排入正式 sprint。
