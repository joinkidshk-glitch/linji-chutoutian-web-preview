# CASTING DETAIL WIRE｜通告招募單（phone sheet-first）

> 對齊：`content/ART_BRIEF_CASTING_NOTICE_DETAIL_v1.md`、`content/PLAN_GIG_CASTING_NOTICE_DETAIL_v1.md`  
> 參考：`/workspace/ref-mv-casting-notice.png`  
> **出圖 HOLD** — 本檔只係線框；Soft≠PASS

## Phone portrait (~390×844；modal 內 scroll)

```
                 safe top 54
┌──────────────────────────────────────┐
│ modal inset ~12                      │
│ ┌─ notice_sheet_frame (9-slice) ───┐ │
│ │                                  │ │
│ │ (opt) poster_wall / 立繪 可收合   │ │
│ │ ┌──────────────────────────────┐ │ │
│ │ │▓▓ notice_header_orange ▓▓▓▓▓│ │ │
│ │ │ 作品名              導演：…  │ │ │
│ │ └──────────────────────────────┘ │ │
│ │ [tag_type] [tag_recruiting 紅]   │ │
│ │ ┌─ notice_period_bar ──────────┐ │ │
│ │ │ 通告期間：…，共 N 週          │ │ │
│ │ └──────────────────────────────┘ │ │
│ │ [tab_on 角色] [tab_off…]         │ │
│ │ ┌─ table_frame ────────────────┐ │ │
│ │ │ 條件          │ ★★★★☆ 難易度 │ │ │
│ │ │ 演技：合／未合 │ 每週 N 天    │ │ │
│ │ │ 魅力：…       │ 總天 M 天    │ │ │
│ │ │ …             │ 片酬 $a–$b   │ │ │
│ │ │               │ 簽約 —       │ │ │
│ │ │               │ 特殊 —       │ │ │
│ │ └──────────────────────────────┘ │ │
│ │ ┌─ synopsis_frame ─────────────┐ │ │
│ │ │ 劇情簡介                      │ │ │
│ │ │ synopsis…                     │ │ │
│ │ │ （可選）角色：roleHint        │ │ │
│ │ └──────────────────────────────┘ │ │
│ │                                  │ │
│ └──────────────────────────────────┘ │
│ ┌ sticky btns ─────────────────────┐ │
│ │     [btn_leave]  [約試鏡／報名]  │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
                 safe bottom 34
```

## Wide / PC optional（跟 MV 參考）

```
┌──────────┬─────────────────────────────┐
│ poster   │ header_orange + director    │
│ wall +   │ tags + period_bar           │
│ 立繪     │ tabs                        │
│          │ conditions | stars/days/pay │
│          │ synopsis_frame              │
│          │              [離開][報名]   │
└──────────┴─────────────────────────────┘
```

## Slice callouts（開閘後產）

1. `notice_sheet_frame` — 外框 9-slice  
2. `notice_header_orange` — 橙頭  
3. `notice_tag_type` / `notice_tag_recruiting` — pills  
4. `notice_period_bar` — 期間條  
5. `notice_tab_on` / `notice_tab_off`  
6. `notice_table_frame` / `notice_table_cell`  
7. `notice_star_on` / `notice_star_off`  
8. `notice_synopsis_frame`  
9. `notice_poster_wall`（左／頂 optional）  
10. `btn_leave`；reuse `seal_*`

文字一律 App live 或 Noto 燒錄；禁 AI CJK。
