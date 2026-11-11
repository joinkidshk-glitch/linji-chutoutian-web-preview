# v20a105 UI 修復包一：A 級硬傷（UI 審計第一期 28 項全處置）

底本：`~/workspace/linji-ui-audit/UI_AUDIT.md`（A 級 28 項）。三組 squash 入 main：
ENC105（D-2/D-3）＋WEEK105（S-12/13/14）＋UI105C（其餘 23 項編號），另加統籌裁決 commit（S-24×ENC79 護欄）。
紀律：SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=` `v20a10` 全冇郁；冇掂 B/C 級（D-8 只做第一階段場景底，具名企立屬第二包）。

## 逐項處置（詳情見各組 NOTES）
- **D-2** 12 星企立全接入（設計庫 p0/standing 入庫 `assets/story/era_stars/{id}_stand_default.png`，零 bust 頂替）＋候補鏈加剪影兜底，唔再「冇人」。**D-3** 巧遇背景改行 LOC_SHEET_BG 逐地點新場景，UI40 類別圖退兜底。
- **D-6** 旁白入底部對話框位。**D-7** 對話計數刪、幕標題只幕首閃現。**D-8（一期）** 隨機事件加當前地點場景底（wf4Scene105；冇逐地點圖嘅地點維持無底）。
- **S-12** 週界旗 `S.weekBoundary105` 落存檔，重開補呈現結算卡＋入編排步；恢復路徑唔呼叫 settleWeek，金額只扣一次（邏輯＋實駕雙證）。**S-13** `scrubInherited105` 繼承剔已完成通告＋todayPlanId 自癒＋paintBar 入口保底。**S-14** `S.execLog105` 記實際執行類型，回顧優先用紀錄、舊檔退槽位標籤。
- **S-3** 導入卡刪教學段＋重複段，教學搬行程編輯頁常駐一行（取捨：冇做逐畫面 contextual）。**S-6** 地圖面板貼圖高收死位。**S-10** 「›」釘卡右中線＋劇情卡副行截句。**S-16** 筆記紙左 padding 46px 黑環唔入字。**S-19** 壓力改行內展開明細唔再彈 modal＋文案重寫。**S-21** 在場紅星加頭像＋「遠觀」標籤（呈現層；實駕限制見 UI105C NOTES）。**S-23** 費用欄統一 $X／免費／+1日，實物名入 hint。**S-24** 見裁決。**S-25** 體檢先確認後扣錢＋醫院用途說明卡（禮品店明碼實價冇加確認，屬判斷）。**S-28** 未達標統一「現值／需 X（差 N）」。**S-31** 報名截止獨立行＋「仲有 N 日截止」。**S-32** 詳情卡高按內容收。**S-35** 獲聘 modal 重排結果→錢→之後，刪成功率＋含糊行（落選 modal 唔喺 S-35 範圍，冇郁）。**S-37** 殺青對帳只留 payWrapNote 一段。**S-39** 生活費提示改用完成日計星期，只六/日板出（兼修舊 code 早一日 bug）。**S-40** 支票插喺殺青行後、對帳行前，第一屏成張可見。**S-43** 屬性唔再顯示 /999（壓力 /100 保留）。**S-44** 開局冬季債狀態改「就嚟到期」對齊開局日＋債主台詞唔再重播。**S-45** 未開放遠幕合併一行。**S-48** 設定頁三行死掣成組收起，改「音效／音樂 … 即將推出」灰字一行。

## 統籌裁決：S-24 × ENC79 護欄衝突
審計 S-24 要刪事務所板結局配方句（劇透＋塞版）；ENC79 護欄（巧遇設計拍板）要求事務所標明信任「通去邊」否則 E5 幾乎行唔到。裁決分工：事務所只留信任數字＋下一階提示（S-24 照行）；「通去邊」按審計修法原文搬去**人情頁**定性承載——renderDebtPane 加指向行（信任深＋清債＋留債權→江湖路），講方向唔講數字門檻。`test_enc79_static.py` 護欄改驗新分工（事務所冇配方字樣＋人情頁有指向），三條全 PASS。

## BGM 包銜接位（S-48）
設定 modal 渲染函數 `openSettingsModal` 內 `.settings-list` 頂部嗰行 `.settings-row`（「音效／音樂 … 即將推出」）就係 BGM 包換真掣嘅位置；prefs 欄位 `bgmMuted`/`sfxMuted` 本包冇郁。

## 測試
- 新增守門：enc105（static+logic）、week105（logic 30/30＋static）、ui105（static 43 項）；全數對 v20a104 基線有反證（舊版行會 FAIL）。
- 舊測試按新規格更新（檔案內註明）：loc96_logic（S-25)、guidance34/verify37(S-28)、progress71(S-45)、enc79_static（裁決）。
- 全套 A/B：合併後 **132 PASS／12 FAIL**，FAIL 清單同 pristine 基線（127 PASS／12 FAIL）逐字相同（12 個全屬已知環境性 static FAIL），零新增回歸；index script `node --check` OK。

## 實駕證據
- ENC105：鍾楚凝＠金鐘創意、顧明輝＠海港廣播（兩位原缺圖星）有人＋新場景底（`~/workspace/enc105-drive/`）。
- WEEK105：16/16——週日 reload 補結算卡＋金額只扣一次、下週三今日計劃復常、上週回顧分類正確（`linji-work105b/qa105/`）。
- UI105C：受影響畫面逐個截圖（`linji-work105c-verify/shots105c/`）。
- 統籌綜合實駕（合併版，`linji-work105/qa105final/`）：人情頁指向＋S-44 第一天狀態、S-48 真選單路徑（探針複驗）、S-35 獲聘 modal（真 pendingAud 公佈鏈：冇成功率行、有簽約金段）、S-37 殺青對帳只一段（$516/$155/$361 對數）、S-40 支票第一屏成張可見（截圖肉眼定奪；量度矩形因 modal-inner 邊界差 7px，以截圖為準）。全程零 pageerror。

## 部署核實
- main 已推 GitHub：`c320f77..83bade2`（經 linji-repo 常駐 clone fast-forward＋push）。
- 線上 index.html：4,956,581 bytes、sha256 `9d939bb96941b083…`，同本地逐字一致（Pages 首次核實係舊版，等約 90 秒後轉新版，屬已知部署延遲）。
- 新資產線上可達：`assets/story/era_stars/chung_choning_stand_default.png` HTTP 200。
