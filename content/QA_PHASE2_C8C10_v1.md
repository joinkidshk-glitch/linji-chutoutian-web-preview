# QA｜Phase2 C8–C10 v1（文件／詞彙｜非 browser）

> **範圍：** `story_detail_phase2_c8c10.json`＋`PLOT_DETAIL_PHASE2_C8C10_v1.md`；合併 `story_detail_phase1_to_c10.json`（C1–C10）。  
> **基準：** C1–C7 = `story_detail_phase1.json` **v3**（含 C6 title 已修＝「首次正式約會對象」）；解鎖 `PLOT_DETAIL_UNLOCK_v1.md` §2 C8–C10／§3 T2／§4 藍若曦／§5 高俊傑·高文瀚·張子駿；詞彙 `COPY_STYLE_HK_LEXICON.md`。  
> **風格對齊：** `QA_PHASE1_C1C7_v3.md`（不引用已作廢 v2）。  
> **本輪：** 只報告、**未改**任何 content 檔。  
> **時間：** 2026-11-02 22:34（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| 禁詞正文清零（薄本／趕板／苛約／拖字訣） | **PASS**（0） |
| 硬鎖台名／真人／政治／結局／出圖／gigs_1988 | **PASS** |
| 結構鎖 vs 解鎖表（C8–C10／T2） | **PASS** |
| 電報文言短句是否佔主導 | **PASS**（均長 23.2；≤10 字僅 3.9%） |
| 標題正確（無 C6 類誤貼） | **PASS** |
| 合併檔 C1–C7＝v3；C8–C10＝phase2 pack | **PASS**（deep equal） |
| Soft：錯字／口語密度／rel_* 數值 | **NIT**（見下；**非** hard FAIL） |

**C1–C10 merge 是否安全：** **是**——可作 C1–C10 合併基準使用。  
**C11+：** **不擋產製**；建議劇本側順手修 C8「位置置」錯字，並視需要把 C8／C10 對白再往書面語靠攏（C9 已達標）。

---

## 1. 禁詞計數（phase2 `nodes` 全樹＝title／setting／synopsis／beats／choice label+notes）

| 詞 | C8–C10 body | 備註 |
|---|---:|---|
| 薄本 | 0 | |
| 趕板 | 0 | |
| 苛約 | 0 | |
| 拖字訣 | 0 | C9_c 用「暫不答覆」✅ |

---

## 2. 硬鎖掃描

| 項 | 結果 | 證據 |
|---|---|---|
| TVB／tvb／無綫／無線（player-facing） | **PASS** | body＋整包 JSON 字串 **0** |
| `event_tvb_anni` | **未出現** | 解鎖表寫 `story_c10`／`event_tvb_anni`；成品只留 `artId=story_c10`。**不計 FAIL**（反而避開 tvb 字串）；列 **NIT／unlock 對齊**：日後若要雙 artId，宜改名去 tvb 字樣 |
| 星河電視台 | **PASS** | C8 setting／synopsis；C10 setting（×3） |
| 真人藝名抽樣 | **PASS** | 周星馳／劉德華／張國榮等 0 |
| 政治／抗爭詞 | **PASS** | 六四／遊行／示威／民運等 0 |
| 完整 HE／已出圖宣稱 | **PASS** | 0；artId 僅 `story_c8`…`c10` 佔位 |
| `gigs_1988.json` | **PASS** | mtime **2026-11-02 16:51**（HK）；phase2 **22:31**——本輪未動 gigs |
| DeepSeek finish | stop×3 | models 皆 `deepseek-chat` |

---

## 3. 結構鎖（對 UNLOCK §2／§3）

