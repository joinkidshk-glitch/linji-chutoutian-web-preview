# NOTES v20a20 — Weave Phase 3-2：報紙花邊入傳聞池（鏈 D 跨系統拼合）

串聯規劃鏈 D 落地：報紙由「睇完即棄」變成拼圖原料——有關聯嘅花邊短訊見報後入埋手帳傳聞頁做「報紙碎片」，可以同聽聞碎片跨系統拼合，拼出同一條情報。

## 研究結論

- **邊幾則花邊有關聯**：花邊池 16 則入面得兩則掂到現有情報線——陸柏言（紅磡開唱）同廖炳星（清水灣開鏡）；**麥震東一則都無**（池入面根本無佢個名），所以今次補寫一則麥震東花邊（煞科宴缺席）先令三線齊全。其餘 13 則（魏詠男／葉敏芝／蘇芷茵／程天諾＋時代質地）同現有三條 merged 情報線無關聯，維持純 flavor 唔入池。
- **拼合配對靠咩鍵**：`MERGE_PAIRS` 以碎片 `id` 精確配對（`findMergePair` 雙向查 a／b），拼合走 `mergePickedRumors()`：兩塊碎片 state 轉 merged、unshift merged 行（id＝pair.merged）、`setIntelFlag(pair.merged)` 置情報旗。碎片要 state 令 `rumorStateLabel` 解作「剛聽聞」（normal）先揀得起。
- **報紙入池現行路徑**：`pushNewspaperRumor(edition)` 頭條＋短訊逐行入池（id `paper_<editionId>[_<eventKey>]`、source「報紙」、state teased＝已知、唔揀得），靠 id 去重；summary 同 side 一律跳過。今次就喺 side 跳過位開一條支線。

## 今次改動

- `PAPER_SIDE_ITEMS`：陸柏言／廖炳星兩則加 `id`（`side_lu_concert`／`side_liao_newfilm`）；池尾新增第 17 則麥震東花邊（`side_mak_wrap`：「麥震東新片煞科宴缺席，劇組話佢唔舒服」）。`paperSideItemForDay` 回傳多 `sideId` 欄帶落 edition。
- 新增 `SIDE_PAPER_FRAGS` 登記表（sideId → 固定碎片 id `paperfrag_*`）＋`paperSideFragmentFor(s)`：只有登記咗嘅 side 先生成碎片描述，其餘一律 null。
- `pushNewspaperRumor`：side 短訊改行新支線——有碎片描述就入 `rows`，落池時生成碎片行：`source:"報紙花邊"`、`fromPaper:true`、`paperFrag:true`、`state:"normal"`（剛聽聞、可揀選），標題／內文照剪當日見報嘅 headline／dek 原文。碎片 id 固定唔跟 edition id，同一則花邊隔幾日再見報都只入池一次（沿用既有 id 去重）。花邊 fameDelta 0 不變，入池唔經聲望路徑（守 P0-2／1-1 口徑）。
- `MERGE_PAIRS` 加三條跨系統對（經典三對原文不動）：報紙碎片 × 一塊指定聽聞碎片 → 同一 merged id，拼到照樣置情報旗、行現有情報使用點；merged 文案按報載證據改寫（唔照抄經典版）：
  - `paperfrag_lu_concert` × `rumor_lu_baiyan_angry` → `rumor_lu_baiyan_breakdown`（片場發脾氣＋紅館開唱迫近）
  - `paperfrag_liao_newfilm` × `rumor_liao_bingxing_talk` → `rumor_liao_bingxing_money`（密談＋新片開鏡擔正）
  - `paperfrag_mak_wrap` × `rumor_mai_zhendong_hurt` → `rumor_mai_zhendong_hide_injury`（片場整親＋煞科宴缺席）

## 防護

- P0-3：碎片顯示同其他傳聞行一樣經 `renderRumorPane`／確認彈窗嘅 `displayRumor` 過濾；三則關聯花邊本身無過濾敏感詞（測試有守），唔會出現原文／軟化版不一致。
- P0-2：頭條／短訊入池邏輯不變（內置 #106 自測以 source「報紙」＋state teased 計數，碎片用唔同 source／state 唔會撞數）。
- 唔改 SAVE key、softRev、?v=。

## 測試

- 新增 `tests/test_weave32_logic.js`（35 項）＋`tests/test_weave32_static.py`（25 項）：登記表／sideId 傳遞／入池／去重／無關聯唔入池／三線跨系統拼合端到端（真 `mergePickedRumors`＋置旗）／經典對不變／P0-3 守衛。
- 全套舊測試（P0、P0-3、Weave 1-1／1-2／1-3、2-1／2-2／2-3、3-1）無回歸；全檔 script `node --check` 通過。

## 未做（留待鏈 D 後段）

- 規劃鏈 D 第 3、4 拍（拼出後嘅通告應對選項、報紙回寫玩家行為）未喺今次範圍；葉敏芝整容疑雲一線現有系统未有 merged 情報／情報旗，今次唔新開線，佢則花邊維持 flavor。
