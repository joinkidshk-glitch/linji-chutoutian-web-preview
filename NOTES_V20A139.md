# NOTES_V20A139.md — v20a139 其餘 6 條 fx 片換 PixelLab character-animation 版

## 背景（用戶 2026-11-12 拍板）
- fx_shoot 全面定版（v129／v130：揮手 loop＋原版場景）、fx_rest 瞓覺片 v3 已定版（v129），唔郁。
- 其餘 6 條跟同一流程：character animation＋原版場景，唔改色。規則：所有片從 character 起手；阿偉沿用 v2（`49907fa9-077f-4f59-aaba-45d3a06958fb`），唔開新 character；動作要簡單 loop。動畫參考只准用我哋自己嘅動畫（8 條已出貨片＋samples19 定版標準 `film_pixel.mp4`），唔准用 ChatGPT 生成片、Kairosoft 截圖或其他外部參考，連對照都唔准。

## 今次落地方式（2026-11-17，現行 main 底重做）
- 舊工作副本 `linji-work139`（HEAD `fedf2dc`，基底 v144，2026-11-12）從未落地，基底太舊（現行 main 已到 v159），**唔 cherry-pick 舊 commit**。新 clone 式工作副本 `linji-work139r`（origin 係常駐 clone 本地路徑）由現行 main `9b1e6f0`（v159）起手，分支 `v139`。
- 6 條片本身已經喺舊副本生成好，**直接沿用＋重新核實**（見下），唔重新生成（PixelLab 零新消耗）。

## 片核實（2026-11-17，沿用前重驗）
- 格式：6 條全部 960×540／24fps／72 幀／3.0 秒（ffprobe 核實）；byte 數＋sha256 同舊 test 檔逐一對得上（shoot_ext 37264／record 42621／audition 34668／train_a 32064／train_b 47894／train_c 49172）。
- 目測（每條 t=1.5s 幀，對照已定版 fx_shoot）：同一阿偉（黑髮、深藍褸＋白恤衫）、像素風一致、場景夾種類——shoot_ext 街頭外景、record 錄音室、audition 試鏡房＋評判、train_a 排練室＋鏡＋導師、train_b 音樂室＋鋼琴＋咪＋老師、train_c 武館＋木人樁＋師傅。
- Loop QC（vf71 vs vf00，全幅）：6 條角落背景漂移全部 **0px**；幀差只限表演中嘅人物姿勢（表演重開），唔係穿崩。舊 QC 數字（240×135 grid：shoot_ext 441／record 280／audition 563／train_a 234／train_b 443／train_c 398px）同一結論。

## 生成記錄（2026-11-12，舊 NOTES 轉錄）
- 6 個 state（PixelLab character v2 `49907fa9` 起手）：shoot_ext `9537ed11`（外景做戲）、record `06e6b88e`（戴耳機唱歌）、audition `6a5690df`（試鏡表演）、train_a `4814e78a`（跟住做動作）、train_b `475c5caa`（對咪唱歌）、train_c `8b39ea0c`（出拳）。train_b state 重試 1 次免費。
- 本票共 **173 次**生成：6 state ×25＝150＋6 animate ×1＝6＋train_c inpaint 9 次＋8 張 pixflux 場景 8 次。餘額 **4641／5000**（2026-11-12 晚核實）。
- 場景來源注意：6 條場景係 pixflux 新生成（description 跟 FX_SPECS §2），唔係由原片抽出嘅背景；「原版場景」喺呢個語境＝每條片首次生成嘅場景（跟 fx_shoot shoot_scene3.png 嘅「原版」同一意思），唔係重生／改色。

## 已知輕微偏離（舊 QC 留檔，唔係硬傷）
- audition：評判 4 位，原片 3 位（pixflux 場景多畫一位；FX_SPECS 寫 3 位）。
- train_a：鏡入面導師重影咗兩個（pixflux 場景 artifact；原片鏡入面係阿偉倒影，新場景刻意唔畫阿偉，避開倒影同步問題，但導師變咗雙重）。
- train_b：老師戴黑超、成人比例（比 chibi 阿偉高約一倍）；原片老師係 chibi 比例。風格上老師似成年人，唔係錯，但同原片比例唔同。
- train_c：木人樁頂 knob 放大睇似細人頭（兩點眼位）；原片樁頂係平圓。見下「披露」。

