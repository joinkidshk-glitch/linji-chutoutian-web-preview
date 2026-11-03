# NOTES_V18R_GIGS_LOCID_1_1_1

**SAVE：** `starVolunteer_map_v18r`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；全量出圖未開；唔 publish

## 用戶拍板

「推 1989–92 1.1.1 上 ?v=18r」（via tester handoff）

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | **gigs_1989–92 → 1.1.1** | synopsis 清 raw locId→顯示名（`film_harbour`→維港電影 等）；`loc` 欄保持 machine id |
| 2 | SAVE | `…_v18q` → `starVolunteer_map_v18r`（bust content/*） |
| 3 | 保留 | v18p 到處逛逛免區鎖／對比／Skip；gigs_1988 仍 2.3.0 |

### Per-year（source SHA16）

| year | version | sha16 | n |
|------|---------|-------|---|
| 1989 | 1.1.1 | `6a2da912643f9af7` | 52 |
| 1990 | 1.1.1 | `0676d4a0658025ac` | 53 |
| 1991 | 1.1.1 | `89dd5602a72f9520` | 52 |
| 1992 | 1.1.1 | `3109a3e6f864ac2f` | 51 |

## Tester 覆測

1. `?v=18r`；SAVE=`starVolunteer_map_v18r`
2. Network：`gigs_1989.json?v=starVolunteer_map_v18r`（90／91／92 同）→ version **1.1.1**
3. 卡文／synopsis：見「維港電影」等；**唔見** raw `film_harbour`
4. Soft≠PASS

## Ship

- feature commit：`a5c3bb962a94` (`a5c3bb962a9414d09f6db2ecb0b23c51bdd2d21c`)
- tip／NOTES：`91dc740c1f97` (`91dc740c1f97231b891891638e3d4357b0c3ca0f`)
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18r
- Soft≠PASS · 全量出圖 HOLD
