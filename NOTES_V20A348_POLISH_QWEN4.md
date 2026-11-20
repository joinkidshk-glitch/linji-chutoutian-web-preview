# v20a348 文字潤飾第三批：romance 兩包＋tutorial（官方 qwen4-max）

日期：2026-11-20
模型：qwen4-max（官方 Bailian CLI，`bl text chat`）
流程：逐 node 細批次（beats／choices 分開送）＋敘述黑名單 brief＋程式閘門＋人手覆核＋成批制（照 v346/v347）

## 入版總數：124 行

| 檔 | 入版行數 | 備註 |
|---|---|---|
| content/story_detail_romance_lan_xu.json | 45 | 全部係徐寶珊（xu）線；藍若曦（lan）線 0 行（見下「覆寫遮蔽」） |
| content/story_detail_romance_vera_hiu_choi.json | 46 | 全部係周采兒（choi）線；林曉晴（hiu）線 0 行（見下） |
| content/tutorial_zh_HK.json | 33 | 教學文字（全敘述層） |

## 批次與閘門

- 22 批全過閘（align／label／punct／digit 全部 0 失敗；串層掃描 10 個 flag 全部係「關係」誤報，人手覆核確認書面語；改動>三成 2 處——TUT_AUD_LOCK body 句序調換，意思不變，人手覆核接受）。
- tut_a 首輪輸出截斷（completion 撞 4096 上限，漏 4 行）→ 拆 tut_a1（17 行）／tut_a2（12 行）以 --max-tokens 8192 重試，兩批全過閘。保留原文批次：零。
- 呼叫次數：23 次（21 首輪＋2 重試；上限 50）。
- 逐行人手覆核：事實／人名／數字／年份／旗標字串零改動；結構核實（還原入版行＝pristine 逐字一致）通過。

## 關鍵發現：lan／hiu JSON 被 index.html 覆寫表遮蔽（87 行還原，唔入版）

- 藍若曦 5 節點：runtime 由 `ROMANCE_WF2_OVERRIDES`（index.html L6915，applyRomanceWf2Overrides81）覆寫 synopsis／beats／choice label+notes。JSON 版文字唔係玩家面來源。
- 林曉晴 5 節點：runtime 由 `ROMANCE_V158_OVERRIDES`（index.html L7177，applyRomanceV158Overrides158）覆寫 beats／choices／flags／conditions——而且覆寫版 beats 同 JSON 版係兩套唔同文字（v158 WIP 重排層）。
- 兩線 JSON 潤飾共 87 行已過閘入版後全數還原（保持 JSON 同覆寫表一致，wf2_81／weave48 測試即時恢復 PASS）。潤飾後文字留底喺 `~/workspace/linji-polish-pilot/batch3/reverted_shadowed.json`。
- 跟進（另開票，唔喺本票範圍）：lan／hiu 玩家面文字要潤飾，須改 index.html 覆寫表（lan 覆寫行同 JSON 原文逐字對應，可直接套用同一批替換；hiu 覆寫係另一套文字，要另跑潤飾），並同步 wf2_81／weave48／hiu266 等測試同行號釘。

## 個別保留原文（3 處）

1. `R_tang_meet_stub` 6 行（lan_xu 檔）：test_tang152 明確要求 stub pack 原稿唔郁（正規化喺載入嗰陣做），還原。
2. `toasts.TUT_SHOOT.body[0]`：潤飾版「獲聘後，拍攝日已排進行程。」同 v108 S-42 已清電報句逐字相同（test_text108 gone 清單），保留原文「獲聘之後，拍攝日已經排進了行程。」
3. `R_choi_ending.beats[0].lines[1]`：潤飾版令 r296 表情分類推導 chow_choiyi shy 由 2 句變 3 句（test_r296 釘死計數），保留原文「但我哋呢條路，好似越行越難行埋一齊咁。」

## 測試同步

- tests/test_text108_static.py：S-42 釘句 11 處＋live 路徑值 5 處改查 v348 潤飾後新句（意思不變；TUT_SHOOT body[0] 釘句不變，見上）。
- tests/test_guidance34_static.py：TUT_MAP 釘句 2 處改查新句。
- Suite：398 PASS／9 FAIL，FAIL 名單同基線九項逐項相同（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），零回歸。相關測試（rom159／rom183／tang152／wf2_81／weave48／r296／r294／r342／r299／hiu266 等）逐個直接覆驗全 PASS。

