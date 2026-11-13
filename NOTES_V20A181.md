# NOTES_V20A181 — 頒獎禮舞台橫向重建（v20a181）

基底 main `91f264a`（v175 NOTES）；分支 `v20a181`；工作副本 `~/workspace/linji-work181/`。
**工人唔落地**：呢票只做實作＋驗證＋commit＋push 分支，唔做 squash merge、唔 push main、唔做設計 review。

## 1. 改動清單

| 範圍 | 改動 |
|---|---|
| `index.html` | ＋171／−163 行（總行數 59434→59442，淨 ＋8） |
| `assets/story/awards/px_*.png` | 新增 36 檔（12 人 × south／east／west），見 §4 |
| `assets/story/awards/bg_awards_ballroom.jpg` | 刪除（M1 實景底圖退役，34KB） |
| `assets/fx/awd_walkup_m4.gif` | 刪除（M4 GIF 退役，19KB） |
| 新測試 | `tests/test_awards181_logic.js`（20 項）、`tests/test_awards181_static.py`（90 項） |
| 舊測試更新 | 160_m1／160_m4／160_m6／166／168／170／174／177／62／63／64_chibi（頒獎禮呈現斷言跟 v181 幾何／退役），＋ `test_soft_tip_111_restore.py` L76（Q 版池改 loadPx） |
| 舊測試 resync（純行號漂移） | kwan151／tang152／tang171／tang173／text125／travel114（見 §6） |
| 實駕 | `qa181/drive181.py`＋`qa181/drive181_report.json`＋`qa181/shots181/`（30 張截圖）＋`qa181/px_verify.tsv` |

## 2. 橫向機制（點做）

- **canvas 邏輯 480×360（4:3）**、backing **720×540**、`setTransform(1.5, 0, 0, 1.5, 0, 0)`；frame 闊 `min(96vw,760px)`，撐滿框冇黑帶。canvas 顯示尺寸實測 932 視口 760×572、700 視口 672×506（≈4:3）。
- **程式舞台 `awards181DrawBase(ctx, W, H, off)`**：淺色幕布 y36–200（`#f2e8d5` 直紋摺）＋深紅側幕；木地板 y200–334（`#d9a75f`＋橫紋豎縫，深 134px＝37.2% 高，對照參考圖下半約四成）；前緣深木邊 y334–340；暗觀眾席 y340–360（`#120c20`＋光點，唔畫人物）；左右簡單深色鐵架燈架 x12–28／452–468。`off`＝pan 橫移 ±6（邊位預留 8px）。`awards62FallbackStage` 改做 delegate 去佢，唔再分叉。**M1 底圖成批撤**：`AWARDS62_STAGE_BG` 常數＋註解＋檔案一併刪。
- **企位**：`FLOOR＝262`；人物 dispH 112（玩家 116、燕尾服 112），人物高約 89px＝框高四分一；won／nominated 4 slots **60／180／300／420**（間距 120，置中 240，罅 78px，兩邊各留 39px）；gallery 3 slots **75／240／405**（罅 165）；入場由台側 −40／520 行入；行前向中央 240 集中 22%、腳 272；獎盃 glyph 燕尾服頂 −112、對手胸前 −52。**冇圓台、冇講台**（v177 C1／C2 舊框問題一併作廢）。
- **文字層係 DOM（`.awd181-*`，`position:absolute` 用 % 對齊 480×360 canvas，`pointer-events:none`，字體用 `cqw` 跟 frame 闊等比縮放）**，字唔入 canvas（免 headless 欠 CJK 字體出豆腐）：橫額 top 1.1%／高 9.5%；數字條 top 12.2%／高 7.8%；白牌 top 22.5%／高 19%（`.long` 縮字）；牌下黃字 top 43.5%。`.awd62-frame` 加 `container-type:inline-size`；`.awd63-glamour` aspect-ratio 改 480/360。
- **人物＝PixelLab character**：`loadPx(starId, dir)`＋`drawPx`，路徑 `assets/story/awards/px_<starId>_<dir>.png`，128px 原圖腳底 y115；企立 south，行跟方向 east／west，唔行嗰陣原地 bob。載唔到畫中性剪影（PixelLab 比例頭＋身），**唔准跌返 Q 版**。
- **Q 版成批清走**：`AWARDS64_SPRITES` 成個 const（34 張 44×50 inline base64，38 行）＋`loadSpr`／`drawSpr`／`sprImgs`／`walkA`／`walkB` 幀值＋頭頂註解一併刪；`AWARDS64` 一詞全檔只剩 1 處（退役註解）。
- **walk-up 改由 canvas 畫**（M4 GIF 已撤）：won beat 2200ms 內阿偉用 px east 幀由台左 −40 行到中央（1400ms 行完，換燕尾服捧杯＋glyph，對手稍暗 alpha 0.7）；文案經 `setCaption("阿偉行上台，接過獎盃，高高舉起。")` 每 tick 補返；beats.walkup.caption 繼續係 `""`（logic test 唔郁）。`syncWalkup` 定義＋兩處呼叫＋`walkupHtml`／`walkEl` 全部刪。
- **保住**：6 beats＋walk-up＋M5 彩紙＋M9 fanfare take 1＋掌聲＋跳過掣＋M6 燕尾服 beat＋comfort beat；卡列／字幕／獎盃 chip 跟橫向重新排位，唔遮人物。
- **唔郁**：fellows 池（上限 3＋阿偉＝4 張卡）、對手加權（頂級 ×3／上一代 ×2／過氣 ×1）、贏線 `AWARDS62_WIN_LINE = 0.875`、comfort beat、報紙流程；淨係改呈現層。

