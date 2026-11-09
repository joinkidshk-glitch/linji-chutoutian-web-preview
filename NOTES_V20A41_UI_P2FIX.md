# NOTES V20A41 — 新 UI 接入第二期補修（StoryPlay 全屏分層版面）

性質：soft 預覽版面修復。**純 CSS 改動**：只喺主 `<style>` 段尾（二期 v20a40 皮膚層之後）加一段「v20a41 皮膚層」，零模板改動、零 JS 改動、冇新素材。唔改 SAVE key（starVolunteer_map_v19w）、softRev（s107）、產品 ?v=（v20a10）；唔改 content pack；唔改 StoryPlay 對話邏輯／劇情數據。一期（HUD/地圖/通告卡）同二期（素材內嵌/hooks/米紙牌膚）規則冇郁。

## 問題（實機驗收發現）

二期素材接通咗，但版面仍係舊骨架：StoryPlay 喺 modal 入面，`.sp-stage` 只係 modal 內一條橫幅（max-height 42dvh），企立圖置中偏大，未達用戶定調嘅《明星志願》式全屏分層（場景全屏做底＋企立企左下＋對話牌壓底）。

## 突破容器嘅方法（研究結論）

DOM 鏈：`#app > #mask.mask > .modal#modal > #modal-inner > .story-play`（另 `#modal-btns` 係 .modal 內第二個子元素）。

- `#mask` 本身 `position:absolute; inset:0`（#app 直接子元素，HTMLParser 核實），已經覆蓋成個遊戲框（手機直向／桌面手機框皆然）。
- 祖先鏈 `#app`／`.modal`／`#modal-inner` 全部冇 `transform`／`filter`／`backdrop-filter`／`will-change`——即係連 `position:fixed` 都唔會失效；但 fixed 會以瀏覽器 viewport 為準，桌面版會逃出手機框，所以**唔用 fixed**，改為喺 `#mask.story-play-on` 作用域內將 `.modal` 拉到 `height:100%`、去邊框/圓角/底色/內距，`.sp-stage` 改 `position:absolute; inset:0` 做全屏底層——效果等同框內全屏，且流式佈局不變。
- 作用域安全：`story-play-on` 只喺對白／選項播放期間由 render()/setStoryPlayLock 加上；`showResult` 結算畫面會主動移除佢（行 21190 起核實），事態列表（.story-picker）modal 唔帶呢個 class——兩者版面零影響。
- 功能按鈕事實更正：模板內 `.sp-actions`（下一句/跳至選項）自 v19z24 起被硬隱藏（CSS `display:none !important`＋JS 再 set inline none），真正 CTA 全部喺 `#modal-btns`；選項模式下真正可撳嘅選項掣亦喺 `#modal-btns`（模板內 `.sp-choices` 係 pointer-events:none 嘅視覺紙條，負責顯示 notes/預覽）。本期按鈕處理對象係 `#modal-btns`。

## 逐項版面改動（全部喺 v20a41 皮膚層，作用域 `#mask.story-play-on`）

1. **容器全屏**：`#mask.story-play-on{padding:0;align-items:stretch}`；`.modal{position:relative;height:100%;max-height:none!important;border:0!important;border-radius:0;background:transparent!important;box-shadow:none!important;padding:0}`（覆蓋 v17w 嘅米色板＋金框 !important 規則，同 specificity 靠段尾位置取勝＋逐項 !important）；`#modal-inner{overflow:hidden!important}`。
2. **主根**：`.story-play{position:relative;height:100%;max-height:none;gap:0}`（解除 58–72dvh 高度帽）。
3. **標題收做頂部半透明條**：`.sp-head` 改 absolute top overlay（z 6、pointer-events:none）：深色漸變（.58→0）、meta 同標題同行細字、`.sp-setting` 半透明底＋最多 2 行截斷、進度細字同行——唔再佔版面、唔遮場景主體。
4. **舞台全屏**：`.sp-stage{position:absolute;inset:0;border:0;border-radius:0;max-height:none}`；`.sp-bg-layer`（原有 absolute inset:0＋cover 機制）即成全屏場景底；`.sp-stage-inner{height:100%;padding-bottom:66px+safe-area}` 畀底部按鈕 overlay 留位。
5. **企立圖**：`.sp-bust.sp-bust-stand` 高改 70%（任務規格 62–72% 內；內嵌圖源高 500px，喺約 700px 高舞台顯示約 490px，近原尺寸唔使點放大）、貼左下、max-width 58%、加 `drop-shadow(3px 5px 9px rgba(0,0,0,.45))`。情緒 filter（tense/angry/warm/tired/smirk/calm 等）逐組鏡像補回 drop-shadow 前綴，唔會被新 filter 蓋走二期情緒色調。
6. **對話牌壓底**：沿用二期米紙金邊膚；企立圖喺牌後面（原有 z 序不變），牌不透明米紙遮住人物下段＝VN 構圖；加安全閥 `.sp-plate{max-height:56%;overflow-y:auto}` 防極長對白裁字。旁白模式維持全屏空景＋中央牌（`.sp-plate-center` max-width 88%）。
7. **選擇畫面全屏分層**：`.sp-stage.sp-mode-choices` 同樣 absolute 全屏（解除 24dvh 矮帽）；`.sp-choices` 紙條 `margin-top:auto` 釘喺下半部（z 4、紙條加投影）；功能選項掣（#modal-btns）保留流程底欄（深啡底＋金線頂邊），同紙條上下呼應、唔疊住紙條文字。
8. **功能按鈕跟牌底**：對白／旁白模式下 `#modal-btns` 改 absolute bottom overlay（z 8、深色漸變 0→.72、無邊線），貼住對話牌底邊嗰帶；用 `:has(.sp-mode-dialogue/.sp-mode-narration)` 區分模式。`:has` 唔支援嘅舊瀏覽器安全退回第 7 點嘅底欄模式（場景仍全屏，只係掣喺欄入面）——同二期 `:has()` 既定取捨一致。

