# v20a362 — UI 四屏改善（實玩評估 P1）

用戶 2026-11-21 拍板開票。原則：先減撳、再加動畫。唔改平衡數值、SAVE key、softRev、產品 `?v=`；玩家面新字香港書面語；年份 source 冇手改。

## 1. HUD（地圖頂欄雙軌）
- 第二行（聲望／年份／信用）由 .56rem（8.96px）升 .78rem（12.48px），數值 .98rem（15.68px）；壓力標籤 .78rem、壓力值加「/100」標示；錢 .98rem（15.68px）。
- 數值變化浮字：`hudFloat362` 接 paintBar／refreshMoneyHud，聲望／信用／錢／壓力有變嗰陣喺數字旁浮 +N／−N（1.1 秒淡出，唔阻操作）。

## 2. 行程手帳 planner
- 刪逐行「⧉ 複製」（7 粒 45×21 細目標，與「複製到…」批次功能重疊；`openCopyFromDay` 函數保留）。
- 觸控區全升 ≥44px：day-row 34→48px、home-tab 32→44px、subtab 23→44px、壓力估行 33→44px。
- 像素貼紙：day row 用真資產 fx 片做貼紙（`nbStickerKind362`／`nbStickerHtml362`，映射 shoot:→fx_shoot、job:/audition:→fx_audition、train_*→fx_train_a/b/c、rest/home_chore→fx_rest，其餘保留 icon）。
- 「確定本週行程」加大（54px）＋蓋章入場動畫；衣櫃／瞓覺掣換紙標籤底。
- 量度：可撳目標 36→29、細目標（<44px）22→0。

## 3. 故事播放
- 「跳至選項」開放畀所有故事（連強制主線；之前 `spIsForcedStory` 閘住）——快進只跳對白，抉擇＋reconfirm 照舊。
- 自動播放開關（打字完停 1.2 秒自動下一句，入抉擇自動停）。
- 對白模式撳舞台任何位置＝下一句（唔使追細字連結掣）。
- 段落進度 chip（第 X／Y 句）。
- 對話框紙底＋微傾＋膠紙條（方向二便條紙）；講者名手寫字體棧（LXGW WenKai→Kaiti TC→KaiTi→Noto Serif CJK TC，唔載 webfont）；講者換人全身圖淡入。
- 量度：到抉擇步數 16→1（跳至選項）。

## 4. 結算／日結卡
- 故事結算冇「下一節」嗰陣「關閉」升主掣；雙軌數字滾動（由現值−增量滾到現值）＋增量浮字；結果行逐行淡入。
- 日結 soft 排程日「開始今日行程」role g→p（唯一主行動升主色）。

## 5. 共通動畫（克制，只喺落實決定／睇結果兩刻）
- 全掣按壓反饋（translateY＋scale＋brightness）；modal 滑入；tab 內容淡入；確認掣蓋章；prefers-reduced-motion 停 v362 動畫。
- 之前 UI 層 CSS animation 係 0；而家 planner 屏量到 3 個動畫元素（貼紙浮動）。

## 驗證
- 實駕（Playwright 390×844 dsf2，證據 `~/workspace/linji-drive362/`）：四屏修前／修後截圖＋量度對照；自動播放實測 8 秒推進 3 段；撳舞台推進實測；HUD 浮字實測（+7）；晨鏈／手帳確定／故事兩步抉擇／結算撳走／過一日／日結卡全部行得通，零 page error。
- suite：**400 PASS／9 FAIL**，同 v361 基線一致（九項 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。
- 測試 resync（index.html 淨 +267 行，47161→47428）：rom159／rom176／text125／gift185／tang171／tang173／tang152／travel114 釘行按內容實量／difflib 映射重寫；book143／ui108 改「逐行複製已刪」斷言；dayend189／dayflow196 改 role p 斷言；verify37 抽取清單加 nbSticker 兩函數。
- 未做（等拍板）：P2 平衡（試鏡曲線／經濟／系統回饋黑箱）同 P3 未開票，今票冇郁任何數值。
