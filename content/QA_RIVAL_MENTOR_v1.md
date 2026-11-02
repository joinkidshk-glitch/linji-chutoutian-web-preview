# QA｜Pack3 對手／導師／友情／資本弧 v1（文件／詞彙｜非 browser）

> **範圍：** `story_detail_rival_mentor.json`（version 1）、`PLOT_DETAIL_RIVAL_MENTOR_v1.md`。  
> **基準：** 解鎖 `PLOT_DETAIL_UNLOCK_v1.md` §5；主計劃 `PLOT_MASTER_PLAN_v1.4-DS.md` §5–6；詞彙 `COPY_STYLE_HK_LEXICON.md`（全面書面語）。  
> **風格對齊：** `QA_ROMANCE_LAN_XU_v1.md`。  
> **本輪：** 只報告、**未改**任何 story content。  
> **時間：** 2026-11-02 23:12（Asia/Hong_Kong）

---

## Overall：**FAIL**（書面語硬鎖）／結構其餘多項 PASS

| 層 | 結果 |
|---|---|
| 硬鎖：禁詞 body／星河／真人／政治／非戀愛 HE·BE／pcSilent／C_*／8×5＝40／出圖暫緩／gigs_1988 | **PASS** |
| 硬鎖：**全面書面語**（含 NPC beats／synopsis／choice label） | **FAIL** |
| 解鎖 §5 八線＋預期連線（C／T／E／P／flag_anti_lei） | **PASS** |
| 高俊傑 ≠ 張克凡聲口（內容立意） | **PASS**（兩者皆口語腔，但資源壓 vs 嘴賤搶板可分） |
| md ↔ JSON 路線表／40 節標題 | **PASS**（速覽齊；md 未自稱書面） |
| Soft：`conflict` 混型、結局 `parallelOk`、旗標跨 kind 命名、雷勁 phase 序、synopsis「你」vs 感情線「阿偉」 | **NIT** |
| 自檢 `qa.pass=true` | **不可採信**（未掃書面；issues=[]） |

**出圖：** 仍暫緩（`arc_*` 僅佔位；repo **0** 對應成品圖檔）。

**可否併入 C1–C17＋romance wiring 草案：**  
- **結構／旗標／linksMain：** 可作 **id 級 wiring 草案**（40 節齊、結局非戀愛標籤、主線鉤齊）。  
- **正文 copy：** **不可**與 romance／主線書面包並鎖定稿——須先整包改寫為書面現代港語（對齊 Pack1／Pack2 beats：**口語標記線 ≈0%**）。  
→ **總評 FAIL，擋 copy-locked wiring；不擋「先掛 id／flag 草圖」。**

---

## 1. 解鎖 §5 對齊表

| 線 | arcKind | 期望連線 | 成品 | 結果 |
|---|---|---|---|---|
| **高俊傑** `A_ko_` | rival | C3,C10,C12,T2 | meet→C3；push2／crisis→C10+T2；ending→C12；結局 respect／cold／mentor 三支 | **PASS** |
| **張克凡** `A_hakfan_` | rival | P2–P4 資源場 | meet／crisis 掛 P2–P4；聲口世家／飯局／爸爸；非高俊傑嘴賤搶板 | **PASS** |
| **張子駿** `A_tsijun_` | mentor | C8,C11,C17,E03,T3 | push2 C8；crisis C11／T3；ending C17／E03；另 deepen C1／T1 | **PASS** |
| **方小龍** `A_fong_` | friend | P3 替身,E05 | crisis `P3替身危機`；ending E05；`flag_friend_saved` | **PASS** |
| **唐素雲** `A_tong_` | mentor | P2 去留,E09 | meet–push 掛 P2去留；crisis／ending E09 | **PASS** |
| **何生** `A_ho_` | mentor | C2,C4,E01 | meet C2；push1 C4；crisis／ending→E01 | **PASS** |
| **高文瀚** `A_gao_` | mentor | C8,C12,E02,T4 | meet C8；crisis C12／T4；ending E02 | **PASS** |
| **雷勁** `A_lei_` | capital | C7,`flag_anti_lei` | crisis C7＋拒約寫 `flag_anti_lei`；ending cold 再寫；ally→`flag_ally_danger` | **PASS** |

**節點數：** 40＝8×5；每線 `meet`＋`push`×2＋`crisis`＋`ending`；`qa.nodeCount=40` 自述正確。

---

## 2. 硬鎖掃描

