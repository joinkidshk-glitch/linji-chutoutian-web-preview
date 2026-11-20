# v354 NOTES — 主線複檢餘下兩類修復（待潤飾 34 項＋resultBeats 13 項＋漏報 N6_b）

Base: v353 (main `54c6782`)。Suite: 398 PASS／9 FAIL（同基線一致，九項 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。

來源：`~/workspace/linji-story-review-gpt/verification.md`（GPT-6.2-sol 全量複檢逐項核實表）。v352 已修 26 項玩家面矛盾、v353 已修 8 項文風取捨；今次清埋餘下 (b) 類證實 34 項＋(a) 類 resultBeats 層面 13 項。誤報 3 項（s6A5／s6A9／s4B2）冇郁。

## 待潤飾 34 項（全部改 `content/story_detail_n1_to_n17.json`，除註明外）

1. s1B2 N1_a notes：「是他好彩」→「已屬難得」
2. s1B3 N2 beats[4]：「是真的有得做」→「是真的有戲份」
3. s1B4 N2 beats[7]／[8]：刪重複小巴交代；「留下，聽多兩句」→「留下多聽幾句，還是上車準時報到，阿偉要立刻決定」
4. s1B5 N2_a notes：「講古」→「說舊事」；「會提他一把」→「會第一個想起他」
5. s2B2 N3 beats[6]：心聲串層改第三人稱旁白（「阿偉想起之前聽過的傳聞——高俊傑成日搶鏡，今天終於輪到自己」）
6. s2B3 N4 beats[7]：「捱到天光」→「熬到天亮」
7. s2B4 N4_a notes：「想不起你」→「想不起阿偉」
8. s2B5 N4_b notes：「換來何生一句捱得」→「換來何生一句「捱得」的評價」
9. s2B7 N5_a notes：「講出／夠真誠／這個料」→「說出／夠坦誠／這些消息」
10. s2B9 N6_b notes＋rb[2]：「學他那時一樣」→「像他當時一樣」（N6F_b 同詞兩處一併同步，見下）
11. s3B1 N6F playerOffer：「定繼續跑」→「由開鏡跟到殺青，還是繼續跑通告？」
12. s3B2 N18 playerOffer：「來年點行」→「來年怎樣走——學幕後，還是專心幕前？」
13. s3B3 N19 playerOffer：「企賭枱邊／本份」→「站在賭桌邊／本分」（同 label 統一）
14. s3B4 N19 beats[1]：「撲去拍賭片／今個月第三套」→「趕拍賭片／這個月第三套」（synopsis 同詞一併同步）
15. s3B5 N19 synopsis：「做賭客幫忙，在桌邊」重複 →「充當賭客」
16. s3B6 N6F_a notes＋rb[2]：刪天天報到重複；「撥了一支煙」→「遞了一支煙」
17. s3B8 N18_a rb[1]：第一人稱冒號加引號
18. s4B1 N7 synopsis：「識不識演戲／識不識做人」→「演技如何／懂不懂做人」
19. s4B3 N10 synopsis：「他企邊，哪邊記住」→「他站在哪邊，哪邊就記住他」
20. s5B2 N11 beats[7]：「誰就有工開」→「誰就有工作」
21. s5B3 N12 synopsis：分支說明改劇情交代
22. s5B5 N13 beats[10]：何生掛名旁白改系統旁白回憶（speaker 何生→系統，內容改「阿偉想起何生在事務所提過的一句話：「…」」）
23. s5B6 N13 synopsis＋N14 beats[9]：「企邊哪邊」→「站在哪邊」
24. s5B7 N14 synopsis：「去唱片公司交代」→「去唱片公司交一疊通告帶」
25. s5B8 N14 playerOffer＋playerHint：「你企邊邊？」→「你站在哪邊？」（aftermathHint 同詞一併同步）
26. s5B9 N14 beats[15]：「剛剛」連用改順
27. s6B1 N15 playerOffer：「靠修音，定練真功夫？」→「靠修音，還是練真功夫？」
28. s6B2 N15_a rb[2]：「放下了一個標籤」→「給他貼上了一個標籤」（同 s6A1 重寫一齊做）
29. s6B3 N16 setting：「趕住年初一上畫」→「趕在年初一上映」
30. s6B4 N16 synopsis：代擬口語問句改書面提問
31. s6B5 N16_c notes：「搏一搏」→「試一試」
32. s6B7 N17_410_b notes＋index.html runtime（endingEveOptions410 三處）：「講明先：」→「先說清楚：」（index.html 同行替換，行數不變）
33. s6B8 N17_epi synopsis：全段口語改書面
34. s6B9 N17_epi beats[0]：「行出」→「走出」

同詞同步（核實表未點名但同詞同節點，一併處理）：N6F_b「學他那時一樣」×2、N19 synopsis「撲去拍賭片」、N14 aftermathHint「你企邊邊」。

## resultBeats 13 項＋漏報（只改數據文字，播放器冇郁；notes 保留，改 resultBeats 邊）

1. s1A2 N2_b rb[3]：共通收尾跳返後巷 → 電視城走廊版（保留「坐在摺凳上的那個人」收尾標記）
2. s2A1 N3_b rb[3]：引「等住睇」→ 改引真講過嘅「唔好阻住我」
3. s2A2 N4_b rb[1]：「聽晚準時」→「今晚準時」
4. s2A3 N4_b rb[3]：共通收尾跳返事務所 → 返屋企版
5. s2A6 N5_b rb[2]：刪「收起筆記本」（唔再演兩次）
6. s2A7 N5_b rb[3]：「不會再問同一條問題」→「還會再問——只是問法會不同」
7. s2A8 N5_c rb[3]：「說了一半」→「一句都沒有說」
8. s3A2 N6F_b rb[3]：「在等下一個肯跟的人」→「只是站的人換了」（N6F_a 共通尾句一併改）
9. 漏報 N6_b rb[3]：「在等下一個肯坐下的人」→「只是坐的人換了」（N6_a 共通尾句一併改）
10. s5A6 N12_a／b rb[2]：同 notes 逐字重複 → 改寫 rb 講法
11. s5A7 N13_a／b／c rb：同 notes 逐字重複 → 改寫 rb 收尾句
12. s5A8 N14_a／b／c rb：同 notes 逐字重複 → 改寫 rb 收尾句
13. s6A1 N15_a／b rb[2]：同 notes 逐字重複 → 改寫 rb 講法（N15_a 含 s6B2 標籤修復）
14. s6A2 N16_a／b／c rb[2]：同 notes 逐字重複 → 改寫 rb 收尾句

## 測試改動

- `test_story157_pack_static.py`：nodes[5:] sha 重算（`d3c47bb9…`）＋v354 註解一行。
- `test_rom159_static.py`：`_ml_touched` 加 N7／N10／N13／N15；加 v354 兩組精確斷言（34 項新句在場舊句清零、resultBeats 新收尾在場舊收尾清零）。
- `test_wf1_80_logic.js`＋`tests/fixtures/spine_n6_n17_v136.json`：N17_410_b notes 意圖改動，fixture 同步一處＋註解。

SAVE key／softRev／年份字串／旗標／數值全部冇郁。index.html 只改 3 行同行字串（講明先→先說清楚），47,386 行不變，零釘行漂移。
