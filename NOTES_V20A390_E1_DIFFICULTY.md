# v390 E1 難易度調節＋錢約束＋音樂獎天花板

用戶拍板：2026-11-23 12:21「難易度要調節的。E1要用心玩才可以到達的」；
12:22 追加批准第十輪深度審計兩項 P1（錢唔約束、音樂獎天花板）同一波做埋，併入 v390。

證據目錄：`~/workspace/linji-drive390/`（measure_gates.py/.json、probe_gates.py/.json、
gate_test.js/.json、sim390.js、sim_P*.json、sim_Q*.json、claude_brief.txt、claude_reply.txt/.json、
gigs390_dump.json、driver_w5_390.py、driver_w4_390.py）。

---

## 一、E1 難易度（主項）

### 量度（對 live code＋第十輪存檔核實）
- E1 現行閘（`ENDING95_T`＋`resolveEnding410`）：fame≥70、credit≥65、dual≥350、負標籤≤1，
  ＋質性閘 `e1Qual95`＝有獎＋擔正媒介≥2＋脊骨行完（讀法甲）。
- W4 正常打法最終存檔（day 1066）：fame 371、credit 458、dual **829**、負標籤 0、
  獎 8 場／9 格、擔正 film **0**／tv 3／music 4／variety 2／ad 6（4 媒介共 15 部）、脊骨行完 → E1。
- W5 衝 E1：dual 911、獎 10 格／7 類、擔正 film **2**／tv 1／music 4／variety 2／ad 6（5 媒介）。
- 衝刺政策 dual 三局範圍 669–1010，同正常政策重疊——**dual 門檻冇區分作用**。
- 電影擔正供應：全庫 `film_lead_big` 只有 10 張（1991 五、1992 五，1990 零），
  要求演技 85–150、體能 70–90。W4 演技最終 578 仍然 0 部——要刻意追先攞到，係真區分閘。

### Claude 諮詢（88api claude-opus-5-5）
- 電影擔正≥1 合理；媒介保持≥2；建議 dual 350→380＋電影作品總數≥3。
- **我方唔採納後兩項**：dual 方差太大加門檻冇區分作用、v377 慢速校準 359 會被 380 打破；
  電影作品數 W4 有 26 部，冇區分作用。

### 實裝
- `e1Qual95` 加 `(lead229.byMedium.film||0) >= 1`（`filmLead390`）。
- E1／SS reason 字串加電影擔正數；`end95BuildGaps` 加電影擔正缺口句
  （「電影擔正，你未曾站上那個位置——天王那一格，要有一部電影由你擔正。」）；
  `ladder95` 加 `filmLead` 欄；`titles162Ladder162` 加第四行現在式事實。
- dual 350／fame 70／credit 65／負標籤≤1／擔正媒介≥2 全部不變。
  試鏡判定／結局判定結構不變，只加一個區分條件。

### 驗證（Node 抽真函數跑存檔，`gate_test.js`）
- W4 正常最終存檔 → **SS**（唔再係 E1），reason 明列「電影擔正 0」，gaps95 出電影擔正句。
- W4 存檔＋播種 film lead=1 → **E1**（證明電影擔正係唯一阻擋項）。
- W5 d900 存檔＋脊骨補完播種 → **E1**。
- 真玩：W5 driver 由 d900 checkpoint 續跑到結局、W4 driver 由 d540 checkpoint 續跑到結局（見下）。

---

## 二、錢約束（P1-1）

### 現況（W2 Monte Carlo 200 局×52 週）
兼職打法年尾現金 $15,189 ≈ 通告打法 $7,949 嘅 1.9 倍，錢全程唔約束。

### Sim 選參（`sim390.js`，參數化版 W2 Phase E/F，抽真函數；基線複現 W2：兼職 15,164 vs 15,189 ✓）
- 過程發現 sim override bug（eval 綁定遮蔽 `global.*` 賦值，生活費／訓練費 override 冇生效），
  已修正重跑；早期 P0–P6 結果只作方向參考，定案以 Q 系列為準。
- **定案 Q4 組合**：咖啡 R(45,75)、街演 R(35,60)、壓力下限 $25／$12、通告片酬 ×1.4、
  生活費 ×1.1、訓練費 $20 全課。
  - 訓練費 $35 試算：訓練型打法破產率 36%（太狠）；$20 → 2.5%（唔識變通嘅固定政策；
    真人會跟警告調整）。免學費緩衝試過（現金<$300 免），對破產率幫助有限且削弱約束，唔採用。

