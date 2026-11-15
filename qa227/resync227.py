#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v20a227 resync：index.html 淨 +2 行（WF4 day24 banner 裁切位：註解 1 行→3 行，
# 插入點舊 L41729；chain 原地換值行數不變）。difflib 對位核實：
# 舊行 <=41729 行號不變（舊 L41729 係被換走嘅註解行，對應新行 41729，即新 3 行
# 註解嘅第一行）、>=41730 者 +2；本腳本先逐項核實釘行舊新內容逐字相同，
# 再用單次掃描 dict 查表一次過改（教訓：唔好逐對 re.sub，會撞值丟失／重複——
# 例如 travel114 FREE 56284→56286 撞舊 56286、56286→56288 撞新 56286）。
# 用法：python3 qa227/resync227.py [--check]   （--check 只核實，唔寫檔）
# 改動範圍：只改 tests/ 下面 5 檔（test_rom176_static.py、test_travel114_static.py、
# test_gift185_static.py、test_tang171_static.py、test_tang173_static.py）。
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = '--check' in sys.argv

def load_old():
    out = subprocess.check_output(['git', 'show', '7e05a4d:index.html'], cwd=str(ROOT), text=True)
    return out.split('\n')
old = load_old()
new = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print('舊行數 %d（split）／新行數 %d（split）；舊 \\n 數 %d／新 %d'
      % (len(old), len(new), len(old) - 1, len(new) - 1))
assert len(old) - 1 == 63132, '舊總行數唔係 63132'
assert len(new) - 1 == 63134, '新總行數唔係 63134'

# ---- 1. difflib 映射核實 ----
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
shift = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            shift[i1 + k + 1] = j1 + k + 1
    elif tag == 'replace' and (j2 - j1) >= (i2 - i1):
        # 原地換值（等長部分 1:1）＋插入（多出嘅新行，舊行無對應）
        for k in range(i2 - i1):
            shift[i1 + k + 1] = j1 + k + 1
    else:
        raise SystemExit('非預期 opcode：%s 舊 %d-%d 新 %d-%d' % (tag, i1 + 1, i2, j1 + 1, j2))
# 舊 41729 係被換走嘅註解行，對應新 41729（新 3 行註解第一行）；其餘 <=41729 不變、>=41730 +2
bad = [(n, m) for n, m in sorted(shift.items())
       if m != (n if n <= 41729 else n + 2)]
assert not bad, '映射唔係 identity／+2：%s' % bad[:10]
print('difflib 映射核實：舊行 -> 新行，<=41729 不變、>=41730 +2；例外 0 項')
# 改動內容核實：舊註解行＋舊 chain 行被換走，新行有 kowloon 80% 分流
assert 'bg_loc_tvb_kowloon.jpg' not in old[41728], '舊 L41729 唔應有 kowloon'
assert 'bg_loc_tvb_kowloon.jpg' not in old[41730], '舊 L41731 唔應有 kowloon'
assert 'v20a227 C1' in new[41728] and 'bg_loc_tvb_kowloon.jpg' in new[41729], '新註解行冇 v227／kowloon'
assert 'indexOf("bg_loc_tvb_kowloon.jpg")' in new[41732] and 'center 80%' in new[41732], '新 chain 行冇 kowloon 80% 分流'
assert '只限呢四張圖' in new[41730], '新註解行冇「只限呢四張圖」'
print('改動內容核實：舊註解＋舊 chain 已換走；新註解（v20a227 C1）＋新 chain（kowloon 80%）在位')

def mapline(n):
    return n if n <= 41729 else n + 2

# ---- 2. 逐項核實釘行舊新內容逐字相同 ----
# (檔，舊行，錨子串；新行由 mapline 計)
PINS = {
 'tests/test_rom176_static.py': [
    (6360, 'lan:{ id:"lan"'), (31963, 'GIFT_REACT = giftReact'),
    (31963, 'rom176ApplyGiftOverrides()'), (55957, '/* ===== v20a176 ROM176'),
    (56325, 'function rom176ApplyGiftOverrides()'),
    (57464, 'function addLocTalkGiftActs(add, L, npcId)'),
    (57558, 'rom176TryIntercept(id)')],
 'tests/test_travel114_static.py': [],
 'tests/test_tang171_static.py': [(57527, 'function openLoc(id, opts){')],
 'tests/test_tang173_static.py': [(57527, 'function openLoc(id, opts){')],
}
# travel114：FREE／COUNT／DEF／WRAPPER 全部釘行（由測試檔讀出嚟，唔用人手抄）
t114 = (ROOT / 'tests/test_travel114_static.py').read_text(encoding='utf-8')
def _setnums(name):
    m = re.search(name + r' = \{(.*?)\n\}', t114, re.S)
    return [int(x) for x in re.findall(r'^\s*(\d+),', m.group(1), re.M)]
