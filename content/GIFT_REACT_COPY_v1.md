# 《臨記出頭天》送禮反應對白短稿 v1

> **用途：** 可直接換掉 iOS／預覽引擎短佔位反應；定稿文案，未接 LIVE story JSON。  
> **狀態：** Soft≠PASS · 出圖 HOLD · **未改 LIVE story JSON**  
> **日期：** 2026-11-03（Asia/Hong_Kong）  
> **對齊：** `PLAN_GIFT_SHOP_STORY_v1`（22 件＋喜好／踩雷＋crisis）· `PLAN_GIFT_SHOP_ALIGN_NOTE_v1`（簽核 likes）· `PLAN_GIFT_SHOP_v1`（cap：日 1／週軟＋2／單次硬＋2）  
> **文風：** 香港書面語、現代易讀；對白稍長自然；禁自造縮寫（見 `COPY_STYLE_HK_LEXICON`／`COPY_STYLE_MODERN_v1`）  
> **欄位：** `npcKey` · `itemId` · `pref`（liked／neutral／dislike）· `lines`（1–3 句對白＋可選 narration）· `crisisVariant`（可選）  
> **同步：** content ＋ bot store 同名檔

---

## 0. 用法說明（eng／iOS）

1. 以 `(npcKey, itemId)` 查表；若無專屬條 → 可 fallback 該角 `pref=neutral` 通用句（文末 §7）或引擎短佔位。  
2. `crisisVariant` 僅在對應主線危機章／romance crisis 觸發時覆寫 `lines`；平時用主條。  
3. 數值仍跟 cap：單次 liked ≤＋2；dislike 硬 −1；週軟＋2 超出只播「心領」（§7）。  
4. 鄧麗萍所有條 **須** `flag_tang_open`；未開 → 用鎖定提示，不播本檔對白。  
5. Soft≠PASS；本檔＝文案資產，**唔**當系統已 PASS。

---

## 1. 條數總表

| npcKey | 角色 | liked | dislike | neutral | crisisVariant 附條 | 主條合計 |
|---|---|---:|---:|---:|---:|---:|
| `vera` | Vera | 5 | 3 | 3 | 2（T5／C12 向） | **11** |
| `hiu` | 林曉晴 | 6 | 3 | 3 | 1（C12） | **12** |
| `choi` | 周采兒 | 4 | 3 | 3 | 1（C13 向） | **10** |
| `lan` | 藍若曦 | 4 | 2 | 2 | 3（C9／C15） | **8** |
| `xu` | 徐寶珊 | 3 | 3 | 2 | 2（C14） | **8** |
| `tang` | 鄧麗萍 | 3 | 1 | 2 | 0 | **6**（`flag_tang_open`） |
| | **合計主條** | | | | | **55** |
| | crisis 附條（另計） | | | | **9** | |

---

## 2. Vera（`vera`）｜造型師 · 克制、講形象

### 2.1 liked

#### GR-vera-silk_scarf｜liked
- **npcKey:** `vera`  
- **itemId:** `gift_silk_scarf`  
- **pref:** `liked`  
- **lines:**
  - Vera：「這條顏色很乾淨，不會搶鏡頭，也適合日常出門。你有想過我平常穿什麼，還是碰巧選中？」
  - Vera：「算你有眼力。下次如果再送，記得避開大印花——素色才耐看。」
  - **narration:** 她把絲巾對折，在鏡子前比了比，嘴角幾乎看不出來地鬆了一下。

#### GR-vera-fashion_mag｜liked
- **npcKey:** `vera`  
- **itemId:** `gift_fashion_mag`  
- **pref:** `liked`  
- **lines:**
  - Vera：「這本我找了很久，片場附近通常只得過季的。你怎麼知道我想看這期的剪裁專題？」
  - Vera：「別以為我只會盯你襯衫。真正有用的參考，是別人怎麼處理肩膀和領口。」
  - **narration:** 她翻到中頁停住，指尖在圖片邊沿點了兩下，像已經開始盤算下一場造型。