## 攻略引文同步候選（改咗嘅對白 23 句，只列清單未做 artifact edit）

- [徐寶珊] 你識我㗎？我好似冇見過你。你係邊個部門派嚟幫手嘅臨記，定係邊位大哥叫你入嚟㗎？
- [徐寶珊] 今日咁多突發嘢，你都一件件拆掂，證明你唔止做臨記咁簡單喇。我睇人好少睇錯㗎。
- [徐寶珊] 你有冇諗過自己開一間製作公司？我可以幫你搭路，資金嗰邊都可以坐低慢慢傾，唔係講笑㗎。
- [徐寶珊] 嗰位陳老闆，公司每年廣告預算過千萬㗎。你識同佢打交道，以後唔怕冇工開，路都闊好多喇。
- [徐寶珊] 你唔使咁緊張喎，我喺度睇住你㗎嘛。你收工之後有咩消遣㗎？仲有呀，你有冇女朋友先？
- [徐寶珊] 我離婚好幾年喇，陪住我嘅就得返盤生意。不過最近覺得，身邊有個人傾下偈，都唔錯囉。
- [徐寶珊] 我唔想轉彎抹角喇。你跟住我做嘢，我擔保你三年內有自己一間製作公司，唔使再做臨記捱世界。
- [徐寶珊] 你係聰明人，應該明我意思㗎。我欣賞你，想留你喺我身邊做嘢，就係咁簡單。
- [徐寶珊] 行內邊個唔係咁上位㗎？齋靠實力邊夠呀。我當年都係一步步捱過嚟，先至有今日呢個位咋。
- [徐寶珊] 今晚係慈善晚宴，私人事我唔答，生意嘅嘢亦唔會喺呢度講。你哋唔好再逼埋嚟喇，得唔得？
- [徐寶珊] 多謝你先。呢啲問題我應付咗好多年，今晚係第一次有人企喺我前面，唔使我一個人頂晒㗎。
- [徐寶珊] 我聽朝就飛去外國傾一單大生意，幾個月都唔喺香港。呢隻錶你收咗佢啦，我見你啱戴，當係臨別小小心意囉，唔好同我計較價錢喇。
- [周采兒] 記者會啲通稿我唔鍾意抄，特登嚟片場搵你問幾句，方唔方便呀？
- [周采兒] 聽講你冇戲嗰陣都會留低，幫手搬嘢，又企埋一邊睇人演。
- [周采兒] 今日多謝你，呢篇嘢我會自己寫，唔會亂加嘢。
- [周采兒] 下次再嚟片場，我可能又會企喺度等你收工㗎喇。
- [周采兒] 最近有傳聞話劇組入面唔妥，你喺現場，有冇聽到啲風聲？
- [週刊編輯] 相係人哋追到交過嚟嘅，呢啲料唔搶先出，好快就畀人搶晒㗎喇。
- [週刊編輯] 你諗清楚，呢單嘢影響你前途㗎。
- [周采兒] 我……我唔想講大話，但又唔想因為私事影響工作。
- [周采兒] 我平時追人哋獨家就一回事，到自己嗰陣，我真係唔想害到人。
- [週刊編輯] 采兒，你係報館嘅得力記者，我唔想你因為呢件事冇咗前途。
- [周采兒] 我梗係想同你行落去啦，但我好驚份工會影響到你。

## 工作檔

`~/workspace/linji-polish-pilot/batch3/`（extract／build_prompts／run／verify／apply 腳本、逐批 prompt＋raw 輸出、verify_results3.json、diffs3.txt、applied3.json、reverted_shadowed.json、guide_candidates.txt）

## 落地紀錄

- main 內容 commit：`594a4d3`（squash merge 自 v348-polish-qwen4 分支 `bdced2f`）
- Suite（工作副本全跑）：398 PASS／9 FAIL，FAIL 名單同基線九項逐項相同，零回歸
- Pages 核實：三檔 byte-identical（lan_xu md5 `b349cc906878198d48ebcb3f14c53718`、vera_hiu_choi `d83ed5aababfec1f19c0f1d325bd2f7a`、tutorial `983243ba5c87873599b903c693306b30`）
- 工作副本 linji-work348 已刪
