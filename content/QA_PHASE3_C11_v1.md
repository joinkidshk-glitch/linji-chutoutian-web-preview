# QA｜Phase3 C11 v1（文件／詞彙｜非 browser）

> **範圍：** `story_detail_phase3_c11.json`＋`PLOT_DETAIL_PHASE3_C11_v1.md`（僅 C11；無合併檔要求）。  
> **基準：** 解鎖 `PLOT_DETAIL_UNLOCK_v1.md` §2 C11／§3 T3／§4 張子駿；詞彙 `COPY_STYLE_HK_LEXICON.md`；schema 對齊 `story_detail_phase2_c8c10.json`（`choices[].effects.{flags,stats,notes}`）。  
> **風格對齊：** `QA_PHASE2_C8C10_v1.md`／`QA_PHASE1_C1C7_v3.md`（不引用已作廢 v2）。  
> **本輪：** 只報告、**未改**任何 content 檔。  
> **時間：** 2026-11-02 22:38（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| 禁詞正文清零（薄本／趕板／苛約／拖字訣） | **PASS**（0） |
| 硬鎖台名／真人／政治／出圖／gigs_1988／T3 軸 | **PASS** |
| 結構鎖 vs 解鎖表（C11／T3） | **PASS** |
| effects 巢狀可讀（非 top-level None） | **PASS** |
| 電報文言短句是否佔主導 | **PASS**（均長 26.9；min 20；0 條 ≤12 字） |
| Soft：cast／口語／用詞 | **NIT**（見下；**非** hard FAIL） |

**C12–C15：** **不擋產製**。可選 polish 見 soft nits。

---

## 1. 禁詞計數（C11 node 全樹＝title／setting／synopsis／beats／choice label+notes）

| 詞 | body | 備註 |
|---|---:|---|
| 薄本 | 0 | |
| 趕板 | 0 | |
| 苛約 | 0 | |
| 拖字訣 | 0 | |

整包 JSON 字串亦 **0**（`qa.tester_steer` 提及「no 位置置」屬 meta 備註，**非**正文錯字）。

---

## 2. 硬鎖掃描

| 項 | 結果 | 證據 |
|---|---|---|
| TVB／tvb／無綫／無線（player-facing） | **PASS** | body＋整包 **0** |
| 真人藝名抽樣 | **PASS** | 周星馳／劉德華／張國榮等 **0** |
| 政治／抗爭詞 | **PASS** | 六四／遊行／示威／民運等 **0** |
| 完整 HE／已出圖宣稱 | **PASS** | md 標「未出圖」；`artId` 僅佔位 `story_c11` |
| `gigs_1988.json` | **PASS** | mtime **2026-11-02 16:51**（HK）；C11 **22:35**——本輪未動 gigs |
| DeepSeek finish | stop | draft+polish＝`deepseek-chat`；`finish_reasons` stop |
| 結局名／十檔改寫 | **N/A** | C11 未觸 E01–E10 |

---

## 3. 結構鎖（對 UNLOCK §2 C11／§3 T3）

| 欄 | 解鎖期望 | 成品 | 結果 |
|---|---|---|---|
| phase | P3 | `P3` | **PASS** |
| title | 曝光還是層次（T3） | `曝光還是層次` | **PASS** |
| when | 1990 秋影展 | `1990秋 / W60-64` | **PASS** |
| cast／線 | 張子駿＋影展／文藝 | cast＝阿偉、張子駿、客戶代表；無高文瀚（解鎖本節點非必需） | **PASS** |
| choices | 曝光廣告 vs 留組磨戲 | `C11_a` 接曝光廣告；`C11_b` 留組磨戲 | **PASS** |
| axes | `route_indie` 深化、`fame`／`craft` | a→`choose_exposure`＋fame+2 wealth+1 craft0 rel_cheung−1；b→`choose_depth`＋`route_indie`＋craft+2 fame0 rel_cheung+2 | **PASS** |
| artId | `story_c11` | `story_c11` | **PASS** |
| conflict | T3 | `T3` | **PASS** |
| eraTag | （時代錨） | `era_1990_autumn_festival` | **PASS**（與 phase2 命名風格一致） |
| 感情留白 | P3 允許 | 無攻略線強制選擇 | **PASS** |

**flags_written：** `choose_exposure`／`choose_depth`／`route_indie` — 與 choices／摘要一致。  
**MD ↔ JSON：** synopsis／beats／effects 對齊，無漂移。

---

## 4. Schema／effects 巢狀

- 頂層／節點鍵集與 phase2（C8）一致。  
- `choices[].effects` 為 dict，含 `flags`／`stats`／`notes`；**勿**在 choice 頂層讀 `flags`/`stats`（會得 `None`）。  
- 摘要宣稱的 `rel_cheung`／fame／wealth／craft **均有明確 stats delta**（非只靠 notes）→ **PASS**。

---

## 5. Soft nits（非擋）

1. **客戶代表：** 在 cast／對白被引用（「客戶代表說…」），但 **無 speaker beat**。解鎖／brief 允許；若要現場感，日後可加 1 段客戶側壓力（可選）。  
2. **口語密度極低：** 符合 lexicon「書面語」＋本包 `tester_steer: low oral Yue density`；比 C8／C10 更乾淨。可選：把「曝光率會很高」改得更港產書面（如「曝光會好大／好高」）——**非必須**。  
3. **設計備註（非 FAIL）：** `C11_a` 不清除既有 `route_indie`（若 C8 已選文藝）。解鎖寫「route_indie 深化」落在磨戲選；廣告選只加 `choose_exposure`。實作／結算層宜明確互斥或疊加規則（可留 C17／引擎表）。

無「位置置」類正文錯字；無電報碎片主導。

---

## 6. Blockers for C12–C15

**無。** C11 可作 P3 定稿基準；C12–C15 可開跑。建議劇本側僅視需要做 soft polish，不擋產製。

---

## 7. 檔案清單（本輪只讀）

| 檔 | 用途 |
|---|---|
| `story_detail_phase3_c11.json` | 驗收主體 |
| `PLOT_DETAIL_PHASE3_C11_v1.md` | 摘要對齊 |
| `PLOT_DETAIL_UNLOCK_v1.md` | C11／T3 鎖 |
| `COPY_STYLE_HK_LEXICON.md` | 禁詞／語氣 |
| `story_detail_phase1.json`／`story_detail_phase2_c8c10.json` | schema 對照 |
