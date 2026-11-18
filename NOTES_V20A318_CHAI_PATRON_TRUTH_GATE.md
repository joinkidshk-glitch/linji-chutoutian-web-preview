# v20a318 — 齊鎮海 patron 閘同收尾獎勵按草稿對齊

## 目的

齊線提攜閘同收尾獎勵判定脫鈎（同 Q24／v311 程線同一類問題）：提攜暖版閘係排除式
（T4＋唔係三壞旗），收尾獎勵讀法係 `truth_change && try_new`。結果：

- 無講真話嘅 T4 玩家（例如 Beat 4 未做就衝到 T4）攞到提攜＋債權，但獎勵唔派。
- 講咗真話但 Beat 5 要穩陣嘅玩家（`play_safe`），提攜照播但獎勵永遠唔派。

草稿（`linji-story-sidelines/drafts/batch2-lok-ngai-chai-pang.md`）：
- Beat 5 引薦閘係 `chai_truth_change`（L1110）。
- 好收尾＝`advise_stop`＋`truth_change`（L1173）；冷收尾＝`silent` 或 `comfort`（L1182）。
- `try_new`／`play_safe` 係好收尾句變體一／二（L1167），唔係暖／冷分界。

## 改動（index.html 淨 2 行）

| 位置 | 改前 | 改後 |
| --- | --- | --- |
| L41830 `chai_patron` 暖版閘 | T4＋!silent＋!comfort＋!loose_fear | T4＋**`chai_truth_change`**＋!silent＋!comfort＋!loose_fear |
| L39818 `sideline280GrantCompletion` 齊線 | `warm = !!chai_truth_change && !!chai_try_new` | `warm = !!chai_truth_change` |

守住（全部唔郁）：冷版閘（L41829）、finale 閘（L41831）、heart 閘（L40260）、
fear 窗（L41826，1990–91）、choice 閘（L41827，1992＋T2）、repay 閘（L41828）、
對白、grants（債權授出）、wrap_safe／cap_try／finale 尾句變體、GRANT229 即派
（fear 守口→tv_111、choice 勸停→tv_114、choice 唔出聲→tv_207、
repay 唔同→tv_111、repay 穩陣→tv_112）、舊檔唔 crash。

## 逐類玩家影響

| 玩家 | 提攜 | 收尾獎勵（聲望＋2／信用淨＋2） |
| --- | --- | --- |
| 講真話＋試新角（try_new） | 暖版（不變） | 有（不變） |
| 講真話＋穩陣（play_safe） | 暖版（不變） | **而家有**（舊制無） |
| 講真話＋未做 Beat 5 | 暖版（不變） | **而家有**（舊制要等 Beat 5） |
| 無講真話＋T4（漏做 heart／揀安慰） | **唔播暖版**（舊制會播） | 無（不變） |
| 講真話＋之後唔出聲（silent） | 冷版（silent 排除保留，草稿 L1182） | 心嗰陣已派（heart 回調），提攜冷版無債權 |
| 講出去（loose_fear） | 冷版（不變） | 無（warm heart 唔開，攞唔到 truth_change） |
| 舊檔（已有 beatsDone.chai_patron，無 truth_change） | — | finale 照播（finale 閘唔讀 truth_change） |

**唔做嘅嘢**（按 brief，草稿反對）：唔改做 truth_change＋try_new 兩旗齊備
（穩陣玩家會失去提攜＋債權＋film_206＋成個 finale）；唔放寬 fear 年窗；
唔喺 heart 閘加 kept_fear 要求；唔喺獎勵／提攜閘加 advise_stop 要求；
唔「修正」choice 閘 1992（草稿寫 1991 係已知漂移，另開票先處理）。

## 測試

新檔 `tests/test_r318_chai_patron_truth.js`：**46 項全 PASS**。
- (A) 靜態：兩閘字串＋grants＋280 讀法＋registry 次序＋對白（patron 7 句）——
  注意：patron 對白係 7 句唔係 6 句，首句係「阿偉，你最近嗰幾場戲，我有睇返……」。
- (B) 提攜閘矩陣：truth_change 有／無 × 三壞旗；T3 唔開；silent＋truth_change 行冷版。
- (C) 獎勵讀法矩陣：truth_change only——play_safe 有獎；try_new 單獨／comfort／
  silent／loose_fear／無旗無獎。
- (D) 次序＋補派：無 heart 嘅 T4 玩家唔播提攜，遲補 truth_change 即播；
  heart 回調（撳最後一句 segFx）／repay／patron 三個補派點邊個後到邊個派獎、唔重派。
  探測筆記：heart 回調掛喺 heart seg 最後一句嘅 segFx（唔係第一句）；
  heart 段要全部 beats 做晒先會跌入 heart 分流。
- (E) 舊檔：已有 beatsDone.chai_patron 但無 truth_change → finale 照播；
  已有 sideline280_chai → 唔重派；無 Beat 5 旗唔 crash。
- (S) 靜態：heart／fear／choice／repay／finale 閘、GRANT229 即派、FRAME 變體、
  回響通告 trigger（tv_114＋film_206 全部係 credit_enc83_chai_patron）、gigs 306 張。

## 舊測試同步（跟 v311 前例，唔係回歸）

| 檔案 | 改咗咩 |
| --- | --- |
| `tests/test_sideline280_logic.js` | (1) 缺一案例刪 truth_change 單獨（而家會派）；(2) 穩陣版 patron grants() 改為獎勵照派；(3) 齊補派改寫：patron 有真話即派＋repay 唔重派；另加「patron 早開未講真話唔派，講真話後 repay 補派」 |
| `tests/test_sideline278_logic.js` | (4) 無壞旗暖版照開：齊加 truth_change（跟駱 v314 前例） |
| `tests/test_r305_warm_finale.js` | (B) 提攜未播先播提攜：齊加 truth_change；(S) 靜態 label「齊三旗排除式」→「齊 truth_change＋三旗排除式」 |
| `tests/test_r306_chai_frame.js` | 頭註＋(D) 暖版 heart 改 truth_change only（try_new 唔再係必要條件）；(F) chai_try_new 出現次數 3→2（280 讀法唔再讀 try_new，淨低授出點＋cap 分流） |
| `tests/test_enc83_logic.js` | (8) T4 提攜八星：齊加 truth_change（跟駱 v314 前例） |
| `tests/test_enc84_logic.js` | (9) T4 提攜十二星：齊加 truth_change |
| `tests/test_r317_chai_echo.js` | (0) 靜態閘斷言改做 v318 新暖版閘字串（舊斷言本身寫明「v318 另票」）；冷版閘字串不變 |

`test_sideline273_logic.js` 唔使改（66 支草稿旗全部仍在 html 出現；BR89 映射不變）。

## Suite

`bash qa131/run_suite.sh`：**TOTAL PASS 381 FAIL 9**（基線 380／9，＋1 係新測試檔；
9 項 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／
weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。

首跑 378／12——多出嘅 3 項 FAIL 係上面 enc83／enc84／r317 三檔寫死舊提攜閘，
已同步更新（唔係回歸）。`qa296/derive296.json` suite 重跑再生，已還原，唔入版。

## §5 落地實數

- main HEAD：`122e27e`（內容 commit `6a1bb5d` squash 合併；本 commit `122e27e` 為 §5 填實數）
- Pages：index.html md5 `2f2dc271c9e6dee7dcc77547490752a5`／4,700,388 bytes，byte-identical，v20a318 標記在位
