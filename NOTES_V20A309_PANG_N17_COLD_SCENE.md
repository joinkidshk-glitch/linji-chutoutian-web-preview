# NOTES_V20A309 — Q22 彭少祺 n17 brushed_off 冷版場面

- 版本：v20a309；基線 main `285e621`（v308，suite 371／9）；落地後 suite 372／9（9 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。
- 問題：`pang_brushed_off` 旗（heart 嗰晚揀「笑著說他想多了」授出）之前只讀於 `pang_finale_cold` 閘；`pang_n17` 一律行暖版——彭喺頒獎禮後台咁多人入面第一個行埋嚟。草稿 PLAN L130 淨寫後果，冇逐字稿。

## 改動（index.html 淨 +33 行）

1. 新 seg `pang_n17_cold`（`ENC84_DLG_pang_siuki.beats`，新 L38159–38187，+29 行）：7 句主線＋2 個選擇。
   - 冷版場面：彭企喺人群中間，見親人都叫得出名，個個都笑住應佢；阿偉行埋去，佢只係客套一句「監製啱啱嗌我過去對流程，你自己周圍行下先啦」，轉身就繼續同監製講流程，連頭都冇回，「唯獨沒有再望向自己」。阿偉望住佢背脊，諗返起 heart 嗰晚：佢講到收工想有人陪佢食碗麵，自己笑住話佢諗多咗，佢塊面僵咗一下——「當時告訴自己是看錯，現在才知道沒有看錯」。
   - 暖版對照：暖版係「咁多人入面第一個行埋嚟，因為玩家嗰晚肯靜靜聽」；冷版係「佢喺度但唔行埋嚟」，玩家親眼見到距離。
   - 兩個選擇照留，label 照含對位關鍵字，授旗同暖版一樣：雲吞麵（「自己去廟街食碗雲吞麵，坐低等佢」，`pang_noodle_night`）／返屋企瞓（「趕住返屋企瞓，聽日仲有工開」，`pang_early_night`）。冷版回應唔同暖版：食麵嗰邊係阿偉自己去老地方坐低等，彭話「隨便你啦。呢行就係咁，邊個等邊個，冇人講得準」；瞓覺嗰邊彭只係客套一句，唔再提碗麵。
2. `enc79BuildScript` beat 分支分流（新 L40146–40149，+4 行）：`beat.id==="pang_n17" && pang_brushed_off` 嗰陣將 `beatSeg100` 換成 `D.beats.pang_n17_cold`。
   - 設計取捨（跟 v304 heartCold 分流模式，但用 seg 換唔係獨立 beat）：beat.id 照係 `pang_n17`，所以 segKey 照用 `"beat:pang_n17"`（GRANT229 即派＋`enc79ChoiceFx` fav 對位唔郁）、`beatsDone.pang_n17` 照標、`grants()`（`sideline280GrantCompletion("pang")`）照行、`pang_finale_cold` 閘（n17 做完＋brushed_off）照去得到。唔使改註冊表、唔使改收尾閘。

## 守住（全部有測試覆蓋）

- 暖版 `pang_n17` 7 句＋2 選擇逐字唔郁；`pang_n17` 註冊閘（tier≥3＋1992 冬，無旗條件）唔郁；`pang_finale_cold` 閘＋對白唔郁。
- 冷版唔派暖線收尾獎勵：`sideline280GrantCompletion("pang")` 要齊 `pang_cover_night`＋`pang_listened`＋`pang_noodle_night` 三旗；brushed_off 玩家缺 `pang_listened`，冷版 n17 照行 grants 都唔會誤派（聲望唔郁）。暖版收尾 `pang_finale` 同樣缺 `pang_listened`，開唔到。
- 冷版選擇 GRANT229 照派同一張通告（雲吞麵→`gig_1991_ad_107`《安穩一生》／返屋企瞓→`gig_1992_tv_301`《便衣幹探》），fav 照計（雲吞麵 +3／返屋企瞓 +1）。
- 舊檔唔 crash：已有 brushed_off、頭兩幕已做嘅舊 save 照播冷版。

## 測試

- 新 `tests/test_r309_pang_n17_cold.js`：27 項全 PASS（A 數據／B 暖冷分流＋選擇／C 播完接駁／D GRANT229＋fav／E 舊檔／S 靜態）。
- `tests/test_sideline278_logic.js`：(6) 67 旗 guard 要修訂——`pang_noodle_night`／`pang_early_night` 由各 1 次改為各 2 次（暖版＋冷版各授一次，同一個 beat、同一對旗，冷版照留兩個選擇係 brief 要求；其餘 65 旗各 1 次不變）。修訂有註解，測試全 PASS。
- 行號漂移：`qa309/resync309.py`（difflib 對位核實純漂移，單次掃描 dict 查表）：gift185 總行數、tang171／tang173 總行數＋DEF＋guard、rom176 4 釘、travel114 DEF＋COUNT 4 處＋FREE 40 處，全部按段 ＋29（38159–40116）／＋33（≥40117）重算。初版漏咗 FREE 第 40 處（舊 L46564，v183 C9），已補返，travel114 PASS。

## 落地

- main HEAD：`13333eb`（squash merge，工作副本分支 commit `5d0eb1c`）
- Pages：byte-identical，index.html md5 `2c9bb88fcfffa0db6e17f2a2ca0e8fa5`／4,697,075 bytes
