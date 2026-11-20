# v355 NOTES — 支線＋感情線複檢嚴重 6 項＋製作備忘外露修復

Base: v354 (main `072553c`)。Suite: 398 PASS／9 FAIL（同基線一致，九項 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。

來源：`~/workspace/linji-story-review-side/verification.md`（GPT-6.2-sol 支線＋感情線全量複檢逐項核實表；220 項發現入面只修嚴重 6 項＋1 處製作備忘外露，其餘 200 項唔郁，留待另票）。

## 7 項修復

1. **雷勁弧說話人錯位**（s4 A1，`content/story_detail_rival_mentor.json`）：`A_lei_meet`／`A_lei_push2`／`A_lei_ending` beats 係雷勁↔張克凡對話，但簡介寫雷勁約阿偉、選項全係阿偉回應——cast 同 beats[1] speaker 改返阿偉。`A_lei_crisis` 阿偉全程冇出現、簡介／選項全係阿偉，唔係有意第三人在場——cast／speaker 改阿偉，「我哋唔會簽呢啲嘢」改「我唔會簽呢啲嘢」。`A_lei_push1` 唔郁（高俊傑介入幫阿偉講話，choice「找高俊傑幫忙擋住」→flag_ko_ally 合理，屬有意安排）。旗標／數值冇郁。
2. **葉敏芝 BE 後照 HE commit**（s8 A2，index.html `rom159PrepareNode`）：crisis 認錯寫入 `flag_yip_be_route` 後，pack ending HE 照寫 `flag_yip_commit`。跟 hiu_family_go 先例（v294）加檢查：who==="yip" && flag_yip_be_route → HE 換「差一步」變體（label「坦白心意：嗰晚我認咗，佢唔會再信我」，只寫 flag_yip_be，唔寫 commit／HE）。
3. **蘇芷茵 BE 後照 HE**（s8 A4，同法）：flag=`flag_so_played_safe`。HE 換差一步變體（「坦白心意：嗰陣我叫佢安全啲，佢唔會再講」，只寫 flag_so_be），同時換走 beats[0]／[1]／[3] 預設「錄完轉型歌」內容（佢冇唱嗰首歌，返去繼續做玉女）；beats[2]／[4] 保留。
4. **藍若曦＋徐寶珊 pack HE 冇正式拍拖**（s5 A1／s7 A7，設計規則 HE＝正式成為情侶）：保留 commit 旗，改文字。藍（JSON＋`ROMANCE_WF2_OVERRIDES` 覆寫表同步，兩邊 beats 逐字相同）：synopsis 尾句「誰都沒有接下去」→「等他接下去」；beat 4 刪「誰都沒有再往前走一步」改懸置（「遞到他面前——接還是不接，就看他這一句」）；beat 6「那一步，沒有走到」刪去改抉擇懸置；beat 8「冇人接」→「等佢接」（連貫性調整）；HE label 改「講明心意：唔使等第日——我想同你拍拖，唔係淨係一餐飯」，notes 改「HE：正式成為情侶、拍拖。…」。徐（只 JSON）：beat 8 改懸置（「她等著他的答案——這一句答下去，就不是一份禮那麼簡單」）；HE label 改「講明心意：兩個世界隔得遠，我都想同你拍拖」，notes 改「HE：正式成為情侶、拍拖。…」。兩線 BE 唔郁。文案避開 wf2_81 半線禁用詞（確定關係／伴侶／承諾／一齊走下去），beats 關鍵詞（通告牌／食飯／錶）同字數底線保留。
5. **蘇芷茵巧遇「一句都冇出聲」**（s15 A1，index.html `ENC84_DLG_so_jiyan` first.choices）：choices[0] 蘇芷茵句「由頭到尾一句都冇出聲」→「冇多講嘢」（共通段阿偉已開口三次）；choices[1] label「讓開站到一邊」→「擋完就讓開」（保留 fx 關鍵字「讓開」），旁白改「阿偉擋完就退開兩步」，蘇芷茵句改「頭先唔該你擋一擋」。
6. **魏詠男旁白他／她混用**（s11 A1，index.html `ENC83_DLG_ngai_wingnaam`＋`ENC83_FRAME_ngai_wingnaam`）：指魏詠男嘅「他」改「她」共 8 處（first 旁白＋汽水 label、照著他一個人的影子、heart 旁白、ngai_help 旁白＋大排檔／熱茶 label、stageup 旁白）。指阿偉／複數／顧明輝嘅「他」唔郁。fx 關鍵字（汽水／大排檔／熱茶）保留。
7. **製作備忘外露**（s8 B4，`content/story_detail_romance_yip_so.json` R_yip_push1 `C_yip_push1_keep` notes）：「經理人人情債權由 ENC79 鏈 D 嗰拍（yip_choice 守口 fx）兌現，呢度唔重複派，免得同一筆人情派兩次」→玩家面文字「呢份人情，佢以後會還返俾阿偉」。同節點 leak choice notes 嘅「標籤種子寫入」唔在範圍，唔郁。

## 測試改動

- `test_weave48_logic.js`：藍 HE label 期望值跟新文案。
- `test_rom159_static.py`：CMT_lan_commit 釘行 26371→26405（+34 純漂移）；v347 精確替代斷言加 v355 層（_FIX355 9 處：cast／speaker／crisis 一句），斷言名改 v347＋v355。
- `test_rom159_yipso_static.py`：守口 notes 斷言反轉——改驗玩家面文字（冇 ENC79／fx 術語、有「以後會還」）。
- `test_gift185_static.py`／`test_tang171_static.py`／`test_tang173_static.py`：總行數 47386→47420（帳目加 ＋v355 +34）；tang 兩檔 openLoc DEF 42606→42640。
- `test_rom176_static.py`：4 個釘行各 +34（40833→40867、41183→41217、42486→42520、42647→42681）。
- `test_travel114_static.py`：COUNT／FREE／DEF／WRAPPER 釘行 >26327 者各 +34（33 處），逐行核實 openLoc( 錨點內容相同。

index.html 淨 +34 行（rom159PrepareNode 葉／蘇 BE 閘，插入點舊 L26327 之後），47,386→47,420 行。

## 實駕抽查（Playwright，`~/workspace/linji-drive355/`）

- 葉 BE 閘：播種 flag_yip_be_route → ending HE 換坦白變體；真撳選擇＋reconfirm 確定後 flag_yip_be=true、flag_yip_commit／flag_yip_he=false。冇行 BE → HE 照常（label 原版、flags 含 commit）。
- 蘇 BE 閘：播種 flag_so_played_safe → beats 換走轉型歌（「沒有錄那首轉型歌」／「嗰首歌，我最後冇唱」）、HE 換坦白變體；撳完 flag_so_be=true、commit／he=false。冇行 BE → beats 原版、HE 照常。
- 藍／徐 HE：新 label＋「正式成為情侶、拍拖」notes 渲染正確；撳完 flag_*_commit／flag_*_he=true；藍 beats 通告牌＋食飯、徐 beats 錶保留，舊「那一步，沒有走到」／「那句話留在心裏就算了」清零。
- 雷勁弧：A_lei_meet／A_lei_crisis session cast=[雷勁，阿偉]、speakers=[雷勁，阿偉，雷勁，雷勁]；crisis 阿偉句「我唔會簽呢啲嘢」在場、舊「我哋唔會簽」清零。
- 截圖：`~/workspace/linji-drive355/shots/`（yip_be_c／so_be_c／lan_he_c／xu_he_c／lei_meet 等）。
