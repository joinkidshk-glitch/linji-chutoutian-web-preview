# NOTES_V20A296_EXPRESSION_DEAD_FILES.md — v20a296 Q9 表情死檔補齊

## 摘要
- 基線 main `4b34904`（v295），分支 `v20a296-expression-dead-files`。
- 出齊 26 張新表情圖（237→263 張）＋補 2 句對白（徐寶珊 serious、張子駿 angry）。
- 兩張孤兒 serious 全部復活：`lin_hiu_serious.webp` 唔使加對白（已有 1 句 live）、
  `tsui_poushan_serious.webp` 加 1 句新對白。
- Suite 基線 359／9（v295）；v296 後見 §5。

## §1 推導（親查，唔係照抄分流數字）
- 工具：`qa296/derive296.js`（抽現行 index.html＋content packs 全部對白，用 runtime
  真分類器 `dlg106ResolveCategory` 分類，逐角逐表情計 live 句數，對返
  `assets/story/fullbody/` 237 檔）＋`qa296/probe296.js`（試分類候選句）。
- 推導分兩輪修正：第一輪誤將 pack 句當非 live（浪漫／主線／對手 pack 本身就係 live
  內容，經 STORY_WIRE 載入）；第二輪補 `text:"..."` 單句 beats（WF4／結果 beats
  唔用 `lines:` 陣列）＋`story_beats_phase1.json`＋speaker 映射（老臨記→crew_laolinji、
  阿媽／場務姐姐→shadow_female、場務／副導演→shadow_male）。
- Pack 句 live 例外：R_hiu_meet／R_choi_meet 由 mock
  `MOCK_STORY_DUAL_MEET_THICKEN_SOFT_v1.json` 覆寫（pack 版播唔到，mock 版先係 live）；
  R_tang_* 感情線已取消；vera 講者排除（Q10／v297 成個移除）。
- 推導結果（`qa296/derive296.json`）：
  - **A組：有 live 句但缺資產**——扣起 4 位新星後共 26 組（見 §2），全部出圖。
  - **B組：零 live 句＋缺資產**——除咗 cheung_tsijun:angry（補對白後生，入 A組）之外
    全部 0 句，唔生成（v127 教訓：唔好為死線補圖）。清單見 derive 輸出 B組。
  - **C組：資產存在但 0 live 句（孤兒）**——v296 前 9 組；復活 2 組之後剩 8 組：
    cheung_tsijun:smile、chow_choiyi:sad／think／angry、gao_wenhan:angry、
    gu_mingfai:angry、lui_ging:serious、ngai_wingnaam:surprise。全部 0 live 句，
    留畀日後內容票，唔喺 v296 處理。
  - **4 位新星 blocked**：hon_sauting、kong_siying、shum_yingsuet、wu_meilam
    完全冇 fullbody 檔（連 base 都冇；base 缺失檢查只 flag 呢四位），佢哋 16 張
    live 表情（hon 3／kong 4／shum 4／wu 5）唔入 v296，等新星美術票先出 base
    設計；佢哋對白現時跌返剪影（v290 已定設計決定）。
  - **lin_hiu:serious 已自行解決**：而家有 1 句 live CORE 句（npc_lines_core
    colleague→lin_hiu：「有前輩教我，等燈光嗰陣要記住走位」），檔案已存在，
    唔使加對白，只需更新測試。

## §2 新圖 26 張（全部第一擲即中，逐張 QC pass）
- 方法（v127／v138 前例）：以該角 base 生成圖做編輯參照，淨換面部表情；風格錨
  `~/workspace/linji-native-design/style-anchor-awei-anime.jpg` 同行；prompt 寫死全身
  企立、四分三面、雙眼齊見、同衫同姿勢同構圖同面型、純色淺色背景、唔准文字；
  prompt 永禁真人姓名；成張重生，唔准合成接駁。表情鍵固定詞彙
  base／smile／serious／sad／angry／surprise／shy／think。
- 生成：`qa296/gen296/`（26 張 PNG 原圖，唔入 repo——v138 前例只 commit baked＋腳本）。
- 去背：`qa296/work296_proc.py`（沿用 v138：連通體剪影＋填洞＋收邊＋羽毛法；
  v123 wedge 選擇性填洞）。26 張全部 components=1、frags 空、wedge_dropped 空；
  ratio diff vs base −0.006～−0.071（最大 so_jiyan_think −0.071，同一人同衫，
  生成構圖略窄，接受）。
- 焗邊：`qa296/bake296.py`（米白 RGB 243,233,210，r=round(3×原生高/422)）。
  **26／26 PASS**：邊帶米白命中 ≥99.99%、內部大差異 0、far_cream_px=0、
  frame_transp ≥0.963。報告 `qa296/bake_results296.json`；焗邊成品
  `qa296/baked296/`（26 張，亦入庫）。