#### GR-vera-perfume_sample｜liked
- **npcKey:** `vera`  
- **itemId:** `gift_perfume_sample`  
- **pref:** `liked`  
- **lines:**
  - Vera：「淡的就好。濃的在密閉化妝間會薰到別人，也會蓋過粉底的味道。」
  - Vera：「你有問過店員濃度，對不對？……還算細心。」
  - **narration:** 她只在手腕內側點了一下，聞過之後就把蓋子蓋回，沒有當眾誇張地噴。

#### GR-vera-hair_clip_set｜liked
- **npcKey:** `vera`  
- **itemId:** `gift_hair_clip_set`  
- **pref:** `liked`  
- **lines:**
  - Vera：「低調的小物反而實用。拍特寫時，頭髮一亂，再好的妝都會散。」
  - Vera：「謝謝。這種東西我寧願自己備，但你送來，我收下。」

#### GR-vera-rose_premium｜liked
- **npcKey:** `vera`  
- **itemId:** `gift_rose_premium`  
- **pref:** `liked`  
- **lines:**
  - Vera：「花可以，包裝也不俗氣。你是想說什麼，還是只想我看見紅色？」
  - Vera：「我收下。不過別以為送花就能代替準時——通告前十分鐘到，比玫瑰重要。」
  - **narration:** 她把花束放進造型間角落的玻璃瓶，動作乾淨，沒有多餘的感嘆。

### 2.2 dislike

#### GR-vera-set_soda｜dislike
- **npcKey:** `vera`  
- **itemId:** `gift_set_soda_pack`  
- **pref:** `dislike`  
- **lines:**
  - Vera：「汽水？你是請我幫忙看造型，還是請我去片場小賣部值班？」
  - Vera：「拿回去吧。衣服和皮膚都要乾淨，這種東西放我桌上，感覺就不對勁。」

#### GR-vera-pineapple｜dislike
- **npcKey:** `vera`  
- **itemId:** `gift_pineapple_bun_set`  
- **pref:** `dislike`  
- **lines:**
  - Vera：「街坊套餐我明白是心意，但你送給造型師，就像叫我帶油煙味進試衣間。」
  - Vera：「下次想請吃，約下班再說。工作中，我寧願你帶一條乾淨的手帕。」

#### GR-vera-egg_tart｜dislike
- **npcKey:** `vera`  
- **itemId:** `gift_egg_tart_box`  
- **pref:** `dislike`  
- **lines:**
  - Vera：「禮盒可以很有誠意，也可以很隨便。這盒……比較像後者。」
  - Vera：「不是貴賤問題，是你有沒有想過對方是誰。你再想想。」

### 2.3 neutral

#### GR-vera-daisy｜neutral
- **npcKey:** `vera`  
- **itemId:** `gift_daisy_bunch`  
- **pref:** `neutral`  
- **lines:**
  - Vera：「雛菊很清爽，放化妝枱不會礙事。謝謝。」
  - **narration:** 她點點頭，把花束放到一邊，沒有多問來意。

#### GR-vera-memo｜neutral
- **npcKey:** `vera`  
- **itemId:** `gift_memo_pad`  
- **pref:** `neutral`  
- **lines:**
  - Vera：「拍紙簿？我可以拿來記尺寸。不算特別，但用得著。」

#### GR-vera-thermos｜neutral
- **npcKey:** `vera`  
- **itemId:** `gift_thermos`  
- **pref:** `neutral`  
- **lines:**
  - Vera：「實用就好。造型間很乾，有熱水比什麼都實際。」
  - Vera：「我收下。你自己也記得喝水，別整天只靠汽水撐。」

### 2.4 crisisVariant（Vera T5 打歌期／C12 陪伴壓力｜短變體）

