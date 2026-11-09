# NOTES V20A30 — Weave Phase 4-7：1990 抉擇三連（鏈 F 第 4／5 拍＋鏈 G 第 4 拍）

soft 預覽改動，唔改 SAVE key（starVolunteer_map_v19w）、softRev（s107）、?v=（v20a10）、content pack JSON。
全部新邏輯喺 index.html 內加 `CHOICE47_*` 模組＋`mergeExodusGigs()`，跟 4-6 先例（index 側覆寫／注入，pack 唔郁）。
**原生移植注意：CHOICE47_NODES／CHOICE47_DEFS／EXODUS_GIGS 三張表要一齊搬（同 STORY_SPINE_NODES_1989 一樣係 index 側內容）。**

## 設計總則

三樣都係畀 **4-10 結局系統回收嘅「餌」**：唔即時改結局／數值（空位通告本身嘅正常結算除外）。
兩個微節點經真 `StoryOC.applyChoice` 落旗＋markDone——旗入 `S.story.flags`，同主幹旗網同源。

## 1. 何生「走定留」微節點（鏈 F 第 4 拍）

- 節點 id：`F4_stay_mind`，標題「何生問：走定留」，場地何生事務所。
- **呈現渠道（決定）**：跟 DualMeet／DengLine meet 先例——`openLoc` 行動清單（DualMeet 區塊之後）加一條 `act-priority act-story` offer
  「何生有句說話想同你講」，撳入行真 `StoryPlay.start(node, {force:true})`。
  **唔用隨機對白池**：offer 喺閘開＋未答期間常駐行動清單，保證玩家入事務所就真係俾人問到。
- 時間閘：`choice47SeasonReached(1990, "夏")`——1990 夏起；過季、過年（1991+ 存檔）都仲問得，唔鎖死；1990 前唔出現。
- 文案摘要：1990 年夏，移民顧問公司門口排長龍做背景；何生收工叫阿偉坐低，問「你有冇諗過走？」三個答案：
  留低／有諗過走／未諗過（中性）。何生三個答案都接得住，唔判對錯（規劃原意：無正確答案）。

## 2. 屋企「穩陣工」微節點（鏈 G 第 4 拍）

- 節點 id：`G4_family_job`，標題「屋企有話同你講」，場景屋企飯枱。
- **呈現渠道（決定）**：手帳人情頁 `renderDebtPane`——屋企卡（`debt_family_home`）之後加一張常駐行動卡
  「屋企有話同你講」（`data-choice47-card`），掣 `data-choice47="G4_family_job"` 經該頁既有委派 `box.onclick`
  嘅新分支行真 `choice47Play` → `StoryPlay`；**唔經還款路徑**（分支排喺 `.debt-repay-btn` 查找之前）。
  揀呢個渠道嘅原因：屋企線（鏈 G）嘅玩家接觸面一直係手帳屋企卡（4-3 態度字條、4-4 回音字條都喺嗰度），
  行動卡同屋企卡並排，語境最連貫；唔使新開事件通道，亦唔使靠茶餐廳隨機留言（保證問到）。
- 時間閘：`choice47SeasonReached(1990, "冬")`——1990 冬起，過季唔鎖死。
- 文案摘要：阿媽煲湯等阿偉返嚟食飯，提出表叔喺銀行薦到嘅文職（月月有糧出、年尾雙糧）；
  兩個答案：去見份工／繼續行呢行。阿媽語氣跟鏈 G 文風——實際、唔煽情（「做邊行都好，唔好餓親自己」）。

## 3. 旗名清單（畀 4-10 對照）

| 旗 | 來源 | 結局軸讀法（專檔 §2／§4.2） |
|---|---|---|
| `flag_stay_mind` | F4 揀「留低」 | 去留軸：留 |
| `flag_leave_mind` | F4 揀「有諗過走」 | 去留軸：有離心 |
| `flag_undecided_mind` | F4 揀「未諗過」 | **專旗記低**（唔歸入無旗）：去留軸讀做「被問過但未表態」，同「三旗皆無＝從未被問／未答」分開；4-10 可按中性處理，但唔好當留或走 |
| `flag_family_job_accept` | G4 揀「去見份工」 | E6 退圈入口之一（專檔 §2） |
| `flag_family_job_decline` | G4 揀「繼續行呢行」 | 「主動留低」訊號，同「從未被問」分開 |

- 只寫一次保證：可用性 `choice47Available()` 以「任一答案旗已寫」＋「節點已 done」雙重把關；
  `choice47Play()` 入口再驗可用性先開播，重播／重撳唔會覆寫答案旗。
- 兩個節點嘅 choices **一律零 stats**（只有 flags＋notes）——靜態測試有斷言。
- 新旗經真 `newspaperStoryResolve` 驗證回傳 null：唔會誤生報紙（STORY_FLAG_EVENT 無對照、無模板）。

## 4. 移民潮空位通告（鏈 F 第 5 拍）

