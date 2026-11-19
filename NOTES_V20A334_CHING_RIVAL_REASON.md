# NOTES_V20A334_CHING_RIVAL_REASON.md

## 一、改動（index.html 淨 ±0 行，47,256 行不變）

只改 GRANT229_ENC79 一句 reason（L27115，程天諾支線 `beat:ching_rival` 揀 B「走先」，
gigId `gig_1991_tv_205`）。

舊句（逐字）：
> 第二朝，何生打電話嚟：聽朝《碼頭故事》工友群戲，朝早六點到，唔好遲到。啟德機場送機群演，聽朝去報到。

新句（逐字）：
> 第二朝，何生打電話嚟：聽朝啟德機場送機群演，朝早六點到，唔好遲到。

## 二、原因

- 全庫根本冇《碼頭故事》呢張通告——改前 `grep -rn "碼頭故事" index.html tests/ content/ docs/` 得 L27115 一處。
- `gig_1991_tv_205` live 標題就係「啟德機場送機群演」（1991 春，臨記，tvb_kowloon）。
- 舊句同一句入面講咗兩樣嘢，互相矛盾；新句三條約束全部滿足：①講明係啟德機場送機群演，唔再提《碼頭故事》；②保留「朝早六點到，唔好遲到」；③唔重複寫兩次崗位名（刪咗尾句「啟德機場送機群演，聽朝去報到」）。
- 對白（廣東話），唔使改書面語。gigId／key／seg／其他行全部唔郁。

## 三、驗收

- 改後 `grep -rn "碼頭故事" index.html tests/ content/ docs/` ＝ 0 命中。
- 冇測試釘死舊句（改前 grep tests 「啟德機場送機群演」0 命中）；同行替換，總行數不變，唔使 resync（qa334 無 resync 腳本）。
- 全套 suite：見 §四。

## 四、測試

- 工作副本全套 suite：**TOTAL PASS 387 FAIL 9**＝v333 基線，9 項 FAIL（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）同基線逐項一致，零回歸。第一跑即達，唔使第二跑。
- 冇測試釘死舊句；同行替換，總行數不變，唔使 resync。

## 五、落地

- （填：內容 commit、main HEAD、Pages md5／bytes）

## 六、跟進（唔係本票）

- 攻略引文（程 Beat 2 B）逐字抄舊句，parent 另外做攻略同步，修好遊戲原文之後先改攻略引文。
