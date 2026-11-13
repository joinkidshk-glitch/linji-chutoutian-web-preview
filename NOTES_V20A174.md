# NOTES_V20A174 — 修 v170 review A1＋B1＋B2＋C1＋C2

工作副本 `~/workspace/linji-work174/`，分支 `v20a174`，基底 main `e8c3a73`（v170，遊戲 `59fdf54`）。
用戶 2026-11-13 13:00 拍板修晒五項。**本票唔落地**（落地由統籌做）。
報告來源：`~/workspace/linji-design-review-v170/REVIEW.md`（175 行）＋`shots/` 42 張＋`probe/` 3 張。

## §0 總覽

| 項 | 修法 | 驗收結果 |
|---|---|---|
| A1 | 裱框收窄到海報直屬 img（`>`）＋獎盃加金底 chip | glamour／reveal 1x 睇得清（計算樣式 bg `rgb(242,193,78)`、22px，截圖 zoom 核實） |
| B1 | 舞台放大：canvas 424×240→424×360（垂直拉伸 1.5×），人仔 ×1.5 | 932 open 上黑帶 295→147px（−50%），canvas 顯示高 233→346px（＋49%），腳底＝舞台頂 290 顯示差 0.0 |
| B2 | 卡列預留高度＋stagger 200＋i*380→60＋i*180 | names frame 跳位 83px→0，第 4 張齊 1382→498–789ms，全淡入 1897→797–984ms |
| C1 | gallery 中央 slot 左移 36（202→166） | 講台重疊 draw-rect 29→4px（像素層面 0px），人物唔浮空、講台完整 |
| C2 | glamour-hide 改 `display:none`，frame 收短 | glamour frame 640→372（−268），canvas 底到 frame 底 26px（舊死位 210px＋框下 244px 黑帶嗰段取消） |

改動：`index.html` 39 行（＋39／−39，**淨行數 0**，kwan151 釘行唔使 resync）＋新測試 1 檔＋5 檔舊測試 resync（新幾何）。
全套：pristine `231／12` → 工作版 **`232／12`**（＋1 係新測試，12 項穩定 FAIL 同一批，零回歸）。
實駕：won_932／won_700／gallery_932／nominated_932 **4/4 PASS、0 pageerror**。

## §1 A1——獎盃圖標喺深色底失效（A 級）

**根因（同 review 一致，兩層）**：① `.awd63-glamour-panel img` 將海報裱框（4px 金邊＋`#2b2118` 底）套落 panel 內所有 img，包括 `.cap` 內 22px 獎盃——border 食咗外框，內裡 14px 深啡獎盃喺深底隱形，淨返金色空心框。② 就算冇金邊，深啡獎盃喺深色底本身近乎隱形（reveal 字幕 1x 係一粒深色點）。

**修法（揀咗兩招並行）**：
1. 裱框規則收窄到直屬海報 img：`.awd63-glamour-panel img` → `.awd63-glamour-panel>img`（海報係 panel 直屬子元素，`.cap img` 喺 `.cap` div 入面，唔再中招）。
2. 獎盃加金底 chip：`.awd63-glamour .cap img.ic112, .awd62-caption img.ic112 { background:#f2c14e; border-radius:4px; padding:2px; width:22px; height:22px; box-sizing:border-box }`——glamour cap＋reveal 字幕兩處一齊受惠，深啡線稿喺金底上面 1x 睇得清。

**唔揀嘅路**：淺色版／金色版獎盃圖——要新資產＋改 `iconHtml112` resolver，會掂成套 26 隻圖標一致性；金底 chip 零新資產、只影響典禮兩處（selector 限定 glamour cap＋`.awd62-caption`，其他地方嘅獎盃唔變）。

**驗證**：實駕計算樣式 glamour cap img `bg=rgb(242,193,78)、w=h=22px、naturalWidth=256、complete=true`；reveal 字幕獎盃同款金底。截圖 zoom（`qa174/` 另存，見 §7）：glamour「🏆 得獎」獎盃形狀清晰，reveal「🏆 得獎！」同款。

## §2 B1——F1 上下空帶，舞台做大（B 級）

**用戶方向**：舞台做大一點。實作嗰陣試過三個方案：

