# QA｜Romance 鄧麗萍（可選第六線）v1（文件／詞彙｜非 browser）

> **範圍：** `story_detail_romance_tang.json`、`PLOT_DETAIL_ROMANCE_TANG_v1.md`。  
> **基準：** 解鎖 `PLOT_DETAIL_UNLOCK_v1.md` §4 鄧麗萍列；主計劃 `PLOT_MASTER_PLAN_v1.4-DS.md` §11（O2 雙條件／O1 關海媚不升格）；詞彙 `COPY_STYLE_HK_LEXICON.md`；Pack2 stub `R_tang_meet_stub`（`supersededBy: R_tang_meet`）。  
> **風格對齊：** `QA_ROMANCE_LAN_XU_v1.md`；書面硬鎖對照 Pack3 FAIL（口語主導＝FAIL）。  
> **本輪：** 只報告、**未改**任何 story content。  
> **時間：** 2026-11-02 23:15（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| 硬鎖（禁詞／星河／真人／政治／關海媚無 HE／出圖／5 節 meet→push×2→crisis→ending／HE·BE＋commit／pcSilent／C_*／flag_tang_*／書面非 Pack3 級口語／雙閘有文件） | **PASS** |
| 解鎖 §4 鄧麗萍列（雙條件／排片·數據互助／檔期數據 vs 人情／另計 HE·BE／旗標） | **PASS** |
| md ↔ JSON | **PASS**（5 節 title／choice id／HE·BE flags／stub 註記一致） |
| Soft：雞生蛋 openConditions、`rel_tang_threshold` token、synopsis「你」vs Pack1／2「阿偉」、stub 雙寫路徑、crisis 三支 vs 解鎖兩極 | **NIT**（非 hard FAIL） |

**出圖：** 仍暫緩（`rom_tang_*` 五佔位；repo **0** 對應成品圖檔）。

**可選第六感情線：** **文字可作 wiring 草案**——五節齊、數據腔書面、HE／BE＋`flag_tang_commit`、stub supersede 兩邊有註。建議 wiring 前先釐清 meet 開閘條件（見 §3.1），否則引擎若對 meet 亦 AND `flag_tang_open` 會死鎖。

---

## 1. 解鎖 §4 對齊表

| 期望（UNLOCK） | 成品 | 結果 |
|---|---|---|
| **雙條件** `flag_tang_open`＋`rel_tang` 門檻 | 檔級＋每節 `openConditions: [flag_tang_open, rel_tang_threshold]`；md「開線閘」明文；meet choice 可寫 `flag_tang_open`；notes：push+ 需雙條件 | **PASS**（文件有；實作雞生蛋 → §3.1） |
| 認識＝排片／數據 | `R_tang_meet` 上門談排片／上座率談判（P3｜1990秋）；`supersedes R_tang_meet_stub` | **PASS** |
| 推進＝排片／數據互助 | `push1` 中控室數據互助；`push2` 黃金檔試水＋可略觸 secret | **PASS** |
| 危機＝檔期數據 vs 人情 | `R_tang_crisis` conflict／title 對題；三支 data／favor／middle | **PASS**（兩極＋折衷 → §3.5） |
| 另計 HE／BE | `C_tang_ending_he`→`flag_tang_he`＋**`flag_tang_commit`**＋`rel_tang+3`；BE→`flag_tang_be`；notes「可與事業結局並存」；`parallelOk=false` | **PASS** |
| 主旗標 `flag_tang_open`、`rel_tang` | 寫入／stats 齊；另線內 `flag_tang_*` | **PASS** |
| 關海媚不升格 | 本檔 **0** 關海媚；無其 commit／結局 | **PASS** |

**節點數：** 5＝meet＋push＋push＋crisis＋ending；`qa.node_count=5`／`romanceLines=[tang]` 自述正確。

---

## 2. 硬鎖掃描

| 項 | 結果 | 證據 |
|---|---|---|
| 禁詞 薄本／趕板／苛約／拖字訣 | **PASS** | body **0** |
| TVB／tvb／無綫／無線 | **PASS** | **0**（本檔無台名句；stub／他包用星河） |
| 真人藝名 | **PASS** | 周星馳／劉德華等抽樣 **0** |
| 政治／抗爭再現 | **PASS** | 六四／民運／遊行／抗爭／政治 **0** |
| 關海媚作第六攻略／HE | **PASS** | 本檔無；MASTER O1／UNLOCK 維持暧昧 |
| 缺 stage／缺 HE·BE／缺 commit | **PASS** | 五節齊；HE 雙寫 he＋commit |
| **書面語**（對照 Pack3 ≈92% 口語 FAIL） | **PASS** | beats 17 線；Pack3 級標記（喺／嘅／咗／冇／唔係／嚟／嗰／啲／㗎／喎…）在 lines+synopsis+label+setting **0**。自檢 `oral_leftover:[]` 大致可信。輕量港式用字見 soft §3.6，**未**構成主導口語 |
| 電報主導 | **PASS** | 均長 ≈43.3；≤12 字句 **0** |
| pcSilent／阿偉非 speaker／無玩家「我」beats | **PASS** | 全節 `pcSilent=true`；`aw_first_person_lines=0`；beats「我」皆鄧／助理自述 |
| Choice id `C_*` | **PASS** | 非 `C_`＝**0** |
| 旗標 `flag_tang_*` | **PASS** | 全寫入皆 `flag_tang_` 前綴 |
| `effects.flags`＋`effects.stats` | **PASS** | MISSING＝**0**；每 choice 有 `rel_tang`（或 ending 含 standing） |
| 確定前平行 | **PASS** | meet→crisis `parallelOk=true`；ending=`false` |
| 數據腔 | **PASS** | 上座／午夜場／百分／數據／檔期／黃金檔等高頻；性格對齊排片審判官 |
| 出圖成品 | **PASS（暫緩）** | `rom_tang_*` 佔位；成品檔 **0**；md「出圖暫緩」 |
| `gigs_1988.json` | **PASS** | mtime **2026-11-02 16:51**（HK）；本包 **23:13**——未動 |
| 雙閘有文件 | **PASS** | md「開線閘」＋ JSON `openConditions`／`openConditionsNote`／`stubCompat` |
| 無擅自批核 MASTER／UNLOCK | **PASS** | 僅 detail 包 |

