# v382 自備戲服通告（服裝系統獨佔入口）

用戶 2026-11-22 拍板「偏弱系統加強」次序②。方案來源：`~/workspace/linji-systems-balance-2026-11-22/REPORT.md`（GPT-6.2-sol＋Claude Opus 5.5 一致建議：唔開新玩法，加獨佔入口）。

## 功能
- 少量通告列明「自備戲服」：玩家持有對應類別服裝（戲行／舞台／正式／日常，四類跟 `CLOTHING_CATS265` 對應）先可報名；未持有時通告卡出細紙標籤「自備戲服 · 類別（未持有）」、詳情頁要求行寫明「自備戲服：需要「X」類服裝（未持有）——到花園街成衣店選購對應類別服裝後即可報名」，首次見到要求時另出一句一次性提示（`S.flags.costume382Seen`）。
- 選取規則（`costume382GigReq`）：只揀中級／高級／稀有 tier（連舊標籤 中／高）通告，以通告 id 雜湊 %10==3 抽約一成；排除入門／補位／softBridge／武指彭人情渠道／引薦觸發通告。genre 對應類別：武俠／動作／警匪／江湖／歷史／賭片→戲行；唱片＋舞台類 genre→舞台；廣告→正式；其餘→日常。
- 實測全庫 330 張有 11 張被標（戲行 4／日常 3／舞台 3／正式 1），全部屬 1991／1992，開局 1990 板面零影響。
- 閘門掛入 `canAudition`（信用閘之後、檔期閘之前），書面語理由指去花園街成衣店；`gateShortReason` 同步。試鏡成功率公式、換衫加成、贏線 0.875、floor 140、warnLine 180、E1 門檻 350、SAVE key、softRev、產品 `?v=` 一律不變。
- 詳情頁「差幾多達標」加自備戲服行（✓ 已持有／✗ 未持有「X」類服裝）；只欠戲服而無數值缺口時，CTA 改「去花園街成衣店」（計出行，travel114 COUNT 類）。

## UI
- 先諮詢 GPT-6.2-sol（原稿 `~/workspace/linji-drive382/gpt_plan.txt`，brief 寫明終極目標原生 iOS app）：短卡細紙標籤跟觸發標籤同排、詳情頁要求行、首次提示一次、唔全卡變灰。CSS 一行 `.gt-pill.gt-costume382`。

## 驗證
- 邏輯測試 `tests/test_costume382_logic.js` 全 PASS（選取、類別映射、門檻前後、呈現兩態、首次提示只出一次）。
- Resync `qa382/resync382.py`（index.html 淨 +99 行）：8 個測試檔釘更新逐個覆驗 PASS（含 travel114 新增呼叫點分類）。
- Playwright 實駕 `~/workspace/linji-drive382/probe382e.py`：開局 1990 板面 14 張 teaser／9 張 ready／0 個戲服標籤；1991 夏九龍電視台板面目標通告 `gig_1991_tv_111`（時裝處境→日常）鎖定＋標籤在 DOM；詳情頁「差幾多達標」紅字 ✗ 自備戲服 未持有「日常」類服裝＋CTA「去花園街成衣店」；零 page error。
- 全套 suite：見 `~/workspace/suite382_v3.txt`（基線 400/9，新增邏輯測試 1）。
