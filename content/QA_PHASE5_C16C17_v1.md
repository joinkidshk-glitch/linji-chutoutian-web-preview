# QA｜Phase5 C16–C17＋合併 C1–C17 v1（文件／詞彙｜非 browser｜end-of-arc）

> **範圍：** `story_detail_phase5_c16c17.json`、`PLOT_DETAIL_PHASE5_C16C17_v1.md`、合併 `story_detail_c1_to_c17.json`。  
> **基準：** 解鎖 `PLOT_DETAIL_UNLOCK_v1.md` §2 C16–C17／§6 E01–E10；主計劃 `PLOT_MASTER_PLAN_v1.4-DS.md` §4（結局名 **一字不差**）；詞彙 `COPY_STYLE_HK_LEXICON.md`；分包深比 C1–C7 `story_detail_phase1.json`（v3）／C8–C10／C11／C12–C15／C16–C17。  
> **風格對齊：** `QA_PHASE4_C12C15_v1.md` 等（**不引用**已作廢 v2）。  
> **本輪：** 只報告、**未改**任何 content 檔。  
> **時間：** 2026-11-02 22:43（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| Phase5 C16–C17 硬鎖（禁詞／星河／真人／政治／出圖／gigs／關海媚無 HE／結局名／十檔齊） | **PASS** |
| 解鎖表 C16–C17 結構（接拒／legacy／結算／orientation／artId） | **PASS** |
| E01–E10 名稱 vs MASTER §4／UNLOCK §6 | **PASS（一字不差）** |
| 電報短句是否佔主導（C16–C17） | **PASS**（均長 C16≈25.9／C17≈34.5；≤12 字 **0**） |
| 合併 17/17 無缺無 dup；C16–C17 與 phase5 包全等 | **PASS** |
| 合併 vs 前段分包深比 | **NIT：** 僅 `C14.conflict` 漂移（pack=`T6`，merge=`null`）——見 §5 |
| Soft：C17 自由揀十檔（無 gate／無 auto-calc 文案）；E05 stats 用 craft／standing 非 `action`；C8–C10 口語殘留（前輪已知） | **NIT**（非 hard FAIL） |

**出圖：** 仍暫緩（`artId` 僅佔位；repo 無 `story_c16`／`story_c17`／`ending_e*` 成品）。

**C1–C17 正文可否當 wiring 完備：** **可以（文字弧完結）**——建議 wiring 前先把合併檔 `C14.conflict` 重蓋成 `T6`（與 phase4 包一致）；結局門檻／自動結算屬引擎層（本 detail 按 UNLOCK「玩家最終選擇 ＞ 旗標 ＞ 數值」做成十選一自由鎖）。**出圖仍暫緩。**

---

## 1. E01–E10 結局名核對表（一字不差）

來源對照：MASTER §4 表｜UNLOCK §6｜phase5 `choices[].endingName`＋`endings_catalog[].name`＋label（去 `E0x`＋表意空格）｜merge 內 C17（與 phase5 全等）。

| ID | MASTER／UNLOCK 鎖定名 | choice `endingName` | catalog `name` | `endingId`／flag／`artId` | 結果 |
|---|---|---|---|---|---|
| E01 | 穩陣男演員 | 穩陣男演員 | 穩陣男演員 | E01／`ending_e01`／`ending_e01` | **PASS** |
| E02 | 有名有實 | 有名有實 | 有名有實 | E02／`ending_e02`／`ending_e02` | **PASS** |
| E03 | 評審眼熟 | 評審眼熟 | 評審眼熟 | E03／`ending_e03`／`ending_e03` | **PASS** |
| E04 | 跨界紅人 | 跨界紅人 | 跨界紅人 | E04／`ending_e04`／`ending_e04` | **PASS** |
| E05 | 動作班底 | 動作班底 | 動作班底 | E05／`ending_e05`／`ending_e05` | **PASS** |
| E06 | 海外發展 | 海外發展 | 海外發展 | E06／`ending_e06`／`ending_e06` | **PASS** |
| E07 | 金援靠山 | 金援靠山 | 金援靠山 | E07／`ending_e07`／`ending_e07` | **PASS** |
| E08 | 有錢但空 | 有錢但空 | 有錢但空 | E08／`ending_e08`／`ending_e08` | **PASS** |
| E09 | 淡出守住 | 淡出守住 | 淡出守住 | E09／`ending_e09`／`ending_e09` | **PASS** |
| E10 | 未出頭 | 未出頭 | 未出頭 | E10／`ending_e10`／`ending_e10` | **PASS** |

- 選擇數：**10／10**（`C17_e01`…`C17_e10`）。  
- 各 choice 另寫 `career_lock`；notes 均註「愛情結局另表並存」——對齊解鎖「愛情另計並存」。  
- **無結局改名／漂移** → 未觸 hard FAIL。

---

## 2. 解鎖對齊｜C16–C17

### C16｜舊底片交付

| 欄 | 解鎖期望 | 成品 | 結果 |
|---|---|---|---|
| title／phase | 舊底片交付；P5 | 同左；`P5` | **PASS** |
| when | 1992 夏回望 | `1992夏 / W100-104` | **PASS** |
| cast | 金九／傳承 | 阿偉、金九 | **PASS** |
| choices | 接／拒 | `C16_a` 接下→`flag_legacy_film`；`C16_b` 婉拒→`flag_legacy_refuse` | **PASS** |
| flags | `flag_legacy_film` | 寫入 a／b 兩支＋`flags_written` 含兩者 | **PASS** |
| artId | `story_c16` | `story_c16` | **PASS**（佔位，未出圖） |
| conflict | （非 T） | `null` | **PASS** |

