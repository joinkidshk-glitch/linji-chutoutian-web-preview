# Phase5 Detail C16–C17 v1

> **狀態：** DeepSeek＋HK lexicon；E01–E10 名稱強制鎖死；**未出圖**。  
> **成品：** `story_detail_phase5_c16c17.json`

---

## C16　舊底片交付
- **when／setting：** 1992夏 / W100-104｜舊片場倉庫／金九休息角
- **eraTag／artId／conflict：** `era_1992_summer_legacy`／`story_c16`／None
- **cast：** 阿偉、金九
- **synopsis：** 舊片場倉庫清拆在即，金九把一卷保存多年的舊底片交到阿偉手上，那是早年臨記的紀錄，也是他半生人脈與心血的起點。金九談起傳承與回望，阿偉要決定接不接這份重量。
- **beats：** 7；speakers=['金九', '阿偉']
- **choices（2）：**
  - `C16_a` 接下舊底片：記住臨記的來路
    - flags=['flag_legacy_film']
    - stats={'craft': 1, 'standing': 1}
    - notes：你接下金九的舊底片與人情；craft／standing 微升，寫入 flag_legacy_film。
  - `C16_b` 婉拒不接：先顧好眼前生計
    - flags=['flag_legacy_refuse']
    - stats={'craft': 0, 'standing': 0}
    - notes：你婉拒；flag_legacy_refuse。金九略失落，傳承線未開。
- **flags_written：** `flag_legacy_film`, `flag_legacy_refuse`

## C17　最終定位／結算
- **when／setting：** 1992收束 / W105-108｜星河電視台會議室／劇本堆與片場晨光
- **eraTag／artId／conflict：** `era_1992_finale`／`story_c17`／None
- **cast：** 阿偉、何生、張子駿
- **synopsis：** 1992年收束。何生與張子駿把幕前、幕後、雙線意向攤開；阿偉在十檔事業結局之中鎖定一條路。愛情 HE／BE 另表並存，本節只鎖事業。
- **beats：** 8；speakers=['何生', '張子駿', '阿偉']
- **choices（10）：**
  - `C17_e01` E01　穩陣男演員
    - flags=['ending_e01', 'career_lock']
    - stats={'standing': 1, 'fame': 1}
    - notes：少醜聞、何生信任；穩定有薪向。愛情結局另表並存。
  - `C17_e02` E02　有名有實
    - flags=['ending_e02', 'career_lock']
    - stats={'standing': 2, 'fame': 2}
    - notes：台慶／賀歲級曝光；高人氣＋高聲望。愛情結局另表並存。
  - `C17_e03` E03　評審眼熟
    - flags=['ending_e03', 'career_lock']
    - stats={'craft': 2, 'fame': 0}
    - notes：張子駿／文藝線；craft 高。愛情結局另表並存。
  - `C17_e04` E04　跨界紅人
    - flags=['ending_e04', 'career_lock']
    - stats={'fame': 2, 'music': 2}
    - notes：打歌／廣告多棲。愛情結局另表並存。
  - `C17_e05` E05　動作班底
    - flags=['ending_e05', 'career_lock']
    - stats={'craft': 1, 'standing': 1}
    - notes：方小龍線／動作向。愛情結局另表並存。
  - `C17_e06` E06　海外發展
    - flags=['ending_e06', 'career_lock']
    - stats={'fame': 1, 'wealth': 1}
    - notes：含蓄離合／海外機會。愛情結局另表並存。
  - `C17_e07` E07　金援靠山
    - flags=['ending_e07', 'career_lock']
    - stats={'wealth': 3, 'standing': 0}
    - notes：徐寶珊金援高；wealth 高、聲望可議。愛情結局另表並存。
  - `C17_e08` E08　有錢但空
    - flags=['ending_e08', 'career_lock']
    - stats={'wealth': 3, 'standing': -1}
    - notes：錢高、聲望歪。愛情結局另表並存。
  - `C17_e09` E09　淡出守住
    - flags=['ending_e09', 'career_lock']
    - stats={'rel_partner': 1, 'fame': 0}
    - notes：關係優先、未大紅未崩。愛情結局另表並存。
  - `C17_e10` E10　未出頭
    - flags=['ending_e10', 'career_lock']
    - stats={'fame': -1, 'standing': -1}
    - notes：四年未穩或崩盤向。愛情結局另表並存。
- **orientation_hint：** ['幕前', '幕後', '雙線']
- **endings_catalog：** E01 穩陣男演員、E02 有名有實、E03 評審眼熟、E04 跨界紅人、E05 動作班底、E06 海外發展、E07 金援靠山、E08 有錢但空、E09 淡出守住、E10 未出頭
- **flags_written：** `ending_e01`, `ending_e02`, `ending_e03`, `ending_e04`, `ending_e05`, `ending_e06`, `ending_e07`, `ending_e08`, `ending_e09`, `ending_e10`, `career_lock`

---
## QA

- 禁用詞／粵口語：body pass
- DeepSeek：C16+C17 deepseek-chat；均長 ~30.5
- E01–E10 名稱與 UNLOCK／主計劃一字不差
- 愛情另計並存；未出圖；未動 gigs_1988