`mergeExodusGigs()` 跟 mergeIntelGigs／mergeFavorGigs／mergeRivalGigs 同一條件注入模式，
掛喺 `gigsForLocSeasonBoard` 同一呼叫點（mergeRivalGigs 之後）。閘：`choice47SeasonReached(1990, "秋")`；
閘未開時會主動清走 GIGS 內嘅 exodus id（防舊狀態殘留）。殺青行現有 wrap 路徑（`isGigConsumed` 食
`S.flags["done_"+id]`＋wrapHistory），唔使專屬結算；換年換庫（syncGigsForCalendarYear）唔影響，每次開板重新注入。

| 通告 id | 地點 | 內容 | 定額 |
|---|---|---|---|
| `gig_exodus_tv_senior` | 星河電視台 tvb_longmen | 《燈火人家》資深臨記（連戲位）頂位：原班兩個資深臨記一齊移民，監製話頂到呢個月之後優先留位 | $3,300（pay [3000, 3600]） |
| `gig_exodus_film_hand` | 維港電影 film_harbour | 《江邊小鎮》動作組熟手：武師班底走咗兩個去加拿大，缺熟手頂上 | $2,900（pay [2600, 3200]） |

- **數值校準理由**：兩份都係「中」級。定額 $3,300／$2,900 同 Phase 2-1 隱藏通告《星夜迷離》$3,100 同量級——
  畀到「資深臨記頂位／上位通道」嘅感覺（boardPriority high＋boardNote「移民空位 · 急聘」），
  但只係同級天花板附近，唔穿經濟：對照同檔先例（競爭通告 $1,200、人情通告 $500 都係「初」級）。
  聲量／人氣回報 [2,3]／[1,2] 略高於常規臨記通告，hard 0.2／0.25 唔加辣，breachFee $300 跟 intel 通告同級。
  req 留空 {}——空位通告賣點係「肯頂就有位」，唔再加能力門檻（canAudition 仍行中級 fameFloor 16）。
- 兩份都係一次性：殺青後 `isGigConsumed` 落板，唔會重複刷錢。

## 5. 時間閘總表

| 項目 | 開閘 | 語義 |
|---|---|---|
| F4 走定留 | 1990 夏 | yearMin/seasonMin：到季開，過季／過年長開至答為止 |
| 空位通告 ×2 | 1990 秋 | 同上（注入至殺青為止） |
| G4 穩陣工 | 1990 冬 | 同上 |

閘用真日曆 `yearSeasonNow()`（dayIndex → dateObj → calendarSeason），同 4-1／4-5 閘同一來源。

## 6. 測試

- 新 `tests/test_weave47_logic.js`（82 項全過）：段一真 openLoc（1990 春／1988 唔出、夏出 offer、真撳掣入 StoryPlay、
  答完／done 後消失、1991 catch-up 仍出、其他地點唔出）；段二真 StoryOC.applyChoice 五個抉擇逐個驗
  （旗正確、其餘答案旗唔郁、done 記錄、五項數值零變動、notes 對照、newspaperStoryResolve=null）
  ＋真可用性開關全季矩陣＋1991 catch-up＋1989 全關；段三真 renderDebtPane（秋唔出、冬出、排屋企卡之後、
  委派 onclick 真撳入 G4、答完消失、1991 catch-up）；段四真 mergeExodusGigs＋gigsForLocSeasonBoard
  （1989／1990 春夏唔注入、秋注入兩份各歸其板、冪等、數值校準斷言、真 canAudition 聲望閘、
  真殺青狀態機 open→booked→wrapped 落板、冬仍注入）。
- 新 `tests/test_weave47_static.py`（全過）：模組／掛點／閘字串、旗名與通告 id 同本 NOTES 清單交叉對照、
  choices 零 stats 斷言、微節點區塊真名／禁用詞掃描、慣例不變（SAVE key／softRev／版本標記）。
- 既有全套（tests/ 40 檔）繼續全過；主 script `node --check` OK。
- 唯一 sanctioned 舊測試更新：`test_weave44_static.py` 嘅 renderDebtPane 拼合串斷言同步為
  `banner+famCardsHtml+choice47Html+cardHtml+...`（4-4 斷言嘅語義——屋企卡排喺季節／債權／其餘債卡之前——不變，
  只係屋企卡後多咗本票嘅行動卡）；斷言處已加註解講明。

## 7. 取捨／遺留（申報）

- 微節點**唔入**事態清單（offers）系統：offer 只喺地點行動清單／手帳行動卡呈現，係刻意嘅——
  避免同主線 pacing 嘅 offers 混雜；`playerOffer` 字串只作節點文案欄位，唔經 `ensureOffers`。
- `StoryPlay` 播完收尾返地圖係現有播放器既定行為，屋企節點播完同樣返地圖（同其他手帳入口播事態一致），唔另改導航。
- 旗嘅結局回收（去留軸修正、E6 入口判定）屬 4-10，本票只負責寫旗＋通告餌，冇郁結局／數值邏輯。
- 空位通告冇專屬殺青後續（冇 tick）：「之後優先留位」係文案承諾，4-8／4-9 若要兌現（例如優先通告或何生對白），
  可讀 `S.flags["done_gig_exodus_tv_senior"]`／`done_gig_exodus_film_hand` 判断已頂過位。
