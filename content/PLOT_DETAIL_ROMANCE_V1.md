# Romance Detail v1（Vera／林曉晴／周采兒）

> **SOFT_NITS_FIX_v1（2026-11-02）：** Choi `R_choi_*`→`C_choi_*`；crisis `linksMain:[C13]`；hiu／choi speaker「我」→旁白＋`pcSilent`；`qa.flagAlias` 供 wiring（不破壞性 rename flags）。


> **狀態：** DeepSeek 三線＋曉晴／采兒 beats 擴寫；**未出圖**。  
> **成品：** `story_detail_romance_vera_hiu_choi.json`

> **規則：** 確定前可平行；HE／BE 另計，可與事業結局並存。

---

## Vera（`vera`）

### R_vera_meet　造型間初遇　〔meet〕
- when／setting：1988春夏｜星河電視台造型間／試裝
- eraTag／artId／conflict：`era_1988_spring_grassroot`／`rom_vera_meet`／None
- cast：阿偉、Vera；beats=6
- synopsis：阿偉第一次到星河電視台試造型，Vera 是當值的造型師。她一眼看出阿偉的草根氣質，語氣帶點挑剔，卻又忍不住給了一句忠告，留下一個小鉤子。
- choices：
  - `C_vera_meet_warm` 暖場：多謝提點，虛心請教 → flags=['flag_vera_met_warm'] stats={'rel_vera': 1, 'craft': 1}
  - `C_vera_meet_cold` 冷淡：點頭就走，趕下一個通告 → flags=['flag_vera_met_cold'] stats={'rel_vera': 0, 'fame': 1}

### R_vera_push1　形象會議　〔push〕
- when／setting：1988秋｜星河電視台形象會議室／試造型
- eraTag／artId／conflict：`era_1988_autumn_unit`／`rom_vera_push1`／None
- cast：阿偉、Vera；beats=5
- synopsis：電視台為阿偉安排形象改造，Vera 負責主導。兩人在會議上討論風格方向，阿偉的投入程度影響 Vera 對他的觀感。
- choices：
  - `C_vera_push1_cooperate` 認真配合：花時間試造型 → flags=['flag_vera_cooperate'] stats={'rel_vera': 2, 'craft': 1}
  - `C_vera_push1_perfunctory` 敷衍：隨便試一套就算 → flags=['flag_vera_perfunctory'] stats={'rel_vera': 0, 'fame': 1}

### R_vera_push2　茶餐廳小聚　〔push〕
- when／setting：1989｜茶餐廳小聚
- eraTag／artId／conflict：`era_1989_spring`／`rom_vera_push2`／None
- cast：阿偉、Vera；beats=5
- synopsis：阿偉與 Vera 在茶餐廳偶遇，難得坐下來閒聊。Vera 問起阿偉的過去，阿偉可以選擇坦白心事，還是只談工作。
- choices：
  - `C_vera_push2_honest` 坦白心事：講自己的過去與夢想 → flags=['flag_vera_honest'] stats={'rel_vera': 2, 'craft': 1}
  - `C_vera_push2_work` 只談工作：保持專業距離 → flags=['flag_vera_worktalk'] stats={'rel_vera': 1, 'fame': 1}

### R_vera_crisis　打歌後台的抉擇　〔crisis〕
- when／setting：1991秋｜打歌現場後台／電台
- eraTag／artId／conflict：`era_1991_autumn_promo`／`rom_vera_crisis`／T5
- cast：阿偉、Vera；beats=5
- synopsis：阿偉在電台打歌，Vera 在後台等他。她問阿偉幾時得閒見面，阿偉要在陪伴她與趕下一個通告之間作出選擇。
- choices：
  - `C_vera_crisis_stay` 陪她：推遲通告，留下來陪 Vera → flags=['flag_vera_stay'] stats={'rel_vera': 2, 'trust': 1}
  - `C_vera_crisis_work` 趕通告：先顧打歌與形象 → flags=['flag_vera_workfirst'] stats={'music': 1, 'rel_vera': -2}

