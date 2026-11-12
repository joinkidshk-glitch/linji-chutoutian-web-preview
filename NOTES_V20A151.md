# NOTES_V20A151 — 關海媚名禁令退役（v20a151）

基底：main `e08a070`（v148；v149／v150 未落地）。工作分支 `v20a151`（工作副本 `~/workspace/linji-work151`）。
用戶原話：「以後佢個名可以直接出現喺玩家面，唔使再用『當紅花旦／台柱』代替。」
狀態：實作＋測試＋實駕完成。**已上線（main `86e391d`，rebase 上 `0c7ebbb` 後 push；線上 5,235,582 bytes、sha256 `faa40207ba06…` 已核實，同 repo 一致）。**
**落地更新（統籌，見 §10）：main 先行落地 v156（`9c850f9`），v151 合併嗰陣 rebase 概念上跟 `9c850f9`；新測試行號 resync +15 後 31/31 PASS，反證改對 `9c850f9`（19 FAIL）。**

## 1. 改動清單（前後對照）

### A. 禁令執行點（index.html，原位改，行數不變：58904 行，diff 11+/11-）
| 行 | 改前 | 改後 |
|---|---|---|
| L25729 | `if(/Ho\s*哥\|關海媚\|陳淑芬\|施南生/.test(face))` | `if(/Ho\s*哥\|陳淑芬\|施南生/.test(face))` |
| L26066 | `["關海媚","陳淑芬","施南生","Ho哥"]` | `["陳淑芬","施南生","Ho哥"]` |
| L26069 | `/* v1.1 note 不再寫角色名；雙女主／關海媚禁令改讀 devAppendix（v1 正文 note 仍算過） */` | `/* v1.1 note 不再寫角色名；雙女主改讀 devAppendix（v1 正文 note 仍算過） */` |
| L26071 | `if(note.indexOf("關海媚")<0 && dev.guanHaimeiUpgradeForbidden!==true) bad("kwan_note");` | `/* v151 退役：關海媚名禁令已撤，kwan_note check 不再執行。 */` |
| L26114 | `["關海媚","陳淑芬","施南生","Ho哥","Ho 哥","nextHint"]` | `["陳淑芬","施南生","Ho哥","Ho 哥","nextHint"]` |
| L26334 | `["關海媚","陳淑芬","施南生","Ho哥","Ho 哥"]` | `["陳淑芬","施南生","Ho哥","Ho 哥"]` |
| `dual_note`（L26070）唔郁；陳淑芬／施南生／Ho哥／Ho 哥禁令全部留返。 |

### B. TEXTFIX55（index.html）
- L31031 `TEXTFIX55_PHRASES`：成對 `["關海媚", "當紅花旦"], ` 拎走，其餘 14 對唔郁。
- L31022 `TEXTFIX55_EXACT`：**映射保留，只改 value**——value 入面「嗰位當紅花旦亦提過佢，頭條係雙刃」→「關海媚提醒頭條係雙刃」。
  其餘 live 修正原封不動（1991年冬→1990年冬、「虛構娛樂周刊」→「娛樂週刊」等）。
  判斷理由：成條映射刪走會令錯年份／舊寫法漏返出玩家面；只改 value 係最小改動。
  語法驗證：抽兩個 inline `<script>` 段出嚟 `node --check`，全部 SYNTAX_OK（主 script 4,304,663 字元）。

### C. UI 顯示名（禁令嘅實際替代位）
- L27308：`kwan_hoimei: { artId:"char_kwan", portraitsKey:null, display:"當紅花旦" }` → `display:"關海媚"`。
  事前 grep：全檔冇 code／test 用 `display==="當紅花旦"` 認佢（display 只經 `spDisplayName()` 回傳做對白名牌）；
  唯一相依測試係 `tests/test_cleanup100_static.py` L95–96（見 §4）。
- L31073 relMap：`["rel_mei","嗰位當紅花旦"]` → `["rel_mei","關海媚"]`。
  事前 grep：relMap 只喺 `textfix55Note()` 內用（L31073–31074），無其他 dependents／tests。
- **追加（同類替代位，任務 C 原文未列明，見判斷）**：L31030 `TEXTFIX55_NOTE_EXACT` 兩句 outcome note
  （「你公開承認，名氣升咗；采兒同嗰位當紅花旦嗰邊都近咗啲…」／「…但采兒同嗰位當紅花旦嗰邊，都冷淡咗。」）
  → 「采兒同關海媚嗰邊…」。判斷：呢兩句係 UI 呈現嘅 outcome note，同 relMap 一樣係用稱號代替佢個名嘅顯示位；
  只改 relMap 會令通用 note 出真名、呢兩句專屬 note 繼續出稱號，前後唔一致。故事散文（L29850／L29938）唔郁。
