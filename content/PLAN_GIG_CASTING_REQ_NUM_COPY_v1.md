# PLAN｜通告 Detail 條件欄：現值／門檻句式 v1

**日期：** 2026-11-03（Asia/Hong_Kong）  
**觸發：** 用戶拍板——條件欄要顯示數值（玩家現值／門檻），唔淨寫合／未合；禁差N、你X、≥；書面語。  
**範圍：** **招募單 Detail 條件欄**（十一欄之「條件」）。列表短卡／`gateShortReason` 板頭仍跟 `PLAN_GIG_CARD_PLAYER_COPY_v1`（唔顯示差額／你X）。  
**對齊：** `PLAN_GIG_CASTING_NOTICE_DETAIL_v1`、`PLAN_GIG_CARD_PLAYER_COPY_v1`、`HANDOFF_DS_PLAYER_ZH_FILTER_v1`、`COPY_STYLE_HK_LEXICON.md`  
**Soft≠PASS**／出圖 HOLD  
**交：** iOS 改 stub（建議跟 ?v=18v 下一版）；tester 抽樣

---

## 0. 拍板一句

條件列：**同時顯示「現」同「要求」**，再標合／未合。數字只作組製標示，**唔**用「差 N」「你 X」「≥」「>」。

---

## 1. 鎖死句式（引擎字串表）

`{名}`＝§STAT_LABEL 中文（演技／台風／外貌／體力／智商／魅力／聲望／人氣）。  
`{cur}`＝玩家當前整數；`{need}`＝該通告門檻整數（`req`／聲望地板原值）。

| 狀態 | 句式（一字勿改骨架） |
|---|---|
| 能力／人氣 **已達** | `{名}：現 {cur}／要求 {need} · 合` |
| 能力／人氣 **未達** | `{名}：現 {cur}／要求 {need} · 未合` |
| 聲望 **已達** | `聲望：現 {cur}／這檔要求 {need} · 合` |
| 聲望 **未達** | `聲望：現 {cur}／這檔要求 {need} · 未合` |

**合／未合：** `cur ≥ need` → 合；否則 未合（比較只內部用 `≥`，**玩家面字串禁止寫出 ≥ 或 >**）。

**一行一例：**
- `演技：現 25／要求 30 · 未合`
- `體力：現 40／要求 35 · 合`
- `聲望：現 12／這檔要求 20 · 未合`

多條件：每項一行，順序跟 JSON `req` key 出現序；聲望地板另起一行置底（或置頂——與現 stub 一致即可，勿混入「差」字）。

---

## 2. 禁用／可用

| 禁用（玩家面） | 可用 |
|---|---|
| `差12`、`演技差5`、`聲望差N` | `現 {cur}／要求 {need}` |
| `你25`、`（你 25）`、`你而家 Y` | `現 {cur}` |
| `≥30`、`>515`、`演技 > 30` | 斜線分隔 `現 …／要求 …` |
| `條件未夠（演技差5）` | `· 合`／`· 未合` |
| 硬鎖、唔能試、有板 | （狀態另欄：招募中／暫未能報） |

---

## 3. 與舊規格關係

| 檔 | 改動 |
|---|---|
| `PLAN_GIG_CASTING_NOTICE_DETAIL_v1` §3.7 | **本拍板覆寫**：Detail 條件改顯示現／要求；`SHOW_REQ_THRESHOLD` Detail＝**true**（用本表句式，唔用 MV 裸 `>N`） |
| `PLAN_GIG_CARD_PLAYER_COPY_v1` §2.5 | **列表卡／短卡**仍可用合／未合、唔顯示數字；**Detail 改跟本檔** |
| `NOTES_V18V` | stub 曾 `SHOW_REQ_THRESHOLD=false` → 下一 preview 版改 true＋本句式 |

板頭總述仍可：`暫未能報 · 條件未合`／`可搏一搏 · 條件未齊`（無數字）。

---

## 4. iOS 實作備註

1. Detail `reqHtml`／條件 cell：逐項套 §1。  
2. **勿**回退拼接 `差${need-cur}` 或 `你${cur}`。  
3. 色：合＝既有通過色；未合＝既有警示色（可選；文案已自足）。  
4. 缺 `req` key 唔顯示該行；聲望無地板則唔顯示聲望行。  
5. 推版標 NOTES（建議 v18x 或跟現流水）。

---

## 5. QA（tester）

1. Detail 條件：見 `現 N／要求 M · 合|未合`；**無**差N／你X／≥／>。  
2. 未合項數字正確（現＜要求）；合項現≥要求。  
3. 列表短卡仍可無數字（唔強制本輪改短卡）。  
4. Soft≠PASS。

---

## 6. 交收

- 本檔：`PLAN_GIG_CASTING_REQ_NUM_COPY_v1.md`  
- 已改：`PLAN_GIG_CASTING_NOTICE_DETAIL_v1` §3.7、`HANDOFF_GIG_CASTING_NOTICE_DETAIL_v1`  
- **請 iOS** 套句式上板；**請 tester** 上板後抽樣

Soft≠PASS · 出圖 HOLD
