# NOTES_V20A142 — v137 設計 review 頭三項修復（A1＋A2＋B1）

- 落地 main：`b06dbc1`（squash merge，分支 `v20a142`，基底 v136 `f0ae995`）
- 線上核實：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/ — 200，5,217,690 bytes，sha256 `29143a46a278d56709156e1cbc6a6948ede393ee6273d1849e9ed057d7b0ce7f`，同 repo `index.html` 一致。
- 改動：`index.html` 淨 +33 行（39 insertions／6 deletions）；新測試 `tests/test_ui142_static.py`（40 項）；`qa142/` 證據全套。
- 紀律：SAVE key／softRev s107／產品 `?v=` v20a10 全部唔郁；唔直改 content pack JSON；git 直接合併，唔開 PR。

## A1 — S-30 詳情老闆 bust 髮頂被切

- 根源（實駕證實，推翻原本假設）：唔係 `#modal-inner` 冇歸零（佢 scrollTop 一直係 0、捲唔到）。真兇係 `#app`（`overflow:hidden` 但 scrollHeight 超高）：`openLoc` 嘅 `scrollIntoView`＋`modal()` 嘅 `focus()` 會捲起 `#app`，`#mask` 係 `#app` 入面 absolute inset:0，成個 modal 跟住上移。Review 原流程重現到 `#app.scrollTop=216` → img `y=-40`；捲數因流程而變（實測 0–537），時現時唔現。
- 修法：`modal()` 開 modal 嗰陣歸零 `#app.scrollTop`＋`#modal-inner.scrollTop`，`firstBtn.focus()` 改 `focus({preventScroll:true})`（setTimeout 入面再歸零一次兜底）。240px 英雄區上限／名牌 `bottom:106px`／`margin-bottom:-100px`／胸口以上 crop 全部唔郁。
- 驗證：review 流程 ×2＋11 位老闆逐位，全部 img_y=176、appST=0。
- 附註：v143 設計 review 量到 img y=176（髮頂完整），話 v137 嘅 y=-40 喺嗰條路徑重現唔到——兩者唔矛盾，bug 係流程相關（取決於開 modal 前 `#app` 捲唔捲起）。呢個修法係防禦性，scrollTop 已經係 0 嗰陣佈局完全唔郁；v141 嘅 y=6（完整）同修後嘅 y=176 都係完整，只係量度路徑唔同。

## A2 — 空狀態死位

- A2a 進度頁：`renderProgress71()` 尾加 `.prog71-next142`「星途寄語」填補區塊（未行晒／十七幕行晒兩種口吻）；pane 底色／外殼唔郁。驗證：進度頁 wrap 底 983＞pane 底 932（內容填滿，微捲）。
- A2b 事業 tab 作品牆：`worksWallHtml59()` 空分支加 3 個虛線金框空畫框（3/4 比例，跟海報，☆）＋「完成作品後，佢嘅作品圖會黐喺呢度。」一句；兩段機制說明文字一字唔郁（B5 唔入呢票）。驗證：3 空畫框見齊。

## B1 — 地圖標籤壓花紋底（4 張）

- 4 個 `.mn68` 靜態錨微調去附近空位（淨郁錨，LOCS 熱區座標唔郁）：香江唱片 28%/+26→29.2%/+31、廟街禮品 44%/-44→28.4%/-104、海港廣播 88%/+16→88%/-44、金龍茶餐廳 11%/-56→16%/-56。
- PIL 逐格灰度 sd：香江 49.8→27.1、廟街 47.6→25.6、海港 67.0→2.7、金龍 3.0→2.9（本身已乾淨，只向右置中）。其餘 11 張唔郁。
- 驗證：15/15 熱區逐針實撳、標籤零碰撞、4 張新位命中。
- 附註：review 報告 B1 寫「墨字＋薄米紙光暈」係講錯咗——實際標籤係深色 pill（`.pin.plab`，`background:rgba(26,20,16,.82)`）；問題本身（4 張壓花紋底）係真嘅。

## 測試＋實駕（v136 基底，最終）

- 全套：pristine 204 PASS／12 FAIL vs 工作樹 205 PASS／12 FAIL，FAIL 清單完全相同（12 個 pre-existing）；多 1 個 PASS 係新測試 test_ui142。
- 新測試 test_ui142_static.py：40/40 PASS，對 pristine 乾淨 FAIL 反證成立。
- 實駕（430×932＋430×700，EXIT 0、ERRORS []、404 []）：A1 11/11 老闆＋review 流程 ×2 全綠；A2 進度頁＋作品牆全綠；B1 15/15 熱區＋零標籤碰撞。
- 12 個 pre-existing FAIL：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43／44／49、wrap38（同 pristine 一致）。

## Rebase 歷史（今晚 main 連續行前，五次 rebase）

- 基底：v141 `4832b85` → v144 `a1b0920` → v143 `632e371` → v134 `c881530` → v136 `f0ae995`；每次 rebase 後全套＋實駕重跑。
- 衝突每次都只係行號測試：test_travel114（44 個 openLoc 呼叫點 difflib 1:1 對位＋內容核實，COUNT 13／FREE 27 不變）＋今次 test_text125（currentLine 27709→27723、advance 27822→27836、familySafe 33423–33425→33439–33441）。
- 教訓：test_travel114 嘅 set 係多行寫法（每行一個數字），resync 要逐行改，唔可以直接 replace 單行字面（v134 嗰轉漏咗，補救時發現）；text125 嘅 `ls[33422]` 係 0-index，換 1-index 行號嗰陣要一併換（rebase --skip 跌咗一次未入 commit 嘅 sed，已補返入 commit `5f9870b`）。
- 落地嗰陣常駐 clone 個 index 入面有 366 個 v138 已 stage 嘅檔案（qa138/baked138 37 張＋assets/story 37 張＋test_dlg138 等，v138 團隊準備緊落地）。合併 commit 只揀咗 v142 嘅 61 個檔案（`git show --name-only` 對過清單，COMMIT-CONTENT-EXACT），v138 嘅 staging 原封唔郁留返畀佢哋。

## 唔入呢票（留返）

- v137 review 殘留 B2–B5、C1–C2。
- v143 review B1–B3 → v145 已派；v134 review A1（700px 短屏 WF4 舞台 modal 間歇性開喺頂部之外，mask bottom-aligned 機制）等用戶決定修唔修。
