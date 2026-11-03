# PLAN｜拍攝生涯規劃（通告排期）v2

> 2026-11-03（Asia/Hong_Kong）｜**取代 v1 日數下限**。  
> **用戶拍板**（經 tester；來源回覆 t320u）：`shootDaysHint` **唔再**用「初≥3／中≥5／高≥7」；改按 **通告類型＋角色檔**。  
> **保留**（用戶未否決）：`shootWeekdays`／`shootDeadlineDays`／逾期罰則（§3＝v1）。  
> Soft≠PASS；全量出圖 HOLD。OK 本表後先改 `gigs_1988`（再滾 89–92）。iOS／eng stub 請改跟 v2。

**前版：** `PLAN_SHOOT_CAREER_SCHEDULE_v1.md`（日數下限作廢；其餘 schema 名沿用）。

---

## 0. 目標

玩家要自己排演藝生涯：拍攝日數跟**真實通告體量**、限定可拍星期、限期內拍完。

---

## 1. 欄位 schema

| 欄 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `type` | string | ✅ | 既有：`電影`／`電視劇`／`廣告`／`唱片通告`／`綜藝`（…） |
| `tier` | `初`\\|`中`\\|`高` | ✅ | 既有；**唔再**驅動日數下限（可留作板位／難度） |
| `roleScale` | string enum | ✅（新） | 角色／製作檔；見 §2；決定 `shootBand` |
| `shootBand` | `[min,max]` int | 建議寫入 | 作者對照帶；QA 校驗 `shootDaysHint` ∈ band |
| `shootDaysHint` | int ≥1 | ✅ | **實際要排入手帳嘅拍攝日數**；必須落喺 §2 對應帶（取帶內整數；作者可選中位或偏短／偏長） |
| `shootWeekdays` | int[] | ✅（新） | 可拍星期；**1=一 … 7=日** |
| `shootDeadlineDays` | int ≥1 | ✅（新） | 自**獲聘日**起日曆日限期；建議 `≥ ceil(shootDaysHint × 7 / \|weekdays\|) + 2` |
| `shootHint` | string | 可選 | 既有拍攝注意 |

### `roleScale` 枚舉（v2）

| roleScale | 適用 type | shootBand（日） | 用戶書面對照 |
|---|---|---|---|
| `film_lead_big` | 電影 | **28–30** | 主角／大製作 |
| `film_support_main` | 電影 | **20–24** | 一般／主要配角 |
| `film_support_small` | 電影 | **12–15** | 小成本／小配角 |
| `tv_lead_long` | 電視劇 | **20–24** | 女主／長篇（男主／第一男主同檔） |
| `tv_support_main` | 電視劇 | **14–16** | 主要配角 |
| `tv_cameo_short` | 電視劇 | **8–10** | 客串／短劇 |
| `rec_album` | 唱片通告 | **12–14**（特短可 **10**） | 唱片錄音 |
| `mtv` | 唱片通告 | **2–3** | MTV |
| `ad_av` | 廣告 | **3–4** | 廣告（賺快錢短單；影音） |
| `ad_print` | 廣告 | **2–4** | 平面／雜誌封面 |
| `photobook` | 廣告或其他 | **5–7** | 寫真集 |
| `variety_ep` | 綜藝 | **2–4** | **暫定**（用戶表未列）：單集短劇／競技 |
| `variety_special` | 綜藝 | **4–7** | **暫定**：大型特備／外景伴舞 |

> 綜藝兩行＝劇本暫定，方便 1988 五則對齊；用戶要改數字就改呢兩行。

### 引擎義務

1. 手帳 shoot：星期 ∈ `shootWeekdays`。  
2. 排滿 `shootDaysHint` 先當完成。  
3. 逾 `shootDeadlineDays` → §3 罰則一次。  
4. QA：`shootDaysHint` 必須 ∈ `shootBand`（或 ∈ §2 表）。  
5. **廢止** v1「按 tier 抬日數下限」。  
6. 缺欄 fallback（過渡）：`shootWeekdays=[1,2,3,4,5]`；`shootDeadlineDays=max(14, shootDaysHint*3)`；`roleScale` 缺則按 `type`+`tier` 粗映射（見附錄），並 QA 紅燈。

---

## 2. 日數對照總表（用戶拍板）

