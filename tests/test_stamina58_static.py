# v20a58 擴展 static tests: 新課程「武師班」九處接線齊全、數值同同級課程對齊、
# 週結三處 stamina 暗加已收、相關文案唔再承諾瞓覺回體能、硬規則（SAVE key）冇郁。
# 反證: run against the rest-only (pre-extension) index -> 課程不存在＋暗加仍在 -> FAIL.
import sys

src = open(sys.argv[1] if len(sys.argv) > 1 else 'index.html', encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# --- 新課程接線（9 處） ---
chk('COURSE_DEFS: train_stamina 武師班', 'train_stamina: { icon:"🥋", name:"武師班", hint:"拳腳／體能", midOf:null }' in src)
chk('COURSE_ENROLL_EXTRA: film 附帶武師班', 'film: ["train_iq", "train_stamina"]' in src)
chk('EVENTS: TRAIN_RESULT_stamina 有句', '"TRAIN_RESULT_stamina":[' in src)
chk('EVENTS: UNLOCK_STAMINA 有句', '"UNLOCK_STAMINA":[' in src)
chk('courseForStatKey: stamina → train_stamina', 'stamina:"train_stamina", fame:null' in src)
chk('preferredLocForTrainTarget: train_stamina 分支（電影地點）', 'if(courseId==="train_stamina")' in src and '"film_lion"' in src)
chk('maybeUnlockMidCourses: 累計 3 堂開放', 'if(total>=3 && !en.train_stamina)' in src)
chk('stressDeltaForAct: train_stamina = 10', 'train_stamina:10' in src)
# v20a75 改版：公式改存 TRAIN75_SPEC（一級 +4~6／+8~12 原值），兩條路徑共用
# train75ApplyLesson 結算，唔再各一份字面量——改驗數據表＋共用核心。
chk('v75 武師班一級公式（數據表）+4~6 體能／+8~12 壓力', 'train_stamina:' in src and 'main:"stamina", mLo:4, mSpan:2' in src and 'sLo:8, sSpan:4' in src)
chk('v75 兩路徑共用 train75ApplyLesson 結算', src.count('train75ApplyLesson(') >= 3)
chk('結算有 TRAIN_RESULT 句（v75 共用核心動態拼 TRAIN_RESULT_<課>，兩路徑共用）', 'eventLine("TRAIN_RESULT_" +' in src and 'function train75ApplyLesson' in src)

# --- 週結暗加已收（三分支） ---
chk('低體能分支：刪 stamina +5（fame/stress 保留）', 'apply({fame:-2, stress:5})' in src and 'stamina:5, stress:5' not in src)
chk('週末分支：刪 stamina +8（stress −6 保留）', 'pushFlavor(apply({stress:-6}))' in src and 'apply({stamina:8, stress:-6})' not in src)
chk('高壓分支：刪 stamina +4', 'pushFlavor(apply({stamina:4}))' not in src)

# --- 文案唔再承諾瞓覺回體能 ---
chk('WEEKEND_SOFT 舊句已清（體能慢慢回來）', '體能慢慢回來' not in src and '先把體能養回來' not in src)
chk('WEEKEND_SOFT 新句（養精神）', '先把精神養回來' in src)
chk('WEEKEND_SOFT fallback 已改（壓力稍降）', '週末休息，壓力稍降。' in src and '週末休息，體能回升。' not in src)
chk('WEEK_LOW_STA 已刪「瞓夠回體能」暗示', '開工前先睡夠' not in src)
chk('低體能警告句保留（提示性質唔係回復承諾）', '體能見底，宜減輕通告。' in src)

# --- 硬規則 ---
chk('SAVE key unchanged', 'starVolunteer_map_v19w' in src)

if fails:
    print('FAILURES:', ' | '.join(fails))
    sys.exit(1)
print('ALL PASS')