- 面部對照：`qa296/qc296/face_{stem}.png`（左 base 頭、右新圖頭，H=620；唔入 repo）。
- QC 逐張 `muse.read` 對返 base：面型／五官／髮型同一人、冇現代造型走樣、
  冇衫／姿勢漂移。重點核實：lan_ruoxi 兩張係 v7 陽光改版（高馬尾＋黃上衣＋
  白百褶裙）；ko_chunkit 兩張除表情外完全一致；lui_ging 三張花恤衫＋粗金鏈＋
  右眉骨淺刀疤一致；tsui_poushan 五張墨綠絲絨裙＋珍珠頸鏈＋金手拿包一致。

| 檔名 | live 句數 | 例句（首句） |
|---|---|---|
| cheung_hakfan_think.webp | 1 | （低聲）佢今次真係押咗好多喺你身上，你講嘢要諗清楚。 |
| cheung_tsijun_angry.webp | 1 | 收聲，聽我講埋先。（§3 新對白） |
| chow_choiyi_shy.webp | 2 | 睇嚟你真係好鍾意睇人，咁對做戲梗係有幫助啦。 |
| crew_laolinji_smile.webp | 1 | 遲啲有咩好嘢，我實提住你。 |
| gao_wenhan_think.webp | 1 | 叫佢等。呢個位由我決定，我未諗清楚就冇人可以覆。 |
| ho_sang_shy.webp | 3 | 不過呢，間中都會聽到，邊個邊個攞咗居留，又返嚟搵食。 |
| ko_chunkit_sad.webp | 1 | 唐老師，佢跟你跟咗成年都係咁，不如算啦。 |
| ko_chunkit_surprise.webp | 1 | 嘩，阿偉你嚟啦？呢個位光線好啲，我企呢度先啦，你企旁邊啦。 |
| lan_ruoxi_surprise.webp | 1 | 咦，阿偉，今日又跟組？ |
| lan_ruoxi_angry.webp | 3 | 喂，臨記仔，企埋一邊先啦，唔好阻住人行。 |
| lin_hiu_surprise.webp | 2 | 估唔到會喺度撞到你，呢個角色對我嚟講好重要㗎。 |
| lin_hiu_think.webp | 1 | 唔緊要。呢行，最唔缺嘅就係等——等通告、等埋位、等人諗清楚。 |
| lin_hiu_angry.webp | 1 | ……好。咁以後殺青，你唔准自己一個走——等埋我。 |
| lui_ging_sad.webp | 1 | 不過你要記住，我呢個人，唔會唔記得邊個喺我低谷嗰陣走咗。 |
| lui_ging_shy.webp | 1 | 哈哈，你呢個後生仔夠直接，我鍾意。 |
| lui_ging_think.webp | 3 | 你諗下，唔急，不過機會唔會等你太耐。 |
| so_jiyan_think.webp | 2 | 唔緊要。呢行，最唔缺嘅就係等——等通告、等出碟、等人諗清楚。 |
| so_jiyan_angry.webp | 2 | ……好。咁以後收工，你唔准自己一個走——等埋我。 |
| tong_souwan_sad.webp | 2 | 演戲唔係要你喊，係要你忍。忍唔住嗰一刻，觀眾先會喊。 |
| tong_souwan_think.webp | 1 | 有人走，有人留。你諗清楚，你係邊種人。 |
| tsui_poushan_smile.webp | 1 | 多謝你先。呢啲問題我應付咗好多年，今晚係第一次有人企喺我前面。 |
| tsui_poushan_sad.webp | 1 | 佢自己一個行咗出去。你嗰句「諗清楚」，仲有冇機會講第二次，冇人知。 |
| tsui_poushan_surprise.webp | 1 | 你有冇諗過自己開一間製作公司？我可以幫你搭路。 |
| tsui_poushan_think.webp | 2 | 唔緊要。呢行，最唔缺嘅就係等——等客、等開會、等人諗清楚。 |
| tsui_poushan_angry.webp | 2 | 今晚係慈善晚宴，私人事我唔答，生意嘅嘢亦唔會喺呢度講。 |
| yip_manji_think.webp | 3 | 唔緊要。呢行，最唔缺嘅就係等——等通告、等埋位、等人諗清楚。 |
| **合計** | **41 句** | |

