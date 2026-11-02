# 對手／導師／友情／資本弧 Detail Pack3 v2（書面回修）

> **SOFT_NITS_FIX_v1 → JSON version 2.1（2026-11-02）：**  
> - 只掃 title／setting／少數 label 書面化；**不改** id／flag／choice id／弧。  
> - synopsis「你」→「阿偉」；「留低／企硬／學嘢」清。  
> - `parallelOk` 未改。


> **狀態：** v2 書面回修完成；**待覆測**；**未出圖**。
> **成品：** `story_detail_rival_mentor.json`（version 2）
> **變更：** 只改 synopsis／beats.lines／choices.label／effects.notes 為書面語；弧／id／flag／choice id／linksMain／artId／arcBeat 結構不變（相對 v1）。
> **對齊：** PLOT_MASTER_PLAN_v1.4-DS §5／§6；PLOT_DETAIL_UNLOCK_v1 §5；COPY_STYLE_HK_LEXICON；COPY_STYLE_MODERN_v1；pcSilent。
> **raw：** `_deepseek_detail_rival_mentor_v2_written_raw.json`

---

## 路線表

| arcLine | 人物 | arcKind | 節點前綴 | 連線主線 | 節數 |
|---|---|---|---|---|---|
| `ko` | 高俊傑 | rival | `A_ko_` | C3, C10, C12, T2 | 5 |
| `hakfan` | 張克凡 | rival | `A_hakfan_` | P2–P4資源場 | 5 |
| `tsijun` | 張子駿 | mentor | `A_tsijun_` | C8, C11, C17, E03, T3 | 5 |
| `fong` | 方小龍 | friend | `A_fong_` | P3替身危機, E05 | 5 |
| `tong` | 唐素雲 | mentor | `A_tong_` | P2去留, E09 | 5 |
| `ho` | 何生 | mentor | `A_ho_` | C2, C4, E01 | 5 |
| `gao` | 高文瀚 | mentor | `A_gao_` | C8, C12, E02, T4 | 5 |
| `lei` | 雷勁 | capital | `A_lei_` | C7, flag_anti_lei | 5 |

## 連線主線摘要

- **高俊傑** ↔ C3 搶板／C10＋T2 台慶位／C12 賀歲 standing
- **張克凡** ↔ P2–P4 資源場（與高俊傑造型／聲口可區分：資源壓 vs 同輩嘴賤搶板）
- **張子駿** ↔ C8／C11＋T3／C17／E03 評審眼熟
- **方小龍** ↔ P3 替身危機／E05 動作班底
- **唐素雲** ↔ P2 去留鉤／E09 淡出氣氛
- **何生** ↔ C2／C4／E01 穩陣線
- **高文瀚** ↔ C8／C12＋T4／E02 有名有實
- **雷勁** ↔ C7 拒苛刻合約／`flag_anti_lei`

## Flag 一覽（本包寫入）
```
flag_ally_danger
flag_anti_lei
flag_cold_war
flag_fong_crisis_call
flag_fong_crisis_freeze
flag_fong_crisis_rescue
flag_fong_ending_cold
flag_fong_ending_respect
flag_fong_ending_save
flag_fong_intro_sent
flag_fong_met
flag_fong_push1_learn
flag_fong_push1_let
flag_fong_push1_watch
flag_fong_push2_leave
flag_fong_push2_rest
flag_fong_push2_train
flag_fong_saved_once
flag_fong_warned
flag_friend_saved
flag_gao_crisis_commit
flag_gao_crisis_honest
flag_gao_crisis_stepback
flag_gao_curious
flag_gao_ending_break
flag_gao_ending_respect
flag_gao_ending_stay
flag_gao_honest
flag_gao_met
flag_gao_push2_deliver
flag_gao_push2_help
flag_gao_push2_safe
flag_gao_push_ask
flag_gao_push_grab
flag_gao_push_wait
flag_hakfan_allied
flag_hakfan_avoided
flag_hakfan_cold_war
flag_hakfan_deferred
flag_hakfan_faced_off
flag_hakfan_leaked
flag_hakfan_mentor_complete
flag_hakfan_met
flag_hakfan_negotiated
flag_hakfan_own_style
flag_hakfan_probed
flag_hakfan_rejected_support
flag_hakfan_rival_respect
flag_hakfan_solo
flag_hakfan_stand_ground
flag_hakfan_took_support
flag_ho_asked_why
flag_ho_big_bet
flag_ho_cold_war
flag_ho_crisis_ask
flag_ho_crisis_leave
flag_ho_crisis_stay
flag_ho_intro_round
flag_ho_mentor_complete
flag_ho_met
flag_ho_quality_trust
flag_ho_refused_deal
flag_ho_rival_respect
flag_ho_self_select
flag_ho_took_deal
flag_ho_trust_up
flag_ko_ally
flag_ko_cold_war
flag_ko_crisis_deal
flag_ko_crisis_fight
flag_ko_crisis_stepback
flag_ko_mentor_complete
flag_ko_met_grab
flag_ko_met_yield
flag_ko_push1_counter
flag_ko_push1_observe
flag_ko_push2_ally
flag_ko_push2_confront
flag_ko_push2_ignore
flag_ko_rival_respect
flag_lei_ally
flag_lei_bluff
flag_lei_bound
flag_lei_cold_war
flag_lei_contract_read
flag_lei_crisis
flag_lei_deal
flag_lei_defiant
flag_lei_met
flag_lei_negotiated
flag_lei_push1
flag_lei_push2
flag_lei_refuse_film
flag_lei_rival_respect
flag_rival_respect
flag_tong_crisis_confess
flag_tong_crisis_leave
flag_tong_crisis_stay
flag_tong_ending_cold
flag_tong_ending_mentor
flag_tong_ending_respect
flag_tong_met_step_in
flag_tong_met_watch
flag_tong_push1_accept
flag_tong_push1_argue
flag_tong_push2_doubt
flag_tong_push2_stay
flag_tsijun_crisis_cut
flag_tsijun_crisis_hold
flag_tsijun_crisis_silent
flag_tsijun_ending_cold
flag_tsijun_ending_complete
flag_tsijun_ending_respect
flag_tsijun_met_leave
flag_tsijun_met_stay
flag_tsijun_push1_grind
flag_tsijun_push1_side
flag_tsijun_push2_film
flag_tsijun_push2_variety
```