### 實裝
1. 兼職：street `R(70,100)`→`R(35,60)`、cafe `R(85,115)`→`R(45,75)`，壓力下限 40→25、20→12。
2. 片酬：`content/gigs_new.json` 330 張 pay 區間 ×1.4（整數；中位：電影 $260→$546、
   電視 $185→$378、唱片 $140→$462、綜藝 $120→$168、廣告 $70→$168）。
   favor 幫忙通告 payExact $40/$60 係 code-side，唔郁。
3. 生活費 `livingCostBand` 五段改（lo/hi/mid）：105/140/120、125/160/145、150/180/165、
   170/205/185、220/310/265，label 同步；年份／fame 加級不變。
4. 訓練費：`TRAIN75_SPEC` 每課 `fee:20`（刪 `fee800` 舊制）；扣費仍以現有現金為上限
   （`min(fee, money)`），預設計劃自動排課唔會扣到負數。

### 驗證（實裝版 sim，`sim_Q4impl.json`）
- 次序反轉 ✓：兼職年尾 $7,498 < 通告 $8,743。
- 休閒破產 0% ✓（minMoney p10 $845、min $380）。
- 訓練型打法破產 4%（固定政策唔變通；真人跟警告調整）。
- 雙軌成長不受影響（各打法 dual 同基線一致）。

---

## 三、音樂獎天花板（P1-2）

### 現況
頒獎計分：base＝0.40×主軌歸一＋0.42×worksScore＋tagBonus＋repPower；贏線 **0.875 不變**。
舊 q 值下音樂現實滿配桶 [0.78,0.66,0.48,0.48] wsum 1.407 < 飽和線 1.45 → base ~0.844，
勝率約 20%（電影滿配 base 0.90 勝率約 75%）。

### 實裝（`AWARDS62_ROLE_Q`）
music_lead 0.78→**0.85**、rec_album 0.66→**0.74**、mtv 0.48→**0.52**（ad_av／variety_special 保持 0.48）。
層級維持 music_lead > rec_album > mtv。

### 驗證（真函數 `awards62ScoreParts`，`gate_test.js`）
- 滿配桶 [0.85,0.74,0.74,0.52]：base **0.900**＝電影滿配 0.900 ✓
- 無 music_lead [0.74,0.74,0.74,0.52]：base 0.892
- 舊現實桶 [music_lead, rec_album, mtv, mtv]：base 0.895（舊 0.844）
- 中桶 [0.74,0.74,0.52,0.52]：0.854；弱桶 [0.52×4]：0.732（正確地贏唔到）

---

## 四、測試 resync
- 行號釘：`qa390/resync390.py`（difflib 映射，index.html 淨 +26 行）——travel114、rom159、rom176、
  tang152、gift185／tang171／tang173（總行數 49484→49510）；text125 釘行手改。
- 數值釘：生活費（calib60／fix65／week105／years66）、訓練費（levels75／ux68）、
  ROLE_Q（p361）、片酬（r286／r292／r301／r307／r316／r317／r319／r320／r337／r5_284／gig229）。
- Suite：**406 PASS／9 FAIL，同基線一致**（九項 pre-existing：flash51／slot50／
  soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。

## 五、真玩覆驗（本地 v390 build，Playwright 實駕）
- **W5 衝 E1**（driver_w5_390.py，由 d900 checkpoint 續跑）：day 1066 結局 **E1 天王接班・留下來的人**
  （fame 412、credit 494、dual 906、殺青 102；1992 電影男主角獎＋音樂歌手獎）。E1 仍然可達 ✓
- **W4 正常打法**（driver_w4_390.py，由 d540 checkpoint 續跑；中途本地伺服器死亡卡住，
  由 d990 checkpoint 重啟完成）：day 1066 結局 **SS 一線巨星・留下來的人**（fame 294、credit 386、
  dual 680、現金 $17,273、殺青 60、脊骨行完），gaps95 正確指出電影擔正缺口。
  正常跟引導玩唔再到 E1 ✓，且冇破產 ✓

## 紀律核對
贏線 0.875 不變；SAVE key／softRev／產品 `?v=`／floor 140／warnLine 180 不變；
試鏡判定／結局判定結構不變，只調門檻數值同加一個區分條件。
