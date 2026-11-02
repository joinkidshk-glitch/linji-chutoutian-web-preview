# QA Phase1.5 Detail C6–C7 v1（文件 QA｜非瀏覽器 playtest）

> **日期：** 2026-11-02（Asia/Hong_Kong）  
> **對象：** `story_detail_phase1_c6c7.json`＋`PLOT_DETAIL_PHASE1_C6C7_v1.md`＋合併 `story_detail_phase1.json`  
> **對照：** `PLOT_DETAIL_UNLOCK_v1.md`（§1 P1.5／§2 C6–C7／§4／§5 雷勁／§8）、`PLOT_MASTER_PLAN_v1.4-DS.md`（§0 硬鎖／§7.3 v1.4.2）、前次 `QA_PHASE1_C1C5_v1.md`  
> **總評：** **PASS with nits**

---

## 總覽

| 項 | 結果 |
|---|---|
| Overall | **PASS with nits** |
| Blocker for C8+ | **無** |
| JSON well-formed | PASS（C6–C7 兩 nodes；`finish_reasons.c6c7=stop`；`qa.truncations=false`） |
| 截斷 | PASS |
| 合併完整性 | **PASS**（見下） |
| MASTER §7.3 T4 | **PASS**（v1.4.2：T4→C12；與 UNLOCK 一致） |

### 節點摘要（自 `story_detail_phase1_c6c7.json`）

| ID | title | when | eraTag | artId | conflict | cast | beats | choices |
|---|---|---|---|---|---|---|---|---|
| C6 | 首次正式約會對象 | 1988秋 / W12-14 | `era_1988_autumn_unitdrama` | `story_c6` | null | 阿偉、Vera、林曉晴、周采兒、何生 | 7 | 3（`C6_a`/`b`/`c`） |
| C7 | 拒雷勁式苛約 | 1988秋冬 / W14-16 | `era_1988_winter_festive` | `story_c7` | null | 阿偉、雷勁、何生 | 6 | 3（`C7_a`/`b`/`c`） |

**Choices／flags／stats（摘要）**

- C6_a → `date_vera_1`；rel_vera+2｜C6_b → `date_hiu_1`；rel_hiu+2｜C6_c → `date_choi_1`；rel_choi+2  
  - notes 均明示不鎖死／關係未定；**無** `flag_*_commit`／完整 HE  
- C7_a → `flag_anti_lei`；standing+1｜C7_b → `flag_lei_delay`；0｜C7_c → `flag_lei_signed`；wealth+2／standing−1（notes：**不鼓勵**）

---

## Hard locks checklist

| # | 項 | 結果 | 證據（一行） |
|---|---|---|---|
| 1 | 台名＝星河／非 TVB·無綫·無線 | **PASS** | C6–C7／合併 nodes 內 `TVB`/`tvb`/`無綫`/`無線`/`無線電視`＝0；本包未點名電視台（可接受） |
| 2 | 無真人藝名作 cast | **PASS** | cast＝阿偉／Vera／林曉晴／周采兒／何生／雷勁；常見真人藝名掃描＝0 |
| 3 | 結局 10 檔名未改寫 | **PASS** | 本包無 E01–E10 名稱字串；無結局文案 |
| 4 | 未出圖／僅 artId 佔位 | **PASS** | artId=`story_c6`/`story_c7`；摘要 md「未出圖」 |
| 5 | 未改 `gigs_1988.json` | **PASS** | `git status` 該檔 porcelain 空；mtime 16:51 HKT，detail／merge 22:14 |
| 6 | 書面語／現代可讀 | **PASS**（NIT 見下） | 口語助詞掃描（㗎／喎／咁／啲等）＝0；對白短句書面 |
| 7 | C6 約會不鎖 commit／HE；C7 拒支含 `flag_anti_lei` | **PASS** | C6 notes「不鎖死／未定」；commit flag＝0；C7_a=`flag_anti_lei` |
| 8 | Unlock C6–C7 對齊 | **PASS** | 見下節逐列 |
| 9 | 合併檔恰為 C1–C7、與分檔一致 | **PASS** | ids=`C1…C7`；無缺無重；逐 node JSON 深比較 vs c1c5+c6c7＝**NONE mismatch** |
| 10 | 無完整 HE／政治禁忌 | **PASS** | 無 HE／commit；無政治口號／抗爭／六四等字樣 |
| 11 | MASTER §7.3 T4 vs UNLOCK | **PASS** | v1.4.2 註記對齊；T4＝賀歲搶位 vs 關係→**C12**；T3→C11；T5＝打歌／形象 vs 陪伴 |

---

## Unlock 逐列（C6–C7）

| ID | 解鎖表要求 | Detail | 結果 |
|---|---|---|---|
| C6 | 首次正式約會；≥1 可攻略達門檻；選當次不鎖死；`rel_*`；1988 秋單元劇；`story_c6` | 標題／三選 Vera·曉晴·采兒；`date_*_1`＋`rel_*`+2；系統句「不必急著承諾」；era 秋 unitdrama；artId 齊 | **PASS** |
| C7 | 拒雷勁式苛約；拒／拖／勉強簽（不鼓勵）；`flag_anti_lei` 於拒；雷勁關係／短期收入；1988 秋冬；`story_c7`；雷勁出場 | 三選齊；C7_a anti_lei＋standing；delay／signed；signed＝wealth↑ standing↓＋「不鼓勵」；cast 含雷勁＋何生；秋冬 festive | **PASS** |

