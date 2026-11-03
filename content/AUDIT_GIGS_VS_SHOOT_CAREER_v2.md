# AUDIT｜通告庫 vs PLAN_SHOOT_CAREER_SCHEDULE_v2（夠唔夠）

> 2026-11-03（Asia/Hong_Kong）｜用戶 t322u 經 tester：以「夠唔夠」檢視為先；**未改庫**。  
> 對照：`PLAN_SHOOT_CAREER_SCHEDULE_v2.md`。roleScale 用 v2 **附錄粗映射**（現庫尚無該欄）。  
> Soft≠PASS。

---

## 0. 一句結論

**種類骨架大致齊（五 type 年年有），但日數全面偏短、長檔／缺邊檔不足，單靠「只改現有欄」可以玩起步，要撐「自己排演藝生涯」建議：先抬現有全則＋少量加則補缺口。**

| 問 | 答 |
|---|---|
| 只抬現有 30 則欄位夠不夠開局？ | **勉強夠**（1988 映射後 12/13 檔有貨；缺寫真） |
| 夠不夠長期排期張力？ | **未夠**——缺寫真；MTV 稀；89–91 幾乎無電影／電視「長主線檔」映射；舊 `shootDaysHint` **八成以上低於 band** |
| 開工建議 | **先抬現有**（roleScale／shootBand／days／weekdays／deadline）→ 再 **加則 6–10／年** 補缺邊 |

---

## 1. 覆蓋缺口表（type × roleScale／shootBand）

### 1.1 1988（30 則）— 映射後件數

| roleScale | band | 件數 | 現況 days 落帶內 | 缺口／備註 |
|---|---|---:|---:|---|
| film_lead_big | 28–30 | 2 | 0 | 有 id（film_05／06）但 days 12／15 **嚴重偏短** |
| film_support_main | 20–24 | 2 | 0 | film_03／04：5／7 → 要抬 |
| film_support_small | 12–15 | 2 | 0 | film_01／02：2／4 → 要抬 |
| tv_lead_long | 20–24 | 2 | 0 | tv_06／07：8／10 → 要抬 |
| tv_support_main | 14–16 | 3 | 0 | 全短 |
| tv_cameo_short | 8–10 | 2 | 0 | 現 2 日 → 抬至 8–10 |
| rec_album | 10–14 | 3 | 0 | 含演唱會嘉賓粗歸 rec（可另議） |
| mtv | 2–3 | 1 | 1 | **僅 1**（rec_02）；建議再 +1–2 |
| ad_av | 3–4 | 6 | 1 | 多數 1–2 → 抬 3–4 |
| ad_print | 2–4 | 2 | 1 | ad_02 现 1 → 抬 |
| photobook | 5–7 | **0** | — | **缺邊：寫真集 0** |
| variety_ep | 2–4 | 4 | 2 | 兩則 1 日偏短 |
| variety_special | 4–7 | 1 | 0 | var_05 现 3 → 抬≥4 |

**1988 低於 band：25／30（83%）。**

### 1.2 1989–1992 一覽（粗映射）

| 年 | n | 缺 roleScale（0 件） | 低於 band |
|---:|---:|---|---:|
| 1989 | 37 | **film_lead_big、tv_lead_long、mtv、photobook、variety_special** | 33／37 |
| 1990 | 37 | **film_lead_big、tv_lead_long、mtv、photobook、variety_special** | 34／37 |
| 1991 | 37 | **film_lead_big、tv_lead_long、mtv、photobook** | 32／37 |
| 1992 | 30 | **tv_lead_long、mtv、photobook、variety_special** | 28／30 |

解讀：

- **電影長檔（28–30）**：僅 1988／1992 有「高」tier 可映射；89–91 **無** → 中期生涯缺「檔期炸彈」。  
- **電視長篇主線（20–24）**：1988 有 2；**89–92 無高 tier 電視**（粗映射下 tv_lead_long=0）。  
- **MTV**：幾乎只有 1988 一則；其後多年 0。  
- **寫真 photobook**：五年 **全 0**。  
- 舊 days 普遍 1–6，同 v2 電影／電視帶差一整個數量級。

