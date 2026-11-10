# NOTES V20A85 POSTER85：A 級 59 張作品圖接入（檔案參照）

日期：2026-11-11（基底 v20a84，5,115,599 bytes，tests 基線 98 項計法下全過；本機環境另有 12 個環境性 static 失敗，v84 pristine 同樣失敗，唔關本包事）

## 本包做咩

- 1990 年選角表（`linji-poster-casting-1990.md`）A 級獨畫 59 部，全部出圖完成並接入遊戲。
- 接入行**檔案參照**：新圖以原檔 WebP 入 `assets/posters/`（git 直推通道，binary 原檔），
  主檔 index.html 只加 `POSTER85_IDS`（59 個 gig id）＋ `poster85File()` 衍生檔名＋
  `poster59Path()` 加一條分支。主檔增幅約 +4KB（冇 base64 內嵌、唔脹）。
- `poster59Path()` 優先序：試點 10 張（POSTER59 內嵌 data URI，行為完全不變）→
  POSTER85 命中回 `assets/posters/poster-<gig id 去 gig_ 前綴>.webp` → 其餘回空字串。
  全部顯示位（通告詳情、作品牆、殺青、頒獎 glamour）本身有 onerror 隱藏／CSS 片名卡降級，
  圖檔缺失或載入失敗唔會爛版（新測試有釘降級路徑回空）。
- 交付圖規格：600w WebP（q80），跟 v59 試點 master 口徑；生成原稿（全尺寸）保留喺
  工作副本 `linji-work85/poster_src/`（連 MANIFEST.json 生產清單），原生版可取用。

## 阿偉企位（本包判斷，已喺交付報告交代）

試點 10 張當年一律「臨記期只有明星」版；A59 59 部橫跨中／高位階通告，改跟 **gig 本身位階**：

- **雙主演**（阿偉同紅星並列入畫）30 張：roleScale = film_lead_big（10）／tv_lead_long（6）／rec_album（14）
- **細位配角**（紅星主演、阿偉細位次要入畫）6 張：film_support_main（5）／tv_support_main（1）
- **只有明星** 23 張：ad_av（6）／ad_print（5）／photobook（3）／mtv（3）／variety_special（6）
  ——廣告／寫真／MTV／綜藝特備係明星面孔載體，照選角表本意唔加阿偉。

## 生產同驗收

- 6 批並行生產（每張帶風格錨＋主演既有立繪做樣貌參照；雙主演／細位再加阿偉錨圖），
  逐張驗收：主演面孔對照立繪、零可讀文字（連遠景道具微字）、直幅、賽璐璐風一致、企位啱。
- 59 張入面 9 張要重出（共多用 11 次嘗試）：主因係首版出咗可讀字／字母
  （ad_06 牆框字跡、rec_hk_spring_high 鋼琴邊字母、rec_star_summer_high 畫邊塗鴉）、
  幅比唔啱（正方形）、或阿偉畫成細路（tv_longmen_spring_mid）。
- 統籌覆核（contact sheet 總覽＋重點放大）再挑出 2 張補出：
  - `film_cotton_autumn_high`《警網雄風》：舊版遠景貨櫃有極細不可讀模板字痕跡；
    補出改用空白貨倉捲閘背景＋電筒對峙（避開貨櫃同槍械措辭——含槍械嘅一次重出曾被生成端內容審查拒絕），
    補出 1 次成功、統籌親自放大覆核背景全空白。
  - `rec_star_summer_mid`《俠影琴心錄像》：舊版劍俠袍內露出西裝背心＋紅領呔；
    補出改全套純古裝（第 1 版劍刃近護手有疑似刻紋，再出第 2 版素面劍刃定版）。

## 測試

- 新增 `tests/test_poster85_logic.js`：POSTER85_IDS 恰好 59 且同選角表 A 級權威清單
  完全一致、全部真喺 1988 通告包、與試點零重疊；查表全部回正確檔案路徑；
  試點優先回 data URI（冇回歸）；B 級／散工／入門／亂 id／空值回空（降級）；
  59 張圖檔喺 `assets/posters/` 齊在且 WebP RIFF、>15KB。對 v84 index 抽取唔到 POSTER85 → FAIL（反證）。
- 新增 `tests/test_poster85_static.py`：標記在位、SAVE key／softRev／?v= 不變、
  NOTES 在位、主檔冇脹大（< v84 + 60KB）、POSTER85 段冇 data URI。
- `tests/test_poster59_logic.js` 只做 harness 維護：抽取清單加 `POSTER85_IDS`／`poster85File`
  （因 poster59Path 擴充咗分支），全部原有斷言冇改、照舊全過。

## 遺留／唔喺本包

- B 級 68 部繼續用分類圖頂住；1991／1992 選角表未做（機制已預留：嗰兩年嘅 gig
  只要補 POSTER85 式查表＋圖檔即可，poster59Path 唔使再改結構）。
- 生成原稿只喺工作副本，未入 repo（repo 只入 600w 交付版，控制體積）。
