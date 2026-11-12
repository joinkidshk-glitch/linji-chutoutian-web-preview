# NOTES_V20A127 — 表情補圖批（22 張新表情）

## 任務
v126 殘留批。批單由 `~/workspace/linji-expression-inventory/EXPRESSION_INVENTORY.md`
逐句核實（句數同檔名有出入以實測為準），22 張、＋32 句。
開工基底 c71526a（v126）→ **rebase 到最新 main `4f4b96a`（v20a131 B 批）**，零衝突
以外嘅 6 處計數斷言衝突已解（見下）。合併嗰陣 main 已行前到 **`7f68665`（v20a132
S-30 英雄區修復）**——squash merge 直接落喺 7f68665，乾淨；全套 A/B 同實駕喺合併後
樹重跑（見測試／實駕節，新基底數字 189/12 vs 191/12）。**新制落地，唔開 PR**
（checkout main → `git merge --squash v127-expr` → commit → push main，經 deploy key）。

## 改動（index.html 零改動）
- **22 張新 webp**入 `assets/story/fullbody/`（全庫 148→**170 張**；非 boss webp
  123→**145 張**）。loader 候補鏈唔使改；覆寫表／merge 注入／載入正規化一概唔郁，
  content pack JSON 零改動。
- **測試計數斷言更新**（rebase 衝突 6 處，v131 B1 加 2 張企立圖＋本批 22 張合併計）：
  dlg107／119／123／126 fullbody 總數 148→170；dlg108／dlg109 真檔數目 123→145。
  另修 test_dlg127_static 一處漏改（146→168 殘留，rebase 後 148→170）。
- **新測試**：`tests/test_dlg127_static.py`（22 張存在＋WebP 檔頭＋>50KB＋全庫 170＋
  句數合計 32＋焗邊報告 22 張全 PASS＋標籤更正守門＋in-memory 反證＋真磁碟反證）、
  `tests/test_dlg127_logic.js`（22 張候補鏈首選＋20 句真實對白分類＋反證）。
- **兩處標籤更正**（v126 殘留表錯咗，已寫入守門測試）：
  (1) `chow_choiyi`＝**周采兒**（display「周采兒」，有 base＋serious／smile／think），
  唔係周刊編輯——真正嘅周刊編輯係無名角色，解像係 `shadow_male`，唔出表情圖。
  核實：index.html 第 26926 行 `chow_choiyi: { artId:"char_chow", ... display:"周采兒"}`。
  (2) **阿金叔 speaker id 係 `uncle_kim`**（唔係 `kam_uncle`，後者唔存在；
  index.html 第 26937 行 `uncle_kim: { ... display:"金九"}`——display 名係「金九」）。
- **剔走（唔出圖）**：`extra_ad_fen` sad 9 句已證實係旁白假陽性（同一句旁白重複 9 次），
  唔使補，唔好重犯；真・周刊編輯無名角色行剪影、冇 base 圖，唔出表情圖；
  鄧麗萍 `tang_liping` corpus 0 句、無 base 圖，唔出。

## 批單（22 張、＋32 句）
顧明輝 shy 3／angry 1／think 1；彭少祺 sad 3；周采兒 sad 3／angry 2；
葉敏芝 surprise 2／angry 2／shy 1；程天諾 shy／surprise／think 各 1；
藍若曦 serious／think 各 1；方小龍 sad 2／angry 1；鄭威廉 serious／shy 各 1；
關海媚 serious 1；莫少輝 sad 1；阿金叔 smile（happy）／serious 各 1。
句源已逐句核實（巧遇真對白／常駐真對白／LIVE／pack 獨有／括號舞台指示句——
葉敏芝 angry 1 句＋程天諾 think 1 句＋藍若曦 think 1 句係括號舞台指示）。

