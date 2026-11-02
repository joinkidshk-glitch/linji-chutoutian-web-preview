# QA｜Romance Pack2 藍若曦／徐寶珊（＋鄧麗萍 stub）v1（文件／詞彙｜非 browser）

> **範圍：** `story_detail_romance_lan_xu.json`（**v2**）、`PLOT_DETAIL_ROMANCE_LAN_XU_v1.md`。  
> **基準：** 解鎖 `PLOT_DETAIL_UNLOCK_v1.md` §4；主計劃 `PLOT_MASTER_PLAN_v1.4-DS.md` §5–6／§11 鄧麗萍雙條件／關海媚無 HE；詞彙 `COPY_STYLE_HK_LEXICON.md`。  
> **風格對齊：** `QA_ROMANCE_VERA_HIU_CHOI_v1.md`；Pack1 steering（`flag_<line>_*`、阿偉非「我」、`C_*`）。  
> **本輪：** 只報告、**未改**任何 story content。  
> **時間：** 2026-11-02 23:01（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| 硬鎖（禁詞／星河／真人／政治／關海媚非第六攻略／出圖／藍·徐各 5 節／HE·BE＋commit／阿偉「我」beats＝0／電報非主導） | **PASS** |
| 解鎖 §4 弧（meet→push×2→crisis→ending）藍／徐齊；鄧 stub OK | **PASS** |
| C9／C14／C15／T6 掛鉤；徐 crisis 尊重／依賴／拒絕三支 | **PASS** |
| Pack1 steering 三項（旗標／阿偉／`C_*`） | **PASS**（本包已跟） |
| 愛情與事業結局並存文案 | **PASS**（藍／徐 HE·BE notes 均「可與事業結局並存」） |
| md ↔ JSON | **PASS**（title／when／flags／artId／conflict／choices 一致） |
| Soft：`flag_tang_open` 於偶遇寫入；`conflict` 欄 C15 vs T6；crisis 支數 vs 主線 C15／C9；cast 書面化 | **NIT**（非 hard FAIL） |

**出圖：** 仍暫緩（`rom_lan_*`／`rom_xu_*`／`rom_tang_meet_stub` 僅佔位；repo **0** 對應成品圖檔）。

**五線感情（Vera／曉晴／采兒／藍／徐；鄧全線另計）：** **文字可作 wiring 草案**——Pack1＋Pack2 五可攻略弧齊；鄧僅 stub，不擋五線 wiring。建議 wiring 前統一 `conflict`／`linksMain` 語意（見 §5）。

---

## 1. 解鎖 §4 對齊表

| 線 | 期望 | 成品 | 結果 |
|---|---|---|---|
| **藍若曦** meet | P2 預告／合唱接觸 | `R_lan_meet` **P2**｜1989 旺角唱片店傘下擋狗仔；合唱落在 `push1` | **PASS**（相位對；meet 偏狗仔初遇，合唱＝push1——soft 見 §3） |
| 藍 push | 假戲真做、擋狗仔（C9） | `push1` 台慶合唱綵排；`push2` 假戲／緋聞走廊｜`conflict=C9`｜`linksMain:[C9]` | **PASS** |
| 藍 crisis | C15 聯姻逼退 | `R_lan_crisis`｜1991春豪門側廳｜`conflict=C15`｜`linksMain:[C15]`｜助抗／成全退讓；寫 `flag_family_marriage` | **PASS** |
| 藍 ending | 抗聯姻 HE／成全 BE；`rel_lan`、`flag_family_marriage` | HE：`flag_lan_he`＋**`flag_lan_commit`**＋`rel_lan+3`；BE：`flag_lan_be`＋`rel_lan-2`；`parallelOk=false` | **PASS** |
| **徐寶珊** meet | P3 廣告／春茗 | `R_xu_meet` **P3**｜1990春 星河春茗 | **PASS** |
| 徐 push | 金援邀約 | `push1` 商場廣告金援口風；`push2` 私人飯局距離 | **PASS** |
| 徐 crisis | C14 尊重或包養 | `R_xu_crisis`｜`conflict=T6`｜`linksMain:[C14,T6]`｜**三支** respect／depend／refuse；雙寫 `flag_xu_*`＋`flag_bao_*` | **PASS** |
| 徐 ending | 平等合作 HE／依賴 BE；`rel_xu`、金援旗標 | HE：`flag_xu_he`＋**`flag_xu_commit`**；BE：`flag_xu_be`；crisis 已落 `flag_bao_*` | **PASS** |
| **鄧麗萍** | 雙條件 `flag_tang_open`＋`rel_tang`；stub OK | `R_tang_meet_stub`｜`stub:true`｜`openConditions` 列雙條件 | **PASS（stub）**；寫入時機 nit → §3 |

