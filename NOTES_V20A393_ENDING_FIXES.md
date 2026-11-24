# NOTES_V20A393_ENDING_FIXES.md

v393：結局梯十項修復（2026-11-24，統籌拍板；諮詢原稿 `~/workspace/linji-fix392-consult/gpt_draft.md`＋`claude_draft.md`，按 brief 直接實裝，唔再問模型）。真玩輪 19 格命中 11／19，8 格結構問題，SS 截格——今票逐格修。

**改號 v392→v393**：本票原編 v392，落地前發現 main 已有 v392（第三輪 UI 檢視頭五項修正，cfd8b2b，2026-11-24 落地），改編 **v393**。改齊：NOTES 檔名、commit message、本票版本字串（`v20a392`→`v20a393`，限結局梯 code 註解＋本票測試檔名／標籤／resync 註解）。**唔郁**：main v392（UI 票）嘅標記（`v392 UI392`／`_v392defer`／`board-tall392`／`syncBoardSub392`／通告欄 TDZ 修正註解 L19607／L19628——嗰段係 UI ③ 板面 code，留 v392）、內部 `*392` 識別名（`forcedCredit392`／`careerStats392Sel`／`ptTopup392`／`DUTY392_*`／`n12_pending392` 等函數名／存檔欄，唔係版本字串）、歷史檔名（`suite392_out*.txt`、實駕 `linji-drive392/`、諮詢 `linji-fix392-consult/`——工作區 scratch，唔係出貨內容）。

## 0. 決定一覽（統籌拍板，括號係被否決嘅另一方方案）

| 項 | 修法 | 否決 |
|---|---|---|
| 1 SS 截格 | 改梯次序：六專長全部排 SS 之前（E1→E4→FK→TK→SK→GH→CK→AK→SS→E3→E5→ID→CR→E2→E0） | Claude 專長豁免 |
| 2 GH | 自選綜藝佔比（≥50%）＋自選綜藝 ≥8 宗下限；板面每 14 日至少一張綜藝、留板 ≥7 日 | 降門檻 |
| 3 CR | fame 窗擴至 35–110 | 減主線 fame／畀拒拍（同「主線即派唔可以拒絕」衝突） |
| 4 E4 | 只在 E4 判定扣除 fame 帶來的信用：`credit − 0.5×fame < 45`＋曝光 ≥6 宗／≥3 個月 | Claude 全局脫鈎 |
| 5 E5 | (a) E3 關係入口加 ≥3 宗自選幕後職務（≥2 製作）；(b) N12 刪動作標籤前置、春／夏窗口、預設 tick、舊檔補掛 | Claude 隨機「導演衝突」事件 |
| 6 ID | 首選 GPT 對照重算落地（強制增量可逐節對帳，見下） | 後備 Claude 放寬窗（未用） |
| 7 E0 | 低名望＋低投入：`fame≤40` 且三年自選通告＋正式試鏡＋正式訓練 ≤2 宗；E2／CR 加同一豁免 | Claude 敘事包裝（冇解決 36＞35） |
| 8 E3 幕後標籤 | 補授予來源：6 張新幕後職務通告（場記／副導演助理／剪接助理），授 `S.castingTags`；判定讀明確職務類別 | 刪路徑 |
| 9 E2 文案 | 通用甘草主文＋按 awardsLog 憑據插入獎項句；E1 同樣寫死獎名一併修 | — |
| 10 錢 | 補班夜班 $185／班、每週上限 2 班（保底 $370／週，live 數重算見下）；欠費改記欠，唔再提前完局 | Claude 生活費 $345→$280／親友借貸 |

## 1. SS 截格——改梯次序（`resolveEnding410`）

- 新梯：E1→E4→FK→TK→SK→GH→CK→AK→SS→E3→E5→ID→CR→E2→E0。注意 GPT 原稿將 GH／CK 留喺 SS 之後係錯——CK 正正係俾 SS 截走嘅一格，六格專長必須全部排 SS 之前。
- 實測（`tests/test_v393_logic.js`）：原被截 FK（dual 320／電影 60%／擔正 2）→ FK；原被截 CK（dual 310／喜劇 57%／信用 95）→ CK；原被截 GH（dual 300／自選綜藝 10/18／彭線）→ GH；無專長一般路線 dual 320 → 仍 SS；雙專長重疊（電影＋電視）→ FK 排先。

## 2. GH——自選綜藝佔比＋8 宗下限＋板面保證