| 方案 | 做法 | 結果 | 決定 |
|---|---|---|---|
| ① cover-crop 424×360（1.5×） | 底圖 cover 填滿高 canvas，左右裁走 | **唔得**：可見源圖闊只得 283px（x71–353），兩盞吊燈（x26–83／340–397）成個裁走，幕布邊＋牆燈一併冇埋；v170 驗證過嘅構圖大改 | 棄 |
| ② cover-crop 細比例（~1.14×） | 保住吊燈（可見闊 371px） | 舞台顯示高只＋14%（233→266），黑帶收窄唔明顯 | 棄 |
| ③ **垂直拉伸 424×360（1.5×）** | `drawImage(bgImg,0,0,424,360)`，x 唔郁 | **得**：構圖完整保留（吊燈／幕布邊／講台／平台全部在位）；`imageSmoothingEnabled=false`，像素邊保持硬淨，拉伸後實駕截圖目測無明顯變形（平台橢圓變深、講台變高，屬合理舞台比例） | **採用** |

**③ 嘅幾何（全部 y ×1.5，x 唔郁）**：canvas attr `424×360`；`FLOOR 193→290`（源圖頂線 193×1.5＝289.5，FLOOR＝291−1＝290）；人仔 fellow 48→72／玩家 50→75／燕尾服 64→96；slotCx 間距 72→80（人仔闊 63px，罅 17px；won 82／162／242／322、gallery 122／166／282）；行前 y＋7→＋10（新腳 300）；光池 66→99；獎盃 glyph 21×12→31×18（−64→−96／−26→−39）；names／reveal 閃粉 y 帶 ×1.5（150–230→225–345／205–231→307–346）；彩紙底界 244→364；後備舞台 H-47→H-70（平台頂 290、正面伸到 H-33＝327、金線 H-76＝284）；glamour overlay aspect 424/240→424/360；接觸影 fy−3／高 4→fy−4／高 6。

**v170 核心重驗（腳底＝舞台頂，唔可以整壞）**：實駕 4 case 腳底 median 全部 290（enter／names／suspense／pan／comfort／glamour），reveal 行前 max 300.0–300.2；顯示值 won_932 腳底 423.0＝舞台頂 423.0（差 0.0）、won_700 307.0＝307.0。Slot x 逐值吻合（won 82.5／162／242.5／322.5、gallery 122.5／166.5／282.5）。

**黑帶數字（932，實駕 frame 實測）**：

| Beat | 舊（review） | 新 | 變化 |
|---|---|---|---|
| open 上／下黑帶 | 295／295 | **147／147** | −50% |
| enter | 304 | 156 | −49% |
| names | 295 | 147 | −50% |
| reveal | 203 | 146 | −28% |
| walkup／glamour | 244 | 188／280* | 見 C2 |

\* glamour 帶 280 係因為 frame 收短咗（卡列＋字幕框都隱藏，frame 得 372 高）；舞台本身（canvas 346px）佔比照舊提升咗。700：open 帶 179／188→**31**，reveal 帶 →30。

**v149 關係**：開工嗰陣 v149 未落地（分支 `v20a149`，rebase 上 main `29d4821`，未合併），本票照 v170 基底做，冇掂 v149 嘅檔。**前向衝突，統籌落地嗰陣留意**：v149 B1 將 canvas backing 改做 636×360，但佢嘅 `draw()` 仍然用 `W=424、H=240` 座標；v174 之後 draw 座標係 `424×360`——如果 v149 原樣落地，`drawImage(bgImg,0,0,424,360)` 喺 636×360 canvas 上只會畫左邊 424px，右邊 212px 留空。v149 落地嗰陣要將 backing 改做 636×540（424×360 嘅 1.5×）或者重新對齊 draw 座標，落地後要重驗全部 beats 企位＋黑帶。**已解決，見 §9**：v149 已上線（main `a500536`），本票 rebase 上去，合併後 backing 636×540、邏輯 424×360、setTransform 1.5 均勻，全部重驗 PASS。

## §3 B2——Names beat 開場 frame 跳位＋卡列逐張淡入（B 級）

**修法（review 建議①＋②並行）**：
1. 卡列預留高度：`.awd63-cards` 由 `display:none` 改常駐 `display:flex`＋`visibility:hidden`，`.on` 先 `visibility:visible`。卡列容器由 stage 建立嗰刻已經佔位（174px），names beat 開場 frame 高唔跳。
2. Stagger 縮短：`syncCards` 由 `elapsed > 200 + i*380` 改 `elapsed > 60 + i*180`——第 4 張 600ms 出齊（舊 1382ms），全淡入約 900ms（舊 1897ms）。