## §3 補對白（2 句，全部廣東話對白）
- **tsui_poushan serious** → `content/story_detail_romance_lan_xu.json`
  R_xu_crisis 第 4 個 beat（徐寶珊「你係聰明人，應該明我意思㗎…」之後、
  「行內邊個唔係咁上位㗎？」之前），加第二句：
  「呢單生意，我唔係講笑。你跟我做嘢，就要認真。」
  候選句經 `qa296/probe296.js` 用真分類器探測：serious ✓。
  驗證：`test_wf2_81_logic.js` ALL PASS、`test_rom159_logic.js` 136／136。
- **cheung_tsijun angry** → `content/story_detail_rival_mentor.json`
  A_tsijun_crisis 第 4 個 beat（張子駿回應高俊傑「發行商話剪短啲先有人睇。
  張導，你唔好同錢鬥氣。」），加首句：
  「收聲，聽我講埋先。」
  候選句經 probe296.js 探測：angry ✓。落點查證：A_tsijun_crisis 喺
  rival_mentor pack（唔係主線 pack）；張子駿 NPC core director 句（greet／chat／
  advice／intel／pressure）全部沉穩提點，唔啱放嬲句，所以用危機節點。
- **lin_hiu serious**：唔使加對白（見 §1）。

## §4 測試
- `tests/test_dlg138_static.py` 更新：NEW 表 36→62 張（加 26 張 v296＋兩張孤兒
  句數 0→1）；實線句數合計 53→96（53＋41＋2）；fullbody 總數 237→263；
  DEAD 剩 vera_shy.webp 一張；DEAD_SHIPPED 清零；加 v296 焗邊驗證段
  （26 張全 PASS＋檔名同 NEW 表一致）。**275 PASS／0 FAIL**。
- 新測試 `tests/test_r296_expression_dead_files.js`：即場重跑 derive296.js 再斷言——
  26 張新圖存在＋WebP＋>50KB＋live 句數逐張對數；兩句新對白落點＋分類；
  缺資產 live 組只准係 4 位新星 16 張；4 位新星冇 base；fullbody 總數 263。
  **68 PASS／0 FAIL**。
- `qa296/derive296.js` 重跑：有 live 句但缺資產嘅組只剩 4 位新星 16 張；
  C組孤兒剩 8 組（全部 0 live）。

## §5 全套 suite
- `bash qa131/run_suite.sh <副本根> ~/workspace/suite296b.txt`：
  **TOTAL PASS 360 FAIL 9**（基線 359／9；＋1 PASS 係新測試 test_r296）。
- 9 項 FAIL 全部係已知 pre-existing，名單同基線一字唔差：
  flash51／slot50／soft_tip_111_restore／start53／weave43_static／
  weave44_static／weave49_static／wf5_87／wrap38。
- 第一輪 352／17：8 項新 FAIL 全部係 resync（7 檔 dlg 測試硬寫 fullbody 總數
  237／真檔 212；rom159_static sha 清單有 rival_mentor），已修：
  7 檔 dlg 測試 resync 到 263／238；rom159_static rival_mentor 出 sha 清單，
  改精確替代斷言（pristine＋A_tsijun_crisis 加 1 句），另加 R_xu_crisis
  針對性斷言；重跑後 360／9。
- 個別測試：test_dlg138_static.py 275 PASS／0 FAIL；
  test_r296_expression_dead_files.js 68 PASS／0 FAIL；
  test_wf2_81_logic.js ALL PASS；test_rom159_logic.js 136／136；
  test_rom159_static.py 146 checks／0 FAIL。

## §6 剩低未做（唔入 v296）
- 4 位新星 16 張表情（hon_sauting 3／kong_siying 4／shum_yingsuet 4／
  wu_meilam 5）：等新星美術票出 base 設計先。
- C組 8 個孤兒（0 live 句）：等日後內容票補對白。
- B組零 live 缺資產各組：唔生成，唔好為死線補圖。

## §7 改動清單
- 新增：`assets/story/fullbody/` 26 張 webp（焗邊成品，見 §2 表）。
- 修改：`content/story_detail_romance_lan_xu.json`（R_xu_crisis 加 1 句）、
  `content/story_detail_rival_mentor.json`（A_tsijun_crisis 加 1 句）、
  `tests/test_dlg138_static.py`（NEW 表＋總數＋DEAD＋焗邊段）。
- 新增：`tests/test_r296_expression_dead_files.js`、
  `qa296/derive296.js`、`qa296/probe296.js`、`qa296/derive296.json`、
  `qa296/work296_proc.py`、`qa296/bake296.py`、`qa296/bake_results296.json`、
  `qa296/work296_metrics.json`、`qa296/baked296/`（26 張）。
- 唔入 repo：`qa296/gen296/`（26 張 PNG 原圖，約 45MB）、`qa296/assets296/`（去背中間檔）、
  `qa296/qc296/`（面部對照圖）——v138 前例。
