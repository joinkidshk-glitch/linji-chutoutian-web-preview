# NOTES_V20A280 — 支線補完第 ③ 組：收尾獎勵（WORKORDER §12）

- 基線：常駐 clone main `451cb8a`（v279，suite 344／9，通告庫 288 張）。
- 本票：`index.html` 46129 → **46167 行（淨 +38）**；新測試 `tests/test_sideline280_logic.js`（40 項）；resync 腳本 `qa280/resync280.py`。
- 設計依據：DECISIONS Q10（2026-11-15 21:45）已批——每條線暖版完成加聲望 ＋2／信用 ＋2＋專屬引薦通告，數字用建議值原樣落地（九條全暖 ＋18／＋18）。攻略側 3.1–3.9「收尾獎勵」小節唔喺本票範圍，冇掂攻略 artifact。
- 唔改 SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`（`v20a10`）。

## §1 九線暖版標記 live 對照（判定點＝`sideline280GrantCompletion(lineKey)` predicate）

暖版完成＝該線人情債權（現行已有）＋聲望 ＋2／信用 ＋2＋專屬引薦通告；冷版／錯過無額外獎勵；之前已授出嘅債權照計，唔收返。

| 線 | live 暖版標記（判定點） | helper predicate | 備註 |
|---|---|---|---|
| 廖 liu | Beat 5 `liu_clash` 抉擇暖邊 `enc79_liu_clash_stand`（冷邊 `enc79_liu_clash_script`；Beat 4 推辭 `enc79_liu_declined`） | `enc79_liu_clash_stand && !enc79_liu_declined` | WORKORDER 草稿旗 `liu_stand_92` 喺 index.html 0 命中，唔用（見 §3） |
| 顧 gu | 無 Beat 5 抉擇；暖版＝patron 閘本身：tier≥4＋無 `enc83_gu_loan_refused`（Beat 3 唔借）＋無 `gu_n10_warned`（`gu_n10after`「提醒他以後不要再碰賭」嗰邊，冷旗） | `!enc83_gu_loan_refused && !gu_n10_warned` | 草稿旗 `gu_patron_take` 0 命中；live 無正面暖旗（見 §3、§7） |
| 麥 mak | 無 Beat 5 抉擇；暖版＝patron 閘本身：tier≥4＋無 `enc79_mak_honest`（`mak_respect`「老實講自己會驚」，L35881） | `!enc79_mak_honest` | 草稿旗 `mak_follow_big` 0 命中；live 無正面暖旗（見 §3、§7） |
| 駱 lok | `lok_calm_truth`（`lok_e4grudge` seg）＋三個冷旗全無 | `lok_calm_truth && !lok_join_rant && !lok_loose_row && !lok_cover_first` | `lok_join_rant` 係同一抉擇嘅互斥冷邊，現實唔會同暖旗齊出，防禦性檢查（測試 (1)「駱陪鬧」個案釘住） |
| 魏 ngai | `ngai_patron_vouch`（`ngai_patron` beat；照實講嗰邊經 `enc79ChoiceFx` fx `ngai_vouch` 授債權） | `!ngai_rain_hold_back`（只喺 vouch fx 入面叫 helper） | 債權改行 fx 通道，`ngai_patron` beat 本身無 `grants()` |
| 齊 chai | Beat 4 `chai_truth_change`＋Beat 5 `chai_try_new` 兩個都要啱 | `chai_truth_change && chai_try_new` | 嚴過 patron 閘——閘唔讀 `try_new`；WORKORDER 話兩個都要啱 |
| 彭 pang | Beat 5 `pang_noodle_night`（`pang_n17` seg）＋`pang_cover_night`＋`pang_listened` | `pang_cover_night && pang_listened && pang_noodle_night` | 嚴過 patron 閘——閘只睇 tier；WORKORDER 話要食麵 |
| 鍾 chung | Beat 3 `chung_kept_quiet`（`chung_f_clue` seg）＋Beat 4 `chung_listened` | `chung_kept_quiet && chung_listened` | 鍾線無 Beat 5 |
| 程 ching | 主線 N15 `flag_vocal_train`＋Beat 3 `ching_back_train`（`ching_e4` seg）＋Beat 4 `ching_stand_slow` | `enc87StoryFlag("flag_vocal_train") && ching_back_train && ching_stand_slow` | 九線之中最嚴，三個都要啱 |

## §2 專屬引薦通告：0 張新開，10 張接駁

三張 WORKORDER 話「現行已有」嘅舊 id（`gig_br89_liu_priority`／`gig_br89_patron_pang`／`gig_br89_patron_ching`）喺 288 張新庫 0 命中——「現行已有」指舊庫，新庫重建嗰陣跌咗。逐張對位後，**10 張專屬引薦通告全部已在新庫（v274 取代版）**，只需接駁 trigger，唔使新開，唔復活舊庫 id：

| 線 | 新庫通告 id | 標題 | trigger（credit id） |
|---|---|---|---|
| 廖優先試鏡 | `gig_1991_film_103` | 《笑住過肥年・外傳》 | `credit_enc79_liu_priority` |
| 廖 G-L1 | `gig_1992_film_103` | 《吉星笑哈哈》 | `credit_enc83_liu_patron` |
| 顧 G-G1 | `gig_1992_rec_205` | 《夜總會登台暖場》 | `credit_enc83_gu_patron` |
| 麥 G-M2 | `gig_1991_film_211` | 《武館群英》 | `credit_enc83_mak_patron` |
| 駱 G-LOK-1 | `gig_1992_rec_111` | 《主打歌》MV | `credit_enc83_lok_patron` |
| 魏 G-NGAI-1 | `gig_1991_film_212` | 《鐵橋風雲》 | `credit_enc83_ngai_patron` |
| 齊 G-CHAI-1 | `gig_1992_film_206` | 《油麻地夜班》 | `credit_enc83_chai_patron` |
| 彭 | `gig_1991_variety_203` | 《台慶大騷》台上助理 | `credit_enc84_pang_patron`（持有債權嗰陣上板，Beat 5 唔重複派） |
| 鍾 G-C1 | `gig_1991_film_213` | 《秋日絮語》 | `credit_enc84_chung_patron` |
| 程 | `gig_1992_rec_106` | 《夜場匯演》 | `credit_enc84_ching_patron` |

- 全部 `trigger.kind==='credit'`＋BR89 映射對位；BR89 映射共 14 對（13＋v279 `gig_1992_film_202`→`credit_wf3_comedy_crew`）。
- 注意：`gig_1991_film_214`《笑住過肥年》夜景補拍係 `wf3harvest` 收割通告（v279），唔係外傳優先試鏡，唔好混淆。
- 通告庫維持 288 張，冇新開。

## §3 同 WORKORDER 出入（以 live 為準）

1. **草稿旗 0 命中**：`liu_stand_92`／`gu_patron_take`／`mak_follow_big` 喺 index.html 0 命中，唔用、唔創建新旗名；判定一律用 §1 嘅 live 旗。測試 (7) guard：呢三個名只喺 v280 註解出現一次，唔入判定 code。
2. **顧／麥 live 無 Beat 5 抉擇**：`gu_patron`／`mak_patron` seg 無抉擇（顧：應承係 patron 閘本身；麥：「跟」係無條件對白）。暖版判定用 patron 閘本身（§1），唔改 WORKORDER 旗名去遷就。
3. **彭／齊 patron 閘鬆**：閘唔讀 Beat 5 暖旗，所以冷版玩家照攞債權（舊制），但**唔攞 ＋2／＋2**（helper predicate 擋住）。測試 (2) 釘住「債權照授但獎勵唔派」。
4. **E1 舊表 vs live**：`ENDING410_T`（L12550）E1 數字（聲望 60／信用 55／雙軌 125）係舊表，live 唔用佢；live 閘係 `ENDING95_T`（L12683，聲望 ≥70、信用 ≥65、雙軌 ≥350）。另 `end95BuildGaps`（L12960–12962）玩家面「差幾多先到天王」提示仍用舊表數字——**已發現嘅舊不一致，唔喺 v280 範圍，唔修**。
5. **派生信用效應**：聲望＝`S.fame` 直加；信用係派生值（`dualTrackNumbers`：`baseCredit = round(fame×0.5 + stage×0.3 + acting×0.2 − max(0,stress−40)×0.1)`，`industryCredit = max(0, baseCredit + industryCreditDelta)`）。＋2 聲望令 baseCredit ＋1，連 ＋2 delta，`readDualTracks` 信用實際 **＋3／線**；九線全暖：聲望 ＋18、delta ＋18、派生信用 ＋27（測試 (6) 釘住）。獎勵寫入通道：`S.fame += 2`（一次性敘事獎勵唔經 CALIB60 遞減，CALIB60 註解本身咁講）＋`S.industryCreditDelta += 2`（殺青反響同一路），之後 `syncDualTracks(S)`。

## §4 實裝機制

- 單一 helper `sideline280GrantCompletion(lineKey)`（`enc79GrantCredit` 之後，舊 L38870 起，＋37 行）：冪等（`S.flags["sideline280_"+line]` 已派標記），暖先派聲望 ＋2／`industryCreditDelta` ＋2，之後 `syncDualTracks(S)`。冷版／錯過：helper 唔派。
- Call sites 共 15 處（＋helper 定義＝16 處 edits）：8 個暖版 patron `grants()`（liu／mak／gu／lok／chai／pang／chung／ching）＋`ngai_vouch` fx 1 處（＋1 行）＋5 個收尾 beat 新加 `grants()`（`liu_clash`／`lok_e4grudge`／`chai_repay`／`pang_n17`／`ching_e4`，補派點：patron 可以喺最終抉擇之前早開，因為 `pickBeat` 會跳過未到時窗嘅 beat）＋heart 完成回調 1 處（chai／pang／chung／ching 四線守衛呼叫）。
- 機制依據：`enc79PickBeat` 按 `ENC79_BEATS` 順序揀第一個 `when()` 真＋未做嘅 beat；`grants()` 喺 segFx 回調行（L39271），抉擇確認寫旗之後先行（`opt.flags` 寫入 L39687），所以 grants 睇到當次抉擇嘅旗；每 beat 只開一次（`beatsDone` 檢查）。`enc79GrantCredit` 冪等。BuildScript 入面 beats 先於 heart 檢查，所以 heart 旗可以喺 patron 之後先落。
- 鍾 `chung_farewell` 鉤考慮過後刪咗（heart＋patron 兩鉤已覆蓋全部次序，冗餘）。

## §5 3.10 結局門檻核實（一致，唔改，唔加新條件）

- **E1**（live 閘 `resolveEnding410` 用 `ENDING95_T` L12683）：聲望 ≥70、信用 ≥65、雙軌（聲望＋信用）≥350、負標籤 ≤1、質性閘：獎 ≥1＋擔正媒介 ≥2＋主線脊骨已走完（`awards95.hasWin && leadMedia95.length >= 2 && spine95.done`）。收尾獎勵只餵現有輸入（聲望／信用→雙軌、作品通告→擔正媒介數），唔自創結局條件。
- **E2**（`endingE2Eligible410`）：信用 ≥42＋聲望 ≥35（`ENDING410_T.e2Credit/e2Fame`）。
- **E4**：聲望 ≥50、信用 ＜30；救回版＝持有債權 ≥2（`e4RescueCredits`），唔放寬。
- **E5**：已清債＋持有 ≥6（`e5FavorTotal`）＋何生 rel ≥60（`e5AgentRel`）。

## §6 測試

- 新測試 `tests/test_sideline280_logic.js`：**40 項，ALL PASS**。7 組：(1) helper 單元 (2) patron grants 整合 (3) 補派次序＋heart segFx 真行 (4) 通告接駁 (5) 3.10 門檻 (6) 九線全暖合計 (7) 靜態 guard。測試模式沿用 v278 做法——由 index.html 用 indexOf＋括號配對抽取 function／const，連同 stubs 一齊 eval。
  - 修過兩處：① helper 駱 predicate 補 `!lok_join_rant`（測試 (1)「駱陪鬧」個案捉到）；② 測試 (3) heart segFx 個案：`enc79BuildScript` 回傳 steps 入面，抉擇段嘅 `segFx` 掛喺 choice step（最後一步），唔係第一句——`pushLines` 只將 `segFx` 掛喺最後一行（`i===(lines.length-1)`），`pushSeg` 抉擇段將 `segFx` 掛喺 choice step；測試改為搵 `seg==='heart:ching_tinlok' && typeof segFx==='function'` 嗰個 step。
- v278 舊測試 `tests/test_sideline278_logic.js` 仍 ALL PASS。
- 全套 suite：`bash qa131/run_suite.sh` → **TOTAL PASS 345 FAIL 9**（基線 v279 344／9；＋1 係新測試檔）。9 項 FAIL 全部係已知 pre-existing，名單同基線一致：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38。**零回歸**。
- `node --check`（抽出 script blocks）：JS-OK。

## §7 Resync（釘行漂移，純漂移，內容逐行核實）

- 本票淨 +38 行（helper ＋37 @舊 L38870 之後＋ngai fx 行 ＋1 @舊 L39065；15 處 grants() 單行原地改，行數不變），令 5 檔 static 測試釘行漂移。`qa280/resync280.py` 用 difflib 對住常駐 clone main（451cb8a）建舊→新行號映射，核實全部錨點內容逐字相同先改檔（travel114 COUNT 12／FREE 40／DEF／WRAPPER、rom176 6 釘、tang DEF）；單次掃描 dict 查表改行號，唔逐對 re.sub。
- 改動：`tests/test_travel114_static.py`（COUNT／FREE 集合內 ＋38 者、DEF 41377→41415）、`tests/test_rom176_static.py`（4 釘各 ＋38：39732→39770、40090→40128、41262→41300、41418→41456；6325／14813 喺插入點之前唔郁）、`tests/test_gift185_static.py`／`test_tang171_static.py`／`test_tang173_static.py`（總行數 46129→46167，鏈尾加 ＋v280 +38；tang 兩檔 DEF 41377→41415＋`lines[]` guard／index 41383→41421／41376→41414）。
- Resync 後 5 檔全部 PASS，全套 suite 回到 345／9。

## §8 已接受偏差

- **顧／麥早開 patron 之後先揀冷版，理論上獎勵已派出**——同債權本身喺 live v269 閘嘅鬆動一致，唔重構。顧：patron 閘讀 `gu_n10_warned`（N10 後事件）同 `enc83_gu_loan_refused`；如果玩家攞咗 patron 之後先行冷邊，helper 已經喺 patron grants 嗰陣派咗。麥同理（`enc79_mak_honest` 係 Beat 4 旗，patron 喺 Beat 5 之後先開——實際上麥線 patron 喺 respect beat 之後，honest 旗落喺 patron 之前，所以麥線唔受影響；顧線 N10 後事件可以喺 patron 之後先發生，係真正嘅邊緣情況）。

## 落地記錄（post-merge）
- main HEAD `cc0a8ca`（squash merge v280，2026-11-18）
- 全套 suite：**345／9**（9 項全部係已知 pre-existing FAIL：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38；基線 344／9＋新測試檔 1 個）
- GitHub Pages 核實：主頁 200、4,678,453 bytes、與本地 index.html byte-identical
- 工作副本 `linji-work280` 已刪
