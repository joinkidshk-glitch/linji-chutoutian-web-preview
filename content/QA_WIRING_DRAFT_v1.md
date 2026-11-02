# QA｜WIRING_DRAFT_v1 對表覆測（文件｜非 browser）

> **範圍：** `content/WIRING_DRAFT_v1.md`（store 副本同 size＝53085；未改 story JSON／不出圖／不做 1989）。  
> **對照 JSON：** `story_detail_c1_to_c17.json` v1；`story_detail_romance_vera_hiu_choi.json` v1.1；`…_lan_xu.json` v2.1；`…_tang.json` v1.1；`story_detail_rival_mentor.json` v2.1；`gigs_1988.json` v2.1.1；`cast_main.json`／`worldview.json`。  
> **Canon：** `PLOT_MASTER_PLAN_v1.4-DS.md`、`PLOT_DETAIL_UNLOCK_v1.md`。  
> **Soft 對照：** `QA_SOFT_NITS_FIX_v1.md` leftover（**HOLD**，唔當 FAIL）。  
> **規則：** Soft≠PASS・唔 publish；配線草案可 **PASS with nits**；本輪只報告、**未改**任何 content JSON。  
> **時間：** 2026-11-02 23:46（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| id 一致性（C1–C17／E01–E10／romance／rival／gigs 關鍵欄） | **PASS** |
| flag 一致性（Tang 雙閘／threshold=2／meet=[]／stub→met；romance／Pack3 抽樣＋關鍵全檢） | **PASS** |
| 範圍（C1–C17＋romance＋Tang＋Pack3＋gigs 標註；無越界改 1989／出圖／改 story 正文） | **PASS** |
| Soft leftover 同向（未誤寫成已修；未提相反 wiring） | **PASS**（同向；見 nits：徐 tier 未列入 §8 清單） |
| UNLOCK／MASTER（尤其 C14↔T6） | **PASS** |
| Soft remaining（HOLD） | **NIT／HOLD**（不升 FAIL） |
| 出圖 | **暫緩** |

**出圖仍暫緩。** Soft leftover **仍 HOLD**。本輪 **唔 publish**。

---

## 1. id 一致性

| 包 | 抽樣／全檢 | 結果 |
|---|---|---|
| 主線 C1–C17 | coverage 17／missing=[]；draft 表 id＝JSON `nodes[].id` **全對** | **PASS** |
| E01–E10 | `C17.endings_catalog` 名稱硬鎖與 draft §3 一致（穩陣男演員…未出頭） | **PASS** |
| Pack1 15 | `R_vera_*`／`R_hiu_*`／`R_choi_*` id＋`flags_written` 與 draft §4.1 **0 mismatch** | **PASS** |
| Pack2 11（含 stub） | lan／xu／`R_tang_meet_stub` id＋fw／`linksMain`／`conflict` 與 draft §4.2 **0 mismatch**；`R_xu_crisis` conflict=`T6`＋linksMain=`[C14]` | **PASS** |
| Tang 5 | `R_tang_meet`…`ending` id／openConditions／fw 與 draft §4.3 一致 | **PASS** |
| Pack3 40 | 8 弧 ×5；expected ids missing/extra=[]；arcs.linksMain 與 draft §5.1 一致 | **PASS** |
| gigs_1988 | 30 則；`eraTag`／`boardPriority`／`seasonWeight`／`boardNote`／`discoverNote`／`loc` **30/30**；version **2.1.1** | **PASS** |
| loc | `tvb_longmen`×7（gigs）；顯示名層「星河」；worldview 龍門顯示＝0 | **PASS** |

**C 選擇支抽樣：** C1／C5／C7／C9／C10／C12／C14／C15／C17 choice id＋effects.flags 與 draft「選擇寫入摘要」一致。

**計數：** 主線 17；感情 31（15+11+5）；對手 40；unique flags／條件代幣 **241**（含 `rel_tang_threshold`）—與 draft §10 一致。

---

## 2. flag 一致性（Tang 重點）

| # | 項 | JSON 實際 | draft | 結果 |
|---|---|---|---|---|
| 1 | meet `openConditions=[]` | 檔級 `meet=[]`；`R_tang_meet.openConditions=[]` | §4.3 同 | **PASS** |
| 2 | push1+ 雙閘 | push1／push2／crisis／ending＝`[flag_tang_open, rel_tang_threshold]`；檔級 `pushAndAfter` 同 | §4.3 同 | **PASS** |
| 3 | `rel_tang_threshold=2` | 檔級＝2 | §4.3 同 | **PASS** |
| 4 | stub→`flag_tang_met` | choice `C_tang_meet_keep_contact` flags=`[flag_tang_met]`＋stats.rel_tang=1；**節點** `flags_written` 仍 `[flag_tang_open]` | draft 明確標 Soft leftover（§4.2 備註＋§8#4） | **PASS**（同向 Soft） |
| 5 | `flag_tang_open` 正式寫入 | `R_tang_meet`／`C_tang_meet_data` | 註冊表＋§4.3 | **PASS** |
| 6 | Pack1 裸旗＋alias | 裸 `hiu_*`／`choi_*` 15；`qa.flagAlias` 15 鍵；draft §4.1／§7 指引引擎讀 alias | **PASS**（同向 Soft） |
| 7 | Pack3 ending `parallelOk` | 8 ending 全 `true`；僅 `A_fong_crisis=false`；draft §5 Soft outstanding／§8#6 | **PASS**（同向 Soft） |
| 8 | Choi `linksMain`／`C_choi_*` | `R_choi_crisis.linksMain=[C13]`；choice ids `C_choi_*` | draft §4.1 | **PASS** |

