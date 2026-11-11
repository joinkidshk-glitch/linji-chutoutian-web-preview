# v20a105 UI105（工人 C：版面＋文字硬傷組）

跟 UI 審計報告 `linji-ui-audit/UI_AUDIT.md` 修 23 項 A 級（D-6、D-7、D-8 第一階段、S-3、S-6、S-10、S-16、S-19、S-21、S-23、S-24、S-25、S-28、S-31、S-32、S-35、S-37、S-39、S-40、S-43、S-44、S-45、S-48）。B 級冇掂。冇改 SAVE key（starVolunteer_map_v19w）／softRev（s107）／產品 ?v=（v20a10）／數值（S-44 只改狀態對齊）。

## 逐項

- **D-6** 旁白句改入底部對話框位：sp 播放器旁白（cur.system）plate 加 `sp-plate-narration105` class＋CSS override（stage 靠底、plate 全闊左對齊）。實駕截圖 `21_story_narration.png`：旁白坐喺場景圖下方對話框。
- **D-7** 頂部 meta 收起：刪常駐「對白 X/Y · 句 X/Y」計數；幕標題＋場景＋meta 只喺幕首句（step 1 第一行）以 `sp-head-opening` 閃現，之後 head 清空。實駕驗：第一行有 head、下一行 head 消失。
- **D-8（第一階段）** 隨機事件補場景底：新 `wf4Scene105(ev)`（ev.loc；day 事件用全域 atLoc；查 `LOC_SHEET_BG` 同地點板同一套新場景來源），`wf4PlayEvent` 三步 modal 共用 head 前置 `.wf4-scene105` 場景圖。hospital／gift_shop 冇逐地點新圖 → 回空字串、冇底（維持現狀）。具名角色企立屬第二包，冇做。實駕截圖 `18_wf4_event.png`（獅子山事件有製片廠場景底）。
- **S-3** 導入卡瘦身：B01 卡刪金色教學段＋同 CTA 重複嘅長段；教學內容搬去行程編輯頁常駐一行 `#plan-teach105`（點排規則）。取捨：冇做逐畫面 contextual 觸發，改做相關畫面（編輯頁）常駐——內容冇失，卡身冇截斷（截圖 `03_b01_card.png`／`04_plan_editor.png`）。
- **S-6** 地圖面板按圖比例收高：`#app .map-polaroid{flex:0 1 auto}`（面板高 798→511px，貼圖高 509；舞台／熱區幾何冇郁，圖仍闊度-bound）；v20a54 羅盤底圖層由 `center 88%` 移去 `center 40%`（俾不透明地圖圖遮住），圖下方唔再有空白帶＋淡羅盤。截圖 `07_map.png`。
- **S-10** 劇情卡：「›」改絕對定位釘喺卡右邊中線，永唔孤行；`storyMapHintHtml` 副行截到第一句，卡面 2 行內。截圖 `07_map.png`。
- **S-16** 筆記紙裝訂環：`.nb-left,.nb-right` 左 padding 32→46px（實駕量度：筆記本左緣 x=25、環入內容約 23px、標題起點 x=63；改後 computed paddingLeft=46px）。截圖 `04_plan_editor.png`。
- **S-19** 壓力資訊去重：`confirmPlan` 直入 `commitPlanAndGo()` 唔再彈 modal（`showStressPreviewModal` 保留畀其他呼叫方）；編輯頁壓力行撳開行內明細 `#nb-stress-detail105`（逐日 ±／累計＋高峰判語＋影響句，改行程自動刷新）；`stressImpactLine34` 四句重寫做完整句子。實駕驗：明細展開 OK、確定後冇 modal。截圖 `05_stress_inline.png`、`06_after_confirm.png`。
- **S-21** 地點板在場紅星行（`enc79SheetPresence` 呈現層；觸發／派位邏輯冇郁，嗰啲係工人 A 範圍）：加頭像縮圖（企立首選圖，onerror 隱藏）＋「遠觀」標籤＋距離句，CSS `.pres105*`。實駕限制：第一日茶餐廳有紅星嗰陣入場會先觸發巧遇（工人 A 流程）蓋過地點板，sheet 態影唔到在場行；以守門 static 測試＋代碼路徑驗證交差。
- **S-23** 行動卡費用欄統一：`openLoc` 嘅 `add()` 渲染層正規化——有 $ 金額只留 `$X`（「+1日」語意併入 hint）；`+1日` 保留；「無／不耗日」→「免費」；已知狀態字原樣；其餘 flavor 名（凍檸茶／萬寶路等）移入 hint 尾、費用欄歸「免費」。實駕：事務所板（免費／+1日／禮物／現金）、醫院板（$500／免費）、獅子山板（+1日）齊。
- **S-24** 事務所信任行刪結局劇透兩句（「信任去到 60…江湖撈家嗰條路」）；信任數字＋下一階提示（npcNextTierHint）保留。實駕事務所板：「何生信任：14／100（再加 11 到『日常情報』）」，冇劇透句。⚠️ 同 enc79 護欄測試有规格衝突，見文末。
- **S-25** 醫院板：體檢改先確認後扣錢（確認 modal 講明 $500／28 日／寬容 10 點／現存款，「確認付款」先行新函數 `buyCheckup105()` 扣錢＋結果 modal；「唔住」返醫院板）；加「醫院有咩用？」免費說明卡（治療 $600 病倒嗰朝先出／探病／體檢三者條件）。禮品店係明碼實價商店列表、撳掣即買係商店慣例，冇加確認。截圖 `09_hospital.png`、`10_checkup_confirm.png`。
- **S-28** 未達標提示統一「演技 14／需 25（差 11）」：`gigGapBits34` bits 加 cur/need；`gigGapLine34` 新格式（「；」join、冇「欠：」前綴）；板面行 `gigGapBoardLine37` 委派同一函數自動跟上。
- **S-31** 通告詳情：`gigApplyDeadlineText` 改「仲有 N 日截止」；`gigCastPeriodLine(g,{noApply:true})` 令期間行唔再黐報名截止；詳情加獨立一行「報名截止／仲有 N 日截止」（ddlRow105）。實駕詳情 modal 兩行分開齊（截圖 `17_notice_detail.png`）。
- **S-32** 通告詳情卡高按內容收：`#mask.casting-sheet-on.notice_sheet_frame` height:100%→auto（max-height:100%＋body 內捲保留）。實駕：詳情卡 y292 h515，一屏內齊。
- **S-35** 獲聘 modal 重排：結果（AUD_PASS）行先→效果→簽約金一行（合約總額只講一次）；刪 `chanceVarianceNote` 含糊行＋`payContractNote` 重複金額兩個 push；「殺青嗰日先入帳」標籤改「殺青嗰日先結算」對位；獲聘 modal 刪「成功率約 X%」行（落選 modal 唔喺範圍冇郁）。
- **S-37** 殺青板對帳只留一段：刪「今次入帳係餘額…冇縮水」嗰段 push，保留 `payWrapNote(sh)` 括號版。
- **S-39** 生活費提示根源修正：日結板顯示嗰陣 dayIndex 已過翌日，舊 `livingCostDayEndHint()` 用 dayIndex 計星期早一日（審計圖週五活動、日期行已週六就係咁嚟）；改用完成日 `weekdayIdx((S.dayIndex|0)-1)`，只週六／週日完成嘅板先出提示。實駕：週一休息板冇生活費句（截圖 `22_dayboard_mon.png`）。
- **S-40** 支票唔再排最尾畀 fold 截：殺青分支記 `wrapNoteIdx105`，支票 `chk101Html` 以 splice 插喺殺青行之後、對帳行之前。
- **S-43** 記數簿：`ledgerStatsParts` 非壓力屬性只顯示數值（bar 比例照用 cap 計），壓力保留「N／100」。實駕截圖 `15_stats.png`：全格冇 /999、壓力 12／100。
- **S-44** 人情頁：`SEASON_COLLECT.card_biao_winter` status「已逾期」→「就嚟到期」（開局 1 月＝冬，第一日唔再有逾期債；金額／玩法冇郁；夏季嗰張已逾期唔屬開局冇郁）；`seasonCollectToast` 唔再原句重播卡面台詞，改短提示指向手帳人情頁。實駕第一日人情頁：阿標卡「就嚟到期」、toast 行 generic 句唔重複（截圖 `14_favor.png`）。
- **S-45** 進度頁遠幕合併：`renderProgressPane71` 加 `farMerged105`，第一個遠幕位出一行「第 loN–17 幕／未開放／完成前面幕數後逐幕揭曉。」（loN＝locked 非 detail 主線幕最小 n），其餘遠幕跳過；合併行保留 class `prog71-row far`。實駕：新遊戲出「第 4–17 幕」合併行（截圖 `13_progress.png`）。
- **S-48** 設定頁：BGM／音效／音量三行「未推出」死掣成組刪走，改一行灰字「音效／音樂 … 即將推出」。**銜接位**：設定 modal 渲染函數（settings-list 頂部）嗰行 `.settings-row` 就係 BGM 包將來換返真掣（set-bgm／set-sfx）嘅位置；prefs 欄位 bgmMuted／sfxMuted 冇郁。截圖 `08_settings.png`（「即將推出」只出現一次——初版 label 底＋右側各一份，已去重）。