- 新計數器 `S.careerStats392Sel`（同 `careerStats95` 同形），`end95AddWrap` 內同步累加非強制、非職務殺青；讀取 `careerStats392SelOf(st)`：有計數器就用，無就由 wrapHistory 衍生（跳過強制），wrapHistory 為空且有 `careerStats95` 時退回其副本（保舊測試 fixture 通過）。
- GH 新條件：`dual≥180 && selVariety≥8 && selVariety/selTotal≥0.5 && 彭線`。N1–N17 強制通告一律剔出分子分母。
- 板面保證 `variety392EnsureBoard`（三個電視台板 `tvb_longmen`／`tvb_kowloon`／`tvb_harbour`）：板上無綜藝時注入最近未完成綜藝 gig；狀態 `S.variety392ByLoc[locId] = {gigId, sinceDay}`，同一張留板 ≥7 日，14 日內唔重複注入同一張。注入只係繞過 NAT92 錯峰——注入嗰張經玩家自選試鏡日報名，構造上唔會撞強制拍攝。
- 實測：原 25% 存檔重跑，`8/16` 達標、`8/17` 及 `7/7` 失敗；重跑 CK 路線確認加密板面後仍到 CK（見 §1 CK 斷言）。

## 3. CR——fame 窗 35–110

- `ENDING95_T.crFameHi: 59 → 110`。副作用：fame 60–110 合 CR 其餘條件者由 E2／E0 升入 CR；ID 排前，雙達標仍入 ID；配合第 7 項低投入分流，防閒置存檔被 CR 吞。
- 實測：fame 59／60 均入；fame 110（credit 105，高過 ID 窗 99）入、111 出（落 E2）；原 CR 路線 fame 95／credit 95 入。注意：ID 排喺 CR 之前，窗係 `credit ≤ max(60, fame×0.9)`——邊界 fixture 必須用高過 ID 窗嘅信用先至測到 CR 本身（例如 fame 110 要用 credit 105，唔係 70）。

## 4. E4——只在 E4 判定扣除 fame 帶來的信用

- 新判定：`fame≥50 && (credit − 0.5×fame) < 45 && 曝光 ≥6 宗／橫跨 ≥3 個月`；全局 credit 繼供 dual 及其他結局用。
- **數字統一用 45**：GPT 原稿 (b) 寫 `<45`、(d) 驗收寫「≤40」，內部不一致，統籌定 45。`ENDING410_T` 欄改名 `e4CreditBelow` → `e4NetCreditBelow: 45`（舊欄已刪）。
- 曝光由 wrapHistory 衍生 `exposure392Of(st)`：type 廣告／綜藝、非強制、計宗數＋唔同年月份數。
- 實測：fame 100／credit 94（扣除後 44）＋曝光 6 宗 → E4；credit 95（扣除後 45）→ 唔入 E4（落 CR）；曝光得 5 宗 → 唔入 E4；高信用偶像對照（fame 100／credit 120）→ 唔入 E4。

## 5. E5——分開修

### (a) E3 關係入口＋職務數

- `endingE3Eligible410` 改為：`credit≥42 && （標籤入口：≥2 種職務＋≥2 製作）或（關係入口：導演 rel≥60 且 ≥3 宗職務＋≥2 製作）`。導演 rel 上升機制不變（任何電影殺青都＋4–7，L22701）。
- 職務系統見 §8。

### (b) N12——核實結果：指定最早日期＝現有閘嘅 1992 年春窗口

- 落手前核實：`STORY_GATE_3Y.N12 = { needDone: ["N11"], tagAny: ["動作","action","tag_action","身手好"], yearMin: 1992, seasonIn: ["春"] }`——最早 1992-03-01，**冇另一個日期**。「指定最早日期」就係呢個 1992 春窗口。
- 改法：刪 `tagAny`，`seasonIn` 擴至 `["春","夏"]`（春錯過唔致死；N13 亦係夏，`ORDER165` 已將 N12 移到 N13 之前）；`CALIB60_NODE_WINDOWS.N12` 改為 seasons `["春","夏"]`、whenLabel「1992 年春／夏」（「回憶」過窗提醒同步延後一季）。
- 持續顯示至處理：閘本身令 N12 由 1992-03-01 起 open，`story165TryForcedPlay` 每日返地圖自動播——忙拍攝順延至下一可操作時段係原有強制主線機制。
- 預設 tick `story392N12DefaultTick()`（`story165NextOpen` 開頭呼叫）：N11 done、N12 未 done、dayIndex ≥974（1992-09-01 秋首日）仍未玩嗰陣，經真 `StoryOC.applyChoice(node, N12_b)` 行預設拒接＋旗 `flag_n12_auto_default`＋toast，每節只結算一次。N12_b 亦係 `GRANT229_CHOICE` 條目（→ gig_1992_tv_103），行 applyChoice 會同時觸發即派記錄，正確。
- 舊檔補掛：`normalizeSaveObj`——N11 done、N12 未 done、日 ≥1992-03-01（dayIndex 790）→ `S.flags.n12_pending392 = true`。
- JSON pack：N12 `openConditionsNote` 改為「三年版閘以 STORY_GATE_3Y 為準（N11 完成＋1992 春／夏）；此欄只作 legacy 對照。」（全文「1992」仍只出現一次；`openConditions: ["tag_action"]` 留原樣——runtime 3Y 閘 short-circuit，永不讀佢；`storyGate113Scrub` 只驗 needDone／weekMin，唔驗 tagAny，N12 done 標記安全）。N12 提示表 lockedHint 只刪「要有動作標籤傍身」嗰句，年份保持舊曆 1990（玩家面 runtime 先＋2，直接寫 1992 會令 `test_gate136_static.py` 失敗）。

