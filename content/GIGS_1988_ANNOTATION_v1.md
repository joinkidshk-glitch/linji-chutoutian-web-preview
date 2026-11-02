# GIGS_1988_ANNOTATION_v1

> §2A 標註交付表｜version 2｜synopsis 鐵律：未改

## 自檢

| 檢查項 | 結果 |
|---|---|
| synopsis SHA256 30/30 不變 | PASS |
| 保護欄（title/blurb/pay/fame/req 等）不變 | PASS |
| eraTag 全在 §2A.6 詞表且為單一 string | PASS |
| 每則含 boardPriority／boardNote／eraTag／discoverNote／seasonWeight | PASS |
| high 計數 春≥4 夏≥4 秋≥2 冬≥3 且 high∈主詞 | PASS {'夏': 4, '春': 4, '冬': 4, '秋': 2} |

### high 計數按季

- **春**：4 high（目標 ≥4）
- **夏**：4 high（目標 ≥4）
- **秋**：2 high（目標 ≥2）
- **冬**：4 high（目標 ≥3）

### eraTag 分布

- `era_1988_autumn_readthrough` × 1
- `era_1988_autumn_studio` × 4
- `era_1988_autumn_unitdrama` × 1
- `era_1988_spring_alley` × 3
- `era_1988_spring_factory` × 2
- `era_1988_spring_grassroot` × 2
- `era_1988_summer_karaoke` × 1
- `era_1988_summer_mall` × 5
- `era_1988_summer_variety` × 3
- `era_1988_winter_festive` × 3
- `era_1988_winter_record` × 3
- `era_1988_winter_recruit` × 2

### synopsis 不變證明（SHA256）

| id | sha256 |
|---|---|
| `gig_1988_ad_01` | `dc52cd54361348ab…` match=True |
| `gig_1988_ad_02` | `cef9692bec2e30d8…` match=True |
| `gig_1988_ad_03` | `12fc51eb8b36b73e…` match=True |
| `gig_1988_ad_04` | `91586e1524c2643e…` match=True |
| `gig_1988_ad_05` | `44beec33e6ea4434…` match=True |
| `gig_1988_ad_06` | `b7950fa5f2fab6ed…` match=True |
| `gig_1988_ad_07` | `1534ad0e15102dd6…` match=True |
| `gig_1988_ad_08` | `62b009ebd2e3695a…` match=True |
| `gig_1988_film_01` | `a15e49edc3fe2871…` match=True |
| `gig_1988_film_02` | `7f9dce15fe6a9978…` match=True |
| `gig_1988_film_03` | `f5d4b49791f326c5…` match=True |
| `gig_1988_film_04` | `9245a661b133fbf4…` match=True |
| `gig_1988_film_05` | `9b8594e1ff4a01bf…` match=True |
| `gig_1988_film_06` | `e2cafa4be9601492…` match=True |
| `gig_1988_rec_01` | `954780886439b82e…` match=True |
| `gig_1988_rec_02` | `b5319aa38014e2ee…` match=True |
| `gig_1988_rec_03` | `3f1becb0028c6a7d…` match=True |
| `gig_1988_rec_04` | `e3fa0396c79ff067…` match=True |
| `gig_1988_tv_01` | `53baacdedaa43e67…` match=True |
| `gig_1988_tv_02` | `6b85ed2443402e83…` match=True |
| `gig_1988_tv_03` | `d0609d2227516cb2…` match=True |
| `gig_1988_tv_04` | `5984d0695ccf7aa6…` match=True |
| `gig_1988_tv_05` | `51de33a17b1dd97a…` match=True |
| `gig_1988_tv_06` | `c2ce84e9056b6e30…` match=True |
| `gig_1988_tv_07` | `28e1a3597428ccba…` match=True |
| `gig_1988_var_01` | `7ef384fd925e235e…` match=True |
| `gig_1988_var_02` | `5c3de5624dbfdb9c…` match=True |
| `gig_1988_var_03` | `30ceae4e79746bec…` match=True |
| `gig_1988_var_04` | `5a5c6c6db6e2f9ef…` match=True |
| `gig_1988_var_05` | `a4818540d741e085…` match=True |

## 標註表