**代價（寫明，唔收埋）**：open／enter beats 嘅 frame 入面，canvas 同字幕框之間會有一段 174px 預留空白（同 stage 底色 `#14101f` 一樣，視覺上係一段暗位）。呢個係建議①本身嘅 trade-off：零跳動嘅代價就係開場預留位。另一個做法（`max-height` 平滑展開，唔預留）今次冇做——要改容器展開機制＋重驗，留返以後再議。

**驗證（100ms 採樣，`drive174.py` names 探針）**：

| Case | frameTop 跳幅 | 第 1 張可見 | 4 張齊（.show） | 全淡入（opacity 1） | 舊數字 |
|---|---|---|---|---|---|
| won_932 | **0px** | 0ms（首採樣已見） | **681ms** | 797ms | 跳 83px／1382ms／1897ms |
| won_700 | **0px** | 584ms* | **789ms** | 984ms | 同上 |
| nominated_932 | **0px** | 0ms | **695ms** | 963ms | 同上 |
| gallery_932 | **0px** | —（冇卡列，N/A） | — | — | — |

\* won_700 首見 584ms 係採樣粒度（poll 間隔 ~250ms：100ms wait＋兩次 evaluate，phase 啱啱錯開），唔係容器遲開——容器喺 names beat 第一個 tick（125ms）內已經 `.on`。閾值定 700ms 係為咗呢個粒度，見 `drive174.py` 註解。
4 張齊由 beat 嘅 60%（1.38／2.35 秒）提前到約 21–33%（0.50–0.79／2.4–2.6 秒）。

## §4 C1——Gallery 中央提名人俾講台遮（C 級）

**調查（像素探針，`qa174/probe_c1.py`，舊幾何 424×240）**：reveal beat 讀 canvas 同底圖原圖同座標對比——overlap 區（x196–226、y184–192）57.3% 像素係人物色、講台-only 區 0.0%、幕布對照區 0.0%。**即係人物本身畫喺講台上面**，唔係講台遮住人物；review 嗰「21% 被遮」係幾何推算（講台頂 y183 vs 腳底 193），視覺上真正嘅問題係講台正面（y193–214）喺中央人腳底下繼續延伸，望落似企講台後面。修法方向因此唔係「移開遮擋」，而係「將人移離講台 x 範圍」。

**修法**：gallery 中央 slot 左移——`slotCx` 入面 `slots.length === 3 && i === 1` 嗰陣 `cx -= 36`（202→**166**）。揀 36 唔係 30 嘅原因：人仔放大後闊 63px（x134–197），移 30 仲剩 10px 貼講台邊，移 36 只剩 3px。兩側 slot 唔郁（122／282），中央唔再係正中——代價係三人企位輕微唔對稱（罅 44／116），但講台而家企喺中央同右邊兩人之間，望落合理。

**驗證（新幾何）**：實駕 draw 記錄中央人 x135–198，講台 x194–229，重疊 **4px**（上限；舊 29px）。像素覆核（`qa174/probe_c1b.py`，reveal 段內 800ms 讀 canvas——注意：段頭即讀會攞到 suspense 尾幀 0.52 暗層，見 §7）：中央人 x=166 垂直掃 FIG 由 y210 到 y288、y294 係 bg（腳底 290）；重疊 sliver x194–198／y274–290 同拉伸後底圖差異 **0.0**（即係像素層面零重疊——人仔右緣嗰幾欄喺呢啲行係透明）；講台-only 區 0.0（講台完整，唔俾人遮）。截圖 zoom 核實：中央人全身見到、腳掂平台、講台完整露出。

## §5 C2——Glamour 174px 隱藏卡列空帶（C 級，即 v168 C1）

**修法（三揀一，揀「frame 收短」）**：`.awd63-cards.glamour-hide` 由 `visibility:hidden` 改 `display:none`。接受現狀唔得（用戶已揀修）；「卡列位放非海報內容」要新內容／新接線，今次唔做。B2 嘅預留高度（常駐 flex）同 C2 唔打架：平時卡列留位，glamour 期間 `display:none` 蓋過佢，frame 收短；下一 beat（out）除返 `glamour-hide` 即恢復（`syncGlamour` 單一 choke point 唔變）。

