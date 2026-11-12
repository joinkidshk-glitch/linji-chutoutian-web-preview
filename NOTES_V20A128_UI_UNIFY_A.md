# NOTES_V20A128 — UI 風格統一 A 批（A1–A6，消除網頁感覺）

## 背景
- 依據：`~/workspace/linji-ui-style-unify/UI_STYLE_UNIFY_PLAN.md` §5（A1–A6）＋§7 地圖建議稿；證據 `DRIVE_NOTES.md`＋`shots/`（139 張截圖）＋`mockup_map.html`。
- 用戶 2026-11-12 14:32 話「想消除網頁感覺」——A 批即修，唔使拍板。B 批（B1–B4）同 C 批（留原生）一律唔掂。
- 產品紅線不變：SAVE key `starVolunteer_map_v19w`、softRev `s107`、產品 `?v=v20a10`；唔改 content pack JSON，一律覆寫表／merge 注入。fx_rest 仲係 `?v=20a129`、fx_shoot 仲係 `?v=20a130`（v129／v130 原狀），其餘 6 條 fx 片仲係 `?v=20a10`。

## 改動一覽

### A1 地圖一屏包（390×844 一屏裝晒）
- 5 個標籤座標微調：星河電視台 `33%/calc(14%-50px)`→`26%/2%`；金禧大酒店 `11%/44.5%`→`11%/32%`（`left:3%` 會因 `.md97{translate(-50%,-50%)}` 置中而出界，改返 11% 先啱）；薄扶林 `41%/65%`→`34%/50%`；灣仔 `78%/71%`→`56%/68%`；銅鑼灣 `89%/73%`→`right:6%/66%`。
- 刪地圖浮「進度」pill（HTML＋CSS＋接線；`_mapProg77` 留 null guard）；**進度入口改返頂欄 chip**：chip 恢復做 `<button>`＋click 接線 `enterHome(null, false, "progress")`＋`cursor:pointer`——按計劃反轉 v108 S-8（chip 係唯一進度入口）。
- 「全部地點」掣由 HUD 搬入底部卡頂行（委派掛喺 `#map-hint`）；drawMap 文字改「全部地點 ▸」／「只亮有事」。
- 壓力 HUD 加粗：track 8px→12px、數字 .78rem→.94rem（實測 15.04px／900）。
- 底部卡改米紙卡（`#fffdf6`、2px `#c97f1f` 金邊、14px 圓角）；「過一日」改全寬金掣；劇情卡改深藍 `#142238`＋2px 金邊；「今日計劃：」文字色修正（舊規則令佢喺淺卡上近乎隱形）。
- N11 根因：唔係捲動，係 toast 一律去頂＋toast-up 嗰 1.8 秒底部卡消失。修法：toast 繼續去頂，但地圖 toast-up 嗰陣底部卡唔再隱藏。
- 劇情卡 2 行截斷：`-webkit-line-clamp:2` 直接落 `<button>` 唔 work（Chromium 計 button 做 `display:flow-root`）；修法係副行改行內流動＋包多層 `<span class="map-hint-story-in128">`。
- 灰色規則字只喺開局第 0 日出（flag `seenMapHelp128`；第 1 日起封死；舊存檔 day>0 永不顯示）。

### A2 地點模板一致性
- N13：`.pres105-line` 啡字落相，對比度低（幾何上無重疊，13px 間隙）。加米白＋陰影相上處理；素底態（`locpanel118-nobg`）另加深色覆寫（見 locfull120）。
- N2：冇企立圖嘅地點（霞姐／禮品老闆娘）唔再浮名牌（隱藏 tagrow＋owner；B1 另案先畫圖）。
- N3：非 hub 地點描述唔再截 28 字，出全文。
- S-23：四個打聽 cost 由裸實物名改動作短語（「請伙記飲凍檸茶」／「請茶客食西多士」／「請化妝師飲咖啡」／「遞包萬寶路畀何生」）。
- 打聽卡圖標按 title 分：還人情／送禮→🎁、飲茶→☕、執漏→🧹、電視城規矩／入廠守則→📺，其餘跌返通用報紙圖 📰。

