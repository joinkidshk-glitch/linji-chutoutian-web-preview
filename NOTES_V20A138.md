# NOTES v20a138 — 表情補圖第二批（先分生死檔）

- main commit：`f451930`（2026-11-12；base f0ae995＝v136 落地後）
- 落地方式：git 直接合併（`merge --squash v20a138`，唔開 PR）
- 線上核實：index.html 5,217,690 bytes，sha256 `29143a46a278d56709156e1cbc6a6948ede393ee6273d1849e9ed057d7b0ce7f`，同 repo 一致（HTTP 200）

## 一句話

v127 嘅教訓係唔好再按 corpus 句數直接排單——22 張入面 10 張實玩播唔到。
呢批先分生死檔：殘留 78 句逐組驗 speaker／覆寫／引擎／講者一致，
生檔先生成。37 張新圖入庫，全庫 170→207 張；
**實駕 35/35 生檔逐張見到，覆蓋 515／593（86.8%）→569／593（95.9%）**。

## 生死檔分類

### 生檔 35 張（已生成＋已實駕）

| 角 | 表情 | 實線句數 | 來源 |
|---|---|---|---|
| chai_zanhoi 齊讚海 | angry／shy／smile／think | 1／2／2／2 | ENC |
| cheung_hakfan 張克帆 | serious | 2 | PACK（C? end） |
| cheung_tsijun 張子駿 | sad／think | 1／1 | PACK |
| chung_choning 鍾楚凝 | angry | 1 | ENC pool T3[0] |
| crew_laolinji 老臨記 | serious | 2 | PACK C2＋LIVE |
| extra_ad_fen 芬姐 | sad／serious | 1／3 | WF4 intro＋farewell |
| ho_sang 何生 | surprise | 1 | CHOICE47 F4 |
| ko_chunkit 高俊傑 | shy／think | 1／1 | PACK |
| lin_hiu 連曉 | smile | 1 | PACK R_hiu_end |
| liu_bingxing 廖炳星 | sad／surprise／think | 2／2／1 | ENC＋LIVE |
| lok_gasing 駱家聲 | angry／shy／smile／surprise | 2／2／1／1 | ENC |
| lui_ging 雷敬 | serious | 1 | PACK R_lei_end |
| luk_baakyin 陸柏言 | angry／sad／smile | 1／2／3 | ENC＋PACK C12 |
| mak_zhendong 麥震東 | angry／smile | 1／1 | ENC |
| ngai_wingnaam 魏永南 | angry／serious／smile／surprise／think | 2／3／3／1／1 | ENC |
| so_jiyan 蘇芷茵 | surprise | 1 | ENC |
| vera | serious | 1 | PACK R_vera_meet |

### 死檔 7 組（唔生成，檔案唔存在）

cheung_tsijun_angry 1、ko_chunkit_sad 3、lin_hiu_angry 2、lin_hiu_think 3、
lui_ging_sad 1、tong_souwan_sad 1、vera_shy 1。
死因：CAST 從未載入／傾談靜態 bust（引擎唔行 dlg106）／GIFT 純文字／
resultBeats 引擎唔讀／pack 被主幹覆寫（C6–C17＋R_lan_*）。

### 判死 2 張（已生成入庫，但實線 0——檔案留低等修復票）

- **lin_hiu_serious**：唯一證據句係 pack R_hiu_meet「不過你要記住，有些助導比較挑剔…」；
  實玩播唔到——`StoryPlay.start(R_hiu_meet, {force:true})` → False
  （DualMeet 閘行喺 force check 之前，mock openGates 要求 C3）；
  過閘後 `meetNode()` 換成 mock 加厚版（6 beats），mock 3 句林曉晴對白分類
  neutral／neutral／sad，零 serious。修復方向（另一票）：mock R_hiu_meet 加一句 serious 台詞。
- **tsui_poushan_serious**：兩條證據句都係 pack 舊文本（書面語），分類 serious；
  但運行版係 index.html 重寫版（廣東話），pack 被主幹覆寫。
  全量核實：index.html 全部 17 句 live 徐寶珊句分類＝neutral 12／angry 1／think 1／
  shy 1／surprise 1／happy 1，**serious 0**。修復方向（另一票）：live R_xu_* 節點加一句 serious 台詞。