## 新資產（22 張，全部 WebP，米白光邊已焗）
- `gu_mingfai_shy.webp` 134,830 bytes，587×2499
- `gu_mingfai_think.webp` 133,960 bytes，584×2511
- `gu_mingfai_angry.webp` 136,986 bytes，584×2513
- `pang_siuki_sad.webp` 176,540 bytes，771×2060
- `chow_choiyi_sad.webp` 104,910 bytes，448×1408
- `chow_choiyi_angry.webp` 99,818 bytes，449×1409
- `yip_manji_shy.webp` 178,792 bytes，892×2336
- `yip_manji_surprise.webp` 180,500 bytes，895×2348
- `yip_manji_angry.webp` 177,976 bytes，895×2344
- `ching_tinlok_shy.webp` 169,786 bytes，631×2350
- `ching_tinlok_surprise.webp` 178,072 bytes，631×2362
- `ching_tinlok_think.webp` 168,012 bytes，630×2356
- `lan_ruoxi_serious.webp` 212,402 bytes，763×2352
- `lan_ruoxi_think.webp` 211,322 bytes，757×2349
- `fong_siulung_sad.webp` 104,200 bytes，586×1394
- `fong_siulung_angry.webp` 105,670 bytes，580×1396
- `cheng_william_serious.webp` 72,786 bytes，444×1407
- `cheng_william_shy.webp` 73,466 bytes，445×1404
- `kwan_hoimei_serious.webp` 95,956 bytes，501×1427
- `mok_siufai_sad.webp` 213,748 bytes，812×2281
- `uncle_kim_serious.webp` 239,524 bytes，764×2142
- `uncle_kim_smile.webp` 240,376 bytes，766×2143

## 出圖＋QC（跟 v106／v123／v126）
- 方法：以該角 base 生成圖（`linji-fullbody-batch/gen/{stem}_base_gen1.png`）做編輯參照，
  淨換面部表情；風格錨 `style-anchor-awei-anime.jpg` 每次同行。媒體生成工具每輪最多
  4 次呼叫，分 6 批（A–F）出齊；輸出檔名係 `media-generation-{name}-0-{uuid}.webp`，
  手動改名做 `{stem}-gen1.webp` 先入管線。生成圖＋QC＋筆記喺
  `~/workspace/linji-work127-keep/`（`NOTES_GEN127.md`＋`gen/`＋`qc/`＋`assets/`＋
  `work127_proc.py`＋`work127_metrics.json`）。
- **唯一重擲**：`uncle_kim_serious` gen1 漏咗煙斗（base 有煙斗＋煙），用 snapshot resume
  （snapshot_id `7d92b279-f481-4fb9-8f13-7575e9e66116:k2l2br`）重擲 gen2 補返煙斗＋煙，
  面不變，PASS。
- QC **22 pass／0 marginal／0 紅旗**（面部對照存 `qc/face_*.png`）。
- 去背（`work127_proc.py`，沿用 v126 管線：連通體剪影＋填洞＋收邊＋羽毛，WebP q92，
  **唔焗米白邊**；另加 v123 wedge 選擇性填洞掃描）：闊高比同各自基本款誤差
  −0.001～−0.011；全部單一連通體、零碎片；腿間白楔掃描零可疑洞，唔使行 wedge fix。
  透明度佔比 0.258–0.555。
- 焗邊（`qa127/bake127.py`，v106 同一條公式，米白 RGB 243,233,210，
  r=round(3×原生高/422)）：**22/22 PASS**，邊帶米白命中 0.9989–1.0000、內部大差異 0、
  far_cream_px 全部 0。焗邊成品喺 `qa127/baked/`，已抄入 `assets/story/fullbody/`。
- 深底 spotcheck（`qa127/spotcheck_baked127_dark.png`）：顧明輝 shy＋周采兒 sad＋
  藍若曦 serious 喺近黑底上米白邊清晰可見，唔溶。PASS。

## 覆蓋率（`qa127/coverage127.py` → `coverage127.json`＋`coverage_report127.md`）
- **全局 515／593＝86.8%**（v126：483／593＝81.5%），＋32 句，同批單一字唔差；
  22 張新資產對應句數全部命中。
