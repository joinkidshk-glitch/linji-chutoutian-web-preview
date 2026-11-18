# NOTES_V20A299 — Q12 三旗遊戲中跟進

基線 main `631ef7a`（v298，suite 362／9）。任務：choi_spin／flag_canteen_grind／flag_studio_follow
三支旗補遊戲中跟進，唔止結局回望一句。對照旗 flag_canteen_quit／flag_studio_roam 對稱跟進。

## §1 前提核實（parent 2026-11-18 17:14 親查＋統籌覆核）

| 旗 | 寫入 | 之前唯一讀者 |
|---|---|---|
| choi_spin | N5_b「打圓場包裝答」（story JSON L1032） | index.html 登記表 `STORY_FLAG_EVENT` L33619（報紙 key），零遊戲中讀者 |
| flag_canteen_grind | N6_a「電視線：接固定閒角」（story JSON L1247） | 結局回望 ECHO89 L13401 |
| flag_studio_follow | N6F_a「電影線：接固定跟班」（story JSON L1434） | 結局回望 ECHO89 L13403 |
| flag_canteen_quit／flag_studio_roam | N6_b／N6F_b（唔接嗰邊） | 結局回望 ECHO89 L13402／L13404 |

- 主線旗經 StoryOC 落旗，`S.flags`＋`S.story.flags` 兩邊都有（index.html L14269）；讀旗用
  `enc87StoryFlag`（L41429，查兩邊）或 `choice47StoryFlag`（L24947，StoryOC.getFlag 優先）。
- N6／N6F 節點本文講明：呢兩個選法「只改他那段日子怎麼過，不改之後哪一幕開」——跟進唔可以扮真分支；
  跟進係「嗰段日子點過」嘅後果（邊個記得你／邊個搵你），唔改主線分叉。
- 路線互斥：一個 playthrough 最多中四支 N6 旗其中一支（grind／quit 一組，或 follow／roam 一組）。

## §2 choi_spin → R_choi_push1 變體（新 hook choi299PrepareNode）

落點核實（研究員 B）：`content/story_detail_romance_vera_hiu_choi.json` R_choi_push1
「茶記的爆料交換」（P1.5，era_1989_spring，顯示 1991 春）——N5 之後第一個采兒節點；
`openConditionsAny` 已列 `flag_choi_spin`（OR 閘已開，唔使修閘）；場面正係「采兒再問料」，
同 N5_b 尾句「以後有咩特別嘢，記得提點我」同一條線；有現成二揀一抉擇可掛差異。
唔揀 meet（時序可交錯）／push2（設定明言今晚唔談工作）／crisis（1991 冬，太遠；另有
pre-existing 時序疑點：when 1991 冬顯示 1993 冬，超出遊戲終點，唔係今票範圍）／ending。

機制：PrepareNode 模式（enc158／rom159 先例）。新函數 `choi299PrepareNode(node)`，
掛喺 `StoryPlay.start` L10699 rom159 之後同一 try/catch 模式；只處理 `R_choi_push1`，
其餘節點回 null。淺拷貝（頂層 Object.assign＋逐 beat 拷 lines＋逐 choice 拷 effects），
原節點唔郁。

變體（廣東話對白；旁白書面語）：

- **spin 版**：beats[0] 換——采兒先提 N5：「上次喺片場休息角，你話嗰晚只係見到人影晃過，
  可能係傾劇本——我返去諗過，你講嘢嗰陣，隻眼望咗去第二度。」／「我唔係怪你，記者等得；
  不過今次，我唔想再聽包裝版。你肯講幾多，我寫幾多，唔會夾硬將你啲嘢寫大佢。」然後入正題。
  beats[3] 換——情報互惠由即時變條件式：「你今次講嘅，我會自己查證；查實咗，我先至話你知
  我嗰邊收到咩。」
- **dodge 版**（對稱，輕量）：beats[0] 冷淡一句：「上次你話副導叫你，行得咁急——今次唔趕時間呀嘛？」
  beats[3] 照舊。a 數值照舊（肯坐低講，已經係補返）；b 同 spin 版一致 rel −1（連續兩次唔合作）。
- **honest 版**：行原版，唔郁。

