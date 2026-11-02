# PLAYER_OFFER_MEET_v1

**目的**：平行／可選 meet 唔自動推（`playerOffer:false`）；主線 C1–C5 仍 `true`。出圖／鄧節序／C5 裸旗 HOLD。

## 規則
- `*_meet`（平行 romance／rival-mentor／鄧 stub＋正式）→ `"playerOffer": false`
- 主線 `C1`–`C5`（`story_detail_c1_to_c17.json` 1.2）→ **唔改**（維持 `true`）
- push／crisis／ending：**唔加欄**（引擎預設）

## 清單（15）

| pack | version | ids |
|------|---------|-----|
| `story_detail_romance_vera_hiu_choi.json` | **1.3.1** | `R_vera_meet` `R_hiu_meet` `R_choi_meet` |
| `story_detail_romance_lan_xu.json` | **2.3.2** | `R_lan_meet` `R_xu_meet` `R_tang_meet_stub` |
| `story_detail_romance_tang.json` | **1.2.1** | `R_tang_meet` |
| `story_detail_rival_mentor.json` | **2.3.1** | `A_ko_meet` `A_hakfan_meet` `A_tsijun_meet` `A_fong_meet` `A_tong_meet` `A_ho_meet` `A_gao_meet` `A_lei_meet` |

## 自檢
- [x] 上表 15 meet 皆 `playerOffer === false`
- [x] `C1`–`C5` 仍 `playerOffer === true`；`c1_to_c17` version 仍 **1.2**
- [x] push／crisis／ending 無新增 `playerOffer`
- [x] 已 cp store `store-cbdfa415-74f6-4e12-8fbd-513ef31077be`

## paths
- web: `/workspace/star-volunteer-web/content/`
- store: `/cursor/stores/store-cbdfa415-74f6-4e12-8fbd-513ef31077be/`