- 附帶：live 徐寶珊句有 angry／think／surprise／happy 各 1 句，庫入面冇對應檔
  （得 base／serious／shy），呢啲句現時跌返 base——下一批候選。

### 覆蓋率重計

批單 inventory 口徑 +66 句＝581／593（98.0%）係虛數，拆解：
54 句真 live 實線＋3 句死檔線（lin 1＋tsui 2）＋9 句 phantom
（extra_ad_fen sad 同一句旁白重複誤歸，盤點抽取器 bug——已修，
同 beat 守則：speaker: 同 lines:/text: 之間唔可以有另一個 speaker: 或 `}`）。
**真實覆蓋：515＋54＝569／593＝95.9%。**
覆蓋唔到嘅 24 條：9 phantom＋3 死檔線＋12 死組線（7 組死檔，另開票）。

### 唔入批嘅 mystery

`lin_hiu_surprise`：現行全檔任何來源都冇一條線會令 loader 探佢；
v119 檔連「連曉」都係 0 次。生成佢就係重犯 v127 死圖錯誤，唔入批。
三輪 drive＋四輪 spot-check 探測全程 0 次，符合預期。

## 實駕證據（逐張，全部真實玩到嗰句對白）

Drive `qa138/drive138.py`（390×844，softPreview，port 8971），
cum `qa138/drive138_cum.json`（35 張），截圖 `qa138/shots138/`（工作副本留檔，唔入 repo）。
全程 target404 {}、all404 []、lin_hiu_surprise 探測 0 次、pageerrors []。