- 阿偉 s1 188／188（100%）；s2／s3 184／188（97.9%），淨 angry 4 句靠 `awi_angry`
  候補鏈實際 100%。
- 全覆蓋角色（missing {}）：顧明輝 22／22、彭少祺 29／29、周采兒 13／13、
  葉敏芝 19／19、程天諾 29／29、藍若曦 11／11、方小龍 8／8、鄭威廉 2／2、
  關海媚 1／1、莫少輝 1／1、阿金叔 2／2（另有何生 33／33 等舊有全覆蓋角）。
- 零精確覆蓋角只剩 `extra_ad_fen`（9 句旁白假陽性，刻意唔補）。
- 殘留缺口（下一批候選，按缺句數排）：ngai_wingnaam 10、lin_hiu 9、chai_zanhoi 7、
  ko_chunkit 7、luk_baakyin 7、lok_gasing 6、cheung_tsijun 4、liu_bingxing 4、
  cheung_hakfan 3、lui_ging 3、mak_zhendong 2、tsui_poushan 2、vera 2、
  chung_choning 1、so_jiyan 1、tong_souwan 1；其餘 69 句（連 extra_ad_fen 9 句計共
  78 句未覆蓋）。

## 測試（零回歸）
- **新鮮 pristine baseline**（`~/workspace/linji-pristine132/`，`git archive origin/main`，
  `7f68665` v20a132）：**189 PASS／12 FAIL**（201 個測試；v132 新加 test_ui132 喺
  pristine 上 PASS）。
- **合併後樹**：**191 PASS／12 FAIL**（203 個測試；189＋2＝兩個新 dlg127 測試全部 PASS）。
- **FAIL 列表同 baseline 完全一致**（12 個環境性 static FAIL：
  flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／
  start53／weave43／weave44／weave49／wrap38）。
- **反證成立**：test_dlg127_static.py 對 pristine131 跑 → 乾淨 FAIL（24 個 FAIL、exit 1、
  冇 crash）；過程中捉到一個 bug 並已修好（初版 temp 目錄反證喺 pristine 上會因抄唔到
  新檔而 `FileNotFoundError` crash——已加 guard，新資產唔齊就 skip 磁碟段，in-memory
  反證已覆蓋）。邏輯測試喺 pristine 上會 PASS，係設計使然（`dlg106Candidates` 只排
  URL 次序、唔查檔案存在；檔案存在由靜態測試守門）——呢點如實記錄，唔好話邏輯測試
  都反證 FAIL。
- 分類探針（開工前用 `/tmp/probe127.js` 逐句驗過）：28 句真實對白全部命中預期分類
  （28/28 OK）。`ching_tinlok think`／`lan_ruoxi think` 係括號舞台指示句，唔入分類
  斷言，只驗首選。

## 實駕（Playwright 390×844，`?softPreview=1`，本地 http.server）
### 全套 drive（`qa127/drive127.py`，新基底 4f4b96a）
- **分支：22／22 見齊，OVERALL PASS: True**；目標 404：{}（0）、all404: []（0）、
  pageerrors: []。`qa127/drive127_branch.log`＋`drive_log127_branch_all.json`。
- **Pristine 對照（linji-pristine131）：0／22，OVERALL PASS: False**；目標 404 合計
  **40**（22 檔全部至少 404 一次）、all404 60、pageerrors: []。
  `qa127/drive127_pristine.log`（JSON 喺 pristine copy 嘅 `qa127/`）。
- **合併後樹重跑（基底 7f68665，v132 只改 S-30 英雄區 CSS＋1 個靜態測試）**：
  **22／22 見齊，OVERALL PASS: True**；目標 404：{}（0）、all404: []（0）、
  pageerrors: []；loader 10 張全部 first_ok＋fetch 200＋解碼。
  `qa127/drive127_merged.log`＋`drive_log127_merged_all.json`。
