# v381 情報站補位試鏡＋屋企留話簿

用戶 2026-11-22 拍板「按建議次序開票」第一票（偏弱系統加強①，方案來源 `linji-systems-balance-2026-11-22/REPORT.md`）。原則：唔開新玩法、唔買分、唔改試鏡判定／頒獎／結局；情報站賣時間同機會，屋企畀「返屋企先有」嘅嘢。唔郁贏線 0.875／E1 門檻 350／floor 140／warnLine 180。

## 前提核實（brief 與 live 對唔上，已按 live 實裝）

brief 講「情報站《星夜迷離》live $60–75、開閘陸好感 ≥25」。對 live code 核實：

- 《星夜迷離》係通告 `gig_1991_tv_203`（陸柏言替工電視通告），唔係情報站名稱。
- live「情報站」係 v267 打聽系統（MOCK_ASK @ 金龍茶餐廳 cafe_cha／何生事務所 agency_ho，S.intelAsked 記錄）。
- 故實裝按打聽系統做：茶餐廳打聽行動新增「打聽補位消息」，價格沿用 $60–75 帶（按月定死），開閘陸柏言好感 ≥25（`enc79StarState("luk_baakyin").fav`）。

## 功能

### 情報站補位試鏡（茶餐廳）

- 新打聽行動 `act_cha_intel381`「打聽補位消息」：向陸柏言買傳聞，每月只可買一次。
- 名額池：由當年 GIGS 揀一張未消費、無 trigger、級別貼近玩家級數（enc79PlayerTier 0–3 → gig tier 窗 [pt, pt+1]）嘅真通告；月份種子定死一張，讀檔唔重擲。唔加新通告、唔改庫總數 330。
- 價格：按月 $60–75（`60+(mk*7)%16`，mk＝月份鍵）。買情報計茶座每日上限（softSocialDailyCap("tea")）。
- 買後彈窗「收到補位消息」：講明傳呼留言已留喺家中電話，要返屋企睇留話簿、5 日內覆電。
- 確認頁專屬文案：「即時支付情報費 $X」。

### 屋企留話簿＋覆 Call 機

- 屋企手帳（home265 列，衣櫃掣右側）加「留話簿」掣 `#btn-intel381`；有未覆留言時露出紙角「新留言」。
- 留話簿 modal 欄位：留言日期／留言人（場務，經陸柏言介紹）／留言內容（《片名》有演員移民，劇組正安排補位試鏡）／試鏡地點／覆電限期（實際日期）。主掣「覆電保留資格」、次掣「稍後覆電」；失效蓋「已失效」印。
- 覆電後通告喺指定地點通告欄以「補位」標籤上板（豁免季節／NAT92 錯峰），試鏡照常 aud91 判定。
- 到期：留言 5 日唔覆失效；覆電後 7 日唔試鏡失效（advanceDay `intel381Tick`）；已試鏡／已開拍轉 used。

### 狀態

- `S.intel381` 單槽 {mk, gigId, locId, title, state, msgDay, keptDay, price}；normalizeSaveObj 補 `o.intel381=null`，舊存檔兼容。唔改 SAVE key／softRev／產品 ?v=。

### UI（GPT-6.2-sol 規格，原稿 `linji-drive381/gpt_ui381.txt`）

- 掣名「打聽補位消息」；「補位」標籤淡赭紙底深墨字，沿用邀約／引薦標籤位；留話簿未讀紙角；失效印。方向二「紙本手帳 · 實物劇組」，brief 寫明終極目標原生 iOS app。

## 編輯點（index.html，淨 +164 行，48856→49020）

- CSS：.intel381-corner／.intel381-book／.intel381-stamp／標籤色（~4212）。
- home265-row 加 `#btn-intel381`；wireHome265 接線。
- normalizeSaveObj 補 `o.intel381=null`。
- MOCK_ASK.cafe_cha 加 `act_cha_intel381` def；mockAskDefs 按 intel381Available() 過濾＋動態 moneyCost/cost；applyMockAsk 加 intel381Buy 分支；render cost236 專屬「情報費」文案。
- advanceDay 加 intel381Tick；gigsForLocSeasonBoard 加 isIntel381 豁免；兩處卡標籤（gigCardHtml trigBit、gigBoardTeaserHtml trigPill）。
- INTEL381 模組（intel381MonthKey/Price/Slot/LukFav/Available/PickGig/Buy/Tick/KeptGig/Label/FmtDay/LocName/Reply/OpenBook）插喺 ENC79 模組完之後。

## Resync

- `qa381/resync381.py`（difflib old→new 單次掃描 dict 查表；old 備份 /tmp/index_v380.html，linemap /tmp/linemap381.json）。
- 修 8 檔：travel114（4 位數行號需 \d{4,5}）、gift185、rom159、rom176、tang152、tang171、tang173、text125；openLoc DEF 44018→44180；總行數 pin 48856→49020（鏈 append「＋v381 +164」）。
- suite 第一跑 392/17 → resync 後 8 個新 FAIL 逐個直接跑 PASS → 全套重跑 400/9（基線，九項 pre-existing 不變）。

## 實駕驗證（Playwright，證據 `linji-drive381/`）

- `probe381b.py`（DOM 版；主 script 封裝，函數唔係 global，改全程撳 UI）：種子存檔預設陸好感 30 → 茶餐廳「打聽補位消息」→ 確認頁「即時支付情報費 $68」→ 扣 $68、slot msg（gig_1990_tv_104《老闆有計》男配角 @ 九龍電視台）→ 屋企留話簿掣＋未讀紙角 → 留話簿 modal 欄位齊（留言日期 1990年1月1日、覆電限期 1990年1月6日）→ 覆電 → kept → 九龍電視台通告欄見「補位」標籤卡。
- 到期：種子 keptDay=-8 → 過一日 → day 1、state expired（`/tmp/dbg381e.py` 流程，結果記於此）。
- 截圖：probe381_confirm.png／probe381_bought.png／probe381_book.png／probe381_board.png／probe381_home.png；數據 probe381b.json。
