# v20a76 — 手帳對比度普查＋修正（CONTRAST76）＋訓練數值統一（UNIFY76）

用戶 2026-11-10 17:02 實玩反映：v72 修咗子頁掣 active＋toast 灰帶兩處之後，
手帳入面依然有字體顏色問題（冇指明邊頁）。方針：唔再逐處補鑊，做全手帳
普查一次修清。同包追加 UNIFY76（用戶 17:28 拍板）。

## 一、CONTRAST76 普查方法（量度證據，唔靠肉眼）

- Playwright 駕駛（槽 3、420px、本地鏡像 sha 核對），逐一開手帳全部畫面：
  五大類 × 全部子頁（行程／進度、作品／獎項／回憶、記數／標籤(dev-gated)／
  庫存、傳聞／剪報、人情債／人脈）、行程頁 browse／soft／可編輯／逐日編輯
  四態、課程選擇器（演技組＋外貌組）、進度頁 fresh＋中段混合態、回憶錯過態
  （calib60Missed 植入）、手帳頂 header，共 23 個畫面。
- 每畫面掃晒 #v-home 內有直接文字嘅可見元素：computed color（fill 優先）×
  有效底色（祖先鏈 premultiplied source-over 合成，連 group opacity 累乘，
  底層頁面白）→ WCAG 對比度。門檻：一般文字 4.5、大字 3.0。
- 圖底元素（漸變／紙紋）computed 量度會穿底誤報，另用截圖像素主色抽樣
  定案（pixels76.py）。

## 二、修復清單（全部只改文字顏色；冇郁底色／版面／字體／行為）

根因：(A) 有啲 pane 冇紙底、內容直接坐 #v-home 深色漸變，但沿用紙面墨色；
(B) 米紙底上嘅次要文字（#8a755a 家族）跌穿 4.5；(C) 金錢晶片金字唔夠亮。

| # | 畫面／元素 | 修前 | 修後 | 改法 |
|---|---|---|---|---|
| 1 | 進度頁 h3.prog71-h「主線進度」 | 1.14 | 10.78 | #43301c → #ecdfc2 |
| 2 | 進度頁 p.prog71-intro | 3.24 | 6.76 | #8a755a → #c3b096 |
| 3 | 作品／庫存／人脈 h3.jobs72-h | 1.14 | 10.78 | #43301c → #ecdfc2 |
| 4 | 作品牆／回憶 h3（empty＋head） | 1.20 | 10.78 | var(--navy) → #ecdfc2 |
| 5 | 人情債 p.pane-intro | 1.24 | 8.06 | #5a4328 → #e6d7ae（v48 明文留低嗰頁，今次補返） |
| 6 | 記數簿 p.ledger-enroll | 1.99 | 6.76 | var(--muted) → #c3b096 |
| 7 | 人脈 p.people-next＋div.people-next | 1.99 | 6.76 | var(--muted) → #c3b096 |
| 8 | 拍攝簿條目 .req（標題行／副行） | 2.49 | 10.89／7.14 | 容器 #d9c9a3；inline var(--muted) ×4 → #b3a284 |
| 9 | 行程 span.plan-hint（各態） | 2.89 | 5.08 | #8a7355 → #59452a（連其 opacity .85 合成後） |
| 10 | .act-item .ah（可編輯態） | 3.64 | 7.34 | #8a7355 → #59452a |
| 11 | 手帳頂 span.hs-i.home-money | 3.93 | 5.63 | #C9A227 → #e3c565（:not 排除 warn/critical/broke 狀態色） |
| 12 | picker .t70-cell span「增益」等格標籤 | 3.98 | 6.31 | #8a755a → #6b5636 |
| 13 | picker p.guide68-note | 4.16 | 6.59 | #8a755a → #6b5636 |
| 14 | 行程壓力 b.good | 4.42 | 5.64 | #1f7a5c → #19684d（限 #v-home 作用域） |

落點：主 CSS 尾一個 `v20a76 CONTRAST76` block（作用域規則＋註解）＋
jobs72SectionHtml 四處 inline 色。CSS 大括號平衡由 polish48 測試覆蓋。

## 三、判斷清單（故意淡化，保留＋保 ≥3:1 地板，逐項交代）

