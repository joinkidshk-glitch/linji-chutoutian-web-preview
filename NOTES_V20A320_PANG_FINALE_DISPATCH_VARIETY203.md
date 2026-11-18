# NOTES_V20A320_PANG_FINALE_DISPATCH_VARIETY203

## 1. 任務一句話
彭少祺好收尾 `pang_finale` 派 `gig_1991_variety_203`《台慶大騷》台上助理——finale grants() 加
`grant229Record`，兌現草稿 L1545 提案同 finale 對白第 6 句「聽日」承諾。

## 2. 改動（index.html 淨改 1 行，對白零改動）
- `pang_finale` registry 條目（L41877）加 grants()，跟 `luk_tease`（v271）寫法一式一樣
  （try／catch＋typeof 守衛）：
  `grants(){ try{ if(typeof grant229Record==="function") grant229Record("gig_1991_variety_203", "彭少祺支線", "第二朝，彭少祺話：聽日台慶大騷嗰邊爭個台上助理，我同監製講咗聲，你去試下啦。"); }catch(_g){} }`
- 守住：`pang_finale` 閘＋對白逐字唔郁；`pang_finale_cold` 唔加 grants；n17 GRANT229 兩行
  （ad_107／tv_301）唔郁；variety_203 trigger／BR89／storyKeys 唔郁；`pang_patron` 閘／grants
  唔郁；variety_106 唔郁；舊檔唔 crash。
- 計數零改動：庫 307 張、trigger 37（credit 26）、BR89 18 對。

## 3. 點解 n17 容納唔到兩份提案（草稿兩份提案）
草稿對同一個抉擇 A 寫咗兩份第二朝派送提案：
- L1528–1529 抉擇即派表：A → 西裝廣告《頒獎禮前哨》（live 已實裝做 GRANT229 L27142，
  `beat:pang_n17`／key「雲吞麵」→ `gig_1991_ad_107`《安穩一生》）；
- L1545：A → 《台慶大騷》台上助理，兌現 `credit_enc84_pang_patron`。
`grant229RecordFromEnc79` 同一 seg 第一命中即回傳，一個抉擇只派一張——n17 再加一
行「雲吞麵」→ variety_203 係死 code（ad_107 排先）；調轉次序會殺咗西裝廣告，推翻草
稿自己份即派表。所以第二份提案改由 `pang_finale` grants() 派——finale 無抉擇，
seg hook 行唔到，grants() 直接記低係唯一出路（`luk_tease` v271 前例）。

## 4. 派送機制
- `pang_finale` 播出嗰晚 grants() 記低 variety_203，dueDay＝聽日、一生一次
  （`grant229_recorded_` 旗）；第二朝晨鏈 `grant229PresentDue` → `grant229DeliverOne`
  直接獲聘，簽約金＝pay 中位數三成（variety_203 pay [200,240] → 中位數 220 → $66），
  餘額殺青入帳；已獲聘／已殺青／等緊消息／已預約嗰陣跳過（`grant229IsConsumed`）。
- 殺青 variety_203 → `br89OnGigComplete` 標債權 redeemedBy，variety_106 自動落板
  （同筆債權雙 gig 前例：陸 film_101＋film_114、駱 rec_111＋rec_112、齊 film_206＋tv_114、
  彭 variety_203＋variety_106）。
- Registry 次序 finale（L41877）排 patron（L41878）之前——暖版 T3 玩家先播 finale，
  派送嗰陣未必持有 patron 債權；按 finale 對白（「我同監製講咗聲」）嚟講係合理嘅，
  唔係 bug。唔喺派送加持有債權條件。

## 5. 逐類玩家影響表
| 玩家 | 影響 |
|---|---|
| 暖版三旗（cover＋listened＋noodle） | finale 播出嗰晚記低 variety_203，第二朝何生電話直接獲聘（簽約金 $66）；殺青標 redeemedBy，variety_106 落板 |
| 已經用 variety_106 兌現咗債權 | finale 照派 variety_203（新機會，唔係重複兌現）；殺青唔重標 redeemedBy |
| 已經用 trigger 攞過／做過 variety_203 | `grant229IsConsumed` 派發嗰陣跳過，唔重派；`grant229_recorded_` 一生一次，finale 唔重複記低 |
| 冷版（early_night／absent／brushed_off／late） | 行 `pang_finale_cold`，無派送，對白亦無承諾 |
| n17 揀 A 玩家 | 照派 ad_107（另一條 queue、更早 dueDay）＋finale 再派 variety_203；1992 冬得 12 月一個月，兩張直接獲聘（各 2 日）時間上做得完 |
| 舊檔 | 已播完 finale 但未拎過 variety_203 嘅舊檔唔追溯（finale 只播一次）；未播 finale 嘅舊檔照新機制派 |

## 6. 測試
- 新檔 `tests/test_r320_pang_finale_dispatch.js`：**20 項全 PASS**（靜態 8＋行為 12）。
  靜態：grants 派 variety_203、閘逐字唔郁、冷版無 grant229Record、n17 兩行唔郁、
  無 GRANT229 死 code 行、variety_203 trigger／storyKeys 唔郁、BR89 第 18 對在位、
  庫 307／trigger 37／credit 26。
  行為：DLG 7 句＋第 6 句承諾逐字唔郁、冷版無 grants、grants 一次記低（dueDay＝聽日）、
  第二次唔重複、簽約金 220→66、殺青標 redeemedBy＋variety_106 落板、再標冪等、
  已兌現照派＋唔重標、grant229IsConsumed 四態跳過、n17 A 共存（ad_107 更早 dueDay）、
  n17 B 共存（tv_301＋冷版乜都唔派）、BR89 18 對。
- 全套 suite：見 §5。

## 5. 落地
- Main HEAD：`3ed34e7`（內容 `e5f59df`＋本 NOTES §5 補填）
- Suite：TOTAL PASS 383 FAIL 9（基線 382／9，＋1 係新測試檔；9 項 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／44／49_static／wf5_87／wrap38）
- Pages byte-identical：index.html md5 `61a46fc8b165a538527b74cda3c20f8e`／4,701,234 bytes，v20a320 標記在位
- 工作副本 `linji-work320` 已刪；`qa296/derive296.json` 已還原，唔入版