### C17｜最終定位／結算

| 欄 | 解鎖期望 | 成品 | 結果 |
|---|---|---|---|
| title／when | 最終定位／結算；1992 收束 | 同左；`1992收束 / W105-108` | **PASS** |
| 意向 | 幕前／幕後／雙線＋鎖 E01–E10 | `orientation_hint`=`['幕前','幕後','雙線']`；對白攤開後十選一 | **PASS** |
| 結局 | 事業結局 ID；愛情另計 | `ending_e01`…`e10`＋`career_lock`；愛情另表 notes | **PASS** |
| artId | `story_c17`＋`ending_e01`…`e10` | 節點 `story_c17`；catalog／choice 各帶 `ending_e0x` | **PASS**（佔位） |
| 台名 | 星河 | setting「星河電視台會議室…」 | **PASS** |

**Free-choice vs auto-calc（soft）：** detail **無** `requires`／gate／自動結算說明；十檔皆可點。與 UNLOCK「結算優先序：玩家最終選擇 ＞ …」一致——**自由揀為準**；數值門檻留給引擎／後續表，不擋本輪 PASS。

---

## 3. 硬鎖掃描（phase5 body＋整包；合併抽查同規）

| 項 | 結果 | 證據 |
|---|---|---|
| 禁詞 薄本／趕板／苛約／拖字訣 | **PASS** | phase5 body＋整包 **0**；merge 正文同 **0** |
| TVB／tvb／無綫／無線 | **PASS** | phase5／merge player-facing **0**；台名「星河」 |
| 真人藝名 | **PASS** | 周星馳／劉德華等抽樣 **0**（關海媚＝本戲虛構） |
| 政治／抗爭再現 | **PASS** | 無六四／遊行／民運等 |
| 關海媚 HE | **PASS** | 僅 C13 公關角色；無 commit／無 HE 檔／無專屬結局；C16–C17 無出現 |
| 出圖成品 | **PASS** | md「未出圖」；repo `story_c16*`／`ending_e*` 檔 **0** |
| `gigs_1988.json` | **PASS** | mtime **2026-11-02 16:51**（HK）；phase5／merge **22:41**——本輪未動 |
| DeepSeek finish | stop | C16／C17＝`deepseek-chat`；`finish_reasons` 皆 `stop` |
| 電報主導 | **PASS** | C16–C17 無 ≤12 字碎片對白 |

---

## 4. 合併完整性｜`story_detail_c1_to_c17.json`

| 檢查 | 結果 |
|---|---|
| `coverage.count` | **17**；`missing=[]`；ids C1…C17 連續無 dup |
| meta | `version=1`；`locale=zh-Hant-written-HK`；`source=merge phase1–5…`；`qa.endings_names_ok=true` |
| C16／C17 vs `story_detail_phase5_c16c17.json` | **全等**（sort_keys） |
| C1–C7／C8–C10／C11／C12–C15（除下項）vs 各分包 | **全等** |
| **C14.conflict** | **DRIFT：** phase4 包＝`T6`；**merge＝`null`** |

### 建議（劇本側，非本輪代改）

1. 重蓋合併：`C14.conflict = "T6"`（對齊 UNLOCK T6／phase4 包），再標 merge meta／changelog。  
2. （可選）引擎映射：E05 stats 目前 `craft+1/standing+1`，UNLOCK 強調 `action`——wiring 時補 `action` 或改 stats。  
3. （可選／前輪）C8–C10 對白口語助詞（哋／嘅／咩等）仍在 merge——非本包引入；若要書面統一可另開 polish，**不擋** arc 完結判定。

---

## 5. Soft nits 一覽（非 hard FAIL）

1. **Merge C14.conflict 未帶上 T6**（唯一深比漂移）——wiring 前應修。  
2. **C17 無 auto-calc／資格閘**——刻意自由揀；引擎若要「推薦結局」需另表。  
3. **E05 effects.stats 未用 `action` 鍵**。  
4. **C16 無 `orientation_hint`**——解鎖未要求；僅 C17 有＝OK。  
5. **前輪口語殘留**限 C8／C10（merge 帶入），phase5 新增 **0**。

---

## 6. md 摘要 vs JSON

`PLOT_DETAIL_PHASE5_C16C17_v1.md` 與 phase5 JSON：title／when／flags／十檔名／orientation／artId **一致**；標「未出圖」正確。

---

## 7. 結論給用戶／劇本 manager

- **Phase5 C16–C17：PASS with nits**（硬鎖全過；結局名一字不差；十檔齊）。  
- **合併 C1–C17：PASS with nits**——唯一實質 nit＝**C14.conflict 未合併 T6**。  
- **文字主線 C1–C17 可當完備**供 wiring／預覽邏輯對接；**出圖仍暫緩**；修 C14 merge 後可視為 canonical 合併定稿。  
- 本報告路徑：`/workspace/star-volunteer-web/content/QA_PHASE5_C16C17_v1.md`。
