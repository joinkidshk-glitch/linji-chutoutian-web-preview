> Soft≠PASS｜Pack B 寫庫｜1988 only｜version **3.2.4-soft**｜SHA `0f18fe14`｜對照 pre `3.2.3-soft` backup｜經 qwen3.7-max｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜0 新槽 n=137

# CHANGELOG_GIGS_1988_3_2_4_SOFT

## 摘要
按統籌 Soft A/B 拍板（**0 新槽**／**castWindow HOLD**／**OOV remap 至 ALIGN §3 現詞庫**）寫入 Soft `gigs_1988.json` → **3.2.4-soft**。

| 項 | 前（3.2.3-soft） | 後（3.2.4-soft） |
|---|---|---|
| n | 137 | **137**（0 新槽） |
| `genreLabel` OOV | 95 | **0** |
| 中階 `limits` | 0／45 | **20／45** |
| 中階 `producer` | 11／45 | **27／45**（≥30%） |
| `isKeyGig` true | 66 | **66**（未改旗標） |
| `counts.keyGigs` | 76 | **66**（meta 對齊） |
| `softStatus` | ≠PASS | **≠PASS** |
| `castWindow` | — | **HOLD**（未加／未改） |

## 改動範圍
1. **OOV remap**：95 則 `genreLabel` → ALIGN §3 原文詞庫（按 type／synopsis／roleScale；qwen3.7-max 產 mapping 後 script apply）。`gig_1988_photo_01` 手動覆寫為 `個人寫真`（photobook）。
2. **中階 limits**：補 **20** 則（結構跟 ALIGN §5；`notes` 香港書面語；禁工程詞）。
3. **中階 producer**：新補 **16** 則虛構港式人名（唔用真藝人；唔覆蓋已有；唔與同則 director 撞名）。
4. **meta**：`counts.keyGigs` **76→66**；version／notes／changelogHint／edits 更新。

## 明確未改
- 唔加新 gig；唔做 1989–1992；唔 tip LIVE；唔 publish；出圖 HOLD
- 未改：`favorDelta`／`rumorKeys`／`isKeyGig`／`pay*`／`breachFee`／`req`／`loc`／`season`／`storyKeys`／`boardHookMode`／`tagOnComplete`／`workTitle`／`synopsis`（驗收：forbidden diff = 0）
- `castWindow` HOLD；玩家面禁「Ho 哥」（掃描 count=0）；favor target 仍 `agency_ho`

## 產物路徑
| 檔 | 路徑 | SHA8 |
|---|---|---|
| Soft JSON | `/workspace/star-volunteer-web/content/gigs_1988.json` | `0f18fe14` |
| 工作副本 | `/workspace/tmp/qwen_pack_b_apply_324/gigs_1988_3.2.4-soft.json` | `0f18fe14` |
| pre backup | `.../gigs_1988_v3.2.3_soft_pre_packb_backup.json`（content＋workdir＋store） | — |
| patch | `/workspace/tmp/qwen_pack_b_apply_324/patch_pack_b_324.json` | `b2341fd2` |
| stats | `/workspace/tmp/qwen_pack_b_apply_324/stats.json` | — |
| store mirror | `/cursor/stores/store-cbdfa415-74f6-4e12-8fbd-513ef31077be/gigs_1988.json` | `0f18fe14` |

## 時間
2026-11-04 20:50（Asia/Hong_Kong）

## Soft≠PASS
本檔同 JSON 均 **Soft≠PASS**；交統籌／tester 抽樣後先可談 tip。

### Soft nit 修（同日）
OOV 前值：**96→95**（對齊 backup／PLAN）。gigs JSON SHA 不變 `0f18fe14`。
