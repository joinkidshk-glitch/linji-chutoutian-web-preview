# v357 — 支線＋感情線複檢：系統性旁白口語化成層改書面語

日期：2026-11-21
基線：v356（main `40d5f07`，suite 398 PASS／9 FAIL）

## 做了甚麼

按語言硬規則（旁白／敘述／簡介一律香港式書面語，對白保留廣東話），將支線＋感情線複檢核實表標「系統性旁白口語化」嘅 76 處逐句重寫做書面語（唔係逐字換字，整句重寫，保留原意／事實／情緒／節奏）。

來源層分佈：
- 曉晴覆寫旁白（`ROMANCE_V158_OVERRIDES`＋enc158 離港變體，s6 B1–B11）：11 處
- choi299 變體旁白（s7 B1）：1 處
- 葉／蘇旁白＋notes＋synopsis（yip_so JSON，s8 B1–B3、B5–B11）：10 處
- ENC N lines＋選項標籤（s9–s16）：54 處（lan 5／lok 5／kong·shum·pang 5／wu·hon·ngai 12／mak 5／liu·luk 11／yip·ching 6／gu 3／chung 2）

做法：官方 qwen4-max 逐 node 分 17 批改寫，brief 帶敘述黑名單；程式閘門（對齊／標點／串層掃描／事實對照）＋人手逐句覆核（指代／性別對照原文上下文）；成批制——4 批因指代、性別、半角標點、術語漂移（「臨記→臨時演員」）不合格，成批重跑（加上下文註明）後合格先入版，冇一批保留原文。

## 機制同步（跟 v356 先例）

標籤書面語化令以下 substring 關鍵字失效，同步更新（邏輯不變）：
- GRANT229_ENC79 key：`first:mak_zhendong`「放低」→「把水放」；`beat:lok_cover`「企硬」→「堅持立場」、「唱住先」→「先唱再說」；`beat:ngai_repay`「下次先」→「下次再」；`beat:ngai_rain`「企埋一邊」→「站到一旁」；`heart:ngai_wingnaam`「認真記低」→「認真記下」；`beat:ching_rival`「留低」→「留下陪他」。
- enc79ChoiceFx 關鍵字：`first:mak_zhendong` has("放低")→has("把水放")；`first:yip_manji` has("唔出聲")→has("保持沉默")；`beat:lok_foreshadow` has("講兩句")→has("聊上兩句")；`beat:lok_cover` has("企硬")→has("堅持立場")；`beat:ching_rival` has("留低")→has("留下陪他")。
- `ENC79_FIRST_ALT98` swaps：麥震東初遇地點變體對（紅棉／獅子山）同步新句。

## 冇郁

- 對白句（角色 speaker／S／A lines）一律冇改；引號內原話冇改。
- 欄位串層 5 項（對白入 N／旁白入 A：s9 B4、s13 B1、s15 B3、s14 B6、s16 B3）唔屬旁白改寫，冇郁。
- (b) 類待潤飾措辭（同旁白句重疊除外）、soft 層鄧麗萍清理、4 文風、1 部分證實、s5 A3／s6 A8 冇郁。
- 事實／年份字串／數值／旗標／SAVE key（`starVolunteer_map_v19w`）／softRev 冇郁；index.html 行數不變（47,440）。

## 驗證

- 全套 suite：398 PASS／9 FAIL，同基線一致，九項全係 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。`qa296/derive296.json` 已還原。
- 測試 resync（邏輯斷言不變）：gig229_grant、r304、r308、r309、r315、sideline271、sideline273、sideline278、contra98、r294 釘句／釘 key 同步；hiu266 語體斷言按語言規則更新（對白拍廣東話／旁白拍書面語分開計）；sideline278 (6) 改驗 v357 書面語化標籤無口語字。
- Playwright 實駕（`~/workspace/linji-drive357/`）：R_hiu_meet 旁白新句在位、舊句清零、對白仍廣東話；R_yip_meet 旁白書面語渲染（截圖確認）；ENC 藍若曦 first N lines＋標籤書面語（數據層核實，ENC 常數喺 IIFE 內）。
