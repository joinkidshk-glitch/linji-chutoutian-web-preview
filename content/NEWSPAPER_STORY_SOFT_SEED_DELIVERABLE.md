# 交貨｜劇情×報紙 Soft 文案種子 v1（Soft tip #102）

> 日期：2026-11-08（Asia/Hong_Kong）  
> Soft≠PASS｜**唔 tip LIVE**｜唔抬 `?v=`／SAVE｜出圖 HOLD｜89–92 HOLD  
> PLAN：`/workspace/linji-playtest/PLAN_STORY_NEWSPAPER_LOOP_SOFT.md`  
> 基線：Soft tip #101 main `28903874`／softRev=s101；產品 `?v=20a10`；SAVE `starVolunteer_map_v19w`  
> 文案：qwen3.7-max｜raw：`linji-chutoutian-web-preview/content/_qwen_raw_newspaper_story_soft/`（mirror playtest）

## 定位對齊 PLAN
| PLAN 點 | 本包 |
|---|---|
| 報紙＝公開娛樂版；傳聞＝圈內耳語 | stub 主文＝報紙；`rumorEcho`＝可選耳語 |
| 劇情選擇後 enqueue → 次日朝早 | meta.timing 註記；引擎＝iOS（非本包） |
| §5.1 14 則 id | story_highlight 8＋story_mixed 6＝**14** |
| 周刊誠實 +1～+2；C5 dodge＝0；C3 hard 可−1 | 見則數表 |
| 玩家面「聲望」；禁「聲量」「噂」 | 禁詞自檢＝0 |
| Soft tip 種子；唔 tip LIVE | softStatus≠PASS；softTip=102 |
| R_hiu distant | skip；無模板 |

## 則數
| bucket | 則數 |
|---|---:|
| story_highlight | 8 |
| story_mixed | 6 |
| **合計** | **14** |

## 則數表（id／eventKey／fameDelta／tone）
| id | bucket | eventKey | choiceFlag | tone | fameDelta | paperName | headline |
|---|---|---|---|---|---:|---|---|
| np_story_c1_tv_01 | story_highlight | `story:C1:route_tv` | `route_tv` | pos | 1 | 電視週刊 | 電視城臨記班底添新血 阿偉獲青睞 |
| np_story_c1_film_01 | story_highlight | `story:C1:route_film` | `route_film` | pos | 1 | 娛樂快報 | 阿偉投身電影圈 展開廠景散工生涯 |
| np_story_c2_network_01 | story_highlight | `story:C2:network` | `flag_network_stay` | pos | 2 | 星河娛樂版 | 臨記阿偉廣結人緣 留廠景聽圈內故事 |
| np_story_c2_hustle_01 | story_highlight | `story:C2:hustle` | `flag_hustle_board` | pos | 1 | 電視週刊 | 阿偉勤力跑通告 準時報到獲讚賞 |
| np_story_c4_harsh_01 | story_highlight | `story:C4:take_harsh` | `flag_take_harsh_gig` | pos | 2 | 娛樂快報 | 何生安排通宵通告 阿偉頂硬上獲好評 |
| np_story_c5_honest_01 | story_highlight | `story:C5:honest` | `choi_honest` | pos | 3 | 電視週刊 | 采兒小訪阿偉 坦率回應敏感提問 |
| np_story_hiu_exchange_01 | story_highlight | `story:R_hiu_meet:exchange` | `flag_hiu_meet_exchange` | pos | 1 | 星河娛樂版 | 廠景休息角交流 阿偉與曉交換情報 |
| np_story_choi_weekly_honest_01 | story_highlight | `story:R_choi_meet:honest` | `flag_choi_meet_honest` | pos | 2 | 電視週刊 | 周刊專訪阿偉 坦誠分享臨記點滴 |
| np_story_c3_hard_01 | story_mixed | `story:C3:hard` | `rival_gao_hard` | mixed | -1 | 星河娛樂版 | 廠景爆發爭執 阿偉與對手火藥味濃 |
| np_story_c3_endure_01 | story_mixed | `story:C3:endure` | `rival_gao_endure` | mixed | 0 | 娛樂快報 | 顧全大局 阿偉片場忍讓免傷和氣 |
| np_story_c4_refuse_01 | story_mixed | `story:C4:refuse` | `flag_refuse_gig_with_ho` | mixed | -1 | 娛樂快報 | 拒接苛刻通告 阿偉與經紀何生傳分歧 |
| np_story_c5_spin_01 | story_mixed | `story:C5:spin` | `choi_spin` | mixed | 1 | 電視週刊 | 采兒小訪 阿偉圓滑應對滴水不漏 |
| np_story_c5_dodge_01 | story_mixed | `story:C5:dodge` | `choi_dodge` | mixed | 0 | 星河娛樂版 | 避談敏感話題 阿偉借故離開採訪 |
| np_story_choi_weekly_official_01 | story_mixed | `story:R_choi_meet:official` | `flag_choi_meet_official` | mixed | 0 | 電視週刊 | 電視週刊訪問 阿偉官腔回應顯謹慎 |

