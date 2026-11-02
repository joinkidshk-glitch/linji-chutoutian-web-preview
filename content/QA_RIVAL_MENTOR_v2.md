# QA｜Pack3 對手／導師／友情／資本弧 v2 覆測（書面語｜非 browser）

> **範圍：** `story_detail_rival_mentor.json`（**version 2**）、`PLOT_DETAIL_RIVAL_MENTOR_v1.md`（已描述 v2）。  
> **對照 FAIL：** `QA_RIVAL_MENTOR_v1.md`（beat 口語 ≈92% → 總評 FAIL）。  
> **書面標準：** romance Pack1／Pack2／Tang（beat 口語標記線 **0%**）；詞彙 `COPY_STYLE_HK_LEXICON.md`；解鎖 `PLOT_DETAIL_UNLOCK_v1.md` §5。  
> **v1 備份結構對照：** `story_detail_rival_mentor_v1_backup.json`。  
> **本輪：** 只報告、**未改**任何 story content。  
> **時間：** 2026-11-02 23:17（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| 硬鎖：**全面書面語**（claimed 改寫欄：synopsis／beats.lines／choices.label／effects.notes） | **PASS**（beat **0／194＝0%**；body 標記線 **1／450＝0.22%**，僅 1 條 label） |
| 硬鎖：禁詞 body／星河／真人／政治／非戀愛結局／pcSilent／C_*／8×5＝40／出圖暫緩／gigs_1988 | **PASS** |
| 結構相對 v1：id／flag／choice id／artId／linksMain／arcBeat／fingerprints | **PASS**（與 backup **0** struct diff；40 節全文有 rewrite） |
| 解鎖 §5 八線＋連線 | **PASS**（同 v1） |
| 高俊傑 ≠ 張克凡聲口（書面後仍可分） | **PASS** |
| Soft：title／setting 未入 v2 改寫仍口語；少數 label／notes 殘「留低／企硬／學嘢」；synopsis「你」；v1 soft nits 仍在 | **NIT** |
| 自檢 `qa.pass`／`colloquialMarkerTotal=0` | **可參考**（與本掃一致於 beats；未掃 title／setting） |

**出圖：** 仍暫緩（`arc_*` 40 佔位；repo **0** 成品圖）。

**可否併入 C1–C17＋romance＋Tang wiring 草案：**  
- **可以。** v1 之 **copy-locked blocker（書面 FAIL）已解除**。  
- Pack3 可與主線＋五／六感情線一併作 **wiring 草案**（id／flag／links／正文 copy）。  
- Soft nits（title／setting 口語殘、1 條「學嘢」label、旗標命名／parallelOk 等）**不擋**草案；建議另開小修或 wiring 前掃一次 title／setting。

---

## 1. 書面語覆測方法與數字（對齊 v1 FAIL 方法）

### 方法
1. 取節點 `beats[].lines[]`、`synopsis`、`choices[].label`、`choices[].effects.notes` 為 **body copy**（即 v2 claim 改寫範圍）。  
2. FAIL 標記（v1 同批口語質感）：`呢個／唔係／嚟／嘅／咗／喺／嗰／啲／冇／喂／㗎／喎／啫／唔／咩／咁／嘢` 等（子串匹配）。  
3. **oral-hit line**＝該行至少命中 1 個標記；比率＝hit／總行。  
4. 對照 romance：Vera／藍徐／鄧 用同一正則。

### 結果

| 包 | beats | synopsis | choice labels | effects.notes | BODY 合計 |
|---|---|---|---|---|---|
| **Pack3 v1（舊 FAIL）** | **179／194（≈92%）** | 38／40 | ≈65 偏口語 | — | 主導口語 |
| **Pack3 v2** | **0／194（0.00%）** | **0／40（0%）** | **1／108（0.93%）** | **0／108（0%）** | **1／450（0.22%）** |
| Romance Vera | 0／128 | 0／15 | 0／30 | 0／8 | 0／181 |
| Romance 藍徐 | 0／37 | 0／11 | 0／23 | 0／23 | 0／94 |
| Romance 鄧 | 0／17 | 0／5 | 0／11 | 0／11 | 0／44 |

**唯一 body 標記命中：**  
`A_tong_push2`／`C_tong_push2_stay` label＝「同唐老師講，你想**留低學嘢**」（標記=`嘢`）。  
→ 相對 romance 仍可視為 **≈0%**；**不構成 hard FAIL**（v1 門檻為 beats 近全面口語）。建議順手改「留下多學一點／想留下跟唐老師學」。

**抽樣前後（檔內 `qa.afterSamples` 與現文一致）：**  
- `A_ko_meet` line0：v1「喂，呢個位我早排咗…」→ v2「那個位置我早已排好，你還不明白嗎？」  
- `A_hakfan_meet`：「你也是等《赤道線》嗎？…這個位置我爸爸和監製吃過飯。」  
- `A_lei_crisis`：「合約我改過，已經很給你面子。」

---

## 2. 硬鎖掃描（非書面項）

