# PLAN_UI_PHASE3_COPY_HOOKS_v1

> Soft≠PASS｜UI Phase 3 政策重修｜對齊 PLAN_UI＋FULL＋ERA｜經 qwen3.7-max｜閘未驗＝Mock｜出圖 HOLD｜唔 tip｜89–92 HOLD｜已殺條件外試投

## 1. 範圍 (Scope)

本計劃確立《臨記出頭天》UI Phase 3 Soft 文案與鉤子規範，供 tester 抽樣及 web Soft 預覽。涵蓋紅星遠觀佔位（純文字＋音）、通告卡接洽樣式、Soft hooks。

**對齊文件**：PLAN_UI_SYSTEM_DESIGN_v1（Phase 3）；PLAN_STORY_QWEN37_FULL_v1；PLAN_ERA_STAR_TARGETS_v1；PLAN_CHAR_LOOKS_REF_v1（出圖 HOLD）；PLAN_UI_PHASE2_COPY_HOOKS_v1；PLAN_GIG_CARD_PLAYER_COPY_v1；PLAN_FULL_MVP_SOFT_LANDING_v1。

## 2. Out of Scope

- LIVE tip 推送
- 行為閘重鎖實作（閘未驗＝Mock only）
- 出圖（紅星立繪／寫實 brief 一律 HOLD）
- 89–92 事件
- 關海媚升格；鄧線實裝（僅 DEV 入口一句）
- 改 gigs JSON 底層
- 交 iOS Soft（本輪唔交）
- **已殺條件外試投路徑**：條件未合＝「暫未能報」＋離開；board 只 ready｜locked；唔設第三態 CTA

## 3. 紅星遠觀佔位（首輪只四人 · 已拍板 B）

遠觀呈現 **B**：首輪＝**純文字＋音效**（出圖後先升剪影）；首輪 Mock 唔當剪影 UI 必需。

### 3.1 陸柏言
- **玩家面顯示名**：陸柏言
- **遠觀／環境描述**：陸柏言身穿深色闊膊西裝配高領冷衫，喺走廊行過，身邊有保鑣跟隨。
- **距離感文案**：保鑣將你隔開，只能喺遠處望住佢哋行過，無法埋身。
- **噂碎片輕鉤**：聽講佢最近接咗套大製作，對劇本極之挑剔。
- **建議出現 loc**：片場走廊／電視台大堂

### 3.2 廖炳星
- **玩家面顯示名**：廖炳星
- **遠觀／環境描述**：廖炳星着住格仔恤衫，坐喺片場梳化度，淨係見到背影。
- **距離感文案**：佢正喺度專心度橋，只能遠望佢個背影，唔好行埋去阻住佢。
- **噂碎片輕鉤**：圈內傳聞佢套新戲嚴重超支，前幾日仲喺茶餐廳同人嗌交。
- **建議出現 loc**：金龍茶餐廳／片場休息區

### 3.3 魏詠男
- **玩家面顯示名**：魏詠男
- **遠觀／環境描述**：魏詠男着住運動外套配功夫衫，企喺後巷半明半暗嘅陰影入面。
- **距離感文案**：佢散發住一股英氣，生人勿近，你只能喺後巷遠處靜靜望住佢。
- **噂碎片輕鉤**：有傳佢準備轉型做幕後，又或者會接拍高難度武打戲。
- **建議出現 loc**：片場後巷／舊區街角

### 3.4 葉敏芝
- **玩家面顯示名**：葉敏芝
- **遠觀／環境描述**：葉敏芝着住針織衫配短裙，喺訓練班鏡前練舞。
- **距離感文案**：佢喺鏡前專心練舞，競爭壓力極大，你只能喺遠處觀望，唔好打擾。
- **噂碎片輕鉤**：聽聞呢批新人為咗爭上位，暗地裏爭奪公司資源爭得好犀利。
- **建議出現 loc**：訓練班排練室／公司走廊

### DEV 附錄（唔入主表）
- 齊鎮海：後輪可選；首輪唔入遠觀主表、唔強掛地圖。

## 4. Casting Detail／通告卡樣式

board 狀態只 `ready`｜`locked`。

### 4.1 條件符合
- **主 CTA**：「接通告」或「真・接通告」
- **成功 Toast**：劇組通知：接通告成功！

### 4.2 條件未合（Toast A · 已拍板）
- **按鈕**：「暫未能報」（Disabled 灰底）
- **tapFeedback**：shake
- **toast**：「條件未合」
- **subLine（業界書面語）**：試鏡表現未夠火候，建議先跟班觀摩再作安排。

*(註：舊版 4.3 條件外試投整節已刪；條件未合即鎖定並離開。)*

## 5. Soft Hooks 表

