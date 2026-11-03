# NOTES v18s — gig card gate + 天星 brand + legend/syn nits

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v18s`  
**Soft≠PASS · 出圖 HOLD**  
**URL：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18s

## Content

| 檔 | version | SHA16 | n |
|---|---|---|---|
| `content/gigs_1988.json` | **2.3.1** | `d90b8a111b69d5b5` | 52 |

Brand：`gig_1988_rec_star_spring`／summer — 「星途」→**天星**（見 `HANDOFF_GIGS_1988_TIANXING_BRAND_v1.md`）。靜態 PASS 後本船推 LIVE。

## index.html

1. **gateShortReason**：不再只因 fame 先 return「聲望未夠」。列齊未達：`聲望差N` + 各能力 `差N`，`、` 接合，最多 4 項；全達則「條件未夠」。
2. **seasonTipHtml**：當季（`s===cur`）改回空字串（卡已上板；唔再綠框「較易出現在通告板」）。全年 tip 保留；非當季仍空。
3. **syn-toggle CSS**：`display:block; margin:4px 0 8px; padding:8px 10px; min-height:36px`（paper＋主 theme），減少貼 synopsis 擠迫。
4. **地圖圖例「劇／事態」**：cream 紙底上由淺字 `#f5e6c0` 改 **ink `#1a1208`**（同 v18p footer 對比方向）。

## Tester checklist

- [ ] `?v=18s` 硬 reload；SAVE `starVolunteer_map_v18s`
- [ ] 通告卡 `gig_1988_rec_star_spring`：標題／blurb／synopsis 見「天星」／《天星序曲》，**無「星途」**；地點「天星音樂」
- [ ] 鎖卡：聲望＋多項能力同時未達時，鎖因列齊（唔止「聲望未夠」）
- [ ] 當季上板卡：**無**綠框「較易出現在通告板」
- [ ] 「展開」鈕唔貼 synopsis；可點
- [ ] 地圖圖例「劇事態」字色深、可讀（cream 底）

## Ship

- feature commit：`8785aecdd707` (`8785aecdd7079c4f639c410e17d1dbdaa5d90049`)
- tip／NOTES：`702e8604193f` (`702e8604193fa82489666a2b50afe3f08e100d57`)
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18s

Soft≠PASS。
