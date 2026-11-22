# v20a386 第七輪評估修正（P1 一項＋P2 重點項）

日期：2026-11-22。來源：`~/workspace/linji-playtest-eval7-2026-11-22/REPORT.md`（live v384/v385）。
證據：`~/workspace/linji-drive386/`（GPT 原稿 gpt_text386.txt、probe386/b/c.py＋json＋截圖）。

## P1：戲服選取「11 張」名不副實（戲行零生效）

根因（對 live code 核實）：`costume382GigReq` 嘅 trigger 排除經 `triggerGigLabel229`，係
state-dependent（fame≥40 等觸發成立先排除）。hash 命中 11 張（戲行 4／舞台 3／正式 1／日常 3）
喺正常進度下 runtime 生效得 4–5 張、戲行 0 張（2 張 Mak 武指渠道、2 張 trigger），
c10–c12 戲行衫獨佔入口從未存在。

修法：
- trigger 排除改靜態：有 `trigger` 欄一律排除（邀約／引薦通告唔疊戲服閘，同武指／彭渠道同口徑）。
- hash 餘數 `%10==3` → `%10==8`：靜態池（tier＋entry/softBridge＋武指／彭／trigger 全排除）84 張抽 11 張，
  戲行 4／日常 1／舞台 3／正式 3，全部 1991／1992，開局 1990 板面零影響（Python 逐張複算＋
  test_costume382_logic.js runtime 口徑 stub 對齊，tagged=11 同複算一致）。
- 生效清單：戲行 gig_1991_film_107／gig_1991_film_206／gig_1991_tv_206／gig_1992_tv_108；
  日常 gig_1992_film_111；舞台 gig_1991_rec_107／gig_1992_rec_203／gig_1992_variety_201；
  正式 gig_1991_ad_203／gig_1992_ad_105／gig_1992_ad_204。
- Playwright 實駕：day 700 film_harbour 板面《沙田夜巡》＋「自備戲服 · 戲行（未持有）」pill；
  持有 c10 後 pill 尾消失、卡照在（probe386c.json）。

## P2-1：蘇待播便箋永不顯示

根因：便箋插入 `#loc-acts` 首位後，`openLoc` 結尾行 `ux68OrganizeLocSheet`，該函數
`box.innerHTML=""` 重建只保留 `.act` 按鈕；有待播劇情時 organizer 必行（urgent），便箋永不顯示。

修法：organizer 重建前收集 `.story-pending384` 元素，搬入 frag 最前再重建。
實駕：day 803 灣仔唱片（同第七輪 W1 觸發日）便箋文字正確顯示、`ux68-organized` 已行
（即重建後保留），probe386c.json note_day803。

## P2-2：補位失效文案「覆電限期已過」唔準

`intel381Tick` 失效時寫 `expiredFrom`（msg／kept）；留話簿 expired 分支按來源分文案：
kept 失效改「試鏡限期已過，這次補位試鏡資格已告失效。」（GPT-6.2-sol 文案，
原稿 linji-drive386/gpt_text386.txt）；msg 失效沿用現行文案。舊檔冇 expiredFrom 時以 keptDay 推斷。

## P2-3：戲服卡輪換消失定性

定性：driver artifact，唔係遊戲 bug。板面 pool 由 loc／季節／NAT92 窗／consumed 決定，
買衫唔改變 pool 成員；買衫前卡喺 locked `<details>` 區、買衫後移去 ready 區，
W2 driver 用 innerText 讀唔到摺疊 details 內容先誤報消失。本票實駕以 textContent 對照：
買衫前後《沙田夜巡》卡同 pill 都喺 DOM（probe386b/c.json）。唔改 code。

## P2-4：wk6 執行層休息覆寫缺口

核實：`lockShootsIntoDraft` 已跳過 rest（v380）；剩餘覆寫路徑係 `placeShootOnPlan` pass2
（經 confirmPlaceShoot modal 玩家確認）按星期序覆寫，週二休息位會先過後段非休息格被佔。
修法：pass2 改兩輪——先覆寫非休息格，唔夠先覆寫休息格；`previewShootPlacement` displaced
次序同步（modal 列名同實際覆寫一致）。`writeTodayPlan` 維持（玩家主動耗日行動嘅執行紀錄，唔假造）。

## P2-5：峰值預覽唔計已 lock 拍攝

`defaultWeekPlan` 峰值預覽改用 `lockShootsIntoDraft(plan)` 副本計（拍攝 +10/日入峰值）；
lock 會寫 `sh.daysLeft`，預覽前後 snapshot／restore 唔留副作用。
邏輯測試：入口 35＋5 日拍攝 → 峰值 85 → 三日休息；無拍攝對照一日（test_eval7_386_logic.js B 段）。

## 其餘 P2 逐項核實

- **蘇 commit 後 ending 仍可揀 BE**（真問題，已修）：判定只讀 commit 旗，BE 抉擇冇效
  （揀咗都出情侶場景）。`endingRomance410`＋`endingRomanceState48` 改為 BE 旗已立就唔當
  committed（最後抉擇生效，反悔路；差一步變體寫 BE 旗嗰陣 commit 未立，唔受影響）。
- **試鏡帶失效後卡留板**：設計如此（v383 NOTES 明言：資格過期後通告變普通通告留板），唔改。
- **1991 廣告獎提名未贏**：平衡觀察（專攻閘口徑，同前輪一致），唔改贏線 0.875。
- **wrapHistory 封頂 90 vs careerStats 111**：設計如此——careerStats95 係殺青累計計數器（v95），
  wrapHistory 係顯示／歷史窗口上限 90，兩者口徑唔同，唔改。

## 唔郁

SAVE key／softRev／產品 `?v=`／贏線 0.875／floor 140／warnLine 180／E1 門檻 350／
試鏡判定／頒獎／結局事業軸判定全部不變。Suite 404 PASS／9 FAIL（基線 403＋新邏輯測試 1，
九項 pre-existing 不變）；resync `qa386/resync386.py`（difflib 單次掃描 dict 查表）。