---

## 3. Soft nits（非 hard FAIL）

1. **雞生蛋（meet × `flag_tang_open`）：** 檔級與 **`R_tang_meet` 自身** `openConditions` 皆含 `flag_tang_open`，同時 `C_tang_meet_data` 才寫入該旗。若引擎對 meet 亦要求雙條件已滿足 → **無法進入 meet**。  
   - 成品已用 `openConditionsNote`／notes 意圖：「本節可寫入 open；**push1 起**需雙條件」。  
   - **另：** `C_tang_meet_wait` 只寫 `flag_tang_met_wait`、`rel_tang:0`——揀 wait＝本節不開閘，需另途（stub 聯絡／任務）再取 `flag_tang_open`。  
   → **建議（劇本／wiring）：** meet 的 `openConditions` 改空或僅相位／任務閘；雙條件只掛 push1+；或引擎特例「meet 豁免 open」。數值門檻另定（見下）。

2. **`rel_tang_threshold` 係條件 token、非數字：** schema 無 `rel_tang >= N` 欄；與 UNLOCK「關係門檻」語意對，但 wiring 須另表（例 `rel_tang>=2`）把 token 解成數值，否則推不進 push。

3. **synopsis／label 用「你」、0「阿偉」：** Pack1／Pack2 synopsis 統一「阿偉」（Vera 包 你=0／阿偉=12；藍徐 你=0／阿偉=16）。本包 synopsis「你」×14、「阿偉」×0——與 Pack2 steering 不一致。rule 仍寫「玩家=阿偉」。  
   → soft；配線前建議統一第三人稱敘「阿偉」或明文允許第二人稱 synopsis。

4. **Stub supersede：** Pack2 `R_tang_meet_stub.supersededBy=R_tang_meet`＋`supersededByFile`；本檔 `supersedes`＋`stubCompat`——**兩邊對齊**。惟 stub **仍可**寫 `flag_tang_open`（公關偶遇），正式 meet 亦寫——雙入口並存。  
   → wiring：正式線優先排片 meet；stub 若保留僅作 `rel_tang`／`flag_tang_met` 或標記 deprecated，避免兩套「初遇」並行。

5. **Crisis 三支 vs 解鎖兩極：** UNLOCK 危機欄＝「檔期數據 vs 人情」；成品另加 `C_tang_crisis_middle` 折衷。屬豐富化，**不擋**；若要事件↔感情兩極對射，折衷可映射「偏數據的溫和」或獨立 flag。

6. **輕量港式殘餘（非 Pack3 級）：** setting「螢幕上**跳住**」「盡頭**係**一間」；對白「**企得住**」；choice／notes「**孭**數／孭上座率」「**識做**／識計數」。屬港產書面可接受偏口，建議下一輪輕潤（跳住→跳動／顯示；係→是），**不**升 hard FAIL。

7. **Meet phase：** 正式 meet＝P3／1990秋；stub＝P4／1991——時序上正式線更早，合理；wiring 勿兩節都當「首次見面」。

---

## 4. md 摘要 vs JSON

`PLOT_DETAIL_ROMANCE_TANG_v1.md` 與 JSON：5 節 id／title／when／setting／openConditions／supersedes／11 choice id／HE·BE（含 commit）／QA 自檢欄 **一致**；標雙條件、stub 相容、出圖暫緩正確。

---

## 5. Wiring 建議／blocker 一覽

| 優先 | 項 | 擋不擋可選第六線 wiring 草案 |
|---|---|---|
| **A** | meet 豁免／清空 `openConditions` 中的 `flag_tang_open`（或引擎特例） | **不擋文字草案**；**擋**「可跑通的開線」若引擎天真 AND |
| **A** | `rel_tang_threshold` → 具體數字表 | 不擋文字；擋數值閘實作 |
| B | synopsis「你」→「阿偉」對齊 Pack1／2 | 不擋 |
| B | stub 棄用策略（只留 rel／deprecated） | 不擋；避免雙初遇 |
| B | setting 跳住／係 輕潤 | 不擋 |
| — | Hard FAIL | **無** |

**無必須先改 copy 才能當 wiring 草案的硬 blocker；開線邏輯須在實作前釐清 A 項。**

---

## 6. 結論給用戶／劇本 manager

- **Romance 鄧麗萍可選線：PASS with nits**（硬鎖全過；書面遠高於 Pack3；五節＋HE／BE＋commit＋數據腔＋stub supersede 齊）。  
- **可選第六感情線文字：** **可作 wiring 草案**；實作前務必處理 meet 雞生蛋與 `rel_tang_threshold` 數值。  
- **出圖仍暫緩。**  
- Pack3 v2 書面回修仍可並行；本包不擋。
