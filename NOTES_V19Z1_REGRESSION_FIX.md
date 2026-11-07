# Regression fixes (v19z1 → branch `fix/playtest-regression-v19z1`)

Official Pages playtest after v19z closeout still saw four UI failures. This patch closes them and tightens soft repay preview.

## Fixed

| # | Bug | Fix |
|---|-----|-----|
| 1 | Locked gig Detail：有缺口文案但只有「暫未能報／離開」 | `openCastingNoticeDetail` 喺未殺青鎖定時**一定**加可見主 CTA「去訓練／手帳」（可附練邊項）；`btn_train_jump` casting sheet **全寬／order 置頂**；fallback 入手帳。 |
| 2 | 已完成主線地點仍標「播事態」 | 已完成 **隱藏**行動（唔再出「播事態／事態已完成」鈕）；`who` 行唔再標已完成事態；結算後 `pruneMapTips`。 |
| 3 | 推門「叮」殘留 | `playPushDoor`：~0.56s 藏鈴清字、~0.82s 移除 DOM；CSS `.push-door.done`／非 `.on` 強制 hidden。 |
| 4 | `story-play-on`／mask 殘留 →「知道了／返屋企」似消失 | `closeModal` 一律 `remove("story-play-on")`＋清 `mask-up`；`showResult` 開結算前清 class，按鈕／dismiss 再清並 `paintBar`／`drawMap`。 |
| 5 | soft「預覽記還」假清債 | `mode:"soft"` **只 toast 說明、唔 splice**；選項改「預覽說明（唔清債）」；債單保持欠住。 |

## Cache

資產／UI／selfCheck 字串 `?v=19z` → `?v=19z1`。

## Verify

正式站（merge 後硬重整）：

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z1&softBehaviorGate=1`

1. 開鎖定通告 → 見到藍色「去訓練／手帳」→ 跳去訓練地／手帳。  
2. 完成 C1 後返同一地點 → **無**「播事態」鈕。  
3. 入何生事務所 → 「叮」一瞬即消失，唔留字。  
4. 播完事態撳「回地圖」→ 地圖／返屋企正常，唔使硬重整。  
5. soft 無禮物無錢「預覽說明」→ toast 說明後債仍在。

## Out of scope

- 正式 live 還人情仍要禮物或 $200。  
- 只用官方 GitHub Pages（`main`）；無第三方預覽依賴。
