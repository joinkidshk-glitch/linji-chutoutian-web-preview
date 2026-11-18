# NOTES_V20A321_CHAI_CHOICE_WINDOW_1991_1992

## §1 任務一句話
齊鎮海 `chai_choice`（Beat 3 勸停）閘由 1992-only 放寬做 1991–1992，對返草稿次序（choice 在 N13 之前），同時唔鎖死 1992 年玩家。

## §2 問題：次序倒轉＋heart 變體永久流失
- 草稿 Beat 3 閘（`batch2-lok-ngai-chai-pang.md` L993）：「T2＋1991 年」；場面 1991 年化妝間；掛鈎「N13〈站隊〉之前，1991 年」。
- N13〈高爾夫球〉顯示 1992夏（`content/story_detail_n1_to_n17.json` source `when: "1990夏"`，YEARS66＋2）——草稿「1991 年、N13 之前」喺顯示年係自洽嘅。
- Live 閘（v83 `7a9b36e` 原始引入，NOTES_V20A83 零解釋）係 `ys.year===1992`，令 choice 只能喺 N13 同年甚至之後先開，次序倒轉。
- 真缺陷唔係純文件唔一致：heart 閘（L40260）淨係 tier≥3、無年份窗；1991 年上到 T3（fav≥45）嘅玩家，choice 閘死 → picker 回 null → heart 照播，`chai_advise_stop`／`chai_silent` 兩個 heart 變體永久錯過（heartDone）。
- 嚴格改返 1991 會鎖死人：1992 年先第一次撞到齊嘅玩家（遲遇，v318 已確認存在）＋舊存檔 1992 年未做 choice 嘅玩家，1991-only 閘會令佢哋永遠攞唔到 advise_stop／silent——同 v318 避開嗰類鎖死一模一樣。草稿 1991 係「由呢年開始」，唔係「淨係呢年」。

## §3 實裝：index.html 淨改 1 行，對白零改動
| 位置 | 改前 | 改後 |
|---|---|---|
| `index.html:41828` `chai_choice` 閘 | `return ys.year===1992 && enc79TierOf(st.fav)>=2;` | `return ys.year>=1991 && ys.year<=1992 && enc79TierOf(st.fav)>=2;`（跟 fear 閘同一寫法） |

- 守住：`chai_fear`／`chai_repay`／`chai_patron`／`chai_patron_cold`／`chai_finale` 閘、heart 閘、對白（choice／heart／repay 全部）、grants、GRANT229 全部唔郁；舊檔唔 crash。
- 唔做：唔改做嚴格 1991；唔郁 win 檔（1991 年 base 概率已經撞得到，`enc79InWindow` 全檔 0 調用者，`enc79PresenceP` 窗外 base p=0.5）；唔郁 N13 時間；唔改草稿（L993 已經啱）。

## §4 逐類玩家影響表
| 玩家 | 影響 |
|---|---|
| 新玩家 | 1991 年 T2＋開始做到 choice，草稿次序（choice → N13 → heart → repay）恢復；heart 變體唔再流失（registry 優先級：`enc79PickBeat` 按次序回傳第一個開到嘅 beat，`enc79BuildScript` 先處理 registry beat，heart 喺 else 分支） |
| 1992 年先撞到齊嘅玩家／舊存檔 1992 年未做 choice | 照做到，零鎖死 |
| 1991 年已做 choice 嘅舊檔 | beatsDone，唔重播 |
| 1992 年已做 choice 嘅舊檔 | 唔受影響 |
| GRANT229 派送 | tv_114／tv_207 唔郁；1991 年選擇嗰陣派送落返季內（兩張都係 1991 年 gig） |
| 計數 | 庫 307 張／trigger 37（credit 26）／BR89 18 對——零改動 |

## §5 落地（待填）
- Main HEAD：
- Suite TOTAL：
- Pages index.html md5／bytes：
- 工作副本已刪：

## §6 測試
- 新檔 `tests/test_r321_chai_choice_window.js` **23 項全 PASS**：
  - (S) 靜態 9 項：新閘字串逐字、舊 1992-only 字串消失、fear／repay／patron／patron_cold／finale 閘唔郁、registry 次序唔郁、庫 307／trigger 37／BR89 18。
  - (B) when() 直接判定 7 項：1991 T2 開、1992 T2 開、1990 T2 唔開、1991 T1 唔開、1993 T2 唔開、1991 T3 開、1992 T4 開。
  - (C) 次序 6 項：1991 年 T3 玩家（fear 已做、choice 未做）picker 回 choice 唔係 heart；buildScript 播 `beat:chai_choice` 唔播 heart；choice 做完之後先輪到 heart（advise_stop 變體「你講中晒。」在位）；無 advise_stop 嗰陣 heart 照播、無變體句；舊檔 1992 年未做 choice 照做到；1991 年已做 choice 唔重播。
  - (D) 共存 1 項：GRANT229 choice 兩行唔郁（停一停→tv_114、唔出聲→tv_207）。
- 舊測試同步 1 檔：`tests/test_r318_chai_patron_truth.js` L253（閘字串斷言＋註解「草稿 1991 漂移另開票」→ 新閘字串＋註解「v321：放寬 1991–1992」）；r318 單獨跑 ALL PASS。
- 全套 suite：**384 PASS／9 FAIL**（基線 383／9，＋1 係新測試檔；9 項 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／44／49_static／wf5_87／wrap38）。
- `qa296/derive296.json` 已還原，唔入版。