| id | season | type | boardPriority | boardNote | eraTag | seasonWeight | discoverNote | QA |
|---|---|---|---|---|---|---|---|---|
| `gig_1988_ad_01` | 春 | 廣告 | normal | 街頭廣告次級曝光 | `era_1988_spring_alley` | 0.6 | 中環經紀行佈告欄的公開選角 | OK |
| `gig_1988_ad_02` | 春 | 廣告 | low | 平面海報曝光有限 | `era_1988_spring_alley` | 0.6 | 導師引薦的喜慶海報試鏡 | OK |
| `gig_1988_ad_03` | 夏 | 廣告 | normal | 沙灘廣告商場向 | `era_1988_summer_mall` | 0.6 | 事務所發出的夏日沙灘選角 | OK |
| `gig_1988_ad_04` | 夏 | 廣告 | high | 無厘頭喜劇曝光 | `era_1988_summer_variety` | 1.0 | 道具房門口的緊急臨記招募 | OK |
| `gig_1988_ad_05` | 秋 | 廣告 | normal | 髮膠廣告棚次級 | `era_1988_autumn_studio` | 0.6 | 時尚總監預留的品牌試鏡 | OK |
| `gig_1988_ad_06` | 秋 | 廣告 | low | 快餐代言曝光有限 | `era_1988_autumn_studio` | 0.6 | 經紀人桌上的商業試鏡 | OK |
| `gig_1988_ad_07` | 冬 | 廣告 | low | 金錶奢華非賀歲主線 | `era_1988_winter_record` | 0.6 | 千金指定的高門檻代言試鏡 | OK |
| `gig_1988_ad_08` | 冬 | 廣告 | low | 社會題材廣告沉底 | `era_1988_winter_record` | 0.6 | 周刊透露的諮詢廣告線索 | OK |
| `gig_1988_var_01` | 春 | 綜藝 | high | 賀歲直播緊急招募 | `era_1988_spring_grassroot` | 1.0 | 錄影廠門口的直播緊急招募 | OK |
| `gig_1988_var_02` | 夏 | 綜藝 | high | 夏檔選美外景主推 | `era_1988_summer_variety` | 1.0 | 黃金時段大型節目曝光名額 | OK |
| `gig_1988_var_03` | 夏 | 綜藝 | high | 水上競技綜藝主推 | `era_1988_summer_variety` | 1.0 | 二台高酬勞遊戲通告 | OK |
| `gig_1988_var_04` | 秋 | 綜藝 | normal | 音樂嘉賓非單元主線 | `era_1988_autumn_studio` | 0.6 | 電台透露的音樂特別節目 | OK |
| `gig_1988_var_05` | 冬 | 綜藝 | high | 台慶特技冬主推 | `era_1988_winter_festive` | 1.0 | 監製下達的台慶硬性任務 | OK |
| `gig_1988_tv_01` | 春 | 電視劇 | high | 春檔主推警匪龍套 | `era_1988_spring_grassroot` | 1.0 | 片場人情爭取的龍套開工 | OK |
| `gig_1988_tv_02` | 春 | 電視劇 | high | 武俠片廠替身主推 | `era_1988_spring_factory` | 1.0 | 武師班底拉來的替身通告 | OK |
| `gig_1988_tv_03` | 夏 | 電視劇 | normal | 夏檔劇非綜藝主線 | `era_1988_summer_mall` | 0.6 | 監製指定的上位轉折角色 | OK |
| `gig_1988_tv_04` | 夏 | 電視劇 | normal | 客串劇沉於綜藝後 | `era_1988_summer_mall` | 0.6 | 二台挖角試探的客串角色 | OK |
| `gig_1988_tv_05` | 秋 | 電視劇 | high | 處境喜劇秋主推 | `era_1988_autumn_unitdrama` | 1.0 | 喜劇組發出的茶餐廳選角 | OK |
| `gig_1988_tv_06` | 冬 | 電視劇 | high | 演技男一搶位主推 | `era_1988_winter_recruit` | 1.0 | 衝擊大獎的深度男一劇本 | OK |
| `gig_1988_tv_07` | 冬 | 電視劇 | high | 台慶壓軸劇主推 | `era_1988_winter_festive` | 1.0 | 台慶月壓軸臨時代替試鏡 | OK |
| `gig_1988_film_01` | 春 | 電影 | high | 動作片廠危險替身 | `era_1988_spring_factory` | 1.0 | 發小介紹的高薪特技替身 | OK |
| `gig_1988_film_02` | 夏 | 電影 | low | 黑幫片非夏主推 | `era_1988_summer_mall` | 0.6 | 片場看中後給予的刀仔角色 | OK |
| `gig_1988_film_03` | 夏 | 電影 | normal | 暑期動作喜劇次級 | `era_1988_summer_mall` | 0.6 | 影業公開招募的動作喜劇 | OK |
| `gig_1988_film_04` | 秋 | 電影 | high | 文藝磨戲秋主推 | `era_1988_autumn_readthrough` | 1.0 | 導師力薦的演技考驗通告 | OK |
| `gig_1988_film_05` | 冬 | 電影 | normal | 黑道逼拍次於賀歲 | `era_1988_winter_recruit` | 1.0 | 強行送來的開工合約 | OK |
| `gig_1988_film_06` | 冬 | 電影 | high | 賀歲動作男一主推 | `era_1988_winter_festive` | 1.0 | 聯手爭取的頂級電影男一 | OK |
| `gig_1988_rec_01` | 春 | 唱片通告 | normal | 錄音試水非春主線 | `era_1988_spring_alley` | 0.6 | 電台引薦的合唱錄音試音 | OK |
| `gig_1988_rec_02` | 夏 | 唱片通告 | high | MV卡拉OK夏主推 | `era_1988_summer_karaoke` | 1.0 | 玉女歌手指名的情歌MV | OK |
| `gig_1988_rec_03` | 秋 | 唱片通告 | normal | 個人EP錄音棚次級 | `era_1988_autumn_studio` | 0.6 | 唱片公司個人開發合約 | OK |
| `gig_1988_rec_04` | 冬 | 唱片通告 | normal | 紅館嘉賓唱片次級 | `era_1988_winter_record` | 0.6 | 電台與唱片聯合推薦登台 | OK |

## 檔案

- 更新：`/workspace/star-volunteer-web/content/gigs_1988.json`（version 2）
- 備份：`/workspace/star-volunteer-web/content/gigs_1988_pre_annotation_backup.json`
- 本表：`/workspace/star-volunteer-web/content/GIGS_1988_ANNOTATION_v1.md`

---

## v2.1 口吻／專名修訂（2026-11-02）

> 接續標註 v1；**允許最小正文修改**修季節口吻與星河顯示名；pay／id／priority／eraTag 未改。詳見 `GIGS_1988_FIX_v1.md`。

| 項 | 狀態 |
|---|---|
| `gig_1988_var_01` 春草根（去賀歲／龍年） | DONE |
| `gig_1988_var_05` 冬賀歲（去台慶） | DONE |
| `gig_1988_tv_07` 賀歲檔大劇口吻 | DONE |
| `gig_1988_var_02` 夏・星河台慶籌備季 | DONE |
| 顯示名 龍門→星河（index＋worldview；loc id 不變） | DONE |
| high 春4夏4秋2冬4 | 維持 |
| version | 2.1 |
