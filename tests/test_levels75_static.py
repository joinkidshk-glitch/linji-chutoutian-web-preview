# v20a75 LEVELS75 static tests：三級制接線齊（數據表／共用核心／遷移掛點／顯示）、
# 進階課獨立存在清走、紅線（SAVE key／softRev／?v=）冇郁。
# 反證：喺 v74 index 上行 → LEVELS75 標記全缺 → FAIL。
import sys

src = open(sys.argv[1] if len(sys.argv) > 1 else 'index.html', encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# --- 數據表＋衍生 ---
chk('LEVELS75 block／數據表在位', 'const TRAIN75_SPEC' in src and 'const LEVELS75_STEP = 5' in src
    and 'const LEVELS75_MAX = 3' in src and 'const LEVELS75_MID_OF' in src)
chk('TRAIN75_SPEC 七課齊', all(('train_%s:' % k) in src for k in
    ['acting', 'stage', 'vocal', 'looks', 'charm', 'iq', 'stamina']))
chk('附帶對照：acting→stage／stage→charm／iq→acting／looks→charm',
    'sub:"stage"' in src and 'sub:"charm"' in src and 'sub:"acting"' in src)
chk('冇附帶三課 sub:null（歌藝／魅力／武師班）', src.count('sub:null') >= 3)
chk('級別衍生函數齊', all(('function %s(' % f) in src for f in
    ['levels75Count', 'levels75Level', 'levels75Next', 'levels75GainRange', 'levels75GainRoll',
     'train75ApplyLesson', 'levels75MigrateSave']))

# --- 共用核心：兩路徑一致 ---
chk('排程路徑行共用核心', 'train75ApplyLesson(id)' in src)
chk('即時路徑行共用核心', 'train75ApplyLesson(courseId)' in src)
chk('核心出 TRAIN_RESULT＋升級提示措辭「升到」', 'eventLine("TRAIN_RESULT_" +' in src and '升到${LEVELS75_NAMES' in src)
chk('maybeUnlockMidCourses 已通用化（冇 mid enroll、開課門檻保留）',
    'enrollCourse("train_acting_mid"' not in src and 'enrollCourse("train_stage_mid"' not in src
    and 'if(total>=2 && !en.train_charm)' in src and 'if(total>=4 && !en.train_iq)' in src
    and 'if(total>=3 && !en.train_stamina)' in src)

# --- 進階課獨立存在清走 ---
chk('COURSE_DEFS 冇進階課行', 'train_acting_mid: { icon' not in src and 'train_stage_mid: { icon' not in src)
chk('玩家面冇「進階演技／進階台風」課名', '進階演技' not in src and '進階台風' not in src)
chk('顯示鏡像 ux68UnlockRule 已刪 mid 個案', 'case "train_acting_mid":' not in src and 'case "train_stage_mid":' not in src)
chk('增益顯示改行數據表衍生', 'levels75GainRange(cid, levels75Level(oo, cid))' in src
    and 'applyTrainLesson.toString()' not in src)

# --- 遷移掛點 ---
i = src.find('function normalizeSaveObj(')
j = src.find('function loadFromSlot(', i)
chk('normalizeSaveObj 載入時行遷移', i >= 0 and j > i and 'levels75MigrateSave(o)' in src[i:j])

# --- 顯示：級別＋進度 ---
chk('picker 卡有級別名＋進度行', 'lvText75' in src and 'prog75' in src and '已到三級' in src and '堂升' in src)
chk('地點上堂掣有級別', 'label += "・" + LEVELS75_NAMES[levels75Level(S, courseId)]' in src)

# --- 紅線 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('softRev 不變', 's107' in src)
chk('產品 ?v= 不變', 'v20a10' in src)

print('\nFAILURES: %d' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
