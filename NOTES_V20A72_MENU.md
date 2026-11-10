# NOTES V20A72 — 主選單整合（一門原則）

用戶 2026-11-10 12:54 拍板：主選單（☰）14 項平列太亂，三類嘢（資訊頁／遊戲
動作／系統功能）溝埋一級；傳聞、人情債同手帳頁完全重複；狀態 vs 記數、
拍攝簿 vs 作品係易混名對。原則＝「一門」：選單只留動作＋手帳一個資訊入口
＋系統組，資訊頁全數歸入手帳五大類，內容唔刪只搬位。

## 選單（#menu）
- 新清單（順序）：劇情（story-play，徽章邏輯原封）／手帳（journal，文案
  「返手帳」→「手帳」）／提早休息・+1日（rest-early，行為不變）／
  `.menu-sep` 分隔線／重看教學／設定／接線・年份（wire 隱藏項保留）／
  存檔／讀檔／新遊戲。
- 刪除入口：狀態 stats、人脈 people、庫存 inv、拍攝簿 jobs、傳聞 rumors、
  人情債 debts。handler 對應六個分支一併移除（冇 orphan）；其餘分支不變。

## 資訊頁歸位（手帳五大類）
- 狀態 → 記數頁：查證 showStats 自 v20a6 起已重定向去手帳「記數」頁，
  同 ledgerStatsHtml 同一渲染，根本冇獨立「狀態」內容——本包只刪選單
  重複入口，showStats 保留做舊呼叫（StoryPlay.openLedger 等）重定向。
  記數頁頂部本來就係狀態摘要（日期＋雙軌＋數值格＋存款＋已報名），
  符合「狀態內容置頂」。
- 拍攝簿 → 事業組「作品」頁頂部：新 jobs72SectionHtml() 由原 showJobs
  modal 內容原封改成頁面段（拍攝中／已獲聘、待試鏡、已殺青履歷三段，
  gigCardHtml 渲染待試鏡卡不變）；導航掣改頁內掣 jobs72-goboard（空態
  「去通告欄」）／jobs72-goloc（「去相關地點」），跳轉邏輯抽出
  jobs72GoBoard()／jobs72GoLoc() 同舊版逐字一致（撳掣時重算狀態）。
  renderWorksPane 改為 jobs72SectionHtml() ＋ worksWallHtml59()。
  重複處理：簿同牆同源 wrapHistory——簿係全量文字履歷（連散工殺青＋
  評價／片酬，牆冇呢啲欄），牆只收有名製作連海報；兩者分段保留，
  唔合併刪減（判斷決定，報告有列明）。
- 人脈 → 人情組新子頁 people：人情組加分段列（人情債／人脈，
  data-hsubgroup="favor"，預設 debt）；people72Html() 由原 modal 內容
  改成頁面版（NPC 列／好感心／解鎖階梯提示／「去找」掣全保留），
  「去找」跳轉抽出 people72GoLoc()，renderPeoplePane 渲染後綁掣。
- 庫存 → 近況組新子頁 inv（記數／標籤／庫存）：inv72Html() 由原 modal
  內容改成頁面版（存款行／物品列／送禮提示不變）；空庫存「去香江唱片
  小賣」掣改頁內掣 inv72-goshop，跳轉抽出 inv72GoShop()。
- 接線：BOOK70_TAB_GROUP 加 people:"favor"、inv:"status"；
  book70GroupSub 加 favor:"debt"；setHomeTab allow／pane 列／渲染分派
  加 people、inv。新 pane：#home-pane-people（#people-list）、
  #home-pane-inv（#inv-list）；新子掣 #htab-people、#htab-inv。
  CSS 新增 .menu-sep／.pane-go72／.jobs72-h／.jobs72-sec（.jobs72-sec 預留）。

## 舊呼叫重定向（跟 showStats／v70 guide 先例）
- showJobs() → kick 檢查後 enterHome 事業組 works 頁。舊呼叫點：
  通告詳情 modal「查看檔期／拍攝簿」（1 處）、地點動作「查看檔期」
  （addLocGigActs 2 處）——全部自動落新位，掣文案唔使改（拍攝簿段
  喺作品頁頂，名稱仍然成立）。
- showPeople()／showInventory() → 同式重定向去 people／inv 子頁；
  除已刪嘅選單分支外冇其他舊呼叫點（全域掃過）。
- 選單 rumors／debts 分支刪除後，傳聞／人情債入口淨返手帳消息組／
  人情組（本來就係同一頁）；其他 setHomeTab("rumor"/"debt") 呼叫
  （地圖提示等）不受影響。

## 紀律
冇改 SAVE key（starVolunteer_map_v19w）／softRev（s107）／產品 ?v=
（v20a10）；冇改 content pack JSON；冇改任何數值／門檻／判定。
玩家面冇 1988／1989 字樣、冇真藝名、關海媚冇出名。

## 外觀修正（用戶 2026-11-10 14:46 睇 v71 截圖追加，同包出）
1. 子頁掣 active 文字隱形：#home-subtabs .home-tab（ID 特異性）蓋走
   .home-tab.on 嘅啡底，但冇規則管文字色，.on 嘅 #fff8e8 白字落
   #fbf3df 淺底＝隱形（五組共用同一 class，全中招；實測計算色證實）。
   修：明文加 #home-subtabs .home-tab.on{ background:#6b4e2e;
   color:#fff8e8; border-color:#4a351e; }，同大類 tab／分類 tab／
   picker chips 嘅 active 語言一致。picker chips 實測原本已正常
   （.guide68-chip.on 成套色喺同一規則），冇郁，駕駛加防回歸斷言。
2. 底部掣俾灰帶罩：真身係 #app.toast-up::after——v17g 遺留嘅 88px
   半透明暗影 slab（rgba(18,22,32,.55)、z510），本意喺地圖 toast
   嗰陣遮地圖提示；地圖側早已用 :has(#v-map.view.on) 隱藏，但手帳
   view 未跟，toast 一出就罩住還原／確定／返回地圖成 2 秒，睇落似
   disabled。修：跟地圖先例加 #app.toast-up:has(#v-home.view.on)
   ::after{ display:none !important; }。toast 票根本身唔受影響。
   兩項都只改呈現，冇郁版面結構同行為。

## 測試
- 基線 76/76 唔跌；test_book70_static.py 三處斷言原位改版（近況組分段
  加庫存、人情組分段新斷言、pane／映射數目 9→11），全部註明 v72 原因。
- 新增 test_menu72_static.py＋test_menu72_logic.js：新清單精確比對、
  handler 冇 orphan、子頁接線、產生器三態／兩態內容、重定向落點、
  外觀兩修嘅 CSS 規則；對 v71 index 行會 FAIL（反證已驗）。