**代價（寫明）**：glamour 入段／出段 frame 會 recentre（canvas 上移約 87px 再移返）——beat 邊界一次過嘅佈局移動，glamour 本身 overlay 大變（海報 panel 出現），接受得。

**驗證**：glamour frame 高 640→**372**（reveal 640 對比，−268＝174 卡列＋~64 字幕框＋邊距）；卡列計算 `display:none`；canvas 底到 frame 底 **26px**（舊：canvas 下 210px 死位＋框下 244px 黑帶）。海報＋燕尾服並置唔變（燕尾服 5 點探針全部 CANVAS、重疊 0，沿用 v166 驗法；實駕 `glamour_tux_drawn` true）。

## §6 測試

### 新測試 `tests/test_awards174_static.py`（41 項，全部 PASS）
- A1：裱框收窄到 `>img`、舊 `img` 規則消失、海報金框保留、金底 chip 規則在場（金底＋22px＋唔帶金邊）、glamour／reveal 仍然用獎盃圖標、圖標資產唔改。
- B1：canvas 424×360、FLOOR 290、人仔 72／75／96、slotCx 間距 80、glamour aspect 424/360、行前＋10、光池 99、glyph −96／−39、彩紙 364、後備 H-70、v149 636 唔入呢票、舊 240 消失。
- B2：卡列常駐 flex＋visibility 隱藏、`.on` 先可見、stagger 60＋i*180、舊 stagger 消失、beat 清單唔變。
- C1：gallery 中央 slot −36、只移中央、won 路唔受影響。
- C2：glamour-hide `display:none`、唔再 visibility 留位、syncGlamour choke point＋兩個 call 位。
- 守衛：cardsData／cardsHtml 唔掂、SAVE key、softRev、掌聲 M9 觸發點仲在。

### 反證（pristine worktree `~/workspace/linji-pristine174`，基底 `e8c3a73`）
- 新測試對 pristine：**28 FAIL**（全部新項斷言）／13 PASS（守衛＋空規則 vacuous pass），**唔 crash**。
- Resync 檔對 pristine：170：19 FAIL／26 PASS；168：5 FAIL／17 PASS；166：4 FAIL／28 PASS；160_m1：1 FAIL／23 PASS；64_chibi：3 FAIL／15 PASS。全部係斷言 FAIL，唔係 import／語法 crash。

### Resync 舊測試（新幾何，5 檔）
- `test_awards170_static.py`：FLOOR 290、後備 H-70／H-76／H-33／H-39、slotCx 間距 80＋gallery 中央 −36、行前＋10、光池 99、glyph −96／−39、人仔 72／75／96、canvas 424×360、glamour aspect 424/360。
- `test_awards168_static.py`：glamour-hide 改 `display:none`（C2）、`.awd63-cards.on` 跟 B2（`visibility:visible`）、panel img selector 改 `>img`、aspect 424/360；syncCards beat 清單唔變（stagger 改咗，見 174）。
- `test_awards166_static.py`：aspect 424/360、panel img selector 改 `>img`、燕尾服 cx 162／dispH 96（右緣 49.5%＜56%）。
- `test_awards160_m1_static.py`：canvas backing 424×360、draw 拉伸（唔再 1:1）；底圖資產本身仲係 424×240，PIL 內容檢查（舞台頂 y194、講台、無椅背）唔變。
- `test_awards64_chibi_static.py`：FLOOR 290、slotCx 間距 80＋gallery 中央 −36、人仔 72／75。
- 全部 resync 檔工作版 ALL PASS。`index.html` 淨行數 0（39＋／39−），kwan151／tang152 釘行唔使 resync（全套入面兩檔都 PASS）。

### 全套 `qa131/run_suite.sh`
- Pristine 基線：**PASS 231 FAIL 12**。
- 工作版：**PASS 232 FAIL 12**（＋1 係新測試 `test_awards174_static.py`）。
- 12 項 FAIL 兩邊同一批（`diff` 零差異）：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38——全部係已知穩定 FAIL，逐項對照證實，唔係回歸。Suite 數字本身會波動（v151 教訓），今次兩次跑數字穩定，判斷以 FAIL 集合為準。
- 結果檔：`qa174/suite_pristine174.txt`、`qa174/suite_work174.txt`。