| 項目 | 修前→修後 | 理由 |
|---|---|---|
| 進度頁 far/missed 行（opacity .62）：act 3.59／note 3.98／未開放標籤 4.21 | 不變 | 未達幕嘅深度提示，同已開放行（全對比）層次分明；全部 ≥3 |
| 唯讀詳細卡 .act-item:disabled（opacity .55）：.at 3.39／.ah 1.89→3.58 | .ah 額外加深 #241a10 | disabled 唯讀回顯；同一資訊喺週行有全對比版；.ah 改色後過 3 地板 |
| 確定掣 .is-locked（opacity .72）3.82 | 不變 | disabled 掣語義淡化，≥3 |
| 傳聞頁 .weak-whisper（opacity .45 鬼影字）1.31→3.16 | 色提亮 #e0d3ac，opacity 保留 | 耳語氛圍字；opacity 所限純色上限 ≈4.3，提色後過 3 地板 |
| 季節印章 span.season-mark「冬」（opacity .35）1.68 | 不變 | 裝飾水印字，唔係內容文字；opacity .35 下純色數學上限 ≈2.36，改色到唔到地板；旁邊正文（又過一季…）合格 |
| span.ai 🗺️ emoji 3.39 | 不變 | emoji 字形由彩色 emoji 字體渲染，computed color 唔驅動其外觀，唔屬文字對比 |

## 四、像素核實假陽性（computed 穿圖底誤報，唔使修）

- 確定掣（金漸變）：主色 (225,201,143)，字 #1a1410 比值 11.25（較深一簇 8.2）。
- 剪報空狀態紙卡：h4 15.33、clip-date 6.41（紙紋圖底）。
- 回憶條目卡 mem-item60（紙漸變）：標題 14.89、日期 6.66。
- 標籤頁係 dev-gated（?devTags=1／localStorage），玩家版面唔出現；
  dev 態量度除金錢晶片外全合格。

## 五、UNIFY76 — 訓練三課數值統一（用戶 2026-11-10 17:28 拍板）

v75 偏差（外貌／魅力／智商一級 +3~5 起步）推翻，TRAIN75_SPEC 三課改到
同其餘四課一致：主增益 +4~6／+6~8／+8~11、壓力 +8~12／+10~14／+12~16。
附帶唔郁（外貌→魅力、智商→演技 +1/+2/+3；魅力冇附帶；外貌學費 $800 不變）；
其餘四課、級別衍生（5 堂一級）、遷移冇掂。

- train_looks：mLo 3→4、sLo 6→8、sSpan 3→4
- train_charm：mLo 3→4、sLo 5→8、sSpan 3→4
- train_iq：mLo 3→4、sLo 4→8、sSpan 2→4

測試跟改（原位註明 v76 拍板）：test_levels75_logic（EXPECT 表）、
test_ux68_logic（iq/looks 兩斷言）、test_fix65_static（入水斷言）、
NOTES_V20A75_LEVELS 對照表加 supersede 註記。test_polish48_static 嘅
「debt pane intro not restyled」斷言同理由 CONTRAST76 第 5 項 supersede 改版。
實駕：picker 外貌卡面（一級增益 +4~6／壓力 +8~12）✓；外貌地點即時上堂
looks 10→16（Δ=6 入帶）、學費 −$800 ✓（修前修後各跑一次）。

## 六、驗證

- 普查修後重掃（同一套量度）：非判斷清單項全過門檻；判斷清單項全 ≥3
  （season-mark 裝飾豁免除外，理由見上）；全程零 pageerror。
- 測試 83/83（82 基線＋新增 test_contrast76_static）；新／改版斷言對
  v75 index 全部 FAIL（反證：contrast 16 項、levels75 19 項、ux68 3 項）。
- v75 存檔相容抽驗 ✓（槽 3 植入舊檔，到地圖＋開手帳＋零 pageerror）。
- 紅線冇郁：SAVE key `starVolunteer_map_v19w`／softRev `s107`／`?v=v20a10`。

## 七、附帶觀察（唔喺今包範圍，冇郁）

- 本地鏡像有幾個資產 404（assets/ui-physical/map-frame/map_pin.png、
  toast/ticket_stub.png、fx/awei-rest-sleep.mp4）——傳聞頁情報拼圖相片
  位喺本地鏡像顯示破圖；serve 鏡像資產目錄同 repo 是否一致待查，
  線上版未見用戶報告，先記低。

（部署重觸發：PR #176 合併後 Pages 未更新，細 commit 直推 main 重觸發。）
（部署重觸發二：合併後逾 20 分鐘 Pages 仍未更新，再推一程。）