| 類型 | 角色／檔 | 拍攝日數 |
|---|---|---|
| 電影 | 主角／大製作 | 28–30 |
| 電影 | 一般／主要配角 | 20–24 |
| 電影 | 小成本／小配角 | 12–15 |
| 電視 | 女主／長篇 | 20–24 |
| 電視 | 主要配角 | 14–16 |
| 電視 | 客串／短劇 | 8–10 |
| 唱片錄音 | （標準） | 12–14（特別短可 10） |
| MTV | — | 2–3 |
| 廣告 | — | 3–4 |
| 寫真集 | — | 5–7 |
| 平面／雜誌封面 | — | 2–4 |

---

## 3. 逾期罰則（保留 v1；用戶未否決）

觸發一次（掉單）；唔每日疊加。

| 項 | 數值 | 玩家面文案 |
|---|---|---|
| 結果 | **掉單**（唔發該則 pay／fame／popularity） | 「限期內未完成拍攝，組製取消你的檔期。」 |
| 聲望 | fame **−8**（`tier=高`：**−12**） | 「臨時缺席的消息傳開，圈子裡對你的評價滑了一截。」 |
| 人氣 | popularity **−5**（高：**−8**） | （可只內部） |
| 壓力 | stress **+12**（高：**+16**） | 「被放鸽子的羞恥感壓在心口，晚上怎麼也睡不穩。」 |
| soft | `rel_ho` **−1**（可選） | 「何生只丟下一句：下次再甩通告，別怪我不再幫你擋。」 |

通告卡／手帳提示：「拍攝限期：獲聘後 {n} 日內；可拍：{weekdayLabel}；尚欠 {remain} 日。」

---

## 4. 1988 抽樣 3 則（對齊現庫 id；建議值尚未入 LIVE）

### A｜廣告影音｜`gig_1988_ad_01`「星聲」隨身聽潮流街舞宣傳片

| 欄 | 現況 → 建議 |
|---|---|
| type / tier | 廣告／初 |
| roleScale | → `ad_av` |
| shootBand | → `[3,4]` |
| shootDaysHint | 2 → **3** |
| shootWeekdays | → `[1,2,3,4,5]` |
| shootDeadlineDays | → **10** |

### B｜電影小配角｜`gig_1988_film_01`《鐵血英雄傳》火海槍手替身

| 欄 | 現況 → 建議 |
|---|---|
| type / tier | 電影／初 |
| roleScale | → `film_support_small` |
| shootBand | → `[12,15]` |
| shootDaysHint | 2 → **12** |
| shootWeekdays | → `[1,2,3,4,5,6]` |
| shootDeadlineDays | → **21** |

### C｜電視長篇主線感｜`gig_1988_tv_06`《城寨暗夜1988》臥底警察阿鋒

| 欄 | 現況 → 建議 |
|---|---|
| type / tier | 電視劇／高 |
| roleScale | → `tv_lead_long`（臥底主線；非客串） |
| shootBand | → `[20,24]` |
| shootDaysHint | 8 → **22** |
| shootWeekdays | → `[1,2,3,4,5,6]` |
| shootDeadlineDays | → **35** |

---

## 5. 附錄｜缺 `roleScale` 時粗映射（僅 fallback）

| type | tier | → roleScale |
|---|---|---|
| 電影 | 高 | `film_lead_big` |
| 電影 | 中 | `film_support_main` |
| 電影 | 初 | `film_support_small` |
| 電視劇 | 高 | `tv_lead_long` |
| 電視劇 | 中 | `tv_support_main` |
| 電視劇 | 初 | `tv_cameo_short` |
| 廣告 | * | 標題含「平面」「海報」「雜誌」→ `ad_print`；否則 `ad_av` |
| 唱片通告 | * | 標題含 MV／mtv → `mtv`；否則 `rec_album`（特短作者可手設 10） |
| 綜藝 | 高 | `variety_special` |
| 綜藝 | 初／中 | `variety_ep` |

---

## 6. 落地順序

1. tester／iOS 收 v2（本檔）— **eng stub 改日數邏輯：跟 roleScale／shootBand，唔跟 tier 下限**  
2. 改 `gigs_1988.json` 全則：補 `roleScale`／`shootBand`／抬 `shootDaysHint`／補 weekdays＋deadline  
3. 滾 1989–92  
4. tester 覆測：短廣告、長電影替身、長劇主線、逾期一次  

---

## 7. 已拍板 vs 暫定

| 項 | 狀態 |
|---|---|
| 按 type＋角色檔日數表 §2 | **用戶拍板** |
| weekdays／deadline／逾期罰 | **沿用**（未否決） |
| 綜藝 band | **暫定** |
| 星期編碼 1=一…7=日 | 沿用 |
| 缺欄 fallback | 沿用平日＋`max(14,days×3)` |

*完 — PLAN_SHOOT_CAREER_SCHEDULE_v2*
