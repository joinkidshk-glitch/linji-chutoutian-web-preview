# NOTES_V20A308 — Q20 駱家聲 heart cover 版變體（關鍵句換懷疑版）

- 版本：v308（Q20）
- 基線：main `4547692`（v307 已落地，suite 370／9）
- 工作副本：`~/workspace/linji-work308`（分支 `v308-lok-heart-cover`，落地後已刪）
- 改動範圍：`index.html` 淨改 1 處（L40239–40241，+3／−1 行）＋新測試 `tests/test_r308_lok_heart_cover.js`

## 1. 問題

現行 cover 版做法（v278，舊 L40239）：`lok_cover_first` 旗嗰陣，喺 heart 第 4 句之後**插入**懷疑句「呢首，我唔知仲唱唔唱得出。」——插入句同之後嘅肯定關鍵句（index 10「歌係自己嘅，嗰種實淨，冇人攞得走」）隔籬互相打架（懷疑同肯定並存），唔係真變體。

## 2. 做法

cover 版唔再插入懷疑句，改為將 heart 關鍵句（index 10）**換成**懷疑版——同一主題反面講：

| | 句 |
|---|---|
| 舊關鍵句（非 cover 版，留返） | 「不過呢，阿偉，歌係自己嘅，嗰種實淨，冇人攞得走。你明唔明？」 |
| 新懷疑版（cover 版） | 「不過呢，阿偉，歌係自己嘅——呢句我講咗咁多年，而家先發覺，我連自己仲唱唔唱得出，都唔敢肯定。你明唔明？」 |

- 換句唔係加句：cover 版 heart 仍係 12 句，其餘 11 句逐字唔變；玩家回應句（index 11「我明。唔怪得你嗌交嗌到咁大聲，都唔肯改嗰幾粒音。」）照接得上（「你明唔明？」尾句保留）。
- 按內容搵句，唔按 index：用 `findIndex` 搵舊關鍵句原文再換——`lok_tried_harmony` 插入句會將關鍵句由 index 10 推後到 11，寫死 index 會換錯句。`findIndex` 搵唔到就唔換（guarded，舊檔／異常唔 crash）。
- 變體只改副本：`l278 = heartSeg278.lines.slice()` 淺拷貝之後先換，source `D.heart.lines` 唔污染（測試 E 核實：cover 跑完再跑非 cover，逐字還原）。

## 3. 守住（全部唔郁）

- 非 cover 版 heart 12 句逐字唔變。
- 其餘兩句：Beat 5 呼應句（L37508「……榜係人排嘅，歌係自己嘅。你呢句，我收落個心度。」）、提攜應用句（L37534「係，我講過。不過我話你知，企到台中間嗰陣……」）。
- `lok_cover` beat（L37453）同 `lok_cover_first` 旗（L37480）唔郁；暖版閘（L39787，cover_first 排除暖版）唔郁；`lok_patron_cover` 閘（L41774）唔郁。
- 播完效果同暖版一樣：heartDone＋好感＋2（變體只改文字，唔改獎勵）。
- 舊插入句「呢首，我唔知仲唱唔唱得出。」全檔消失（grep 0 命中）。
- 對白廣東話；舊檔唔 crash（測試 D 舊檔 case）。

## 4. 測試

新測試 `tests/test_r308_lok_heart_cover.js`（27 項，全 PASS；sandbox 跟 v304 同一套抽取＋eval）：

- (A) cover 版：12 句、index 10 係懷疑版、舊關鍵句／舊插入句唔見、懷疑版只出現一次、其餘 11 句逐字唔變、抉擇照在位、玩家回應句照在位。
- (B) 非 cover 版 12 句逐字等於 source；cover＋harmony（13 句，問句 index 5，關鍵句推後到 11 照換）；cover＋honest（13 句，收尾附加句最尾，關鍵句照換）；harmony 單獨（13 句，關鍵句 index 11 照係舊版）。
- (C) Beat 5 呼應句／提攺應用句在位；舊插入句全檔消失。
- (D) lok_cover beat／旗／暖版閘／patron_cover 閘在位；播完 heartDone＋好感 45→47；舊檔（得 fav／met）唔 crash、照播懷疑版。
- (E) source 唔污染；cover 跑完再跑非 cover 逐字還原。

### 4.1 舊測試更新（預期行為改咗，唔係回歸）

- `tests/test_sideline278_logic.js` 兩處斷言寫死舊做法，同步改做 v308 新行為：cover_first 斷言改做「關鍵句換懷疑版、12 句、舊句／舊插入句唔見」；三變體疊加斷言改做「問句＋懷疑版＋收尾附加句在位、舊插入句唔見」。
- 行數釘 resync（改動淨 +3 行，1 行→4 行＠舊 L40239）：difflib 核實唯一 hunk 係呢個改動，37 處錨點內容逐字相同、純漂移；五檔同步 ＋3——`test_gift185_static.py`（總行數 47239→47242）、`test_tang171_static.py`／`test_tang173_static.py`（總行數＋openLoc DEF 42448→42451＋DEF guard 42454→42457／index 42447→42450）、`test_rom176_static.py`（4 釘行 40680→40683／41030→41033／42333→42336／42489→42492）、`test_travel114_static.py`（COUNT 4 處＋FREE 24 處＋DEF 42448→42451；插入點之前嘅錨點唔郁）。

## 5. Suite＋落地

- 全套 suite（第二輪重跑）：**TOTAL PASS 371 FAIL 9**——9 項全部係已知 pre-existing FAIL（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）；新測試 test_r308 全 PASS。第一輪 365／15 係上述舊斷言＋行數釘未同步，逐個直接覆驗後全部修返，唔係回歸。
- Pages 核實：見 §5（落地時填實數）。

## 6. 殘留

無。Q20 結案。
