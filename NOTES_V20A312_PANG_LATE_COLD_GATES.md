# NOTES_V20A312 — Q25 彭少祺 pang_help 遲到行冷版，全套三閘

## 1. 做了什麼

草稿 PLAN L128：「留名→頂班開；遲到→頂班唔開，行冷版」。`pang_late` 旗（`pang_intel` 遲到選擇授旗）之前三處都未讀，今票三閘齊加，淨改 `index.html` 3 行，對白零改動。

| # | 位置 | 改前 | 改後 |
|---|------|------|------|
| ① | `ENC79_BEATS.pang_siuki` pang_help 閘（L41873） | `tier>=1 && enc83NodeDone("N11")` | 加 `&& !(S.flags\|\|{}).pang_late`——遲到嗰陣 Beat 3 頂一晚唔開 |
| ② | 暖版 heart 閘（L40260，enc79BuildScript） | 彭嗰邊淨排除 `pang_absent_night` | 加 `&& !(starId==="pang_siuki" && (S.flags\|\|{}).pang_late)`——唔播暖版交心，行 pool |
| ③ | pang_finale_cold 閘（L41875） | absent_night／brushed_off／early_night 三旗 | 加 `|| (S.flags\|\|{}).pang_late` 做第四旗——遲到玩家有冷收尾 |

## 2. 守住的東西

- `pang_intel` 選擇、授旗（`pang_showed_up`／`pang_late`）、即派（GRANT229：準時→`gig_1991_variety_201`／遲到→`gig_1991_variety_104`）、fav（準時＋3／遲到＋0）全部唔郁。
- `pang_n17` 閘唔郁（淨 T3＋1992 冬）：遲到玩家去得到 n17，唔死局。
- `pang_patron` 閘唔郁（淨 T4，無 pang_late）：同 `pang_absent_night` 玩家一致，提攜照舊行暖版——今票只處理三閘，唔擴範圍。
- `pang_finale` 暖收尾閘唔郁；但註冊次序冷收尾排暖收尾之前，遲到玩家即使集齊 cover／listened／noodle 三旗，pickBeat 都先取冷收尾（測試 C 已釘實）。
- 彭無獨立冷版交心（`pang_heartCold`／`pang_patron_cold` 皆不存在）：遲到交心行 pool，冷後果由 `pang_finale_cold` 承接——同 `pang_absent_night` 舊有做法一致，今票係閘改動，唔寫新對白。

## 3. 測試

新檔 `tests/test_r312_pang_late_cold.js`，38 項全 PASS（A 靜態 8／B when() 直接判定 12／C buildScript 端到端 8／D GRANT229＋fav 對位 4／E 舊檔 2／S 靜態其餘 4）：

- 遲到→頂一晚唔開、唔播暖版交心、去得到 n17、冷收尾照去得到；準時→三閘行為唔變。
- 遲到＋暖收尾三旗齊→冷收尾贏；準時＋三旗齊→暖收尾。
- 舊檔（已有 pang_late）唔 crash，閘行為同新檔一致。

測試教訓：`when()` 回傳值唔係 boolean（`&&` 鏈尾段回旗值 1／undefined），直接判定要用 `!!`／`!` 唔好用 `=== true`／`=== false`；`enc79BeatOpen` 嗰類要先 `setFav`＋`metStar`，否則星態預設 fav 0。

## 4. 全套 suite

`bash qa131/run_suite.sh`：**TOTAL PASS 375 FAIL 9**（基線 374／9；＋1 係新測試檔）。9 項 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38。

`qa296/derive296.json` suite 重跑再生（＋245 行，衍生盤點檔唔係 source），commit 前已 `git checkout --` 還原，唔入版。

## 5. 落地

- main HEAD：`TBD`（合併後填）
- Pages md5／bytes：`TBD`（curl 核實後填）
- 工作副本 `linji-work312` 已刪。