## 6. ID——首選 GPT 對照重算落地

- 落手前核實：強制拍攝確有兩條可逐節對帳嘅直接寫入信用流水——(1) 每單殺青 `contractCredit361OnWrap` 寫入 `industryCreditDelta` ＋1（高級／稀有 ＋2），季上限 ＋4／生涯 ＋36，強制即派 gig 殺青亦照寫；(2) N1–N17 抉擇 `effects.stats.industryCredit`（經 `applyChoice` 寫入 delta），JSON 實測約 20 個抉擇帶 ＋1／＋2（N7_a ＋2、N7_c ＋1、N9_b ＋2、N10_b ＋2、N10_c ＋1、N11_b ＋2、N8_a ＋1、N8_c ＋1、N14_b ＋1、N14_c ＋1、N16_b ＋2、N16_c ＋1、N13_a ＋2、N13_c ＋1、N12_b ＋1、N15_b ＋2、N18_a ＋1、N18_b ＋2、N19_a ＋2、N19_b ＋1）。**所以首選可行，落地首選，後備放寬窗未用。**
- 做法：新 ledger `S.forcedCredit392 = { direct, fame, wraps, choices }`——殺青嗰刻若 gig 係 grant229 即派（`S.flags["grant229_delivered_"+gigId]` 或 recorded），`direct += contract gain`、`fame += sh.fame`；`applyChoice` 逢主線節點（N1–N17／N6F／N18／N19）且 `stats.industryCredit>0`，`direct += 該數`。
- 舊檔回填 `forcedCredit392Backfill(o)`（一次性、冪等）：(a) 重播殺青流水（`forcedCredit392ReplayWraps`，季上限 ＋4／生涯 ＋36，只計強制 gig）；(b) `S.story.choices`＋`StoryOC.findNodeRaw` 無歧義匹配主線抉擇 `stats.industryCredit>0`。
- ID 判定用對照 credit：`fameC = max(0, fame − forcedFame)`，`creditC = max(0, round(fameC×0.5 + stage×0.3 + acting×0.2 − max(0,stress−40)×0.1) + (delta − forcedDirect))`（**先加分再封頂**），窗仍套原窗 `creditC ≤ max(60, fame×0.9)`（窗用實際 fame），下限 `credit≥30` 用實際 credit，neg 條件不變。`resolveEnding410` 保持純函數——所有 derive 唯讀，唔寫入。
- 實測：fame 100／credit 100、無強制增量 → 唔入 ID（落 CR）；同數值＋強制帳 {direct:15, fame:5} → 對照信用 83 → ID；對照組（同終局 fame、靠自選推高信用）→ 唔入 ID。

## 7. E0——低名望＋低投入

- `activity392Of(st)`＝自選殺青宗數（sel.total）＋正式試鏡宗數＋正式訓練宗數。正式試鏡由狀態衍生：`aud91Log`／`pendingAud`／`booked`／`shoots`／`done_*`（剔除 grant229）嘅 gigId 併集（無持久試鏡計數器，失敗試鏡只留 `aud91Log` 上限 12 條，夠分流用）；正式訓練＝`Σ S.trainCount`。
- `isLowActivity392(st)`＝`fame≤40 && activityTotal≤2`。實裝方式：else 分支維持 E0 預設（函數必須有回傳），活躍度分流放喺上游——E2 分支加 `!(fame≤40 && activity≤2)` 豁免；CR 分支同樣加（第 3 項要求防閒置存檔被 CR 吞）；E3／E5 已分別由新職務／人情門檻守住，SS／專長格閒置玩家到唔到，ID 要 fame≥60，E4 要 fame≥50。snapshot 加 `activity392` 診斷欄。
- 實測：三條路線（全程只推日／只做糊口兼職／只完成兩宗不同方向低曝光活動）都要走完 N1–N17 落 E0（邏輯斷言：fame 36 零投入 → E0；fame 40 投入 2 → E0；實駕見下）；驗 40／41、投入 2／3（fame 41 零投入 → E2；fame 40 投入 3 → E2）；同樣低 fame 但持續工作嘅正常 E2 仍落 E2。

## 8. E3 幕後標籤——補授予來源

