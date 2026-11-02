# QA｜Phase4 C12–C15 v1（文件／詞彙｜非 browser）

> **範圍：** `story_detail_phase4_c12c15.json`＋`PLOT_DETAIL_PHASE4_C12C15_v1.md`。  
> **基準：** 解鎖 `PLOT_DETAIL_UNLOCK_v1.md` §2 C12–C15／§3 T4·T6／§4 攻略＋關海媚無 HE；詞彙 `COPY_STYLE_HK_LEXICON.md`；schema 對齊 C11（`beats[].lines`＋`choices[].effects.{flags,stats,notes}`）。  
> **風格對齊：** `QA_PHASE3_C11_v1.md`／`QA_PHASE2_C8C10_v1.md`／`QA_PHASE1_C1C7_v3.md`（不引用已作廢 v2）。  
> **本輪：** 只報告、**未改**任何 content 檔。  
> **時間：** 2026-11-02 22:41（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| 禁詞正文清零（薄本／趕板／苛約／拖字訣） | **PASS**（body＋整包 0） |
| 硬鎖台名／真人／政治再現／出圖／gigs／關海媚無 commit·HE | **PASS** |
| 結構鎖 vs 解鎖表（C12–C15 選擇軸／artId／when 季節） | **PASS** |
| effects 巢狀＋數字 stats | **PASS** |
| 電報文言短句是否佔主導 | **PASS**（均長 23.6；≤12 字僅 C13×2；非整包主導） |
| Soft：T6 conflict、年表序、高俊傑無 speaker、setting 舵手括號 | **NIT**（見下；**非** hard FAIL） |

**C16–C17：** **不擋產製**。建議劇本側視需要修 soft nits，不擋開跑。

---

## 1. 禁詞計數（C12–C15 node 全樹＝title／setting／synopsis／beats.lines／choice label+notes）

| 詞 | body | 整包 JSON |
|---|---:|---:|
| 薄本 | 0 | 0 |
| 趕板 | 0 | 0 |
| 苛約 | 0 | 0 |
| 拖字訣 | 0 | 0 |

`qa.banned_scan_body: pass` 與實測一致。無「位置置」類錯字；「綵排」寫法一致（5 處，可接受）。

---

## 2. 硬鎖掃描

| 項 | 結果 | 證據 |
|---|---|---|
| TVB／tvb／無綫／無線（player-facing） | **PASS** | body＋整包 **0**；台名用「星河電視台／星河」 |
| 真人藝名抽樣 | **PASS** | 周星馳／劉德華／張國榮等 **0**（關海媚＝本戲虛構角色） |
| 政治／抗爭再現 | **PASS** | 對白無六四／遊行／示威／民運等；「政治口號」**僅**出現在 C15 `setting` 舵手括號「（含蓄，勿政治口號）」＝產製備註，非劇情再現（soft 見 §5） |
| 關海媚 HE／commit | **PASS** | 無 `flag_*_commit`、無 HE／BE 字樣、無專屬結局檔；C13 僅 `rel_mei`± 與公關旗標 |
| 完整出圖宣稱／art 成品 | **PASS** | md 標「未出圖」；`artId` 僅佔位 `story_c12`…`story_c15`；repo 無對應 art 檔 |
| `gigs_1988.json` | **PASS** | mtime **2026-11-02 16:51**（HK）；phase4 JSON **22:39**——本輪未動 gigs |
| DeepSeek finish | stop | C12C13／C14C15／C15_family_polish＝`deepseek-chat`；`finish_reasons` 皆 `stop` |
| 結局名／十檔改寫 | **N/A** | 本包未觸 E01–E10 |

---

## 3. 結構鎖（對 UNLOCK §2／§3／§4）

### C12｜T4 賀歲搶位 vs 關係危機

| 欄 | 解鎖期望 | 成品 | 結果 |
|---|---|---|---|
| phase／title | P4；賀歲搶位 vs 關係危機（T4） | `P4`／`賀歲搶位 vs 關係危機` | **PASS** |
| when | 1991 夏 | `1991夏 / W80-84` | **PASS** |
| conflict／artId | T4／`story_c12` | `T4`／`story_c12` | **PASS** |
| choices | 搶位 vs 顧關係 | `C12_a` 全力搶位；`C12_b` 顧好關係 | **PASS** |
| flags／stats | standing／愛情危機 | a→`anni91_seize`+`love_crisis` standing+2 fame+1 `rel_partner`−2；b→`anni91_tend` `rel_partner`+2 standing0 | **PASS** |
| cast | 高文瀚、可攻略、高俊傑 | 阿偉、高文瀚、約會對象、高俊傑 | **PASS**（高俊傑僅對白提及，見 soft） |

### C13｜緋聞公關真假

| 欄 | 解鎖期望 | 成品 | 結果 |
|---|---|---|---|
| title／when | 緋聞公關真假；1991 冬 | `緋聞公關真假`；`1991冬 / W92-96` | **PASS** |
| artId | `story_c13`（可兼 `paper_gossip`） | `story_c13` | **PASS**（無 `paper_gossip`＝可選佔位 nit） |
| choices | 認／否／模糊 | `C13_a` 承認；`C13_b` 否認；`C13_c` 模糊 | **PASS** |
| flags | 形象、`rel_choi`、关海媚暧昧 | `gossip_*`＋`flag_public_romance`；stats 含 `rel_choi`／`rel_mei` | **PASS** |
| 關海媚無升格 | 無 commit／無 HE 檔 | 無 | **PASS** |
| conflict | （非 T 表） | `null` | **PASS** |

