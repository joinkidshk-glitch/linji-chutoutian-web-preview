# Phase4 Detail C12–C15 v1

> **狀態：** DeepSeek 分批＋C15 家人對白潤稿＋HK lexicon；**未出圖**。  
> **成品：** `story_detail_phase4_c12c15.json`

---

## C12　賀歲搶位 vs 關係危機
- **when／setting：** 1991夏 / W80-84｜星河電視台高層會議室／賀歲檔籌備
- **eraTag／artId／conflict：** `era_1991_summer_anni`／`story_c12`／T4
- **cast：** 阿偉、高文瀚、約會對象、高俊傑
- **synopsis：** 1991年夏，賀歲檔與台慶級位置開搶。高文瀚要阿偉連軸綵排守住位置，高俊傑亦在爭同一席；同一週，高好感的約會對象出狀況，要他現身。事業搶位與關係危機撞在一起。
- **beats：** 7 段；speakers=['約會對象', '阿偉', '高文瀚']
- **choices（2）：**
  - `C12_a` 全力搶位：連軸綵排，把賀歲位置拿到手
    - flags=['anni91_seize', 'love_crisis']
    - stats={'standing': 2, 'fame': 1, 'rel_partner': -2}
    - notes：你守住賀歲位置，standing 與 fame 上升；當前約會線 rel_partner 下滑，觸發愛情危機。
  - `C12_b` 顧好關係：推掉部分綵排，先處理對方的事
    - flags=['anni91_tend']
    - stats={'standing': 0, 'fame': 0, 'rel_partner': 2}
    - notes：你顧好關係，rel_partner 上升；賀歲搶位讓步，standing 不升。
- **flags_written：** `anni91_seize`, `anni91_tend`, `love_crisis`

## C13　緋聞公關真假
- **when／setting：** 1991冬 / W92-96｜虛構娛樂周刊採訪室／公關會議室
- **eraTag／artId／conflict：** `era_1991_winter_gossip`／`story_c13`／None
- **cast：** 阿偉、周采兒、關海媚
- **synopsis：** 1991年冬，虛構娛樂周刊已寫好緋聞草稿。周采兒要阿偉表態；關海媚提醒頭條是雙刃。承認、否認或模糊帶過，每條路都改寫形象與關係。
- **beats：** 7 段；speakers=['周采兒', '關海媚', '阿偉']
- **choices（3）：**
  - `C13_a` 承認關係：公開表態，站在對方身邊
    - flags=['gossip_admit', 'flag_public_romance']
    - stats={'rel_choi': 1, 'fame': 2, 'rel_mei': 1}
    - notes：公開承認；fame 升，rel_choi／rel_mei 微升，公開戀愛壓力開始。
  - `C13_b` 否認緋聞：劃清界線，保住事業形象
    - flags=['gossip_deny']
    - stats={'rel_choi': -1, 'fame': 0, 'rel_mei': -1}
    - notes：對外否認；形象暫穩，但 rel_choi／rel_mei 下滑。
  - `C13_c` 模糊帶過：不承認也不否認，暫不答覆
    - flags=['gossip_vague']
    - stats={'rel_choi': 0, 'fame': 1, 'rel_mei': 0}
    - notes：態度模糊；fame 微升，兩線關係不加不減，後續仍可被追問。
- **flags_written：** `gossip_admit`, `gossip_deny`, `gossip_vague`, `flag_public_romance`

## C14　徐寶珊尊重或包養
- **when／setting：** 1991秋 / W88-90｜資本場宴會／廣告客戶包廂
- **eraTag／artId／conflict：** `era_1991_autumn_capital`／`story_c14`／None
- **cast：** 阿偉、徐寶珊
- **synopsis：** 1991年秋，資本場宴會上，徐寶珊提出代談大品牌廣告與檔期護航。條件可以聽成互相尊重的合作，也可以聽成依賴式金援。阿偉要決定怎麼接。
- **beats：** 7 段；speakers=['徐寶珊', '阿偉']
- **choices（3）：**
  - `C14_a` 尊重合作：把條件講清楚，平等簽約
    - flags=['flag_bao_respect']
    - stats={'rel_xu': 2, 'wealth': 1, 'standing': 1}
    - notes：平等合作；rel_xu／wealth／standing 上升，寫入 flag_bao_respect。
  - `C14_b` 接受依賴結構：全盤交由她安排
    - flags=['flag_bao_depend']
    - stats={'rel_xu': 1, 'wealth': 3, 'standing': -1}
    - notes：金援依賴加深；wealth 大升，standing 微跌，寫入 flag_bao_depend。
  - `C14_c` 拒絕：不靠金援，自己談通告
    - flags=['flag_bao_refuse']
    - stats={'rel_xu': -1, 'wealth': 0, 'standing': 1}
    - notes：拒絕金援結構；rel_xu 下滑，standing 微升，自主通告路線。
- **flags_written：** `flag_bao_respect`, `flag_bao_depend`, `flag_bao_refuse`

## C15　藍若曦聯姻逼退圈
- **when／setting：** 1991春 / W72-76｜豪門宴會側廳（含蓄，勿政治口號）
- **eraTag／artId／conflict：** `era_1991_spring_family`／`story_c15`／None
- **cast：** 阿偉、藍若曦、藍父
- **synopsis：** 1991年春，藍家在宴會側廳把聯姻與退圈暗示攤開。藍若曦不想走，問阿偉站哪邊：助她抗、成全家族，還是袖手旁觀。
- **beats：** 8 段；speakers=['藍父', '藍若曦', '阿偉']
- **choices（3）：**
  - `C15_a` 助抗：陪她向家族爭取
    - flags=['flag_family_help', 'flag_family_marriage']
    - stats={'rel_lan': 3, 'fame': -1, 'standing': 0}
    - notes：你陪她抗聯姻壓力；rel_lan 大升，fame 微跌，寫入 flag_family_help。
  - `C15_b` 成全：尊重她聽從家族安排
    - flags=['flag_family_yield', 'flag_family_marriage']
    - stats={'rel_lan': 1, 'fame': 0}
    - notes：你選擇成全；rel_lan 微升，路線分開，寫入 flag_family_yield。
  - `C15_c` 袖手：不表態，保持距離
    - flags=['flag_family_standby', 'flag_family_marriage']
    - stats={'rel_lan': -2, 'fame': 0}
    - notes：你袖手；rel_lan 下滑，寫入 flag_family_standby。
- **flags_written：** `flag_family_help`, `flag_family_yield`, `flag_family_standby`, `flag_family_marriage`

---
## QA

- 禁用詞／粵口語粒子：body pass
- DeepSeek：C12C13 + C14C15 + C15_family_polish（`deepseek-chat`）
- 均長約 23.6 字；beat_counts={'C12': 7, 'C13': 7, 'C14': 7, 'C15': 8}
- effects：全部含 flags + 數字 stats（含 rel_*）
- 配角對白：C13 周采兒／關海媚；C14 徐寶珊；C15 藍家長
- 未出圖；未動 gigs_1988