- 6 張新 runtime 注入職務 gig（`mergeDuty392Gigs()`，仿 `mergeFavorGigs` 模式，喺 `gigsForLocSeasonBoard` 呼叫；**唔入 `content/gigs_new.json`，唔郁 330 張計數**）：每種 2 張，製作名各異——1990《廟街夜話》場記（film_harbour）／《碼頭風雲》副導演助理（film_lion）；1991《電視城長劇》剪接助理（tvb_longmen）／《獅子山下情》場記（film_cotton）；1992《香江歲月》副導演助理（tvb_kowloon）／《海港之夜》剪接助理（film_harbour）。
- 欄位：id `duty392_*`（避開 NAT92 錯峰——`nat92StaggerEligible` 只認 `^gig_\d{4}_`／`^g36_`；season「全年」令 `gigSeasonHidden88` 永遠唔藏；year 用舊曆源頭值 1988／1989／1990 經 `years66GigRemap`＋2，仿 `gig_favor_ho_errand` year:1988 precedent；文案避開四位年份數字），type 電影／電視劇，category「幕後職務」，genre「劇情」，roleLabel 即職務名，roleScale `"crew"`（唔入任何擔正尺度），tier「臨記」，hard 0.2，req {}，days 2，pay [120,180]，fame [0,1]，`duty392: true`＋`dutyKind` 欄。導演用虛構名：方子健／梁志強／吳國榮／何偉棠／沈家豪／劉天成。
- 殺青嗰刻（`resolvePlannedDay` wrap 分支，`applyGigTagOnComplete` 隔籬）：經 `applyCastingTags` 授標籤（id `tag_duty_clapper`／`tag_duty_ad`／`tag_duty_editor`，label「場記」／「副導演助理」／「剪接助理」；`castingTagMeta` 未知標籤回 fallback、無雙軌 delta，安全），並寫 `S.backstageDuties392` log（{kind, production(workTitle), gigId, day}，每 gigId 一次）。`castingTagMeta` 註冊表 `content/STUB_CASTING_TAGS_v1.json` 加 3 個標籤＋labelToId 映射，現共 13 個標籤（文字編輯，格式無變——第一次用 python json.dump 重寫兩個 JSON 檔時整檔格式被改，已 `git checkout` 還原再用文字編輯重做；**以後 JSON 只准文字編輯**）。
- 判定 `backstageDuties392Of(st)`（純讀；先讀 log，無 log 就由 wrapHistory＋職務 registry 衍生）回 distinct kinds／productions／總數；E3 判定讀佢，取代舊 `endingBackstageTagCount410>=2` 入口（關鍵字計數保留畀 `endingBackstageClose410` 差少少診斷＋snapshot 顯示）。
- 幕後職務唔入自選履歷（`end392SelDeriveStats` 跳過 `duty392_` 前綴／`duty392` 旗；`end95AddWrap` 自選分支同樣跳過）——職務唔係演藝通告，唔應入 GH 分母／E0 活動量。
- **現有 2 張「幕後代唱歌手」唔郁**：`gig_1990_rec_202`（卡拉OK影碟代唱歌手，genre 情歌）同 `gig_1992_rec_204`（大碟錄音代唱歌手，genre 情歌）經 `gigGenreTag360` 回 null——genre 唔喺 `GIG_GENRE_TAG360`、roleLabel 唔係「動作替身」，**唔授予任何 castingTag**，唔計入新入口。
- 實測：rel<60 存檔完成兩個不同製作的兩種職務必須落 E3（邏輯單元：2 種／2 製作 → tagEntrance 開）；兩次同類職務、同一製作兩個職務、只做電影常駐散工均唔開標籤入口（單元斷言）；測殺青重播同讀檔，同一交付只授予一次（log 每 gigId 一次；衍生路徑由 wrapHistory 重播）。

## 9. E2 文案——通用主文＋按紀錄插入獎項句

- 新 helper `endingAward392TvSupport(st)` 掃 awardsLog 搵 category id `cat_tv_support_m`（電視台最佳男配角；`AWARDS188_CATEGORIES` 有 `cat_tv_support_m`／`cat_film_support_m`，label 均為「最佳男配角」），回 "won"／"nominated"／""（勝出優先於提名）；`endingAward392WonLabel(st)` 經 `AWARDS188_CATEGORIES` 查首個 won 類別 label。awardsLog 條目形狀（`commitAwardToLog`）：`categories: [{id, outcome, repTitle,...}]`，上限 24 條。
- E2：主文刪寫死獎句，改通用甘草敘事；won 加得獎句、nominated 加提名句、無紀錄只出主文。**E1 同樣寫死「最佳男配角」係錯**（E1 只要求任一獎）——一併修：通用開場＋有 won 紀錄先具名獎項，舊檔欠紀錄用通用版。唔郁其他結局文案。
- 實測（五組存檔）：0勝/0提名、只有該獎提名、贏得該獎、只贏其他獎、舊檔欠紀錄；同一獎既有提名又有勝出只顯示勝出句（`tests/test_v393_logic.js` E2 文案段全過）。

## 10. 錢——補班夜班＋記欠（live 數重算）

