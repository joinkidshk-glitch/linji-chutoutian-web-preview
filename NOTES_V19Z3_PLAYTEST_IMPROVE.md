# v19z3 — playtest improve（P0–P2）

Branch `fix/playtest-improve-v19z3`. Implements all items from《臨記出頭天 · 阿偉》v19z2 再試玩改善方向.

## Fixes

| # | Pri | Bug | Fix |
|---|-----|-----|-----|
| 1 | P0 | 星河／海港針重疊誤點 | 座標錯開；同區近針扇形展開；點擊 nearest-pin（≤10%）；加大 hit；本區地點列表備選 |
| 2 | P0 | 事態中背景可扣茶錢 | `story-play-lock` + `#mask.story-play-on` 鎖 pin／loc-acts；`isStoryPlayActive` 擋 `openLoc`／`applyMockAsk`；關閉清鎖 |
| 4 | P0 | 獲聘誤標已殺青 | `gigLifecycleStatus`：hired→shooting→wrapped；`gigRecruitStatus` 跟三態；Detail 已接改「查看檔期」 |
| 7 | P0 | 過週今日計劃殘留試鏡 | 過週 `enterHome(editable)` 清 `audition:`／`wrap:`；`todayPlanId` 防殘留 |
| 5 | P1 | 已完成仍接通告 | `ensureEntryTierBoardFill` 跳過 consumed；快捷列改「查看檔期」；Detail early-return |
| 6 | P1 | 拍攝簿空白 | `S.wrapHistory` 殺青寫入；`showJobs` 顯示進行中＋履歷 |
| 8 | P1 | 跨日休息吞結算 | 街頭／咖啡／休息標題帶「週X」日結卡，逐日 modal 繼續 |
| 9 | P1 | 傾談後送禮仍鎖 | 傾談寫 `gift_met_*`／`flag_*_talk_met`；`canGive` 認 met；文案改寫門檻 |
| 10 | P1 | 人情債無還款 CTA | 債卡「去還」→ 跳事務所＋`openHoRepaySheet`；顯示金額／建議 |
| 11 | P1 | 週結大字易誤讀 | 主數字「本週淨結餘」加減色；收入／生活費次行 |
| 3 | P2 | 事態完成仍閃播事態 | `markDone`／`leaveStory` 同 tick／關閉後 `openLoc` 刷新灰態 |
| 12 | P2 | 類型標籤不一 | 快捷列主類型＋副標；`成功率 N%` |
| 13 | P2 | 檔期黏字 | 工作天與報名截止換行 |
| 14 | P2 | 差幾多漏達標 | 達標 ✓／未達 ✗ 紅字＋差值 |
| 15 | P2 | 右欄空白地點 | `closeSheet` 空態「點地圖針選擇地點」 |
| 16 | P2 | 熟人針 vs 未見熟人 | 針標只跟 `locNpc`；文案說明 |
| 17 | P2 | 傳聞 toast 虛 | toast 帶「傳聞『標題』」 |
| 18 | P2 | 打招呼像情報 | 何生打招呼副文改寒暄 |
| 19 | P2 | 第2週行程重複 | `defaultWeekPlan` 依訓練／欠債差異化 |
| 20 | P2 | soft 免費社交可刷 | 每日上限：傾談3／打聽5／打招呼3；UI 顯示剩餘 |
| 21 | P2 | 選單無傳聞／人情債 | 選單捷徑 → 手帳分頁 |
| 22 | P2 | 教學地圖提示過長 | 單一針焦點（星河）；map-hint 縮短 |

## Key symbols

`gigLifecycleStatus` · `isGigWrapped` · `isStoryPlayActive` · `setStoryPlayLock` · `softSocialDailyCap` · `drawMap`（cluster／nearest）· `wrapHistory` · `showJobs` · `renderDebtPane` repay CTA

## Cache

`?v=19z2` → `?v=19z3`.

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z3&softBehaviorGate=1`

1. 九龍塘連點星河 ≥9／10 開對  
2. 播事態連點茶錢 10 次，餘額不變  
3. 接通告後徽章＝已獲聘（非已殺青）  
4. 過週後今日計劃＝當日手帳格  
5. 傾談後可送禮（或門檻文案正確）  
6. 週結主數字＝淨結餘  
