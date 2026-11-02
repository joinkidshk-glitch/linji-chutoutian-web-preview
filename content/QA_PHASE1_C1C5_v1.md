# QA Phase1 Detail C1–C5 v1（文件 QA｜非瀏覽器 playtest）

> **日期：** 2026-11-02（Asia/Hong_Kong）  
> **對象：** `story_detail_phase1_c1c5.json`＋`PLOT_DETAIL_PHASE1_C1C5_v1.md`  
> **對照：** `PLOT_DETAIL_UNLOCK_v1.md`（§2 C1–C5／§3 T1／§4 周采兒／§5／§8）、`PLOT_MASTER_PLAN_v1.4-DS.md`（§0／§2A era／§7.3／硬鎖）  
> **總評：** **PASS with nits**

---

## 總覽

| 項 | 結果 |
|---|---|
| Overall | **PASS with nits** |
| Blocker for C6–C7 | **無**（可開；見下方 nits／對照註） |
| JSON well-formed | PASS（5 nodes；`finish_reasons` 皆 `stop`） |
| 截斷 | PASS（無截斷跡象；beats／choices 齊） |

### 節點摘要（自 JSON）

| ID | title | when | eraTag | artId | conflict | cast | beats | choices |
|---|---|---|---|---|---|---|---|---|
| C1 | 先練／先賺 | 1988春 / W3-4 | `era_1988_spring_grassroot` | `story_c1` | **T1** | 何生、阿偉、張子駿 | 7 | 2（`C1_a`/`C1_b`） |
| C2 | 留人脈／趕板 | 1988春 / W4-5 | `era_1988_spring_alley` | `story_c2` | null | 何生、阿偉、林曉晴 | 7 | 2 |
| C3 | 對對手硬／忍 | 1988春 / W6-8 | `era_1988_spring_factory` | `story_c3` | null | 阿偉、高俊傑、林曉晴 | 6 | 2 |
| C4 | 何生拒單 | 1988春 / W8-9 | `era_1988_spring_grassroot` | `story_c4` | null | 何生、阿偉 | 6 | 2 |
| C5 | 采兒小訪題 | 1988夏 / W9-10 | `era_1988_summer_variety` | `story_c5` | null | 周采兒、阿偉 | 8 | 3 |

**Choices／flags／stats（摘要）**

- C1_a → `route_tv`；craft+1／wealth+0｜C1_b → `route_film`；wealth+1／craft+0  
- C2_a → `flag_network_stay`；standing+1｜C2_b → `flag_hustle_board`；wealth+1  
- C3_a → `rival_gao_hard`；standing+1｜C3_b → `rival_gao_endure`；craft+1  
- C4_a → `flag_refuse_gig_with_ho`；standing+1｜C4_b → `flag_take_harsh_gig`；wealth+1／standing−1  
- C5_a → `choi_honest`；rel_choi+2／fame+1｜C5_b → `choi_spin`；rel_choi+1／fame+2｜C5_c → `choi_dodge`；0／0  

---

## Hard locks checklist

| # | 項 | 結果 | 證據（一行） |
|---|---|---|---|
| 1 | 台名＝星河／非 TVB·無綫·無線 | **PASS** | nodes 文案僅「星河電視台／星河」；JSON nodes 內 `TVB`/`無綫`/`無線`/`無線電視`＝0 |
| 2 | 無真人藝名作 cast | **PASS** | cast 僅計劃內虛構：何生、阿偉、張子駿、林曉晴、高俊傑、周采兒 |
| 3 | 結局 10 檔名未改寫 | **PASS** | 本包無 E01–E10 名稱字串；`qa.ending_names_untouched: true` |
| 4 | 未出圖／僅 artId 佔位 | **PASS** | artId=`story_c1`…`c5`；摘要明示「未出圖」；無 shipped 聲稱 |
| 5 | 未改 `gigs_1988.json` | **PASS** | `git status` 無該檔；mtime 16:51 HKT，detail 22:12；JSON 未引用重寫 gigs |
| 6 | 書面語／現代可讀 | **PASS**（NIT 見下） | 對白偏短句書面；口語助詞掃描無主導（無㗎／啦／喎等堆疊） |
| 7 | 選擇數 C1–C4＝2、C5＝3 | **PASS** | 與 JSON／摘要／內建 qa.choice_counts 一致 |
| 8 | Unlock C1–C5 對齊 | **PASS** | 見下節逐列；無 FAIL 級錯位 |
| 9 | Unlock §8（本包適用項） | **PASS**／其餘 N/A | 見 §8 表 |
| 10 | T4 MASTER vs UNLOCK | **NIT（對照註）** | Detail **跟 UNLOCK**：C1=`T1`；C5 `conflict=null`（非 T4）。MASTER §7.3 寫 T4→C5，與 UNLOCK §3 T4→C12／MASTER 年表 C12(T4) 不一致——以解鎖表為準 |

---

## Unlock 逐列（C1–C5）