## 節點速覽

### 高俊傑（`ko`／rival）

#### A_ko_meet　搶板初遇　〔meet〕
- when／setting：1988春｜星河電視台二號錄影廠外走廊，臨時演員排隊等派通告
- speakers：['高俊傑']；pcSilent=True
- conflict／links：C3／['C3']
- synopsis：你排隊等派通告，高俊傑突然插隊搶走你手上嗰張板紙通告，仲要當眾讀出你個名來激你。
- choices：`C_ko_meet_grab` 搶返通告機會，企硬唔讓, `C_ko_meet_yield` 讓佢一次，睇清楚佢咩底細
- flags：['flag_ko_met_grab', 'flag_ko_met_yield']

#### A_ko_push1　同場走位互懟　〔push〕
- when／setting：1988夏｜星河電視台一號錄影廠，處境劇圍讀同走位排練
- speakers：['高俊傑']；pcSilent=True
- conflict／links：排練場上互較執生同搶鏡位／None
- synopsis：圍讀時高俊傑刻意搶你句對白嘅節奏，走位又霸住你個位，副導在場睇住邊個執生快。
- choices：`C_ko_push1_counter` 即場改節奏反壓佢，畀副導睇你執生, `C_ko_push1_observe` 先記住佢嘅走位習慣，唔急住反擊
- flags：['flag_ko_push1_counter', 'flag_ko_push1_observe']

#### A_ko_push2　台慶籌備互較　〔push〕
- when／setting：1989秋｜星河電視台台慶籌備會議室同排舞室
- speakers：['高俊傑']；pcSilent=True
- conflict／links：台慶排位同放風比較，爭企中間嘅機會／['C10', 'T2']
- synopsis：台慶節目排位，高俊傑四圍放風話你嘅環節係「攝時間」，仲喺排舞室當眾比較邊個企中間。
- choices：`C_ko_push2_ally` 拉攏排舞師同助導，用實力爭返個位, `C_ko_push2_confront` 當面同佢講清楚，唔好再放風, `C_ko_push2_ignore` 懶理佢把口，專心練自己環節
- flags：['flag_ko_push2_ally', 'flag_ko_push2_confront', 'flag_ko_push2_ignore']

#### A_ko_crisis　台慶位危機　〔crisis〕
- when／setting：1989冬｜星河電視台台慶綵排後台同監製房
- speakers：['高俊傑']；pcSilent=True
- conflict／links：C10／T2／['C10', 'T2']
- synopsis：台慶前夕突然要 cut 一個環節，高俊傑同你都被點名，監製要你哋自己講點解應該留低。
- choices：`C_ko_crisis_fight` 喺監製面前企硬，講出自己環節嘅價值, `C_ko_crisis_deal` 同高俊傑私下講數，一人讓一步, `C_ko_crisis_stepback` 主動退一步，換取下次機會
- flags：['flag_ko_crisis_deal', 'flag_ko_crisis_fight', 'flag_ko_crisis_stepback']

#### A_ko_ending　賀歲片場再遇　〔ending〕
- when／setting：1991夏｜星河電視台賀歲片廠景，兩人多年後再同場
- speakers：['高俊傑']；pcSilent=True
- conflict／links：C12／['C12']
- synopsis：賀歲片開鏡，你同高俊傑多年後再同場，佢主動行埋嚟，講返當年搶板同台慶嘅事。
- choices：`C_ko_ending_respect` 同佢握手，承認大家鬥咗咁多年都係為咗做好場戲, `C_ko_ending_cold` 笑笑口帶過，唔表態，留返條界線, `C_ko_ending_mentor` 反過來提點佢幾句，當自己行先一步
- flags：['flag_ko_cold_war', 'flag_ko_mentor_complete', 'flag_ko_rival_respect']

### 張克凡（`hakfan`／rival）

