# NOTES_V20A398_UI_AUDIT6_TOP5

第六輪 UI 檢視（`~/workspace/linji-ui-audit-2026-11-24e/REPORT.md`：GPT A 0／B 3／C 131，
Gemini A 0／B 128／C 6）頭五項修復。基線 v397（main `9fae41f`，suite 419／9），
落地後 suite **421 PASS／9 FAIL**（9 個全部係 pre-existing，同基線同一批）。
`index.html` 50,979 → 51,111 行（淨 +132）。

## 修復一覽

### 1. TUT_MAP 聚光燈缺失＋教學卡遮 pin（UI398-1）
- 教學層獨立 overlay 金圈 `#tut-spotlight-ring`（`.tut-spotlight-ring398`，z-index 520，
  pointer-events none），唔靠 pin class。`refreshTutSpotlight398()` 每次用
  `data-loc="tvb_longmen"` 搵返當前 pin、重新量 `rect` 定位；掛喺 drawMap 尾段、
  `alignTutSurface` rAF、`showTutMainStep`、`finishTutorial`（收起），resize／
  `.map-wrap` 捲動監聽只掛一次。
- **補丁（實駕捉到）**：入場嗰陣地圖仲喺度 settle（實量 pin x 80.1→65.3 約 200ms，
  stage x 15.3→3），即刻嗰次 refresh 攞到舊 rect，金圈偏右 ~15px；`showTutMainStep`
  加 400ms 延遲再 refresh 一次（refresh 內部檢查仲係唔係 TUT_MAP，離開咗會收起金圈）。
  驗證：初次／真重繪（`__phase2.showMap()`）／resize682／resize844 全部置中（偏移 0.0）。
- 教學卡 TUT_MAP 嗰步貼地圖底邊（`#mask.tut-on.tut-step-map{align-items:flex-end}`），
  pin rect (65.3, 258.9, 52, 52) 同卡片零重疊。WELCOME 步聚光燈（`#btn-confirm-plan`）唔郁。
- `rom183ApplyLineOverrides` TUT_MAP 分支重複句「去他們常出沒的地方……」已刪（push 完即返）。

### 2. 大地圖底邊截籤殘留（UI398-2）
- `clampMapLabels397` 改夾**可見帶**（polaroid 頂 → 日卡頂 −2px／viewport 底），唔再用舞台底；
  加頂邊夾實；`deCollideLabels363` 尾段再夾一次，settle 鏈（400／800／1200ms）唔會再推出帶。
  四態（844／682 × seeded／unseeded）量度：clipped []、overlaps []、標籤中點／底邊無不透明遮蓋；
  seeded682 可見帶 ~310px、18 張籤分布均勻，無堆疊。
- **入地圖「今日」大卡刪除**：根源係地圖版 `#toast`（`top:64px`，v20a11 P0-4）喺入地圖嗰陣
  彈「今日：…」遮住頂部地點牌 1.8 秒。兩處 toast 呼叫已刪；資訊由日卡 `#map-hint`
  常駐顯示同一句，過日指引留喺「過一日」掣 title。唔搬落底——底部有手帳拉柄
  （`#book389-handle`），搬落去只係轉移遮蓋對象。
  影響測試：`test_r295_click_not_gam.js` 'day toast' 斷言改釘「toast 已刪＋日卡有今日行」
  （見 `qa398/resync398.py`）。
- 唔郁：venue99 重疊已真修好（紅棉／金禧淨距 12.4px）；「圖釘撞標題」唔成立（最小間距 126.6px）。

### 3. 35c 相片橫額唔對口（UI398-3）
- `np214AwardPhoto214` 非金碟夜典禮設 `cropBanner`；`photoFigure214` 渲染
  `np214-photo-cropbanner`（容器鎖 aspect、img 貼底裁頂）；`#modal-inner` 逢
  `.awd-result396` 加底 26px 淡出。P2 lead 底比摺位高 63.7px（修正後），首屏只露完整行。
- **補丁（實駕捉到）**：520/550（裁頂 108px）裁唔清 awi 相——橫額文字底 ~150px
  （頭髮頂 ~165px），「星河金碟夜」五隻字仲讀到晒。awi 相改 inline `aspect-ratio:520/500`
  深裁（裁頂 158px），頭髮完整、橫額清零；lok 相牌較淺（牌底 ~95px、頭髮 ~110px），
  留 520/550。兩張相實測原圖量度（PIL 行掃＋目視）先定數。P1／P2 相高 230.8px，
  標題＋日期（1991）＋圖說（維港街招・年度廣告賞）全部對口。

