# NOTES v20a237 — RW-3 對手／師徒線逐句重寫

- 日期：2026-11-16
- 分支：`v237`（base main `210f253`，v236 已上線）
- 工作報告：`~/workspace/linji-language-sample/RW3A_WORKLOG.md`

## 改咗乜

`content/story_detail_rival_mentor.json` 一檔，40 個節點（A_ko／A_hakfan／A_tsijun／A_fong／A_tong／A_ho／A_gao／A_lei 各 5 幕），輕口語對白＋香港式書面語旁白逐句重寫。

- **實寫 378 處字串**，舊 596 句 → 新 517 句（範圍內 live 句 744 句，實寫比例 80.1%）；保留未改 125 處（已合標準）。
- **WF4 內嵌版 20 節點**（ko／tsijun／fong／ho）：重寫 `index.html` 內 `RIVAL_WF4_OVERRIDES` 嘅 beats＋synopsis（127 處），再同步返 JSON（同一措辭；JSON 拍數由 3 拍擴到 5–6 拍，跟內嵌版）。其餘 20 節點（hakfan／tong／gao／lei）直接改 JSON。全部 40 節點嘅 choices label／notes 改 JSON。
- 只改文字，唔改劇情、旗標、數值、結構、node id、beat speaker 次序、title／setting／when／cast／eraTag／qa／arcs。
- **TEXTFIX55 拆走 12 條**：EXACT 2 條（171→169）、NOTE_EXACT 10 條（36→26），逐條對值核實後先刪（5 條 ALIVE＋5 條死 key；感情線相關 key 留返 v238）。
- A_ko_push1 title「同場走位互懟」唔郁（PHRASES「互懟」→「駁火」keep，繼續兜底）。

## 驗收

- `python3 -m json.tool` 通過；`vm.Script` 編譯全部 2 個 inline script block 通過。
- 載入模擬（JSON → WF4 → `textfix55StoryPack`＋`textfix55RivalSpeakers`）：只剩 4 處預期 diffs（title PHRASES 1＋lei speaker 翻轉 3），**新句 0 處被覆寫**。
- 禁詞掃描新句範圍 0 命中；10 句試讀全部一次讀順。
- 全套 suite：**314 PASS／10 FAIL**，同基線 314／10 完全一致，FAIL 名單逐項相同，零回歸。
- Live drive 實機抽檢未做（瀏覽器唔可用，押後）。

## 留意

- 起草嗰陣一度憑印象寫錯 A_ho／A_gao／A_lei 舊句（133 處 0 命中），覆核腳本捉到後已按原文重寫，378／378 逐條核實恰好命中一次先套用。
- `qa.afterSamples` 保留三條舊句做 QA 樣本（唔係 live 文字，無測試讀佢哋），按「qa 唔郁」留低。
- A_lei 三拍 speaker 錯標（「張克凡」）由 load 層修正，新句保留行首「雷先生」，修正繼續生效。
- WF4 內嵌表本身刪除唔係今版範圍（今版只係同步措辭一致）。