## 3. 數字條數值來源（遊戲真實數值，唔抄參考圖字）

| 位置 | 內容 | 來源 |
|---|---|---|
| 橫額 | 典禮名 | `pack.displayName`（例「廣告年賞」） |
| 左數字條 | 聲望 | `S.fame` 即時值（實駕 seed 42→得獎後 43） |
| 右數字條 | 角逐 | `pack.categories.length`（今屆 1–2 項；實駕 2） |
| 白牌 | 焦點獎項名 | `focus.label` 經 `awards63FocusCat(pack)`（例「最佳男主角」） |
| 牌下黃字行 1 | 代表作 | `repTitle`（`pack.repWork62`／focus.repWorkTitle；冇就「入圍名單逐一揭曉」） |
| 牌下黃字行 2 | 會場名 | `pack.venue99`（冇就典禮名；例「九龍電視城」） |

參考圖字全部唔抄：冇 "Production Announcement"／"Hype 32"／"Popular 11"／"Star Venture"／"First appearance!"；幕布用我哋自己淺色直紋，唔抄淺綠格仔花紋；燈架係簡單深色鐵架。

## 4. PixelLab 人物圖驗證（零 generations 成本）

- 來源 `~/workspace/linji-work180/assets/story/awards/px_*.png`（36 檔，未 commit）＋ v180 正規化腳本 `normalize_px180.py`。
- 人名 ↔ 準確 character id（任務書給定）：阿偉 v2 `awei` `49907fa9-077f-4f59-aaba-45d3a06958fb`（錨：高 102px、頭頂 y13、腳底 y114）；陸柏言 `luk_baakyin` `f8446d12-3619-4b73-9dbb-c93b5601fba6`；廖炳星 `liu_bingxing` `775e2994-7574-40f0-b103-2a7f84f8348f`；齊鎮海 `chai_zanhoi` `aaf8ee63-4173-4261-b8f6-257765c59e06`；麥震東 `mak_zhendong` `29835e66-8052-40ec-b2ea-87671272f99f`；駱家聲 `lok_gasing` `2545998a-e4ca-48b1-a018-0292ca0ce258`；鍾楚凝 `chung_choning` `776ccfd0-1141-45b8-b924-e5a17f1e1d98`；蘇芷茵 `so_jiyan` `f10ca4fb-e5cb-48f7-aba7-48d84be0c922`；魏詠男 `ngai_wingnaam` `31a7520f-1443-4b53-bed4-671e357297a1`；顧明輝 `gu_mingfai` `5e9be5c1-19bb-4a16-a71a-467d60faa9bf`；葉敏芝 `yip_manji` `b46e9a7d-a859-437b-a3ea-5b7deaf1fe3b`；高俊傑 `ko_chunkit` `bbaa5bf2-a598-4863-ba5a-47cc7cc4fe03`。
- 驗證：36 個官方幀全部經 `https://backblaze.pixellab.ai/file/pixellab-characters/6585b418-4b67-4f3b-8ed9-b1e1344cc8d1/<id>/rotations/<dir>.png` 重新下載做 sha256 對照（腳本 `/tmp/px181_verify.py`，輸出 `qa181/px_verify.tsv`）。
- 結果：**18 檔 NORM_MATCH**（work180 檔＝任務規則正規化後嘅官方 raw）、**16 檔 REPLACED**（east／west 幀：v180 將佢哋放大到 102px，任務規則只縮高過 103px 嘅，改用原生高度 99–103px、腳底 y115）、**2 檔 MISSING180**（`px_ko_chunkit_east.png`、`px_ko_chunkit_west.png`，work180 冇，由官方新下載）。34 檔 work180 檔同官方 raw 逐隻 resample 後平均絕對差 MAD 0.00–0.04（0.04 係 103px south 幀 resample 捨入），身份無誤。
- 最終 36 檔（`assets/story/awards/px_*.png`）：全部腳底 y115，高度 99–103px；縮過嘅只有高過 103px 嘅（廖炳星 south 105→102、駱家聲 104/105→102、鍾楚凝 110→102、蘇芷茵 108/109→102、高俊傑 south/east/west 104/105→102）；麥震東 south 103、魏詠男 south 103 原樣保留。**唔經 connector 開新 character、唔用生成 API**（淨下載＋本地量度，零 generations 成本）。
- 池外 starId 冇 px 檔時畫中性剪影（高俊傑唔喺 fellows 池內，只可能經主演衍生；已入埋 3 幀做齊 12 人）。

## 5. 測試

