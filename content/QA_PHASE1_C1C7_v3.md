# QA｜Phase1 C1–C7 **v3** 定稿（文件／詞彙｜非 browser）

> **範圍：** `story_detail_phase1.json` v3＋分包 c1c5／c6c7；對照 `_hk_lexicon_fix_v3.md`、`COPY_STYLE_HK_LEXICON.md`、`PLOT_DETAIL_UNLOCK_v1.md`。  
> **不引用／不信任：** `QA_PHASE1_HK_LEXICON_v1.md`（v2＝VOID）。  
> **本輪：** 只報告、**未改**任何 content 檔。  
> **時間：** 2026-11-02（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| 禁詞正文清零（薄本／趕板／苛約／拖字訣） | **PASS**（0） |
| 硬鎖台名／真人／政治／結局名／出圖／gigs_1988 | **PASS** |
| 結構鎖（choice id＋關鍵 flags） | **PASS** |
| 對白電報風是否仍佔主導 | **PASS（整體）**；C1 尾段仍偏短＝NIT |
| 標題／解鎖語意對齊 | **NIT（擋「乾淨定稿」）**：**C6 title 誤貼成 C2** |
| 分包與 merged 同步 | **PASS**（節點 JSON 全等；三檔 version=3） |

**是否可作 C1–C7 文字定稿：**  
- **詞彙＋結構：** 可作定稿基準（v2 作廢）。  
- **完整乾淨定稿：** **否**——須先修 **C6 `title`**（現誤為「留人脈／趕通告」，與正文／解鎖「首次正式約會」不符；與 C2 撞名）。修完可標 v3.1／再掃 title 即可，無需重跑全套 lexicon。  
- **C8+：** **不擋產製**（結構旗標齊）；建議並行修 C6 title，免 UI／目錄顯示錯節點名。

---

## 1. 禁詞計數（story body＝`nodes` 全樹）

| 詞 | merged nodes | c1c5 | c6c7 | 備註 |
|---|---:|---:|---:|---|
| 薄本 | 0 | 0 | 0 | changelog／fix report 提及 OK（本掃只計 JSON body） |
| 趕板 | 0 | 0 | 0 | |
| 苛約 | 0 | 0 | 0 | 「苛刻合約」≠ 苛約 |
| 拖字訣 | 0 | 0 | 0 | |

**替換到位（merged nodes 出現次數）：**

| 應用 | 次數 | 抽樣路徑 |
|---|---:|---|
| 記數簿 | 3 | C3／C4 setting＋對白 |
| 趕通告 | 10 | C1 synopsis／choices；**C2 title**；多處對白 |
| 苛刻合約 | 2 | **C7 title**；C7_a label |
| 先拖住 | 1 | C7_b label |
| 暫不答覆 | 1 | C7_b label（與「先拖住，暫不答覆」同 label） |

標題核對（v3 report）：**C2＝留人脈／趕通告** ✅；**C7＝拒雷勁式苛刻合約** ✅。

---

## 2. 硬鎖掃描

| 項 | 結果 | 證據 |
|---|---|---|
| TVB／無綫／無線 | **PASS** | nodes 內 0；「星河」×4、「星河電視台」×2 |
| 真人藝名抽樣表 | **PASS** | 周星馳／劉德華／張國榮等 0 |
| 政治口號／抗爭詞 | **PASS** | 六四／遊行／示威／民運等 0 |
| E01–E10 改名 | **PASS** | 本檔未寫結局名／未改十檔（無出現＝未擅自重命名） |
| 宣稱已出圖 | **PASS** | artId 僅 `story_c1`…`story_c7` 佔位；無「已出圖」類字樣 |
| `gigs_1988.json` | **PASS** | mtime **2026-11-02 16:51**（HK）；story v3 **22:23**——本輪 lexicon **未動** gigs |

---

## 3. 結構鎖表（對早期 unlock QA choice id；標題變更以 v3 為準）

| 節點 | choice ids | 關鍵 effects | 鎖結果 |
|---|---|---|---|
| C1 | `C1_a`／`C1_b` | a→`route_tv`；b→`route_film` | **PASS** |
| C2 | `C2_a`／`C2_b` | network_stay／hustle_board | **PASS** |
| C3 | `C3_a`／`C3_b` | rival_gao_hard／endure | **PASS** |
| C4 | `C4_a`／`C4_b` | refuse_with_ho／take_harsh_gig | **PASS** |
| C5 | `C5_a`／`b`／`c` | `choi_honest`／`choi_spin`／`choi_dodge` | **PASS** |
| C6 | `C6_a`／`b`／`c` | `date_vera_1`／`date_hiu_1`／`date_choi_1`；**無** commit／HE | **PASS** |
| C7 | `C7_a`／`b`／`c` | a=`flag_anti_lei`；b=`flag_lei_delay`；c=`flag_lei_signed` | **PASS** |

