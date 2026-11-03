# V18E_C1_FUSION_126

**SAVE：** `starVolunteer_map_v18e`  
**時間：** 2026-11-03 09:38 HKT（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；唔 publish；出圖暫緩  
**契約：** 用戶批合 LIVE C1 fusion → JSON **1.2.6**（SHA16 `ec26240c44c21a04`）；meet／送禮 unlock **未改**；gift shop v18d 保留

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | LIVE C1 | `story_detail_c1_to_c17.json` **1.2.5 → 1.2.6**：beats **7 → 11** |
| 2 | 文案 | 「學做動作戲」＋茶餐廳／何生人情／張電話；hints／notes 換入 |
| 3 | 硬契約 | choice `C1_a`／`C1_b`；flags／stats／pacing／locId／playerOffer **不變** |
| 4 | SAVE | `starVolunteer_map_v18d` → `starVolunteer_map_v18e` |
| 5 | 未改 | meet `playerOffer`；gift unlock；商店／送禮引擎；Soft／出圖／鄧 |
| 6 | phase 鏡像 | 預覽 index **唔載** phase1 薄檔；本刀唔推（web 本地已 3.1／1.1） |

**Handoff：** `content/HANDOFF_C1_FUSION_LIVE_v1.md`

## Tester 覆測（清 SAVE）

1. 清 `starVolunteer_map_*` → `?v=18e`（硬 refresh／無痕）
2. 開局播 C1：確認 **11 beats** 可播完、無崩
3. 場面感：茶餐廳／手頭緊／何生人情／張子駿電話／「學做動作戲」；title「先學做動作戲／先賺」（唔再「先練／先賺」）
4. `C1_a` → `route_tv`＋craft+1；`C1_b` → `route_film`＋wealth+1
5. 返地圖：`locId` 仍 `tvb_longmen`；開局無 Vera／采兒／鄧牆
6. meet／送禮解鎖行為與 v18d 一致（meet 仍 `playerOffer:false`）
7. Soft≠PASS；出圖 HOLD

## curl-verify（公開 Pages）

- SAVE=`starVolunteer_map_v18e`
- JSON version=`1.2.6` SHA16=`ec26240c44c21a04`
- C1 beats=11；title=`先學做動作戲／先賺`
- fusion：動作戲／茶餐廳／何生／張子駿 = PASS
- 舊 title「先練／先賺」= 唔見

## Ship

- feature commit：`d6ed19d` (`d6ed19db2069f2e43bab1e663c2d1770a9696568`)
- NOTES commit：`b598376` (`b598376ccc32fe83dd19d9bd56a5238802c35d68`)
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18e
- tar：`/workspace/star-volunteer-web-v18e.tar.gz`
- Soft≠PASS · 出圖 HOLD