- **重算（live 數，唔照抄 GPT）**：1992 生活費最高 $365（fame≥250 帶；$325／$345／$365 三帶）；咖啡 7 日全勤均值 $300／上限 $375；街演均值 $237.5／上限 $300。保底 $370／兩班各 $185 **成立**，理據改為 live 數：最高生活費 $365＋$5 緩衝＝$370；零工週做足兩班淨 ＋$5／週，8 週 ＋$40（期初 $0 期末為正）；一班 $185＋咖啡均值 $300＝$485 ≥ $365。
- 補班：新日程活動 `pt_topup`（補班夜班，$185／班，每週上限 2 班，唔畀 fame／credit／導演 rel／演藝通告計數；壓力小加），放 `PLAN_ITEMS.perform`（同 street／cafe_gig 一組），揀掣嗰陣滿 2 班即 lock（`ptTopup392WeekCount()`＋動態 item），`resolvePlannedDay` 硬截（第 3 班起 $0＋提示）；計數 `S.ptTopup392 = {wk, count}`（週 key 同 `ptWeek368` 式 `floor(dayIndex/7)+1`）；$185 固定，唔疊 taper／壓力折扣；壓力 `6+R(0,4)`；`stressDeltaForAct` 表加 `pt_topup: 8`（實際均值 8 對齊）；`exec105KindForSlot` 及 k105 映射加 pt_topup → "perform"。注意：live 咖啡已係 `R(45,75)`（v390，註解寫明均值 $60），街演 `R(35,60)`——重算數字已用呢個為準。
- 欠費改記欠：`settleWeek` 短缺 `living − paid` 累入新欄 `S.moneyArrears`（新檔預設 0，normalize 補 0），結算卡寫明記欠＋主線照常；`conseq61SettleEval` 刪破產寬限分支（起寬限／倒數／用盡收場），`CONSEQ61_CFG.graceWeeks` 刪欄，`conseq61State` 刪 `grace` 初始化，舊檔殘留 grace 由 `conseq61LegacyMark` 清走；`conseq61SettleEval` 第三參數 `weekEarnIn` 保留（`void` 標記，呼叫兼容）。E7 破產**呈現**分支（`endingCareerScene410` bankrupt 版、總結／剪報「寬限期滿」字眼）保留作已錄得破產 E7 舊檔嘅顯示兼容，只刪**產生**路徑。
- 驗證：由 SS day 819、TK day 875 破產前至少 8 週的存檔重跑（實駕見下），逐週記可接班次、實收、生活費、扣費後餘額及錯過通告，兩條都要靠實際可排入的補班避破產並命中原定格；另期初 $0、連續 8 週無普通兼職的壓力存檔，做足補班後期末須為正數；零補班對照按週記欠並走到三年結算。

## 其他設計定案（實裝前制定）

- **「自選／強制」判定謂詞（GH／E4／E0／職務共用）**：強制＝grant229 即派 gig，以 `S.flags["grant229_delivered_"+gigId] || S.flags["grant229_recorded_"+gigId]` 判斷（delivered 優先；recorded-but-未-delivered 又經板面完成嘅邊緣誤判窗口不足一日，可忽略）。N1–N17 強制通告全部經 grant229（`GRANT229_CHOICE`／ENC79／DRAFT），謂詞覆蓋晒。
- **E1 邊界唔變**：349／350、擔正 0／1（`tests/test_ladder95_logic.js` 守門）。
- **刪舊**：`ENDING410_T.e4CreditBelow` → `e4NetCreditBelow`；`ENDING410_T.e3BackstageTags` 死欄已刪（無任何讀取）；`CONSEQ61_CFG.graceWeeks`、寬限分支、`conseq61State.grace` 已刪；E1／E2 寫死獎句已刪。
- **唔郁**：SAVE key（`starVolunteer_map_v19w`）／softRev／產品 `?v=`；頒獎贏線 0.875；source 年份（YEARS66 runtime 推移）；MEMORY.md；E6「心灰」版。

## 測試