**節點數：** 11＝2×5（藍／徐）＋鄧 meet stub；`qa.node_count=11`／`romanceLines=[lan,xu,tang]` 自述正確。

---

## 2. 硬鎖掃描

| 項 | 結果 | 證據 |
|---|---|---|
| 禁詞 薄本／趕板／苛約／拖字訣 | **PASS** | body **0** |
| TVB／tvb／無綫／無線 | **PASS** | **0**；台名「星河電視台」 |
| 真人藝名 | **PASS** | 周星馳／劉德華等抽樣 **0** |
| 政治／抗爭再現 | **PASS** | 六四／民運／遊行／抗爭／政治 **0** |
| 關海媚作第六攻略／HE | **PASS** | 僅 `rule` 句「關海媚無 HE」；無 `flag_*_commit`／無結局節 |
| Pack1 人物誤入正文 | **PASS** | Vera／曉晴／采兒 **0** |
| 藍／徐缺 stage | **PASS** | 各 meet＋push＋push＋crisis＋ending |
| Ending 無 HE／BE／commit | **PASS** | 藍／徐 HE 皆雙寫 `flag_*_he`＋`flag_*_commit` |
| 阿偉第一人稱「我」beats | **PASS** | `pcSilent=true`；`qa.aw_first_person_lines=0`；synopsis 用「阿偉」；beats 內「我」皆 NPC 自述 |
| 電報主導 | **PASS** | 均長 **29.0**；≤12 字句 **0** |
| 出圖成品 | **PASS** | `rom_*` 成品檔 **0**；md「未出圖」 |
| `gigs_1988.json` | **PASS** | mtime **2026-11-02 16:51**（HK）；romance **22:59**——本輪未動 |
| 每 choice `effects.flags`＋`effects.stats`＋`rel_*` | **PASS** | 頂層 `flags`／`stats`＝None 屬 schema（與 Pack1 同：巢狀在 `effects`）；**MISSING=0** |
| Choice id `C_*` | **PASS** | 全包 **0** 非 `C_` |
| 旗標 `flag_*` 前綴 | **PASS** | 全寫入皆 `flag_`；無 Pack1 裸前綴混用 |
| 確定前平行 | **PASS** | meet→crisis `parallelOk=true`；ending=`false` |
| 徐 crisis ↔ C14 三支 | **PASS** | respect／depend／refuse；`flag_bao_respect|depend|refuse` 與主線 C14 **同名** |
| 無擅自批核 | **PASS** | 未改 MASTER／UNLOCK；僅 detail 包 |

---

## 3. Soft nits（非 hard FAIL）

1. **鄧 stub 寫入 `flag_tang_open`：** UNLOCK／§11＝雙條件閘（`flag_tang_open`＋`rel_tang` 門檻）；成品 `C_tang_meet_keep_contact` 在偶遇直接寫 `flag_tang_open`，同時 `openConditions` 又列同一旗作開線條件——易變成「偶遇＝開閘」而非「另途取得 open 後＋rel 再開」。  
   → **建議（劇本側）：** 偶遇只加 `rel_tang`／`flag_tang_met`；`flag_tang_open` 留給主線／任務閘；或文件註明 stub 暫用「聯絡＝open」待正式弧改寫。