#### GR-vera-silk_scarf · crisisVariant T5／C12
- **觸發：** Vera 打歌／形象高壓期，或 C12「賀歲 vs 關係」且當前高好感為 Vera  
- **lines:**
  - Vera：「這種時候你還記得絲巾……好。至少你沒有只會買花。」
  - Vera：「別亂花錢充場面。我要的是你出現在對的位置，不是一堆包裝。」

#### GR-vera-rose_premium · crisisVariant C12
- **觸發：** C12 且只送花、近期未出現其他懂工作的禮物  
- **lines:**
  - Vera：「又是花？你是不是覺得，只要顏色夠紅，我就能當你有陪過我？」
  - Vera：「花我收下。下一次，先問我缺不缺人手，再決定要不要送禮。」

---

## 3. 林曉晴（`hiu`）｜同期臨記 · 親切、同路人

### 3.1 liked

#### GR-hiu-pineapple｜liked
- **npcKey:** `hiu`  
- **itemId:** `gift_pineapple_bun_set`  
- **pref:** `liked`  
- **lines:**
  - 林曉晴：「菠蘿油加奶茶？你也太懂臨記的命根了。早上空腹等場，就靠這個續命。」
  - 林曉晴：「走，我們找個梯間先咬兩口。謝你，真的。」
  - **narration:** 她眼睛一亮，立刻把奶茶券小心地夾進通告夾裡。

#### GR-hiu-egg_tart｜liked
- **npcKey:** `hiu`  
- **itemId:** `gift_egg_tart_box`  
- **pref:** `liked`  
- **lines:**
  - 林曉晴：「美珍的蛋撻！我上次路過已經賣完。你還專程買整盒……」
  - 林曉晴：「晚上收工我們分給其他臨記一點，好不好？大家都會記得你。」

#### GR-hiu-thermos｜liked
- **npcKey:** `hiu`  
- **itemId:** `gift_thermos`  
- **pref:** `liked`  
- **lines:**
  - 林曉晴：「保溫瓶？你是不是看見我冬天抱著紙杯發抖？太實用了。」
  - 林曉晴：「我可以裝熱水，也可以裝涼茶。這份心意比什麼名牌都實際，謝謝你。」

#### GR-hiu-hair_clip｜liked
- **npcKey:** `hiu`  
- **itemId:** `gift_hair_clip_set`  
- **pref:** `liked`  
- **lines:**
  - 林曉晴：「平價又好看，拍群戲不會被罵搶鏡。你選飾物的眼光，比我想像中細心。」
  - 林曉晴：「我現在就夾上——你看看，是不是整齊一點？」

#### GR-hiu-handmade_sweet｜liked
- **npcKey:** `hiu`  
- **itemId:** `gift_handmade_sweet`  
- **pref:** `liked`  
- **lines:**
  - 林曉晴：「手作甜品盒……打開還有小字條？你這個人，表面趕通告，內心其實很軟。」
  - 林曉晴：「我慢慢吃，不跟別人搶。今天心情好了半截。」

#### GR-hiu-cassette｜liked
- **npcKey:** `hiu`  
- **itemId:** `gift_cassette_indie`  
- **pref:** `liked`  
- **lines:**
  - 林曉晴：「卡帶？是不是你從哪個通告聽來的？我最喜歡這種『有人記掛你』的情報味。」
  - 林曉晴：「回家路上一邊等車一邊聽。你有空也跟我講講，邊首最好聽。」

### 3.2 dislike

#### GR-hiu-auction｜dislike
- **npcKey:** `hiu`  
- **itemId:** `gift_auction_brooch`  
- **pref:** `dislike`  
- **lines:**
  - 林曉晴：「這……也太貴重了。你是不是搞錯對象？我只是臨記，收這個會睡不著。」
  - 林曉晴：「如果你真心想對我好，不如一齊食碗麵。這種東西，我會覺得你把我當成另一種人。」

