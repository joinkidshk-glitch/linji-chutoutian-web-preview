# NOTES_V20A325_SEAL_RARE — 稀有印章 seal_rare.png 補圖

> Base：main `b5d1522`（v20a324，通告庫 322 張）。票源：v229 已知缺口 #4（`NOTES_V20A229.md:40`）。
> 偵察 brief：`~/workspace/linji-seal-rare-brief.md`（2026-11-19，唯讀核實，全部前提喺工作副本再對一次先動手）。

## 一、改動（3 檔，index.html／gigs_new.json／?v=／SAVE key／softRev 零改動）

| 檔案 | 改動 |
|---|---|
| `assets/ui-physical/notice/seal_rare.png`（新增，57,155 B） | 照 v20a94 前例：`seal_junior` 做底保留原雙圈（r ≥148 原封），中心字換 Noto Sans CJK TC Bold「稀」，朱紅 `(196,59,42)`，字框對齊原「初」字位。腳本 `/tmp/make_seal_rare.py`（由 `linji-work94/verify94/make_seal_extra.py` 改三樣：字 `'臨'`→`'稀'`；SRC／DST 指工作副本；glyph 198×197 at (112,104)，font size 208）。唔用 AI 出圖／PixelLab／外部參考（ART_BRIEF 禁 AI CJK）；binary 原檔入 repo。 |
| `tests/test_press94_static.py` | 加 `S07b_seal_rare_asset`，照 S07 款式斷言 `seal_rare.png` 存在。`gigTierKey` 稀有→rare 已有 `tests/test_gig229_tiers.js` 斷言，唔使加。 |
| `assets/ui-physical/MANIFEST.md:15` | 印章行補 `seal_rare.png`（Noto 稀）。 |

## 二、圖規格驗證（實測，唔係目測）

- 420×420 RGBA；四角 alpha 0；全透明像素 130,471／176,400。
- 最多不透明色 `(196,59,42)`（29,122 px）。
- 環區（r ≥148）同 `seal_junior.png` 逐像素相同。
- 中心區（r <148）字框外紅像素 0 粒——無殘留「初」字筆畫；中心紅框 x113–309／y105–299（目標框 x112–310／y102–304）。
- 目視：六印並排（初／中／高／急／臨／稀）同一套（雙圈＋單字置中、無裁切）。

## 三、測試

- `python3 tests/test_press94_static.py`：13／13 PASS，含 `S07b_seal_rare_asset`。
- 全套 suite：`bash qa131/run_suite.sh` → **TOTAL PASS 385 FAIL 9**＝基線；9 項 FAIL 全部係已知 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），逐項同基線一致，零回歸。跑完已還原 `qa296/derive296.json`（唔入版）。

## 四、實機驗收（本地工作副本 http://127.0.0.1:8901/，Playwright headless shell，viewport 390×844 dsf 2，pageerrors 0）

播種：新遊戲攞預設 S → `dayIndex=622`（1991-09-15 秋）寫入槽 3 → reload 讀檔。舊 fullarc `setup_to_slot3` 流程已唔啱現行 main（planner confirm 會開「通告板」modal，冇「確定出發」掣），今次改用 localStorage 播種（key `starVolunteer_map_v19w_slot3`／prefs `starVolunteer_prefs_v19z9`，`normalizeSaveObj` 會補預設值）。

- **通告板短卡**（清水灣片場 `film_cotton`）：`gig_1991_film_116`《劍嘯長空》男主角 teaser——`seal=assets/ui-physical/notice/seal_rare.png?v=20a8`、`alt=稀有`、`loaded=true`、`natW=420`、transform matrix＝rotate 6°（cos 0.9945／sin 0.1045）、dispW 31（28px 旋轉後包圍框）。截圖 `board_film116.png`：右上角「稀」印章，同卡「臨」印章對照齊。
- **手帳全卡**（作品副頁 `htab-works` → 拍攝簿「待試鏡」段，`gigCardHtml`）：同一張 gig——`seal=seal_rare.png?v=20a8`、`alt=稀有`、`loaded=true`、`natW=420`、`dispW=dispH=44`（`.gig-card .g-seal` 44px override，`index.html:1423`）。截圖 `fullcard_jobs.png`：全卡右上角「稀」印章 44px。
- 附帶核實：詳情頁（`castingNoticeDetailHtml`）本身無印章（`NOTES_V20A94_PRESS94.md:63`），撳短卡只見「接通告／離開」，唔係漏圖。

## 五、唔郁清單

`index.html` 零改動；`content/gigs_new.json` 唔郁（稀有 21 張不變）；`?v=20a8` 沿用；SAVE key `starVolunteer_map_v19w`／softRev 唔郁。

## 六、觀察（pre-existing，唔喺呢票範圍，唔改 code）

`gigCardHtml` 兩個 call 位喺現行 live 幾乎行唔到——`promptAudition`（`index.html:45331`，內含「未能試鏡」modal 全卡）全檔 0 呼叫；`S.booked`（拍攝簿「待試鏡」段）新存檔永遠空陣列（只讀／過濾，冇 push 位）。即係新玩家喺 live 只會喺通告板短卡見到「稀」印章；全卡要舊存檔帶住 `booked` 預約先見到（今次驗收就係咁播種）。唔係呢票造成，唔開修復票住，記低先。

## 七、落地

- 內容 commit：（待填）
- main HEAD：（待填）
- Pages 核實：（待填：`seal_rare.png` 線上在位＋index.html byte-identical）