| 節點 | title | when／era | artId | conflict | choices | 關鍵 effects | 鎖結果 |
|---|---|---|---|---|---|---|---|
| C8 | 商業片 vs 文藝線 | 1989春／`era_1989_spring_quiet` | `story_c8` | None | `C8_a`／`C8_b` | a→`route_commercial`（fame+1 wealth+1）；b→`route_indie`（craft+2）；cast 含高文瀚＋張子駿＋何生 | **PASS** |
| C9 | 藍若曦擋狗仔後 | 1989夏秋／`era_1989_summer_literary` | `story_c9` | None | `C9_a`／`b`／`c` | 認愛→`flag_public_romance`+`lan_confess`+`rel_lan`+2；切割→`lan_cut`+`rel_lan`-1；模糊→`lan_blur`+`rel_lan`+1 | **PASS** |
| C10 | 台慶位 vs 陪伴 | 1989冬／`era_1989_winter_anniversary` | `story_c10` | **T2** | `C10_a`／`b`／`c` | 硬搶→`anni_seize`+`standing`+2；讓位→`anni_yield`；協調→`anni_mediate`+`standing`+1；cast 含高俊傑＋何生 | **PASS** |

摘要 md 與 JSON 選擇／旗標一致。  
**NIT（soft）：** 解鎖 axes 寫 C10 影響「當前約會線 `rel_*`」——成品僅用 notes 敘事（「約會線可能受影響／有進展」），**未寫**具體 `rel_*` delta。語意在，數值層可選補；**非**缺 T2／缺三選結構。

---

## 4. 合併完整性

| 檢查 | 結果 |
|---|---|
| merged ids | C1…C10 連續、無缺無重 |
| C1–C7 vs `story_detail_phase1.json` v3 | **逐節點 deep equal**（含 C6 title＝「首次正式約會對象」） |
| C8–C10 vs `story_detail_phase2_c8c10.json` | **deep equal** |
| `parts` 指標 | `c1c7`→phase1.json；`c8c10`→phase2 pack |
| merged.`version` | **1**（合併包版本；內容已含 v3 C1–C7）——可接受；勿與 phase1 `version:3` 混淆 |

**結論：merge safe = YES。**

---

## 5. 對白長度／電報風（soft；對齊 lexicon「不要電報短句」）

| 節點 | 行數 | 均長（字） | ≤10% | ≤12% | 評 |
|---|---:|---:|---:|---:|---|
| C8 | 21 | 17.8 | 9.5% | 14.3% | 可接受；兩句 9 字收束 |
| C9 | 16 | 25.9 | 0% | 0% | **良好**（書面完整） |
| C10 | 14 | 28.2 | 0% | 0% | **良好** |
| **合計** | 51 | **23.2** | **3.9%** | 5.9% | **非電報主導 → 不觸 hard FAIL** |

大陸網文黑話抽樣（卷王／破防／yyds／賦能／絕絕子等）：**0**。

---

## 6. Soft NITs（建議修；不擋 C11+）

1. **錯字（C8 高文瀚）：**「我就可以幫你留這個**位置置**。」→ 應為「位置」。  
2. **口語密度：C8／C10 偏口語粵拼寫入書面對白**（我哋／你哋／嘅／諗／咩／俾／畀／啩／面左左 等）；C9 幾乎全書面。pack `qa.oral_leftover: []` **自稱清空偏樂觀**。對齊 `COPY_STYLE_HK_LEXICON`「全面書面語」可再 polish 一輪（非禁詞級 FAIL）。  
3. **C10 `rel_*` 無數值 delta**（見 §3）——可選。  
4. **Unlock `event_tvb_anni`：** 成品未用（佳）；建議日後改 unlock／art 命名去 `tvb` 字樣，免與台名硬鎖混淆。

---

## 7. Blockers

| 對 | Blocker？ | 說明 |
|---|---|---|
| **C11+ 產製** | **否** | 結構／禁詞／硬鎖／合併皆過 |
| **C8–C10 文字定稿「全乾淨」** | **小否** | 建議修「位置置」；口語密度可選 |
| **出圖** | 維持暫緩 | 本輪未觸 |
| **引用 v2 QA** | 禁止 | 本報告未引用 |

---

## 8. 給劇本 manager／用戶一句

**C8–C10 文件 QA＝PASS with nits。** 解鎖結構（商業／文藝、藍若曦三選、T2 台慶三選）與星河硬鎖、禁詞清零、C1–C10 合併 deep-equal 均過關；**merge 可安心用**。請順手改 C8「位置置」；C8／C10 對白若要完全貼「書面語」指南可再收一輪口語（C9 已是樣板）。**不擋 C11+。**

*QA agent｜document only｜未改 content*
