# NOTES · Soft tip #104 — 臨記段殺青見報出淡紙

> **狀態：** Soft≠PASS｜**唔 tip LIVE**｜SAVE `starVolunteer_map_v19w`｜產品 `?v=20a10` 唔抬  
> **softRev：** `s104`  
> **預覽：** `https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s104`  
> `<html data-soft-rev="s104">` 先算載到今次 index。89–92 HOLD。出圖 HOLD。  
> 基線：Soft tip #103 main `f0512b28`／softRev=`s103`。

## 玩家面

- 幕前聲望 **＜ 15**（臨記段）：殺青仍入佇列。短卡當日唔彈整張報。再下一個曆日朝早出**淡紙**——有剪報，`fameDelta = 0`，收下之後聲望唔加。版面寫「這則未再改聲望。」
- 淡紙頭條／內文沿 #103：本 gig 片名＋玩家角色（臨記／路人／班底，例如《天星碼頭》／過海路人、跟組特約）。唔寫跟男主角、男一、男星。
- 報紙名、欄目仍來自 `wrap_success` 桶。
- 幕前聲望 **≥ 15**：維持 #103 正紙，`fameDelta` +1～+3。玩家自己的角色名（包括飾演男主角）照寫。淡紙先至禁「跟男主角」敘事。
- 劇情報（#102）同「聲望」正名（#101）唔改。短卡同次日朝早嘅分層唔拆。

## 閘點

C3 劇情閘係 `fame > 15`（`fameMin` 16，15 分不過）。呢個閘唔搬來做淡紙：用戶鎖聲望 ≥15 仍出正紙。淡紙只限 `S.fame < 15`，喺 `enqueueNewspaperFromWrap` 組好 subject／face 之後先分支。

## 本票做咗咩

- 低聲望：`fameDelta` 強制 0，再用 `newspaperWrapFadeLines` 走 #103 FaceLines。角色字串如果係男主角／男一／男星敘事，改回路人、班底、臨記或「臨記入鏡」。`跟組特約` 係本角，保留。
- 高聲望：face 同 `fameDelta` 維持 #103。
- `__newspaper.check()`：fame 14／0 淡紙、毒角色無男主角敘事、跟組特約仍在、收下唔加聲望、fame 15／16 正紙 +1～+3。天星碼頭回歸加 `ferry_fade`。

## 本票唔做

- 唔 tip LIVE；唔抬 SAVE；唔抬產品 `?v=20a10`。
- 唔出圖；89–92 HOLD。
- 唔改劇情報規則、唔改通告板氣味、唔加 C2+。

## Console

- `__newspaper.check()`（框架載入後）應 `{ ok:true, softRev:"s104", version:"v20a10", softStatus:"≠PASS" }`

## QA

新分頁開上面條 URL。聲望未到 15 就殺青：當日只有短卡；再過一日朝早有紙；收下後聲望唔加；文案寫本角，唔寫男主角。聲望已到 15 的殺青仍係 +1～+3。