---

## 2. 夠唔夠撐「自己排演藝生涯」（星期＋限期）

### 已有（抬欄後可立刻用）

- 短單（廣告 3–4、平面 2–4、MTV 2–3）↔ 長單（電影 12–30、電視 8–24）對比 → **日數張力**主要靠抬現有電影／電視。  
- 五 type 齊 → 板面唔會只有一種通告。  
- 1988 已有可映射嘅 lead／support／cameo／mtv／ad 多數檔。

### 未夠（玩法風險）

| 風險 | 原因 | 建議 |
|---|---|---|
| 中期無「長主線炸彈」 | 89–91 無 film_lead_big／tv_lead_long | 每年至少 +1 電影大檔、+1 電視長篇（或升現有高曝光則之 roleScale＋days） |
| 週末／平日無差異可排 | 現庫無 weekdays | 抬欄時 **刻意混**：廣告／沙灘週末；廠景平日；長劇一至六 |
| 賺快錢同長投資無寫真檔 | photobook=0 | **+1–2 寫真／年**（或廣告改一則） |
| MTV 太稀 | 多年 0–1 | 每 1–2 年 +1 MTV |
| 演唱會歸 rec_album 彆扭 | rec_04 類 | 可另 `live_guest` 或仍 rec、days 取 10–12 |

**數量：** 30–37／年 **唔使加到 60**；問題係 **band 覆蓋同日數真實度**，唔係張數。

---

## 3. 綜藝暫定 2–4／4–7 夠唔夠？

| 判斷 | 說明 |
|---|---|
| **夠用（建議暫留）** | 單集短劇／競技本來就短；同廣告短單一齊做「填隙」；大型特備 4–7 已同「唔搶長劇檔」分工 |
| 唔建議抬到電視客串 8–10 | 會同 tv_cameo 糊埋，手帳張力變鈍 |
| 可微調 | variety_special 下限維持 4；若賀歲夜特技要兩日廠＋一日綵排，取 **5–6** 即可 |

→ **綜藝暫定帶 OK**；用戶若覺得特備仍短，只改 special → 5–8，唔使動 ep。

---

## 4. 改庫開工建議（拍板用）

| 方案 | 做咩 | 何時 |
|---|---|---|
| **A｜先抬現有（推薦第一步）** | 1988 全 30：補 `roleScale`／`shootBand`／抬 `shootDaysHint` 入帶／`shootWeekdays`／`shootDeadlineDays`；手訂星期組合（平日／週末／一至六） | 用戶 OK 改庫即做 |
| **B｜加則補缺邊（緊接 A）** | 每年度優先：**photobook×1–2、mtv×1、film_lead_big×1（若缺）、tv_lead_long×1（若缺）** → 約 **+4–6／年**，1988 可先 +2–3（寫真＋多 1 MTV） | A 後同一輪或下一輪 |
| **C｜只加則不抬** | **唔建議**——現有電影／電視 days 離 band 太遠，新則反而同舊則衝突 |

**建議拍板句：**「先 A（1988 抬欄）→ 交 tester 手感 → 再 B 補寫真／MTV／長檔」。89–92 同樣 A→B 滾動。

---

## 5. 交用戶拍板（tester widget 可用）

1. 同意審計結論？先 A 抬現有，再 B 少量加則？  
2. 寫真／MTV／每年長電影＋長電視：要唔要做硬性配額？  
3. 綜藝暫定帶：留 2–4／4–7，定改 special？  
4. 是否而家開工改 `gigs_1988`（PLAN v2 改庫尚未 widget 明 OK）？

*完 — AUDIT_GIGS_VS_SHOOT_CAREER_v2*
