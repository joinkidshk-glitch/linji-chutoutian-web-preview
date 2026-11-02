# Romance Detail 藍若曦／徐寶珊 v1（steering 修訂）

> **SOFT_NITS_FIX_v1（2026-11-02）：**  
> - `conflict` 慣例：T 碼→`conflict`；C 碼→`linksMain`（藍 C9／C15；徐 T6＋C14）。  
> - 藍 meet synopsis 補一句鋪到 push1 合唱。  
> - `R_tang_meet_stub`：偶遇只寫 `flag_tang_met`＋`rel_tang`；正式開閘見 `R_tang_meet`。


> **狀態：** Pack2 按 steering 重潤：`cast_main` 性格、`flag_<line>_*`、無阿偉「我」對白、`C_*` choice id、連 C9／C14／C15／T6。**未出圖**。  
> **成品：** `story_detail_romance_lan_xu.json`

---

## 藍若曦

### R_lan_meet　唱片店外的傘　〔meet〕
- when／setting：1989｜旺角唱片店門外，突然下起大雨，狗仔隊在對街守候。
- speakers：['藍若曦']；pcSilent=True
- links：None
- synopsis：阿偉為避雨衝入唱片店，撞見藍若曦被狗仔隊追訪。她情急之下躲到他傘下，阿偉順勢掩護她離開。
- choices：
  - `C_lan_meet_warm` 溫柔接住：護她離開鏡頭 → ['flag_lan_met_warm'] {'rel_lan': 1}
  - `C_lan_meet_cool` 客氣疏離：只盡同事本分 → ['flag_lan_met_cool'] {'rel_lan': 0}

### R_lan_push1　錄音室的半首歌　〔push〕
- when／setting：1989秋｜星河電視台錄音室，兩人為台慶合唱環節綵排。
- speakers：['藍若曦']；pcSilent=True
- links：None
- synopsis：監製要求兩人合唱半首歌，阿偉緊張走音，藍若曦耐心教他咬字。
- choices：
  - `C_lan_push1_serious` 認真合唱：投入感情 → ['flag_lan_sang_together'] {'rel_lan': 2, 'music': 1}
  - `C_lan_push1_work` 只當工作：唱完即止 → ['flag_lan_work_only'] {'rel_lan': 0, 'music': 0}

### R_lan_push2　假戲與真話　〔push〕
- when／setting：1989｜電視台化妝間外走廊，狗仔隊收到風聲指兩人緋聞。
- speakers：['藍若曦']；pcSilent=True
- links：['C9']
- synopsis：公司建議兩人以情侶檔姿態出席活動，藍若曦猶豫，阿偉要決定是否護她。
- choices：
  - `C_lan_push2_protect` 護她：願意扛公開壓力（連 C9） → ['flag_lan_protected'] {'rel_lan': 2, 'fame': -1}
  - `C_lan_push2_distance` 劃清同事：不認曖昧（連 C9） → ['flag_lan_colleague'] {'rel_lan': 0}

### R_lan_crisis　豪門側廳的條件　〔crisis〕
- when／setting：1991春｜豪門宴會側廳，藍父與聯姻對象在場。
- speakers：['藍父', '藍若曦']；pcSilent=True
- links：['C15']
- synopsis：藍父要求藍若曦與豪門子弟訂婚，以換取家族生意支持。藍若曦向阿偉求助。
- choices：
  - `C_lan_crisis_help` 助抗：陪她面對家族（連 C15） → ['flag_lan_help', 'flag_family_help', 'flag_family_marriage'] {'rel_lan': 2, 'fame': -1}
  - `C_lan_crisis_stepback` 成全／退讓：勸她考慮家族（連 C15） → ['flag_lan_stepback', 'flag_family_marriage'] {'rel_lan': -1}

### R_lan_ending　晨光與登機證　〔ending〕
- when／setting：1992｜片場晨光，或機場離境大堂。
- speakers：['藍若曦']；pcSilent=True
- links：None
- synopsis：藍若曦決定是否為愛情留下，還是退圈離開。阿偉要作出最後表態。
- choices：
  - `C_lan_ending_he` HE：抗聯姻，一起走下去 → ['flag_lan_he', 'flag_lan_commit'] {'rel_lan': 3}
  - `C_lan_ending_be` BE：成全離開或疏離 → ['flag_lan_be'] {'rel_lan': -2}

## 徐寶珊

### R_xu_meet　春茗初遇　〔meet〕
- when／setting：1990春｜星河電視台春茗酒會，廣告客戶雲集，阿偉以臨時演員身份在場協助佈景。
- speakers：['徐寶珊']；pcSilent=True
- links：None
- synopsis：阿偉在春茗酒會搬運道具時，不慎撞到剛好經過的徐寶珊。徐寶珊是廣告界有名的女強人，正與客戶應酬。阿偉連忙道歉，徐寶珊見他手腳勤快，順口提點幾句。
- choices：
  - `C_xu_meet_polite` 有禮接招：不卑不亢 → ['flag_xu_met_polite'] {'rel_xu': 1, 'craft': 1}
  - `C_xu_meet_distance` 保持距離：不攀談 → ['flag_xu_met_distance'] {'rel_xu': 0, 'standing': 1}