- **新測試**：`tests/test_awards181_logic.js` **20/20 PASS**（mock ctx 錄 fillRect 驗 `awards181DrawBase` 幾何＋pan ±6＋beats 守衛：得獎全長約 13.35 秒、walkup 2200ms caption ""、旁聽約 9.6 秒、comfort 2600ms）；`tests/test_awards181_static.py` **90/90 PASS**（橫向呈現、佈局、企位、人物 px、36 檔 px 資產、Q 版清走、M1／M4 退役、唔郁守衛）。**反證**：對 pristine main `91f264a` 乾淨 FAIL（logic 抽唔到函數 exit 1；static 62 FAIL），唔 crash。
- **舊測試更新**：160_m1／160_m4／160_m6／166／168／170／174／177／62／63／64_chibi／soft_tip_111 全部 PASS；反證 pristine 各有 3–22 FAIL（新斷言數目，唔 crash）。`test_awards62_static` 初版漏咗 3 項（M1 底圖＋Q 版精靈圖）已補返。`test_awards62_logic.js`／`test_awards63_logic.js` 唔受影響，ALL PASS。
- **全套 A/B**：`qa131/run_suite.sh`——工作版 **241 PASS／12 FAIL**，pristine（現時 main，含 v178）**241 PASS／12 FAIL**，FAIL 清單逐項相同（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38——12 項穩定 FAIL）；兩份輸出 diff 只差 `test_awards181_*` vs `test_awards178_*` 檔名。**零回歸**。（註：任務書話基線 239／12 係 v175 當時數字；main 其後落地 v178 加咗 2 檔測試，家下基線係 241／12。）
- 主 script `node --check` 通過（抽出主 script 驗）。

## 6. 行號 resync（v160 教訓：CSS 插入會令釘行漂移）