## 檔清單＋sha8
| 檔 | sha8 |
|---|---|
| `linji-chutoutian-web-preview/content/STUB_NEWSPAPER_STORY_SOFT_v1.json` | `4dabcb42` |
| `star-volunteer-web/content/STUB_NEWSPAPER_STORY_SOFT_v1.json` | `4dabcb42` |
| `…/SCHEMA_NEWSPAPER_STORY_SOFT_v1.json`（preview＝sv） | `c7d266d4` |
| `…/NOTES_NEWSPAPER_STORY_SEED_v1.md`（preview＝sv） | `ce539281` |
| playtest 本交貨稿 | （本檔；executor 回報 sha） |
| qwen raw dir | `_qwen_raw_newspaper_story_soft/`（preview＋playtest mirror） |

## 禁詞自檢（玩家面 headline／dek／clipLabel／rumorEcho／paperName）
| 項 | 次數 |
|---|---:|
| 聲量／幕前聲量 | 0 |
| 噂 | 0 |
| 真藝名（抽樣：何生／采兒／曉＝局內） | 0 |
| 真報紙長弧 | 0 |

## 完整玩家面稿表
### story_highlight
| id | paperName | headline | dek | fameDelta | clipLabel | rumorEcho | boardScentTag |
|---|---|---|---|---:|---|---|---|
| np_story_c1_tv_01 | 電視週刊 | 電視城臨記班底添新血 阿偉獲青睞 | 新生代臨時演員阿偉正式加入電視城班底，展現演藝潛力。 | 1 | 電視城臨記班底添新血 | 聽講電視城個組頭覺得阿偉幾聽話，打算帶住佢跑多幾個廠景。 | tv_extra |
| np_story_c1_film_01 | 娛樂快報 | 阿偉投身電影圈 展開廠景散工生涯 | 新晉臨時演員阿偉選擇電影路線，積極參與各類廠景拍攝。 | 1 | 阿偉投身電影廠景散工 | 圈內話阿偉寧願走電影散工路線，想搏下大銀幕機會。 | film_extra |
| np_story_c2_network_01 | 星河娛樂版 | 臨記阿偉廣結人緣 留廠景聽圈內故事 | 阿偉不急於趕場，選擇留在現場與前輩交流，積累行業人脈。 | 2 | 阿偉廣結人緣聽圈內故事 | 聽講阿偉好識做，收工無急住走，留低同班老臨吹水學嘢。 | network |
| np_story_c2_hustle_01 | 電視週刊 | 阿偉勤力跑通告 準時報到獲讚賞 | 臨時演員阿偉以準時勤力見稱，連日趕赴多個通告表現專業。 | 1 | 阿偉勤力跑通告獲讚賞 | 話阿偉做臨記好準時，朝早六點call time佢五點半已經到廠。 | board_hustle |
| np_story_c4_harsh_01 | 娛樂快報 | 何生安排通宵通告 阿偉頂硬上獲好評 | 面對苛刻拍攝條件，阿偉展現敬業精神，通宵工作毫無怨言。 | 2 | 阿偉頂通宵通告獲好評 | 聽講何生開個極苛刻通宵通告，阿偉都頂硬上，班底都話佢捱得。 | night_shift |
| np_story_c5_honest_01 | 電視週刊 | 采兒小訪阿偉 坦率回應敏感提問 | 新晉臨記阿偉接受周刊專訪，以誠懇態度回答業界敏感議題，幕前聲望提升。 | 3 | 采兒小訪阿偉坦率回應 | 采兒話阿偉個小訪好坦白，無識做戲呃人，反而幾討好。 | interview_honest |
| np_story_hiu_exchange_01 | 星河娛樂版 | 廠景休息角交流 阿偉與曉交換情報 | 阿偉在廠景拍攝期間與同事曉互動，分享行業資訊與拍攝心得。 | 1 | 阿偉與曉交換廠景情報 | 聽講阿偉同曉喺廠景休息角傾偈，互相交換組頭喜好情報。 | set_gossip |
| np_story_choi_weekly_honest_01 | 電視週刊 | 周刊專訪阿偉 坦誠分享臨記點滴 | 采兒撰文報導阿偉的臨記生涯，其坦誠態度獲讀者好評，成為頭條候選。 | 2 | 周刊專訪阿偉坦誠分享 | 圈內話采兒寫阿偉該篇小訪好正面，聽日出街實做頭條候選。 | mag_feature |
### story_mixed
| id | paperName | headline | dek | fameDelta | clipLabel | rumorEcho | boardScentTag |
|---|---|---|---|---:|---|---|---|
| np_story_c3_hard_01 | 星河娛樂版 | 廠景爆發爭執 阿偉與對手火藥味濃 | 兩人於片場拍攝期間發生口角，現場氣氛一度緊張，幕前聲望恐受影響。 | -1 | 廠景爭執見報 幕前聲望受挫 | 聽講當日片場有人錄低成段嗌交過程，仲話阿偉態度強硬，完全唔肯讓步。 | conflict_watch |
| np_story_c3_endure_01 | 娛樂快報 | 顧全大局 阿偉片場忍讓免傷和氣 | 面對對手挑釁選擇退讓，以完成拍攝進度為重，展現專業態度。 | 0 | 片場忍讓顧全大局 | 圈內人話阿偉今次忍得幾辛苦，不過為咗個騷順利拍完，唯有吞聲忍氣。 | — |
| np_story_c4_refuse_01 | 娛樂快報 | 拒接苛刻通告 阿偉與經紀何生傳分歧 | 臨記阿偉疑因工作時間過長拒絕通告，引發經紀何生不滿，雙方關係現裂痕。 | -1 | 拒接苛刻通告惹經紀不滿 | 聽講何生對阿偉拒接通告好唔高興，仲喺經紀圈放話，話佢唔識做，以後未必有好嘢派。 | refuse_risk |
| np_story_c5_spin_01 | 電視週刊 | 采兒小訪 阿偉圓滑應對滴水不漏 | 面對週刊記者采兒連番追問，阿偉對答如流，巧妙化解敏感話題，幕前聲望微升。 | 1 | 週刊小訪圓滑應對 | 采兒私底下話阿偉好醒，答嘢圓滑到滴水不漏，搞到佢都分唔清邊句真邊句假。 | — |
| np_story_c5_dodge_01 | 星河娛樂版 | 避談敏感話題 阿偉借故離開採訪 | 遇上週刊記者采兒突擊訪問，阿偉以趕通告為由匆匆離去，未有正面回應。 | 0 | 避談敏感題借故離開 | 有人見到采兒問埋啲敏感嘢，阿偉即刻借尿遁走人，搞到場面有啲尷尬。 | — |
| np_story_choi_weekly_official_01 | 電視週刊 | 電視週刊訪問 阿偉官腔回應顯謹慎 | 阿偉接受週刊訪問時以官方口吻作答，未見披露個人感受，報道篇幅偏向平淡。 | 0 | 週刊訪問官腔回應 | 采兒話阿偉今次打官腔，問極都係嗰幾句標準答案，搞到篇稿出街都只係淡淡帶過。 | — |

## 驗收點（文案包）
1. 14 則 id 齊；eventKey／choiceFlag／tone／fameDelta 對 PLAN §4＋§0 拍板  
2. C3 hard＝−1；C5 dodge＝0；choi weekly honest＝+2（即時+1之外）  
3. 禁詞 0；R_hiu distant 無模板  
4. preview stub sha＝sv stub sha  
5. Soft≠PASS；唔 tip LIVE；唔抬 ?v=／SAVE  
6. 引擎 enqueueFromStory／softRev=s102 → **等統籌抽樣 OK 先叫 iOS**（非本包）

## 已知（非本包）
- `enqueueNewspaperFromStory`／朝早 modal／favorGate／relGate／`__newspaper.fromStory` → Soft tip／iOS  
- softRev bust `s102` → iOS  
- boardScent 演算法 → P1 HOLD  
- #101 press 口語 nit heal → 本包 skip  
- Soft≠PASS｜唔 tip LIVE｜89–92 HOLD｜出圖 HOLD

---
完。劇本 executor 停；唔打統籌（父代理交）。