- 更新測試（全部通過）：`test_ladder95_logic.js` 47/0（FN_LIST 加 15 個 v393 函數，CONST_LIST 加 `DUTY392_KIND_BY_ID`／`DUTY392_GIGS`；rOneLead 期望由 SS 改 FK；E3 三變體 fixture 補職務 log；加守門：導演 rel 65 但 0 職務 → E0；兩種職務同一製作 → E0）；`test_weave410_logic.js` 76/0（抽取清單加 v393 函數＋兩個 DUTY392 const；新增 `EXPO392` 共享履歷；E4 rescued／sunk fixture 補 EXPO392，加守門斷言；E3 導演線 fixture 補 3 宗職務，加守門；E3 標籤線改為職務 fixture，加守門；四處 E2 fixture（fame 40／stage 50／acting 35）補 `trainCount: {train_acting: 3, train_stage: 2}`——教訓：新低投入規則下，零活動紀錄嘅合成 E2 fixture 會正確地判 E0；fixture 代表「持續工作嘅正常 E2」就要帶活動紀錄）；`test_conseq61_logic.js` 82/0（§3 寬限整段改寫為「寬限已刪」測試；§5 破產 present 改為先證見底 5 週唔再產生 bankrupt pending、無 pending 就唔呈現，再手動設 grandfathered `pendingEnding {kind:"bankrupt"}` 證顯示兼容）。
- 待更新測試（本票已更新，全部通過）：`test_fix65_logic.js` 38/0（§3「FIX65-2 寬限入帳解除」整段改寫為「寬限已刪」測試：見底唔起寬限／唔寫 pending／連續 5 週唔收場／舊檔殘留 grace 唔再被倒數）；`test_fix65_static.py` ALL PASS（CFG 無 graceWeeks；`weekEarnIn` 第三參數保留）；`test_conseq61_static.py` PASS（CFG 無 graceWeeks＋`moneyArrears` 在位）；`test_weave410_static.py` ALL PASS（`'e4NetCreditBelow: 45'`）。
- 新增測試：`tests/test_v393_static.py` ALL PASS（梯次序、E4 新窗 45、CR 110、E0 40／2 宗、GH 8 宗下限、職務入口、N12 閘、補班 $185／上限 2、記欠、寬限已刪等靜態守門）；`tests/test_v393_logic.js` **52 passed, 0 failed**（梯次序 FK／CK／GH 截格修復、E4 邊界 44／45、CR 110／111、E0 40／41 及投入 2／3、ID 對照重算正反、職務入口正反、GH 8/16 達標 vs 8/17 及 7/7 失敗、forcedCredit392Of 衍生、exposure／activity 單元、獎項句憑據）。
- 全套 suite：第一輪 `bash qa131/run_suite.sh ~/workspace/linji-work392 ~/workspace/suite392_out.txt` → **TOTAL PASS 392 FAIL 26**。26 個 FAIL 之中：9 個已知 pre-existing；4 個係 v393 改動引起嘅測試期望落後（gig229_counts／gig229_v251_c／qa101／weave48_logic——resolveEnding410 新依賴未抽取＋N12 舊閘期望），已修好；13 個係行號釘＋N12 閘期望漂移，見 resync 一節。**第二輪重跑 `~/workspace/suite392_out2.txt` → TOTAL PASS 409 FAIL 9：409＝基線 407＋2 個新 v393 測試；9 FAIL 全部係已知 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），新 FAIL 0。**第三輪（rebase 後，`~/workspace/suite392_out3.txt`）→ **TOTAL PASS 411 FAIL 9**：411＝基線 409＋2 個新測試；9 FAIL 全部係已知 pre-existing，新 FAIL 0。第四輪（改號 v393 後，`~/workspace/suite393_out.txt`）→ **TOTAL PASS 411 FAIL 9**，同一組 9 個已知 FAIL——改名只動註解／檔名／標籤，index.html 語法檢查 2 scripts／0 bad，受影響測試（ladder95／weave410／conseq61／fix65／gig229／qa101／weave48＋8 檔 resync 頭註解檔）逐個直接跑全部 PASS。`qa296/derive296.json` 每次跑完已還原。

## Resync（v393 第一輪；腳本當時叫 `qa392/resync392.py`，同 UI 工人版同名 AA 衝突後改名 `qa392/resync393_endings.py`；rebase 後見下）

- index.html 淨 **+607 行**（49753→50360）。13 檔漂移全部係行號釘純漂移（difflib 對位映射、內容逐字核實、零移除）＋5 項有意改版期望更新：
  - travel114（COUNT／FREE／DEF／WRAPPER；DEF 44847→45393、WRAPPER 31067→31613）、rom159（6 釘＋全佳行 27225→27771）、rom176（6 釘）、tang152（2 釘）、text125（3 錨點 12001→12011／12143→12153／17324→17703）、gift185／tang171／tang173（總行數＋openLoc DEF，鏈尾加 ＋v393-endings +607；UI 嗰截 ＋v392 +146 不變）。
  - 有意改版：story157 pack sha 重算（N12 note 改寫，`f85832c3…`）；story_gate113 N12 閘字串（刪 tagAny、春／夏）；weave46 N12 改斷言「無 tagAny」（只驗 code 部分，行尾註解提到 tagAny 係解釋）；weave48_static N12 閘片段；terms57「身手好」計數 2→1（N12 閘刪 tagAny 後只剩 N9 一處）。
  - 另外 4 檔（suite 第一輪 FAIL）：gig229_counts／qa101 係 FN_LIST 未抽 v393 新 helper（`careerStats392SelOf is not defined`），已補抽取清單＋兩個 DUTY392 const；gig229_v251_c 係 D8 附錄 N12 閘期望（改新閘）；weave48_logic 係 N12 兩條舊斷言（冇標籤唔出現／夏唔出現）改為新行為（冇標籤都出現／夏都出現）。覆驗：17 檔逐個直接跑全部 PASS。