### C14｜徐寶珊尊重或包養（T6）

| 欄 | 解鎖期望 | 成品 | 結果 |
|---|---|---|---|
| title／when | 尊重或包養；廣告／資本場 | `徐寶珊尊重或包養`；`1991秋 / W88-90` | **PASS** |
| artId | `story_c14` | `story_c14` | **PASS** |
| choices | 尊重／依賴／拒 | `C14_a` 尊重合作；`C14_b` 接受依賴；`C14_c` 拒絕 | **PASS** |
| flags／stats | `flag_bao_*`、wealth、`rel_xu` | a `flag_bao_respect` rel_xu+2 wealth+1 standing+1；b `flag_bao_depend` wealth+3 standing−1；c `flag_bao_refuse` rel_xu−1 standing+1 | **PASS** |
| conflict T6 | UNLOCK §3 T6→C14 | `conflict: null` | **NIT**（見 §5；非 intentional 則建議補 `T6`） |

### C15｜藍若曦聯姻逼退圈

| 欄 | 解鎖期望 | 成品 | 結果 |
|---|---|---|---|
| title／when | 聯姻逼退；1991 春 | `藍若曦聯姻逼退圈`；`1991春 / W72-76` | **PASS** |
| artId | `story_c15` | `story_c15` | **PASS** |
| choices | 助抗／成全／袖手 | `C15_a` 助抗；`C15_b` 成全；`C15_c` 袖手 | **PASS** |
| flags | `flag_family_marriage`＋分歧 | 三選皆寫 `flag_family_marriage`＋help／yield／standby；`rel_lan`± | **PASS** |
| 政治禁忌 | 無政治口號／抗爭再現 | 對白為家族聯姻／退圈壓力；無抗爭場面 | **PASS** |

**flags_written** 與各 choice `effects.flags` 聯集一致（無漂移）。  
**MD ↔ JSON：** synopsis／beats 數／effects／when 對齊。

---

## 4. Schema／effects 巢狀

- 頂層鍵與 C11 一致：`version`／`locale`／`phase:P4`／`nodes[4]`／`qa`／`models`／`finish_reasons`。  
- 節點鍵集與 C11 相同；`beats[].{speaker,lines[]}`；`choices[].effects.{flags,stats,notes}`。  
- 全部 choice 皆有 **數字** `stats`（含宣稱之 `rel_*`／standing／fame／wealth）→ **PASS**（非 notes-only）。

---

## 5. Soft nits（非擋）

1. **C14 `conflict` 為 null，UNLOCK T6 掛 C14：** 任務註明「if conflict null, NIT unless intentional」。摘要 md 亦寫 `None`。若非刻意省略，建議補 `T6` 以利檔期衝突表／引擎掛鉤；**不擋 C16–C17**。  
2. **年表序 vs 檔內節點序：** `when` 欄位自洽——時序為 **C15 春 W72 → C12 夏 W80 → C14 秋 W88 → C13 冬 W92**；JSON／md 仍按 ID **C12→C13→C14→C15** 排列。非錯誤，但 playtest／合併表宜按週數排序，免誤以為冬在秋前。  
3. **C12 高俊傑：** 在 `cast` 且被高文瀚對白點名搶同一賀歲位，但 **無 speaker beat**（speakers＝高文瀚／阿偉／約會對象）。與 C11「客戶代表」同類可選加強；解鎖允許對手作壓力源即可。  
4. **C15 `setting` 舵手括號：** 「豪門宴會側廳（含蓄，勿政治口號）」若直接進 UI，玩家會看到產製指令。建議日後把舵手句移出 player-facing `setting`（留在 `qa`／prompt）。非硬 FAIL。  
5. **C13 口語／短句：** 兩條 ≤12 字（「但我不想你覺得我在迴避。」「你想清楚再答我。」）屬完整句，非整包電報腔；均長仍 23.6。可選略加長，非必須。  
6. **口語密度極低：** 對白無粵助詞堆砌，符合 lexicon 書面語；比 C8／C10 更乾淨。  
7. **可選 art 佔位：** UNLOCK 寫 `story_c13`／`paper_gossip`；本包僅 `story_c13`。出圖仍暫緩，無需本輪補。

無電報碎片主導；配角對白齊（周采兒／關海媚／徐寶珊／藍父）。

---

## 6. Blockers for C16–C17

**無。** C12–C15 可作 P4 文件定稿基準（T6 conflict 建議補標，非 blocker）。C16–C17 可開跑。

---

## 7. 檔案清單（本輪只讀）

| 檔 | 用途 |
|---|---|
| `story_detail_phase4_c12c15.json` | 驗收主體 |
| `PLOT_DETAIL_PHASE4_C12C15_v1.md` | 摘要對齊 |
| `PLOT_DETAIL_UNLOCK_v1.md` | C12–C15／T4·T6／關海媚鎖 |
| `COPY_STYLE_HK_LEXICON.md` | 禁詞／語氣 |
| `story_detail_phase3_c11.json` | schema 對照 |
| `gigs_1988.json` | mtime 未動證明 |