### R_vera_ending　造型間收工　〔ending〕
- when／setting：1992｜造型間收工
- eraTag／artId／conflict：`era_1992_finale`／`rom_vera_ending`／None
- cast：阿偉、Vera；beats=5
- synopsis：阿偉與 Vera 在造型間收工後獨處。兩人回望過去幾年的點滴，阿偉可以選擇確定關係，還是保持現狀。
- choices：
  - `C_vera_ending_he` 確定關係：與 Vera 一起走下去 → flags=['flag_vera_he', 'flag_vera_commit'] stats={'rel_vera': 3}
  - `C_vera_ending_be` 保持距離：專注事業，感情隨緣 → flags=['flag_vera_be'] stats={'rel_vera': -2}

## 林曉晴（`hiu`）

### R_hiu_meet　廠景休息角初遇　〔meet〕
- when／setting：1988春｜廠景休息角
- eraTag／artId／conflict：`era_1988_spring_grassroot`／`rom_hiu_meet`／None
- cast：阿偉、林曉晴；beats=5
- synopsis：在廠景休息角，我與同期臨記林曉晴初次碰面。她主動搭話，透露一些通告情報，似乎想交換消息。
- choices：
  - `C_hiu_meet_a` 交換情報 → flags=['hiu_meet_exchange'] stats={'rel_hiu': 1}
  - `C_hiu_meet_b` 客氣疏離 → flags=['hiu_meet_distant'] stats={'rel_hiu': 0}

### R_hiu_push1　茶餐廳互相帶通告　〔push〕
- when／setting：1988秋｜茶餐廳／廠景後門
- eraTag／artId／conflict：`era_1988_autumn_unit`／`rom_hiu_push1`／None
- cast：阿偉、林曉晴；beats=5
- synopsis：我與林曉晴在茶餐廳碰面，互相分享通告情報。她提到一個試鏡機會，但名額有限，我們之間出現微妙的競爭。
- choices：
  - `C_hiu_push1_a` 幫她讓位／報料 → flags=['hiu_push1_help'] stats={'rel_hiu': 2}
  - `C_hiu_push1_b` 自己先搶 → flags=['hiu_push1_self'] stats={'rel_hiu': -1, 'standing': 1}

### R_hiu_push2　夜班殺青後　〔push〕
- when／setting：1989｜夜班殺青後
- eraTag／artId／conflict：`era_1989_summer`／`rom_hiu_push2`／None
- cast：阿偉、林曉晴；beats=5
- synopsis：夜班殺青後，我與林曉晴一起收拾東西，氣氛輕鬆。她主動聊起私人生活，關係似乎可以更進一步。
- choices：
  - `C_hiu_push2_a` 約下次 → flags=['hiu_push2_date'] stats={'rel_hiu': 2}
  - `C_hiu_push2_b` 只當同期 → flags=['hiu_push2_friend'] stats={'rel_hiu': 0}

### R_hiu_crisis　同場搶通告　〔crisis〕
- when／setting：1991｜同場搶通告／試鏡廊
- eraTag／artId／conflict：`era_1991_summer_anni`／`rom_hiu_crisis`／None
- cast：阿偉、林曉晴；beats=5
- synopsis：在試鏡廊，我與林曉晴同時爭取一個重要的角色。兩人面對直接競爭，關係受到考驗。
- choices：
  - `C_hiu_crisis_a` 成全她 → flags=['hiu_crisis_yield'] stats={'rel_hiu': 2, 'standing': -1}
  - `C_hiu_crisis_b` 硬搶同場 → flags=['hiu_crisis_fight'] stats={'rel_hiu': -2, 'standing': 2}

### R_hiu_ending　廠景天台　〔ending〕
- when／setting：1992｜廠景天台
- eraTag／artId／conflict：`era_1992_finale`／`rom_hiu_ending`／None
- cast：阿偉、林曉晴；beats=5
- synopsis：在廠景天台，我與林曉晴回顧過去幾年的點滴，決定是否要確立關係。
- choices：
  - `C_hiu_ending_he` 確定關係：同行情侶 → flags=['flag_hiu_he', 'flag_hiu_commit'] stats={'rel_hiu': 3}
  - `C_hiu_ending_be` 保持距離：漸行漸遠 → flags=['flag_hiu_be'] stats={'rel_hiu': -2}

