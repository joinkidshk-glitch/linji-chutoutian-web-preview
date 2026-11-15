#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v20a219 resync：index.html 淨 +3 行（CONTRA98 表加 R_tang_meet_stub 行＋註解 2 行，
# 插入點舊 L31845 之後；其餘改動全部原地換值，行數不變）。difflib 對位核實：
# 舊行 <=31845 行號不變、>=31846 者 +3；本腳本先逐項核實釘行舊新內容逐字相同，
# 再用單次掃描 dict 查表一次過改（教訓：唔好逐對 re.sub，會撞值丟失／重複——
# 例如 travel114 COUNT 39860→39863 撞舊 39863、FREE 56109→56112 撞舊 56112）。
# 用法：python3 qa219/resync219.py [--check]   （--check 只核實，唔寫檔）
# 改動範圍：只改 tests/ 下面 9 檔（contra98_logic.js 另用人手改邏輯期望，唔經本腳本）。
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = '--check' in sys.argv

def load_old():
    out = subprocess.check_output(['git', 'show', '5580f8d:index.html'], cwd=str(ROOT), text=True)
    return out.split('\n')
old = load_old()
new = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print('舊行數 %d（split）／新行數 %d（split）；舊 \\n 數 %d／新 %d'
      % (len(old), len(new), len(old) - 1, len(new) - 1))

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
bad = [(n, m) for n, m in sorted(shift.items())
       if m != (n if n <= 31845 else n + 3)]
assert not bad, '映射唔係 identity／+3：%s' % bad[:10]
print('difflib 映射核實：舊行 -> 新行，<=31845 不變、>=31846 +3；例外 0 項')

def mapline(n):
    return n if n <= 31845 else n + 3