選擇數值（spin 版）：
- `C_choi_push1_a`（給獨家方向）：rel_choi ＋2→**＋1**，fame ＋1→**＋0**，另落
  `flag_choi_spin_repaid`（補返信任，留畀日後節點讀，今票唔實裝後續）。
- `C_choi_push1_b`（拒絕提供）：rel_choi ＋0→**−1**，standing ＋1 照舊。

硬約束（rel 計數，親查 JSON）：meet a ＋1／push1 a 原版 ＋2／push2 a ＋2／crisis a ＋2，全佳上限 7，
commit 門檻 `COMMIT48_REL_MIN` 6。spin 全佳＝1＋1＋2＋2＝**6，剛好夠門檻，零容錯**——所以 spin 版 a
必須至少 ＋1，唔可以 ＋0。spin 的代價係「情報互惠延遲＋fame 少 1＋零容錯」，唔係永久落後。

## §3 四旗 → code-side 特別通告（Q12_FOLLOW_GIGS＋mergeQ12Gigs）

路線決定：**唔行新庫 trigger**。`triggerGigOn` 七種 kind 無一種讀 story 旗（`story` 只讀
`S.story.done[nodeId]`，N6_a 同 N6_b 都會令 done.N6 變真，開唔到選項閘）；加第八種 kind＋
4 張入 `gigs_new.json` 會郁 302 張計數測試（P0／T0／A6／C0／B1 等）。跟 v298 前例行
code-side 池，`gigs_new.json` 零改動。

機制（照抄 `mergeFavorGigs` L22883–22927 模式）：
- 池 `Q12_FOLLOW_GIGS`（4 張）＋`mergeQ12Gigs()`，掛喺 `gigsForLocSeasonBoard` 開頭
  `mergeFavorGigs()` 隔籬（L43293），同一 try/catch＋typeof 守衛。
- 開閘 `q12FlagOn(key)`：`choice47StoryFlag` → `enc87StoryFlag` → `S.flags` 直讀。
  旗本身就係時間閘（N6 之後、W15／1990-04-09 之後先存在），**唔設 dueDay／window／tick**——
  Q12 係「記得你」的機會，長期有效，唔逼玩家。
- 落板：旗在＋未完成（無 `S.flags["done_"+id]`，`wrapHistory` 無該 gigId）先注入；
  `normalizeGigRecord(Object.assign({}, raw, { q12FollowGig:true }))`，冪等；
  殺青／拍攝中／等消息嗰陣 `isGigConsumed`（L17383）本身已擋返板。
- 通知：code-side gig 無 `trigger`，`mergeTriggerGigs` 唔會通知；merge 入面自己做一次 toast
  （`S.flags["q12Notified_"+id]` 冪等）：grind／follow 用「何生轉告」口徑（班底經何生搵你），
  quit／roam 用「情報站」口徑（出面聽到風聲）。
- 對稱：四張同一 tier、同一 pay、同一 days、同一 req、同一 fame，只係 loc／戲名／角色／文案唔同。
- 舊檔兼容：旗已寫入舊 save `S.flags`，舊檔下次開板即見到；`season:"不限"` 令已過季的舊檔都見到。

共通欄位（四張一樣，照 FAVOR 形狀）：`year:1988`（normalize 經 YEARS66＋2 變 1990，**唔可以寫 1990**；
文案零四位年份數字）；`season:"不限"`；`category:"臨記通告"`；`tier:"臨記"`；
`req:{acting:24}`（開局演技 18，一級演技課 1–2 堂就到；完全唔練就見鎖卡——「班底記得你，
但你要夠班」。刻意唔用 stamina：開局 75 已達標，等於白送）；`pay:[55, 65]`、`payExact:60`
（2 日，$27.5–32.5／日，新庫臨記標準；hi/lo＝1.18 ≤ 1.25）；`breachFee:0`；
`fame:[5, 10]`（新庫 1990 臨記全數）；`popularity:[0, 1]`；`stressDeltaHint:"低"`；
`hard:0.43`（新庫臨記主流）；`stars:1`；`shootDaysHint:2`；`shootBand:[2, 2]`；
`shootWeekdays:[1..7]`；`shootDeadlineDays:14`；`boardPriority:"high"`；`tagOnComplete:[]`；
`rumorKeys:[]`；`seasonHook:[]`；`boardHookMode:"normal"`；`isKeyGig:false`；
**無 `trigger`、無 `cast`、無 `favorDelta`、唔設 `applyDeadlineDays`**（長期有效，唔用假截止日）。