#### A_hakfan_meet　試鏡房門外嘅世家子弟　〔meet〕
- when／setting：1989春｜星河電視台三號試鏡房走廊，牆上貼住新劇《赤道線》角色表，長櫈坐滿等叫名嘅演員。
- speakers：['張克凡', '副導演芬姐']；pcSilent=True
- conflict／links：P2資源場／['P2資源場']
- synopsis：你喺走廊等試鏡，張克凡由芬姐親自帶入房，連排隊都唔使。佢臨入房前望你一眼，語氣唔重但句句都係資源壓人，話呢個角色早有人打過招呼。你未入房已經知道，呢場唔止考演技。
- choices：`C_hakfan_meet_hold` 企定唔走，等入房用實力講嘢, `C_hakfan_meet_probe` 唔動氣，反問佢邊個角色最難做, `C_hakfan_meet_walk` 唔想糾纏，轉身去搵其他通告
- flags：['flag_hakfan_avoided', 'flag_hakfan_met', 'flag_hakfan_probed', 'flag_hakfan_stand_ground']

#### A_hakfan_push1　人脈飯局搶走嘅角色　〔push〕
- when／setting：1989夏｜星河電視台製作部樓層，佈告板啱啱貼出《赤道線》casting名單，隔籬茶水間有人講緊昨晚飯局。
- speakers：['張克凡', '助導阿森']；pcSilent=True
- conflict／links：張克凡靠飯局人脈搶走主角，你只剩配角位；連 P2資源場，接 A_hakfan_push2。／None
- synopsis：名單出咗，角色落喺張克凡手上。你喺茶水間撞到佢，佢唔否認係飯局傾返嚟，仲話呢行本來就係咁行。你手上只剩一個戲份少嘅配角位，要決定爭唔爭。
- choices：`C_hakfan_push1_take` 應承配角位，留喺同一個廠鬥, `C_hakfan_push1_negotiate` 同助導講數，要求加戲份先接, `C_hakfan_push1_reject` 唔接配角，另覓其他劇組
- flags：['flag_hakfan_negotiated', 'flag_hakfan_rejected_support', 'flag_hakfan_took_support']

#### A_hakfan_push2　同一場戲，兩種演法　〔push〕
- when／setting：1990｜星河電視台五號錄影廠，《赤道線》中段重頭戲排練，導演要求一次過排完整場對手戲。
- speakers：['張克凡', '導演陸志明']；pcSilent=True
- conflict／links：同場對戲，張克凡用世家訓練壓你節奏，你用地道演法頂返；連 A_hakfan_crisis。／None
- synopsis：排練場上你同張克凡正面對戲。佢用世家出身嘅方法拆解角色，你用地道草根嘅演法回應。導演未叫停，全廠都喺度睇邊個帶得住場。
- choices：`C_hakfan_push2_match` 接住佢嘅節奏，當場對到盡, `C_hakfan_push2_own` 唔理佢，照自己草根演法做到底, `C_hakfan_push2_defer` 讓半拍，等佢帶完整場先
- flags：['flag_hakfan_deferred', 'flag_hakfan_faced_off', 'flag_hakfan_own_style']

#### A_hakfan_crisis　廠期危機，兩條船同一條水　〔crisis〕
- when／setting：1991｜星河電視台製作部會議室，臨時召開《赤道線》續集危機會議，佈景費同廠期都出咗問題。
- speakers：['張克凡', '監製周世昌']；pcSilent=True
- conflict／links：P2–P4資源場／['P2–P4資源場']
- synopsis：續集資金出事，電視台想削減廠期，你同張克凡嘅重頭戲隨時被剪。監製要人孭飛同外間製作公司傾，張克凡手上有人脈，你有草根觀眾緣，兩條路本來唔相交，而家要揀聯手定各自保命。
- choices：`C_hakfan_crisis_ally` 同張克凡聯手，一齊去傾外間公司, `C_hakfan_crisis_solo` 唔靠佢人脈，自己搵監製傾減廠期方案, `C_hakfan_crisis_leak` 將佢爸爸搭路嘅事爆俾記者，搶輿論
- flags：['flag_hakfan_allied', 'flag_hakfan_leaked', 'flag_hakfan_solo']

#### A_hakfan_ending　頒獎禮後台，兩種收場　〔ending〕
- when／setting：1992｜星河電視台台慶頒獎禮後台化妝間，獎項啱啱頒完，走廊仲傳嚟掌聲。
- speakers：['張克凡', '副導演芬姐']；pcSilent=True
- conflict／links：台慶後台最後對望，張克凡放下家世語氣講演技，你決定敵線收於尊重抑或繼續死敵；連 A_hakfan_crisis。／None
- synopsis：幾年較量去到台慶夜。你同張克凡喺後台化妝間撞正，獎項塵埃落定。佢望住你，第一次冇用家世開場，而係講演技。你點回應，決定呢條敵線點收。
- choices：`C_hakfan_ending_respect` 伸手話下次同場再較量，認佢係對手, `C_hakfan_ending_cold` 冷淡回應，話獎項先係真章, `C_hakfan_ending_mentor` 反問佢有冇興趣一齊帶新人
- flags：['flag_hakfan_cold_war', 'flag_hakfan_mentor_complete', 'flag_hakfan_rival_respect']

### 張子駿（`tsijun`／mentor）

