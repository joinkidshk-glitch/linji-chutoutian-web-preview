# NOTES_V20A405_P1_FIXES

v405：v403 深度試玩 P1 七項修復（基線 v404，main `58c0b19`；分支原基 v403 `ce3b547`，落地前已 rebase）。
證據來源：`linji-playtest-v403-2026-11-25/REPORT.md`。用戶 2026-11-26 00:29 HKT 批准開始修改。P2 項目本版不做。

## 改動一覽

### P1-1 E1 電影擔正供應＋戲服閘疊加
- `costume382GigReq`：`roleScale==="film_lead_big"` 一律不疊自備戲服閘（戲服係門檻加成，唔係入場券）。排除後 %10==8 池冇日常類，日常類補選 %10==3，保四類每類至少一張（v386 標準）。
- 新增 `filmLead405EnsureBoard`（跟 `variety392EnsureBoard` 同規則）：電影地點（film_lion／film_harbour／film_cotton）板上無 film_lead_big、玩家聲望 ≥32 且演技有效數值 ≥85 時注入一張，留板 7 日、14 日不重複（狀態 `S.filmLead405ByLoc`），喺 `gigsForLocSeasonBoard` 呼叫。
- E1 其餘門檻（獎項、脊骨、雙軌、負標籤）不變，正常打法仍需獎項＋脊骨先入 E1。

### P1-2 v400 壓力建議掣 140 週 0 次
- `freeDays400` 可換日擴至訓練日／兼職日（自由日優先，拍攝鎖位照擋）。舊制只認自由日，高峰週結構性冇目標日。
- 建議掣標籤按日型別寫明（自由日／訓練日／兼職日）。

### P1-3 E4 截 GH
- `resolveEnding410` 先計 `ghQualified405`（同 GH 分支條件：雙軌、綜藝佔比、綜藝宗數、彭少祺線進展），E4 分支加 `!ghQualified405` 守衛。E4 非綜藝路徑保留。

### P1-4 服裝成功率口徑
- `chance()` 改用有效數值 `costume265EffStat`（同 `reqGap` 一致），並加 `GIG_REQ_KEYS88` 過濾；無 req 分支同樣用有效數值。

### P1-5 廣告／綜藝頒獎雙擔正
- `awards62ScoreParts` 對 matchTypes 含廣告／綜藝嘅類別，worksScore 分母 1.6→1.32。贏線 0.875 不變；電影／音樂／電視分母不變。

### P1-6 感情 rel day 85 封頂
- `bumpRel` 加分段封頂：push1 未完成封頂 3、push1 後 5、push2 後 6、crisis 後 7（六線 hiu／choi／lan／xu／yip／so 同規則）。`applyChoice` 按 node id 後綴傳 paceCap（push1→5、push2→6、crisis／ending→7、meet→3）。負值照舊不 clamp；舊檔已超段嘅正增量只係不再升。commit 門檻 rel 6 要 push2 後先到。

### P1-7 送禮入口可發現性
- `addLocTalkGiftActs`：女角在場（面板 NPC 係佢，或巧遇在場盤 `rom176PresenceAt` 有佢）且已正式見面（meet done）時，地點面板出「送禮畀X」行動，開 `openGiftPick`。傾談照舊經巧遇。

## 驗收證據

- Suite：427 PASS／9 FAIL（9 項穩定 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），同 v403 基線一致。
- P1-2（`qa405/check_p12.js`）：零自由日高壓週出「用週一訓練日換休息」，撳掣後週一變休息。
- P1-3（`qa405/check_p13.py`）：GH 態修復前落 E4、修復後落 GH；E4 非綜藝態仍落 E4；GH 缺彭線進展仍落 E4。
- P1-4（`qa405/check_p14.js`）：演技 47 靠 c11（+3）有效 50，成功率 0.5225 同達標原值一致（裸值 0.1424）。
- P1-5 數學：單擔正強桶 base 0.8746（贏線 0.875，連品味 ±0.05 有機會贏），弱桶 0.7110 照輸；雙擔正保留優勢。
- P1-6 實駕：rel 分段 3→3（未 push1 封頂）→5→6→7，負增量照扣。
- P1-1／P1-7 實駕：見 `linji-drive405/` 證據（板面保證狀態、送禮入口截圖）。

## 測試同步

- `tests/test_v400_logic.js` 4A 期望更新至可換日新語義。
- 釘行 resync：`qa405/resync405.py`＋`qa405/resync405b.py`（difflib 映射，OLD=v404 `58c0b19`）：travel114／rom159／rom176／tang152／text125／gift185／tang171／tang173；總行數 52085→52227。
- `qa296/derive296.json` 為 suite 再生檔，不入版。