### Rebase 上 cfd8b2b（v392 UI 檢視第三輪先行落地）

- Commit 嗰陣常駐 clone main 已經由 967e2d8（v391）行前到 cfd8b2b（v392 第三輪 UI 檢視頭五項修正，index.html 淨 +146 行）。本票 rebase 上去：`index.html` 自動合併成功（零衝突標記、兩邊標記齊全、語法通過）；`qa392/resync392.py` 同名唔同內容（AA）——留 UI 版，我嗰份改名 `qa392/resync393_endings.py`；8 檔測試釘兩邊都改過（gift185／rom159／rom176／tang152／tang171／tang173／text125／travel114）——取 cfd8b2b 版做底，再跑 endings resync（舊釘值＝cfd8b2b 版）：index.html 49899→50506（淨 +607，DEF 44938→45484、WRAPPER 31128→31674、全佳 27284→27830），零移除、零 mismatch。教訓：rebase 入面 `--theirs` 係被 replay 嗰邊（我）、`--ours` 先至係新 main——第一次用錯方向，要由 `git show HEAD:` 還原重做。
- Rebase 後覆驗：我嗰邊 25 檔＋UI 工人嗰邊 18 檔，逐個直接跑全部 PASS。Suite 第三輪 411／9（見測試一節）。錢實駕 M1／M2 喺 rebase 後重跑，見錢一節——UI 工人改咗日結／休息卡 dismiss（撳外面唔推進日期），舊 driver 靠 mask-outside 推進，第一次重跑 M1 FAIL，harness 改掣後重跑全過（唔係 game bug，見錢一節）。

## 實駕驗證

播種實駕 `~/workspace/linji-drive392/drive392.py`（Playwright，Chromium headless shell，viewport 390×844 dsf 2；播種：fresh() 形狀＋逐格改欄位，寫 localStorage slot 1，dayIndex 1096＝1993-01-01，N17 backstopDay 無條件開；推 N17 對白→選「順其自然」→「完成這一節」，讀 `S.ending410.career`）＋`drive392b.py`（N12＋錢）：

### 結局格（16 格，15 過／1 唔過）

| 格 | 結果 | Live 終局數值 |
|---|---|---|
| FK | ✅ PASS | dual 324（fame 170／credit 154） |
| CK | ✅ PASS | dual 314（160／154） |
| GH | ✅ PASS | dual 304（160／144） |
| SS | ✅ PASS | dual 324（170／154）——無專長一般路線仍 SS |
| E1 | ✅ PASS | dual 424（220／204）——守門成立 |
| TK | ✅ PASS | dual 324——電視 55%＋長劇擔正 1，零負標籤 |
| SK | ✅ PASS | dual 324——唱片 55%＋音樂獎提名，零負標籤 |
| AK | ✅ PASS | dual 324——動作 60%＋武師班 6，零負標籤 |
| CR | ✅ PASS | dual 194（95／99）——fame 95／credit 95 |
| E4 | ✅ PASS | dual 194（100／94），variant sunk——扣除後 44＜45＋曝光 6 宗／3 個月 |
| E4B（邊界對照） | ✅ PASS | dual 195（100／95）——扣除後 45，唔入 E4，落 CR |
| E3 | ✅ PASS | dual 234（120／114），variant 大導演——職務入口 2 種／2 製作，導演 rel 30 |
| E5 | ✅ PASS | dual 234（120／114）——人情 6＋何生 rel 65，E3 職務入口唔開 |
| ID | ✅ PASS | dual 204（100／104）——對照信用 83（實信用 100 高過 ID 窗 90） |
| E2 | ✅ PASS | dual 234（120／114）——持續工作正常 E2 |
| **E0** | ❌ **FAIL：落 E7** | dual 76（fame 36／credit 40），`earlyEnd={kind:"review", year:1992, dual:76, floor:140, week:157}`——見下「新發現」 |

- 註（live ＋4 信用）：播種用 `industryCreditDelta` 計出嘅信用，讀檔嗰陣 `contractCredit361Backfill` 補返 wrapHistory 嘅合約信用（同一季封頂 +4），所以 live delta 一律比種子值 ＋4、信用 ＋4、dual ＋4（FK 320→324、E1 420→424 等）。真存檔唔受影響（殺青嗰刻已寫入）。E4 邊界播種已預留呢個 +4（設計扣除後 40，live 44，仍＜45；對照格設計 41，live 45，唔入）。
- 註（E5 播種）：`creditsHeld` 讀 `mockCredits` 持有數（`favorCreditCountsAsHeld`），唔係 `favorLedger.credits`——播種要加 2 張未收債權先至湊夠 6（settled 4＋持有 2）。第一版播種漏咗呢點，落 E2；補返之後落 E5。