## 測試

- 新增守門 `tests/test_ui105_static.py`：43 項全 PASS（含紅線 SAVE key／softRev）。
- 舊測試跟新规格更新（註明版本）：`test_loc96_logic.js`（S-25 確認流程＋說明卡，47 PASS）、`test_guidance34_logic.js`（S-28 新格式，ALL PASS）、`test_verify37_logic.js`（S-28 板面行，ALL PASS）、`test_progress71_logic.js`＋`test_progress71_static.py`（S-45 合併行，ALL PASS）。
- 其餘針對性舊測試：jan67／enc79 logic／aud91 logic＋static／loc96 static 全 PASS。
- 全套掃描入面 flash51／giglib36／pacing35／poster59／soft_tip_111／wrap38 等 FAIL 喺未改嘅 main clone 一模一樣，係既有狀態，唔係本包回歸。

## ⚠️ 规格衝突（要 parent／用戶裁決）

`tests/test_enc79_static.py` 護欄「事務所 loc-who 有何生信任進度＋E5 指向」要求 `enc79HoTrustLine` 3000 字內有「江湖撈家」字樣（源自巧遇設計 D 包護欄：事務所要標明信任進度通去邊，否則 E5 幾乎行唔到）；S-24（UI 審計 A 級）正正要刪走呢句結局路線劇透。本包跟審計做，嗰項護欄測試而家 FAIL（其餘 enc79 測試全 PASS）。緩解現況：信任數字＋「再加 X 到『下一階名』」提示仍在，只係唔再點名結局同門檻數字。要取捨邊邊行先，請 parent 裁決；裁決後同步改返 enc79 測試或 S-24 呈現。

## 實駕

Playwright 420×900 本地鏡像（port 8905），截圖存 `~/workspace/linji-work105c-verify/shots105c/`（repo 外）：03_b01_card、04_plan_editor、05_stress_inline、06_after_confirm、07_map、08_settings、09_hospital、10_checkup_confirm、12_agency、13_progress、14_favor、15_stats、16_film_sheet、17_notice_detail、18_wf4_event、20_story_first、21_story_narration、22_dayboard_mon。未有實駕圖：S-21（巧遇蓋過地點板，見上）、S-35／S-37／S-40（要行到試鏡結果／殺青日先出，靠 static 測試＋代碼路徑驗）。