- chai_zanhoi_angry｜e_chai_T0 step 0｜「又係你？企遠少少，唔好阻住我默書。」
- chai_zanhoi_shy｜e_chai_heart step 5｜「後生嗰班追到好貼，個個識打識跳，鏡頭又鍾意佢哋嗰種新鮮感。」
- chai_zanhoi_smile｜e_chai_beats step 5｜「台慶爭位，年年都爭，今年特別勁……」
- chai_zanhoi_think｜e_chai_beats step 10｜「留低嘅亦唔一定係忠心，可能係驚去到新台冇位企……」
- cheung_hakfan_serious｜s_hakfan_end step 1｜「我從小到大都是人家讓我先，你沒有讓過，所以我記住你。」
- cheung_tsijun_sad｜s_tsijun_crisis step 1｜「嗰個長鏡頭係成套戲個心嚟㗎，剪走咗，」
- cheung_tsijun_think｜s_tsijun_meet step 7｜「有戲拍，同拍到戲，係兩回事嚟㗎。企多陣，諗下」
- chung_choning_angry｜e_chung_heart step 8｜「有天份冇用功，一樣企唔穩。演技係磨出嚟㗎，唔係跌落嚟㗎。」
- crew_laolinji_serious｜s_c2 step 3｜「後生仔，」
- extra_ad_fen_sad｜s_fen_intro step 10｜「驕傲少少唔怕，最怕你哋呢班後生，走嘅走、散嘅散。唉……唔講喇，飲茶。」
- extra_ad_fen_serious｜s_fen_farewell step 0｜「得啦。廣播嗌我入閘喇——阿偉，你要捱落去呀，捱到第三年嗰啲，先至係真命天子嚟㗎。」
- ho_sang_surprise｜s_f4 step 2｜「呢排成日有人嚟問我攞主意：」
- ko_chunkit_shy｜s_ho_meet step 4｜「何生帶人呀？你就聽話啲啦，佢唔鍾意人臨場至問東問西㗎。」
- ko_chunkit_think｜s_fong_crisis step 5｜「邊個負責條安全帶㗎？點解會鬆成咁？快啲搵人上去呀！」
- lin_hiu_smile｜s_hiu_end step 5｜「聽到你咁講，我真係好開心。其實我都一直好在意你，只係唔敢開口啫。」
- liu_bingxing_sad｜e_liu_heart step 0｜「做笑匠最攰嘅，唔係諗橋，係你幾唔開心都好，上到台都要畀人笑得出。」
- liu_bingxing_surprise｜e_liu_stageup step 0｜「咦，隔籬枱嗰個變咗熟客仔喎。」
- liu_bingxing_think｜e_liu_T1 step 4｜「呢度啲奶茶，飲咗咁多年都係呢隻味，唔知係茶好，定係我念舊。」
- lok_gasing_angry｜e_lok_first step 0｜「冇運行？你都識講。行開啦後生仔，唔好阻住條走廊。」
- lok_gasing_shy｜e_lok_T2 step 2｜「鍾意還鍾意，但電視台直情唔畀原創上大騷，話怕觀眾唔識欣賞。咁寫歌嗰啲人，係咪要餓」
- lok_gasing_smile｜e_lok_beats step 6｜「唔使你唱到幾勁，嗰段得幾句，你把聲夠實淨就得，我聽過你喺片場哼歌㗎。」
- lok_gasing_surprise｜e_lok_stageup step 0｜「咦，你又嚟呀？坐低啦，唔使企到咁拘謹。」
- lui_ging_serious｜s_lei_end step 7｜「不過你要記住，我這個人，不會忘記誰在我低谷時走了。」
- luk_baakyin_angry｜e_luk_first step 0｜「臨記咁多個，我記唔晒。唔好阻住走廊。」
- luk_baakyin_sad｜s_c12 step 10｜「唔好意思，連累你哋。做呢行，俾人愛同俾人鬧，有時係同一班人。」
- luk_baakyin_smile｜e_luk_heart step 0｜「……多謝。肯靜靜聽我講晒嘅人，真係冇幾個。」
- mak_zhendong_angry｜e_mak_first step 0｜「收聲。」
- mak_zhendong_smile｜e_mak_heart step 12｜「捱到今日，唔係我叻，係我唔敢停。」
- ngai_wingnaam_angry｜e_ngai_T0 step 2｜「走啦。唔好學人哋咁八卦，武行嘅嘢，睇多都冇用。」
- ngai_wingnaam_serious｜e_ngai_T0sup step 3｜「後生仔，你嗰場企穩啲，鏡頭掃過嚟嗰陣唔好亂郁。」
- ngai_wingnaam_smile｜e_ngai_first step 8｜「你企喺度做咩啫？等我請你飲呀？我而家請唔起喇。」
- ngai_wingnaam_surprise｜e_ngai_stageup step 0｜「咦，阿偉嚟咗呀？坐低先啦，唔使企到咁生外。」
- ngai_wingnaam_think｜e_ngai_pool step 4｜「而家人哋一聽我個名，就話諗下先，諗下先即係冇下文㗎喇。」
- so_jiyan_surprise｜e_so_T1 step 0｜「咦，你咪嗰日喺大堂幫我擋鏡頭嗰個？」
- vera_serious｜s_vera_meet step 3｜「規矩好簡單：你企到鏡頭前面，觀眾第一眼睇到嘅係成個感覺，唔係你嗰套演技，衫錯咗就」

## 實駕診斷（今批搵到嘅三個根源，全部已修＋證實）

1. **chung 攔截唔觸發——C9 軟 loc 壓制（softPreview-only）**：
   day 368 rec_star 盤上有 chung，但 `enc79StoryPendingAt("rec_star")` 回 true——
   C9 喺 soft behavior gate 下 soft loc 係 rec_star（硬表係 tvb_harbour），
   C9 未做就壓住嗰度嘅巧遇。soft gate 係 opt-in（`?softPreview=1`），
   live 遊戲 C9 係 tvb_harbour，rec_star 唔受壓——所以呢張係生檔，唔係死檔。
   修法：phase seed 加 `story_done=["C9"]`。證實：day 368 overlay 即刻觸發。
2. **chung angry 唔係 T3 opener，係 pool T3[0]**（resolver section 標籤再次錯）：
   C9 閘清除後播出嚟嘅係 heart 線；實查 `ENC84_DLG_chung_choning`，
   「有天份冇用功」喺 `pool.T3[0]`。修法：seed 加 `heartDone=True`
   （無 beat＋無 heart → pool T3[0] 首段）。證實：fix-up 即見。
