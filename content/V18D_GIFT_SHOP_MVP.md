# V18D_GIFT_SHOP_MVP

**SAVE：** `starVolunteer_map_v18d`  
**時間：** 2026-11-03 08:46 HKT（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；唔 publish；出圖暫緩  
**契約：** 用戶「你先做好系統…劇本要等」→ 引擎／UI 先落地；反應接 `GIFT_REACT_COPY_v1`（55＋9）；唔改 LIVE story JSON

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | JSON | `items_gifts.json`（10）· `shops.json`（`shop_street_mk`＠`rec_hk`）· `gift_prefs.json` · `gift_react_copy.json`（MD→JSON） |
| 2 | Save | `S.inventory` · `S.giftMeta` |
| 3 | API | `buyItem`／`canGive`／`giveGift`；`bumpRel` only；無 flagsOnGive |
| 4 | Cap | 日硬1／週淨軟+2／單次硬+2／厭−1／送禮耗1日／買唔耗日 |
| 5 | UI | `rec_hk`「小賣／禮品」；romance「送禮」；選單「庫存」 |
| 6 | 對白 | lookup `npcKey:itemId:pref`；crisis 輕量；缺→neutral→短佔位 |
| 7 | 鄧 | 須 `flag_tang_open` |

## API 摘要

- `GiftShop.buyItem(shopId,itemId)` → money／stock／inventory（唔耗日）
- `GiftShop.canGive(npcKey)` → meet／日 cap／庫存
- `GiftShop.giveGift(npcKey,itemId)` → 扣庫存、`bumpRel`、meta、回傳長稿 HTML、呼叫端 `tickDay`
- `GiftShop.inventoryList`／`shopList`／`reactionEntry`

## Tester 覆測（清 SAVE）

1. 清 `starVolunteer_map_*` → `?v=18d`
2. 香江唱片 → 小賣／禮品 → 買（扣錢＋庫存；唔耗日）
3. 選單庫存只讀
4. meet Vera／曉晴／采兒 → 送禮 → 耗日＋長稿（非純佔位）
5. 同日再送擋；週超+2 心領句
6. Vera×菠蘿油 dislike；曉晴×菠蘿油 liked
7. 唔繞 week_min／同日 C*
8. 靜態：SAVE v18d；GiftShop；gift_react_copy 55 keys

## Ship

- feature commit：`294f413` (`294f4131a8646143f7967dcf1e86f34cf6d64967`)
- NOTES commit：`d595a56` (`d595a56fab58afa26681536a50e87f7ba8cc195c`)
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18d
- tar：`/workspace/star-volunteer-web-v18d.tar.gz`
- Soft≠PASS · 出圖 HOLD