- **12 張真 UI 渲染**：巧遇 9 張（顧明輝 shy／think／angry、彭少祺 sad、葉敏芝
  shy／surprise／angry、程天諾 shy／surprise）＋主線 3 張（方小龍 sad／angry，
  A_fong_meet；藍若曦 think，R_lan_ending step 13——括號舞台指示句）。
- **10 張 loader 證明**（首選＋fetch 200＋img 解碼，in-page module-eval）：
  cheng_william serious／shy、ching_tinlok think、chow_choiyi angry／sad、
  kwan_hoimei serious、lan_ruoxi serious、mok_siufai sad、uncle_kim serious／smile。
  loader 相 `first_ok=True` 全部經 in-page（唔係 node-test fallback）。
- **程天諾主場 rec_star（天星音樂）巧遇攔截唔觸發**（遊戲 bug，唔喺本批範圍，另開一票）：
  ching／chung／luk 在場＋met／unmet＋seed 有／冇，入 rec_star 一律 `triggered=0`、
  overlay=False，sheet 正常開；對照 rec_hk／ad_central／tvb_harbour 全部觸發。
  drive 改行副場 rec_hk（香江唱片），日子 [732, 737, 741, 747, 760]
  （probe3 掃描 730–800 得出 ching 喺 rec_hk 嘅日子）。

### Targeted re-drive：10 張 loader-only 圖逐張阻塞實證
任務書要求 loader-only 圖要喺場景真渲染見齊先可以報「見齊」。逐張追查後結論係
**10 張全部喺現行引擎下播唔到**，每張阻塞原因唔同，全部有代碼＋實機雙重證據
（`qa127/drive127b.py` T1–T5、`qa127/drive127c.py` T1b、`qa127/tally_talk127.js`）。
loader 證明係本批驗收上限；跟進要內容／引擎改動，另開票，唔喺本批範圍
（唔改 content pack JSON 係紅線）。

1. **cast_main.json 死檔——4 張**（`cheng_william serious／shy`、`mok_siufai sad`、
   `uncle_kim smile`）：4 句只喺 `content/cast_main.json`（npcs[5] greet／advice、
   npcs[9] pressure、npcs[10] advice）。`cast_main` 喺 index.html 出現 **0 次**，
   從未被載入；T5 全程 104 個 resource entries 入面 **cast_main fetch＝0 次**
   （對照 story_detail＝1、npc_lines_core＝1）。12 個 cast NPC 嘅對白池全部係死檔。
2. **pack 節點被主幹覆寫——3 張**（`lan_ruoxi serious`、`kwan_hoimei serious`、
   `uncle_kim serious`）：3 句只喺 `content/story_detail_c1_to_c17.json`
   （nodes/8 C9 beat 6 lines[1]、nodes/12 C13 beat 5 lines[1]、nodes/15 C16 beat 4
   lines[1]）。載入時主幹覆寫（`applyStorySpineOverrides46/48`）換成 spine／LIVE 版；
   T3 新基底再確認：C9 播 1991 年冬酒廊／何生追數（22 步）、C13 播 1992 年冬賀歲片
   煞科（28 步）、C16 播 1992 年秋末舞蹈室程天諾練舞（29 步），3 張目標 found＝[]。
   `findNode`／`findNodeRaw` 同解（後者只係前者加 `.node`），冇 raw-pack 路徑。
3. **resultBeats 引擎唔讀——1 張**（`ching_tinlok think`）：唯一出處係 C16_a 抉擇
   resultBeats（index.html:21190，括號舞台指示句）。T2 實機：播 LIVE C16、揀
   「靠修音」（C16_a）後 **effects.notes 現身（True）、resultBeats 程天諾句唔現身
   （False）**。`applyChoice` 只讀 `effects`（flags／stats／ripple／tags／notes）；
   全檔唯一 `.resultBeats` 讀取係 C1 文字 canon（`softCanonC1Face`，數據映射，唔係播放）。
   （v125 已確立：resultBeats 50 句繼續唔播，引擎設計。）
