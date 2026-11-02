# Romance Detail 鄧麗萍 v1（可選攻略）

> **SOFT_NITS_FIX_v1（2026-11-02）：**  
> - `R_tang_meet.openConditions=[]`（可寫入 `flag_tang_open`）；push1+＝`flag_tang_open`＋`rel_tang_threshold`（**數值=2**，playtest 可調）。  
> - synopsis／setting 第二人稱「你」→「阿偉」。  
> - 輕潤：跳住→跳動；企得住→站得住；孭→扛；識做→懂分寸。  
> - stub（Pack2）改寫 `flag_tang_met`＋`rel_tang`，**不**寫 `flag_tang_open`。


> **狀態：** 用戶確認後開 detail；`cast_main` tang_laiping 聲口；雙條件 `flag_tang_open`＋`rel_tang` 門檻；**未出圖**。  
> **成品：** `story_detail_romance_tang.json`  
> **Stub 相容：** `story_detail_romance_lan_xu.json` → `R_tang_meet_stub` 保留，`supersededBy: R_tang_meet`

---

## 開線閘

- **雙條件：** `flag_tang_open` ＋ `rel_tang` 門檻（`rel_tang_threshold`）
- **Meet：** 排片上門談判（取代公關偶遇 stub）；一支 choice 寫入 `flag_tang_open`
- **Push+：** 需雙條件已滿足

---

## 鄧麗萍

### R_tang_meet　上門談排片：四成上座率先講數　〔meet〕
- when／setting：1990秋｜龍頭院線排片部會議室；牆上貼滿午夜場與周末場的報表，紅筆圈住每一格未達標的數字。
- speakers：['鄧麗萍', '院線助理']；pcSilent=True
- conflict：新片爭檔期 vs 院線數據門檻
- openConditions：['flag_tang_open', 'rel_tang_threshold']
- supersedes：`R_tang_meet_stub`
- synopsis：你帶着新片資料上門，想在龍頭院線爭一個正式檔期。鄧麗萍沒有同你寒暄，一開口就是上座率和午夜場數據；你要在她的報表邏輯裏面，證明自己這套戲值得一個位。
- choices：
  - `C_tang_meet_data` 攤開你手上的觀眾數據，同她講清楚這套戲的目標客群同口碑走勢 → ['flag_tang_open'] {'rel_tang': 1}
  - `C_tang_meet_wait` 不急着爭，先問清楚她這條線的排片準則，回去再補數據 → ['flag_tang_met_wait'] {'rel_tang': 0}

### R_tang_push1　中控室夜話：數據互助第一步　〔push〕
- when／setting：1990冬｜院線票房中控室，深夜十一點半，螢幕上跳住各院即時入座數字，枱面有一疊未拆的午夜場報告。
- speakers：['鄧麗萍']；pcSilent=True
- conflict：冷門檔期風險 vs 數據回報
- openConditions：['flag_tang_open', 'rel_tang_threshold']
- synopsis：你同鄧麗萍開始有來往，但她仍然句句帶百分比。你們交換試映情報同冷門檔期資料，她第一次主動問你這套戲在其他區的口碑走勢。
- choices：
  - `C_tang_push1_exchange` 用你手上的試映口碑情報，換她一個冷門檔期的正式位 → ['flag_tang_push1_exchange'] {'rel_tang': 1}
  - `C_tang_push1_prove` 不換情報，直接應承冷門檔期，用午夜場數字證明自己 → ['flag_tang_push1_prove'] {'rel_tang': 1}

### R_tang_push2　午夜場之後：黃金檔試水　〔push〕
- when／setting：1991春｜周六深夜午夜場散場後，戲院後巷茶餐廳，枱上攤着即日票房紙，隔壁枱還有人吃着宵夜。
- speakers：['鄧麗萍']；pcSilent=True
- conflict：純商業計算 vs 私人情感試探
- openConditions：['flag_tang_open', 'rel_tang_threshold']
- synopsis：黃金檔試水成績出爐，鄧麗萍約你在午夜場後對數。她心情比平時鬆一點，講起自己以前排過一套文藝片，蝕到要寫報告。你可以選擇繼續純商業，或者問她私人那一句。
- choices：
  - `C_tang_push2_business` 不追問私人事，順着數據講下一季黃金檔合作 → ['flag_tang_push2_business'] {'rel_tang': 1}
  - `C_tang_push2_private` 問她當年那套文藝片，是不是到今日還有一條刺 → ['flag_tang_push2_private'] {'rel_tang': 1}

### R_tang_crisis　檔期數據 vs 人情：黃金檔只得一個　〔crisis〕
- when／setting：1991秋｜院線總部會議室，對手片發行商剛剛離開，枱面留下兩份搶黃金檔的建議書，牆上排片表用紅筆畫到密密麻麻。
- speakers：['鄧麗萍', '院線助理']；pcSilent=True
- conflict：檔期數據vs人情
- openConditions：['flag_tang_open', 'rel_tang_threshold']
- synopsis：對手片用高價搶黃金檔，你手上有一套帶人情和藝術傾向的片想排同一個位。鄧麗萍要你在數據和人情之間揀，她自己亦被上頭壓住要交數。
- choices：
  - `C_tang_crisis_data` 照數據排，將黃金檔讓給對手片，自己這套戲退去次檔 → ['flag_tang_crisis_data'] {'rel_tang': 1}
  - `C_tang_crisis_favor` 堅持為人情片爭黃金檔，願意自己孭上座率風險 → ['flag_tang_crisis_favor'] {'rel_tang': 1}
  - `C_tang_crisis_middle` 提出折衷：黃金檔讓一半場次，午夜場用你這套戲試口碑 → ['flag_tang_crisis_middle'] {'rel_tang': 1}

### R_tang_ending　年終檢討之後：盟友定決裂　〔ending〕
- when／setting：1992｜院線年終檢討會後，走廊燈光半暗，盡頭係一間未開場的空戲院，銀幕還未拉開。
- speakers：['鄧麗萍']；pcSilent=True
- conflict：商業盟友 vs 感情原則
- openConditions：['flag_tang_open', 'rel_tang_threshold']
- synopsis：年終數字出爐，你這套戲全年為院線帶來實質增長。鄧麗萍在走廊叫住你，講明她認可你的號召力；但她要你揀，是做一個並肩的商業盟友，還是繼續用感情挑戰她這條線。
- choices：
  - `C_tang_ending_he` HE：商業盟友＋感情（可與事業並存） → ['flag_tang_commit', 'flag_tang_he'] {'rel_tang': 3, 'standing': 1}
  - `C_tang_ending_be` BE：數字至上決裂／冷淡（可與事業並存） → ['flag_tang_be'] {'rel_tang': -2}

## QA 自檢

- banned_scan_body: pass
- oral_leftover: []
- aw_first_person_lines: 0
- aw_speaker_beats: 0
- flag_tang_open_on_meet: True
- he_be_flags: True
- data_voice_hits: 6
- node_count: 5
- node_ids: ['R_tang_meet', 'R_tang_push1', 'R_tang_push2', 'R_tang_crisis', 'R_tang_ending']
- lexicon: COPY_STYLE_HK_LEXICON.md
- deepseek_calls: deepseek-chat romance_tang
- steer: cast_main tang_laiping; flag_tang_*; pcSilent; C_*; openConditions dual gate; no art
- polish: 書面語輕潤；HE/BE stats；cast+助理

## 出圖

暫緩（artId 僅佔位）。