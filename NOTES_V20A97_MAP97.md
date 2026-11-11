# v20a97 MAP97 — 地圖接入包（換 v6 定版圖＋地區名細字層）

基底 v20a96（378b818）。用戶 2026-11-11 16:31 對 v6 全圖重畫版拍板：「這個ok阿，雖然很多地方都怪怪的。但可以當作是架空世界」——圖稿定版，今包純接入，冇改圖入面任何像素、冇掂玩法／數值／劇情。審計依據：`~/workspace/linji-map-v6/AUDIT_v6.md`（逐格審計＋15 地點漂移清單：全部 ≤1.3%，釘位可沿用）。

## 一、換圖

- 新資產：**`assets/hk_map_v6.jpg`**——來源 `~/workspace/linji-map-v6/world-map-v6-candidate.png`（1376×1824，PNG sha256 `6bbd8b0a…`），轉 JPEG q88／4:2:2／optimize，**793,164 bytes**，sha256 `331df308c7bbfabc33e1742740b19f59a910d4442171327263d4d21f03b8b38f`，尺寸同 v3 一樣 1376×1824、同座標系。
- `MAP_IMG` 由內嵌 base64 data URI（v3 圖，509,318 字元嗰行）改指檔案路徑 `assets/hk_map_v6.jpg`。原因：git 直推後 binary 可原檔入 repo（唔使再內嵌）；新檔名避開 app 按路徑快取見舊圖嘅老問題；index 主檔因此細咗約 509KB（5,397,774 → 約 4.89MB）。
- 保留唔刪：`assets/hk_map.jpg`、`assets/hk_map_full.jpg`（舊圖資產）；兩處 fallback 字串仍指 `assets/hk_map.jpg`（MAP_IMG 未定義時唔會 404）；舊 v3 內嵌圖可由 git 歷史（v96 index）還原。
- 紅館（v6 實測約 (46,37)）係景物，冇 LOCS，今包唔畀功能。

## 二、地點標籤／熱區：零改動、逐個實測通過

- **LOCS 15 地點座標一字冇改；15 個方案 B 標籤（.mn68）位置一字冇改**——AUDIT_v6 漂移 ≤1.3% 嘅結論經實駕證實夠用，冇需要動用 ±2% 微調額度。
- 實駕（drive97，見下）逐個熱區篤入：15/15 開到正確地點 sheet（標題逐個對應）；52×52 熱區、pin 視覺全隱藏（釘圖／名牌／NPC 熟人徽章 display:none，v43 規則）冇變。

## 三、地區名細字層（新）

用戶 2026-11-11 15:19 提出、已定方向：地圖除咗地點名，要加一層真實地區名做地理骨架。做法：app 排字（唔入圖，將來多語言可換）——`#map-stage` 內加 `#map-districts97` 層（喺 `.map-names68` 之後），CSS `.md97` 跟方案 B 墨字同一語言但更細更淡：10.5px（地點名 12.5px）、weight 700、letter-spacing .22em、色 #7a5c33、opacity .88、同款紙色光暈；層＋字都 `pointer-events:none`，z-index 2（低過地點名層 3），唔擋熱區、唔搶地點名。

最終落位（left%, top%；跟 v6 圖風格化地理大致方位）：

| 地區名 | left | top | 落位 |
|---|---|---|---|
| 鑽石山 | 49 | 8 | 片場棚群北面山脊（星河電視台／獅子山製片之間） |
| 清水灣 | 84 | 7 | 衛星站半島北面山地 |
| 旺角 | 31 | 15 | 香江唱片以北空地 |
| 九龍城 | 63 | 29 | 城寨樓群東南、跑道根西側 |
| 油麻地 | 20 | 35 | 廟街排檔列西面草地 |
| 紅磡 | 56 | 35 | 紅館以東岸邊 |
| 尖沙咀 | 18 | 51 | 古典大樓岸尖以南 |
| 中環 | 50 | 54 | 中銀背後、太平山東北山腳 |
| 金鐘 | 72 | 57 | 中銀以東北岸 |
| 薄扶林 | 37 | 62 | 仁康醫院西面山坡 |
| 灣仔 | 78 | 71 | 階梯塔（金鐘創意）東南草地 |
| 銅鑼灣 | 89 | 73 | 港島東岸 |

落位迭代申報（新層著位，經實駕 bbox 量度三輪調整；地點標籤／LOCS 本身零改動）：鑽石山初版 (45,7) 同星河電視台標籤 bbox 相撞 → (49,8)；油麻地初版 (22,35) 同九龍電視台標籤擦邊（x 重疊 0.3%）→ (20,35)；中環初版 (52,50) 落喺海灣水面 → (50,54) 山腳陸地；薄扶林初版 (34,63) 掂住西岸水線 → (37,62) 山坡。最終：地點標籤組內、地區名組內、跨組三組 bbox 兩兩**零重疊**，全部標籤喺 stage 內（實測 stage 384×509 @430px viewport）。

## 四、測試

- 新增 `tests/test_map97_static.py`（20 項斷言：MAP_IMG 指新資產、資產存在／JPEG／>700,000 bytes／1376×1824、舊圖保留、15 標籤＋LOCS 座標同 v96 逐一一致、地區層 12 名＋細字＋pointer-events）。**反證：對 v96 index 行有 15 項 FAIL（exit 1）**。
- `tests/test_ux68_static.py` 原位改版一項（有意改變行為）：「MAP_IMG 保留原圖」舊斷言假設內嵌 data URI，改為驗資產檔存在＋>370,000 bytes（「唔硬減」精神保留；實檔 793,164）。改版斷言對 v96 index FAIL（反證）；其餘 ux68 斷言冇郁。
- 全套 A/B：基線（pristine v96）113 PASS／12 FAIL → v97 **114 PASS／12 FAIL**，唯一差異係新增 test_map97 PASS；12 個 FAIL 逐檔一致（已知本機環境性：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111／start53／weave43／weave44／weave49／wrap38），零回歸。
- 觸達審計 `tests/audit_wf5.js` 輸出同 v96 逐行一致（除標頭 index 路徑）。
- index 兩個 inline script block `node --check` 皆 OK。

## 五、實駕證據（drive97，證據檔喺工作副本 `~/workspace/linji-work97/drive97/`）

本地鏡像（work97 工作副本，byte 同本 commit 一致）＋Playwright 真 UI，**34/34 PASS**：

- 地圖圖 currentSrc＝`assets/hk_map_v6.jpg`、naturalSize 1376×1824 已載入；全圖截圖 `shot_map_stage.png` 肉眼確認係 v6（冇橋、中銀、城寨、格仔山丘、紅館），唔係 v3。
- 標籤 bbox：15 地點＋12 地區，三組零重疊、全部喺 stage 內（`boxes.json`）。
- 熱區逐個入 sheet：15/15 標題正確（`sheets.json`；另存 gift_shop／hospital／ad_central sheet 截圖）。
- 地圖頁其他功能：進度掣（去到進度／手帳再返到地圖）、選單→手帳→返回地圖、「全部地點」開關、sheet「返回地圖」掣全部正常；全程零 page error。

## 六、冇掂嘅嘢

SAVE key（`starVolunteer_map_v19w`）／softRev（`s107`）／產品 `?v=`（`v20a10`）不變；content pack JSON 冇直改；v6 圖本身零像素改動（PNG→JPEG 轉碼除外）；玩法、數值、劇情、LOCS、既有標籤位置全部冇郁。