2. **`conflict` 欄型別混用：** 藍 crisis／push2 用主線節點碼（`C15`／`C9`）；徐 crisis 用檔期碼（`T6`），C14 放在 `linksMain`。主線側 C14.`conflict=T6`、C15.`conflict=null`——romance 與主線不完全鏡像。  
   → **可接受若引擎視 `conflict`＝鬆散掛鉤**；wiring 前建議定：T 碼進 `conflict`、C 碼進 `linksMain`（或兩者皆列），避免雙讀。

3. **藍 push2 `conflict=C9`：** 與 Pack1 采兒 crisis「只寫 setting、conflict=null」不同；本包明示 C9——**OK if intentional**（報告備註）。

4. **主線支數 vs romance crisis：** C15 主線三支（助抗／成全／袖手）；romance crisis 兩支（助抗／成全退讓），無「袖手」。C9 主線三支（認／切／模糊）；romance push2 兩支（護／劃清）。解鎖感情表以 HE／BE 為主，**不擋**；若要事件↔感情一一對射，可後補。

5. **藍 meet vs「預告／合唱」字面：** meet＝唱片店擋狗仔；合唱＝`push1`。相位 P2 正確，字面略偏——soft。

6. **Cast 口語樣句 vs 本包書面：** `cast_main` 藍／徐／鄧 lines 偏粵口語；本包 beats 正確書面化且貼性格（藍外柔內剛／怕聯姻；徐資本壓迫開價；鄧公事對接）。非 FAIL；正式開鄧線時續守書面＋數據腔。

7. **`cast_main` 徐寶珊 `tier:阻力`：** 主計劃／UNLOCK 已列可攻略——屬 cast 檔舊標，非本包錯；可另開 cast 對齊（不擋 wiring）。

8. **雙寫旗標：** 徐 crisis 同時 `flag_xu_respect`＋`flag_bao_respect`（depend／refuse 同理）——與 C14 金援旗對齊且線內可讀；wiring 用 alias／其一為準即可。

---

## 4. md 摘要 vs JSON

`PLOT_DETAIL_ROMANCE_LAN_XU_v1.md` 與 JSON：節點 id／title／when／setting／artId／`conflict`／`linksMain`／HE·BE flags（含 commit）／徐三支／鄧 stub 與 `flag_tang_open` 註記 **一致**；標「未出圖」、steering 修訂說明正確。`version=2`。

---

## 5. Wiring 建議／blocker 一覽

| 優先 | 項 | 擋不擋五線 wiring／文字定稿 |
|---|---|---|
| A | 定 `conflict` vs `linksMain`（T vs C）讀法 | **不擋**；建議 wiring 前一頁約定 |
| A | 鄧 `flag_tang_open` 寫入時機 | **不擋**五線；擋鄧正式開線前應釐清 |
| B | C15／C9 支數與 romance 兩支對照表 | 不擋 |
| B | cast 徐 `tier` 改可攻略（另檔） | 不擋 |
| — | Hard FAIL | **無** |
| — | Pack1 steering 三項 | **本包已遵守**（可回頭 polish Pack1） |

**無必須先修才能做五線（不含鄧全弧）wiring 的 blocker。**

---

## 6. 結論給用戶／劇本 manager

- **Romance Pack2（藍若曦／徐寶珊＋鄧 stub）：PASS with nits**（硬鎖全過；10／10 藍徐節＋stub；C9／C14／C15／T6＋`flag_bao_*`＋雙 commit 齊；steering 三項達標）。  
- **五可攻略感情線文字：** Pack1＋Pack2 **夠齊，可作 wiring 草案**；鄧麗萍僅 stub，正式弧另開。  
- **出圖仍暫緩。**