#### GR-hiu-yacht｜dislike
- **npcKey:** `hiu`  
- **itemId:** `gift_yacht_invite_prop`  
- **pref:** `dislike`  
- **lines:**
  - 林曉晴：「遊艇午宴？我聽都未聽過怎麼站。你送這個給我，是想我陪你攀關係，還是開玩笑？」
  - 林曉晴：「收回去吧。我們這種身份，突然拿這種帖，只會被人笑。」

#### GR-hiu-wine｜dislike
- **npcKey:** `hiu`  
- **itemId:** `gift_red_wine`  
- **pref:** `dislike`  
- **lines:**
  - 林曉晴：「紅酒……我屋企連高腳杯都沒有。你這樣送，會不會太隆重？」
  - 林曉晴：「我不是嫌你，是怕人家誤會我們在做交換。換便宜一點的，我反而開心。」

### 3.3 neutral

#### GR-hiu-daisy｜neutral
- **npcKey:** `hiu`  
- **itemId:** `gift_daisy_bunch`  
- **pref:** `neutral`  
- **lines:**
  - 林曉晴：「雛菊很可愛，放宿舍窗台剛剛好。謝謝你還記得帶花。」

#### GR-hiu-memo｜neutral
- **npcKey:** `hiu`  
- **itemId:** `gift_memo_pad`  
- **pref:** `neutral`  
- **lines:**
  - 林曉晴：「拍紙簿我可以拿來抄通告時間。實用，雖然不算驚喜。」

#### GR-hiu-soda｜neutral
- **npcKey:** `hiu`  
- **itemId:** `gift_set_soda_pack`  
- **pref:** `neutral`  
- **注：** 簽核 likes 未列汽水；STORY 禮物表對曉晴為 liked。本短稿按 common 見面禮走 **neutral 偏暖**；若 eng 以 STORY 表 liked 為準，用下方升格變體。  
- **lines:**
  - 林曉晴：「片場汽水拼裝？你真的很臨記。謝謝，待會大家一齊開。」
  - **narration:** 她笑着接過，沒有大驚小怪，像收下一份同事的心意。

> **升格變體（若引擎按 STORY 表 `liked:hiu`）：**  
> 林曉晴：「你居然記得片場最缺汽水！這才叫同路人。今晚加場，我請你半包薯片。」

### 3.4 crisisVariant（C12）

#### GR-hiu-thermos · crisisVariant C12
- **觸發：** C12 賀歲壓力、陪伴不足  
- **lines:**
  - 林曉晴：「忙成這樣還記得送保溫瓶……我寧願你抽半小時出來行一轉，但這個我也要。」
  - 林曉晴：「別用錢湊時間。你人在，我才安心。」

---

## 4. 周采兒（`choi`）｜記者 · 利落、厭公關套餐

### 4.1 liked

#### GR-choi-coffee｜liked
- **npcKey:** `choi`  
- **itemId:** `gift_coffee_beans`  
- **pref:** `liked`  
- **lines:**
  - 周采兒：「蘭芳的豆？你有做功課。夜更截稿前，就靠這個提神。」
  - 周采兒：「別指望我寫软文回報你。不過這包豆，我會煮完才睡。」
  - **narration:** 她掂了掂分量，點頭的幅度很短，卻是真的滿意。

#### GR-choi-memo｜liked
- **npcKey:** `choi`  
- **itemId:** `gift_memo_pad`  
- **pref:** `liked`  
- **lines:**
  - 周采兒：「空白拍紙簿——你是在說『你可以自己寫，我不塞稿給你』嗎？」
  - 周采兒：「這種禮物我喜歡。坦白，又用得着。謝了。」

#### GR-choi-rose｜liked
- **npcKey:** `choi`  
- **itemId:** `gift_rose_premium`  
- **pref:** `liked`  
- **lines:**
  - 周采兒：「私下送可以。別在記者會門口遞，我會當你搞公關。」
  - 周采兒：「花不錯。下次直接講你想講的話，比包裝紙清楚。」
  - **narration:** 她把花束轉到身後，像不想讓路人多看一眼。

