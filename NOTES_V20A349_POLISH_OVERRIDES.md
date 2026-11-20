# v20a349 文字潤飾第四批：藍若曦＋林曉晴覆寫表（玩家面生效文字）

日期：2026-11-20
模型：qwen4-max（官方 Bailian CLI，`bl text chat`；lan 套用部分零新呼叫）
流程：照 v347/v348（細批次＋敘述黑名單 brief＋程式閘門＋人手覆核＋成批制）

## 入版總數

| 對象 | 入版行數 | 備註 |
|---|---|---|
| 藍若曦 JSON（story_detail_romance_lan_xu.json） | 41 | v348 reverted_shadowed 全數套用（setting 3／synopsis 5／beats 18／choices label+notes 15） |
| 藍若曦覆寫表（index.html ROMANCE_WF2_OVERRIDES） | 26 | 25 行逐字對應套用（synopsis 4／beats 18／ending choiceText 3）＋ crisis synopsis 1 行新跑（覆寫版同 JSON 版係兩套文字） |
| 林曉晴覆寫表（index.html ROMANCE_V158_OVERRIDES） | 35 | 新跑：synopsis 5＋beats 30（林曉晴/助導對白 16＋旁白 14） |

## 工作 A：藍若曦逐字對應核實

- 41 條 reverted entries：JSON 原文 41/41 逐字對應；覆寫表 25 條逐字對應、1 條唔對應（R_lan_crisis.synopsis，覆寫版係另一套文字，改行新跑）、15 條冇覆寫對應（setting 3＋非 ending choices 12，JSON 專屬欄位）。
- 一致性做法（跟 wf2_81_logic「藍 JSON 版原 lines 全數保留」斷言）：beats／synopsis 同一批替換同時套落 JSON＋覆寫表；choices label 同步 fixture（romance_wf2_v80.json lanPa 5 個 label）＋weave48_logic 釘死嘅 ending 2 個 label；ending choiceText（label/notes）同 JSON 同步。
- 覆寫表 beats 冇 JSON 之外嘅行（加厚只加 beats 數，行文字同 JSON 一致），唔使額外新跑。

## 工作 B：林曉晴新跑（6 批，6 次呼叫，上限 20）

- 批次：hiu_meet／push1／push2／crisis／ending（各 synopsis＋beats）＋ lan_crisis_syn（1 行）。
- 分層：synopsis 敘述（書面語＋黑名單）；beats 全部行（包括旁白行）係呢層嘅廣東話層，brief 明文禁止改成書面語、禁止書面語標記（的/了/沒有/什麼/為什麼/他們/我們/不是/著）——跟 test_hiu266 語體斷言（beats 廣東話 ≥25／書面語 0／≥300 字；synopsis 廣東話標記 0）。
- 閘門：align／label／punct／digit 全 0；串層掃描 1 個 flag（hiu_crisis synopsis「關係」誤報，人手覆核確認書面語）；改動>三成 0；hiu266 閘（標記／字數／靚女／年份）除下述字數外全過。
- **個別保留原文 4 行**（v348 先例：測試約束行唔郁）：hiu_meet beats[3].lines[1]、hiu_push2 beats[1].lines[1]／beats[2].lines[1]／beats[3].lines[0]——潤飾後成節 beats 字數跌穿 hiu266 ≥300 底線（meet 299、push2 289），還原呢 4 行後 302／302。保留原文批次：零（成批制下 6 批全過，例外只係呢 4 行）。
- 逐行人手覆核：事實／人名／數字／年份／旗標字串零改動；對白口吻保留（林曉晴直接、助導公事公辦）；choice label／flags／stats／openConditions 一律冇郁（hiu266 釘死 push2 label「我哋一齊捱」不變）。

## 測試同步＋釘行

- tests/fixtures/romance_wf2_v80.json：lanPa 5 個 label 同步新句（wf2_81_logic merge 斷言）。
- tests/test_weave48_logic.js：ending 2 個 label 釘句同步新句。
- 釘行：今票全部係行內字串替換，index.html 行數不變（47,368），零漂移；kwan151／tang152 逐個覆驗 PASS，唔使 resync。
- Suite：398 PASS／9 FAIL，FAIL 名單同基線九項逐項相同，零回歸。相關測試（wf2_81 靜態+邏輯／weave48 靜態+邏輯／hiu266／r294／rom159 靜態+邏輯／rom183／rom176／delete268／weave46／tang152／kwan151／r296／r299／r342）逐個直接覆驗全 PASS。