- `台柱` grep：全檔 2 處（L50505「台柱嗰味嘢」、L51480「成行都嗌你做台柱喇」）——**全部指阿偉**，唔係佢嘅代稱，唔郁。

### D. content JSON flag（`dev.guanHaimeiUpgradeForbidden` 淨係為佢而設）
- 刪走 4 行（成行刪，語法安全，逐檔 `node -e JSON.parse` 驗證有效）：
  - `content/MOCK_STORY_DENG_LINE_MEET_SOFT_v1.1.json:187`
  - `content/MOCK_STORY_DENG_LINE_MEET_SOFT_v1.json:156`
  - `content/MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json:42` 及 `:633`（刪 42 行後第二處行號變 632，先後次序已處理）
- `mvpDualHeroineProtected` 全部留返。刪完全 repo `guanHaimeiUpgradeForbidden`／`guanHaimei` 出現次數＝0。

### 絕對唔郁（已核實）
- L27275 speaker registry `"關海媚":"kwan_hoimei"` 留返。
- L29850／L29938 故事散文稱號句、L51637「當紅花旦唔入名冊（硬規則）」（12 星名冊規則）留返。
- `content/cast_main.json`、感情線規則（「關海媚無 commit／無 HE」係感情線設計規則，唔係名禁令）留返。
- SAVE key `starVolunteer_map_v19w`、softRev `s107`、產品 `?v=`（`v20a10`）不變。

## 2. content 掃描結果
- `DS_PLAYER_ZH_FILTER_TABLE_v1.json`：再核實一次，入面**冇關海媚**（同偵察一致）。
- `關海媚` 喺 content/ 出現嘅檔：3 個 DENG mock（dev note／flag，已處理 flag；note 入面嘅名係 DEV 備註，唔係玩家面禁令執行點）、
  `content/cast_main.json:300`（角色名冊，留返）、`content/story_detail_c1_to_c17.json`（C13 synopsis／cast／beats／openConditionsNote，係玩家面內容來源，TEXTFIX 層已改）、
  `content/story_detail_romance_lan_xu.json:953`（「關海媚無 HE」感情線規則，唔郁）。
- PLAN_*.md 歷史設計文件：有提及（例如「關海媚唔升格」「關海媚升格仍禁」），係**感情線升格規則**，唔係名禁令，按任務指示唔郁，備註於此。

## 3. 新測試
- `tests/test_kwan151_static.py`（31 項）：A1–A9／B1–B5／C1–C5／D1–D2×3 檔／E1–E5。工作版 **31/31 PASS**。
- `tests/test_kwan151_textfix.js`（11 項，仿 `test_terms57_logic.js` 抽 TEXTFIX block 做法）：工作版 **11/11 PASS**。
- 反證（對 pristine main `e08a070` index＋3 個 JSON）：static **18 項乾淨 FAIL**（唔 crash）、JS **9 項乾淨 FAIL**；「唔郁」類守門項喺 pristine 照樣 PASS。
- `tests/test_terms57_logic.js` 繼續 **ALL PASS**。

## 4. 相依舊測試更新（全部係將已退役規則改寫做新規則，唔係放寬守門）
| 測試 | 原因 | 改法 |
|---|---|---|
| `test_cleanup100_static.py` L8／L95–96 | 直接斷言 display＝「當紅花旦」＋唔准 `display:"關海媚"`（即係禁令本身） | 改做斷言 display＝「關海媚」＋唔准 `display:"當紅花旦"`，註解加（v151 解禁） |
| `test_text55_logic.js` L21–23 KHM | 斷言 walk 將 speaker／lines 洗做「當紅花旦」 | 改做斷言直出「關海媚」 |
| `test_text55_static.py` L43／L51 | 斷言 cleaner pattern `"關海媚", "當紅花旦"` 在位 | 改做斷言該配對已拎走；「KHM outside tables only in QA/registry contexts」嗰項唔使改（已 PASS：L27308 display 上下文有 `display`／`kwan_hoimei`，L26071 退役註解有「禁令」關鍵字） |
| `test_aud91fix122_static.py`／`test_aud91fix124_static.py`（`git status` 守門） | D 改咗 3 個 content JSON | 加 `_v151_flag_only()`：准許且僅准許 diff 淨係刪 `guanHaimeiUpgradeForbidden` 一行（PUSH 檔有兩處，共 1–2 行刪走、零新增）；其餘 content JSON 改動照舊 FAIL |
| `test_gigreq110_static.py`（`git diff HEAD -- content/` 守門） | 同上 | 同一個 `_v151_flag_only()` 過濾 |
| `test_wf5_87_static.py`（逐檔 sha 對照 `~/workspace/linji-work86`） | D 改咗其中 2 檔 | 2 檔 DENG 改做精確對照：BASE 版刪走 flag 行之後要同現版逐字相同；其餘 6 檔照舊 sha 對照 |