### 4. 通告欄頂部報表感＋底欄截印章（UI398-4）
- 板頭去漸變：`.board-head392` 透明貼紙底、冇框冇漸變，sticky 保留；總數行縮成紅印紙章
  （inline-block、1.5px `#9E2F2F` 框、半透明白底、轉 −0.5°）。
- **補丁（實駕捉到）**：板頭底色原寫 `background:var(--panel)`，但 `--panel` 全域只得一個值
  `#3A3530`（深啡），畫面留返條深色報表帶——註解寫明「透明貼紙底」但 code 唔啱。
  改 `background:var(--paper)`（`#E6D2A8`，同 modal 紙面同一值），深帶消失，
  板頭同紙面融為一體；sticky 照樣唔透底（捲動緊嘅卡唔會喺頭板後面現形）。
  `test_v397_static.py`／`test_v398_static.py` 相關斷言一併由 `--panel` 改 `--paper`。
- 排序＋媒介合成一個「整理 ▾」掣（單一選單，分排序／媒介兩組；原有
  `data-sort392`／`data-filter392` 處理唔郁；`sortLabel392` 已刪；靜態 `<button` 112→111）。
- 列表成功率「約 86%」，詳情計法行註明「成功率用精確值，未取整 $81.5，四捨五入」；
  計法本身（$378×86.3%÷4→$82）唔郁。第 6 張卡「可接通告」徽章底 760 ≤ 摺位 745＋淡出 26px，
  落喺淡出區讀做「未完待續」。列表底墊 26px＋`#mask.board-tall392 #modal-inner` 底淡出。

### 5. 日結卡場景唔一致＋黑 backdrop 家族（UI398-5）
- `modal()` 逢 `opts.keepScene397` 掛 `scene398`（`#mask.scene398` 用 v396 日結漸變
  `rgba(0,0,0,.10)` 頂／`rgba(0,0,0,.42)` 底；`closeModal` 拆走）。7 處新增：
  設定（41）、`confirmSpendDay`／43、日結 rest-fallback 同 generic else（27c／44）、
  `rom159DateScene` showResult 同 intro、`presentAwardInvite`／35_invite；
  另加 3 處 pre-existing（`afterDayModal`、`presentStartScheduleConfirm45`、
  `presentRestSleepDayEnd`），共 10 處。
- 實駕：休息卡／訓練卡／設定卡全部 `mask on scene398 day-res`、v396 漸變、地圖可見
  （設定卡 `vmapVisible:true`、無 `ui-hide-under396`）。`confirmChoice236` 唔郁（範圍外）。
- 唔喺範圍：`confirmPlaceShoot`「拍攝排程」modal 係 mid-day 排 shoot 衝突確認，唔係日結卡，唔郁。

## 測試
- 新：`tests/test_v398_static.py`（38/38）、`tests/test_v398_logic.js`（13/13：
  可見帶夾實、cropBanner、TUT_MAP 單句）。
- 全套：`bash qa131/run_suite.sh` → **TOTAL PASS 421 FAIL 9**（9 個 pre-existing：
  flash51、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wf5_87、wrap38）。
  跑完已還原 `qa296/derive296.json`。
- Resync：`qa398/resync398.py`（difflib 映射，內容逐字核實純漂移；travel114 FREE 42＋COUNT 13
  單次掃描 dict 查表；11 檔 patch——總行數鏈、DEF／WRAPPER、rom159／rom176／tang152／
  text125／tang171／tang173 釘行，連同 r295／reconfirm236 C5／v396 button 三項有意圖改動）。
  另記：`drawMap`／`refreshTutSpotlight398` 係 IIFE 內部，probe 經 `__phase2.showMap()` 先係真重繪。

## 實駕證據
`~/workspace/linji-drive398/`：`tut398.json`、`venue398.json`、`board398.json`、
`awards398.json`、`dayres398.json`＋`shots/`（15 張截圖，逐項目視核實）。
Probe 修補：tut 重繪改行 `__phase2.showMap()`；dayres 設定卡嗰腳要循環閂日始 modal 鏈
（晨報「收下這份剪報」→排 shoot「留待下週」→何生來電「好」→WF4 劇情），mask 熄咗先開選單。

## 範圍外（唔郁）
33 底部截斷、34 factbox 淡字、11c、88（下一批）；venue99；「圖釘撞標題」；
板卡計法行同鎖定位置；SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=20a10` 不變。
