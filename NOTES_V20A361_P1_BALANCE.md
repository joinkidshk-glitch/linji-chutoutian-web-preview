# v20a361 — 實玩評估 P1 兩項平衡修復（頒獎天花板＋結局可達性）

用戶 2026-11-21 14:09 批准開票。範圍只做 P1 A＋B，P2（試鏡曲線／經濟／動畫等）未動。
驗證：qa361/qa361_harness.js（36 項，真引擎／真函數抽取）＋tests/test_p361_static.py（35 項）；
suite 400 PASS／9 FAIL（基線 399/9，新增 p361 靜態釘 +1，九項 pre-existing 不變，零回歸）。

## A：頒獎天花板（贏線 0.875 不變，抬天花板）

根因（W2 真引擎重算）：廣告桶封頂 ad_av 0.48／ad_print 0.40，理論天花板 base 0.7951（P=0%）；
綜藝司儀格同樣；音樂要借電影擔正先有機會。

修法：新增三個擔正級 roleScale，q 一律 0.78（同 film_support_main 同級）：
- `ad_lead`／`music_lead`／`variety_host_lead` 加入 AWARDS62_ROLE_Q、ROLE_SCALE_BAND
  （ad_lead [1,2]／music_lead [6,14]／variety_host_lead [1,3]，同各自媒介既有工期帶同寬）、
  AWARDS65_LEAD_SCALES、END95_LEAD_SCALES、PRESS94_NAMED_SCALES、end229IsLead
  （ad_lead＋代言/主角、music_lead＋主唱、variety_host_lead＋主持）。
- 通告庫（323→326 張）：
  - 轉換 11 張現有通告：廣告 gig_1992_ad_107／gig_1992_ad_203（ad_av→ad_lead）；
    綜藝 gig_1991_variety_103／gig_1992_variety_102／gig_1992_variety_106（variety_special→variety_host_lead）；
    唱片中級＋高級大碟主唱 6 張（gig_1990_rec_110、gig_1990_rec_303、gig_1991_rec_107、
    gig_1991_rec_108、gig_1992_rec_105、gig_1992_rec_109，rec_album→music_lead）。
  - 新增 3 張：gig_1991_ad_109《清涼一夏》廣告主角（高級，恒昌電器冷氣機）、
    gig_1991_ad_110《穩健同行》廣告主角（稀有，港城商業銀行形象廣告）、
    gig_1991_variety_110《全港同心夜》慈善晚會主持（高級）。
  - 1990 不設 ad_lead：1990 跨媒介 crossQ 上限 0.78，即使加 ad_lead 天花板仍 <0.875
    （與電影 1990 年無 film_lead_big 同口徑，第一年廣告獎難贏屬設計）。

真引擎重算（qa361 harness A 段，修前→修後 full-kit 天花板／P(win)）：
- 廣告 1991/1992：0.7951（0%）→ 0.9000（75%）；strong-year（3 作品＋中級跨媒介）：0.8633（38%）。
- 綜藝（司儀）1991/1992：0.7951/0.7909（0%）→ 0.9000（75%）；strong 0.8633（38%）。
- 唱片 1990：0.8656（41%）→ 0.8824（57%）；1991/1992：0.8944（69%）→ 0.9000（75%）；
  strong 0.8310（6%）→ 0.8798（55%）——唔再一定要借電影擔正，跨媒介 q0.78 已夠。
- 電影／電視不變（0.9000／75%）。
即每個媒介滿配天花板同影視睇齊（0.90），要接近滿配（2 張擔正級＋跨媒介作品）先贏，唔易但贏得到。

未採納 GPT 嘅「cross 封頂 +0.010」同「純媒介基準 0.865–0.880」（GPT 自標首輪試值）；
保留 FIX65-3 跨媒介獎勵哲學，只抬天花板。

## B：結局可達性（GPT 方案）