#### A_tsijun_meet　練功房的第一課　〔meet〕
- when／setting：1988春｜星河電視台舊廠大樓三樓，單元劇練功房。牆身油漆剝落，鏡前鋪住一塊起毛嘅地膠，角落擺住一疊手寫分鏡紙。
- speakers：['張子駿', '高俊傑']；pcSilent=True
- conflict／links：C1／T1／['C1', 'T1']
- synopsis：你被派去單元劇練功房試鏡，遇到文藝導演張子駿。佢唔急住睇你演戲，反而叫你喺鏡前企定，慢慢講一次自己點解想做戲。高俊傑喺門口探頭，催你唔好嘥時間。
- choices：`C_tsijun_meet_stay` 留低跟張子駿慢慢磨，唔理外面催, `C_tsijun_meet_leave` 跟高俊傑走，先接廠期通告
- flags：['flag_tsijun_met_leave', 'flag_tsijun_met_stay']

#### A_tsijun_push1　單元劇班底　〔push〕
- when／setting：1988秋｜星河電視台二號錄影廠，單元劇《夜行街》佈景。凌晨兩點，劇組食完外賣，燈光師喺度換燈泡。
- speakers：['張子駿', '高俊傑']；pcSilent=True
- conflict／links：收視話題同演出層次拉扯；張子駿守住班底，高俊傑要廠方交代。／None
- synopsis：張子駿把你收入單元劇班底，要你演一個只有三場戲嘅小角色。高俊傑嫌你曝光太少，話廠方想換個有話題嘅人。張子駿頂住壓力，叫你喺排練房再磨一次。
- choices：`C_tsijun_push1_grind` 留喺排練房，同張子駿磨到收廠, `C_tsijun_push1_side` 私下應承高俊傑，兩邊都唔得罪
- flags：['flag_tsijun_push1_grind', 'flag_tsijun_push1_side']

#### A_tsijun_push2　商業同文藝兩張通告　〔push〕
- when／setting：1989春｜星河電視台大堂，兩張通告同時貼喺佈告板：一張係大騷綜藝嘉賓，一張係張子駿嘅影展短片試鏡。
- speakers：['高俊傑', '張子駿']；pcSilent=True
- conflict／links：C8／['C8']
- synopsis：高俊傑幫你爭到綜藝大騷嘅位，話曝光難得。張子駿同時遞上短片試鏡邀請，講明冇錢、冇人氣，但會送去影展。你只可以揀一張通告。
- choices：`C_tsijun_push2_film` 揀張子駿嘅短片試鏡，放棄大騷, `C_tsijun_push2_variety` 揀綜藝大騷，同張子駿講聲抱歉
- flags：['flag_tsijun_push2_film', 'flag_tsijun_push2_variety']

#### A_tsijun_crisis　曝光同層次　〔crisis〕
- when／setting：1990秋｜影展放映室，外面落緊雨。張子駿嘅短片入圍一個小單元，你喺片入面只有一個長鏡頭。
- speakers：['張子駿', '高俊傑']；pcSilent=True
- conflict／links：C11／T3／['C11', 'T3']
- synopsis：短片放映後，有發行商想剪走你嗰個長鏡頭，換成節奏快嘅版本，話咁先有人氣。張子駿堅持保留，高俊傑就話機會難得。你被夾喺中間。
- choices：`C_tsijun_crisis_hold` 公開支持張子駿，企硬保留長鏡頭, `C_tsijun_crisis_cut` 勸張子駿剪短，換發行商支持, `C_tsijun_crisis_silent` 唔表態，等兩邊自己傾
- flags：['flag_tsijun_crisis_cut', 'flag_tsijun_crisis_hold', 'flag_tsijun_crisis_silent']

#### A_tsijun_ending　評審席上嘅熟面口　〔ending〕
- when／setting：1992｜影展頒獎禮後台走廊，張子駿坐喺評審席隔籬嘅休息位，手上仲揸住節目表。
- speakers：['張子駿', '高俊傑']；pcSilent=True
- conflict／links：C17／E03／['C17', 'E03']
- synopsis：幾年過去，你喺影展再遇張子駿。佢望住你，話你個樣熟口熟面，但問你仲記唔記得當初練功房嗰堂。高俊傑喺旁邊等緊你過去應酬。
- choices：`C_tsijun_ending_respect` 留低同張子駿講返當年嗰堂，先過去酒會, `C_tsijun_ending_complete` 請張子駿做你下一部戲嘅監製, `C_tsijun_ending_cold` 點頭就走，過去酒會應酬
- flags：['flag_tsijun_ending_cold', 'flag_tsijun_ending_complete', 'flag_tsijun_ending_respect']

### 方小龍（`fong`／friend）

#### A_fong_meet　茶餐廳兩份早餐　〔meet〕
- when／setting：1988｜旺角舊式茶餐廳，卡位油漬斑斑，吊扇慢轉
- speakers：['方小龍', '高俊傑']；pcSilent=True
- conflict／links：你對入行嘅猶豫 vs 小龍嘅熱心拉攏；高俊傑對臨記嘅冷淡／None
- synopsis：你同方小龍由細喺武館識到大，佢而家做武師替身，成日大嗓門拍你膊頭。今日佢拉你嚟茶餐廳，話有門路介紹你入星河電視台做臨記，順便講下自己棚入面嘅辛酸。
- choices：`C_fong_meet_take` 多謝小龍，跟佢去星河見識下, `C_fong_meet_ask` 問清楚替身有幾危險先決定
- flags：['flag_fong_intro_sent', 'flag_fong_met', 'flag_fong_warned']

