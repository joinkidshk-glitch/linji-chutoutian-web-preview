# v383 後期金錢自費試鏡帶（偏弱系統加強③）

用戶 2026-11-22 拍板「按建議次序開票」第三票（次序①情報站補位試鏡＋屋企留話簿 v381、②服裝自備戲服通告 v382 已落地）。方案來源：`~/workspace/linji-systems-balance-2026-11-22/REPORT.md`（GPT-6.2-sol 首選「自費試鏡帶」：第二、三年每季一次付費錄影棚試鏡帶，換另一類試鏡入場資格，七圍照常判定）。原則：唔開新玩法、買入場資格唔買分、唔改試鏡判定／頒獎／結局；唔郁贏線 0.875／E1 門檻 350／floor 140／warnLine 180。

## 定價（對 live 經濟做數，唔照抄報告）

| 參照 | 數值 |
|---|---|
| 1991 通告 pay 中位／p75（content/gigs_new.json 110 張） | $285／$607 |
| 1992 通告 pay 中位／p75（90 張） | $390／$1,089 |
| 真玩第二年現金中位（第四輪評估） | 約 $5,000 級 |
| 現有奢侈品級支出：最貴衫 | $1,500 |
| 日常支出：外貌課學費／醫院／禮物／生活費 | $40／$60／$10–65／$110 週起 |

定價：**按季種子 $1,200–1,800**（`1200 + ((qk*37)%7)*100`，qk＝季鍵 year*4+季；1991Q1＝$1,500）。理由：①跟最貴衫同級——都係後期奢侈品級別支出；②約等於 1991 年 4–6 張／1992 年 3–5 張中位通告收入、現金中位 24–36%，每季一次一年全買 4 次＝$4,800–7,200，定位係畀「後期錢冇去向」玩家買選擇，唔係必買；③flat scale（用戶 2026-11-15 拍板唔跟通脹）——季種子浮動跟 v381 按月定價先例一致，唔係通脹調整。

## 功能

- 何生事務所新打聽行動 `act_ho_tape383`「自費拍攝試鏡帶」：1991 年起開放，每季一次。掣原位常駐——停用態（1990 年「此行動將於 1991 年開放。」／本季已用「本季已使用。下季可再次使用。」）半透明顯示＋狀態字（GPT 規格，唔隱藏）。
- 流程（專屬流程，跟 `act_ho_repay` 先例截走，唔經通用打聽確認頁）：撳掣 → 類別選擇 modal（電影／電視劇／唱片通告／廣告／綜藝五張紙卡，每張顯示實價，44px 觸控）→ 揀類後先揀通告（揀唔到唔收錢）→ 確認付款（「確認後將即時支付 $X，拍攝並寄出試鏡帶，取得一項{類別}通告的試鏡資格。本次付款將使用本季一次機會。試鏡按一般規則判定，不保證入選。」）→ 扣錢 → 通告以「自費試鏡」標籤喺其地點通告欄上板（豁免季節／NAT92，7 日試鏡窗就係檔期本身），卡面加「自費試鏡 · 請於 {日期} 前到場試鏡」行。
- 選通告（`tape383PickGig`）：自選媒介類別，由嗰類揀一張未消費、無 trigger、tier 窗 [玩家級數, +1] 嘅真通告（跟 v381 補位同口徑），季鍵＋類別種子定死，讀檔唔重擲。唔加新通告（庫總數 330 不變）。
- 試鏡照常 aud91 判定（唔改成功率公式、唔可付費重試、唔設主線／E1 必經；每類保留免費途徑——普通板照舊）。付費買資格嘅通告唔再疊 v382 自備戲服閘（`costume382GigReq` 排除）。
- 到期：保留後 7 日未試鏡失效（`tape383Tick`，advanceDay）；已試鏡／已開拍／已完成轉 used。唔耗日（同打聽行動一致，試鏡本身耗一日；同 GPT 原案「另佔半日」偏差——現行系統冇半日機制，時間成本喺試鏡嗰日），唔計茶座上限。
- 狀態 `S.tape383` 單槽 {qk, gigId, locId, title, type, state, keptDay, price}；normalizeSaveObj 補 `o.tape383=null`，舊存檔兼容。唔改 SAVE key／softRev／產品 `?v=`。

## UI（GPT-6.2-sol 規格，原稿 `linji-drive383/gpt_ui383.txt`，brief 寫明終極目標原生 iOS app）

掣名「自費拍攝試鏡帶」；類別選擇單欄紙卡（撳卡即去付款確認，GPT 嘅「選中＋繼續」兩步合併為一步，觸控同資訊不變）；標籤「自費試鏡」灰藍紙底 `#dce6ea`、深藍墨字 `#243e4a`（同「補位」淡赭區分）；完成提示「已取得試鏡資格」＋地點＋截止日期；停用態原位顯示。方向二「紙本手帳 · 實物劇組」。

## 編輯點（index.html，淨 +163 行，49119→49282）

- CSS：.bp-tag.tape383／.gt-pill.gt-tape383／.tape383-note／.tape383-cat（~4220）。
- normalizeSaveObj 補 `o.tape383=null`。
- MOCK_ASK.agency_ho 加 `act_ho_tape383` def；mockAskDefs 按 tape383State 動態改 moneyCost/cost/hint；add 段 isTeaAct 排除＋專屬流程截走＋停用態 class；applyMockAsk 加保險分支（唔經通用流程）。
- advanceDay 加 tape383Tick；gigsForLocSeasonBoard 加 isTape383 豁免（兩處）；gigCardHtml 標籤＋限期行；詳情頁 cn-sum-row 截止日行；gigBoardTeaserHtml pill；costume382GigReq 排除。
- TAPE383 模組（tape383QuarterKey/Price/Slot/State/PickGig/FmtDay/LocName/OpenPicker/Confirm/Tick/KeptGig/Label/DeadlineText）插喺 INTEL381 模組完之後。

## 驗證

- 邏輯測試 `tests/test_tape383_logic.js` 全 PASS（開閘三態、定價帶、五類選通告＋種子定死、保留／到期／used）。
- Resync `qa383/resync383.py`（difflib old→new 單次掃描 dict 查表；old 備份 /tmp/index_v382.html，linemap /tmp/linemap383.json）：修 9 檔（gift185／reconfirm236 呼叫點 13→14／rom159 含全佳行／rom176／tang152／tang171／tang173／text125／travel114 含 2 個新 FREE 呼叫點 43533／43553）；總行數 pin 49119→49282（鏈 append「＋v383 +163」）；openLoc DEF 44279→44435。
- suite：第一跑 393/18 → resync 後 9 個新 FAIL 逐個直接跑 PASS → 全套重跑 **402 PASS／9 FAIL**（基線 401＋新邏輯測試 1，九項 pre-existing 不變）。輸出 `~/workspace/suite383_v3.txt`。
- Playwright 實駕 `~/workspace/linji-drive383/probe383.py`：種子 1991-01-01＋現金 $10,000 → 事務所「自費拍攝試鏡帶」$1,500 → 揀電視劇 → 確認付款 → 扣 $1,500、slot kept → 通告欄「自費試鏡」標籤＋截止日行 → 本季已用停用態 → keptDay 拉後 8 日瞓覺 → expired。截圖 probe383_*.png，數據 probe383.json。