---

## 3. 範圍／非目標

| 聲稱 | 核對 |
|---|---|
| 範圍 C1–C17＋romance＋Tang＋Pack3＋gigs 標註接線 | draft 章節 §3–§6 齊；與 JSON 對得上 |
| 未改 story JSON／gigs／index | draft §10「本輪觸碰檔」僅 md＋store 複製；本 QA **未改** JSON |
| 不做 1989–1992 年庫／不出圖／不 Soft 重寫 | §1 非目標＋§9 暫緩明確 |
| 配線草案可 PASS with nits | 本 verdict |

---

## 4. Soft leftover 同向（HOLD）

對照 `QA_SOFT_NITS_FIX_v1.md` §3：

| Soft leftover | draft 處理 | 同向？ |
|---|---|---|
| stub `flags_written` 仍列 `flag_tang_open` | §4.2／§8#4 標 Soft leftover；建議下輪 Soft；引擎讀 choice 實寫 | **是** |
| Vera 裸旗＋須讀 `qa.flagAlias` | §2／§4.1／§7／§8#5 | **是** |
| Vera speaker「阿偉」 | §8#12 非 blockers／outstanding | **是** |
| Pack3 ending `parallelOk=true` | §5 註＋§8#6 | **是** |
| 徐 cast `tier=阻力` | draft **未**列入 §8（`阻力`＝0） | **漏列（nit）**；**未**誤稱為已修 |

**無**發現 draft 把 HOLD soft 寫成已修，或提出與 Soft leftover **相反**的 wiring（例如要求 stub 再寫 `flag_tang_open`、或要求 Pack3 ending `parallelOk=false` 當本輪必改）。

---

## 5. UNLOCK／MASTER（C14↔T6）

| 源 | C14 conflict |
|---|---|
| JSON `story_detail_c1_to_c17` | `C14.conflict="T6"`；flags `flag_bao_*` |
| UNLOCK §3 | T6「金援 vs 自主」→ C14 |
| MASTER §7.3 | T6 → C14 |
| draft §3 | C14 conflict=T6；連 `R_xu_crisis` |
| Pack2 JSON／draft | `R_xu_crisis` conflict=T6／linksMain=[C14] |

其餘 T 碼抽樣：C1=T1、C10=T2、C11=T3、C12=T4、`R_vera_crisis`=T5 — 與 draft 表一致。

gigs 高覆蓋：春 high4／夏4／秋2／冬4 — 與 draft §6.1 聲稱一致。

---

## 6. Nits（不升 FAIL）

1. **Soft leftover 清單漏列：** 徐寶珊 `cast_main` `tier=阻力`（JSON 仍是；`QA_SOFT_NITS_FIX_v1` leftover#5）—draft §8 未寫；建議補一行「非 blockers／另票」。  
2. **Pack3 表頭欄名：** draft §5.1 用 `kind`；JSON 欄位名為 `arcKind`（值 rival／mentor／friend／capital **一致**）—文件 nit，接線無歧義。  
3. **（資訊／既有缺口）** Pack1／多數 R／A／C 無 JSON `openConditions`（draft 已標 `<MISSING>`／硬接線）—屬 wiring 實作債，**非**本草案誤報。  
4. Soft leftover 其餘四項 **仍 HOLD**（本輪草案正確不改 JSON）。

---

## 7. 建議下一步

1. 餘 Soft 繼續 HOLD；若要清 stub `flags_written`／徐 tier／Pack3 `parallelOk`／Vera 裸旗 rename，另開 Soft 票後再極短覆核。  
2. 引擎 Phase1 按 draft §9：讀 `gigs_1988.json` 標註欄；Tang 用 meet 空閘＋push 雙閘＋threshold=2；Pack1 讀 `qa.flagAlias`。  
3. **出圖仍暫緩**；唔 publish（Soft≠PASS）。  
4. 可選：WIRING 小修補 §8 徐 tier 一行（純 md）。

---

## 8. 一句給用戶／劇本 manager

**WIRING_DRAFT_v1：PASS with nits**（`QA_WIRING_DRAFT_v1.md`）。C1–C17／E01–E10／romance／Tang 雙閘／Pack3／gigs §2A id・flag 與 JSON **一致**；C14↔T6 對齊 UNLOCK；Soft leftover **同向 HOLD**（draft 未誤稱已修；nit：徐 tier 未列入 §8）。出圖仍暫緩。
