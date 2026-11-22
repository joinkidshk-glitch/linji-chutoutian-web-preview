# v20a378 第三輪評估第三波（P2 批次＋覆核）

基線：v377（main `990bcf6`，suite 400/9）。第三波後 suite 400/9（九項 pre-existing 不變：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。index.html 淨 +134 行（48639→48773），十項釘 resync（gift185／p361／rom159_static／rom176_static／tang152／tang167／tang171／tang173／text125／travel114，difflib 逐行核實內容逐字相同）。

## B5 首年緩衝引導（唔派錢，只做引導）
破產率實證 0–1%，唔加現金緩衝。試鏡完成 modal＋「等消息」詳情加並行提示：「等消息嘅日子可以照常試其他通告（最多同時等 3 張）或者做兼職，唔使空等。」（AUD91_CAP 動態帶入。）

## B6 ID／E4 入口反向養成
### ID
- 判定次序：ID 移後到 E3／E5 之後（E1→E4→SS→FK→TK→SK→GH→CK→AK→E3→E5→ID→CR→E2→E0）。舊次序 ID 排先，fame 60–70／credit 50–60 段有幕後／人情證據都俾 ID 截走。
- 信用窗：固定 30–60 → 30–max(60, fame×0.9)（聲望主導帶）。自然信用 = round(fame×0.5＋stage×0.3＋acting×0.2)＋delta，fame 80–110 時 70–95，舊窗要刻意壓信用先入到。人氣型 profile 信用 ≈ 聲望×0.82–0.86，平衡 profile ≈ ×0.99–1.03，0.9 分得開。

| profile | fame | stage | acting | delta | credit | 舊窗（≤60） | 新窗（≤max(60,fame×0.9)） |
|---|---|---|---|---|---|---|---|
| 人氣型 A | 80 | 35 | 30 | +12 | 69 | ✗ | ✓ ID（≤72） |
| 人氣型 B | 100 | 45 | 35 | +15 | 86 | ✗ | ✓ ID（≤90） |
| 人氣型 C | 120 | 55 | 40 | +18 | 103 | ✗ | ✓ ID（≤108） |
| 平衡 A | 80 | 65 | 55 | +12 | 83 | ✗ | ✗ → E2 |
| 平衡 B | 100 | 80 | 70 | +15 | 103 | ✗ | ✗ → E2 |

weave410_logic 三案（fame 70／credit 61）由 E2 改落 ID，測試期望同步改（E1 擋下／E6 唔自觸發意圖不變）。
### E4
入口 fame≥50＋credit<30 不變。新增信用負向來源：逾期掉單（failShootOverdue）扣業內信用 −3（一般）／−5（high），經 industryCreditDelta，取消卡出「業內信用 −N」行。例：fame 60／stage 30／acting 25 → base 44，5 次一般逾期（−15）→ 29 <30 入 E4——「紅咗但成日甩通告」有路可循，唔使刻意壓數。贏線 0.875／floor 140／warnLine 180 不變。

## B8 聲望衰減交代（核實：冇被動衰減）
W1 見到嘅 −8/週係逾期掉單罰則（failShootOverdue fame −8/−12），唔係自然衰減。settleWeek 加限期交代：尚欠日數多過限期前可拍日子（或限期 ≤3 日仍未拍完）出紅字 flavor 行，講明逾期會取消檔期、扣違約金同聲望。

## B11 檔期衝突警告覆核（核實：接通告嗰刻冇警告）
新增 aud378ScheduleRisk(gig)：按限期由近至遠累計尚欠拍攝日 vs 限期前可拍日子（各拍攝可拍星期聯集），唔夠就喺通告詳情頁出警告（唔阻止）。實駕驗證：手頭尚欠 10 日／限期 3 日 → 「檔期可能撞期：計埋手頭拍攝，限期前要拍 10 日，可拍日子得 3 日——逾期會取消檔期、扣違約金同聲望。」

## B12 約會 rel 上限＋送禮面板落數
- bumpRel 加上限 clamp 7（設計尺度：rel 5 鎖、rel 6 commit、滿 7；負值照舊）。舊制無上限，純約會刷到 32。
- giveGift：before 改 bump 前擷取，回傳 delta 改實際落數（after−before），週軟頂計數跟實際落數。
- 約會結果顯示改實際落數（撞頂唔再假報 +1）。
- Playwright 實駕（GiftShop.giveGift）：最愛 0→3（delta 3）；6→7（delta 1）；7→7（delta 0）；relFinal 7。

## U6 UI 殘餘（GPT-6.2-sol 諮詢，原稿 linji-drive378/gpt_ui_reply_raw.txt）
- 通告欄重疊：教學態非教學 modal 改底部對齊＋max-height 78dvh（教學卡版面不變）。實駕量度：tut-on modalTop 170px > HUD bottom 84px，maxH 658px。
- 詳情成功率：摘要錢行之後加成功率行（同一支 chance()，只喺 ready 出）。實駕：「試鏡成功率 約 46%」。
- pin 輕跳：一般 pin 加按壓回饋（:active 下沉 1px＋縮 0.95＋內陰影，120ms，唔用光暈；prefers-reduced-motion 停用）。

## U7 衣櫃掣
.wardrobe265-row button min-height 36→44px。實駕 computed 44px。

## U8 操作摩擦
巧遇對白加「跳至選項」掣：沿途每步 segFx 照行，跳到下一個抉擇步停低（冇抉擇步唔出掣）。故事跳轉／日結加速／預設計劃經核實已存在，記錄為已驗證。

## U10 徐先遇後約
rom159DateGate 改必須行完故事初遇節點（六線一致），傾過偈唔再解鎖約會。reason：「要先喺劇情入面正式見過面，先約得出街。」實駕 sheet 已見新文案。rom159_logic F 段測試同步改（預設六線 meet 已做）。

## U11 人情 status
- 債權卡 status：已兌現優先過絕響（芬姐兌現後唔再顯示「絕響」蓋過「已兌現」；「人已不在香港」照出）。
- creditRedeemLine283 加進行中狀態：兌現通告試鏡中／拍攝中，卡面講明「已用於《X》…」。
- favorDueHintText 何生嗰筆加地點「去何生事務所」。

## U12 音樂獎格性別
buildAwardResultPack gallery 兜底 pool 排除性別不符格（AWARDS188_PLAYER_GENDER="m"），唔再抽中女歌手格做「你嗰格」；請柬全 slate 列名不變。

## B10 NOTES 算術＋死項
- NOTES_V20A371 §2「臨記通告期望日均 $75–125」更正：臨記片酬中位 $60／3 日，日均 $15、期望 $10；$300–500 係 film_support_small 帶。
- 刪 ENDING410_T 死欄 e1Fame／e1Credit／e1Dual／e1NegMax（判定只讀 ENDING95_T，從無引用）；weave410 釘字串同步移除。
- tagBonus 保留機制（schema cat_ensemble 有 tagBonusAny 但 mvp:false；production 格無定義，恆 0）——刪 code 會郁 awards62／fix65 邏輯測試期望，唔刪，只交代。

## 驗證
- suite 400/9（基線不變）。
- Playwright 實駕：B11 警告觸發、B12 送禮三段落數、U6 成功率行＋tut-on 量度、U7 44px、U6 pin :active 規則、U10 sheet 文案。證據 linji-drive378/（probe378*.py／.json、probe378_detail.png）。
- 唔改 SAVE key／softRev／產品 ?v=；玩家面文字香港書面語（非對白）。