FREE_OLD = _setnums('FREE_LINES'); COUNT_OLD = _setnums('COUNT_LINES')
for ln in FREE_OLD:
    PINS['tests/test_travel114_static.py'].append((ln, 'openLoc('))
for ln in COUNT_OLD:
    PINS['tests/test_travel114_static.py'].append((ln, 'openLoc('))
PINS['tests/test_travel114_static.py'].append((57527, 'function openLoc(id, opts){'))
PINS['tests/test_travel114_static.py'].append((45641, 'openLoc: function(id, opts){ openLoc(id, opts); }'))
FREE_FLAGS = ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')

n_checked = 0
for fname, pins in PINS.items():
    for ln, anchor in pins:
        nl = mapline(ln)
        assert old[ln - 1] == new[nl - 1], \
            '%s 舊 L%d ≠ 新 L%d：\n舊：%s\n新：%s' % (fname, ln, nl, old[ln - 1][:120], new[nl - 1][:120])
        assert anchor in old[ln - 1], '%s 舊 L%d 冇錨 %r：%s' % (fname, ln, anchor, old[ln - 1][:120])
        n_checked += 1
print('釘行逐字核實：%d 項全部舊新內容相同（含 travel114 FREE %d＋COUNT %d＋DEF／WRAPPER）'
      % (n_checked, len(FREE_OLD), len(COUNT_OLD)))
# travel114 額外語義核實：FREE 行舊內容帶旗、COUNT 行舊內容冇旗
for ln in FREE_OLD:
    assert any(f in old[ln - 1] for f in FREE_FLAGS), 'FREE 舊 L%d 唔帶旗：%s' % (ln, old[ln - 1][:100])
for ln in COUNT_OLD:
    assert not any(f in old[ln - 1] for f in FREE_FLAGS), 'COUNT 舊 L%d 帶旗：%s' % (ln, old[ln - 1][:100])
print('travel114 語義核實：FREE %d 行全部帶旗、COUNT %d 行全部冇旗' % (len(FREE_OLD), len(COUNT_OLD)))

if CHECK:
    print('CHECK 模式：核實全部通過，冇寫檔')
    sys.exit(0)

# ---- 3. 單次掃描 dict 查表改寫 ----
def replace_once(path, pairs):
    """pairs：(舊片段，新片段)；每舊片段必須恰好出現 1 次；新片段唔可以等於任何舊片段（防撞值）。"""
    p = ROOT / path
    txt = p.read_text(encoding='utf-8')
    olds = [o for o, _ in pairs]
    news = [n for _, n in pairs]
    assert len(set(news) & set(olds)) == 0, '%s 新舊片段撞值' % path
    for o, _ in pairs:
        assert txt.count(o) == 1, '%s 舊片段出現 %d 次（要恰好 1 次）：%r' % (path, txt.count(o), o[:80])
    for o, n in pairs:
        txt = txt.replace(o, n, 1)
    p.write_text(txt, encoding='utf-8')
    print('改 %s：%d 處' % (path, len(pairs)))

def resync_region(path, start_pat, mapping):
    """只改指定 set literal 區內行首數字，一次 re.sub 掃描＋dict 查表（唔會重掃撞值）。"""
    p = ROOT / path
    txt = p.read_text(encoding='utf-8')
    m = re.search(start_pat + r' = \{(.*?)\n\}', txt, re.S)
    assert m, '搵唔到 %s' % start_pat
    region = m.group(1)
    def repl(mo):
        v = int(mo.group(2))
        return mo.group(1) + str(mapping.get(v, v)) + ','
    new_region, n = re.subn(r'^(\s*)(\d+),', repl, region, flags=re.M)
    assert n == len(re.findall(r'^\s*\d+,', region, re.M))
    txt = txt[:m.start(1)] + new_region + txt[m.end(1):]
    p.write_text(txt, encoding='utf-8')
    changed = sum(1 for v in mapping if v in [int(x) for x in re.findall(r'^\s*(\d+),', region, re.M)])
    print('改 %s %s 區：%d 個數字改動（其餘唔郁）' % (path, start_pat, changed))