| 項 | 結果 | 證據 |
|---|---|---|
| 禁詞 薄本／趕板／苛約／拖字訣 | **PASS** | body **0**；`rule` 提及薄本／趕板／苛約（允許） |
| 星河／禁 TVB | **PASS** | 「星河」**36**；TVB／tvb／無綫／無線 **0** |
| 真人藝名 | **PASS** | 周星馳／劉德華等抽樣 **0** |
| 政治／抗爭 | **PASS** | 六四／民運／遊行／抗爭／政治 **0** |
| 戀愛 HE／BE | **PASS** | 無 `flag_*_he`／`*_be`；結局 rival_respect／cold_war／mentor_*／friend_saved／ally_danger 系 |
| pcSilent／阿偉非 speaker | **PASS** | 全 40 `pcSilent=true`；speakers 無阿偉 |
| Choice id `C_*` | **PASS** | 非 `C_`＝**0** |
| 8×5＝40／每線 meet+push×2+crisis+ending | **PASS** | arcs 8；每線 5 ids |
| 高≠張 | **PASS** | ko：插隊／難讀名／「不是星二代」；hakfan：爸爸飯局／資源壓／世家節奏——書面後仍可分 |
| 出圖 | **PASS（暫緩）** | artId=`arc_*`×40；成品檔 **0** |
| `gigs_1988.json` | **PASS** | mtime **2026-11-02 16:51**（HK）；本包 **23:16**——未動 |
| 結構 vs v1 backup | **PASS** | id／choice id／flags／stats／artId／linksMain／conflict／phase／when／cast／parallelOk／pcSilent／beat speakers＋line counts：**0 diff**；40／40 有正文改寫；title／setting **未改**（符合 claim） |

---

## 3. 解鎖 §5（覆核，同 v1）

| 線 | 期望連線 | 結果 |
|---|---|---|
| 高俊傑 `A_ko_` | C3,C10,C12,T2 | **PASS** |
| 張克凡 `A_hakfan_` | P2–P4 資源場 | **PASS** |
| 張子駿 `A_tsijun_` | C8,C11,C17,E03,T3 | **PASS** |
| 方小龍 `A_fong_` | P3 替身,E05 | **PASS** |
| 唐素雲 `A_tong_` | P2 去留,E09 | **PASS** |
| 何生 `A_ho_` | C2,C4,E01 | **PASS** |
| 高文瀚 `A_gao_` | C8,C12,E02,T4 | **PASS** |
| 雷勁 `A_lei_` | C7,`flag_anti_lei` | **PASS** |

md 路線表／未出圖／pcSilent／「只改書面」聲明與 JSON **一致**。

---

## 4. Soft nits（非 hard FAIL）

1. **title／setting 仍口語（改寫範圍外）：** title **8／40**、setting **21／40** 仍含 嘅／咗／喺／嚟／嘢 等；romance 同欄 **0／***。  
   → 與「全面書面語」產品觀感未完全齊；**建議 v2.1 只掃 title＋setting**（不改弧）。不擋 wiring 草案。

2. **殘口語／半口語（標記外或邊緣）：**  
   - label「留低學嘢」「留低，…」「企硬…」；notes「企硬留低」；beat「觀眾才會留低」。  
   - synopsis：`喝住`（`A_fong_crisis`）、`孭飛`（`A_hakfan_crisis`）——港產可懂，但若硬鎖「書面易讀」可改「喝止／喊住」「揹責任／頂飛」。

3. **synopsis 人稱：** 全 40「你…」；romance 多用「阿偉…」。pcSilent OK；導語宜全作統一（延續 v1 nit）。

4. **延續 v1 soft：** `conflict` 混型；全部 ending `parallelOk=true`（僅 `A_fong_crisis=false`）；旗標跨 kind（`flag_ko_mentor_complete` 等）；雷勁 phase 序；主線並行加深播表。

5. **詞彙邊角：** setting 仍見「通告板」（lexicon 可保留但優先通告欄）；「劇組」「片酬」「落地（動作落地）」——非硬禁，偏港／中性。

6. **Pack 自檢** `colloquialMarkerTotal=0`／`writtenApproxPass=true`：對 beats 可信；**未涵蓋 title／setting**，QA 以本報告為準。

---

## 5. Wiring 建議

| 優先 | 項 | 擋不擋 |
|---|---|---|
| — | 書面語（beats／synopsis／絕大多數 label／notes） | **已過** → **可 copy wiring 草案** |
| A | 修 `C_tong_push2_stay`「學嘢」＋可選清「留低／企硬」 | 不擋草案 |
| A | title／setting 書面小修（v2.1） | 不擋草案；擋「全欄位 copy-locked 定稿」觀感 |
| B | conflict／parallelOk／旗標命名／雷勁 phase／synopsis「你」vs「阿偉」 | 不擋草案 |
| — | 禁詞／星河／非戀愛／pcSilent／40 節／§5 | **已過** |

---

## 6. 結論給用戶／劇本 manager

- **Pack3 v2 覆測：PASS with nits**（v1 書面 hard FAIL **已修**）。  
- beats 口語標記 **0%**，與 romance 齊；禁詞清；結構相對 v1 **一字未改 id／flag／choice／links**；非戀愛結局／pcSilent／星河／高≠張／出圖暫緩均達標。  
- **可與 C1–C17＋romance Pack1／2＋鄧麗萍一併進入 wiring 草案。**  
- Soft：title／setting 未改仍口語；1 條「學嘢」label——建議後續小修，**不擋**本輪放行。  
- **出圖仍暫緩。**  
- **未改** story content。
