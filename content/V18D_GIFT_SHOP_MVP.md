# V18D_GIFT_SHOP_MVP

**SAVE：** `starVolunteer_map_v18d`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；唔 publish；出圖暫緩  
**契約：** 用戶「你先做好系統。詳細對白，劇本要等 @臨記出頭天劇本manager」→ 引擎／UI 先落地；反應已接 `GIFT_REACT_COPY_v1`（55＋9）；唔改 LIVE story JSON

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | JSON | `items_gifts.json`（10 common/uncommon）· `shops.json`（`shop_street_mk`＠`rec_hk`）· `gift_prefs.json`（vera/hiu/choi/lan/xu/tang）· `gift_react_copy.json`（由 MD parse） |
| 2 | Save | `S.inventory` · `S.giftMeta`（lastGiveDay／weekGiftGain／givenCount／shopStock／shopWeek） |
| 3 | API | `GiftShop.buyItem`／`canGive`／`giveGift`／`inventoryList`／`shopList`；`bumpRel` 只改好感；無 flagsOnGive |
| 4 | Cap | 日硬 1／週淨軟 +2（超出「心領」）／單次硬 +2／厭 −1／送禮耗 1 日／買唔耗日 |
| 5 | UI | `rec_hk` sheet「小賣／禮品」；romance 針「送禮」；選單「庫存」只讀 |
| 6 | 對白 | lookup `npcKey:itemId:pref`；crisis 輕量覆寫；缺條 → 同角 neutral → 短佔位 |
| 7 | 鄧 | 須 `flag_tang_open`；鎖定句跟 §8 |

## 檔案

- `content/items_gifts.json`
- `content/shops.json`
- `content/gift_prefs.json`
- `content/gift_react_copy.json`（源：`GIFT_REACT_COPY_v1.md`）
- `content/V18D_GIFT_SHOP_MVP.md`
- `index.html`（SAVE v18d + GiftShop）

## Out of scope（本版）

- 出圖／icon 美術（emoji OK）
- 新地圖 pin／多店
- Soft PASS／publish
- LIVE story JSON 改動
- 對手／前輩可送

## Tester 覆測（清 SAVE）

1. 清 `localStorage` `starVolunteer_map_*` 後開 `?v=18d`
2. 去旺角「香江唱片」→「小賣／禮品」→ 買菠蘿油／雜誌等（扣錢、庫存＋1；唔耗日）
3. 選單「庫存」只讀見到貨
4. Debug／劇情令 Vera／曉晴／采兒已 meet（或設 flag）→ 地圖遇人 →「送禮」→ 確認耗 1 日 → 播長稿對白（非純佔位）
5. 同日再送同人 → 擋「今天先到這裡」
6. 一週禮物淨好感超 +2 →「心領了…數字就先不動」
7. Vera 收菠蘿油 → dislike 長稿；曉晴收菠蘿油 → liked 長稿
8. 主線 week_min／同日 C* 閘唔因送禮繞過
9. 靜態：SAVE v18d；`GiftShop`／`gift_react_copy.json`／`shop_street_mk` 存在

## Ship

- commit：`294f413` (`294f4131a8646143f7967dcf1e86f34cf6d64967`)
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18d
- tar：`/workspace/star-volunteer-web-v18d.tar.gz`
- Soft≠PASS · 出圖 HOLD
