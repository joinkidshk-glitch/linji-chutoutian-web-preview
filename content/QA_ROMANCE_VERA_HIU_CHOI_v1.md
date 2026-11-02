# QA｜Romance Pack1 Vera／林曉晴／周采兒 v1（文件／詞彙｜非 browser）

> **範圍：** `story_detail_romance_vera_hiu_choi.json`、`PLOT_DETAIL_ROMANCE_V1.md`。  
> **基準：** 解鎖 `PLOT_DETAIL_UNLOCK_v1.md` §4；主計劃 `PLOT_MASTER_PLAN_v1.4-DS.md` §5–6／T5／關海媚無 HE；詞彙 `COPY_STYLE_HK_LEXICON.md`。  
> **風格對齊：** `QA_PHASE5_C16C17_v1.md`。  
> **本輪：** 只報告、**未改**任何 story content。  
> **時間：** 2026-11-02 22:56（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| 硬鎖（禁詞／星河／真人／政治／關海媚非第六攻略／出圖／每線 5 節／HE·BE／Vera `flag_vera_commit`／Vera crisis `T5`／Choi meet↔C5） | **PASS** |
| 解鎖 §4 弧（meet→push×2→crisis→ending）三線齊 | **PASS** |
| 愛情與事業結局並存文案 | **PASS**（各 HE／BE notes 均寫「可與事業結局並存」） |
| 電報短句是否佔主導 | **PASS**（均長 **26.1**；≤12 字僅 **3** 句，非主導） |
| md ↔ JSON | **PASS**（title／when／flags／artId／conflict／choices 一致） |
| Soft：旗標命名混用；「我」vs「阿偉」；choi choice id 前綴；C13 conflict 欄；beats 密度 | **NIT**（非 hard FAIL） |

**出圖：** 仍暫緩（`rom_*` 僅佔位；repo 無對應成品圖檔）。

**Pack1 可否一邊寫 Pack2（藍若曦＋徐寶珊）：** **可以。** 無 hard FAIL；nits 不擋 Pack2 開工。建議 Pack2 起草時統一旗標／speaker 慣例，回頭一次 polish Pack1。

**Wiring 可否開工：** **文字可作 Pack1 wiring 草案**——見 §5 建議先對齊旗標／id／POV，避免引擎雙套命名。

---

## 1. 解鎖 §4 對齊表

| 線 | 期望 | 成品 | 結果 |
|---|---|---|---|
| **Vera** meet | P1 造型／唱片 | `R_vera_meet` P1｜造型間／星河｜1988春夏 | **PASS** |
| Vera push | 形象合作、小聚 | `push1` 形象會議；`push2` 茶餐廳小聚 | **PASS** |
| Vera crisis | T5 打歌期陪伴 | `R_vera_crisis`｜`conflict=T5`｜1991秋打歌後台；陪她 vs 趕通告 | **PASS** |
| Vera ending | 信任形象 vs 工具化；`rel_vera`、`flag_vera_commit` | HE：`flag_vera_he`＋**`flag_vera_commit`**＋`rel_vera+3`；BE：`flag_vera_be`＋`rel_vera-2`；`parallelOk=false` | **PASS** |
| **林曉晴** meet | P1 同期廠景 | `R_hiu_meet` P1｜廠景休息角｜1988春 | **PASS** |
| 曉晴 push | 互相帶通告、比較溫柔 | `push1` 茶餐廳帶通告；`push2` 夜班殺青後約糖水 | **PASS** |
| 曉晴 crisis | 競爭比較／同場搶位 | `R_hiu_crisis` 同場搶通告／試鏡廊｜1991 | **PASS** |
| 曉晴 ending | 同行情侶 vs 漸行；`rel_hiu` | HE：`flag_hiu_he`＋`flag_hiu_commit`；BE：`flag_hiu_be`；皆帶 `rel_hiu` | **PASS** |
| **周采兒** meet | C5 小訪前後 | setting「片場採訪角（**C5小訪前後**）」｜1988夏｜`era_1988_summer_anni` | **PASS** |
| 采兒 push | 爆料交換、私下約 | `push1` 茶記爆料；`push2` 私下晚餐 | **PASS** |
| 采兒 crisis | C13 真假緋聞 | setting「周刊會議室（**對齊C13真假緋聞**）」｜1991冬；公開真情 vs 公關切割；`flag_public_romance`／`choi_deny_romance` | **PASS**（結構）；見 soft：`conflict` 欄仍 `null` |
| 采兒 ending | 公開真情 vs 公關犧牲；`rel_choi` | HE：`flag_choi_he`＋`flag_choi_commit`；BE：`flag_choi_be` | **PASS** |

**節點數：** 15＝3×（meet＋push＋push＋crisis＋ending）；`qa.lines`／`arc` 自述正確。

---

## 2. 硬鎖掃描

