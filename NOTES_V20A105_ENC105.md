# v20a105 ENC105 — 巧遇資產組（UI 審計 D-2＋D-3）

日期：2026-11-11（施工員 A 分支 `v20a105-enc`，未合併；合併由統籌員做）

## D-2 巧遇企立（A）
- 審計根源：`enc79StandCandidates` 只有 `UI40_STAND`（12 星得陸柏言）＋ era_stars bust（得 6 星有檔），麥震東／彭少祺／鍾楚凝／顧明輝／齊鎮海／程天諾候補全 404 → 立繪隱藏、對話冇人。
- 資產真相：原生美術庫 `linji-native-design/p0/standing/` 12 星企立原圖（webp）全齊。跟 repo bust pipeline 入庫：cover-crop 864×1152 PNG（top-anchored 保頭像）→ `assets/story/era_stars/{id}_stand_default.png`（12 張）＋中性剪影兜底 `enc105_stand_silhouette.png`（864×1152 RGBA，程式繪製）。對照：mak_zhendong←mak-jandung、pang_siuki←pang-siugei、chai_zanhoi←chai-janhoi、ching_tinlok←ching-tinok、gu_mingfai 用 v2 版。
- 注意（畫面性質）：設計庫「企立版」係素色底腰上企立，同 repo 既有 bust 同格式（非去背全身圖）；入企位槽後人物在場清楚可見。去背／雙企位屬第二包（D-1/D-4）範圍，本包唔掂。
- 改 `enc79StandCandidates`：企立（`?v=20a105`）第一候補 → bust 後備 → UI40 內嵌 → 遠觀剪影 → 入庫剪影檔 → 內嵌 SVG 中性剪影（`ENC105_STAND_FALLBACK`，唔經網絡）。新常數引用包 try/catch（舊測試 sandbox 冇抽常數都唔會 ReferenceError——enc84 人脈頁測試實證）。
- 改 `enc79PlayEncounter` tryNext：候補行晒唔再 `display:none`，改落 SVG 剪影兜底，畫面唔會冇人。

## D-3 巧遇背景（A）
- 改 `enc79SceneSrc`：`LOC_SHEET_BG[locId]`（v103/v104 逐地點新場景，同地點板同一來源）行先；UI40 類別圖（`UI40_BG_BY_KEY`/`UI40_SCENE`）退做兜底；冇逐地點檔嘅地點（如 hospital）仍回 UI40 studio，唔回傳唔存在嘅路徑。

## 冇掂
SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=20a10` 不變；冇掂週界／版面 CSS／文案／其他系統。

## 測試
- 新增 `tests/test_enc105_static.py`＋`tests/test_enc105_logic.js`：ALL PASS（12 星逐個第一候補＝企立逐字路徑＋實檔；13 個巧遇可達地點逐個＝LOC_SHEET_BG 逐字＋實檔；hospital 退兜底）。
- 反證：企立路徑 version 改爛 → logic 12 FAIL；場景 LOC 分支改爛 → logic 39 FAIL；v20a104 index 上行 → FAIL。
- 回歸：enc79/83/84＋cleanup100＋contra98＋scene103/104＋loc96 全 PASS；全套 tests 同 main 對照，失敗清單逐字相同（歷史 softRev 預期等既有 FAIL，唔係本包引入）。全檔 script `node --check` 2/2 OK。

## 實駕（Playwright，本地鏡像 420×900）
新遊戲第 1 日（1990-01-01，dayIndex=0 種子盤）：金鐘創意撞鍾楚凝、海港廣播撞顧明輝（同屬審計點名冇圖 6 星）——兩次立繪 src 均為新企立檔（natural 864×1152、顯示約 490×653／506×674）、背景 src 分別 `bg_loc_ad_adm.jpg?v=20a104`／`bg_loc_tvb_harbour.jpg?v=20a104`（720×1280），零 pageerror。截圖：`~/workspace/enc105-drive/shots/chung_adadm.png`、`gu_tvbharbour.png`；腳本 `~/workspace/enc105-drive/drive_enc105.py`（DRIVE VERDICT: ALL PASS）。