## 5. 全套測試 A/B（`qa131/run_suite.sh`）
- Pristine baseline：**211 PASS／12 FAIL**（223 檔；12 FAIL＝flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38，pre-existing）。
- 工作版（初版，未修 6 個回歸）：207 PASS／18 FAIL——6 個新 FAIL 全部係 §4 嘅相依舊測試。
- 工作版（修好之後）：**213 PASS／12 FAIL**（225 檔；＋2 係兩個新測試；12 FAIL 同 pristine 逐檔相同）。**零回歸。**

## 6. Node 層 TEXTFIX 驗證（`tests/test_kwan151_textfix.js`）
- Source synopsis「1991年冬，虛構娛樂周刊已寫好緋聞草稿。周采兒要阿偉表態；關海媚提醒頭條是雙刃。承認、否認或模糊帶過，每條路都改寫形象與關係。」
  經 `textfix55Str(..., TEXTFIX55_OPTS_STORY)` 之後＝「1990年冬，娛樂週刊已經寫好緋聞草稿。周采兒要阿偉表態；**關海媚提醒頭條係雙刃**。承認、否認定係含糊帶過，每條路都會改寫形象同關係。」
  （出「關海媚」、唔出「當紅花旦」；1990年冬修正保留。）
- `PHRASES` 唔再有 `關海媚` 配對；bare name 直出；其餘 phrase（星河電視城→星河電視台）照常。
- `textfix55Note` 兩句 rel_mei outcome note 而家出「關海媚」、唔出「當紅花旦」。

## 7. 實駕（本地鏡像＋Playwright；腳本 `/tmp/drive151.py`，log `qa131/drive151.json`，截圖 `qa131/shots151/`）
- 鏡像 port 8962，390×844，`?softPreview=1`；新遊戲成功（day 0）。
- **P1 DengLine.selfCheck() live（工作版）**：`{ok:false, fails:["chrome_fields","soft_chrome","push_era"]}`——
  冇 `kwan_note`、冇 `banned:關海媚`；去註解後嘅可執行 source 零 `kwan_note`／零 `關海媚`（`execHasKwanNote:false, execHasKwanBan:false`），退役註解在位。
  餘下 3 個 fail 係 pre-existing（見 P3 對照）。
- **P3 混合對照（pristine index.html `e08a070` ＋ 工作版 content/，port 8963）**：selfCheck fails
  `["kwan_note","chrome_fields","soft_chrome","push_era"]`——同 P1 差別**淨係多咗 `kwan_note`**。
  證明：JSON 刪 flag 同 check 退役係綁埋一齊、缺一不可（淨刪 flag 而唔退役個 check，selfCheck 會 fail）。
- **P2a live registry C13**：`StoryOC.findNodeRaw('C13')` → title「賀歲片」（紅棉影業片場）——見 §8 重要發現。
- **P2b pack C13 node-object 直播**：`StoryPlay.start(packC13node, {force:true})` 成功；14 句對白，
  speakers＝周采兒×4／阿偉×4／**關海媚×4（steps 4、5、10、11）**；全程 14 句**零「當紅花旦」**。
  截圖 `qa131/shots151/c13pack_kwan_speaker.png`：舞台右邊關海媚（風褸、舉鋼筆），對話框名牌「**關海媚**」，
  台詞「我提醒你，頭條這種東西是雙刃刀，用得好可以幫你上位，用不好會反過來傷你。」
  （抉擇屏今次未出現：14 句行完 plate 即 inactive，choices 係 []——pack 節點嘅 choices 掛法同 live 節點唔同，唔影響名牌驗證。）
- **0 pageerror、0 HTTP404。**

## 8. 重要發現（等統籌／用戶決定，唔喺 v151 範圍）
**Pack C13（緋聞公關真假）喺 live registry 入面俾 inline 主幹遮住咗，現時行唔到。**
`applyStorySpineOverrides48()`（index.html L24098，`refreshCopyPacksFromDisk` 內 L31618 呼叫）按 id 將
`STORY_WIRE.main.nodes` 入面嘅 pack 節點成個換做 inline `STORY_SPINE_NODES_1990` 節點；C13 喺 1990 主幹入面係「賀歲片」
（紅棉影業片場，L21488；`StoryOC.findNode` 經 `iterNodes()` 只讀 `STORY_WIRE.main.nodes`，即係換完之後嘅版本）。
後果：
- TEXTFIX55_EXACT 嗰條 C13 synopsis 映射同 TEXTFIX55_NOTE_EXACT 兩句 rel_mei note，喺現行 live build 入面**冇渲染面**
  （佢哋所屬嘅 pack 節點載入後被換走；inline 主幹入面零「關海媚」beats／notes）。