index.html 淨 ＋8（awards CSS ＋13／頒獎禮區淨 −26／尾段 ＋8），6 檔釘行測試要 resync。用 `git cat-file 91f264a:index.html` 做真基底＋difflib 對位，逐行核實內容逐字相同先改行號（單次掃描 dict 查表，唔逐對 re.sub）：
- kwan151：13 個錨點一律 ＋13（25608→25621、25949→25962、25952→25965、25953→25966、25954→25967、25997→26010、26216→26229、27162→27175、27195→27208、30961→30974、30969→30982、30970→30983、31012→31025）。
- tang152：25768→25781、31451→31464、31595→31608。
- tang171／tang173：總行數 59434→59442、openLoc DEF 53953→53961；tang173 L4845→L4858。
- text125：三錨點一律 ＋13（currentLine 27687→27700、advance 27816→27829、familySafe 33509→33522；報錯字串行號一併更新）。
- travel114：44 個 openLoc( 呼叫點逐行相同（＜45175 者 ＋13、≥52828 者 ＋8；COUNT 13／FREE 27 不變，DEF 53953→53961、WRAPPER 44328→44341）。
- 全部 PASS；pristine main（v178）嗰邊呢 6 檔本身已經 FAIL（基底郁咗），唔係我整爛（對 v175 基底先係有意義嘅比較）。

## 7. 實駕（Playwright，`qa181/drive181.py`）

- 環境：venv `/home/hatch/pwenv49/bin/python`，headless_shell；本地鏡像＋`python3 -m http.server`（port 8972）；`?softPreview=1`；新局 → C1 自動彈出播完 → morning chain → 請柬 modal → 出席／推辭 → 典禮全程。pack 係 hand-built，經真實 UI 路徑餵入：seed `S.pendingAwardPack`＋`S.awardsFlags["1990/award_harbour_ad"]="invited"` → 返地圖 → `queueAwardsOnSeasonWindow` → `restorePendingAward136` 還原請柬 → `presentPendingAward` → 請柬 modal（出席／推辭）。主 script 係 IIFE，`awards62PlayCeremony` 唔係 global，唔可以直接叫。
- **結果：6/6 播完**（932／700 × won／nominated／gallery），**0 pageerror、0 http fail**（報告 `qa181/drive181_report.json`；30 張截圖 `qa181/shots181/`）。
- DOM 證據（每 beat 中段取樣）：932 視口 frame 760×~846、canvas attr 720×540、顯示 760×572（4:3）；700 視口 frame 672×~780、canvas 顯示 672×506；橫額「廣告年賞」、左「聲望42」（得獎後 43）、右「角逐2」、白牌「最佳男主角」、黃字「《夜更和音》／九龍電視城」、卡 4 張（won／nominated）／0 張（gallery）、glamour beat `glamourOn=true`。gallery 推辭版字幕「今晚你喺屋企睇電視轉播」＋揭曉「陸柏言憑《城寨暗夜1988》得獎」；nominated comfort 字幕「何生拍拍你膊頭…」；won walkup 字幕「阿偉行上台，接過獎盃，高高舉起。」。
- 截圖對參考圖逐項核對（`932_gallery_pan.png`、`932_won_names.png`、`932_won_suspense.png`、`932_won_walkup.png`、`700_won_reveal.png`）：橫向 4:3 撐滿冇黑帶 ✓；啡金橫額 ✓；左右黃色數字條（紅喇叭 icon／黃星 icon）✓；大白牌 ✓；牌下兩行黃字 ✓；淺色幕布 ✓；平木地板佔下半約四成 ✓；前緣深木邊 ✓；暗觀眾席帶光點 ✓；三／四人左／中／右分開企、中間大段空地板 ✓；左右深色燈架 ✓；冇圓台、冇講台 ✓；人物約佔框高四分一 ✓。glamour beat 燕尾服＋右邊海報 panel 並置（v166 設計）✓；walkup beat 阿偉由台左行入、對手稍暗 ✓。
- 已知實駕限制：headless_shell 截圖有 stale frame 殘影（例一張 won reveal 截圖白牌字未印上，但同 beat DOM 證據 board＝「最佳男主角」；以 DOM 為準）；取樣時鐘會俾截圖拖慢約 2 秒（每 run 最尾 1–2 個 sample 嗰陣舞台已拆走，frame＝None——證據喺截圖嘗試之前已錄低，唔影響驗證；walkup／glamour／comfort 尾段截圖由上一輪同 code 實駕補返）。

## 8. 實駕捉到嘅 bug（已修）

- **`ReferenceError: esc is not defined`（致命，實駕捉到，靜態測試捉唔到）**：我新加嘅 `awd181Html` 用咗裸 `esc()`，但 `playCeremony` 呢個 scope 本身冇 `esc`（`esc` 係逐個函數 local alias，例 46182 行）。結果：撳「出席」即刻 throw，`attend()` 嘅 catch 跌返結果卡——典禮完全冇播過，0.2 秒就出結果卡。用 CDP `Debugger.setPauseOnExceptions(all)`＋`setTimeout` 延遲撳掣捉實（直接 evaluate 撳掣會死鎖：pause 發生喺 evaluate 執行緊嗰陣）。修法：喺 `posterOf` 同行 append `const esc = (typeof esc59 === "function") ? esc59 : function(s){ return String(s == null ? "" : s); };`（跟 46182 行同一寫法），**零行數漂移**（總行數維持 59442，§6 嘅 resync 唔使重做）。新斷言：`test_awards181_static.py` 加「esc 係 playCeremony local alias」一項（家下 90 項）。
- Drive 教訓（只影響 drive181.py，唔影響遊戲）：「返回地圖」有幾粒同名掣（`#home-back-map-tabs`／`#loc-close`／`#modal-btns` 入面嗰粒），要限死範圍撳；`#map-area-list` 掣喺地圖畫面永遠隱藏，要撳地圖熱區文字；C1 會喺第一次入地點嗰陣自動彈出，要播完先行 morning chain；抉擇屏嗰陣 `.dlg106-plate` 會消失，唔可以當播完；「過一日」之後有報紙 modal（「收下這份剪報」）＋行程 modal，morning chain 要逐個撳；典禮完之後地圖掣由「過一日」變「開始今日行程」（地圖掣唔係 modal 掣）。

## 10. Rebase 上 main 9640c6f（v183）＋重驗（2026-11-13）

- **新基底**：`9640c6f`（v183；開工核實 main 冇再郁）。舊基底 `91f264a`（v175）→ 新基底之間 main 落地四次：v176（ROM176，＋538）、v178（高俊傑入池，＋21）、v182（獎項頁／請柬，＋17）、v183（ROM183，＋117）。合併後 index.html 總行數 60127→**60135**（v181 淨 ＋8）。
- **衝突（10 處）**：
  - `index.html` ×2：① CSS 區——v182 將 `.awd63-csscard` 改做 fellow 專屬卡面，v181 將 `.awd63-glamour` aspect 改 480/360：兩邊都要，取 v182 卡面＋v181 480/360。② `AWARDS64_SPRITES` const——v178 改過佢（ko 衍生來回），v181 成批刪：取 v181（成批清走，只留 1 處退役註解；`loadSpr`／`drawSpr` 刪除本身乾淨合併）。解完核實：`AWARDS64` 全檔 1 處、`AWARDS62_STAGE_BG =` 0、`bg_awards_ballroom` 1（註解）、`awd_walkup_m4` 0、`AWDS63_TINTS182` 4、`awards181DrawBase` 4、esc local alias 喺 L46486（原 L46464，＋22 漂移，寫法不變，**冇跌**）。
  - 測試檔 ×8：全部係行號 resync 衝突（兩邊對唔同基底改同一組釘行），唔係邏輯衝突。解法：difflib 對位（`qa181/resync181_rebase.py`，v181 基底＋main 各自對合併後檔），逐行核實內容逐字相同先改 code 行號，prose 數字／歷史註解唔 blanket 改（只合併歷史＋加一行 rebase 註記）。
- **Resync 結果**（全部內容逐字相同，純漂移）：
  - kwan151：13 錨點 ＋11（＜30523 者）／＋12（≥30523 者）；tang152：25781→25792、31464→31476、31608→31620；tang173：L4858→L4862（名＋code 一併改）、總行數 60135、DEF 54631；text125：27700→27711、27829→27840、33522→33534（報錯字串行號一併更新；v183 註解行補返）；travel114：掃描全部 52 個 `openLoc(` 呼叫點——COUNT 12／FREE 34 不變（v176 8 處 encDone＋v183 C9 intro 免費照舊；v181 嗰兩處「傾談／送禮結果 modal go」喺 main 已改行 `rom176BackOpts()`，由 back176 守衛動態認，唔入 FREE_LINES），DEF 54623→54631、WRAPPER 44340→44353；rom176：6 釘行 6032→6045、31536→31549、53053→53061、53421→53429、54560→54568、54654→54662。
  - awards63／awards64_chibi：淨註解衝突，取 v181 版（Q 版退役文案）。
- **額外修復（rebase 先露出，唔係衝突）**：
  - `test_awards178_static.py` 2 FAIL：(4) 兩項仲斷言 `loadSpr`／walkA／walkB——v181 退役咗 Q 版，呢檔喺 v181 基底嗰陣唔存在（v178 後落地），上一手冇得更新。改做 `loadPx(f.starId, d)`＋三向幀 `["south","east","west"]`，其餘 v178 條款唔郁 → ALL PASS。
  - `test_rom176_static.py` 6 FAIL：6 個釘行仲係 main 行號，v181 漂移未跟（見上）→ resync 後 ALL PASS。
  - `test_soft_tip_111_restore.py` 21 FAIL：**pre-existing，唔係 rebase 整爛**——對 v181 基底 index.html 同款 21 FAIL（fail 清單逐項相同）；對 main pristine 係 22 FAIL（多 1 項係 v181 嘅 Q 版退役斷言，合併後正確 PASS）。根源：s111 嗰層功能（`mapFilterToastText`／`eraSightIsPlaceholder`／`SOFT_REV s111`）喺現行 index.html 已經唔存在（grep 0 處），測試本身過期；全套 12 項穩定 FAIL 之一，唔喺呢票修。
- **重驗數字**：
  - 新測試：`test_awards181_logic.js` **20/20**、`test_awards181_static.py` **90/90**；反證對 pristine main 乾淨 FAIL（logic 抽唔到函數 exit 1；static 62 FAIL）。
  - 相關頒獎禮測試逐個直接跑：160_m1／160_m4／160_m6／166／168／170／174／177／62／63／64_chibi／178／182（static）＋62／63／178（logic）全部 ALL PASS；kwan151／tang152／tang171／tang173／text125／travel114／rom176 全部 PASS。
  - 全套 `qa131/run_suite.sh` A/B：工作版 **248 PASS／12 FAIL**，pristine main（`9640c6f`）**246 PASS／12 FAIL**；兩份輸出 diff 只差兩行新測試 `test_awards181_*` PASS，FAIL 清單逐項相同（12 項穩定 FAIL）——**零回歸**。
  - 主 script `node --check` 通過（抽出主 script 驗）。
- **實駕**：`qa181/drive181.py` 全套 6 run（932／700 × won／nominated／gallery）重跑，報告 `qa181/drive181_report.json` 已覆寫：**6/6 播完，0 pageerror、0 http fail**。DOM 證據同上一輪一致：canvas attr 720×540、橫額「廣告年賞」、白牌「最佳男主角」、卡 4 張（won／nominated）／0 張（gallery）、跳過掣在位（典禮期間 True）；尾段 walkup／glamour／comfort／reveal 取樣嗰陣舞台已拆走（取樣時鐘俾截圖拖慢約 2 秒，上一輪同一已知限制，DOM 證據以較早 beats 為準）。

## 9. 殘留問題（唔阻落地，等統籌／設計 review 決定）

- 實駕 pack 係 hand-built（focus 類別＋3 位真池 fellows＋won 用真 poster `gig_1988_ad_central_spring_high`），經還原路徑餵入；自然贏出嚟嘅 outcome（由 S 計分）唔喺呢票驗證範圍（贏線／計分由 logic test＋v147 校準覆蓋）。
- walkup 行前嗰陣，阿偉會短暫掠過左邊提名人（fwd64 向中央行 22%＋walkup 由台左行入）——過渡幀重疊，企定嗰陣分開，符合設計。
- 700 視口 glamour beat：海報 panel 左緣啱啱掂到白牌右緣（貼住，冇重疊）；再長獎項名要重驗（`.long` 縮字已備）。
- 實駕取樣時鐘漂移（見 §7）：每 run 最尾 1–2 張截圖缺失，證據用 DOM 補。
- `qa181/shots181/` 入面 `932_won_walkup.png`／`700_won_walkup.png` 係上一輪同 code 實駕留低（尾段截圖嗰輪影唔切，檔未被覆蓋；index.html 自 esc fix 後冇再改過，截圖反映最終版）。
- v177 嘅加闊幾何（FLOOR 250 等）已由呢版取代；v177 C1–C3 同 v174 C1／C2 舊框問題作廢，唔使再修。

## 11. 黃字撞頭 fix（2026-11-13，統籌＋用戶睇截圖捉到）

### 11.1 根因（實測，唔係推測）

- 問題檔案（修前）：`qa181/shots181/932_won_names.png`、`932_won_walkup.png`——代表作／會場名兩行黃字落喺人頭高度，第二行「九龍電視城」俾燕尾服阿偉個頭遮住；walkup「九」「龍」俾頭髮遮一半。
- 探針（修前，932 won names，`/tmp/probe181.py`，`getBoundingClientRect()` 實測）：sub 框 **y239–327**（顯示 px）vs 人頭頂 **y265**——成個字框 70% 高度落喺人頭區；換算邏輯座標，兩行字 **156.6–212.6** vs 頭頂 **173**（FLOOR 262 − 可見身高 89），重疊 **40 邏輯 px**；行 2 成行喺人頭區，行 1 下半截都喺度。
- 任務書懷疑嘅「% 係對成個 frame 計」**證實唔成立**：sub 計算值 `top: 248.812px`＝43.5% × **canvaswrap 高 572**（frame 高 865 嗰陣 43.5% 會係 376，唔係實測 239）；`offsetParent` 係 `.awd62-canvaswrap`（`position:relative`，高＝canvas 顯示高）。% 基準本身冇錯，錯在位置本身就係人頭高度——就算對 canvas 計都撞。
- 層疊細節（要講清楚，唔好誤讀）：`elementFromPoint` 喺字行中心返 `CANVAS.awd62-canvas`，唔係因為 canvas 畫喺字上面——係因為 `.awd181-sub` 有 `pointer-events:none`，hit-test 會穿過佢。字層本身 `z-index:3`，係畫喺人物／彩紙（z-index:2）上面；放大裁圖見到黃字筆畫的確疊喺頭髮上面。真正問題係**位置**：黃字壓喺頭髮／面／額頭上面＋彩紙方塊橫過，黃色喺黑髮上面對比崩壞，睇落似俾頭遮住。修位置就解決，唔使郁 z-index。
- 點解牌下空位唔夠用：白牌底 149.4 邏輯 → 頭頂 173 邏輯，得 **23.6 邏輯**罅；兩行字現尺寸要 ~56 邏輯，縮到塞得入會細到唔讀得；獎盃 glyph 頂 150 邏輯亦喺同一高度，字行貼牌底仲會壓住獎盃。牌下冇位，只可以搬入牌。

### 11.2 修法：白牌改三行牌（首選方向，跟參考圖「First appearance!」寫喺牌上面嗰個做法）

- 兩行字搬入白牌，變成牌內細字：**獎項名（大字）＋《代表作》＋會場名（兩行細字）**，字嘅內容一字不變。
- 白牌：`top 22.5%／高 19%` → **`top 21%／高 20.5%`**；牌底 **41.5%＝149.4 邏輯唔郁**——獎盃 glyph 頂 150 邏輯照舊啱啱讓開（1px），人頭頂 173 邏輯照舊有 23.6 邏輯罅。牌頂上移 5.4 邏輯，數字條底 20%（72 邏輯）→牌頂 75.6 邏輯，仲有 3.6 邏輯罅。
- 牌內三行：獎項名用新 span `.awd181-t`（`5.4cqw`，同舊牌面字一樣大，`line-height:1.15`）；細字 `.awd181-sub` 改做牌內 span（**深啡 `#7c4f22`**——黃色 `#ffe14d` 喺白牌上面讀唔到，入牌就要轉深色；對比 6.8 ≥ 4.5；`3.0cqw`、`line-height:1.3`、`margin-top:.3cqw`）。三行總高 **68.4 ≤ 牌高 73.8 邏輯**（1cqw＝4.78 邏輯）。
- `.long` 條件擴大：舊淨係獎項名 ＞8 字先縮；家下細字行 ＞10 字都觸發（獎項名 `4.2cqw`、細字 `2.6cqw`），長代表作／會場名唔會俾牌邊裁走。
- 唔郁：橫額／數字條／地板／FLOOR／企位／獎盃 glyph 位置／人物大小／字嘅內容（代表作／會場名照舊）；彩紙 M5（z-index:2）同 glamour panel（z-index:2）繼續喺白牌（z-index:3）下面，唔會遮牌內字。
- 零行數漂移：`index.html` 總行數維持 **60135**（改動 9 行入／9 行出，原位編輯），kwan151／tang152／tang171／tang173／text125／travel114／rom176 釘行唔使 resync。

### 11.3 改動清單

| 檔案 | 改動 |
|---|---|
| `index.html` L812–815、827–829、46489、46499–46500 | CSS 註解＋白牌／細字規則＋play 註解＋`awd181Html`（board div 包住 `.awd181-t`＋`.awd181-sub` 兩個 span 先閂；`.long` 條件加細字行長度） |
| `tests/test_awards181_static.py` | 90→**99 項**：兩項舊檢查改名（「牌下黃字」→「白牌內細字」）；新加 §(b1) 9 項——舊 `top:43.5%` 已撤、細字喺 board 入面、牌底 149.4＜glyph 頂 150、牌底＜頭頂 173、牌頂唔撞數字條、牌內三行總高 68.4≤73.8（邏輯 px 計出嚟，唔係齋斷言字串）、細字對比 6.8≥4.5、細字唔再係黃色、`.long` 覆蓋長細字行 |
| `qa181/drive181.py` | `EVIDENCE_JS` 加每 beat 幾何：frame／canvas／board／sub 框、sub 兩行行框（Range 量文本節點）、人頭頂（173 邏輯）／glyph 頂（150 邏輯）／地板（262 邏輯）／slots x；每樣本計 `subInsideBoard`／`subAboveHeads`／`boardAboveGlyph` 三項 |
| `qa181/drive181_tail.py`＋`qa181/drive181_tail_report.json` | 新增：尾段補拍腳本＋報告（見 §11.4，主 drive 取樣時鐘漂移嗰 6 個尾段 beat 專用） |
| `qa181/drive181_report.json`＋`qa181/shots181/`（36 張） | 實駕重跑覆蓋；6 張尾段截圖係第一次有檔（之前缺失），其餘 30 張全部修後版 |

### 11.4 測試

- 新測試：`tests/test_awards181_logic.js` **20/20**、`tests/test_awards181_static.py` **99/99**（新加 9 項全過：三行總高 68.4 ≤ 73.8、對比 6.8、牌底 149.4）。
- 相關頒獎禮測試逐個直接跑，全部 ALL PASS：160_m1／160_m4／160_m6／166／168／170／174／177／62／63／64_chibi／178／182（static）＋62／63／178（logic）。
- 主 script `node --check` 通過（抽主 script L5881–60132 驗）。
- 全套 `qa131/run_suite.sh` 呢票**冇重跑**：`index.html` 零行數漂移＋改動只限白牌／細字 CSS＋HTML（grep 過，得 `test_awards181_static.py` 一檔掂 `.awd181-board`／`.awd181-sub` 幾何；`test_awards166_static` 嗰項 `awd181Html + "</div>" + glamHtml` 唔郁，已逐個跑過 PASS）。基底全套數字沿用 §10（248／12）。

### 11.5 實駕（Playwright，`qa181/drive181.py`＋尾段補拍）

- 主 drive：**6/6 播完**（932／700 × won／nominated／gallery），**0 pageerror、0 http fail**；31 個有舞台嘅樣本，幾何三項檢查 **31/31 全 True**（細字行框喺 board 入面、細字底高過人頭頂、board 底唔過 glyph 頂）。
- 每 run 實測數字（顯示 px，board／行 1／行 2／人頭頂）：
  - 932 won names：board 119–236，行 172–203／201–232，頭頂 274（行 2 底離頭頂 **42px**）；walkup：board 151–268，行 204–235／233–264，頭頂 306（42px）；glamour（補拍）：board 243–360，行 296–327／325–356，頭頂 398（42px）。
  - 932 nominated names：board 119–236，行 172–203／201–232，頭頂 274；comfort（補拍）：board 110–227，行 163–194／192–223，頭頂 265。
  - 932 gallery names：board 211–328，行 264–295／293–324，頭頂 366（42px）；reveal（補拍）：同一組數字。
  - 700 won names：board 138–242，行 185–213／211–239，頭頂 275（行 2 底離頭頂 **36px**）；700 gallery names：board 230–334，行 277–305／303–331，頭頂 367（36px）。
  - 全部 beats：board 底離 glyph 頂 **1px**（932 names：board 底 236 vs glyph 頂 237；700 names：242 vs 243——同 v181 原設計一樣啱啱讓開）。
- 尾段補拍（`qa181/drive181_tail.py`）：主 drive 取樣時鐘漂移 ~2 秒，6 個尾段樣本嗰陣舞台已拆走（932_won glamour、932_nominated comfort、932_gallery reveal、700_won glamour、700_nominated comfort、700_gallery reveal）＋700_won walkup 截圖失敗——呢 7 張唔係修後證據（6 張根本未有過檔，1 張係 09:04 舊圖）。補拍每場只取尾段 beat（截圖先、DOM 後，唔累積漂移）：**8/8 樣本幾何全 True、截圖齊晒**，`shots181/` 而家 36 張全部係修後版。
- 視覺驗收（親自睇過）：`932_won_names.png`、`932_won_walkup.png`、`932_won_glamour.png`、`700_won_walkup.png`——白牌三行「最佳男主角／《夜更和音》／九龍電視城」全部完整見到；獎盃 glyph 喺牌底下面露出嚟，冇俾牌遮；人頭離字行成段距離；glamour beat 海報 panel 喺右邊，牌內字唔受影響。彩紙只喺 reveal／comfort／out 期間出現，z-index 喺牌下面，唔遮牌內字。
- 已知現象（唔係問題）：glamour beat 成個 frame 垂直置中位置會移低（932：board 頂由 names 嘅 119 移到 243；卡列嗰陣收起咗），但 board／sub／人頭頂／glyph 頂相對關係不變，三項幾何檢查照過。

## 12. 第二次 rebase 上 main 77603b3（v184）＋重驗（2026-11-13）

- **新基底**：`77603b3`（v184 NOTES；遊戲 `454ed8e`）。舊基底 `9640c6f` 已經係孤兒——reflog 證實 v183 統籌落地後 reset 返 `6ed68f8` 再重落地做 `7497c9e`；`9640c6f` 得返 v181 分支先搵到。
- **孤兒處置**：開工先核實 `git diff 9640c6f 7497c9e -- index.html` 係空（兩個 patch 逐字相同）；10 張 qa183 截圖喺 `7497c9e` 嗰陣未入、之後逐張補返上 main，blob 逐個相同。rebase 停喺 `9640c6f`（index.html 自動合併咗，測試檔 NOTEs／rom176／tang171／tang173／travel114 衝突），核實 diff 已經喺 main 入面之後 `git rebase --skip` 抌走佢——v183 改動冇重新 apply 過一次。
- **衝突（`a684522` 嗰陣，4 檔）**：`test_rom176_static.py`／`test_tang171_static.py`／`test_tang173_static.py`／`test_travel114_static.py`，全部係行號 resync 衝突，唔係邏輯衝突。解法：rom176 頭註解兩邊都留（v184 resync 註記＋v181 rebase 註記），其餘取 v181 嗌邊再 resync；`index.html` 自動合併（v184 嗰 20 行加法同 v181 唔撞位）。冇用過 `checkout --ours/--theirs`。
- **合併後核實**：總行數 60151（60143＋v181 淨 8）；`AWARDS64` 全檔 1 處、`awards181DrawBase` 4、`AWDS63_TINTS182` 4、`bg_awards_ballroom` 1（註解）、`awd_walkup_m4` 0、`AWARDS62_STAGE_BG =` 0；esc local alias 喺 L46497（上一手 L46486，＋11 漂移，寫法不變）；v184 20 行加法逐行 grep 全部在位（`AWDS63_DEEPS184`＋`awardsCatsSorted184`，卡面色＋排序邏輯冇跌；v181 橫向舞台＋三行白牌＋PixelLab 人物冇跌）。
- **Resync**（`qa181/resync181_rebase2.py`，difflib 雙基底對位——`a684522` 60135 行＋`77603b3` 60143 行各自對合併後 60151 行，內容逐字相同先認純漂移，兩個映射交叉一致）：kwan151／tang152／tang173 L4862／text125 唔郁（全部喺 v184 插入點 45748 之前）；DEF 54631→54647；WRAPPER 44353 唔郁；rom176：6045／31549 唔郁，53061→53077、53429→53445、54568→54584、54662→54678；travel114：COUNT 後 4 處＋16、FREE 52884 之後 22 處＋16，其餘唔郁，COUNT 12／FREE 34 不變，全掃描 52 點 FREE 34／COUNT 12／DEF 54647。改行號只改 code 行（單次掃描 dict 查表），prose 數字／歷史註解唔 blanket 改（4 檔各加一行 rebase 註記）。
- **額外修復（rebase 先露出，唔係衝突）**：`test_awards181_static.py` 黃字斷言 L119 格式化 `board_h * 3.6` 唔守衛——對 pristine `77603b3` 會 `TypeError` crash（上一手反證 62 FAIL 係對 `91f264a`，嗰陣 regex 啱啱搵到數所以冇 crash）。改做 `(board_h or 0)`，工作樹輸出逐字不變（99/99）。
- **重驗數字**：`test_awards181_logic.js` **20/20**、`test_awards181_static.py` **99/99**；反證對 pristine `77603b3`：logic exit 1（`FAILED: 1`，抽唔到函數）、static 31 PASS／68 FAIL、exit 1、零 traceback；相關頒獎禮測試（17 static＋4 logic）＋resync 7 檔全部 PASS；主 script `node --check` 通過。
- **全套 A/B（呢輪作廢，見 §13）**：工作版 249/12，但 pristine 嗰輪誤用常駐 clone 工作樹——v185 喺 suite 跑緊嗰陣落地（`7c23238`，09:54:47 UTC），pristine 讀到半落地樹（`test_gift185_logic.js` 喺 `.js` glob 展開之後先寫入，冇跑到；`test_gift185_static.py` 喺 `.py` glob 嗰陣已入，PASS），248/12 唔係有效基線。教訓：**pristine 一定要用 `git archive` 抽指定 commit，唔好用常駐 clone 工作樹**（佢會郁）。兩份 rebase2 suite 檔已刪除，數字以 §13 重跑為準。實駕嗰輪未跑（等最終樹）。

## 13. 第三次 rebase 上 main cd4985f（v185）＋重驗（2026-11-13）

- **原因**：v185 喺第二次 rebase 做緊嗰陣落地——code `7c23238`（09:54:47 UTC）＋NOTES `cd4985f`（09:57:52 UTC），main 由 `77603b3` 郁到 `cd4985f`。第二次 rebase 嘅 resync 工作已先 commit（`7df5d0f`）再 rebase。
- **v185 改動**：`index.html` 淨 2 個同行 hunk（L3847 禮物選擇器 CSS、L58609 `openGiftPick` spans），淨 **0 行**，總行數 60143 不變；其餘係 `test_gift185_logic.js`／`test_gift185_static.py` 新檔＋`test_icons112_static.py`＋qa185。
- **Rebase 零衝突**：4 個 commit 一次過 replay（`07da4c2`／`f6c154b`／`f7bfda8`／`3f2b348`），新 HEAD `3f2b348`。合併後總行數維持 60151；esc alias 仲喺 L46497；v185 兩處改動在位（`gift-pick-name` ×2、`v20a185 B1+C1` ×1）；v184 卡面色＋排序、v181 舞台＋三行白牌全部在位。
- **Resync**：v185 淨 0 行，釘行零漂移——resync 7 檔（kwan151／tang152／tang171／tang173／text125／travel114／rom176）＋gift185／icons112 逐個重跑全部 PASS，唔使改行號。唯一例外：`test_gift185_static.py` 總行數斷言 `== 60143`→`== 60151`（code 數更新，標籤留返 main 數字＋加一行 rebase 註記），修後 19/19。
- **重驗數字**：`test_awards181_logic.js` **20/20**、`test_awards181_static.py` **99/99**；反證對 pristine `cd4985f`：logic exit 1（`FAILED: 1`，抽唔到函數）、static 31 PASS／68 FAIL、exit 1、零 traceback；相關測試（頒獎禮 17 static＋4 logic、gift185 logic＋static、icons112、resync 7 檔）全部 PASS；主 script `node --check` 通過。
- **全套 A/B**（`git archive cd4985f` 抽真 pristine，見 §12 教訓）：`qa131/run_suite.sh <repo-root> <outfile>`——pristine **249 PASS／12 FAIL**，工作版 **251 PASS／12 FAIL**；FAIL 清單逐項相同（12 項穩定 FAIL：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），兩份輸出 diff 只差兩行新測試 `test_awards181_*` PASS——**零回歸**。
- **實駕**：`qa181/drive181.py` 全套 6 run（932／700 × won／nominated／gallery）重跑，報告 `qa181/drive181_report.json` 已覆寫：**6/6 播完，0 pageerror、0 http fail**；29 個 staged 樣本幾何三項全 True（sub 喺 board 入面、sub 底高過人頭頂、board 底唔過 glyph 頂）；三行白牌「最佳男主角《夜更和音》九龍電視城」每樣本齊；board 底離 glyph 頂最少 **1px**、行 2 底離人頭頂最少 **36px**（黃字 fix 喺 rebase 後仲在位）。截圖存返 `qa181/shots181/`（36 張，今輪覆寫 24 張）。已知限制同上一輪：尾段取樣時鐘漂移 ~2 秒，7 個尾段樣本嗰陣舞台已拆走（932_won walkup／glamour、932_nominated comfort、932_gallery reveal、700_won glamour、700_nominated comfort、700_gallery reveal），DOM 證據以較早 beats 為準；其餘 12 張（§11 補拍尾段圖）未被覆寫。