### N12（4 項全過，`drive392b.py`）

- N12A 準時：day 790（1992-03-01 春）、冇動作標籤 → N12 開、N12_a 完成、`flag_stunt_double` 在位。注意：day 790 撞正 3 月 1 日廣告賞請柬遮住畫面，driver 要先「推辭」請柬先至播到 N12（harness 問題，唔係 code 問題）。
- N12B 夏窗口：day 850（夏）、冇動作標籤 → N12 開。
- N12C 預設 tick：day 980（秋）、N11 done 欠 N12 → `flag_n12_auto_default` 在位、N12 done（行 N12_b）。
- N12D 舊檔補掛：day 800、N11 done 欠 N12 → 讀檔後 `S.flags.n12_pending392 = true`。

### 錢（2 項全過，`drive392b.py`）

- M1 補班：day 734（第 105 週星期日，錢 $340＝第 105 週生活費上限）收週（生活費 roll $325，錢 $15、欠 $0）→ 入屋 editable → 排第 106 週（週二／週三補班夜班、其餘休息）→ 兩班實收 $370（日結卡「本週第 1 班／2 班」「本週第 2 班／2 班」，各 +$185；壓力 +9／+6）→ 收第 106 週：錢 $60（$15＋$370−生活費 roll $325）、欠 $0、`ptTopup392={wk:106,count:2}`、`pendingEnding=null`。保底成立。
- M2 零補班對照：同樣起點、全週休息 → 收第 106 週：錢 $0、欠 $310（生活費 roll $325 − 週初 $15）、`pendingEnding=null`、日子照推到 day 742——欠費記欠、主線照常，無提前完局。
- **Rebase 後重跑（2026-11-24，改號 v393 後）**：第一次 M1 FAIL——收週 105 後 `homeEditable=False`、plan 唔郁、日子停喺 day 735。根因係 harness 唔係 game：UI ① 刪咗「點擊外面＝回家結算」細字，撳 mask 外面唔再入屋結算；舊 driver 喺 `advance_to_day` 目標日嗰陣只識撳「點擊外面」mask，CLICK_JS 亦唔識「回家結算」掣，結果入唔到屋（editable 假）→ 手帳唯讀 → 排唔到補班 → 推唔到日。修 harness（`~/workspace/linji-drive392/drive392.py` CLICK_JS 加「回家結算」／「開始並結算當日」／「開始今日行程」；`drive392b.py` 目標日改行 CLICK_JS 撳卡面正掣）：重跑 **M1 PASS**（收週 105 day 735 錢 $15 欠 $0 editable=True；第 106 週 plan `["scout_all","pt_topup","pt_topup","rest","rest","rest","rest"]`；收週 106 day 742 錢 $60 欠 $0、`ptTopup392={wk:106,count:2}`、`pendingEnding=null`）；**M2 PASS**（收週 106 day 742 錢 $0 欠 $310、`pendingEnding=null`）。途中撞到強制劇情「啟德送芬姐」照常播完，唔影響推進。
- 附註：生活費係 band 內隨機 roll（第 105 週 $250–340、第 106 週 $280–370），唔係 mid 定數——播種預期用區間斷言；週計劃要經真流程先排到（星期日收週 → 結算 → 入屋 editable；中途撳手帳掣開出嚟係唯讀，`homeEditable` 由 `enterHome` 嗰陣定，播種值會被覆寫）。

### 新發現（未修，等拍板）

- **E0 喺 live 到唔到——1992 floor 改判 E7（第 7 項驗收準則唔成立）。** 閒置路線（fame 36／credit 40／dual 76／零投入）行到 N17，`resolveEnding410` 本身判 E0，但 `ending410ResolvePresent410` 嗰刻 dual 76＜1992 floor 140、E0 唔喺 `ending361FloorExempt` 豁免之列（只豁免 E6／E4／E3／E5），改判 E7 `review1992`。第 7 項只修咗分支條件（fame≤40＋低投入），冇掂 floor 豁免——兩者衝突，brief 兩邊都有寫（「E0 唔豁免」＋「閒置路線落 E0」），現場實駕先至對到。
- 上限推算：fame≤40 嘅玩家，credit 上限約 84（base ~34＋delta 上限 ~50：合約上限 +36＋抉擇 ~+25，仲要扣 stress），dual 上限約 124，**結構上到唔到 140**——唔係播種數值問題，係 E0 定義同 floor 互斥。
- 兩個選項（等拍板）：(a) E0 加入 `ending361FloorExempt` 豁免（閒置路線落 E0；E7 繼續由破產／評核／主動退圈觸發）；(b) 接受 E0 係死格（19 格得 18 格可達，E0 永遠由 floor 轉去 E7）。建議 (a)——E0 本身就係為「浮沉」而設，floor 嘅原意係捉「玩得差」而唔係「玩得少」，而家兩者分唔開。
