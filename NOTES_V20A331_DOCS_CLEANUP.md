# NOTES_V20A331_DOCS_CLEANUP.md — v331：SPEC 12→17 紅星清理＋B1 五則實裝註（docs-only）

## §一 改動（docs-only，唔郁 game code／測試／index.html／gigs_new.json）

### A5. `~/workspace/linji-gig-redesign/SPEC.md`（live 名冊 17 位，v290）
- L61「F8 選角對位（12 紅星＋2 位新女星）」→「17 紅星」。
- L63「12 紅星定位」→「17 紅星定位」，補藍若曦（電視台 PA／場記轉歌手）、胡美琳（影視花旦，巔峰 1990）、韓秀婷（跳唱天后，巔峰 1991）三句（照 v290／v204 設定）。
- L212 欄位表「12 紅星 id＋沈映雪／江詩盈」→「17 紅星 id」。
- §2.7 對位表（L319 起）補 3 行：藍若曦（唱片／電視）、胡美琳（電影／電視）、韓秀婷（唱片／綜藝），限制一律「見 v290 設定」，唔憑空加。表由 14 行→**17 行**。
- L969「12 紅星主場／副場」→「17 紅星主場／副場」。
- SPEC 係下一次全庫重生成嘅設計檔，改數字唔影響 live。

### B1. `~/workspace/linji-story-sidelines/drafts/batch2-lok-ngai-chai-pang.md`（跟 live，唔改 code）
裁決 brief `~/workspace/linji-brief-b1-b2-adjudication.md` §3 逐字抄，寫法跟 L323 已有嗰則（`> `）：
1. L90（駱 Beat 2）下面加一則：維持 live `lok_help` 閘 T3＋歌藝≥35（v278 NOTES L59），唔跟草稿 T1–T2。
2. L323 已有實裝註（現 L327）內補一句：Beat 開閘嗰半同樣維持 live（T1＋E4 新聞出街，`index.html:41777`）。
3. L590（魏 Beat 3）下面加一則：買茶冷版已跟（v278）。
4. L1373（彭 Beat 3）下面加一則：維持 live 無年份閘（v278 NOTES L59＋Q21）。
5. L1112（齊 Beat 5）下面加一則：維持 live `chai_repay` 閘（v278 NOTES L59）。
- 插入後新註位置：L92／L327（原有則）／L594／L1118／L1381（由底到頂插，行號逐則 ＋2 漂移已核實）。

## §二 驗收
- `grep -n "12 紅星\|十二紅星" SPEC.md` ＝ **0 命中**；`grep -c "17 紅星"` ＝ 4（L61／L63／L212／L969）；§2.7 表 17 行（陸廖魏葉麥駱彭鍾顧蘇齊程沈江藍胡韓）。
- `grep -c "實裝註 2026-11-19"` 草稿檔 ＝ **5**（L92／L327／L594／L1118／L1381）。
- Game code／測試／index.html／gigs_new.json 零改動；唔使跑 suite（docs-only）。`qa296/derive296.json` 嘅 M 係 parent 嘅 v330 suite 重跑再生，唔入本票 commit（本票只 commit 呢個 NOTES 檔）。

## §三 備註
- B1 裁決關鍵：草稿閘門行寫明 live 係「原閘」，草稿數係事後提案，唔係 live 偏離原設計；v278 NOTES L59 已裁決「其餘閘跟 live」，今次逐處重新論證過先跟。
- 下一票按 triage 建議：v332 攻略 A6（須 parent 授權後行 repair 流程）、v333 B2（魏腿替身缺位修正版選項 i）。

## §四 合併＋部署（待填）
- NOTES-only commit → push main → `git ls-remote` 核實。
- 唔使 Pages 核實（index.html 零改動）。