# ---- 2. 逐項核實釘行舊新內容逐字相同 ----
# (檔，舊行，錨子串；新行由 mapline 計)
PINS = {
 'tests/test_rom176_static.py': [
    (6360, 'lan:{ id:"lan"'), (31974, 'GIFT_REACT = giftReact'),
    (31974, 'rom176ApplyGiftOverrides()'), (55780, '/* ===== v20a176 ROM176'),
    (56148, 'function rom176ApplyGiftOverrides()'),
    (57287, 'function addLocTalkGiftActs(add, L, npcId)'),
    (57381, 'rom176TryIntercept(id)')],
 'tests/test_tang152_static.py': [
    (26116, 'const HELD = ["R_tang_push1"'),
    (31899, 'function normaliseTangStub152(pack){'),
    (32045, 'try{ normaliseTangStub152(rom2);')],
 'tests/test_text125_static.py': [
    (28090, '[b.text]'), (28227, '[b.text]'),
    (33963, 'if(typeof b.text === "string" && b.text){')],
 'tests/test_travel114_static.py': [],
 'tests/test_tang171_static.py': [(57350, 'function openLoc(id, opts){')],
 'tests/test_tang173_static.py': [(57350, 'function openLoc(id, opts){')],
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
PINS['tests/test_travel114_static.py'].append((57350, 'function openLoc(id, opts){'))
PINS['tests/test_travel114_static.py'].append((45479, 'openLoc: function(id, opts){ openLoc(id, opts); }'))
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
# contra98_static.py 正則核實：表內條目新 23／舊 22
for label, lines in (('舊', old), ('新', new)):
    src = '\n'.join(lines)
    m = re.search(r'const CONTRA98_WHEN_FIX = \{(.*?)\n\};', src, re.S)
    entries = re.findall(r'\b[A-Za-z_][A-Za-z_0-9]*:\["(?:1989|1990)[秋冬春夏]","era_[^"]+"\]', m.group(1))
    print('CONTRA98 表條目（%s）：%d' % (label, len(entries)))
    assert len(entries) == (22 if label == '舊' else 23), entries
assert 'R_tang_meet_stub:["1989秋","era_1989_autumn_capital"]' in '\n'.join(new)
assert '\n'.join(new).count('"1990冬","era_1990_winter_finale"') == 8
assert '\n'.join(old).count('"1990冬","era_1990_winter_finale"') == 11
print('winter_finale 計數核實：舊 11 → 新 8；stub 行在位')

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

PINMAP = {ln: mapline(ln) for ln in FREE_OLD + COUNT_OLD}  # >=31846 者 +3，之前者 identity
resync_region('tests/test_travel114_static.py', 'FREE_LINES', PINMAP)
resync_region('tests/test_travel114_static.py', 'COUNT_LINES', PINMAP)
replace_once('tests/test_travel114_static.py', [
    ('DEF_LINE = 57350      # function openLoc(id, opts){',
     'DEF_LINE = 57353      # function openLoc(id, opts){'),
    ('WRAPPER_LINE = 45479  # window.__phase2.openLoc：轉發 opts',
     'WRAPPER_LINE = 45482  # window.__phase2.openLoc：轉發 opts'),
    ('# v20a218 resync：index.html 淨 +136 行；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重算，內容逐字核實純漂移（47 個錨點，見 qa218/resync218_pins.py）；COUNT 12／FREE 33 不變，DEF 57230→57350、WRAPPER 45430→45479。',
     '# v20a218 resync：index.html 淨 +136 行；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重算，內容逐字核實純漂移（47 個錨點，見 qa218/resync218_pins.py）；COUNT 12／FREE 33 不變，DEF 57230→57350、WRAPPER 45430→45479。\n# v20a219 resync：index.html 淨 +3 行（CONTRA98 表加 stub 行＋註解 2 行，插入點舊 L31845 之後）；其後錨點各 +3（FREE 25 處／COUNT 12 處／DEF 57350→57353／WRAPPER 45479→45482；＜31846 者唔郁），difflib 對位核實純漂移，見 qa219/resync219.py。'),
])

replace_once('tests/test_rom176_static.py', [
    ("'GIFT_REACT = giftReact' in line(31974) and 'rom176ApplyGiftOverrides()' in line(31974))",
     "'GIFT_REACT = giftReact' in line(31977) and 'rom176ApplyGiftOverrides()' in line(31977))"),
    ("line(55780).startswith('/* ===== v20a176 ROM176')",
     "line(55783).startswith('/* ===== v20a176 ROM176')"),
    ("line(56148).startswith('function rom176ApplyGiftOverrides()')",
     "line(56151).startswith('function rom176ApplyGiftOverrides()')"),
    ("line(57287).startswith('function addLocTalkGiftActs(add, L, npcId)')",
     "line(57290).startswith('function addLocTalkGiftActs(add, L, npcId)')"),
    ("'rom176TryIntercept(id)' in line(57381))",
     "'rom176TryIntercept(id)' in line(57384))"),
    ('# v20a218 resync：index.html 淨 +136 行，釘行按 difflib 映射重寫（31941→31974、55660→55780、56028→56148、57167→57287、57261→57381；6360 唔郁），見 qa218/resync218_pins.py。',
     '# v20a218 resync：index.html 淨 +136 行，釘行按 difflib 映射重寫（31941→31974、55660→55780、56028→56148、57167→57287、57261→57381；6360 唔郁），見 qa218/resync218_pins.py。\n# v20a219 resync：index.html 淨 +3 行（CONTRA98 stub，插入點舊 L31845 之後）；釘行各 +3（31974→31977、55780→55783、56148→56151、57287→57290、57381→57384；6360 唔郁），difflib 對位核實純漂移，見 qa219/resync219.py。'),
])

replace_once('tests/test_tang152_static.py', [
    ("ok('刪節點：CONTRA98 winter_finale 由 12 減到 11', src.count('\"1990冬\",\"era_1990_winter_finale\"') == 11)",
     "ok('刪節點：CONTRA98 winter_finale 由 11 減到 8（v20a219：hiu／choi／xu 結局改秋）', src.count('\"1990冬\",\"era_1990_winter_finale\"') == 8)"),
    ("lines()[31898].startswith('function normaliseTangStub152(pack){')",
     "lines()[31901].startswith('function normaliseTangStub152(pack){')"),
    ("lines()[32044].strip().startswith('try{ normaliseTangStub152(rom2);')",
     "lines()[32047].strip().startswith('try{ normaliseTangStub152(rom2);')"),
    ('# v20a196 resync：showResult 淨 −1 行，兩錨點各 −1（31510→31509、31654→31653），difflib 對位核實內容逐字相同，純漂移。',
     '# v20a196 resync：showResult 淨 −1 行，兩錨點各 −1（31510→31509、31654→31653），difflib 對位核實內容逐字相同，純漂移。\n# v20a219 resync：index.html 淨 +3 行（CONTRA98 stub，插入點舊 L31845 之後）；winter_finale 11→8（hiu／choi／xu 結局改秋）；normaliseTangStub152 31899→31902、stub 呼叫行 32045→32048（difflib 對位核實純漂移，見 qa219/resync219.py）。'),
])

replace_once('tests/test_text125_static.py', [
    ('    if len(ls) < 33689 or \'if(typeof b.text === "string" && b.text){\' not in ls[33962]:',
     '    if len(ls) < 33692 or \'if(typeof b.text === "string" && b.text){\' not in ls[33965]:'),
    ('        probs.append("applyFamilySafeToNode 第 33963 行冇 b.text 分支")  # v196 落地合併上 main 2de5026：v197 33672→33671（showResult 淨 −1）；v20a218 resync：33930→33963',
     '        probs.append("applyFamilySafeToNode 第 33966 行冇 b.text 分支")  # v196 落地合併上 main 2de5026：v197 33672→33671（showResult 淨 −1）；v20a218 resync：33930→33963；v20a219 resync：33963→33966'),
    ('    # v20a218 resync：淨 +136 行，currentLine 28082→28090、advance 28211→28227、applyFamilySafe 33930→33963（difflib 對位核實純漂移，見 qa218/resync218.py）。',
     '    # v20a218 resync：淨 +136 行，currentLine 28082→28090、advance 28211→28227、applyFamilySafe 33930→33963（difflib 對位核實純漂移，見 qa218/resync218.py）。\n    # v20a219 resync：淨 +3 行（CONTRA98 stub，插入點舊 L31845 之後），applyFamilySafe 33963→33966；currentLine／advance 喺插入點之前唔郁（difflib 對位核實純漂移，見 qa219/resync219.py）。'),
])

for fname in ('tests/test_gift185_static.py', 'tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    txt = (ROOT / fname).read_text(encoding='utf-8')
    assert txt.count('62894') >= 1
replace_once('tests/test_gift185_static.py', [
    ('總行數 62894（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136）',
     '總行數 62897（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3）'),
    ("html.count('\\n') == 62894", "html.count('\\n') == 62897"),
    ('# v20a218 resync：index.html 淨 +136 行（見 qa218/resync218.py difflib 對位核實純漂移），總行數 62758→62894。',
     '# v20a218 resync：index.html 淨 +136 行（見 qa218/resync218.py difflib 對位核實純漂移），總行數 62758→62894。\n# v20a219 resync：index.html 淨 +3 行（CONTRA98 stub，插入點舊 L31845 之後），總行數 62894→62897（difflib 對位核實純漂移，見 qa219/resync219.py）。'),
])
for fname in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    replace_once(fname, [
        ('總行數 62894（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136）',
         '總行數 62897（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3）'),
        ("src.count('\\n') == 62894", "src.count('\\n') == 62897"),
        ('openLoc DEF 行 57350（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +120，travel114 釘行）',
         'openLoc DEF 行 57353（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +120＋v219 +3，travel114 釘行）'),
        ("len(lines) >= 57350 and 'function openLoc(id, opts){' in lines[57349])",
         "len(lines) >= 57353 and 'function openLoc(id, opts){' in lines[57352])"),
        ('# v20a218 resync：index.html 淨 +136 行（見 qa218/resync218.py difflib 對位核實純漂移），總行數 62758→62894、DEF 57230→57350。',
         '# v20a218 resync：index.html 淨 +136 行（見 qa218/resync218.py difflib 對位核實純漂移），總行數 62758→62894、DEF 57230→57350。\n# v20a219 resync：index.html 淨 +3 行（CONTRA98 stub，插入點舊 L31845 之後），總行數 62894→62897、DEF 57350→57353（difflib 對位核實純漂移，見 qa219/resync219.py）。'),
    ])

replace_once('tests/test_contra98_static.py', [
    ('import sys\nfrom pathlib import Path',
     'import re\nimport sys\nfrom pathlib import Path'),
    ("ok('A-01/02: CONTRA98_WHEN_FIX 表在位（22 節點；v20a152 刪 R_tang_ending）', src.count('\"1990冬\",\"era_1990_winter_finale\"') >= 11 and 'era_1990_autumn_capital' in src)",
     "# v20a219：表加 R_tang_meet_stub 衞生行（22→23）；hiu／choi／xu 結局由冬改秋，winter_finale 11→8。\n_m98 = re.search(r'const CONTRA98_WHEN_FIX = \\{(.*?)\\n\\};', src, re.S)\n_fix98 = re.findall(r'\\b[A-Za-z_][A-Za-z_0-9]*:\\[\"(?:1989|1990)[秋冬春夏]\",\"era_[^\"]+\"\\]', _m98.group(1)) if _m98 else []\nok('A-01/02: CONTRA98_WHEN_FIX 表在位（23 節點；v20a219 加 R_tang_meet_stub）',\n   len(_fix98) == 23 and 'R_tang_meet_stub:[\"1989秋\",\"era_1989_autumn_capital\"]' in src\n   and src.count('\"1990冬\",\"era_1990_winter_finale\"') == 8)"),
])

print('全部寫檔完成')
