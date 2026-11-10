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
chk('FAME bands const', 'const CALIB60_FAME_BANDS' in src and '[230,0.10]' in src)
chk('ATTR bands const', 'const CALIB60_ATTR_BANDS' in src and '[190,0.19]' in src)
chk('applyCalib60 defined', 'function applyCalib60(delta)' in src)
chk('calib60BankedGain defined', 'function calib60BankedGain(key, v, cur)' in src)
chk('calib60MissedScan defined', 'function calib60MissedScan(st)' in src)
chk('renderMemoryPane60 defined', 'function renderMemoryPane60()' in src)

# --- (1) 接線：拍攝／訓練／散工 ---
rpd = slice_fn('resolvePlannedDay')
chk('shoot wrap 走 applyGain60', 'applyGain60(daily)' in rpd)
chk('resolvePlannedDay 訓練鏈走 applyGain60（9 課）', rpd.count('applyGain60({') >= 9)
atl = slice_fn('applyTrainLesson')
chk('applyTrainLesson 訓練鏈走 applyGain60（9 課）', atl.count('applyGain60({') >= 9)
chk('直接 fame 寫入走 calib60FameGain（3 處）', src.count('calib60FameGain(sv)') == 3)
chk('fallback alias 在位（抽函數沙盒相容）', src.count('const applyGain60 = (typeof applyCalib60') == 2)
# 抉擇路徑刻意唔縮：applyChoice 唔准出現 applyCalib60
chk('applyChoice 唔經校準（抉擇獎勵原額）', 'applyCalib60' not in slice_fn('applyChoice'))

# --- (2) 經濟 ---
lcb = slice_fn('livingCostBand')
chk('livingCostBand 有 CALIB60-2 年份/名氣加幅', 'CALIB60-2' in lcb and 'yr>=1989' in lcb and 'f>=250' in lcb)
chk('livingCostBand base 帶（v20a65 FIX65-2 首年緩坡 1100/1300/1500/1700＋full 2400）', all(x in lcb for x in ['mid:1100', 'mid:1300', 'mid:1500', 'mid:1700', 'mid:2400']))
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
chk('漏失窗表齊 12 節點', all(re.search(r'\b%s:\s*\{' % n, _nw) for n in ['C6','C7','C8','C9','C10','C11','C12','C13','C14','C15','C16','C17']))

# --- (4) 聲樂 ---
dwp = slice_fn('defaultWeekPlan')
chk('defaultWeekPlan 輪入 train_vocal', 'plan[1] = "train_vocal"' in dwp)
bj = slice_fn('bestTrainJumpForGig')
chk('bestTrainJumpForGig frozenVocal', 'frozenVocal' in bj and 'train_vocal' in bj)
ocd = slice_fn('openCastingNoticeDetail')
chk('詳情頁聲樂凍結提示行', 'cn-train-jump-frozen60' in ocd and '從未練過歌藝' in ocd)
chk('凍結提示 CSS 在位', '.cn-train-jump-frozen60' in src)

# --- (5) tutorialFx ---
chk('tutorialFxFingerErr 發布去 window', 'window.tutorialFxFingerErr = tutorialFxFingerErr' in src)
chk('tutorial fx img 仍用具名 handler', 'onerror="tutorialFxFingerErr(this)"' in src)

# --- 硬規則 ---
chk('SAVE key 冇郁', 'starVolunteer_map_v19w' in src)

print('\nFAILURES: %d' % len(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