| 內部 key (DEV) | 玩家句 | loc／表面 | 對齊註 (DEV) |
| :--- | :--- | :--- | :--- |
| `hook_star_luk_corridor` | 保鑣將你隔開，只能喺遠處望住佢哋行過，無法埋身。 | 片場走廊 | 陸柏言遠觀佔位 |
| `hook_star_luk_rumour` | 聽講佢最近接咗套大製作，對劇本極之挑剔。 | 金龍茶餐廳 (傳聞板) | 陸柏言噂碎片 |
| `hook_star_liu_cafe` | 佢正喺度專心度橋，只能遠望佢個背影，唔好行埋去阻住佢。 | 金龍茶餐廳 | 廖炳星遠觀佔位 |
| `hook_star_liu_rumour` | 圈內傳聞佢套新戲嚴重超支，前幾日仲喺茶餐廳同人嗌交。 | 金龍茶餐廳 (傳聞板) | 廖炳星噂碎片 |
| `hook_star_ngai_alley` | 佢散發住一股英氣，生人勿近，你只能喺後巷遠處靜靜望住佢。 | 片場後巷 | 魏詠男遠觀佔位 |
| `hook_star_yip_mirror` | 佢喺鏡前專心練舞，競爭壓力極大，你只能喺遠處觀望，唔好打擾。 | 訓練班排練室 | 葉敏芝遠觀佔位 |
| `hook_casting_success` | 劇組通知：接通告成功！ | 通告卡面 | 接通告成功 Toast |
| `hook_casting_fail_toast` | 試鏡表現未夠火候，建議先跟班觀摩再作安排。 | 通告卡面 | 暫未能報副行 |
| `hook_ho_advice_soft` | 何生提醒：練好基本功，條件未合就暫未能報，唔好硬闖。 | 事務所 (對話) | 何生條件提醒 |

## 6. Mock 規格與接入備註

對應 `MOCK_UI_PHASE3_STAR_CASTING_v1.json`：
- `meta`：version／date 2026；softStatus≠PASS；sightingMode=text_plus_sfx；abLocked 遠觀B／Toast A／第五星B
- `starSightings[]`：**剛好 4**（陸柏言／廖炳星／魏詠男／葉敏芝）
- `castingCta`：只 `canCast`｜`cannotCast`（唔設第三態 CTA）
- `boardCardStates`：只 `ready`｜`locked`
- `devAppendix`：齊鎮海後輪可選一句
- `hooks[]`：≥8
- 接入：web Soft／Mock only；閘未驗唔改 LIVE；本輪唔交 iOS Soft

## 7. 驗收清單

- [ ] 頁眉含 Soft≠PASS 及 qwen3.7-max
- [ ] 玩家面經理人一律「何生」，無「Ho 哥」
- [ ] 玩家可見文案無工程詞
- [ ] castingCta 只 canCast｜cannotCast；board 只 ready｜locked；無第三態 CTA
- [ ] 玩家面／通告卡無條件外試投／灰區遞相文案；條件未合＝暫未能報＋離開
- [ ] 遠觀首輪＝純文字＋音效（唔強制剪影 UI）
- [ ] 紅星遠觀主表剛好 4 人（齊鎮海唔入主表）
- [ ] 玩家面剪影／遠觀描述一律中文書面（如「闊膊深色西裝」），禁外文身形修飾詞
- [ ] Soft hooks ≥8；`hook_ho_advice_soft` 對齊註為「何生條件提醒」
- [ ] 通告語無「報名」「Audition」
- [ ] 日期 2026；無簡體／大陸網文腔

## 8. A/B 決策（已拍板）

1. **紅星遠觀**：**B** 純文字＋音效（出圖後先升剪影）
2. **暫未能報反饋**：**A** shake＋「條件未合」＋業界書面語副行
3. **第五星齊鎮海**：**B** 首輪唔強掛——只留四人；齊鎮海僅 DEV 附錄「後輪可選」

## 9. Out of scope（補）

- 紅星近距離互動留後續
- 鄧線完整劇情：僅 DEV 入口一句
- LIVE 行為閘／tip：本檔唔改
- 多語言、紅星寫實立繪（出圖 HOLD）

## 10. 頁腳

- 日期：2026-11-04（Asia/Hong_Kong）
- 經：qwen3.7-max
- 狀態：Soft≠PASS；閘未驗＝Mock only；唔 tip LIVE；出圖 HOLD；89–92 HOLD；唔交 iOS Soft；已殺條件外試投

### Soft nit 修（同日）
- starId 對齊 LOOKS／era_stars：`liu_bingxing`／`ngai_wingnaam`／`yip_manji`（唔再用 liu_bingsing／ngai_wingnam／yip_manchi）
- 條件未合 Detail：除「暫未能報」外保留 **「離開」**（用戶硬鎖）
- Mock SHA8 `2a531f10`
