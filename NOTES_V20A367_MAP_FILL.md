# v367 地圖填滿舞台＋同紙底融合

用戶 2026-11-21 實玩指出：大地圖同周圍白色／米色底唔匹配，地圖 size 同舞台比例唔夾。

## 成因
- 舞台 aspect 1270/1824 係舊圖（v137）窗闊；v10 圖係 1024×1536（2:3），cover 裁切。
- `.map-well`／`.map-polaroid` flex:1 撐高，舞台下方留一截米色空白帶。
- 圖邊（綠山／藍海）同手帳紙底硬切，睇落唔融合。

## 修法（原地改 v137 舞台四行，零行數變化，LOCS 圖 % 座標唔郁）
1. 舞台 aspect 改跟 v10 圖本身 `1024/1536`，`object-position:50% 50%`——cover 變 identity，唔裁唔拉伸，圖填滿舞台。
2. `.map-polaroid`／`.map-well` 改 `flex:0 0 auto`（well `height:auto`）收返去舞台高度，唔再留空白帶。
3. 舞台加紙邊框（米紙外框 6px＋啡線＋落影）同內緣柔光（`::after` z:1，喺圖上、針／標籤下），圖邊同紙底之間有印刷邊界過渡。

## 驗證
- 實駕（`~/workspace/linji-drive367/`）：舞台＝well＝圖 384×576（比例 0.6667＝圖本身），空白帶上／下均 0；片場層 17 pin＋17 標籤零重疊、約會層 8 pin＋8 標籤零重疊、撳山頂／廟街禮品 pin 入到地點、像素人「我喺呢度」在位、零 page error。
- Suite：TOTAL PASS 400 FAIL 9，九項同基線完全一致（flash51／slot50／soft_tip_111_restore／start53／weave43／44／49／wf5_87／wrap38）。
- 測試 resync：`tests/test_ui137_map_static.py` 三項（aspect／object-position／polaroid flex）按新定案更新，內容逐項核實；其餘釘行零漂移（總行數 47865 不變）。

## 回滾
還原 v137 舞台四行（aspect 1270/1824、object-position 60% 50%、polaroid/well flex:1）即返 v366 幾何。
