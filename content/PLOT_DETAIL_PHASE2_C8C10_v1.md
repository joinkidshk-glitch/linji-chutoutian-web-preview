# Phase2 Detail C8–C10 v1

> **狀態：** DeepSeek＋HK lexicon＋書面潤飾；**未出圖**。  
> **成品：** `story_detail_phase2_c8c10.json`  
> **合併：** `story_detail_phase1_to_c10.json`

---

## C8　商業片 vs 文藝線
- **when／setting：** 1989春 / W20-24｜星河電視台會議室／獨立片廠茶水間
- **eraTag／artId／conflict：** `era_1989_spring_quiet`／`story_c8`／None
- **cast：** 阿偉、高文瀚、張子駿、何生
- **synopsis：** 同一個下午，阿偉在星河電視台會議室收到高文瀚的商業片與台慶曝光邀約，隨後在獨立片廠茶水間又遇上張子駿的低片酬文藝磨戲邀請。兩邊通告撞期，他只能先選一條路。
- **beats：** 7 段（均長約 17.8 字）
- **choices（2）：**
  - `C8_a` 跟高文瀚走商業線 → flags=['route_commercial'] stats={'fame': 1, 'wealth': 1}
  - `C8_b` 跟張子駿走文藝線 → flags=['route_indie'] stats={'craft': 2}
- **flags_written：** `route_commercial`, `route_indie`

## C9　藍若曦擋狗仔後
- **when／setting：** 1989夏秋 / W28-32｜停車場後巷／車上（狗仔剛散）
- **eraTag／artId／conflict：** `era_1989_summer_literary`／`story_c9`／None
- **cast：** 阿偉、藍若曦
- **synopsis：** 狗仔在停車場追問阿偉與藍若曦的關係，藍若曦搶先擋住問題，拉阿偉上車。車門關上後，兩人要在認愛、切割與模糊之間定調；無論選哪邊，明日娛樂周刊的標題都不會客氣。
- **beats：** 8 段（均長約 25.9 字）
- **choices（3）：**
  - `C9_a` 認愛：明日一起見記者，公開承認關係 → flags=['flag_public_romance', 'lan_confess'] stats={'rel_lan': 2, 'fame': 1}
  - `C9_b` 切割：對外統一口徑，只說是合作同事 → flags=['lan_cut'] stats={'rel_lan': -1}
  - `C9_c` 模糊：不認也不否認，先暫不答覆記者 → flags=['lan_blur'] stats={'rel_lan': 1}
- **flags_written：** `flag_public_romance`, `lan_blur`, `lan_confess`, `lan_cut`

## C10　台慶位 vs 陪伴
- **when／setting：** 1989冬 / W40-44｜星河電視台台慶後台化妝間／走廊
- **eraTag／artId／conflict：** `era_1989_winter_anniversary`／`story_c10`／T2
- **cast：** 阿偉、高俊傑、何生
- **synopsis：** 台慶夜後台，高俊傑為爭取演出黃金時段的位置，與阿偉正面交鋒。阿偉同時記掛著與伴侶的約會，要在事業與陪伴之間取捨。何生從旁觀察，暗示機會難得。
- **beats：** 7 段（均長約 28.2 字）
- **choices（3）：**
  - `C10_a` 硬搶：守住台慶位置，不退讓 → flags=['anni_seize'] stats={'standing': 2}
  - `C10_b` 讓位：退一步換人情，趕去赴約 → flags=['anni_yield'] stats={}
  - `C10_c` 協調：跟高俊傑商量分工，各讓一步 → flags=['anni_mediate'] stats={'standing': 1}
- **flags_written：** `anni_mediate`, `anni_seize`, `anni_yield`

---
## QA

- 自造縮寫與真實台名掃描 → 正文 0
- 殘餘口語已再清一輪
- 未出圖；未動 gigs_1988；無完整 HE

