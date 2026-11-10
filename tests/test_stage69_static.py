# -*- coding: utf-8 -*-
# v20a69 STAGE69 靜態測試：台風訓練接線（電視台附帶／自動開放／指南鏡像／捷徑去別名）。
# 反證：喺 v20a68 index 上行會 FAIL（tv 附帶冇 train_stage、冇 stage 解鎖規則、捷徑仍別名去 train_acting）。
# 用法：python3 tests/test_stage69_static.py [path-to-index.html]
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- (1) 附帶駐點 ---
ok('COURSE_ENROLL_EXTRA.tv 補入 train_stage', 'tv: ["train_charm", "train_stage"]' in src)
ok('既有附帶冇被郁（film／iq／stamina、music／ad／charm）',
   'film: ["train_iq", "train_stamina"]' in src and 'music: ["train_charm"]' in src and 'ad: ["train_charm"]' in src)
ok('TRAIN_BY_TYPE 主課冇被郁（tv/film 演技、music 歌藝、ad 外貌）',
   'tv:    { courseId:"train_acting"' in src and 'film:  { courseId:"train_acting"' in src
   and 'music: { courseId:"train_vocal"' in src and 'ad:    { courseId:"train_looks"' in src)

# --- (2) 解鎖規則＋指南鏡像 ---
ok('maybeUnlockMidCourses 補台風自動開放（累計 2 堂）', 'if(total>=2 && !en.train_stage)' in src
   and 'enrollCourse("train_stage", notes, "unlock")' in src)
ok('ux68UnlockRule 鏡像補 train_stage 個案', 'case "train_stage":' in src)
# v20a75 改版：進階台風併入台風級別（3 堂開進階規則廢止）——改驗 mid 解鎖
# 規則已清走（只剩存檔遷移參照）＋升級門檻 5 堂喺 levels75Level。
ok('v75：進階台風獨立解鎖已廢止（併入級別）', 'en.train_stage_mid' not in src and 'LEVELS75_STEP = 5' in src)

# --- (3) 通告捷徑去別名 ---
ok('preferredLocForTrainTarget 唔再將 train_stage 別名去 train_acting',
   'courseId==="train_stage"?"train_acting"' not in src)
ok('train_stage 有獨立捷徑分支（指去電視台）', 'if(courseId==="train_stage")' in src)

# --- (4) 增益／堂數本體冇被郁（接線包唔改數值） ---
# v20a75 改版：增益改存 TRAIN75_SPEC（一級 stage +4~6／壓力 +8~12＝舊字面量原值），
# 兩條路徑共用 train75ApplyLesson——改驗數據表台風行＋共用核心。
ok('v75：台風一級增益（數據表）+4~6／壓力 +8~12＋兩路徑共用核心',
   'main:"stage"' in src and 'sub:"charm",  sLo:8, sSpan:4' in src and src.count('train75ApplyLesson(') >= 3)

print('\nFAILURES: %d' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