|  | G1 grind | G2 quit | G3 follow | G4 roam |
|---|---|---|---|---|
| id | gig_q12_canteen_grind | gig_q12_canteen_quit | gig_q12_studio_follow | gig_q12_studio_roam |
| 閘旗 | flag_canteen_grind | flag_canteen_quit | flag_studio_follow | flag_studio_roam |
| loc | tvb_longmen（星河，同 N6 班底） | tvb_kowloon（九龍電視台，出面） | film_lion（獅子山，同 N6F 班底） | film_harbour（維港電影，出面） |
| workTitle／title | 《茶餐廳風雲》／班底通告：《茶餐廳風雲》飯堂熟客 | 《夜市人生》／街外通告：《夜市人生》大排檔熟客 | 《茶樓風雲》／班底通告：《茶樓風雲》茶樓跑堂 | 《夜班貨倉》／街外通告：《夜班貨倉》貨倉領頭 |
| roleLabel／director | 飯堂熟客（有對白）／處境劇副導 | 大排檔熟客（有對白）／副導 | 茶樓跑堂（有對白）／電影組副導 | 貨倉領頭（有對白）／副導 |
| roleScale | tv_cameo_short | tv_cameo_short | film_support_small | film_support_small |
| boardNote | 班底記得你 | 搏到機會 | 片場記得你 | 搏到機會 |
| storyKeys | ["N6"] | ["N6"] | ["N6F"] | ["N6F"] |

四個戲名＋角色名已對 `gigs_new.json` 全庫核對，零撞名。文案守則：旁白／blurb／synopsis 用香港書面語，
對白先用廣東話；`director` 用職銜（全部喺 `GIG_DIRECTOR_ROLE_KEYWORDS121` 內）。

獎項影響（據實寫，唔寫「零影響」）：提名門檻計數嗰層零影響（臨記 category 計 0）；
`awards62YearWorks` 計分嗰陣唔濾 category，殺青咗嘅 Q12 通告會入作品桶（q＝0.51，桶底），
正常年份貢獻 base 約 ＋0.01–0.03——同 FAVOR 兩張已接受的水平一致，唔係新風險。

## §4 唔郁清單

- ECHO89 結局回望表（L13390–13410）四句文案唔郁；N5／N6／N6F 抉擇本身唔郁；
  `gigs_new.json`（302 張）唔郁；`GRANT229_CHOICE` 即派表唔郁（Q12 係板面機會，唔係即派）；
  `rom159PrepareNode`（R_choi_ending HE 拆分）唔郁；`triggerGigOn` 唔加 kind；
  `mergeTriggerGigs` L26600「46 張」過時註解唔係今票範圍，唔掂。

## §5 測試

新 `tests/test_r299_three_flags.js`（抽函數 eval 沙盒，照 `test_br89_favor_due.js` 寫法）：
choi 段——閘已開（openGate 任一 N5 旗入 push1）；spin 版 beats[0]／beats[3] 含回指句，無旗回 null，
原節點唔郁；spin a rel＋1／fame＋0／落 flag_choi_spin_repaid，spin b rel−1；dodge b rel−1、a 照舊；
honest 版行原版；spin 全佳 rel＝6 ≥ 門檻；rom159 ending 唔受影響。
gig 段——池形狀（4 張、欄位、year 1988、標題無年份數字、pay hi/lo ≤ 1.25、req acting 24）；
旗未落 merge 回 0；逐支旗只開自己嗰張（互斥）；殺青後落板；通知一次；舊檔旗在即見。
靜態段——ECHO89 四句在位；N5／N6／N6F 選擇原文唔郁；gigs_new.json 仍係 302 張。

## §6 殘留

- `flag_choi_spin_repaid`（push1 spin-a 落旗）留畀日後節點讀，今票只落旗唔實裝後續。
- R_choi_crisis when 1991 冬顯示 1993 冬（超出遊戲終點）係 pre-existing，唔係今票範圍。
- 實機覆驗：合約拍攝期（N6 即派 2 週合約）內見到 Q12 gig、接咗之後 scheduleShoot 點處理——
  suite 驗唔到，要實駕。