3. **芬姐 intro 撳唔到——兩重撳掣問題**：
   (a) 海港針中心俾嘢遮住，Playwright click hit-test timeout
   （pin 可見 52×52 但 `click_first` 回 None）→ `open_loc_retry` 改用 DOM `.click()`；
   地圖區列表掣係死路（onclick 空，DOM click 完全無反應），只有 pin 先係 live。
   (b) sheet 滑入中 Playwright click actionability timeout → `play_offer`
   改用 DOM `.click()` 撳 action 掣＋搵唔到嗰陣 dump 標題同 acts。
   另：新遊戲後第一次撳針間歇性靜默失效（第二次即開），機制未完全證實，
   `open_loc_retry`（驗 sheet＋最多 3 次）兜住咗。呢個本身可能係真 UX bug，
   範圍外，列入跟進。

## 生成＋接入

- 方法跟 v127：以該角 base 生成圖做編輯參照，淨換面部表情；風格錨同行；
  prompt 永禁真人姓名；成張重生，唔准合成接駁。37 張，總擲數 41 次。
- 去背 `qa138/work138_proc.py`（連通體剪影＋填洞＋收邊＋羽毛，WebP q92，唔焗邊）；
  焗邊 `qa138/bake138.py`（米白 RGB 243,233,210，r=round(3×原生高/422)），37/37 PASS。
- 接入：新圖入 `assets/story/fullbody/`，loader 註冊跟 v127 做法；
  **index.html 零改動**（SAVE key／softRev s107／產品 `?v=` v20a10 全部唔郁）。
- 入庫範圍：37 張 webp＋2 新測試＋7 計數測試＋qa138/（drive／分類／trace／log）。
  **唔入**：gen138／assets138／qc138（生成中間檔）、qa138/shots138（38MB 截圖，
  工作副本 `~/workspace/linji-work138/qa138/shots138/` 留檔，跟 v127 前例）。

## 測試（rebase 後最終基底 f0ae995＝v136）

- 全套：work **206 PASS／12 FAIL** vs pristine **204 PASS／12 FAIL**，
  FAIL 清單一模一樣（12 個全部 pre-existing：flash51、giglib36、pacing35、poster59、
  rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38），**零回歸**。
  Work 多 2 個 PASS＝兩張新 dlg138 測試。
- 新測試 `tests/test_dlg138_static.py`（實線 57→54，死檔清單加 lin／tsui，
  DEAD_SHIPPED 語義：檔案存在但實線 0）＋`tests/test_dlg138_logic.js`，
  全部 PASS，連反證。
- Rebase 三次（v143→v134→v136 落地），每次重跑全套＋drive spot-check：
  spot-check 1（632e371）：chung＋lok＋fen intro 4/4；
  spot-check 2（c881530）：fen intro 兩張＋lok sweep；
  spot-check 3（c881530）：fen farewell；
  spot-check 4（f0ae995）：chung＋fen intro＋lok sweep 4/4。
  全部 target404 {}、pageerrors []。

## 併發落地說明

落地嗰陣 v142 統籌同時喺同一個常駐 clone 落地（commit `b06dbc1`）。
兩邊檔案零重疊（v142：index.html＋qa142／tests 若干；v138：37 webp＋tests 9 張＋qa138），
squash merge 嗰陣 index 一度同時有兩邊嘅 staged 檔；v138 commit 用 `--only` 精確檔案清單
（209 張）提交，v142 嘅檔原封不動留返畀佢哋，之後佢哋嘅 commit 先落，
次序係 b06dbc1（v142）→ f451930（v138）。落地後 index 已清。

## 跟進（唔入呢批）

- 死檔修復票：mock R_hiu_meet 加 serious 台詞；live R_xu_* 加 serious 台詞
  （兩張死圖已入庫，加返線即用得，唔使重生）。
- 下一批表情候選：tsui_poushan_angry／think／surprise／smile（live 句已核實，庫入面未有）。
- v127 揭出嘅四類阻塞另開票（cast_main.json 死檔／pack C9·C13·C16 覆寫／
  resultBeats 引擎／傾談分流錯配）。
- 第一次 pin click 靜默失效（可能係真 UX bug，玩家第一撳無反應），要設計／引擎決定先修。
- 盤點抽取器已修（同 beat 守則＋補抽 text:-beat），下一批唔會再重犯 phantom 誤歸。