- v151 拆走嘅係執行層禁令（以後內容可以用佢個名）；但要玩家真係喺遊戲入面見到佢個名，
  要等內容層有返用佢個名嘅 live 節點——例如進行中嘅 v157 主線重整／v158 支線實裝（海媚 meet 掛 N10 台慶＋1991 冬緋聞 beat）
  或者另開一票處理 pack C13 被遮住嘅問題。
- 實駕 P2b 用 raw pack node object 直播，驗到嘅係 dialogue renderer 本身出唔出到「關海媚」名牌（出到）；
  load-time 清洗層出唔出到真名，另由 node 層測試（§6）驗證。兩者加埋先係完整鏈，唔好單憑 P2b 當成「live C13 已出真名」。

## 9. 檔案清單（分支 `v20a151`，未 push）
- 改：`index.html`（11+/11-，行數不變）、3 個 content DENG JSON（各刪 flag 行）、7 個舊測試（§4）。
- 新：`tests/test_kwan151_static.py`、`tests/test_kwan151_textfix.js`、本 NOTES、`qa131/drive151.json`、`qa131/shots151/`（4 張截圖）。
- 實駕腳本留喺 `/tmp/drive151.py`（未入 repo）。

## 10. 落地 resync（統籌；合併嗰陣 main 已經郁咗）
- 合併嗰陣 main HEAD 係 `9c850f9`（v20a156：v145 review B1+B3），唔係 `e08a070`。`e08a070..9c850f9` 得一個 commit（v156 直接接喺 v148 後面；v149／v150 未落地）。`git log -S "關海媚"` 證實 v156 冇掂過任何 v151 位置（禁令行、DENG mock、6 個舊測試），squash merge 零衝突。
- v156 喺 index.html L733 插入 15 行（其餘插入喺 L32074 之後），所以全部 v151 錨點行號 **+15**（25729→25744、26066→26081、26069→26084、26070→26085、26071→26086、26114→26129、26334→26349、27275→27290、27308→27323、31022→31037、31030→31045、31031→31046、31073→31088；總行數 58904→58945）。JS 測試係 marker-based，唔受影響；其餘 6 個舊測試冇行號錨點，唔使郁。
- `tests/test_kwan151_static.py` 已 resync +15（連 assertion 名同註解）：合併後樹上 **31/31 PASS**；反證改對 `9c850f9`（pristine index＋3 個 JSON 抽出嚟跑）→ **19 項乾淨 FAIL**，零 crash（12 項「唔郁」守門喺 pristine 照樣 PASS）。
- 合併後樹上覆驗：`test_kwan151_textfix.js`／`test_terms57_logic.js`／`test_text55_logic.js` 全部 ALL PASS；cleanup100／text55_static／aud91fix122／aud91fix124／gigreq110／wf5_87／handbook156（v156 自身測試）全部 PASS。
- 全套數字（§5）係工人喺 `e08a070` 基底跑出嚟嘅；合併後因行號漂移只係 resync 咗新測試，index.html diff 內容不變，唔重跑全套（另註：統籌獨立重跑全套嗰陣發現 `run_suite.sh` 本身有波動——同一 repo 連續跑出 211/12、137/86、200/23 三個唔同數，失敗項每次唔同、全部係 .py；直接逐個跑嗰啲測試 5–8 次全部 PASS，flash51 等 12 項先係每次都出現嘅 pre-existing FAIL；結論係 suite runner 喺呢部機有波動，唔係 v151 回歸；v151 相關測試已逐個直接覆驗晒）。

## 11. 落地紀錄（統籌）
- 落地嗰陣 GitHub main 已先行到 `0c7ebbb`（v156 NOTES），本地 main `f8a254e` 分叉（ahead 2、behind 1）。rebase：`git rebase --onto origin/main 4901732 main`——只 replay v151 自己嗰個 commit，本地重複嘅 `4901732`（v156 NOTES 補錄，同 `0c7ebbb` 內容只差 NOTES 一行）drop 咗；rebase 零衝突。
- Rebase 後新 commit `86e391d`，`git diff f8a254e 86e391d` 得 `NOTES_V20A156.md` 一行（GitHub 版嗰行），v151 內容零改動；合併後樹上覆驗（新測試 31/31、JS 11/11、terms57／text55_logic／cleanup100／text55_static／aud91fix122／124／gigreq110／wf5_87／handbook156 全部 PASS）。
- Push：`0c7ebbb..86e391d main -> main`（經已修好嘅 `~/workspace/gh_tunnel.py` 隧道直接推；18080 嗰條已死，唔使再用 `/tmp/gh_tunnel.py`）。
- 線上核實：`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/` HTTP 200、**5,235,582 bytes、sha256 `faa40207ba06…`**，同 repo `index.html` 完全一致。
