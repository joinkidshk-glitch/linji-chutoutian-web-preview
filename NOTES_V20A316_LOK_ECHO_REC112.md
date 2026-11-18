# NOTES_V20A316 — 駱家聲支線回響通告：gig_1992_rec_112《追風少年》升格

- 票：v316（D-11／§3.6B 支線回響 9 張表之駱家聲行）
- 基線：main `6b087d8`（v315，suite 378／9）
- 內容：見 §1；測試：見 §3；落地數字：見 §5

## §1 改動（index.html＋content/gigs_new.json）

`gig_1992_rec_112`《追風少年》MV 男主角（唱片通告，中級，1992 春，搖滾，days 3，pay [330,396]，singer lok_gasing）升格做駱家聲支線回響通告：

1. `content/gigs_new.json`：加 `storyKeys: ["lok_gasing"]`＋`trigger: {kind:"credit", creditId:"credit_enc83_lok_patron", creditOwner:"駱家聲"}`。其餘欄位（title／tier／type／year／season／days／pay／req／synopsis／cast）一行都唔郁。
2. `index.html` `BR89_PATRON_OF_GIG`：加第 16 對 `gig_1992_rec_112:"credit_enc83_lok_patron"`（跟陸 film_101＋film_114 雙 gig 同一筆債權格式，註解寫明 v316）。其餘 15 對唔郁。
3. `rec_111`《銅鑼灣》唔郁（佢而家係 N14 tag＋lok trigger 共用）；`rec_102` 初級搖滾唔郁。
4. 註解舊數同步：BR89 映射表頭加 v316 第 16 對一行；`triggerGigOn`／`genericCreditOnGigComplete283`／`creditRedeemLine283`／`br89OnGigComplete` 註解入面「BR89 13／14 張」舊數一律改 16（v284 之後已漂移，今次一併執正）。

## §2 行為對照

| 情況 | 之前 | 之後 |
|---|---|---|
| 未持有 `credit_enc83_lok_patron` | rec_112 普通板通告（1992 春上板） | 隱藏（D-4 觸發前唔見） |
| 持有債權 | rec_111 一張兌現通告 | rec_111＋rec_112 兩張都開（`br89GigOn` 讀同一筆債權） |
| 殺青 rec_111 | 債權標 redeemedBy，rec_111 落板 | 同左，rec_112 同時落板 |
| 殺青 rec_112 | （普通殺青） | 債權標 redeemedBy，rec_111 同時落板 |
| 人情卡「可以換」行 | 淨《銅鑼灣》 | 《銅鑼灣》＋《追風少年》（BR89 反查自動） |
| 1992 春唱片中級板通告 | 6 張 | **5 張**（rec_112 轉觸發通告——D-4／D-11 既定機制，唔係回歸） |
| 通告庫總數 | 306 張 | 306 張（唔開新 gig） |
| 觸發通告總數 | 34 張（credit 23） | **35 張（credit 24；fame 5／rel 3／rival 1／story 1／wf3harvest 1／award 0 不變）** |
| BR89 映射 | 15 對 | **16 對** |

守住：`lok_patron` 閘（v314 嚴格閘）／對白／grants 唔郁；`rec_111`／`rec_102` 唔郁；`lok_patron_cold`／`lok_patron_cover` 唔郁；舊檔唔 crash。

已知限制（唔係呢票範圍）：rec_112 季窗係 1992 春；玩家遲過 1992 春先攞到 `lok_patron` 債權就趕唔切——同 rec_111 現狀一樣，唔喺呢票開接力 gig。

## §3 測試

新檔 `tests/test_r316_lok_echo.js`，20 項全 PASS：
- (0) 靜態：庫 306 張、觸發 35／credit 24、rec_112 tag＋trigger 齊、其餘欄唔郁、lok_patron grants 一致、v314 嚴格閘唔郁、rec_111／rec_102 唔郁、BR89 16 對逐對啱。
- (1) 未持有債權（包括持有陸引薦）：rec_112 唔上板。
- (2) 持有債權：兩張都開；窗口 1992-03-15 可見、1991-11-01 未入窗。
- (3) 雙 gig 互斥：殺青邊張，另一張自動落板；人情卡「可以換」出齊兩張名。
- (4) 舊檔：無債權／無 mockCredits／絕響債權，唔掟錯。

寫死總數嘅斷言同步（全部係計數，唔係行為改動）：
- `tests/test_gig229_pack.js` P7：34→35、credit 23→24。
- `tests/test_nat92_logic.js` E0：34→35（MAXED 由 pack 自動抽 credit，rec_112 照開；E2 普查 0 數 13／21／28 不變）。
- `tests/test_gig229_trigger.js` T0／T8／T10：34→35、BR89 15→16（EXPECT 加 rec_112）。
- `tests/test_br89_logic.js` H1：BR89 15→16（EXPECT13 加 rec_112）。
- `tests/test_r5_283_logic.js`：BR89 15→16、credit 23→24。
- `tests/test_r5_284_logic.js`：credit 23→24、BR89 15→16。
- `tests/test_gig291_winter.js` W4 標籤：P7 維持 34→35（斷言本身唔變）。
- `tests/test_sideline274_logic.js` A1／A2／D1：34→35、credit 23→24、BR89 15→16；**A2 實質改動**：v274「每筆債權只兌現一張」前提而家對駱 lok 例外（同陸 luk film_101＋film_114 前例一樣），A2 改為其餘 5 筆照一張、lok 恰好 rec_111＋rec_112 兩張。
- `tests/test_sideline158_logic.js` T8、`tests/test_sideline273_logic.js` (d)：BR89 15→16。

## §4 殘留

無。下一票：v317 候選齊鎮海（tv_114 高級男主角但齊只係配角格、無 tag 無 trigger）、v318 候選彭少祺（級＋崗位分咗兩張）——要設計決定；陸柏言行（SPEC 表有、計數同生成映射冇）要先拍板。

## §5 落地數字（填）

- 內容 commit：`e2e4cdb`
- NOTES commit：
- main HEAD：`e2e4cdb`
- Suite TOTAL：**379 PASS／9 FAIL**（基線 378／9；＋1 係新測試檔；9 項 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／44／49_static／wf5_87／wrap38）
- Pages：index.html md5 `8dba5e378b9a11787c4b56c1943ac0bb`／4,699,628 bytes，byte-identical，v316 標記在位
- 工作副本 `linji-work316`：已刪
- `qa296/derive296.json`：suite 再生嗰份已還原，唔入版
