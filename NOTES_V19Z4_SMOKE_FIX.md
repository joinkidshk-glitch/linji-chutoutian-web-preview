# v19z4 — smoke-test fix（v19z3 驗收失敗項）

Branch `fix/playtest-smoke-fix-v19z4`. Hardens seven smoke failures from official `?v=19z3`.

## Root causes & fixes

| # | Smoke FAIL | Root cause | Fix |
|---|------------|------------|-----|
| 1 | 事態中仍扣茶錢 | CSS `#mask ~ #app` 無效（mask 在 app **之後**）；鎖只靠 class，loc-acts 仍可點；`applyMockAsk` 閘偶發未擋 | `_storyPlayLocked` boolean latch；`setStoryPlayLock` 禁用 `#loc-acts`／sheet；click 再檢；`applyMockAsk` 雙閘；修 CSS |
| 2 | 傾談後送禮仍「沒打過照面」 | `unmet` 文案仍在 JSON；met flag 只寫 romance key；`canGive` 閉包舊 gate | `talkMetOk` 雙寫 romance+map id；`gift_talked_*`；click 時 live `canGive`；改 unmet 文案 |
| 3 | 週結大字 −$生活費 | `apply({money:-paid})` 的 `<span class="bad">−$ …</span>` 仍入 notes，視覺蓋過淨結餘 | 扣款唔入 HTML notes；主塊 `settle-net`＝本週淨結餘；次行方程「收入 − 生活費 ＝ 結餘」 |
| 4 | 事態完仍「播事態」 | `markDone` 喺 story 仍 active 時 `setTimeout(0)` 跳過 `openLoc` | `refreshLocAfterStory` 輪詢至鎖清；`leaveStory`／劇情結算 dismiss／wrapBtn 都刷新 |
| 5 | 獲聘後仍「接通告」 | `scheduleShoot` 未踢晒各 loc board | 獲聘 `push` 後清所有 `S.board`；`openLoc` 再濾 active shoots |
| 6 | 拍攝簿殺青空白 | `wrapHistory` load 未初始化；舊檔無履歷 | `load()` 保底 `[]`；`ensureWrapHistoryFromFlags` 由 `done_*` 補履歷；`showJobs` 先補再渲染 |
| 7 | 人情債無「去還」 | CTA 有時唔顯眼／漏綁 | `.debt-repay-btn` 強制顯示；包 `debt-cta-wrap` |

## Cache

`?v=19z3` → `?v=19z4`

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z4&softBehaviorGate=1`

1. 播 C1 事態中連點「大堂飲茶」10 次 → 餘額不變、toast「事態進行中」
2. 傾談林曉晴後 → 送禮可開（或門檻文案講明相遇／傾談，永唔「沒打過照面」）
3. 週結主數字＝本週淨結餘（加減色）；生活費唔做大字頭條
4. 事態完成關結算後 → 地點列即變「事態已完成」／無「播事態」
5. 獲聘《跟組雜務》後開海港 → 無「接通告」該單
6. 殺青後拍攝簿 → 有「已殺青履歷」
7. 人情債何生／老張卡 → 有「去還」