### 實駕 `qa174/drive174.py`（本地鏡像＋Playwright，port 8995，`?softPreview=1`）
- **won_932／won_700／gallery_932／nominated_932：4/4 PASS，0 pageerror**（結果 `qa174/drive174.json`，截圖 `qa174/shots174/`）。
- 逐 beat 腳底：全部 median 290（FLOOR），reveal 行前 max 300.0–300.2；顯示差 0.0（won_932 423.0＝423.0、won_700 307.0＝307.0）。
- A1／B1／B2／C1／C2 各項實駕數字見 §1–§5。
- 實駕教訓（已處理）：① 逐 beat 歸屬有 poll 邊界 race——一格 reveal 行前燕尾服（腳 ~293）可以撥入 suspense 統計，suspense 改用 median＋min 驗（同 comfort 一樣），唔驗 max；② C1 canvas 像素擷取要喺 reveal 段內 800ms 先讀，段頭即讀會攞到 suspense 尾幀（0.52 暗層，亮度剩一半）；③ 頭兩輪 drive 嘅 B2 check 有 `0 or 999` 寫錯（0 俾當成缺失），已修正做 `is not None` 判斷；④ gallery 冇卡列，B2 卡片指標 N/A、reveal 帶比較要分開處理（字幕行數差）。

## §7 證據

- `qa174/drive174.py`（實駕腳本，100ms names 採樣＋A1／B1／C1／C2 探針）、`qa174/drive174.json`（4 case 全結果）、`qa174/shots174/`（逐 beat 截圖）。
- `qa174/probe_c1.py`（舊幾何 z-order 探針：人物畫喺講台上面；存檔 `qa174/c1_live.png` 係 424×240 舊幾何 canvas）＋`qa174/probe_c1b.py`（新幾何 reveal 段內像素覆核，存檔 `qa174/gallery_932_c1_canvas.png` 424×360）。
- `qa174/suite_pristine174.txt`、`qa174/suite_work174.txt`。
- 視覺核實（實駕截圖，1x）：glamour cap 金底獎盃＋「得獎」清晰；reveal 字幕金底獎盃＋「得獎！」清晰；open beat 舞台大咗（吊燈完整、講台置中、平台加深）；gallery 中央人企講台左邊、全身見到、講台完整；glamour frame 收短、燕尾服＋海報並置不變。

## §8 唔郁／殘留

- 提名卡人像（bust 裁切／Pixellab 像素／留返深色字卡）唔喺呢票——用戶未拍板路向；`cardsData`／`cardsHtml` 原封不動（新測試有守衛）。
- 掌聲 MP3 唔喺呢票（M9 觸發點仲在，新測試有守衛）。
- v149／v171／v172／v173 唔掂（見 §2 v149 前向衝突提醒）。
- B2 預留空白代價（§3）：open／enter beats frame 內 174px 預留暗位；平滑展開（`max-height` 過渡）留返以後。
- C2 trade-off（§5）：glamour 入段／出段 frame recentre 一次。
- C1 輕微唔對稱（§4）：gallery 三人罅 44／116。
- v149 落地後要重驗全部 beats 企位＋黑帶（§2）。

## §9 Rebase 紀錄

- 無 rebase（開工嗰陣基底 `e8c3a73` 係最新 main，`git log --oneline -1` 已核實；v149 未落地，冇衝突要解）。
- `git diff --stat`：`index.html` 39＋／39−；`tests/test_awards160_m1_static.py`、`test_awards166_static.py`、`test_awards168_static.py`、`test_awards170_static.py`、`test_awards64_chibi_static.py` resync；新檔 `tests/test_awards174_static.py`、`NOTES_V20A174.md`、`qa174/`。

### §9.1 第二次 rebase（統籌，落地前）
- 期間 **v153 落地**（main `a500536`→`0ecaeb3`，遊戲 `bbd318e`，線上 5,266,916 bytes sha `094072a4…`）。v153 掂 C17 路由／開場旁白／order71，唔掂典禮區，rebase 乾淨零衝突，新 HEAD `f7523ef`。
- 重驗（最終樹）：關鍵測試 174／170／168／166／160_m1／64_chibi 全 PASS＋qa149 36/36；全套 pristine `0ecaeb3` **232／12** → 工作版 **233／12**（＋1 係新測試 174），FAIL 集合 `diff` 零差異，零回歸（結果 `qa174/suite_pristine174s.txt`／`suite_work174s.txt`，pristine worktree `~/workspace/linji-pristine174s`）。
- 實駕 `qa174/drive174.py` 最終樹：**4/4 PASS、0 pageerror**。注意：第一次全跑 nominated_932 FAIL——`force_nominated` 8 次重骰都係 won（probe 層，唔係遊戲錯）；同一樹即刻重跑 nominated 單 case 即 PASS，再全跑一次 4/4 PASS。結論係探針 flake（8 次上限偏緊／推辭 click 時序），唔係 v174／v153 回歸，證據係同一樹重跑即過。

