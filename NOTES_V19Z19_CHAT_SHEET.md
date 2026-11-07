# v19z19 — 傾談死鍵＋地點 sheet CTA 首屏

Branch `fix/playtest-chat-sheet-v19z19`. Follows merged `v19z18` map frame.

玩測（沉浸式育成）：九龍電視台「同林曉晴傾談」可 hover／可點但無反應，剩次停喺「剩 3」；送禮永遠「未開放」。星河／九龍 sheet 底「報名：旁聽」「休息室」常 y>800 或被攔截。

## Root cause

| # | Issue | Cause |
|---|-------|-------|
| 1 | 傾談靜默死鍵 | `#app.mask-up`／`ui-inert`／`#loc-sheet[inert]` 殘留時，CSS `pointer-events:none` 令真實滑鼠點擊唔入 `onclick`（DOM `.click()` 仍可觸發，易誤判「handler 有綁」） |
| 2 | soft 日 cap 顯示永遠剩 3（day 0） | `softSocialDailyState` 用 `!S.flags.softSocialDay`；`dayIndex===0` 時 `softSocialDay=0` 係 falsy，每次 use 後立刻清零 |
| 3 | 報名／休息室難點 | 訓練／休息排喺通告列表之後；有 banner＋多張通告時 CTA 落 fold 下（~800px 高度） |

送禮「未開放」係傾談從未成功解鎖嘅後果（`gift_talked_*` 未寫入），唔係獨立 gate 靜默擋。

## Fixes

| # | Fix |
|---|-----|
| 1 | 新增 `ensureLocSheetInteractive()`：開 loc／撳 act 前清殘 `mask-up`／`ui-inert`／`inert`／inline pointer-events；事態進行中明示 toast |
| 2 | soft／試玩：若仍被事態鎖擋 → modal「暫時未能點」＋**「仍要試玩進行」**（force 清鎖再跑）／「先完成對白」——禁止靜默 no-op |
| 3 | `add()` 包 try/catch；`button type="button"`；`doTalk` 防空 NPC |
| 4 | `softSocialDailyState`：改 `softSocialDay !== day`（保留 day 0） |
| 5 | 非 hub：`報名`／`休息室` 提前到通告列表前，並標 `act-priority` |
| 6 | 矮屏收短 `.loc-bg`（860／720）；開 sheet 後 priority `scrollIntoView`；CSS：無真實 `#mask.on` 時唔畀殘 `mask-up`／`ui-inert` 食點擊 |
| 7 | Cache bust `?v=19z18` → `?v=19z19` |

**保留**：BehaviorGate／`featureFlag_softBehaviorGatePreview`／`gatePath` 解析器；傾談／送禮 soft 不耗日規則；通告／訓練耗日。唔 tip LIVE。唔做 P1 經濟／事態進度條／P2 地圖打磨。

## Soft≠PASS

- 唔改 soft flag 預設或 stub 解析
- 「仍要試玩進行」只喺 soft preview 路徑提供 force 解鎖 UI；live 只 toast 原因

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z19&softBehaviorGate=1`

1. 開九龍電視台（林曉晴在場）→「同林曉晴傾談」必出對白（或 toast／試玩解鎖 modal），剩次會減
2. 傾談成功後送禮唔再永遠「未開放」（庫存空則顯示「庫存空」）
3. 開地點 sheet：事態／傾談／報名／休息室喺首屏可見，唔使深滾（~800px 桌面高度）
4. 人為殘留 `mask-up`／`ui-inert` 再開地點 → 仍可點傾談