#### GR-choi-cassette｜liked
- **npcKey:** `choi`  
- **itemId:** `gift_cassette_indie`  
- **pref:** `liked`  
- **lines:**
  - 周采兒：「獨立樂隊卡帶？你倒不像會跟潮流版要通稿的人。」
  - 周采兒：「我收下。有空當背景聲，總好過聽娛樂新聞迴圈。」

### 4.2 dislike

#### GR-choi-pr_basket｜dislike
- **npcKey:** `choi`  
- **itemId:** `gift_pr_flower_basket`  
- **pref:** `dislike`  
- **lines:**
  - 周采兒：「公關花籃？你把我當成要被餵稿的窗口嗎？」
  - 周采兒：「拿走。我可以收咖啡，可以收拍紙簿，就是不收這種『請多關照』的道具。」

#### GR-choi-auction｜dislike
- **npcKey:** `choi`  
- **itemId:** `gift_auction_brooch`  
- **pref:** `dislike`  
- **lines:**
  - 周采兒：「胸針這種價位，放在記者桌上，看起來就像封口費。」
  - 周采兒：「我當你不懂行規，先提醒一次：別再用貴重東西試探我。」

#### GR-choi-yacht｜dislike
- **npcKey:** `choi`  
- **itemId:** `gift_yacht_invite_prop`  
- **pref:** `dislike`  
- **lines:**
  - 周采兒：「遊艇帖送記者，通常後面都有議程。你有議程嗎？」
  - 周采兒：「沒有就收回；有的話，開門見山講，別用禮物繞。」

### 4.3 neutral

#### GR-choi-daisy｜neutral
- **npcKey:** `choi`  
- **itemId:** `gift_daisy_bunch`  
- **pref:** `neutral`  
- **lines:**
  - 周采兒：「小束雛菊還好，不似公關。謝謝，我放辦公室角落。」

#### GR-choi-egg_tart｜neutral
- **npcKey:** `choi`  
- **itemId:** `gift_egg_tart_box`  
- **pref:** `neutral`  
- **lines:**
  - 周采兒：「蛋撻可以，同事會開心。你人倒是實在。」

#### GR-choi-thermos｜neutral
- **npcKey:** `choi`  
- **itemId:** `gift_thermos`  
- **pref:** `neutral`  
- **lines:**
  - 周采兒：「保溫瓶實用。我夜更常忘記喝水，這個提醒我一下也好。」

### 4.4 crisisVariant（采兒 C13 公關壓力向）

#### GR-choi-pr_basket · crisisVariant C13
- **觸發：** 采兒線危機／C13 類「關係曝光 vs 報館」壓力期  
- **lines:**
  - 周采兒：「這個時候還送花籃？你是想我明天頭條更好寫，還是想我 indignant 到拒稿？」
  - 周采兒：「立刻拿走。你要支持我，就別做最像公關的那種動作。」

---

## 5. 藍若曦（`lan`）｜街頭音樂 · 自由、厭包裝

### 5.1 liked

#### GR-lan-handmade｜liked
- **npcKey:** `lan`  
- **itemId:** `gift_handmade_sweet`  
- **pref:** `liked`  
- **lines:**
  - 藍若曦：「手作的……我聞得到不是工廠味。你有花時間，我收得安心。」
  - 藍若曦：「今晚錄音前先偷吃一粒。謝你，真的。」

#### GR-lan-cassette｜liked
- **npcKey:** `lan`  
- **itemId:** `gift_cassette_indie`  
- **pref:** `liked`  
- **lines:**
  - 藍若曦：「這隊我聽過現場。你怎麼找到這卷卡帶的？」
  - 藍若曦：「比任何名牌都好。音樂這東西，送對了，比說話更準。」
  - **narration:** 她把卡帶貼近耳邊搖了搖，像在確認帶子還緊。

