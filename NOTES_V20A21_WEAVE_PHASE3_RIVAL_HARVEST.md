# v20a21 — Weave Phase 3-3：高俊傑競爭線收割（鏈 E）

串聯規劃最後一步。建基於現有足跡，唔另起爐灶：

- 高俊傑係現有 core NPC（NPC_LINES_CORE.rival／S.npcs.rival，對手演員）。
- 傳聞種子 `gao_steal_spotlight`（高仔片場搶鏡；茶餐廳 act_cha_gao_spotlight 拎到）。
- 主線 C3 本身就係同佢正面交鋒：`S.story.done.C3`，揀 hard／endure 寫
  `S.story.flags.rival_gao_hard／rival_gao_endure`；C3 見報剪報 topicKey 係 `rival:gao`（Phase 3-1）。
- 采兒內幕對白（Phase 2-3）早已預告呢條競爭線。

## 累積（衍生計分）

新狀態 `S.rivalry`（舊檔自動回填）。分數每次由現有訊號衍生計算，唔逐次累加：

- 聽過搶鏡傳聞（手帳有 gao_steal_spotlight）+1
- C3 交鋒過（done.C3 或任一 rival 旗）+2
- 報紙連載寫過（剪報 topicKey = rival:gao）+1

夠 3 分 → 高俊傑落戰書（toast），`faceoffState: "open"`，企位喺開戰嗰刻鎖定（stance）。

## 收割（競爭通告）

揀「競爭通告」而唔揀二選一事件：通告欄先係佢成日同你爭嘅地方，而且殺青有現成結算點。

- `mergeRivalGigs()` 條件注入（同 mergeIntelGigs／mergeFavorGigs 同一模式，掛喺
  gigsForLocSeasonBoard）：open 先上板，結算後落板，唔重複觸發。
- 新通告 `gig_rival_gao_faceoff`《霓虹夜影》新人爭位試演（星河電影組 tvb_longmen，
  即 C3 交鋒場地；$1,200 定額、1 日）。試鏡落選唔會令通告消失（未殺青唔算消費，可再報）。
- 勝負唔靠試鏡隨機 roll：殺青後 `rivalryTick()`（掛 advanceDay，喺 favorDueTick 之後）
  按當時雙軌（幕前聲量＋業內信用）判定，門檻 40；C3 揀 hard 佢記仇出盡力 +6，
  揀 endure 留一線佢冇出盡力 −6。

## 後果與落幕

- 贏：業內信用 +3（industryCreditDelta）＋報紙點名寫你贏咗
  （eventKey `story:C3:faceoff_win` → topicKey rival:gao，連載接得返 C3 嗰期，fameDelta +2）
  ＋高俊傑好感 +3（服氣）。
- 輸：人氣 −1（細懲罰，唔羞辱）＋高俊傑好感 −1＋報紙寫佢先拔頭籌，
  但 dek 畀玩家留「輸得起、監製記住個名」嘅口碑。
- 落幕：faceoffState 落 won／lost 終態；報紙剪報＋手帳傳聞（rival_faceoff_result）各留一痕。

## 未做（留待日後）

- 鏈 E 第 5 拍完整版：壓佢路線嘅負面碎片報復／留一線路線嘅對手私下畀情報（情報反餽）。
  今次 endure／hard 已影響決戰門檻，算係第一步。

## 測試

- test_weave33_logic 33/33、test_weave33_static 22/22。
- 舊測試全套（P0、P0-3、Weave 1-1/1-2/1-3、2-1/2-2/2-3、3-1/3-2）無回歸；node --check 過。
- 唔改 SAVE key、softRev、?v=。
