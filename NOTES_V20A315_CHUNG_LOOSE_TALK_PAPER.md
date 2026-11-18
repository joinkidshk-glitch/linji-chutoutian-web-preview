# NOTES_V20A315 — 鍾楚凝 Beat 3「講出去」報紙花邊回音（Q25）

## §1 任務
- 鍾楚凝 Beat 3（`chung_f_clue`，後台走廊）揀「講出去」之後，下一期晨報加一則《維港日報》花邊碎片回音，跟 v302 模式。
- 真缺陷（parent 2026-11-18 22:23 親查 live）：對白 L38708 明寫「《維港日報》花邊多了一句碎片，沒有點名」，但 live 無呢則；`rumor_chung_canada_heard`／`rumor_chung_farewell_truth` 全檔 0 命中；`enc79PaperWhisper` 查表三項無 chung；`chung_loose_talk` 全檔 4 命中，0 處報紙。

## §2 實裝（index.html 淨 +15 行，47266→47281）
- Build 側（新 L34338–34350，v302 block 之後）：條件 `S.flags.chung_loose_talk` 有旗且未出過（已出旗 `S.flags.chungLooseTalkPaper315`）；列尾額外加，唔取代輪替花邊、唔入 3 則短訊上限、唔做頭條；已出旗唔喺 build 記。
- 文案（提案照跟）：headline「聽聞有女星赴加手續辦緊」；dek「有行內人表示，有女星近日正辦赴加手續，詳情未明。」；paperName「花邊短訊」；source `"side"`；sideId `side_chung_loose315`。書面語、含蓄口徑（聽聞）、無玩家名、**唔點名鍾楚凝**（DLG L38708 明寫「沒有點名」——同 v302 點名寫法唔同）。
- Commit 側（新 L34634–34635，跟 v302 模式）：見到呢則先記已出旗 `chungLooseTalkPaper315`。
- sideId 用專屬值，`enc79PaperWhisper` 查表唔認得就 no-op（L41428–41431）——唔開風聲窗，呢則係泄漏回音唔係風聲。
- 翌日晨報出，嗰日無報紙項目就順延下一期（done && !out 機制本身做到，唔使另寫順延）。

## §3 守住咩（全部唔郁）
- `chung_f_clue` 對白、選擇、授旗（`chung_loose_talk`／`chung_kept_quiet`）、fav（講兩句 −2／守口 ＋3）、即派（講兩句→`gig_1990_tv_207`）、heartCold 分流、patron 兩閘（冷版有 loose_talk／暖版排除）。
- v302 告別花邊（`side_chung_farewell302`）一行都唔郁；兩則可以先後出現，互不干擾（Beat 3 係 1991＋，告別係 1992 秋／冬）。
- `enc79PaperWhisper` 查表唔郁（只得三項）。
- 舊檔唔 crash（`S.flags` 未有旗就當無；已有 `chung_loose_talk` 旗嘅舊檔，下一期晨報照出呢則）。

## §4 測試
- 新檔 `tests/test_r315_chung_loose_paper.js`，跟 `test_r302` 模式：有旗→下一期晨報出呢則、列尾額外加、只出一次（第二期唔再出）、無旗→唔出、舊檔（已有 `chung_loose_talk` 旗）下一期照出、文案唔含「鍾楚凝」同玩家名、兩則齊備互不干擾、唔開風聲窗。**全 PASS**（單獨跑 ALL PASS）。
- 測試教訓：day 701 嗰期除咗輪替花邊，仲有 `side_lu_concert` 外加項（已知風聲 id），commit 會開一個 lu 風聲——E 段斷言要預期呢一個，唔係零個（v302 test_r302 day 39 同理，開兩個）。
- 全套 suite：**PASS 378 FAIL 9**（基線 377／9；＋1 係新測試檔；9 項 FAIL 全部已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／44／49_static／wf5_87／wrap38）。
- 首跑 373／14——多出嘅 5 項 FAIL 全部係靜態測試釘行漂移（本票 ＋15 行引起）：`qa315/resync315.py` 用 difflib 核實純漂移後，resync 咗 gift185／tang171／tang173／rom176／travel114 五檔（總行數 47266→47281、DEF 42475→42490、錨點按段 shift：＜34338 唔郁、34338–34620 ＋13、≥34621 ＋15）。

## §5 落地核實（待填）
- Main HEAD：
- Pages md5／bytes：
- 工作副本已刪；`qa296/derive296.json` 已還原，唔入版。

## §6 殘留
- 無。