## 披露：train_c inpaint（要 parent 判斷，舊 NOTES 轉錄）
- train_c 木人樁經 `inpaint-image-pro-flash` 修過（9 次，2026-11-12 21:22），係結構修復唔係改色。
- 但用戶 21:15 嗰句「inpaint／重生都唔用」係針對 fx_shoot 幕布改色講嘅；train_c inpaint 喺決定之後發生。上一手冇留低書面理據話點解呢次 inpaint 合規。修後樁頂 knob 仍然似細人頭（見上），即係話 inpaint 亦冇完全修好。
- 決定權交 parent：接受現狀（留檔）、機械遮眼點（0 次生成，PIL 塗走 knob 上兩點深色，唔郁其他像素，重建 train_c mp4 再重驗）、定係重生場景（1 次生成，但違反「場景用原版」定版流程）。

## 改動清單（index.html，＋6 行）
- `actFx102Html()`（現行 main 約 L43036 起）：加 6 個 `?v=20a139` early return——shootExt／record／audition／trainA／trainB／trainC（L43040–43045）。shoot 行（`?v=20a130`）只係註解更新（「其餘 7 條仲係 20a10」已唔啱，改做「其餘 6 條行 20a139，fx_rest 行共用 20a10」）；共用行 `?v=20a10` 不變（而家淨係 fx_rest 行佢）。SAVE key／softRev s107／產品 `?v=` v20a10 全部不變。
- 6 張 mp4 覆寫（`assets/fx/`，byte 數見上）。
- 新測試 `tests/test_fx139_static.py`：每條新片存在＋byte 數＋sha256＋ffprobe 格式＋接線（map 唔郁、6 條各有 `?v=20a139`、共用行 `?v=20a10`、fx_rest 20a129／fx_shoot 20a130 唔郁）＋紅線（SAVE key／softRev／產品 `?v=` 不變）。反證註明：pristine v159 index 冇 `?v=20a139`、舊片 byte 數唔同 → 多項 FAIL。
- `tests/test_fx129_static.py`／`test_fx130_static.py`：註解更新（v139 後共用行淨係 fx_rest 行）。

## 測試（現行 main 底）
- `node --check` 兩個 inline script 段全部通過。
- `test_fx139_static.py`／`test_fx130_static.py`／`test_fx129_static.py` 逐檔跑全部 ALL PASS。
- 全套（`bash qa131/run_suite.sh`，見 `/tmp/suite139b.log`）：**325 PASS／10 FAIL，零回歸**（基線 324／10；+1 係新測試 `test_fx139_static.py`）。FAIL 十項同基線完全一致，全部 pre-existing：flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38。
- 第一輪全套 320／15：新 FAIL 5 檔全部係 index.html 淨 +6 行引致嘅釘行漂移（gift185／tang171／tang173 總行數鏈、travel114 COUNT 4 處＋FREE 7 處）＋rom159 pristine 反證失效（見下）；第二輪 resync 後逐檔重跑全 PASS（`/tmp/resync139.py`：difflib 單次掃描映射，內容逐行核實純漂移）。
- rom159 pristine 反證失效根因：v159 落地後常駐 clone 個 main 已經係 v159，test 預設 pristine（`~/workspace/linji-repo`）唔再係 pre-v159。修法：pristine 改由 `git show 846e952`（v154 main HEAD，v159 落地前最後一個 main）讀；核實過 846e952 嘅 index 完全冇 ROM159 標記／CMT_vera_commit／commit 鎖條件句，且 v159 改嘅 pack 得 lan_xu（已排除）＋yip_so（新檔），9 個對照 pack 全部唔郁。

## 實駕（押後）
- 瀏覽器死咗（自 2026-11-15），6 條片實機播放未驗。舊底實駕（v144，`qa139/drive139.py`）6/6 PASS——每條 src 啱 `?v=20a139`、readyState 4、960×540、duration 3s、playing、currentTime 推進、0 pageerror、0 http404。等瀏覽器恢復再喺現行 main 重驗。

## 回滾
- index.html：刪 6 個 `?v=20a139` early return 行（shoot 行註解還原）；6 張 mp4 還原舊檔（byte 數見 test_fx139_static.py 反證）；刪 `tests/test_fx139_static.py`。
