> Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜SAVE `starVolunteer_map_v19w`｜`?v=19w` 唔抬｜`liveWeekGateStillActive()` 仍 true｜禁 soft-try

# Soft UI Phase3 — 紅星遠觀＋Casting CTA

Web Soft 把 main 上的 `content/MOCK_UI_PHASE3_STAR_CASTING_v1.json` 接到 `?v=19w&softBehaviorGate=1`（`BehaviorGate.gatePath()==="soft"`）。政策仍見 `PLAN_UI_PHASE3_COPY_HOOKS_v1.md`。無關旗時唔 fetch 呢份 Mock，遠觀同通告掣保持原本 LIVE 字串。

## 遠觀（Mock B · 文字＋音）

只四人，地點綁定沿用原本地圖，唔係 Mock 新釘：

| starId | 玩家名 | 地點 |
|---|---|---|
| `luk_baakyin` | 陸柏言 | 獅子山製片 `film_lion` |
| `liu_bingxing` | 廖炳星 | 金龍茶餐廳 `cafe_cha` |
| `ngai_wingnaam` | 魏詠男 | 維港電影 `film_harbour` |
| `yip_manji` | 葉敏芝 | 香江唱片 `rec_hk` |

地點表行動「遠觀：{displayName}」，副行係 distanceLine。打開後見 silhouetteDesc（當作文案）、distanceLine、rumor teaser、locHint。Toast 用該星 `resultToast`（「已遠觀…」）。音效沿用既有 `playSightChime`；播唔到就靜音 toast。無立繪、無剪影圖。齊鎮海只留 Mock `devAppendix`，唔上地圖。

## Casting Detail

board 只 `ready`｜`locked`。Detail **唔讀** `isSoftTryGig`，無「搏一搏」／試投第三掣。

- 條件合：主鈕「接通告」。成功 toast「劇組通知：接通告成功！」。次鈕「離開」。
- 條件未合：主鈕「暫未能報」（灰、`aria-disabled`，仍可撳）、shake、toast「條件未合」、副行用 Mock `subLine`、次鈕「離開」。

字串在 Soft 路徑來自 Mock `castingCta` 同 `boardCardStates`。`canAudition` 門檻唔改。gigs JSON 唔改。

## 載入

Soft on：先鋪與 Mock 同文的 inline，再 `fetch("content/MOCK_UI_PHASE3_STAR_CASTING_v1.json?v="+SAVE)`。成功則 `window.__phase3.source()` 為 `"fetch"`；失敗維持 `"inline"`。主控台 `__phase3.check()` 應 `{ ok:true }`，而且 `BehaviorGate.liveWeekGateStillActive()` 仍 `true`。

## 抽樣

1. 開 `?v=19w&softBehaviorGate=1`，新遊戲，跳過教學。
2. 主控台等 `await __phase3.load()`，確認 `source()==="fetch"`、`stars()` 剛好上面四個 id、`check().ok`。
3. 金龍茶餐廳 →「遠觀：廖炳星」→ 見距離句同噂，toast「已遠觀廖炳星。」，只有「離開」。
4. 其餘三地各遠觀一次，toast 對應該星。
5. 通告欄開一張條件未合：主鈕「暫未能報」灰、撳一下 shake、toast「條件未合」、有「離開」，無第三掣。
6. 條件合（或把能力調到過閘）主鈕「接通告」。
7. 唔加 `softBehaviorGate=1` 再開一次：`__phase3.source()` 為 `"live"`，`liveWeekGateStillActive()` 仍 true。

Soft≠PASS｜唔 tip LIVE｜唔抬 ?v=（19w）｜出圖 HOLD｜89–92 HOLD
