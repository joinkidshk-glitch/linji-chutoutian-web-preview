# HANDOFF｜Story UI Beat Schema v1

> 2026-11-03 Asia/Hong_Kong｜用戶拍板劇情界面 → **只鎖字段**；出圖 HOLD；LIVE JSON **唔改**。

1. **鎖咗咩：** beat＝`kind` dialogue|system ＋ `speakerId`／`speaker`／`emotion`／`expression`／`lines`／可選 `bg`|`locId`；system 無半身置中＋環境底；舊稿 `系統`/`旁白` 兼容推導。  
2. **Registry：** 主角+六人+cast_main 19 具名半身位；雜角 generic_crew／剪影；詳見 `PLAN_STORY_UI_BEAT_SCHEMA_v1.md` §B。  
3. **Emotion v1：** neutral/calm/tense/angry/warm/tired/smirk/worried/soft/firm；expression＝default/smile/frown/raise_brow/eyes_down/look_aside。  
4. **環境：** `bg_loc_{11 LOCS}`；C11–C17＋romance／rival **soft loc** 已表列；`setting`≠debug；`artId`＝關鍵卡。  
5. **不變：** Soft≠PASS；出圖 HOLD；鄧 HOLD；meet `playerOffer` 唔改 false。  
6. **下一步：** 下一刀 C1 sandbox 加字段樣本（唔改 LIVE 除非再叫）→ 再 C1–C17 批量 → meet/romance/rival。  
7. **@iOS：** 讀本 plan 做 layout／佔位（半身槽＋system 置中＋環境 tint）；資產未到用 placeholder。  
8. **@tester：** 字段落地後抽樣 E 清單；而家只收 plan PASS 認知即可。

Paths: `content/PLAN_STORY_UI_BEAT_SCHEMA_v1.md` · 本 handoff · 鏡 sv-phone-preview + store。