#### A_fong_push1　武師棚推進　〔push〕
- when／setting：1989｜星河電視台舊廠棚，木搭高台同軟墊，燈光刺眼
- speakers：['張克凡', '方小龍']；pcSilent=True
- conflict／links：張克凡嘅嚴要求 vs 小龍嘅死頂；你喺棚入面嘅位置／None
- synopsis：廠景開拍，方小龍喺棚入面做替身跳高台，你喺下面做臨記。張克凡做武指，要求愈嚟愈高。小龍跳完一次，拍你膊頭話仲頂得住，但腳已經有啲拐。
- choices：`C_fong_push1_watch` 喺下面睇實小龍個位，出事即扶, `C_fong_push1_learn` 趁機問張克凡點樣做武師, `C_fong_push1_let` 唔敢出聲，企埋一邊睇
- flags：['flag_fong_push1_learn', 'flag_fong_push1_let', 'flag_fong_push1_watch']

#### A_fong_push2　外銷高峰練功夜　〔push〕
- when／setting：1990夏｜星河電視台天台，夜燈同水塔，遠處霓虹招牌
- speakers：['方小龍', '高俊傑']；pcSilent=True
- conflict／links：密集通告下嘅練功壓力 vs 班底規矩；你同小龍嘅投入程度／None
- synopsis：動作片外銷高峰，棚入面通告密到爆。方小龍收工拉你上天台練功，話唔練就追唔上。高俊傑路過，講起替身行情同班底規矩。
- choices：`C_fong_push2_train` 陪小龍練到落雨先走, `C_fong_push2_rest` 勸小龍休息，唔好練到傷, `C_fong_push2_leave` 話攰，先走一步
- flags：['flag_fong_push2_leave', 'flag_fong_push2_rest', 'flag_fong_push2_train']

#### A_fong_crisis　替身危機　〔crisis〕
- when／setting：1990夏｜星河電視台廠棚，高台邊緣同濕滑地板，現場一片混亂
- speakers：['張克凡', '方小龍', '高俊傑']；pcSilent=True
- conflict／links：P3替身危機／['P3替身危機']
- synopsis：一場高台跳躍戲，方小龍做替身，落地時腳一滑，半邊身掛喺台邊。張克凡叫停，高俊傑喺下面喝住。你要即刻決定點做。
- choices：`C_fong_crisis_rescue` 衝上去捉實小龍，唔理台穩唔穩, `C_fong_crisis_call` 大聲叫張克凡同高俊傑指揮救人, `C_fong_crisis_freeze` 嚇到呆咗，企喺原地
- flags：['flag_fong_crisis_call', 'flag_fong_crisis_freeze', 'flag_fong_crisis_rescue', 'flag_fong_saved_once']

#### A_fong_ending　動作班底兩條路　〔ending〕
- when／setting：1992｜星河電視台新廠棚外，黃昏，貨車同道具箱堆滿空地
- speakers：['方小龍', '張克凡', '高俊傑']；pcSilent=True
- conflict／links：E05／['E05']
- synopsis：兩年過去，動作班底重組。方小龍傷後復出，問你仲會唔會同佢一齊捱。張克凡想拉你入新班底，高俊傑就話規矩要講清楚。你要揀點行落去。
- choices：`C_fong_ending_save` 同小龍一齊入新班底，互相睇住, `C_fong_ending_respect` 各自跟唔同班底，但講明有起事上嚟一定幫手, `C_fong_ending_cold` 唔再玩替身，同小龍各行各路
- flags：['flag_cold_war', 'flag_fong_ending_cold', 'flag_fong_ending_respect', 'flag_fong_ending_save', 'flag_friend_saved', 'flag_rival_respect']

### 唐素雲（`tong`／mentor）

#### A_tong_meet　旁聽點名　〔meet〕
- when／setting：1989｜星河電視台排練室，下午，陽光斜照，唐素雲正為幾位新人試戲。
- speakers：['唐素雲', '高俊傑']；pcSilent=True
- conflict／links：唐素雲賞識 vs 高俊傑輕視；玩家要決定是否踏出第一步。／['P2去留']
- synopsis：你混入排練室旁聽，唐素雲點名要你即場演一段，考你膽量同反應。
- choices：`C_tong_meet_step_in` 行入去，照唐老師指示演一段, `C_tong_meet_watch` 企喺門口繼續睇，唔敢行入去
- flags：['flag_tong_met_step_in', 'flag_tong_met_watch']

#### A_tong_push1　演技矯正　〔push〕
- when／setting：1989夏｜星河電視台二號排練室，黃昏，唐素雲單對單指導你。
- speakers：['唐素雲']；pcSilent=True
- conflict／links：唐素雲的嚴格要求 vs 你對自己演法的堅持。／['P2去留']
- synopsis：唐素雲逐句矯正你的唸白，要你放低演嘢，用真感情。
- choices：`C_tong_push1_accept` 虛心接受，照唐老師方法重新演一次, `C_tong_push1_argue` 覺得自己方法冇問題，同唐老師理論
- flags：['flag_tong_push1_accept', 'flag_tong_push1_argue']

#### A_tong_push2　去留一句鉤　〔push〕
- when／setting：1989｜星河電視台走廊，夜晚，排練完結後唐素雲叫住你。
- speakers：['唐素雲', '張克凡']；pcSilent=True
- conflict／links：P2去留／['P2去留']
- synopsis：唐素雲用一句說話鉤住你，要你諗清楚係咪真係想喺呢行留低。
- choices：`C_tong_push2_stay` 同唐老師講，你想留低學嘢, `C_tong_push2_doubt` 坦白同唐老師講，你仲未諗清楚
- flags：['flag_tong_push2_doubt', 'flag_tong_push2_stay']

