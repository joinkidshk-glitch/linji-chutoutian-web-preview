# V18F_C1_NITS_127

**SAVE：** `starVolunteer_map_v18f`  
**時間：** 2026-11-03 11:10 HKT（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；唔 publish；出圖暫緩  
**契約：** 用戶批「跟兩條再推」（widget t157s681）→ JSON **1.2.7**（SHA16 `ed1f006c2267cfe8`）；meet／送禮 unlock **未改**；gift shop v18d 保留；Soft／出圖／鄧 HOLD

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | C1 setting | 删玩家可見「locId 暫掛 tvb_longmen」；`locId` 欄仍 `tvb_longmen` |
| 2 | B01／fallback 標題 | 「先練／先賺」→「先學做動作戲／先賺」（STORY_TITLES／hints／週結） |
| 3 | Version | `story_detail_c1_to_c17.json` **1.2.6 → 1.2.7**；edits `C1_NITS_127_v1` |
| 4 | SAVE | `starVolunteer_map_v18e` → `starVolunteer_map_v18f` |
| 5 | 未改 | meet `playerOffer`；gift unlock；商店／送禮引擎；Soft／出圖／鄧 |

**Handoff：** `content/HANDOFF_C1_NITS_127_v1.md`

## Tester 覆測（清 SAVE）

1. 清 `starVolunteer_map_*` → `?v=18f`（硬 refresh／無痕）
2. C1 每拍 setting 只見「星河電視台附近茶餐廳；片場後巷感」（無 locId／暫掛）
3. 手帳／B01／事態標題／fallback：**「先學做動作戲／先賺」**，唔見「先練／先賺」
4. version＝**1.2.7**，SHA16＝`ed1f006c2267cfe8`
5. 11 beats／C1_a／C1_b／開局鎖／契約回歸仍 PASS
6. Soft≠PASS；出圖 HOLD

## curl-verify（公開 Pages）

- SAVE=`starVolunteer_map_v18f`
- JSON version=`1.2.7` SHA16=`ed1f006c2267cfe8`
- C1.setting 無「暫掛／locId」
- 舊 title「先練／先賺」= 唔見（註解除外）

## Ship

- feature commit：`5b73bb4` (`5b73bb410680bbc7e193d93f8acb477a89cefe2c`)
- NOTES commit：（填）
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18f
- tar：`/workspace/star-volunteer-web-v18f.tar.gz`
- Soft≠PASS · 出圖 HOLD