## 攻略引文同步候選（改咗嘅對白 22 句，只列清單未做 artifact edit）

- [藍若曦] 哎呀——唔好意思，唔好意思，借過！（成疊通告牌同流程表俾人一撞，散晒一地）
- [藍若曦] 你都聽到嗰啲講法啦？我冇偏幫你——你嗰陣企得穩，又從來唔遲到，我先排你嗰格，係咁多。
- [藍若曦] （佢望住塊通告牌，笑得有啲勉強）做呢行，女人做場記，講咩都有人有意見。你明就得㗎喇。
- [藍若曦] 阿爸今日親自嚟等我收工，話要同我食飯——其實係想話我知，場記呢份工做到幾多歲，叫我一個月內轉文職。
- [藍若曦] 但係嗰度冇呢塊通告牌，冇你哋呢班人……我係咪好唔爭氣？一份工啫，我居然唔捨得成層後台。
- [藍若曦] （佢笑住轉身嗌下一組埋位，嗰句說話留咗喺走廊，冇人接。）
- [林曉晴] 你有興趣嘅話，我幫你問下，不過要快啲決定喇，啲位好快畀人搶晒㗎。
- [林曉晴] 不過記住呀，有啲助導好揀擇㗎，打聽清楚佢哋鍾意啲咩先，費事白行一趟。
- [林曉晴] 阿偉，今晚你得唔得閒？我想搵人傾下，呢兩封信我睇咗成晚，都未諗掂。
- [林曉晴] 一封係公司寄嚟，一封係屋企寄嚟。兩封都要我即刻覆，覆錯一步，成個人生唔同晒。
- [林曉晴] 公司嗰封，話想簽我做玉女，三年約，人工唔錯，但三年內唔准拍拖，唔准接其他公司嘅戲。
- [林曉晴] 屋企嗰封，話阿爸阿媽諗住走，問我跟唔跟埋去。佢哋話，呢邊捱臨記，捱到幾時先出頭。
- [林曉晴] 跟屋企走，我又唔捨得呢邊。呢邊先係我發夢嘅地方，行到呢步，點捨得走。
- [林曉晴] 你講咩我都聽，不過你要諗清楚先好講。呢個決定，我會記一世。
- [林曉晴] 今晚夜班真係攰到死，又凍又眼瞓，好彩總算殺青喇。你之後有咩打算呀？
- [林曉晴] 嗰日試鏡之後，我成晚瞓唔到，諗如果嗰個角色係你攞到，我會唔會嬲你。
- [林曉晴] 我知你都好想要呢個機會，但最後只揀得一個，你會點做呀？
- [助導] 評審會睇你哋臨場反應，放鬆啲，當平時演戲咁就得喇。
- [林曉晴] 嗰陣你叫我唔好簽，我聽你話。今日我終於有返個屬於自己嘅角色，唔係人哋派畀我嘅玉女，係我爭返嚟嘅。
- [林曉晴] 嗰陣我以為留低慢慢捱，係最傻嘅揀法。而家我先知，傻嗰個捱到最後先有得笑。
- [林曉晴] 不過，我唔想淨係還人情。我想問你，我哋之間除咗人情，仲有冇其他嘢。
- [林曉晴] 嗰晚你話我哋一齊捱，我記住咗。捱到而家，我哋真係一齊捱到呢度喇。

## 附註

- enc158PrepareNode（index.html L27761）入面 crisis／ending 變體 beats 係玩家面文字，唔喺今票範圍（只潤覆寫表），未潤，留待日後另開票。
- 林曉晴 JSON 版 beats（vera_hiu_choi 檔）今票冇郁——runtime 由 V158 覆寫，JSON 版唔係玩家面來源；v348 還原嘅 JSON 潤飾稿仍喺 batch3/reverted_shadowed.json。
- 工作檔：`~/workspace/linji-polish-pilot/batch4/`（verify_lan.js、apply_lan.py、extract/build_prompts/run/verify/apply 腳本、逐批 prompt＋raw 輸出、verify_results4.json、diffs4.txt、applied4.json）。

## 落地紀錄

- main 內容 commit：`8bb9043`（squash merge 自 v349-polish-overrides 分支 `51391f4`）
- Suite（工作副本全跑）：398 PASS／9 FAIL，FAIL 名單同基線九項逐項相同，零回歸
- Pages 核實：index.html md5 `182867f0fc22bd67985c4ca0295d2b12`、lan_xu md5 `393093ee469a92b65e73de4fd7eaac9f`，同本地 byte-identical
- 工作副本 linji-work349 已刪