| 項 | 結果 | 證據 |
|---|---|---|
| 禁詞 薄本／趕板／苛約／拖字訣 | **PASS** | body **0** |
| TVB／tvb／無綫／無線 | **PASS** | **0**；台名「星河電視台」出現 |
| 真人藝名 | **PASS** | 周星馳／劉德華等抽樣 **0** |
| 政治／抗爭再現 | **PASS** | 六四／民運／遊行／抗爭 **0** |
| 關海媚作第六攻略／HE | **PASS** | 本包 **0** 出現；無 `flag_*_commit` 給關 |
| Pack2 人物誤入 | **PASS** | 藍若曦／徐寶珊 **0** |
| 每線缺 stage | **PASS** | 三線皆 5 節、弧序正確 |
| Ending 無 HE／BE | **PASS** | 三線各 2 支 |
| Vera HE 缺 `flag_vera_commit` | **PASS** | HE 雙寫 `flag_vera_he`＋`flag_vera_commit` |
| Vera crisis 非 T5 | **PASS** | `conflict":"T5"` |
| Choi meet 未掛 C5 | **PASS** | setting 明示 C5 小訪前後 |
| 電報主導 | **PASS** | ≤12 字僅 3；均長 26.1 |
| 出圖成品 | **PASS** | `rom_vera_*`／`rom_hiu_*`／`rom_choi_*` 成品檔 **0**；md「未出圖」 |
| `gigs_1988.json` | **PASS** | mtime **2026-11-02 16:51**（HK）；romance **22:55**——本輪未動 |
| DeepSeek finish | stop | vera／hiu／choi／expand_* 皆 `stop` |
| 每 choice 有 `rel_*` | **PASS** | 掃描 **MISSING=0** |
| 確定前平行 | **PASS** | meet→crisis `parallelOk=true`；ending=`false` |
| 無擅自批核 | **PASS** | 未改 MASTER／UNLOCK；僅 detail 包 |

---

## 3. Soft nits（非 hard FAIL）

1. **旗標命名兩套：** Vera 全程 `flag_vera_*`；曉晴／采兒前段多用裸前綴（`hiu_meet_exchange`、`choi_give_tip`…），至 ending 才用 `flag_hiu_*`／`flag_choi_*`。另：crisis 公開支用全域感 `flag_public_romance`（合理，但與 `choi_deny_romance` 不對稱）。  
   → **建議（劇本側，非本輪代改）：** Pack2 起統一 `flag_<line>_*`；Pack1 可另開 rename／alias 表供 wiring。

2. **POV 不一致：** Vera synopsis＋speaker＝「阿偉」；曉晴／采兒 synopsis＋對白 speaker＝「**我**」。  
   → 書面 polish 時統一第三人稱「阿偉」（或引擎映射「我」＝玩家）。

3. **Choi choice id 前綴：** 非 ending 用 `R_choi_*`，ending 用 `C_choi_*`；Vera／曉晴多用 `C_*`。  
   → wiring 前建議統一 `C_<line>_*`。

4. **Choi crisis `conflict`：** 解鎖掛 C13；成品僅 setting 文字「對齊C13」，`conflict=null`（無 T 碼——C13 非 T 表項，可接受）。若引擎要節點級掛鉤，可加 `linkedMain:"C13"` 或 notes——**soft**。

5. **Beats 密度不均：** Vera 多為 1 句／beat；曉晴／采兒 expand 後每 beat 常 2 句（ending 采兒 6 beats／12 lines）。非電報失敗，但節奏／字數與 Vera 差一截——可選後續對齊。

6. **Vera meet beats=6**（餘多為 5）——無害。

7. **曉晴 crisis 無獨立 conflict 代號**——解鎖未要求 T#；OK。

---

## 4. md 摘要 vs JSON

`PLOT_DETAIL_ROMANCE_V1.md` 與 JSON：三線節點 id／when／setting／artId／Vera `T5`／HE·BE flags（含 `flag_vera_commit`）／C5·C13 註記 **一致**；標「未出圖」正確。

---

## 5. Wiring 建議／blocker 一覽

| 優先 | 項 | 擋不擋 Pack2／文字定稿 |
|---|---|---|
| A | 接受現況雙套旗標 **或** 統一 rename | **不擋** Pack2；**建議** wiring 前定 alias |
| A | Speaker「我」→「阿偉」或 UI 映射 | 不擋 |
| B | Choi `R_`→`C_` choice id | 不擋 |
| B | Choi crisis 加 `linkedMain:C13`（可選） | 不擋 |
| — | Hard FAIL | **無** |

**無必須先修才能寫 Pack2 的 blocker。**

---

## 6. 結論給用戶／劇本 manager

- **Romance Pack1（Vera／曉晴／采兒）：PASS with nits**（硬鎖全過；15／15；T5＋`flag_vera_commit`＋C5／C13 掛鉤齊）。  
- **可開 Pack2（藍若曦＋徐寶珊）並行**；出圖仍暫緩。  
- 本報告路徑：`/workspace/star-volunteer-web/content/QA_ROMANCE_VERA_HIU_CHOI_v1.md`。