根因（W4 36 播種案例）：信用係派生值（fame×0.5＋台風×0.3＋演技×0.2＋delta），
E3/E5 被 E2（credit≥42＋fame≥35）排喺前面吞咗，只剩 fame<35＋credit≥121 死位；
E4（fame≥50＋credit<30）同派生下限矛盾且 dual<155 被 F2 兜底改判 E7；
E0 同樣被 F2 蓋過。

修法四項：
1. **獨立信用來源（合約信用）**：殺青完成合約 +1、高級／稀有額外 +1，正增長每季上限 +4、
   工作來源生涯上限 +36，寫入 industryCreditDelta（contractCredit361OnWrap，殺青 hook 喺
   end95AddWrap 旁；季＝13 週）。舊檔由 wrapHistory 按時序重播同一套上限一次性回填
   （contractCredit361Backfill，normalizeSaveObj 呼叫，wrapHistory 上限 90 條係下限）。
   「準時」無獨立訊號，以 tier 代替（寫明）。
2. **判定次序**：E3/E5 移到 CR/E2 之前（ID 之後），加 **credit > fame**（信用主導）守門，
   避免搶走一般演員格。E4 次序不變。E1 門檻（dual 350／fame 70／credit 65）不變。
3. **1992 floor 155→140、warnLine 195→180**（保留 40 點警告帶，同 1990→1991 帶寬升幅一致）。
   F2 兜底覆寫加豁免：ending361FloorExempt（E6＋明確路線 E3/E4/E5），
   「先判明確路線，再判 E7 兜底」——E4 dual 天生 <90，唔豁免永遠被 E7 蓋過。
4. **負標籤即時預警**：applyCastingTags 新增負標籤（八卦／耍大牌／高冷／爛片）即 toast
   （第 1 個提示上限、第 2 個起強警告）；gaps95 加負標籤交代行（neg≥2 時講明擋住天王／巨星格）。

可達性證明（qa361 harness B 段，25 案例全過）：E1／SS／FK／TK／SK／GH／CK／AK／ID／CR／E2／
E3（大導演／金牌監製／製片老闆三變體）／E5／E4（sunk／rescued）／E0／E7／E6 全部有正常路徑落點。
例：E3（F50/C100＋導演 rel70＋合約信用 +20）、E5（F55/C91＋人情 8＋何生 rel70）、
E4（F54/C29 高壓未練台演）、E0（F30/C116 無幕後證據）。

## 測試釘更新

- 通告庫 323→326：test_gig229_pack／grant／press94_advice／years、test_gig291_winter、
  test_nat92_logic（311→314）、test_r286_load_year_sync（1991:105→108）、test_sideline280_logic、
  r299–r322／r337／r5_284／sideline274 嘅庫總數守門（26 檔）。
- test_gig229_pack：五級分布（高級 23／稀有 22）、作品 199、cast 256、影視廣告作品 136、唱片綜藝作品 63。
- test_gig229_trigger：稀有級 21→22。test_sideline158_logic：司儀 matcher 6→7（variety_110）。
  test_r319_pang_echo：v106 roleScale→variety_host_lead、司儀類 6→7。
  test_awei195_logic：真男主角數 1990:0→2、1991/1992:8→14（music_lead/ad_lead/variety_host_lead 入列）。
- floor 155→140：test_conseq61_1992_logic（warnLine 195→180、邊界案例 139/140）、
  test_r345_fullarc_fix（floor 140＋新增 E4/E3 豁免 2 案例＋ending361FloorExempt 抽取）、
  test_gate136_static。
- 行號釘 resync（index.html 淨 +93 行，47068→47161；qa361/resync361_apply.py difflib 映射，
  逐行核實內容逐字相同純漂移）：test_travel114_static、test_tang152_static、test_tang171_static、
  test_tang173_static、test_gift185_static、test_rom159_static、test_rom176_static、test_text125_static。

## 未做（跟進）

- P2 項目（試鏡曲線／經濟／動畫／系統回饋黑箱）等用戶拍板，未動。
- W4 C1：總結頁「（review1992版）」內部字串未包喺本票。
- 1990 廣告獎仍贏唔到（設計：第一年無 ad_lead，與電影 1990 年無擔正同口徑）。