### §9.2 第三次 rebase（統籌，落地前）
- 期間 **v173 落地**（main `0ecaeb3`→`cd4291b`，遊戲 `4762572`，線上 5,267,258 bytes sha `a84b8d2b…`）。v173 掂地點板淡出／送禮掣 hint，唔掂典禮區，rebase 乾淨零衝突，新 HEAD `24af66f`。
- 重驗（最終樹）：關鍵測試 174／170／168／166／160_m1／64_chibi 全 PASS＋qa149 36/36；全套 pristine `cd4291b` **233／12** → 工作版 **234／12**（＋1 係新測試 174），FAIL 集合 `diff` 零差異，零回歸（結果 `qa174/suite_pristine174t.txt`／`suite_work174t.txt`，pristine worktree `~/workspace/linji-pristine174t`）。
- 實駕 `qa174/drive174.py` 最終樹：**4/4 PASS、0 pageerror**（一次過，nominated flake 今次冇出現）。

## §10 落地紀錄（統籌）
- Squash merge 分支 `v20a174`（HEAD `82908fe`，三輪 rebase：上 `a500536` v149、上 `0ecaeb3` v153、上 `cd4291b` v173，全部乾淨）→ main 遊戲 commit **`e2add29`**。
- Push main 三次先得（頭兩次 egress proxy reset 斷線，第三次成功；`cd4291b..e2add29`）。
- **線上核實：5,269,914 bytes、sha256 `3af45a51789cc015`**，同 repo `main:index.html` 逐字一致，live 係 v174。

### Rebase 上 main `a500536`（v149 已落地，遊戲 `461dc87`）

- 開工核實 main HEAD＝`a500536`（預期一致，落地期間冇再郁）。
- 第一次 `git rebase origin/main` 異常中斷（報 local changes 會被覆寫，但 `git status` 樹係乾淨；疑似環境問題）——`git rebase --abort` 返去乾淨 `8e9ca2d`，第二次重試即成功停喺預期衝突，唔係內容問題。
- 衝突 2 檔（其餘自動合併）：`index.html` 4 處＋`tests/test_awards160_m1_static.py` 1 處。
- 合併態（統籌定）：**backing 636×540、邏輯 424×360、setTransform 1.5 均勻**（424×1.5＝636、360×1.5＝540）。解法：
  1. CSS L801：v149 B3 全數保留（`.awd63-card.win::after` 🏆 角標＋`.awd63-csscard` flex-column＋icon／name 規則），glamour aspect 取 v174 嘅 **424/360**。
  2. Canvas 元素行：取 v149 嗰版（canvaswrap＋兩張 M5 GIF），height 360→**540**；v149 B1 註解更新做 636×540＋邏輯 424×360。
  3. `draw()`：`const W = 424, H = 360;`（v174）＋保留 v149 嘅 `ctx.setTransform(1.5, 0, 0, 1.5, 0, 0);`（註解更新做 636×540）。
  4. 彩紙落下：兩邊合併——條件取 v149（`reveal || comfort`），底界取 v174（`p.y > 364`）。
  5. 其餘 v149 內容逐項核實零丟失：M5 GIF 兩張、spawn 90 粒、syncConfetti149、reveal 不限 won、comfort 繼續落＋畫、跳過掣 top:8px／right:8px、B2 報紙＋結果卡、B3 comfort 紫 panel＋win 卡、B4 700 padding、贏線 0.875（`grep -c` 逐項在位）。
  6. 對 main 嘅 `index.html` diff 係 **43＋／43−**（原票 39＋／39−，多 4 行係兩處 v149 註解更新）；`−` 側逐行核對，刪走嘅全部係舊 240 幾何／舊 stagger／舊 CSS 或已被取代嘅 v149 行（636×360、244 底界），冇靜默丟失。