## 未覆蓋企立角色嘅呈現處理

行舊 bust 鏈嘅 17 位角色（img.sp-bust 無 stand class）同剪影（.sp-bust-sil）：唔參與企立全高呈現，維持原 bust 框（38%/max 148px、3:4、金邊圓角，**冇拉伸冇變形**），喺新版面入面以流程內元素企喺舞台左下、對話牌左邊（stage-inner 原有 flex 底對齊），只加一層較深投影（`box-shadow:0 6px 18px rgba(0,0,0,.4)`）令佢喺全屏場景上企得穩。視覺上係「頭像牌企左下＋對話牌喺右」嘅合理退階，同有企立角色嘅全屏構圖唔打架。

## 已知限制

- 舞台全屏後，舊 bust／場景漸變底（冇相片嘅 bg key）會成全屏漸變——屬原有佔位機制範圍，唔係本期新增問題。
- `:has()` 依賴（按鈕 overlay 模式）同二期同一取捨；唔支援時退回底欄，功能無損。
- 企立圖只有 default 表情（二期已申報），本期冇變。

## 驗證結果（工作副本 ~/workspace/linji-work41）

- 改動範圍：index.html 只加一段 CSS（v20a41 皮膚層，約 95 行）；逐行差異核對確認冇其他改動。
- `node --check`：全檔 2 個 script 段抽出逐個驗（見下「驗證實測」）。
- repo tests 全套、二期 hook 測試、紅線 grep：見下「驗證實測」。
- 檔大小：4,184,081 → 見下（純 CSS，增量約 +5KB 內）。

## 驗證實測

- `node --check`：全檔 2 個 script 段抽出逐個驗，syntax OK。
- **repo tests 全套：30/30 PASS**（16 node 邏輯＋14 python 靜態，喺副本根目錄以 `python3 test_x.py index.html` 行；同 v20a40 基線一致）。
- **二期 hook 測試重行：15/15 PASS**（喺今期 index 抽真函數 `spBustUrl`/`spBustIsStand40`/`spBgImageCandidates`＋真常數 `UI40_STAND`/`UI40_SCENE`/`UI40_BG_BY_KEY` 行 node：awi/ho_sang/luk_baakyin 命中企立、awi smile 表情 fallback 企立、so_jiyan/liu_bingxing/ngai_wingnaam/yip_manji/gao_wenhan 行舊鏈、企立覆蓋＝10/場景＝5、cafe/c1_tea 首位內嵌＋保留檔案 fallback、tvb_kowloon 行檔案鏈、generic_interior 維持空）。今期 JS 零改動（逐行 diff 已證），此項屬防腐核對。
- 紅線 grep：`const SAVE = "starVolunteer_map_v19w"`（行 4261）、`softRev=s107`、`version: "v20a10"` 全部在位冇變。
- 新 CSS 段大括號平衡核對：0（平衡）。
- **檔大小：4,184,081 → 4,190,579 bytes（+6,498，全部係 v20a41 CSS 段，冇新素材）**；推送體積同二期同級，唔會再撞 413。