#### GR-lan-street_charm｜liked
- **npcKey:** `lan`  
- **itemId:** `gift_street_charm`  
- **pref:** `liked`  
- **lines:**
  - 藍若曦：「街頭檔的手工飾？有點粗糙，但我喜歡這種溫度。」
  - 藍若曦：「戴出去也不怕撞款。謝謝你沒有送那些亮閃閃的籠子。」

#### GR-lan-daisy｜liked
- **npcKey:** `lan`  
- **itemId:** `gift_daisy_bunch`  
- **pref:** `liked`  
- **lines:**
  - 藍若曦：「雛菊很乾淨，不像那些會上雜誌的花束。我放窗邊就好。」
  - 藍若曦：「你懂我——不用太大朵，真心就夠。」

### 5.2 dislike

#### GR-lan-perfume｜dislike
- **npcKey:** `lan`  
- **itemId:** `gift_perfume_sample`  
- **pref:** `dislike`  
- **lines:**
  - 藍若曦：「香水……即使你說是淡的，我一聞還是會皺眉。舞台燈光一熱，味道會變得很兇。」
  - 藍若曦：「換別的吧。卡帶、小甜品，什麼都好，別用香味包裝我。」

#### GR-lan-pr_basket｜dislike
- **npcKey:** `lan`  
- **itemId:** `gift_pr_flower_basket`  
- **pref:** `dislike`  
- **lines:**
  - 藍若曦：「這種花籃我在通告門口見過太多，後面通常跟着鏡頭。」
  - 藍若曦：「你不是那些人，就別學他們的送禮方式。」

### 5.3 neutral

#### GR-lan-egg_tart｜neutral
- **npcKey:** `lan`  
- **itemId:** `gift_egg_tart_box`  
- **pref:** `neutral`  
- **lines:**
  - 藍若曦：「蛋撻可以啊，錄音室大家都會搶。謝謝。」

#### GR-lan-thermos｜neutral
- **npcKey:** `lan`  
- **itemId:** `gift_thermos`  
- **pref:** `neutral`  
- **lines:**
  - 藍若曦：「保溫瓶實用，練歌時喉咙要護着。我收下。」

### 5.4 crisisVariant（C9 公開壓力／C15 聯姻）

#### GR-lan-cassette · crisisVariant C9
- **觸發：** C9 公開壓力／狗仔期  
- **lines:**
  - 藍若曦：「外面那麼吵，你還送卡帶……我就當這是安靜的支持。」
  - 藍若曦：「別替我發聲明，也別送花籃。有這卷帶子，已經夠我撐一陣。」

#### GR-lan-handmade · crisisVariant C9
- **觸發：** C9  
- **lines:**
  - 藍若曦：「手作甜品我收下。這種時候，大人物的禮我反而怕。」
  - **narration:** 她把盒子藏進帆布袋最底，像怕閃光燈拍到商標以外的東西——偏偏這盒沒有商標。

#### GR-lan-street_charm · crisisVariant C15
- **觸發：** C15 聯姻壓力  
- **lines:**
  - 藍若曦：「家族那邊要看名分，你卻送我街頭小飾……我反而鬆一口氣。」
  - 藍若曦：「奢華的東西這陣子別送來，會被讀成收買，也會被讀成門不當戶不對。這個，我戴得安心。」

---

## 6. 徐寶珊（`xu`）｜豪門距離 · 遊戲感、嫌寒酸

### 6.1 liked

#### GR-xu-wine｜liked
- **npcKey:** `xu`  
- **itemId:** `gift_red_wine`  
- **pref:** `liked`  
- **lines:**
  - 徐寶珊：「年份還過得去。你開始懂，場上什麼叫『識玩』。」
  - 徐寶珊：「今晚若有空，開一瓶。別緊張，我不是要考你品酒詞——我要看你坐不坐得穩。」
  - **narration:** 她轉了轉瓶身看標籤，眼神像在估值，也像在估值你。

