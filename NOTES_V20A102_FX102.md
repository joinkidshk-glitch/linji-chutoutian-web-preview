# NOTES V20A102 — FX102 行程像素動畫全量＋接入

## 合併基線（重要）
- 本包工作副本由 v20a101 開出；出貨前已先將 **main 最新版 merge 入分支**
  （merge commit f961dd2，基線 **v20a104 / git 639a7be**），零衝突。
- v20a103/v20a104 嘅改動（`LOC_SHEET_BG` 逐地點新檔、`spBgImageCandidates`
  檔案鏈行先、背景圖版本參數 `?v=20a104` 兩處、新場景圖 14 張）喺合併檔
  逐項核實齊全，冇俾本包覆蓋。本包只郁 fx 接入代碼段。

## 內容：八條行程像素動畫（assets/fx/）
統一規格：240×135 逐粒畫、3 秒 24fps 無縫循環、960×540 mp4；
人物跟 **samples19 定版標準**（第十六版＋三輪修訂：碎瀏海深度圖／
光澤簇／鬢邊收分、raiseN 肘彎＋膊升＋頭移、outN 彎肘攤手、場記板
細步斜棒、近黑 1 格剪影邊、表情全實線）；人物全部由共用庫
anim_lib.draw_person 即時渲染，冇烘死入底圖。
背景按用戶 21:31 指示對位遊戲場景圖；場景圖重製（v103）落地後，
底本已換成**新場景圖**逐條對位（錄音片按合併時 main 最新版
bg_loc_rec_wanchai＝v104 版核對）：

| 片 | 場景／對位來源 | 完成 beat | 接縫 | 量度 |
|---|---|---|---|---|
| fx_shoot.mp4 | 片廠（film_lion）：佈景板改畫唐樓街景布景（窗＋招牌帶＋簷篷），保留定版構圖 | Cut 打板＋星閃 | 0.014 | 定版參照本身 |
| fx_shoot_ext.mp4 | 街景（film_lion 街景）：唐樓＋鐵閘＋綠簷篷＋晾衫竹＋反光板 | 同拍攝版節拍 | 0.0 | ext 帶 PASS（bgS 28.4／gapS +84） |
| fx_record.mp4 | 灣仔唱片新圖（v104）：開盤帶機（玻璃後）＋紅燈置玻璃頂＋譜架＋掛牆耳機＋混音台 VU 錶排＋暖米木牆 | 紅燈熄＋除耳機＋錄音師舉手＋星光 | 0.0 | dark 帶 PASS（gapS +32／gapV +33） |
| fx_audition.mp4 | 九龍電視台新圖：成幅 CRT 電視牆（5×3）＋綠腰線牆＋水磨石地＋木門 | 評判點頭＋主評判舉綠牌＋星光 | 0.0 | pale 帶 PASS（bgS 36.6／gapS +55） |
| fx_train_a.mp4 | 龍門電視台新圖：水松通告板＋白紙（代黑板）＋水磨石地；落地鏡牆保留 | 導師舉手＋星光 | 0.0 | pale 帶 PASS（gapS +63） |
| fx_train_b.mp4 | 星河唱片新圖：金唱片框×2＋彩色海報塊；鋼琴＋化妝鏡燈保留 | 老師舉手＋大星光 | 0.0 | day 帶 PASS（gapS +55） |
| fx_train_c.mp4 | film_lion 片廠角：戲服架（衣架鈎＋斜肩＋襟線）＋沙包堆＋兵器架；榻榻米＋木人樁保留 | 出拳擊中衝擊星＋師傅點頭 | 0.0 | day 帶 PASS（gapS +38） |
| fx_rest.mp4 | 跟現行瞓覺片內容（床/枱燈/窗夜景/Z）以新標準人仔重做 | 呼吸起伏＋Z 浮動（無敘事 beat） | 0.0 | night 帶 PASS（gapS +32） |

量度口徑：verify_measure.py（有人版 vs 無人版差分遮罩，HSV S/V 平均）。
淺色場景（試鏡室/表演教室/外景）bgS 天然低，另設 pale/ext 帶並註明
理由——唔為就量度改走場景身份（用戶 21:31 原則）；硬指標係差距。

## 接入（FX102）
- 機制跟 v20a10 休息片：日結板頂嵌 `<video class="act-fx102">`
  （muted/loop/autoplay、唔阻斷流程），純視覺——**唔掂存檔／數值／
  判定**，舊存檔零影響；週加速期間唔播（跟休息片先例）。
- `resolvePlannedDay` 加 local `fx102Kind`：shoot 分支用
  `actFx102KindForShoot(sh)`、job 分支只喺真試鏡嗰個 sub-branch set
  `"audition"`（資格不符／已等消息唔播）、train 分支用
  `actFx102KindForTrain(id)`；喺通用 modal 呈現前計好 html、
  modal 後 `armActFx102()`；`closeModal` 加 `stopActFx102()`。
- 地點即時訓練：`afterDayModal` 加 `opts.fx102Kind` 支援，
  `doEnrollRun` 按 `tr.courseId` 傳入。
- 映射規則：唱片類（type 含「唱片」/music/locId `rec_` 開頭）→record；
  標題關鍵字（外景/戶外/街頭/廟街/夜市/碼頭/沙灘/海邊/郊野/城門河/
  天台/遊樂場/村屋/渡輪）→shootExt（「清水灣」唔入列——片場係室內）；
  其餘拍攝→shoot。訓練：acting/stage/charm/iq→trainA、vocal/looks→
  trainB、stamina→trainC。
- 全日休息：`REST_SLEEP_FX_SRC` 改指 `fx_rest.mp4`（舊檔
  `awei-rest-sleep.mp4` 保留唔刪）；**`restSleepFxCheck()` 嘅 src
  斷言同步改版**（有意改變行為）；FX102 自檢 `actFx102Check()`
  嘅 SAVE 把關委託 restSleepFxCheck，唔重複 SAVE 字面值
  （polish48 等四個靜態測試精確計數 ==10）。
- 所有新函數呼叫點跟代碼慣例加 `typeof` 守衛（抽函數沙盒測試需要）。
- 紅線不變：SAVE key `starVolunteer_map_v19w`、softRev `s107`、
  產品 `?v=` `v20a10` 全部冇郁。

## 測試
- 新守門：`tests/test_fx102_logic.js`（22 項：映射表/拍攝/訓練映射/
  html 生成/頁內自檢；對 v101 index 反證 FAIL）、
  `tests/test_fx102_static.py`（資產存在/接線點/紅線；對 v101 反證
  34 FAIL）。
- 全套 A/B（基線＝v104 main）：基線 125 PASS／12 FAIL（環境性）→
  合併版 **127 PASS／12 FAIL，FAIL 集同基線完全一致**，零回歸。

## 實駕（本地鏡像，qa102/）
- drive_fx.py：拍攝 fx_shoot／錄音 fx_record／外景 fx_shoot_ext／
  試鏡 fx_audition（gig_1988_entry_ad_passerby）——出啱片＋真係播緊
  （currentTime 推進）＋冇 pageerror。
- drive_fx2.py（新局版）：訓練甲/乙/丙＋全日休息 fx_rest——9/9 PASS。
  （連跑多場景嗰陣訓練日改植唔咬係駕駛狀態問題，逐個新局驗證通過；
  遊戲本體計劃日流程由 drive_fx2 證明正常。）
- 截圖存 qa102/out/；動畫幀 vs 場景圖對照圖存
  linji-anim102/verify/compare_*.png；生產管線存 linji-anim102/
  （build_*.py＋common.py＋anim_lib.py＝samples19 庫）。