| ID | 解鎖表要求 | Detail | 結果 |
|---|---|---|---|
| C1 | 先練／先賺；T1；route_tv／route_film；craft／wealth；何生＋張子駿；story_c1；1988 春 | 全齊；setting 含星河電視台；era 春 grassroot | **PASS** |
| C2 | 留人脈／趕板；C1 後；人脈 vs 趕板；story_c2 | 標題／二分／artId／春 alley；何生在場；無 prereq 欄位（文件層預期） | **PASS**（NIT：無顯式 `after:C1` 欄） |
| C3 | 對對手硬／忍；高俊傑；story_c3 | 高俊傑搶板；硬／忍旗標；春 factory | **PASS** |
| C4 | 何生拒單；standing／wealth；story_c4 | 拒／硬接；standing±／wealth；春 grassroot | **PASS** |
| C5 | 采兒小訪；誠實／包裝／迴避；rel_choi、fame；story_c5；1988 夏台慶籌備；星河 | 三選；夏 variety；synopsis／對白提星河台慶籌備；conflict=null（正確非 T4） | **PASS** |

### Unlock §3／§4／§5（本包）

| 項 | 結果 | 證據 |
|---|---|---|
| T1 ↔ C1 | **PASS** | C1.`conflict`=`T1`；人物何生＋張子駿 |
| T2–T6 本包 | **N/A** | 未寫入 C5 為 T4（正確跟 UNLOCK） |
| 周采兒認識＝C5 | **PASS** | C5 小訪＋`rel_choi`／`choi_*` |
| 高俊傑 C3 | **PASS** | C3 搶板 |
| 何生 C2／C4（＋C1 出場） | **PASS** | C1／C2／C4 均有何生 |
| 張子駿於 C1（解鎖要求） | **PASS** | C1 cast＋電話線；§5 後期節點 N/A |

---

## Unlock §8 驗收清單（本包範圍）

| §8 項 | 結果 | 說明 |
|---|---|---|
| C1–C17 觸發可列、無死節 | **PASS**（C1–C5）／**N/A**（C6–C17） | 本包五節齊；後段未產 |
| 五可攻略＋鄧麗萍雙條件＋關海媚無 HE | **N/A**（結構）／**PASS**（C5 采兒認識） | 本包僅落地采兒認識；曉晴僅配角出場 |
| 高俊傑／張克凡並存可測 | **PASS**（高俊傑 C3）／**N/A**（張克凡） | 張克凡屬後段 |
| E01–E10 名稱一字不差 | **PASS**（本包未改）／**N/A**（未寫結局文） | 無改名字串 |
| 星河文案、虛構獎名無真實商標 | **PASS** | 星河；無真實台名；獎名未展開（僅台慶籌備傳聞） |
| 無政治口號／抗爭再現 | **PASS** | 抽查 beats 無相關內容 |
| 出圖未擅自開工 | **PASS** | artId 佔位；摘要「未出圖／未叫 GD」 |

---

## Banned-string findings

| 來源 | 發現 |
|---|---|
| `story_detail_phase1_c1c5.json`（nodes） | **無** TVB／tvb／無綫／無線／無線電視 |
| `PLOT_DETAIL_PHASE1_C1C5_v1.md` | 僅 QA 段提及「TVB·無綫」作禁掃說明（非劇情文案）→ **不計 FAIL** |
| 常見真人藝名掃描 | **無命中** |

---

## 書面語抽查（2–3 行）

1. 何生（C1）：「你想做演員，還是想做臨記？」→ 書面、現代、可讀。  
2. 高俊傑（C3）：「阿偉，你上次走位慢了半拍。」→ 書面敘事口吻，非濃口語。  
3. 周采兒（C5）：「星河台慶在籌備，你聽過吧。」→ 台名正確；書面。  

**NIT（非 blocker）：** 對白整體偏短句／少修飾，風格統一；C4「無。」可接受書面省略。非「濃粵語助詞主導」。

---

## Unlock mismatches／對照註

1. **MASTER §7.3 T4→C5** vs **UNLOCK §3 T4→C12**（且 MASTER 年表自身寫 C12＝T4）。  
   - **Detail 跟 UNLOCK：** C5 `conflict=null`；僅 C1 掛 T1。  
   - **建議：** 後續修 MASTER §7.3 與 UNLOCK／年表對齊（非本包改文 blocker）。  
2. JSON 無顯式 `requires: C1` 類欄 → 文件／產製層 NIT，不影響本包對白驗收。

---

## Recommended blockers before C6–C7

**無硬 FAIL blocker。** 建議知悉：

- 開 C6–C7 前可另開「MASTER §7.3 T4 列修正」小票（計劃層，非改 C1–C5）。  
- C6 起注意解鎖表約會對象／平行規則；本包未測。  
- 出圖仍暫緩（硬鎖／閘門維持）。

---

## Nits 清單（不阻 C6–C7）

1. MASTER↔UNLOCK T4 掛點不一致（detail 已正確跟 UNLOCK）。  
2. 無機器可讀 prereq 欄（C2「C1 後」僅敘事順序）。  
3. 摘要 md QA 提及 TVB 字樣僅作禁掃說明（可接受）。  
4. `qa.truncations` 欄為缺省／非嚴格 `false`（實際無截斷）。

---

*QA 類型：文件對照｜未改內容檔｜未發明批核。*