#### A_tong_crisis　是否繼續跟她磨　〔crisis〕
- when／setting：1990｜星河電視台排練室，深夜，唐素雲同你排一場重頭戲，你頻頻NG。
- speakers：['唐素雲', '高俊傑']；pcSilent=True
- conflict／links：E09氣氛／['E09']
- synopsis：你哋排咗成晚，唐素雲開始失去耐性，高俊傑喺旁邊冷嘲熱諷，你要決定係咪繼續跟唐素雲磨落去。
- choices：`C_tong_crisis_stay` 留低，繼續跟唐老師磨, `C_tong_crisis_leave` 頂唔順，決定唔再跟唐老師, `C_tong_crisis_confess` 同唐老師坦白自己嘅困難，請求體諒
- flags：['flag_tong_crisis_confess', 'flag_tong_crisis_leave', 'flag_tong_crisis_stay']

#### A_tong_ending　教室窗邊的去留　〔ending〕
- when／setting：1992｜星河電視台天台，黃昏，唐素雲約你見面，話有嘢同你講。
- speakers：['唐素雲']；pcSilent=True
- conflict／links：E09／['E09']
- synopsis：唐素雲話你知，佢要退休喇，問你記唔記得當初點解留低，並將佢嘅演戲心得交託畀你。
- choices：`C_tong_ending_mentor` 承諾會記住唐老師教誨，繼續做戲, `C_tong_ending_respect` 多謝唐老師，但話自己可能會轉行, `C_tong_ending_cold` 冷淡回應，話自己已經唔再需要佢教
- flags：['flag_tong_ending_cold', 'flag_tong_ending_mentor', 'flag_tong_ending_respect']

### 何生（`ho`／mentor）

#### A_ho_meet　事務所初帶　〔meet〕
- when／setting：1988春｜星河電視台走廊，排隊等試鏡嘅人龍旁邊
- speakers：['何生', '高俊傑']；pcSilent=True
- conflict／links：C2／['C2']
- synopsis：何生喺走廊截住你，話你企位企錯晒，順手教你點樣喺人龍入面畀導演記得你個名。佢唔講大道理，只講邊個監製睇人睇邊樣。
- choices：`C_ho_meet_follow` 跟何生行一圈，逐個監製打招呼, `C_ho_meet_ask` 先問清楚何生點解要幫你
- flags：['flag_ho_asked_why', 'flag_ho_intro_round', 'flag_ho_met']

#### A_ho_push1　拒單信任　〔push〕
- when／setting：1988春｜何生間細細嘅事務所，枱面擺住一疊通告紙
- speakers：['何生', '張克凡']；pcSilent=True
- conflict／links：C4／['C4']
- synopsis：有張出手好闊嘅單搵上門，錢多但條件糊塗，何生睇完搖晒頭，要你哋自己揀接唔接。
- choices：`C_ho_push1_refuse` 聽何生講，推咗張糊塗單, `C_ho_push1_take` 照接，錢要緊，條款自己啃
- flags：['flag_ho_refused_deal', 'flag_ho_took_deal', 'flag_ho_trust_up']

#### A_ho_push2　通告品質把關　〔push〕
- when／setting：1989｜深夜嘅片場外圍，何生攞住張通告表逐項圈
- speakers：['何生', '高俊傑']；pcSilent=True
- conflict／links：通告量同品質拉鋸；何生要你唔好做蝕底嘅工／None
- synopsis：你開始多咗通告，何生逐張同你核對，話你知邊張係消耗你、邊張係幫你儲底。
- choices：`C_ho_push2_trust` 交畀何生篩，自己專心拍戲, `C_ho_push2_self` 自己揀通告，唔想乜都靠人
- flags：['flag_ho_quality_trust', 'flag_ho_self_select']

#### A_ho_crisis　賭大嘅信任考驗　〔crisis〕
- when／setting：1991冬｜何生事務所，暖爐壞咗，兩個人着住大褸講數
- speakers：['何生', '張克凡']；pcSilent=True
- conflict／links：忠誠同利益對撞；何生押上身家；連 E01／['E01']
- synopsis：何生押咗事務所大半本錢幫你爭一個大項目，另一邊有人出更高價撬你過檔，佢要你講清楚企邊邊。
- choices：`C_ho_crisis_stay` 留低，同何生一齊賭呢鋪, `C_ho_crisis_leave` 過檔，錢同前途要緊, `C_ho_crisis_ask` 要求何生講明風險先決定
- flags：['flag_ho_big_bet', 'flag_ho_crisis_ask', 'flag_ho_crisis_leave', 'flag_ho_crisis_stay']

#### A_ho_ending　穩陣線信任巔峰　〔ending〕
- when／setting：1992｜星河電視台大堂，頒獎禮散場後人潮漸散
- speakers：['何生', '高俊傑']；pcSilent=True
- conflict／links：E01／['E01']
- synopsis：幾年過去，何生企喺大堂一角等你，講返當年走廊嗰句「呢行靠人帶」，然後問你之後想點行。
- choices：`C_ho_ending_complete` 認何生做一世師傅，留喺穩陣線, `C_ho_ending_respect` 多謝何生，但想自己出去闖, `C_ho_ending_cold` 當面講清條數，從此各行各路
- flags：['flag_ho_cold_war', 'flag_ho_mentor_complete', 'flag_ho_rival_respect']