`flags_written` 與 choices 一致；`structure_locked: true`（meta.qa）。  
對照舊 C6C7 QA 報告中的 choice／flag 表：**無 id／flag 漂移**（僅 C6／C7 **顯示標題**應跟 v3／解鎖語意，見下）。

---

## 4. 標題／解鎖語意

| ID | 檔內 title | 解鎖表語意／預期 | 判定 |
|---|---|---|---|
| C1–C5、C7 | 與解鎖或 v3 改名一致 | OK | **PASS** |
| **C6** | **「留人脈／趕通告」**（＝C2 撞名） | 解鎖：**首次正式約會對象**；正文亦係約會三選 | **NIT／定稿 blocker** |

正文 synopsis／beats／choices 語意正確（Vera／曉晴／采兒；不鎖死）；**僅 title 欄誤貼**。舊文件 QA 曾錄 C6 title＝「首次正式約會對象」→ v3 polish **回歸**。

建議改回例如：`首次正式約會對象` 或 `約誰：Vera／曉晴／采兒`（劇本側決定；QA 不改檔）。

---

## 5. 對白長度／電報風（soft）

| 節點 | 行數 | 均長（字） | ≤12 字占比 | 評 |
|---|---:|---:|---:|---|
| C1 | 18 | 12.3 | **56%** | 開場已加長；**收束仍碎句多** |
| C2 | 14 | 16.9 | 21% | 可接受 |
| C3 | 12 | 17.8 | 17% | 可接受 |
| C4 | 11 | 16.5 | 27% | 可接受 |
| C5 | 24 | 14.0 | 33% | 偏短但非文言電報主導 |
| C6 | 24 | 18.2 | 4% | **良好** |
| C7 | 13 | 21.2 | 0% | **良好** |
| **合計** | 116 | **16.4**（median 16.5） | 15.5% ≤10；40.5% ≤15 | **整體非「電報主導」→ 不觸 hard FAIL** |

抽樣（與 fix report 一致）：何生三句長開場；雷勁條件說明完整；C6 系統／何生／Vera 正常書面白話。  
**NIT：** 若要「長度也定稿」，可選修 C1 beats 尾段（「我知道。」「我選。」類）略補上下文——**非 C8+ 硬擋**。

大陸網文黑話抽樣（卷王／破防／yyds／賦能等）：**0**。

---

## 6. 分包同步

| 檢查 | 結果 |
|---|---|
| merged／c1c5／c6c7 `version` | 皆 **3** |
| C1–C5 節點 vs merged | **byte-level 欄位全等** |
| C6–C7 節點 vs merged | **全等** |
| 故 C6 錯 title 在 **三檔同時存在** | 修時須 **merged＋c6c7**（及若有摘要 md）一併改 |

---

## 7. Lexicon 抽樣（PASS 佐證）

- C4 setting：`桌面堆著**記數簿**與通告紙`  
- C1_b label：`先賺錢、**趕通告**：接電影散工臨記`  
- C7 title／C7_a：`拒雷勁式**苛刻合約**`／`拒絕**苛刻合約**`  
- C7_b：`**先拖住，暫不答覆**`  
- 禁詞四式正文 **0**（與 `_hk_lexicon_fix_v3.md` 宣稱一致）

---

## 8. Blockers

| 對 | Blocker？ | 說明 |
|---|---|---|
| **C8+ 產製** | **否** | flags／choice 鎖完好 |
| **C1–C7 乾淨文字定稿** | **是（小）** | 必修 **C6 title** 去撞名 |
| **再跑 DeepSeek 全量 lexicon** | **否** | 禁詞已清零 |
| **出圖** | 維持暫緩閘門 | 本輪未觸 |

---

## 9. 給劇本 manager／用戶一句

**v3 定稿 QA＝PASS with nits。** 禁詞與硬鎖過關；結構未漂。唯一定稿小擋：**C6 標題誤複製成 C2「留人脈／趕通告」**——請改回約會節點名並同步 `story_detail_phase1.json`＋`story_detail_phase1_c6c7.json`。修後可視作 C1–C7 文字定稿；C8+ 可開。C1 尾段對白偏短列為可選 polish，不擋。

*QA agent｜document only｜未改 content*
