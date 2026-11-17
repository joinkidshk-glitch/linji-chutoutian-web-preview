# NOTES_V20A262 — 6 張約會場景圖重做平滑版（2026-11-17）

## 號碼

- 任務原稱 v164，但 **v20a164 已有人用**（2026-11-1x 鄧麗萍送禮補完，main `3973d4a`，`NOTES_V20A164.md` 已存在）。按 brief 指示改用下一個未用過嘅號：**v262**（v20a262 無 git log、無 NOTES、無工作副本；v219／v257 雖係吉號但夾喺舊號之間，唔用；v139／v158／v162 另有排隊票）。
- 基底 main `9b1e6f0`（v159）。工作副本 `linji-work262`（clone 式，origin 係常駐 clone 本地路徑），分支 `v262`。

## 做咗啲乜

v159 落地嗰陣 6 張新約會場景圖出咗像素風，同現成 15 張平滑動畫場景圖唔同。用戶 2026-11-17 拍板重做，行一般人物設計嘅風格（平滑二次元動畫風）。像素版作廢，檔名／路徑不變，換圖唔郁 code。

| 圖 | 構圖（跟像素版） | 真實參照相 | 目視核實 |
|---|---|---|---|
| bg_159_harbour 尖沙咀海傍 | 海傍欄杆前景＋天星小輪＋紅帆船＋黃昏天際線 | 尖沙咀海傍長廊實拍（TST promenade，Star Ferry＋junk） | PASS。初版畫咗 IFC 圓柱塔（2003 年落成，時代錯誤），用 resume edit 換走，改版後最高係中銀大廈（1990 落成），其餘樓矮過佢；冇人冇字。 |
| bg_159_airport 啟德機場 | 747 低飛越過唐樓屋頂＋海＋山＋右邊控制塔 | Kai Tak 低飛實拍（Cathay 747 越過九龍舊樓） | PASS。747 綠白素色塗裝、冇航空公司名／logo；唐樓晾衫／冷氣機／水箱齊；冇人冇字。 |
| bg_159_beach 淺水灣 | 黃昏大太陽＋綠山＋棕櫚樹＋白色酒店＋彎月沙灘 | Repulse Bay 沙灘實拍（彎曲沙灘＋棕櫚＋白色建築） | PASS。冇人冇字，冇現代樓。 |
| bg_159_cinema 旺角戲院 | 全白空白招牌＋紅篷＋木門＋單車＋盆栽 | 皇都戲院外貌實拍（只借舊戲院質感） | PASS。招牌全白留空畀 app 排字；冇抄皇都拱形結構／浮雕；冇人冇字。 |
| bg_159_lounge 酒廊 | 空舞台＋咪架＋譜架＋兩盞吊燈＋盆栽＋白枱布圓枱 | Sheraton 酒店酒廊實拍（暖木＋白枱布＋燈光） | PASS。舞台留空，冇歌手／樂手、冇品牌招牌；樽身標籤係深色塊，冇可讀文字。 |
| bg_159_peak 山頂 | 石欄杆露台前景＋夜晚維港＋兩岸燈火＋山 | 山頂夜景實拍（維港全景） | PASS。最高係中銀大廈，冇 IFC／ICC；冇人冇字。 |

- 全部 720×1280 JPEG，cover-crop 自生成圖 1152×2048（harbour 初版 1184×2096）。
- 生成工具：media.generate_image，三參照（像素版構圖＋風格錨＋真實相片）。Pixellab 唔啱用（只出像素畫）。
- 風格錨：`~/workspace/linji-native-design/style-anchor-awei-anime.jpg`（平塗賽璐璐、清線條）。
- 參照相＋來源記錄：`~/workspace/linji-work-news-refs/ref_262_*.jpg`＋`SOURCES262.md`；生成原圖（1152×2048）存 `~/workspace/linji-work262-refs/gen/`。
- 每張圖逐張目視核實合格先入庫，唔係成批生成先驗。
- 唔郁 code：`index.html` 零改動。`spBgImageCandidates` 嘅 `?v=20a104` 同 6 個 date_* 原路徑維持不變（見下文「緩存決定」）。

## 緩存決定（點解唔升版本參數）

- 場景圖有兩條載入路徑：StoryPlay 經 `spBgImageCandidates`（`?v=20a104`）、地圖面板經 `LOC_SHEET_BG`（原路徑，v159 設計刻意唔加 `?v=`，且 `test_map159_static.py` 釘死咗原路徑）。
- 升 `?v=` 會拖垮 `test_scene103/104_static.py`（釘死 `?v=20a104` 共 29 處）＋其餘 8 檔釘死 20a104 嘅測試，得不償失。
- GitHub Pages 設 `Cache-Control: max-age=600`，部署後約 10 分鐘內瀏覽器會重新驗證，舊像素版唔會長期留低。v159 像素版只上線幾個鐘，接觸面細。
- 結論：純換檔，唔升版本參數；新測試 §3 釘死原路徑不變。

## 測試

- 新測試 `tests/test_scene262_static.py`：33 項全 PASS（§1 存在＋JPEG＋720×1280、§2 sha256 唔等於 v159 像素版舊 sha、§3 date_* 原路徑＋SAVE key／softRev／產品?v= 不變）。
- 反證：對 pristine main（`9b1e6f0`）跑，§2 6 項乾淨 FAIL，其餘 PASS，exit 1——測試識分新舊版。
- 全套 `bash qa131/run_suite.sh`：第一跑（基底 9b1e6f0）324／11——多出 1 項 `test_rom159_static.py` 反證 FAIL，原因係佢預設 pristine 讀 `~/workspace/linji-repo`，而常駐 clone main 落地 v159 後已經唔再係 pristine。呢個唔係 v262 引起；同期落地嘅 v139 已將該測試 resync（pristine 改由 `git show 846e952` 讀），v262 rebase 上 v139（`f3a08c3`）之後該測試 0 FAIL。第二跑（基底 f3a08c3，325／10）：**326／10，零回歸**（+1 係新測試 `test_scene262_static.py`；FAIL 10 項同基線完全一致，全部 pre-existing：flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。

## 落地

- 分支 `v262`（commit `4ecbf9b`）由 9b1e6f0（v159）rebase 上 f3a08c3（v139）後合併；squash merge 入 main，commit `947cf56`，已推 GitHub（`git ls-remote` 核實 `947cf56`）。
- Pages 核實（推後約 4 分鐘）：6 張圖 URL 全部 HTTP 200，sha256 同本地一致（airport `925e7ff5b75b`、beach `bf8dc0b8de2f`、cinema `58541ecfe0a9`、harbour `9b7281dd8ed2`、lounge `aafbfd755fb1`、peak `7e79d9711bf8`）。
- 工作副本 `linji-work262` 已刪。

## 押後

- 實機驗證押後（瀏覽器死）：6 張新圖喺約會場面／地圖面板嘅實際顯示未實機驗過，等瀏覽器恢復再驗。