## 周采兒（`choi`）

### R_choi_meet　片場採訪角的小訪　〔meet〕
- when／setting：1988夏｜片場採訪角（C5小訪前後）
- eraTag／artId／conflict：`era_1988_summer_anni`／`rom_choi_meet`／None
- cast：阿偉、周采兒；beats=5
- synopsis：在片場採訪角，記者周采兒初次訪問我。她問得直接，我選擇坦誠回答還是官腔回應，影響她對我的印象。
- choices：
  - `R_choi_meet_a` 坦誠回答：分享真實想法 → flags=['choi_meet_honest'] stats={'rel_choi': 1, 'fame': 1}
  - `R_choi_meet_b` 官腔保護：只說標準答案 → flags=['choi_meet_official'] stats={'rel_choi': 0, 'fame': 0}

### R_choi_push1　茶記的爆料交換　〔push〕
- when／setting：1989｜茶記／報館附近
- eraTag／artId／conflict：`era_1989_spring`／`rom_choi_push1`／None
- cast：阿偉、周采兒；beats=5
- synopsis：周采兒約我在茶記見面，希望我提供一些獨家消息。我可以在不傷害他人的前提下給她方向，或拒絕提供。
- choices：
  - `R_choi_push1_a` 給她獨家方向：在不傷害人的前提下提供線索 → flags=['choi_give_tip'] stats={'rel_choi': 2, 'fame': 1}
  - `R_choi_push1_b` 拒絕提供：保護劇組聲譽 → flags=['choi_refuse_tip'] stats={'rel_choi': 0, 'standing': 1}

### R_choi_push2　私下晚餐的試探　〔push〕
- when／setting：1989｜私下晚餐
- eraTag／artId／conflict：`era_1989_autumn`／`rom_choi_push2`／None
- cast：阿偉、周采兒；beats=5
- synopsis：周采兒約我私下晚餐，氣氛曖昧。我可以把這次當作真正的約會，或者當作採訪的延續。
- choices：
  - `R_choi_push2_a` 當真約會：放下記者與受訪者的身份 → flags=['choi_real_date'] stats={'rel_choi': 2}
  - `R_choi_push2_b` 當採訪延續：保持專業距離 → flags=['choi_keep_professional'] stats={'rel_choi': 0}

### R_choi_crisis　周刊會議室的抉擇　〔crisis〕
- when／setting：1991冬｜周刊會議室（對齊C13真假緋聞）
- eraTag／artId／conflict：`era_1991_winter_gossip`／`rom_choi_crisis`／None
- cast：阿偉、周采兒、周刊編輯；beats=5
- synopsis：周刊收到緋聞消息，編輯要求周采兒表態。我必須決定公開真情還是公關切割，影響我與她的關係及公眾形象。
- choices：
  - `R_choi_crisis_a` 公開真情：承認關係，共同面對 → flags=['flag_public_romance'] stats={'rel_choi': 2, 'fame': 1}
  - `R_choi_crisis_b` 公關切割：否認關係，保護事業 → flags=['choi_deny_romance'] stats={'rel_choi': -2, 'fame': 0}

### R_choi_ending　報館後巷的結局　〔ending〕
- when／setting：1992｜報館後巷
- eraTag／artId／conflict：`era_1992_finale`／`rom_choi_ending`／None
- cast：阿偉、周采兒；beats=6
- synopsis：在報館後巷，我與周采兒的關係迎來結局。可以選擇承諾未來，或分道揚鑣。
- choices：
  - `C_choi_ending_he` 承諾未來：低調真情 → flags=['flag_choi_he', 'flag_choi_commit'] stats={'rel_choi': 3}
  - `C_choi_ending_be` 分道揚鑣：公關犧牲感情 → flags=['flag_choi_be'] stats={'rel_choi': -2}

---
## QA

- 禁用詞／粵口語：pass
- DeepSeek：vera/hiu/choi draft + hiu/choi expand；均長 ~26.1
- 15 節：每線 meet→push×2→crisis→ending
- 未出圖；未動 gigs_1988