### 高文瀚（`gao`／mentor）

#### A_gao_meet　試鏡房嘅第一眼　〔meet〕
- when／setting：1989春｜星河電視台七樓試鏡房，長枱後面坐住三個監製，窗外係春天濕漉漉嘅廣播道
- speakers：['高文瀚', '張克凡']；pcSilent=True
- conflict／links：C8／['C8']
- synopsis：你喺走廊等咗成個鐘，入到試鏡房，高文瀚冇叫你自我介紹，淨係叫你讀手上嗰頁劇本。你讀完，佢冇即刻評語，反而問你一句：你覺得呢場戲，個角色係想贏定係想走？你答完，佢先慢慢揭返你嘅履歷。
- choices：`C_gao_meet_answer` 照直講角色想走，唔怕同監製唱反調, `C_gao_meet_safe` 順住劇本講角色想贏，穩陣啲先, `C_gao_meet_ask` 反問佢心目中嘅答案係咩
- flags：['flag_gao_curious', 'flag_gao_honest', 'flag_gao_met']

#### A_gao_push1　搶位要趁早　〔push〕
- when／setting：1989｜星河電視台服裝間外面嘅走廊，通告板貼滿手寫紙仔，人來人往
- speakers：['高文瀚', '助導阿玲', '張克凡']；pcSilent=True
- conflict／links：爭位嘅野心 vs 唔想顯得咄咄逼人；高文瀚要睇你係唔係真係餓／None
- synopsis：高文瀚手上有一個二線角色嘅位，幾個人爭。佢冇明講畀邊個，只係喺走廊撞到你，同你講咗句「你知唔知自己爭緊咩」。你要喺佢面前展示你值得個位，定係乖乖等安排。
- choices：`C_gao_push1_grab` 即場講出你點演呢個角色，搶返個位, `C_gao_push1_wait` 唔搶，等佢自己決定，做好本分先, `C_gao_push1_ask` 問清楚個角色嘅戲份同走向先決定
- flags：['flag_gao_push_ask', 'flag_gao_push_grab', 'flag_gao_push_wait']

#### A_gao_push2　台慶夜嘅一分鐘　〔push〕
- when／setting：1990｜星河電視台一號錄影廠，台慶綵排現場，燈光師試燈，滿地電線
- speakers：['高文瀚', '助導阿玲', '張克凡']；pcSilent=True
- conflict／links：一次過嘅壓力 vs 廠內等你出錯嘅目光；高文瀚要睇你係唔係佢可以推出去嘅人／None
- synopsis：台慶夜有一個一分鐘嘅曝光位，高文瀚話畀你，但條件係你要喺綵排時一次過搞掂，唔可以 NG。廠入面所有人都睇住你，包括幾個等緊你出錯嘅人。
- choices：`C_gao_push2_deliver` 頂住壓力，一次過交足貨, `C_gao_push2_safe` 收住做，寧願穩陣唔博, `C_gao_push2_help` 主動叫張克凡幫你對一次位
- flags：['flag_gao_push2_deliver', 'flag_gao_push2_help', 'flag_gao_push2_safe']

#### A_gao_crisis　賀歲檔嘅賭注　〔crisis〕
- when／setting：1991夏｜星河電視台高文瀚嘅辦公室，枱面攤住賀歲片嘅預算表，冷氣開到好凍
- speakers：['高文瀚', '助導阿玲', '張克凡']；pcSilent=True
- conflict／links：C12／T4／['C12', 'T4']
- synopsis：高文瀚押咗公司嘅賀歲檔喺你身上，但上面有人質疑，話你未夠班孭飛。高文瀚叫你入房，冇安慰你，淨係將預算表推到你面前，問你一句：你覺得我應唔應該繼續賭落去。
- choices：`C_gao_crisis_commit` 叫佢繼續賭，你孭晒個責任, `C_gao_crisis_honest` 照直講你驚，但會盡做, `C_gao_crisis_stepback` 叫佢縮細個賭注，保住公司
- flags：['flag_gao_crisis_commit', 'flag_gao_crisis_honest', 'flag_gao_crisis_stepback']

#### A_gao_ending　金牌推手嘅最後一句　〔ending〕
- when／setting：1992｜星河電視台天台，黃昏，遠處係九龍嘅樓景，風有點大
- speakers：['高文瀚', '張克凡']；pcSilent=True
- conflict／links：E02／['E02']
- synopsis：幾年過去，高文瀚約你上天台。佢話自己手上嘅資源開始要分畀新人，問你覺得自己企唔企得穩。你點答，決定佢係繼續做你嘅推手，定係慢慢撤走啲資源。
- choices：`C_gao_ending_respect` 多謝佢一路推你，講明你會自己行落去, `C_gao_ending_stay` 叫佢繼續推，你仲需要佢個位, `C_gao_ending_break` 話你唔想再靠佢個名，想自己爭
- flags：['flag_gao_ending_break', 'flag_gao_ending_respect', 'flag_gao_ending_stay']

### 雷勁（`lei`／capital）