| 項 | 結果 | 證據 |
|---|---|---|
| **書面語（含 NPC dialogue）** | **FAIL** | Romance Pack1／Pack2 beat 口語標記線 **0／37、0／128**；本包 beat 線 **179／194（≈92%）** 含 呢個／唔係／嚟／嘅／咗／喺／嗰／啲／冇／喂 等。例：`A_ko_meet`「喂，呢個位我早排咗，你仲唔識趣？」；對照藍若曦 meet「不好意思，可以借你的傘擋一擋嗎？」。synopsis **38／40**、choice label **≈65** 條同樣偏口語。另有㗎／喎／啫 **10** 處（詞彙禁過度助詞堆砌）。`locale` 雖標 `zh-Hant-written-HK`，**正文未達**。 |
| 禁詞 薄本／趕板／苛約／拖字訣 | **PASS** | **body 0**；僅 `rule` 字串提及薄本／趕板／苛約（允許） |
| TVB／tvb／無綫／無線 | **PASS** | **0**；「星河電視台」出現 **33** |
| 真人藝名 | **PASS** | 周星馳／劉德華等抽樣 **0** |
| 政治／抗爭再現 | **PASS** | 六四／民運／遊行／抗爭／政治 **0** |
| 戀愛 HE／BE 標籤 | **PASS** | 無 `flag_*_he`／`*_be`／commit 戀愛結局；結局為 rival_respect／cold_war／mentor_complete／friend_saved／ally_danger 系（`flag_gao_crisis_commit`＝事業 commit，非 HE） |
| pcSilent／阿偉非 speaker | **PASS** | 全 40 `pcSilent=true`；beats speaker 無阿偉；無玩家「我」對白 |
| Choice id `C_*` | **PASS** | 非 `C_`＝**0** |
| `effects.flags`＋`effects.stats` | **PASS** | MISSING＝**0** |
| 八線齊／每線四段 | **PASS** | 見 §1 |
| 高俊傑 ≠ 張克凡 | **PASS** | ko：插隊／讀名／搶鏡／「我唔係星二代」；hakfan：爸爸飯局／世家節奏／人脈搭路——立意可分（書面改寫後須保持） |
| 出圖成品 | **PASS（暫緩）** | `artId=arc_*` 40 佔位；成品檔 **0**；md「未出圖」 |
| `gigs_1988.json` | **PASS** | mtime **2026-11-02 16:51**（HK）；本包 **23:10**——未動 |
| 無擅自批核 MASTER／UNLOCK | **PASS** | 僅 detail 包 |

---

## 3. Soft nits（非本輪 hard FAIL 主因；書面修好後仍建議清）

1. **`conflict` 欄型別混用：** 有 `C3`／`C10／T2` 碼，亦有長句自由文（如 hakfan push、fong meet）、相位標（`P2資源場`）、甚至 `flag_anti_lei` 進 conflict。與 romance／主線「T→conflict、C→linksMain」建議不完全一致。  
   → wiring 前定讀法。

2. **`parallelOk`：** 僅 `A_fong_crisis=false`；**全部 ending＝true**（romance ending 為 false）。非攻略線或可平行收束——請劇本側明文；否則改 ending=`false`。

3. **旗標跨 kind 命名：** rival 線寫 `flag_ko_mentor_complete`／`flag_hakfan_mentor_complete`；mentor 何生 ending 用 `flag_ho_rival_respect`；friend 冷線複用全域 `flag_cold_war`／`flag_rival_respect`。可讀但易與「導師完成／對手尊重」語意撞車。  
   → 建議統一：`flag_<line>_ending_{respect|cold|…}`＋少數全域（`flag_anti_lei`／`flag_friend_saved`／`flag_ally_danger`）。

4. **雷勁 phase 序：** meet／push1／**crisis** 皆標 P1.5（1988秋冬），**push2** 標 P2（1989）——節點 id 序仍是 push2→crisis，但 phase／when 顯示 crisis 早於 push2。  
   → 對齊 C7 時間軸，改 phase 或調節序。

5. **synopsis 人稱：** 本包全用「你…」；romance 用「阿偉…」。pcSilent OK，但導語人稱宜全作統一。

6. **主線重疊：** ko／ho／tsijun／gao／lei 明顯 deepen C3／C2–C4／C8／C11–C12／C7——內容方向對；wiring 須標「並行加深」避免 UI 當兩場獨立大事件重複播。

7. **結局支數：** 八線 ending／crisis 皆 **3** 支——齊；fong／lei 有全域友善／資本旗——OK。

8. **Pack 自檢 `qa.pass=true`：** 未涵蓋書面語；QA 以本報告為準。

---

## 4. md 摘要 vs JSON

`PLOT_DETAIL_RIVAL_MENTOR_v1.md` 路線表八線、40 節速覽（id／title／when／setting／conflict／links／flags）、flag 一覽、未出圖／待 QA／pcSilent 與 JSON **一致**。md **未**聲明已書面化——與正文口語現況相符（非 md 謊報書面）。

---

## 5. Wiring 建議／blocker

| 優先 | 項 | 擋不擋 |
|---|---|---|
| **P0** | **整包 beats＋synopsis＋choice label 改寫書面**（對齊 lexicon＋romance 樣句；保留聲口差異） | **擋 copy-locked 定稿／與主線併開發布** |
| A | `conflict` vs `linksMain` 讀法約定 | 不擋 id 草圖 |
| A | ending `parallelOk`／旗標跨 kind 命名 | 不擋草圖 |
| B | 雷勁 phase 序；synopsis「你」vs「阿偉」；主線並行播表 | 不擋草圖 |
| — | 禁詞／星河／非戀愛結局／pcSilent／40 節結構 | **已過** |

**必須先修才能與 C1–C17＋romance 一併作 copy wiring 定稿的 blocker：** 書面語 FAIL。  
**可先做：** id／flag／links 掛接草圖（標明 copy TBD）。

---

## 6. 結論給用戶／劇本 manager

- **Pack3（對手／導師／友情／資本八線）：結構 PASS；書面語 FAIL → 總評 FAIL。**  
- 禁詞清、非戀愛結局、pcSilent、星河、連線 §5、高≠張立意、40／40 均達標；**對白／導語／選項大量粵口語**，與用戶鎖定及 Pack1／2 **書面**標準衝突。  
- **請 @臨記出頭天劇本manager 出 Pack3v2：只改文體為書面，不改弧結構／id／主線鉤**（除非顺手清 §3 nits）。  
- **出圖仍暫緩。**  
- **未改** story content。