### A3 對話舞台收尾
- N5：播片嗰陣收起成條 HUD 頂欄（`#app.story-play-lock #map-bar{visibility:hidden}`）——兩個金 pill 頂部穿透 mask 露出，睇落似被裁一半。
- N4：抉擇屏得返紙卡——刪 `.sp-head`（meta＋title＋synopsis），唔再將選項推入金掣列（只留「先返回」），刪走紙卡 `pointer-events:none`／`aria-hidden` 隱藏。`.sp-actions` 隱藏保留（beats 模式）。
- D-7：取捨——揀 Option 2（meta 只喺開場第一句閃現，抉擇步唔出）。唔揀 Option 1（全程顯示會食 ~100px 場景位，人物縮細，同「洩劇本結構」修法方向相衝）。代價：抉擇屏失去 synopsis 上下文（紙卡本身有標題＋後果描述，玩家啱啱播完 setup beats）。
- D-1：開場單人嗰陣，若阿偉喺呢個 node 入面任何 beat 做過 speaker，就補佢企左邊（`spDlgPairIds` unshift "awi"）。阿偉全程唔開口嘅 node 唔會誤加；旁白分支唔郁。
- N16：巧遇第三方句出中間剪影——`ENC79_THIRD128` map（副導／導演／場務／伙記等 12 個職銜→`shadow_male`）＋`enc79ThirdParty128()` helper；overlay 加 `.e79-char3`＋`.e79-char3-halo`（`shadow_male_base.webp`，全光；兩主角 dim 0.6）；名牌出職銜，文案 strip 走行內前綴（只改顯示，唔郁數據）。主線 StoryPlay 本身已識影，唔受影響。
- WF4：舞台 `min-height:480px`（`#mask.wf4-stage-on #modal-inner.story-play.sp-stage`），人物由 34×100 變 98×287。

### A4 通告欄＋文字清理
- N1：刪主頁底 dev 字 block（「本頁修訂 s107。」）；`#start-soft-tip` 本身留返。
- N15-1：通告詳情「💡 有情報」→手繪 sparkle `${iconHtml112("✨")}`。
- 🔒：全檔清零（4 處）——改用 CSS 畫鎖（`.sp-lock-ico` 11×8px 墨線鎖身＋`::before` 弧形鎖扣）。
- N14：通告列表膠囊改印章／紙籤——類型 pill 改米紙籤（dashed 金邊），「可接通告」改紅印章（透明底＋rotate -3deg），已接改灰印章。
- N18：通告詳情「劇情簡介」白底 inset 改米紙；`.cn-lab` 藍改墨色；老闆 hero 高由固定 240px 改 auto（bust 圖 240×312，舊容器會裁走 46px）；「返地點選單」掣改名「返去地點」。
- N12／S-19：壓力明細「而家壓力」vs「而家 0」打架——兩個 call site 傳 `"高峰壓力"` label（`stressImpactLine34` 加可選 label 參數）。
- N9：落選 modal 刪「成功率約 X%」行＋var-note 行（`presentAudFailSettlement` 另一條結算路徑唔郁）。
- N10：週結算文案矛盾句重寫（「阿媽冇提過半句…屋企人唔會開口催數，記低就算。」）。
- S-44：人情卡狀態講三次→講一次——季節卡刪 `· ${status}` 後綴＋null-amount 逾期特例；`DEBT_FUZZY` 頭三句改純指引；絕響句唔郁（測試釘死前綴）。

### A5 圖標補圖（9 張新手繪圖標，風格跟 v112）
- `assets/icons/icon_trophy.png`＋8 隻禮物象形（菠蘿油／蛋撻禮盒／保溫瓶／髮夾組／拍紙簿／卡帶／手作甜品盒／香氛樣品瓶），256×256 RGBA 透明底，墨線 #3a2e22。
- `EMOJI_ICON112` 加 mapping：🏆＋8 禮物；☕／📰 已有 mapping 唔使新圖。7 個 🏆 渲染位全部改用 `iconHtml112("🏆")`——fellowsTxt 經 `esc()`，要拆開（`fellowsWinHtml128` 另加，唔塞入 esc 字串）。
- 九龍電視台 data emoji 📻→📺（inline 數據，唔係 content pack JSON）。

### A6 設定／選單收尾
- 對白速度 `<select>` 改 4 粒紙掣（慢／中／快／即出）＋hidden input（關閉 handler 照讀 `.value`，唔使郁）。
- S-20：還原收細（34px 高）；「返回地圖」由底部搬去頂部（`.home-top` 之後、`.home-tabs` 之前，左對齊細掣）。