4. **傾談分流錯配——2 張**（`chow_choiyi angry／sad`）：5 句只喺 `NPC_TIER_LINES`
   （colleague.daily[1]、colleague.insider[2]、rival.insider[0,2]、director.daily[1]）。
   `npcTierPool(npcId, aff)` 只回傳 `NPC_TIER_LINES[npcId]`；T1 點票（直接執行遊戲真
   `pickNpcLine` 代碼，aff=100，每 NPC 2000 抽）：colleague 72＋99、rival 76＋72、
   director 70、**reporter 0、agent 0**——周采兒永遠唔會講呢 5 句。T1b 實機：
   曉晴（colleague，aff 100，紅棉影業）第 3 談講出 chow_sad#1
   （「陸柏言嗰場戲，佢明明背熟晒對白…」），頭像三談 **byte-identical 靜態 bust**
   （data URI 19,935 字元，唔隨句變）；傾談 modal 用 `PORTRAITS[npc.face]`，
   唔行 dlg106 loader。截圖 `qa127/shots/branch_T1b_talk3_colleague.png`。
   附帶發現：入地點 sheet 要先拆 WF4 風物卡多頁 modal（繼續 → 睇落去 → 二揀一
   「認真跟住企一次」／「追問埋點樣收尾」），拆完返地圖再入過先開到 sheet
   （攔截後重入免費）。
- **盤點教訓**：表情盤點「常駐」桶（396 句）混埋死檔——`cast_main.json` 嘅句同
  live 傾談池嘅句同屬「常駐」，但前者從未載入。**下一批批單要先分生死檔，唔好再
  按 corpus 句數直接排。**
- s5_c16a `StoryPlay.start("C16_a", {force:true})` 回 False（C16_a 係 choice id，
  唔係 node id）——預期之內。

## 紅線
- SAVE key（`starVolunteer_map_v19w`）、softRev（s107）、產品 `?v=`（v20a10）全部唔郁
  （diff 零出現）；`content/` 零改動；**index.html 零改動**（本批純加圖＋加測試）。
- 動畫參考規矩唔適用（本批冇動畫）。

## 殘留（唔喺本批範圍，另開票）
- **rec_star（天星音樂）巧遇攔截唔觸發**（見上）：luk／ching／chung 在場都 trig=0，
  其他地點正常。
- **pack C9／C13／C16 被主幹覆寫**（見上；同 3 張圖同一根因）。
- **cast_main.json 死檔**：12 個 NPC 對白池從未載入（4 張圖＋其餘句）；要接駁定刪除，
  等拍板。
- **傾談分流錯配**：chow 5 句盤點歸周采兒、運行時歸曉晴／高俊傑／張子駿；要定係咪
  重寫歸屬／補周采兒真對白／傾談 modal 行表情 loader。
- **resultBeats 50 句繼續唔播**（v125 已知引擎設計；程天諾 think 句係其中之一）。
- 下一批表情候選（見覆蓋率殘留缺口表；頭選 ngai_wingnaam 10、lin_hiu 9）。
- v125 殘留 4 個缺檔：`crew_laolinji_serious`、`ho_sang_surprise`、`liu_bingxing_sad`、
  `extra_ad_fen_serious`（最後一個係旁白假陽性，唔補；其餘 3 個未排期）。
- 舊殘留：WF4 舞台太細（342×168px、人物 34×100px）要另開一票改 modal 幾何；
  開局企立＋UI40_STAND 9 張舊圖未換（要成張全身圖，另開一票）。

## 出貨
新制：分支 `v127-expr` → checkout main → `git merge --squash v127-expr` → commit →
push main（經 deploy key，唔使 approve；唔開 PR）。合併後 curl 線上核實 index byte／sha
＋22 張新圖逐張 200。

<!-- 合併後補：main commit／線上 byte／sha／逐張圖 200 核實結果 -->