PINMAP = {ln: mapline(ln) for ln in FREE_OLD + COUNT_OLD}  # >=41730 者 +2，之前者 identity
resync_region('tests/test_travel114_static.py', 'FREE_LINES', PINMAP)
resync_region('tests/test_travel114_static.py', 'COUNT_LINES', PINMAP)
replace_once('tests/test_travel114_static.py', [
    ('DEF_LINE = 57527      # function openLoc(id, opts){',
     'DEF_LINE = 57529      # function openLoc(id, opts){'),
    ('WRAPPER_LINE = 45641  # window.__phase2.openLoc：轉發 opts',
     'WRAPPER_LINE = 45643  # window.__phase2.openLoc：轉發 opts'),
    ('# v20a225 resync：index.html 淨 +272 行（對手線強化 rebase 上 main 719975f）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重算，內容逐字核實純漂移（47 個錨點，見 qa225/resync225.py）。',
     '# v20a225 resync：index.html 淨 +272 行（對手線強化 rebase 上 main 719975f）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重算，內容逐字核實純漂移（47 個錨點，見 qa225/resync225.py）。\n# v20a227 resync：index.html 淨 +2 行（WF4 day24 banner 裁切位：註解 1 行→3 行，插入點舊 L41729；chain 原地換值行數不變）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重算，內容逐字核實純漂移（47 個錨點，見 qa227/resync227.py）。'),
])

replace_once('tests/test_rom176_static.py', [
    ("line(55957).startswith('/* ===== v20a176 ROM176')",
     "line(55959).startswith('/* ===== v20a176 ROM176')"),
    ("line(56325).startswith('function rom176ApplyGiftOverrides()')",
     "line(56327).startswith('function rom176ApplyGiftOverrides()')"),
    ("line(57464).startswith('function addLocTalkGiftActs(add, L, npcId)')",
     "line(57466).startswith('function addLocTalkGiftActs(add, L, npcId)')"),
    ("'rom176TryIntercept(id)' in line(57558))",
     "'rom176TryIntercept(id)' in line(57560))"),
    ('# v20a219 resync：index.html 淨 +3 行（CONTRA98 stub，插入點舊 L31845 之後）；釘行各 +3（31974→31977、55780→55783、56148→56151、57287→57290、57381→57384；6360 唔郁），difflib 對位核實純漂移，見 qa219/resync219.py。',
     '# v20a219 resync：index.html 淨 +3 行（CONTRA98 stub，插入點舊 L31845 之後）；釘行各 +3（31974→31977、55780→55783、56148→56151、57287→57290、57381→57384；6360 唔郁），difflib 對位核實純漂移，見 qa219/resync219.py。\n# v20a227 resync：index.html 淨 +2 行（WF4 day24 banner 裁切位：註解 1 行→3 行，插入點舊 L41729；chain 原地換值行數不變）；釘行各 +2（55957→55959、56325→56327、57464→57466、57558→57560；6360／31963 唔郁），difflib 對位核實純漂移，見 qa227/resync227.py。'),
])

replace_once('tests/test_gift185_static.py', [
    ('總行數 62860（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272）',
     '總行數 63134（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2）'),
    ("html.count('\\n') == 63132", "html.count('\\n') == 63134"),
    ('# v20a225 resync：index.html 淨 +272 行（對手線強化 rebase 上 main 719975f；difflib 對位核實純漂移，見 qa225/resync225.py），總行數 62860→63132。',
     '# v20a225 resync：index.html 淨 +272 行（對手線強化 rebase 上 main 719975f；difflib 對位核實純漂移，見 qa225/resync225.py），總行數 62860→63132。\n# v20a227 resync：index.html 淨 +2 行（WF4 day24 banner 裁切位：註解 1 行→3 行，插入點舊 L41729；chain 原地換值行數不變），總行數 63132→63134（difflib 對位核實純漂移，見 qa227/resync227.py）。'),
])

for fname in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    replace_once(fname, [
        ('總行數 62860（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272）',
         '總行數 63134（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2）'),
        ("src.count('\\n') == 63132", "src.count('\\n') == 63134"),
        ('openLoc DEF 行 57527（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +120＋v219 +3＋v222 −37＋v225 +211，travel114 釘行）',
         'openLoc DEF 行 57529（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +120＋v219 +3＋v222 −37＋v225 +211＋v227 +2，travel114 釘行）'),
        ("len(lines) >= 57527 and 'function openLoc(id, opts){' in lines[57526])",
         "len(lines) >= 57529 and 'function openLoc(id, opts){' in lines[57528])"),
        ('# v20a225 resync：index.html 淨 +272 行（對手線強化 rebase 上 main 719975f；difflib 對位核實純漂移，見 qa225/resync225.py），總行數 62860→63132、DEF 57316→57527。',
         '# v20a225 resync：index.html 淨 +272 行（對手線強化 rebase 上 main 719975f；difflib 對位核實純漂移，見 qa225/resync225.py），總行數 62860→63132、DEF 57316→57527。\n# v20a227 resync：index.html 淨 +2 行（WF4 day24 banner 裁切位：註解 1 行→3 行，插入點舊 L41729；chain 原地換值行數不變），總行數 63132→63134、DEF 57527→57529（difflib 對位核實純漂移，見 qa227/resync227.py）。'),
    ])

print('全部寫檔完成')