- v149 掂過 5 檔 resync 嘅邊個：只得 `160_m1`（backing 斷言）——已再對，合併做 636×540；170／168／166／64_chibi v149 冇掂，佢哋嘅斷言（aspect 424/360、`W = 424, H = 360`、FLOOR 290 等）合併後照舊成立，唔使郁。kwan151／tang152 等 v149 resync 嘅釘行檔：v174 淨行數 0，main 行號唔郁，全套入面全部 PASS。

### 測試 resync（合併態）

- **`qa149/test_awards149.js`（更正：任務話嘅 `tests/test_awards149_static.py` 並唔存在；v149 測試本身就係 `qa149/` 呢個 Node 檔，36 項）**：成檔逐項對位讀過，只有 2 項掂幾何——backing 斷言 636×360→**636×540**；setTransform 斷言名由「邏輯座標唔郁」改做邏輯 424×360，條件加埋 `const W = 424, H = 360`。其餘（B2／B3／B4／彩紙／跳過掣／紀律）唔郁。工作版 **36/36**；反證對 pristine `a500536`：**34/36，淨係 2 項幾何斷言 FAIL**（其餘全部 PASS，證明 resync 係手術式，唔係成檔放水）。
- `tests/test_awards174_static.py`（41 項，總數不變）：backing 斷言 424×360→**636×540**；舊守衛「v149 636 唔入呢票」已作廢，換做**合併態斷言**（backing 636×540＋setTransform 1.5＋邏輯 424×360 三合一）；header 註解更新（反證基底改 `a500536`）。
- `tests/test_awards160_m1_static.py`：backing 斷言→**636×540**（＋header 註解＋底圖尺寸註解澄清邏輯／backing）。
- 相關測試工作版全 PASS：174（41／41）＋149（36／36）＋170／168／166／160_m1／64_chibi 全部 ALL PASS。
- 反證（pristine worktree `~/workspace/linji-pristine174r`，`a500536`）：174：**29 FAIL**／12 PASS（全部新項斷言，守衛 PASS）；170：18 FAIL；168：5 FAIL；166：4 FAIL；160_m1：1 FAIL（淨係 backing 新斷言）；64_chibi：3 FAIL；149：2 FAIL（淨係 2 項幾何）。全部係斷言 FAIL，唔 crash。

### 全套 `qa131/run_suite.sh`（基線 `a500536`，唔係 `e8c3a73`）

- Pristine：**PASS 231 FAIL 12**（結果 `qa174/suite_pristine174r.txt`）。注意：第一次跑相對路徑 outfile 寫唔到（run_suite.sh 會 `cd` 去 pristine root，嗰度冇 `qa174/`），改絕對路徑重跑先存到檔；數字兩次一致 231／12。
- 工作版：**PASS 232 FAIL 12**（結果 `qa174/suite_work174r.txt`，＋1 係新測試 174）。
- FAIL 集合 `diff` 零差異（12 項同一批：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38），零回歸。

### 實駕重驗（rebased 樹，`qa174/drive174.py`，port 8995，`?softPreview=1`）

- **won_932／won_700／gallery_932／nominated_932：4/4 PASS、0 pageerror**（結果 `qa174/drive174.json`，截圖 `qa174/shots174/`，數字同 rebase 前一致，證明 636×540 backing 顯示幾何完全唔變——CSS `width:100%;height:auto`，636/540＝424/360 同比例）。
- 腳底 median 全部 **290**（FLOOR），reveal 行前 max 300.0–300.2；顯示差 0.0（won_932 423.0＝423.0、won_700 307.0＝307.0）；932 open 上黑帶 **147px**（唔係 295）；canvas 顯示高 346px；B2 frame 跳 0、第 4 張齊 655–772ms；A1 金底獎盃 bg `rgb(242,193,78)`、22px、nw 256 complete；C1 中央人重疊 **4px**（cx 166.5，x135–198）；C2 glamour frame 372 vs reveal 640，canvas 底到 frame 底 26px。
- M5 彩紙補驗（新探針 `qa174/probe_m5.py`，結果 `qa174/probe_m5.json`）：won＋nominated **2/2 PASS、0 pageerror**——兩張 GIF 全部 complete、naturalWidth 160；reveal／comfort／out（`?` 段）期間 `.on`＝2 張，其餘 beats 全部 0 張。
- 探針教訓：第一版漏設 `D.PORT`，`check_served` 預設 8991 連唔到 8995 伺服器——已補 `D.PORT／D168.PORT／W.PORT＝8995`。
