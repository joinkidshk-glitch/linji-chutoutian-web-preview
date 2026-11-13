# v20a168 NOTES：頒獎禮 glamour 期間提名卡列隱藏（v166 review C1）

- 分支：`v20a168`；基底 main `60b0a8f`（遊戲 `da05b32`，v166）；工作副本 `~/workspace/linji-work168/`。
- 範圍：淨修 v166 review 唯一新項 C1——glamour beat 期間，同一張海報出現兩次（右邊 panel＋下方提名卡列第一張「阿偉」卡）。
- 唔郁：v166 並置佈局（overlay 只冚 canvas、右邊 44% 暗 panel、海報 121×126）、燕尾服、字幕框邏輯（v166 C1 setCaption）、音頻、贏全長、beats 時長；v147 B1／B2（v149 處理中）；掌聲 MP3。

## 1. 調查：卡列點解 glamour 期間仲見到

- 提名卡列係 `.awd63-cards`（DOM 層，`awards62PlayCeremony` 起 stage 嗰陣一次過渲染，`cardsData`：阿偉卡＋對手卡；阿偉卡用 `posterOf(pack.repGigId63)`，同 glamour panel 係同一張圖）。
- 顯示由 `syncCards(b, elapsed)` 控制：只喺 names／suspense／reveal／comfort 先加 `.on`（`display:flex`），**之後唔會除返**——reveal 之後經 walkup→glamour→out，卡列一路都係 `on` 態。
- glamour overlay 由 `syncGlamour(b)` 控制：淨係 glamour beat 先加 `.on`。v160 嗰陣 overlay 係 stage 全幅＋0.93 暗層，卡列俾暗層壓住唔覺眼；v166 將 overlay 收窄到只冚 canvas，卡列重見天日，同一張 poster 喺 glamour 獨家出現兩次（reveal 嗰陣海報只喺卡列出現一次，冇呢個問題）。
- `syncGlamour` 係單一 choke point：init（`syncGlamour(beats[0])`）＋`advance()` 每次轉 beat 各叫一次；`syncCards` 每 tick 叫，但唔掂 glamour。修法跟返 v166 C1 嘅 setCaption 模式——喺同一個 choke point 加開關，唔另起機制。

## 2. 修法：隱藏（唔係壓暗），`visibility:hidden`

- **揀隱藏唔揀壓暗**：缺陷本身就係「同一張海報出現兩次」——壓暗（例如 opacity 0.15）會留低同一張圖嘅鬼影，重複仲喺度，只係淡啲；只有隱藏先徹底消除。panel 已經講晒得獎資訊（海報＋「得獎／獎項名：《幻彩舞影》」cap），glamour 期間卡列零資訊損失。
- **用 `visibility:hidden`，唔用 `display:none`**：卡列留位（框高 174px 唔變，相對 frame 頂偏移 243→244px，只係 1px 四捨五入），frame 高度／字幕／tap 行唔會喺 glamour 入段／出段嗰陣跳動。`display:none` 會令 frame 成 174px 縮水再彈返，視覺跳動大過原本個問題。
- **恢復機制（自動，唔使另行清理）**：`syncGlamour` 入面跟 overlay 同一條件 toggle——`cardsEl.classList.toggle("glamour-hide", !!(b && b.id === "glamour"))`。下一 beat（`out`）`advance()` 再叫 `syncGlamour`，條件變 false 即刻除返 class，卡列恢復正常；「跳過」／典禮完結拆成個舞台，更加唔使恢復。`syncCards` 唔郁：卡列 glamour 期間繼續係 `on` 態，只係俾 visibility 隱藏，恢復嗰陣唔使重新唱名。
- **改動（零行數變化，唔使 resync）**：`index.html` 改 3 行、加 0 行——
  - L789 同行追加 CSS：`.awd63-cards.glamour-hide{visibility:hidden}`（連註解）。
  - `syncGlamour`（L46277 附近）同行加 cardsEl toggle＋註解（`if(cardsEl)` null guard：gallery 分支冇卡列、冇 glamour 層，`!glamEl` 早返，唔會爆）。
  - 總行數 58,952 行不變；kwan151／tang152／travel114（DEF 53562）等行號錨點全部唔受影響，唔使 resync。

## 3. 測試

- 新 `tests/test_awards168_static.py`：**22/22 PASS**。
  - (1) CSS：`glamour-hide` 規則在場、`visibility:hidden`、唔係 `display:none`、舊 `.on` 規則唔郁。
  - (2) JS：`syncGlamour` 入面 cardsEl 同 overlay 同條件 toggle、null guard、註解寫明恢復、兩個 call 位（init＋advance）齊。
  - (3) `syncCards` 唔郁：只喺 names／suspense／reveal／comfort 加 `on`、唔掂 glamour、唔會除 `on`。
  - (4) v166 並置佈局唔變：overlay absolute＋424/240、panel 44%＋0.93 暗底、海報 88%／60%、glamour 層仲喺 frame 入面。
  - (5) beats 唔變：won 順序 reveal→walkup→glamour→out、glamour 1800ms、walkup 2200／out 500、setCaption 唔郁。