#### A_lei_meet　茶餐廳攤約　〔meet〕
- when／setting：1988秋｜旺角一間舊式茶餐廳，卡位油漬未抹乾淨，雷勁坐喺最入面嗰張枱，面前擺住一疊文件同兩杯凍奶茶。
- speakers：['雷勁', '張克凡']；pcSilent=True
- conflict／links：雷勁想收你入旗下，你想保住自主；合約條款苛刻，簽與唔簽都係壓力。／None
- synopsis：雷勁透過中間人約你見面，話想傾「合作」，實際上係想睇你係咪一個可以收歸旗下嘅人。佢一開口就笑住講以前做龍虎武師點樣捱，笑完就將一份合約推到你面前。
- choices：`C_lei_meet_read` 攞起合約逐條睇清楚先講, `C_lei_meet_polite` 客氣推搪，話要同公司商量, `C_lei_meet_bluff` 扮晒有後台，唔好意思拒絕
- flags：['flag_lei_bluff', 'flag_lei_contract_read', 'flag_lei_met']

#### A_lei_push1　脅迫推進　〔push〕
- when／setting：1988秋冬｜星河電視台停車場出口，夜晚，雷勁靠住一架舊平治，兩個手下企遠少少食煙。
- speakers：['雷勁', '高俊傑']；pcSilent=True
- conflict／links：雷勁用通告同人脈施壓，你想守住立場又唔想斷咗條路。／None
- synopsis：雷勁開始出手，先係叫你嘅通告被「技術性」調走，再喺停車場截住你，語氣半笑半嚇，話呢行好現實，唔埋堆就會被邊緣化。
- choices：`C_lei_push1_stand` 企硬，話唔會因為咁就範, `C_lei_push1_soften` 低調安撫，話有機會再傾, `C_lei_push1_seek_help` 搵高俊傑幫手擋一擋
- flags：['flag_ko_ally', 'flag_lei_defiant', 'flag_lei_push1']

#### A_lei_push2　低成本動作片班底拉攏　〔push〕
- when／setting：1989｜新界一間改裝貨倉，用嚟拍低成本動作片，地下有軟墊，牆邊擺住幾支木棍同威也。
- speakers：['雷勁', '張克凡']；pcSilent=True
- conflict／links：雷勁用電影機會換你接受苛刻條件，你想上位又唔想俾人食住。／None
- synopsis：雷勁搞緊一部低成本動作片，想搵你入班底做主角，話係機會，但合約條件一樣苛，仲要你兼做替身同宣傳。佢帶你睇貨倉，語氣似賞識又似試探。
- choices：`C_lei_push2_join` 應承入班底，但要改兩條條款, `C_lei_push2_refuse` 婉拒，話想留喺電視台發展, `C_lei_push2_probe` 問清楚片酬同分帳先算
- flags：['flag_lei_contract_read', 'flag_lei_deal', 'flag_lei_push2', 'flag_lei_refuse_film']

#### A_lei_crisis　拒苛刻合約危機　〔crisis〕
- when／setting：1988秋冬｜雷勁嘅寫字樓，枱面擺住合約同一個計數簿，窗外係舊樓天台。
- speakers：['雷勁', '高俊傑']；pcSilent=True
- conflict／links：C7／['C7']
- synopsis：雷勁要你即刻簽一份長約，年期長、抽佣高、違約罰得重，仲話唔簽就當你唔俾面。你拒絕之後，佢冇即刻發惡，只係慢慢合上計數簿，講咗句令你心寒嘅說話。
- choices：`C_lei_crisis_refuse` 當面拒絕，話唔會簽呢種約, `C_lei_crisis_negotiate` 提出反建議，拉高自己籌碼, `C_lei_crisis_sign` 頂唔住壓力，簽咗先算
- flags：['flag_anti_lei', 'flag_lei_bound', 'flag_lei_crisis', 'flag_lei_negotiated']

#### A_lei_ending　危險盟友或決裂　〔ending〕
- when／setting：1992｜一間已經丟空嘅舊片場，佈景拆剩一半，雷勁一個人坐喺導演椅上，手上轉住一支筆。
- speakers：['雷勁', '張克凡']；pcSilent=True
- conflict／links：flag_anti_lei／['flag_anti_lei']
- synopsis：幾年過去，雷勁嘅勢力唔同以前，你亦唔再係當年嗰個新人。佢約你喺舊片場見面，話想「埋尾」，但講到尾都係要你表態：做佢盟友，定係各行各路。
- choices：`C_lei_ending_ally` 應承做盟友，但講明底線, `C_lei_ending_respect` 拒絕埋堆，但保住互相尊重, `C_lei_ending_cold` 當面數清舊帳，各行各路
- flags：['flag_ally_danger', 'flag_anti_lei', 'flag_lei_ally', 'flag_lei_cold_war', 'flag_lei_rival_respect']

---

## QA 自檢

- nodeCount: **40**
- noForbiddenLexicon: **True**
- noAweiSpeaker: **True**
- choiceIdsAllCPrefix: **True**
- flagsPresent: **True**
- meetPushCrisisPerLine: **True**
- noRomanceHEBELabels: **True**
- starRiverTV: **True**
- noRealCelebrityNames: **True**
- artDeferred: **True**
- pass: **True**

*出圖暫緩；待 tester QA（本回合未通知 tester）。*