### R_xu_push1　商場活動的試探　〔push〕
- when／setting：1990｜大型商場廣告活動，徐寶珊的公司是主要贊助商，阿偉獲派做現場臨時演員統籌。
- speakers：['徐寶珊']；pcSilent=True
- links：None
- synopsis：活動結束後，徐寶珊主動找阿偉，讚他現場應變快，並暗示可以投資幫他開設製作公司，條件是阿偉要跟她合作。
- choices：
  - `C_xu_push1_accept` 願意談合作：聽金援條件 → ['flag_xu_coop_talk'] {'rel_xu': 2, 'wealth': 1}
  - `C_xu_push1_decline` 婉拒口風：想先靠自己 → ['flag_xu_coop_decline'] {'rel_xu': 0, 'standing': 1}

### R_xu_push2　私人飯局的距離　〔push〕
- when／setting：1991｜高級私人會所飯局，徐寶珊約阿偉單獨見面，說要介紹幾位重要客戶給他認識。
- speakers：['徐寶珊']；pcSilent=True
- links：None
- synopsis：飯局上徐寶珊談笑風生，介紹人脈之餘，也問起阿偉的私生活。阿偉察覺徐寶珊對自己不止公事上的興趣。
- choices：
  - `C_xu_push2_open` 打開私人一面 → ['flag_xu_personal_open'] {'rel_xu': 2}
  - `C_xu_push2_business` 只談生意 → ['flag_xu_business_only'] {'rel_xu': 1, 'standing': 1}

### R_xu_crisis　包廂裡的條件　〔crisis〕
- when／setting：1991｜資本場私人包廂，徐寶珊約阿偉見面，直接提出更緊密的合作條件，暗示可以包起他的事業。
- speakers：['徐寶珊']；pcSilent=True
- links：['C14', 'T6']
- synopsis：徐寶珊開門見山，說可以全力支持阿偉的事業，但條件是他要成為她的人。阿偉要決定接受尊重合作，還是依賴這條捷徑。
- choices：
  - `C_xu_crisis_respect` 尊重合作（連 C14／T6） → ['flag_xu_respect', 'flag_bao_respect'] {'rel_xu': 2, 'wealth': 1, 'standing': 1}
  - `C_xu_crisis_depend` 依賴結構（連 C14／T6） → ['flag_xu_depend', 'flag_bao_depend'] {'rel_xu': 1, 'wealth': 3, 'standing': -1}
  - `C_xu_crisis_refuse` 拒絕（連 C14／T6） → ['flag_xu_refuse', 'flag_bao_refuse'] {'rel_xu': -1, 'standing': 1}

### R_xu_ending　燈光之後的抉擇　〔ending〕
- when／setting：1992｜資本場合大型晚宴結束後，後台走廊只剩阿偉與徐寶珊，兩人終於要面對關係的定局。
- speakers：['徐寶珊']；pcSilent=True
- links：None
- synopsis：晚宴曲終人散，徐寶珊問阿偉接下來的路想怎樣走。阿偉要決定是否與她建立平等伴侶關係，還是讓這段關係走向決裂或冷淡。
- choices：
  - `C_xu_ending_he` HE：平等伴侶 → ['flag_xu_he', 'flag_xu_commit'] {'rel_xu': 3, 'standing': 1}
  - `C_xu_ending_be` BE：依賴決裂或冷淡 → ['flag_xu_be'] {'rel_xu': -2, 'wealth': -1}

## 鄧麗萍（stub｜supersededBy `R_tang_meet`）

> 正式完整線：`PLOT_DETAIL_ROMANCE_TANG_v1.md`／`story_detail_romance_tang.json`。本 stub 保留相容。


### R_tang_meet_stub　公關公司偶遇鄧麗萍　〔meet〕
- when／setting：1991｜公關公司會議室
- speakers：['鄧麗萍']；pcSilent=True
- links：None
- synopsis：阿偉到公關公司洽談臨記工作，在會議室遇見鄧麗萍。二人短暫交談，交換聯絡與否，將影響日後感情線能否正式開啟。此節為佔位短認識，正式開線需同時滿足 flag_tang_open 及 rel_tang 達到門檻。
- choices：
  - `C_tang_meet_keep_contact` 留下聯絡：寫入 flag_tang_open → ['flag_tang_open'] {'rel_tang': 1}
  - `C_tang_meet_hold_back` 先不深交 → [] {'rel_tang': 0}

---
## QA

- 禁用詞／粵口語／阿偉對白：pass
- 均長 ~29.0；nodes=11
- 未出圖；未動 gigs_1988