#### GR-xu-yacht｜liked
- **npcKey:** `xu`  
- **itemId:** `gift_yacht_invite_prop`  
- **pref:** `liked`  
- **lines:**
  - 徐寶珊：「你把請帖道具組帶來，意思是你願意入場？還是只想觀摩規則？」
  - 徐寶珊：「都可以。但入場之後，別再用臨記那套低頭走路——抬頭，看清楚誰在開局。」

#### GR-xu-brooch｜liked
- **npcKey:** `xu`  
- **itemId:** `gift_auction_brooch`  
- **pref:** `liked`  
- **lines:**
  - 徐寶珊：「拍場小品……眼光可以。你知道光靠努力不夠，有時要會揀物件說話。」
  - 徐寶珊：「我收下。下一次，記得物件背後的故事也要講得漂亮。」

### 6.2 dislike

#### GR-xu-pineapple｜dislike
- **npcKey:** `xu`  
- **itemId:** `gift_pineapple_bun_set`  
- **pref:** `dislike`  
- **lines:**
  - 徐寶珊：「菠蘿油奶茶券？你是請司機，還是請我？」
  - 徐寶珊：「心意我聽見了，但場面上這叫未熟。換一件配得上對話的東西再來。」

#### GR-xu-handmade｜dislike
- **npcKey:** `xu`  
- **itemId:** `gift_handmade_sweet`  
- **pref:** `dislike`  
- **lines:**
  - 徐寶珊：「手作小禮物很可愛，留給需要被安慰的人。」
  - 徐寶珊：「我這邊講規則、講籌碼。甜的，我怕黏手。」

#### GR-xu-daisy｜dislike
- **npcKey:** `xu`  
- **itemId:** `gift_daisy_bunch`  
- **pref:** `dislike`  
- **lines:**
  - 徐寶珊：「包裝太街市。花不是不可以，是你送得太寒酸，會連你一起被看輕。」
  - 徐寶珊：「拿回去。想送花，至少讓它看起來像你認真挑過。」

### 6.3 neutral

#### GR-xu-scarf｜neutral
- **npcKey:** `xu`  
- **itemId:** `gift_silk_scarf`  
- **pref:** `neutral`  
- **lines:**
  - 徐寶珊：「絲巾還可以，不算失禮。你有在進步。」

#### GR-xu-mag｜neutral
- **npcKey:** `xu`  
- **itemId:** `gift_fashion_mag`  
- **pref:** `neutral`  
- **lines:**
  - 徐寶珊：「雜誌我隨手翻翻。你當寒暄禮，我接受。」

### 6.4 crisisVariant（C14 尊重／包養讀法）

#### GR-xu-wine · crisisVariant C14｜尊重合作肢
- **觸發：** C14 且玩家走「尊重合作」方向  
- **lines:**
  - 徐寶珊：「紅酒送到這個節骨眼，我當你在談合作，不是在求包養。」
  - 徐寶珊：「坐直一點。我們可以談條件，但別用禮物代替談判。」

#### GR-xu-brooch · crisisVariant C14｜依賴／獻媚風險肢
- **觸發：** C14 且關係讀法偏「依賴／獻媚」風險  
- **lines:**
  - 徐寶珊：「胸針很亮。你是想證明誠意，還是想我可憐你？」
  - 徐寶珊：「我可以收，也可以當沒看見。你自己選要哪一種讀法——我只提醒一次。」

---

## 7. 鄧麗萍（`tang`）｜院線實用 · 冷淡、要可量化｜**須 `flag_tang_open`**

> **開送條件：** 已有 `flag_tang_open`。未開 → 不播下列對白；UI：「院線那邊，還未到送禮的時候。」

### 7.1 liked

