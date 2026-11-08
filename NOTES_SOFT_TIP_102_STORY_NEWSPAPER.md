# NOTES · Soft tip #102 — 劇情選擇入次日朝早報紙

> **狀態：** Soft≠PASS｜**唔 tip LIVE**｜SAVE `starVolunteer_map_v19w`｜產品 `?v=20a10` 唔抬  
> **softRev：** `s102`  
> **預覽：** `https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s102`  
> `<html data-soft-rev="s102">` 先算載到今次 index。89–92 HOLD。出圖 HOLD。  
> 基線：Soft tip #101 main `28903874`／softRev=`s101`。種子抽樣 **PASS with nits**（nits 唔擋）。

## 本票做咗咩
- 劇情種子（原樣）：`content/STUB_NEWSPAPER_STORY_SOFT_v1.json` sha8 `4dabcb42`。`story_highlight` 8＋`story_mixed` 6＝14。`R_hiu` distant 無模板（`stub.skip`）。
- 同包：`SCHEMA_NEWSPAPER_STORY_SOFT_v1.json` sha8 `c7d266d4`；`NOTES_NEWSPAPER_STORY_SEED_v1.md` sha8 `ce539281`；`NEWSPAPER_STORY_SOFT_SEED_DELIVERABLE.md` sha8 `e62e3644`。
- 本 repo 無 `star-volunteer-web/`，唔另鏡像。
- `loadFreeplayFramework` 同時載入 story stub／schema（內容 bust 仍 `20a7`，唔抬產品 `?v=`）。
- `enqueueNewspaperFromStory(node, choice, opts)`：按 choice flag／eventKey 對模板，`source:"story"`，`publishDay=day+1`，重用 `enqueueNewspaperItem`。次日朝早 modal、聲望 `fameDelta`、剪報、`rumorEcho`→`pushNewspaperRumor`（source「報紙」）沿 #101。
- 只掛一次：`StoryOC.applyChoice` 成功 `markDone` 之後。DualMeet 走同一條，唔再喺 `pickChoice` 加第二掛。種子未載完先暫存，載入後補入佇列，避免雙入。
- 拍板：周刊誠實紙 `fameDelta` **+2**；C5 `choi_dodge` **出淡紙** `fameDelta` **0**（唔 skip）；C3 `rival_gao_hard` **−1**。
- 人情／好感閘：C5 誠實稿要 `rel_choi≥1` 或已有 `flag_choi_meet_honest`，否則降 mixed、聲望 +1。C4 拒單若模板係正面而何生 favor&lt;1，降 mixed、唔出洗白。**報紙唔加 favor、唔加 rel。**
- `boardScentTag` 只存喺佇列項。通告板氣味演算法 **P1 HOLD**。
- `__newspaper.fromStory`。`__newspaper.check()` 加劇情入佇列單元（誠實次日、迴避淡紙、硬碰 −1、distant 跳過、低好感降級、周刊 +2）。
- 玩家面「聲望」／「幕前聲望」。禁「聲量」「噂」（傳聞）。

## 本票唔做
- 唔 tip LIVE；唔抬 SAVE；唔抬產品 `?v=20a10`。
- 唔出圖；89–92 HOLD。
- 唔做 C6–C17／鄧線報紙；唔做重負面醜聞弧。
- 唔做通告板氣味演算法。
- 自然試玩唔用 softSeed。

## Console
- `__newspaper.check()`（框架載入後先見到 story stub 單元）
- `__newspaper.fromStory(node, choice)`

## QA
新分頁開上面條 URL。揀 C1–C5 或廠景交換／周刊小訪之後，**當日唔彈整張報**；過日或返地圖先見。迴避仍出淡紙，聲望唔因此再改。客氣疏離唔出紙。HUD 仍係「聲望」。
