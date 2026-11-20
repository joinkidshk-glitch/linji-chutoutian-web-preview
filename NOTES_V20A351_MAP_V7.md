# NOTES V20A351 — 大地圖換 v7 生成圖＋pin 重新對位

日期：2026-11-20
用戶拍板：用 gpt-image-2 生成圖 2（`linji-map-gen-pilot/gen_map2.png`）做新底圖。

## 換圖
- 新資產：`assets/hk_map_v7.jpg`（1024×1536，JPEG q88，579,000 級 bytes；由 gen_map2.png 轉檔，圖入面冇字，地點名照舊 app 排字疊加）。
- `MAP_IMG` 改指 v7；`MAP137_NATURAL` 改 1024×1536。
- 顯示：舞台 aspect 1270/1824＋object-fit:cover＋object-position 60% 50% 唔郁——新圖比例 0.667 對舞台 0.696，cover 只上下各裁約 2% 羊皮紙邊，唔變形；pin／標籤經 `map137CoverTransform` 即場換算，圖 % 座標照舊係 source of truth。
- 舊圖 `assets/hk_map_v6.jpg` 已刪（引用清零後 `git rm`；index 內剩 2 處歷史註解提及 v6，屬版本紀錄唔郁）。fallback `assets/hk_map.jpg` 保留。

## Pin 對位（圖 % 座標，視覺定位核實地標）
片場層 17：
- film_lion 獅子山製片 (86,20) 東北攝影棚廠房
- rec_hk 香江唱片 (34,21) 旺角高樓群
- tvb_longmen 星河電視台 (48,21) 九龍塘高樓群
- tvb_kowloon 九龍電視台 (55,38) 紅磡海旁
- tvb_harbour 海港廣播 (93,27) 東端清水灣舊樓群
- film_cotton 紅棉影業 (43,40) 尖沙咀鐘樓旁商廈
- film_harbour 維港電影 (13,67) 港島西環
- ad_central 中環廣告 (44,63) 中銀大廈
- ad_adm 金鐘創意 (52,61) 中銀／合和之間
- rec_wanchai 灣仔唱片 (60,61) 合和圓塔
- rec_star 天星音樂 (89,59) 黑膠唱片天台大樓
- cafe_cha 金龍茶餐廳 (22,34) 油麻地
- agency_ho 何生事務所 (36,63) 中環西
- gift_shop 廟街禮品 (16,40) 西九龍排檔
- hospital 仁康醫院 (76,61) 紅十字醫院大樓
- clothing_shop 花園街成衣店 (29,29) 旺角
- home 阿偉屋企 (14,24) 深水埗

約會層 6（同底圖，一齊對位）：
- date_harbour 尖沙咀海傍 (42,46) 鐘樓海傍
- date_peak 山頂 (28,65) 纜車山頂站
- date_lounge 酒廊唱歌 (49,66) 中環山坡
- date_cinema 旺角戲院 (17,26) 旺角西
- date_beach 淺水灣 (64,81) 港島南岸
- date_airport 啟德機場 (84,38) 跑道飛機

會場標籤金禧大酒店 → left:33%;top:37%。
同層最近距離全部 ≥7.5%（唔觸發 fan-out）；西九龍密集區（home／cinema／clothing／cafe／gift／rec_hk）已拉開。

## 測試同步
改咗 11 個測試嘅釘值（資產名／尺寸／LOCS 座標／標籤錨）：test_map97、test_ui137_map、test_ux68、test_map159、test_loc96、test_costume265、test_ui142、test_awards207、test_v155、test_ui108、test_ui128a1。
index.html 全部同行替換，行數不變（47,368），kwan151／tang152 釘行零漂移（兩測 ALL PASS）。

## Suite
398 PASS／9 FAIL，同 v350 基線一致（九項 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。`qa296/derive296.json` 已還原。

## 實駕
Playwright（390×844 dsf2，本地 http.server）：底圖載入 v7（natural 1024×1536）；片場層 17 pin、約會層 8 pin（6 新＋茶餐廳＋廟街）齊；撳 film_harbour／hospital／film_lion／date_airport 地點面板開得啱。截圖 `~/workspace/linji-drive351/shots/`（map_set.png／map_date.png／sheet_*.png）。
