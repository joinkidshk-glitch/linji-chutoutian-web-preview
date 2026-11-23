# v20a60 全弧校準包 static tests: CALIB60 區塊在位、五部分接線齊（遞減帶／經濟／漏失／聲樂／tutorialFx）、
# 手帳「回憶」頁 UI、硬規則（SAVE key）冇郁。
# 反證: run against a pre-v60 index -> CALIB60 block missing -> FAIL.
import sys, re, os

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(idx_path, encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def slice_fn(name):
    i = src.find('function ' + name + '(')
    if i < 0: return ''
    depth = 0
    j = src.find('{', i)
    for k in range(j, len(src)):
        if src[k] == '{': depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0: return src[i:k+1]
    return ''

# --- 區塊本體 ---
chk('CALIB60 block present', '/* ===== v20a60 CALIB60' in src)
chk('CALIB60-3 block present', 'CALIB60-3' in src)
chk('FAME bands const', 'const CALIB60_FAME_BANDS' in src and '[15,1]' in src and '[200,0.12]' in src)  # v20a370 P3-12：×1.0 帶 <15；v20a373 上段收緊；v20a377 只壓門檻以上（≥200 帶 0.12、頂帶 0.04）
chk('ATTR bands const', 'const CALIB60_ATTR_BANDS' in src and '[160,0.18]' in src)  # v20a373：190+ 帶收緊；v20a377 門檻以下放寬（160 帶 0.18、頂帶 0.05）
chk('applyCalib60 defined', 'function applyCalib60(delta)' in src)
chk('calib60BankedGain defined', 'function calib60BankedGain(key, v, cur)' in src)
chk('calib60MissedScan defined', 'function calib60MissedScan(st)' in src)
chk('renderMemoryPane60 defined', 'function renderMemoryPane60()' in src)

# --- (1) 接線：拍攝／訓練／散工 ---
rpd = slice_fn('resolvePlannedDay')
chk('shoot wrap 走 applyGain60', 'applyGain60(daily)' in rpd)
# v20a75 改版：兩條上堂路徑合併共用核心 train75ApplyLesson（增益按級 roll 後經
# applyGain60），唔再各自內嵌 9 課字面量——原斷言改驗共用核心＋兩路徑都行佢。
t75 = slice_fn('train75ApplyLesson')
chk('v75 共用核心 train75ApplyLesson 走 applyGain60', 'applyGain60(roll)' in t75)
chk('resolvePlannedDay 訓練鏈走共用核心（v75）', 'train75ApplyLesson(id)' in rpd)
atl = slice_fn('applyTrainLesson')
chk('applyTrainLesson 訓練鏈走共用核心（v75）', 'train75ApplyLesson(courseId)' in atl)
chk('直接 fame 寫入走 calib60FameGain（3 處）', src.count('calib60FameGain(sv)') == 3)
chk('fallback alias 在位（抽函數沙盒相容）', src.count('const applyGain60 = (typeof applyCalib60') == 2)
# 抉擇路徑刻意唔縮：applyChoice 唔准出現 applyCalib60
chk('applyChoice 唔經校準（抉擇獎勵原額）', 'applyCalib60' not in slice_fn('applyChoice'))

# --- (2) 經濟 ---
lcb = slice_fn('livingCostBand')
chk('livingCostBand 有 CALIB60-2 年份/名氣加幅', 'CALIB60-2' in lcb and 'yr>=1991' in lcb and 'f>=250' in lcb)
chk('livingCostBand base 帶（v20a65 FIX65-2 首年緩坡 110/130/150/170＋full 240；v261 ÷10；v390 ×1.1 → 120/145/165/185＋full 265）', all(x in lcb for x in ['mid:120', 'mid:145', 'mid:165', 'mid:185', 'mid:265']))
tbp = slice_fn('takeSoftBridgePay')
chk('散工正薪 fame>=200 ×0.75', 'f>=200' in tbp and '0.75' in tbp)
chk('散工補場 $800 字面保留', 'pay:800, stipend:true' in src)

# --- (3) 漏失接線 ---
sw = slice_fn('settleWeek')
chk('settleWeek 週結登記＋提示行', 'calib60MissedScan' in sw and '錯過了' in sw)
nso = slice_fn('normalizeSaveObj')
chk('normalizeSaveObj 舊檔靜靜補登', 'calib60MissedScan(o)' in nso)
chk('手帳回憶 tab 掣', 'data-htab="memory"' in src and 'id="htab-memory"' in src)
chk('手帳回憶 pane', 'id="home-pane-memory"' in src and 'id="memory-list"' in src)
sht = slice_fn('setHomeTab')
chk('setHomeTab allow memory＋render 分支', 'memory:1' in sht and 'renderMemoryPane60()' in sht)
chk('回憶 CSS 在位', '.mem-item60' in src and '.mem-when60' in src)
_nw = src[src.find('const CALIB60_NODE_WINDOWS'):src.find('const CALIB60_NODE_TITLES')]
chk('漏失窗表齊 12 節點', all(re.search(r'\b%s:\s*\{' % n, _nw) for n in ['N6','N7','N9','N10','N11','N8','N14','N16','N13','N12','N15','N17']))

# --- (4) 聲樂 ---
dwp = slice_fn('defaultWeekPlan')
chk('defaultWeekPlan 輪入 train_vocal', '"train_vocal"' in dwp and 'plan[1] = pick360' in dwp)  # v360 P0-3：訓練位輪替保底（最低屬性／最少堂數）取代固定輪入，未報歌藝都排
bj = slice_fn('bestTrainJumpForGig')
chk('bestTrainJumpForGig frozenVocal', 'frozenVocal' in bj and 'train_vocal' in bj)
ocd = slice_fn('openCastingNoticeDetail')
chk('詳情頁聲樂凍結提示行', 'cn-train-jump-frozen60' in ocd and '從未練過歌藝' in ocd)
chk('凍結提示 CSS 在位', '.cn-train-jump-frozen60' in src)

# --- (5) tutorialFx ---
chk('v267 tutorialFxFingerErr 已刪（傳聞教學 fx 一併刪除）', 'tutorialFxFingerErr' not in src)
chk('v267 tutorial fx img 具名 handler 已刪', 'onerror="tutorialFxFingerErr(this)"' not in src)

# --- 硬規則 ---
chk('SAVE key 冇郁', 'starVolunteer_map_v19w' in src)

print('\nFAILURES: %d' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