#### GR-tang-pen｜liked
- **npcKey:** `tang`  
- **itemId:** `gift_fountain_pen`  
- **pref:** `liked`  
- **lines:**
  - 鄧麗萍：「名筆。簽名、批檔期、改數字，都用得着。你至少知道我不是靠感人情書辦事的人。」
  - 鄧麗萍：「謝謝。下次如果你要談場次，直接帶報表，比帶花有用。」

#### GR-tang-calc｜liked
- **npcKey:** `tang`  
- **itemId:** `gift_desk_calculator`  
- **pref:** `liked`  
- **lines:**
  - 鄧麗萍：「桌上計數機……你觀察過我辦公桌。上座率、拆帳、場次，我都要即時核。」
  - 鄧麗萍：「實用。我喜歡可以量化的誠意。」

#### GR-tang-watch｜liked
- **npcKey:** `tang`  
- **itemId:** `gift_dress_watch`  
- **pref:** `liked`  
- **lines:**
  - 鄧麗萍：「正裝腕表。開會不能遲到，檔期也不能含糊——時間就是數字。」
  - 鄧麗萍：「我收下。别以為送完表就可以談感情條款；我們先把場次談清楚。」

### 7.2 dislike

#### GR-tang-rose｜dislike
- **npcKey:** `tang`  
- **itemId:** `gift_rose_premium`  
- **pref:** `dislike`  
- **lines:**
  - 鄧麗萍：「玫瑰？你想綁架我的情緒，還是想拖延談判？」
  - 鄧麗萍：「花我不收。有話直說，有數直接列。」

### 7.3 neutral

#### GR-tang-memo｜neutral
- **npcKey:** `tang`  
- **itemId:** `gift_memo_pad`  
- **pref:** `neutral`  
- **lines:**
  - 鄧麗萍：「拍紙簿可以，開會隨手記。不算加分，也不扣分。」

#### GR-tang-coffee｜neutral
- **npcKey:** `tang`  
- **itemId:** `gift_coffee_beans`  
- **pref:** `neutral`  
- **lines:**
  - 鄧麗萍：「咖啡豆……夜更對帳用得着。放那邊，我自己煮。」

---

## 8. 系統短句（非角色對白｜可換佔位）

| 情況 | 文案 |
|---|---|
| 未認識 | 「你們還沒真正打過照面，現在送禮太突兀了。」 |
| 錢不足 | 「口袋裡的數目不夠——先去趕一兩個通告吧。」 |
| 每日上限（每角硬 1） | 「人情急不來；今天先到這裡。」 |
| 週軟 cap＋2 超出 | 「心領了。這份心意我記住，數字就先不動。」 |
| 同 item 冷卻／重複減弱 | 「同樣的東西短時間再送一次，誠意會變淡。」 |
| 鄧未 `flag_tang_open` | 「院線那邊，還未到送禮的時候。」 |
| 危機禁用貴價（如 C15→藍） | 「這種時候，太貴重的東西只會增加誤會。」 |

---

## 9. 引擎對照小註

| 項 | 說明 |
|---|---|
| `npcKey` | `vera`／`hiu`／`choi`／`lan`／`xu`／`tang`（對齊 relKey：`rel_*`） |
| 缺條 fallback | 同角任意 `neutral`；再缺用「謝謝，我收下。」＋ narration 空 |
| crisis 覆寫 | 有 `crisisVariant` 且章節 flag／節點命中時優先 |
| Soft≠PASS | 本檔可換 iOS 短佔位；數值／商店仍跟 `PLAN_GIFT_SHOP_v1` |
| LIVE JSON | **未改** |

---

## 10. 路徑

| 位置 | 路徑 |
|---|---|
| content | `/workspace/star-volunteer-web/content/GIFT_REACT_COPY_v1.md` |
| bot store | `/cursor/stores/store-cbdfa415-74f6-4e12-8fbd-513ef31077be/GIFT_REACT_COPY_v1.md` |

---

*送禮反應對白短稿 v1 完｜可換 iOS 佔位｜Soft≠PASS｜出圖 HOLD｜未改 LIVE JSON*