## 守門測試
- 新測試 7 個（全部對工作副本 PASS、對 pristine main 乾淨 FAIL）：`test_ui128a1_static.py`（14 項）、`test_ui128a2_static.py`（12）、`test_ui128a3_static.py`（19）、`test_ui128a4_static.py`（15）、`test_ui128a5_static.py`（21）、`test_ui128a6_static.py`（11）、`test_ui128n16_logic.js`（10）。
- 舊測試更新 16 個（A 批刻意改咗期望）：awards62／awards63（iconHtml112 stub）、icons112（35 stems）、locpanel118（📺）、weave43（N10 新句）、guidance34（高峰壓力）、hub77（pill 取消＋chip 入口）、map54（whitelist 加 v20a128）、s30text115（成數 3→2）、terms57（成數 x3→x2）、text125（行號）、travel114（行號 resync，見下）、ui108（標籤座標＋chip）、ux68（全文＋星河座標）。
- 全套：v130 基線 **177 PASS／12 FAIL**；分支 **184 PASS／12 FAIL**（+7 係新測試；12 個 FAIL 同基線完全一致，全部環境性 softRev marker 檢查）。零回歸。
- `test_travel114_static.py` resync 兩次：第一次對 v126 base（44 個 openLoc 呼叫點序列一致、純漂移）；rebase 上 v130 後再 resync 一次（DEF 52955／WRAPPER 43750；COUNT 13／FREE 27 不變）。

## 實駕（`qa128/verify_a3a6.py`，Playwright 390×844、`?softPreview=1`、本地鏡像；另 `qa128/shot_home.py` 補 S-20 頂部截圖）
- C1：step2–4 阿偉＋何生雙人企立（167×487／177×487）；HUD 頂欄全程 hidden（N5）；step16 抉擇屏 head=False、modalBtns=[]、紙卡 2 張可撳（pointer-events auto），撳紙卡→result（N4／D-7）。
- A1 地圖 390×844＋420×900：docScrollH=vh、scrollY=0、hintBottom 816、chip 係 BUTTON、浮 pill 係 null；toast-up 嗰陣 hint 保持可見（opacity 1）；撳 chip→homeOn＋progressOn。
- A6：速度紙掣 4 粒，撳「慢」→hiddenVal=slow；S-20 出口喺 tabs 之上（exitY 92＜tabsY 134），「返回地圖」細掣 90×36 左對齊（截圖 `v128_home_top2.png`）。
- A5 禮品店：購買清單 8 隻禮物圖標齊出（`icon_gift_*.png`）。
- N16：廖炳星 first encounter 第 5 句「副導」——中間影 150×439 全光＋光暈，兩主角同暗 0.6，名牌「副導」、文案已去前綴（截圖 `v128_enc_fudao.png`）。
- WF4 boss01：第 3 次入場觸發，stage 342×480（原 168）、阿偉 98×287（原 34×100）、modal 342×550、wf4-stage-on 生效（截圖 `v128_wf4.png`）。
- **0 pageerror**。截圖喺 `qa128/shots/v128_*.png`。
- Probe 教訓（probe-only，唔係遊戲 bug）：modal 開關係 `#mask.on` 唔係 `#modal.on`；買禮物 modal 嘅 dismiss 掣係「返去地點」（會經 forceRestore 重開 sheet）；encounter 收尾要用返 probe_a3b 嘅 close loop（撳「返去」），唔係淨係 skip。

## 已知殘留（唔喺 A 批範圍，唔好順手修）
- 巧遇攔截靜默吞點擊（pre-existing，v126 一樣）：有星在場撳 pin 嗰陣 intercept 觸發但 overlay 永遠唔出現，板又唔開，但出行額度照扣。間歇性／狀態相關，要設計決定（播唔到就應該開板或 toast，唔好靜默扣額度）。
- 保溫瓶圖標蓋頂有細圓環，睇落似拉環／噴罐頂，可接受，下一批可重畫。

## 合併紀錄
- 分支 `v20a128`（工作副本 `~/workspace/linji-work128/`；origin 係 github.com 直連，唔係常駐 clone 本地路徑）。
- rebase 兩次：第一次上 v129 main `d37284a`（零衝突，`d857870`）；第二次上 v130 main `78b574f`（一個衝突：`test_travel114_static.py` 行號，取 main 版再 resync，`0d44093`）。
- PR：待填。squash 合併入 main：待填。
- 線上核實：待填（index.html byte＋sha；fx_rest `?v=20a129`、fx_shoot `?v=20a130`、其餘 fx `?v=20a10` 不變）。
- 本 NOTES 由分支 commit 入 repo；合併紀錄段由 follow-up commit 補入 main（跟 v129／v130 前例）。

## 回滾
- 成個 squash 係一個 commit：`git revert <squash>` 即退返 v130 狀態。
