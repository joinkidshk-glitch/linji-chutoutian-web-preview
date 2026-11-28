# NOTES V20A425 — UI 第二十七輪（B→A 小修）

基線：v424 main `9356384`（Pages byte-identical，SHA-256 `50b037681283eef5b2be0034e99c63b7f0049f65c09379862ab6f35b75837c46`，suite 430／9）。
打磨方向經 GPT-6.2-sol 加強方案（`linji-ui-audit-2026-11-24z/GPT_PLAN425.md`）再實裝；美術票範圍（立繪白邊、非何生場景錨點）本輪不掂、不出圖。

## 改動（只改呈現層與文案連貫）

### 1. 篩選條件明示（doScout 板頭）
- 板頭新增常駐狀態行：`排序：X · 媒介：全部`；篩選生效時顯示媒介紙籤＋「解除篩選」掣（44px），解除後保留排序、焦點落狀態行。
- 整理掣改名「排序與篩選」，選項加 `aria-pressed`；狀態行 `tabindex=-1`。
- 細板（≤3 張）承接既有媒介篩選時照篩選出卡並顯示媒介＋解除篩選（`lockedShown392` 統一用篩選後列）。
- 「返去地點」改「返回地點」；板頭統計「可接」改「可報名」；lead 改「達標可報名試鏡（耗一日）」。

### 2. 金額對齊
- 詳情合約三欄改共用標籤列／主金額列／附註列（`cn-money-main425`／`cn-money-note425`）：主金額同字級、同基線、左對齊、等寬數字；欄內改由頂排起（撤 space-between 底部對齊），末欄撤頂線偏移。
- 範圍寫「預計片酬範圍 $1,694–$2,002」，不再用「約酬」；簽約金主金額與「獲聘後即收」分層；預期日薪值撤疊「約」。
- 跨屏金額統一 `$` 緊貼千分位（HUD、入帳 delta、支票、獲聘行、存款、拍攝簿、待入帳行）；「約酬」改「預計片酬」，「完成約酬」改「完成片酬」，合約鎖定行改「預計片酬範圍」。
- 短屏（≤760px 高）合約與分段收緊、詳情紙 max-height 94dvh，檔期段保留首屏。

### 3. 排程鎖定標籤切字修復（GPT second opinion 觸發）
- GPT 首評 86b／86c 為 C：週一至週三日格「拍攝檔期已定」左右被裁切。修復：緊湊日格鎖定標籤縮短為「檔期已定 · 不可改」（全句「拍攝檔期已定」仍在編輯摘要與詳情可讀），同步 `test_v400_logic.js` 釘位。
- 重截量度（`recapture86_measure.json`）：三個鎖定格「檔期已定」56px、「不可改」42px，`scrollWidth=clientWidth`、`withinCard=true`；GPT 重評 86b／86c 均升 B。

### 4. 試鏡語意與底部層級
- 印章「可報名試鏡」／「試鏡報名未開放」；主掣「報名試鏡」；返回「返回通告欄」；獲聘 toast「劇組通知：獲聘！」。
- 詳情底部常駐成本句「試鏡需用 1 日，能否獲聘視乎試鏡結果。」；主操作 52px 唯一主掣，人情免試鏡降次操作；鎖定但人情可用時人情升主操作、修正去向降次操作。
- 確認框標題「報名試鏡」、主掣「確認報名」；`confirmSpendDay` 新增 opts（title/bodyHtml/confirmLabel/cancelLabel/onDismiss，預設行為不變）；取消或 dismiss 重開詳情、不耗日。
- 流程句只保留簽約金時機；板卡「可接通告 · %」改「可報名試鏡 · 成功率 %」；進度「接通告 N／M 張」改「完成通告」；商店／衣櫃／約會／教學板相關文案同步。

## 量度（focus425_after5，390×844／430×707／430×932）
- 板頭：三視口各區重疊 0；篩選 17→11 張、解除回復 17 張、排序保留；選單選中態 aria-pressed=true。
- 合約：主金額基線差 0px、標籤差 0px（三視口）；檔期段首屏全入（430×707 底 537.4 ≤ 捲動區底 561.4）。
- 真玩：取消確認 day 不變（1→1）、詳情重開；確認報名 day 1→2、pendingAud=1、入等消息。
- 觸控：主操作 52px、返回 52px、解除篩選 44px、鎖定去向 48px。

## 測試
- 新增 `tests/test_v425_static.py`；同步更新 v392／v396／v397／v398／v399／ui108／text108／s30text115／s30dedup117／wrap38／guidance34／progress71／story172／story179／aud91／qa101／v400 釘位（意圖不變，文案與結構跟隨）。
- 行號釘 resync（`qa425/resync425.py`，difflib 對位、內容逐字核實純漂移）：gift185／tang171／tang173／tang152／rom159／rom176／travel114／text125；總行數鏈 53759→53823（UI27 +64）。
- Suite：最終 TOTAL PASS 428 FAIL 12（`suite425_final.txt`）；9 項為穩定 pre-existing（flash51／slot50／soft_tip_111／start53／weave43／weave44／weave49／wf5_87／wrap38），額外 3 項（fx129／fx139／newspaper214_award）逐個直接覆驗全部 PASS，屬 suite 波動（fx139 首次覆驗 ffprobe 讀片失敗、重跑全 PASS）。排程標籤修復前一輪 suite 為 431／9。

## 不變量
玩法、數值、結局條件、SAVE key `starVolunteer_map_v19w`、softRev、產品 `?v=`、頒獎贏線 0.875 全部不變；不手改 source 年份。