- 反證（pristine main `60b0a8f`）：**6 項修復斷言乾淨 FAIL、零 crash**（CSS 規則、toggle、null guard、註解四項＋同條件兩項）；其餘 16 項回歸守衛喺 pristine 應 PASS，全部 PASS——證明斷言係對修復本身 FAIL，唔係對住唔存在嘅嘢 crash。
- `node --check`：兩段 inline script 全部通過（Node 24 拒 `.html`，抽段驗證）。
- 全套 `qa131/run_suite.sh` A/B（同日即場對照）：
  - pristine `60b0a8f`：**223 PASS／12 FAIL**。
  - 工作版：**224 PASS／12 FAIL**——差額正正係新加嘅 `test_awards168_static.py` 一檔，**零回歸**。
  - 12 項 FAIL 兩邊逐項相同（`test_flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38`），全部係已知穩定 pre-existing FAIL。報告：`qa168/suite_work168.txt`、`qa168/suite_pristine168.txt`。

## 4. 實駕（本地鏡像＋Playwright，`?softPreview=1`，force won）

- 腳本 `qa168/drive168.py`（沿用 v166 `drive166.py`，port 8989），結果 `qa168/drive168.json`，截圖 `qa168/shots/`（18 張）。
- **won_932＋won_700 全部 PASS（每 case 31 項 checks 全 True）、0 pageerror／0 failed request**。
- v168 C1 實測（兩個 viewport 數字一致）：
  - glamour 期間卡列 `visibility:hidden`＋class 含 `glamour-hide`；卡列框高 174px 唔變（reveal 同 glamour 都係 174），相對 frame 頂偏移 243→244px（1px 四捨五入）——留位生效，佈局唔跳。
  - 隱藏時長 1851ms（932）／1681ms（700），對 glamour beat 1800ms 規格（探測滯後內）。
  - 恢復：隱藏完咗之後 timeline 即刻有返 `visible` 項（out beat 期間卡列照常顯示），`cards_restored_after_glamour` PASS。
  - 海報只出現一次：glamour 期間畫面得一張可見海報圖（右 panel，`poster-1988_film_lion_autumn_high.webp`）；reveal 期間亦只得一張（卡列阿偉卡）。字幕／cap 入面嘅獎盃 icon（`icon_trophy.png`）唔係海報，唔計。
  - 卡列張數唔變：glamour 期間 4 張卡照喺度（只係隱藏），同 reveal 一致。
- v166 回歸守衛（兩個 viewport 一致）：
  - 燕尾服 x140–202、61×62px，glamour beat 繪製 15／14 次；5 點探針（中心＋上／下／左／右）**全部命中 CANVAS**。
  - 海報 x268–389、121×126px；海報—燕尾服、panel—燕尾服重疊均 **0 px²**；overlay 對齊 canvas。
  - 空字幕框隱藏：walkup／glamour／out 期間 caption display 全部 `none`；open／names／suspense／reveal 有字 beats 係 `block`。
  - 贏全長（撳「出席」計）：13,608ms（932）／14,076ms（700），對 v166 實測 13,629／13,614ms 一致。
  - 今次獎項名：「影壇新面孔（臨記組）：《幻彩舞影》」（force pack 重骰結果）。
- 實駕量度附註（唔係遊戲問題）：
  - `beats_seen` 嘅 glamour durMs（2447／2665ms）虛高——out beat 唔觸發 segment 轉換，尾項吸埋 out 嗰 500ms＋收尾探測；以 cardsTimeline 嘅隱藏時長（1851／1681ms）為準。
  - `total_about_13_3s` 上限由 v166 嘅 14200 放寬到 15500：`total_from_click` 包含 `attend()` 輪詢等候（第一輪 +775ms），唔係典禮本身變長；watch totalMs（13135／13269）對 beats 總和 13350＋探測滯後，喺合理範圍。
  - 卡列框頂絕對值 reveal→glamour 郁咗 42px（446→488 @932）——係 caption 隱藏嗰陣 frame 縮短＋成個 frame 垂直置中（v166 C1 已有行為），唔係卡列郁；正確不變量係相對 frame 頂偏移（243→244px）。
  - `stage_state` 用兩次 evaluate（base＋extra），beat 邊界嗰陣 seg 標籤同卡列狀態可以差一個 poll——timeline 恢復判斷改用「hidden 項之後有 visible 項」，唔靠 seg 標籤。

## 5. 殘留／已知 outstanding（唔係今票範圍）

- v149 未落地：典禮舞台幾何（v147 B1 舞台細）＋報紙賽果（v147 B2）＋comfort beat 改動嗰陣，glamour 並置＋卡列隱藏要重驗。
- 掌聲 MP3 未經人耳試聽（狀態不變，今票唔郁音頻）。
- 截圖 `won_*_beat_glamour.png` 肉眼對照：右邊 panel 海報＋cap、左邊燕尾服企紅地毯，下方卡列位置留空（暗底），同一張海報只出現一次。

## 6. 合併紀錄（統籌填）

- （待落地）