### Unlock §1／§4／§5（本包）

| 項 | 結果 | 證據 |
|---|---|---|
| Phase P1.5＝C6–C7 | **PASS** | 兩節 `phase=P1.5`；when 1988 秋／秋冬 |
| 約會選當次不確定關係 | **PASS** | 無 commit；notes 不鎖死 |
| §4 認識線：Vera／曉晴／采兒可進 C6 | **PASS** | 三人入選；藍若曦＝P2、徐寶珊＝P3 → **本包不出現＝正確** |
| §5 雷勁＝C7＋`flag_anti_lei` | **PASS** | cast＋拒支旗標 |

---

## Unlock §8 驗收清單（本包範圍）

| §8 項 | 結果 | 說明 |
|---|---|---|
| C1–C17 觸發可列、無死節 | **PASS**（C1–C7）／**N/A**（C8–C17） | 合併七節齊 |
| 五可攻略＋鄧麗萍雙條件＋關海媚無 HE | **PASS**（結構方向） | C6 僅開 P1 已見三線約會；無關海媚 HE／commit |
| 高俊傑／張克凡並存可測 | **N/A**（本包） | 高俊傑已在 C3；本包無對手新節 |
| E01–E10 名稱一字不差 | **PASS**（本包未改） | 無結局名字串 |
| 星河文案、虛構獎名無真實商標 | **PASS** | 無真實台名；C7 僅「賀歲檔」籌備風聲 |
| 無政治口號／抗爭再現 | **PASS** | 禁掃乾淨 |
| 出圖未擅自開工 | **PASS** | artId 佔位 |

---

## 合併完整性（`story_detail_phase1.json`）

| 檢查 | 結果 |
|---|---|
| node ids | `C1,C2,C3,C4,C5,C6,C7` 恰好七個 |
| 與 `c1c5`＋`c6c7` 集合 | 無缺、無多、無重 |
| 逐 node 內容深比較 | **NONE mismatch**（title／beats／choices／flags／artId 全同） |
| source 標記 | `Merged C1-C5 + C6-C7; aligned …` |

---

## Banned-string findings

| 來源 | 發現 |
|---|---|
| `story_detail_phase1_c6c7.json`／合併 nodes | **無** TVB／tvb／無綫／無線 |
| 常見真人藝名掃描 | **無命中** |
| 政治／抗爭關鍵字 | **無命中** |
| E01–E10 十檔名 | **本包未出現**（未改寫） |

---

## 書面語抽查（2–3 行）

1. 何生（C6）：「約人，就約一個。兩個都等，最難看。」→ 書面、現代。  
2. 雷勁（C7）：「片酬先壓低，賣座再分。簽了，就別接別人的戲。」→ 書面敘事口吻。  
3. 系統（C7）：「這一節不判結局，只記方向。」→ 明確非 HE／結局鎖。

**NIT（非 blocker）：** 對白仍偏短句／少修飾，與 C1–C5 風格一致；非濃粵語助詞主導。

---

## MASTER §7.3 狀態（前次 NIT 結案）

- **前次 QA：** MASTER 誤寫 T4→C5；detail／UNLOCK 跟 C12。  
- **現況：** `PLOT_MASTER_PLAN_v1.4-DS.md` **v1.4.2**（2026-11-02）§7.3 已改：T4→**C12**；T3→C11；T5＝打歌／形象 vs 陪伴。  
- **結果：** **PASS**（與 UNLOCK §3 一致）。

---

## Unlock mismatches／對照註

1. JSON 仍無機器可讀 `requires:`／約會門檻欄（「至少一條可攻略達門檻」僅敘事／系統層）→ 文件層 **NIT**，同 C1–C5。  
2. C6 可選三人＝P1 已落地線；藍若曦／徐寶珊／鄧麗萍未入選＝**跟解鎖表 Phase 正確**，非 mismatch。  
3. C7 `phase` 欄＝`P1.5`（UNLOCK 寫 P1.5→P2）→ 可接受；拖字訣 notes 已指 P2 再攤牌。

---

## Recommended blockers before C8+

**無硬 FAIL blocker。** 建議知悉：

- C8+ 放行可開（商業片 vs 文藝線等）；注意 C7 三旗標（`flag_anti_lei`／`flag_lei_delay`／`flag_lei_signed`）在 P2 的銜接。  
- 出圖仍暫緩。  
- MASTER §7.3 T4 nit **已結案**，無需再擋。

---

## Nits 清單（不阻 C8+）

1. 無顯式 prereq／門檻欄（敘事順序推定）。  
2. 對白短句風格（風格統一，非口語 FAIL）。  
3. 合併檔未帶分檔級 `finish_reasons`／`models`（僅 `parts`／`phases`／nodes）→ 元數據 NIT，不影響正文驗收。

---

*QA 類型：文件對照｜未改內容檔｜未發明批核。*
