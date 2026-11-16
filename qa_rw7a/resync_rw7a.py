#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# RW-7A resync：index.html 淨 −69 行（刪 TEXTFIX 死映射＋gig 清洗層；
# 刪除區間舊 L14372–14379／14399／14402／14410／14558–14615／15884–15885，
# 另有行內換值 L14371／14381／14389／14390／14395／14413／14659–14660／29011）。
# difflib 對位核實後，單次掃描 dict 查表一次過改（教訓：唔好逐對 re.sub，會撞值丟失／重複）。
# 用法：python3 qa_rw7a/resync_rw7a.py [--check]   （--check 只核實，唔寫檔）
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = '--check' in sys.argv
BASE = '076382f'

def load_old():
    out = subprocess.check_output(['git', 'show', BASE + ':index.html'], cwd=str(ROOT), text=True)
    return out.split('\n')

old = load_old()
new = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print('舊行數 %d（split）／新行數 %d（split）；淨 %d' % (len(old), len(new), len(new) - len(old)))
assert len(new) - len(old) == -69, '淨行數唔係 -69'

# ---- 1. difflib 映射 ----
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
shift = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            shift[i1 + k + 1] = j1 + k + 1
    elif tag == 'replace':
        for k in range(min(i2 - i1, j2 - j1)):
            shift[i1 + k + 1] = j1 + k + 1
    elif tag in ('delete', 'insert'):
        pass
    else:
        raise SystemExit('未知 opcode：%s' % tag)

# ---- 2. 逐項核實釘行 ----
# (檔, 舊行, 模式, 錨)；exact＝舊新行逐字相同；contains＝新行含指定子串（行內刪條目嘅例外）
PINS = {
    'tests/test_kwan151_static.py': [
        (9052, 'exact', None), (9393, 'exact', None), (9396, 'exact', None),
        (9397, 'exact', None), (9398, 'exact', None), (9441, 'exact', None),
        (9660, 'exact', None), (10661, 'exact', None), (10694, 'exact', None),
        (14380, 'exact', None),
        (14389, 'contains', (['采兒同關海媚嗰邊都近咗啲', '但采兒同關海媚嗰邊，都冷淡咗'], ['嗰位當紅花旦'])),
        (14390, 'contains', (['["星河電視城", "星河電視台"]', '["送命題", "辣手問題"]'], [])),
        (14428, 'exact', None),
    ],
    'tests/test_rom176_static.py': [
        (6360, 'exact', None), (14843, 'exact', None), (38274, 'exact', None),
        (38647, 'exact', None), (39785, 'exact', None), (39885, 'exact', None),
    ],
    # tang152：lines()[N] 0-based 索引（名入面嘅 L31610／L31754 係歷史標籤，唔郁）
    'tests/test_tang152_static.py': [
        (9212, 'exact', None), (14772, 'exact', None), (14894, 'exact', None),
    ],
    # text125：ls[N] 0-based 索引
    'tests/test_text125_static.py': [
        (11186, 'exact', None), (11323, 'exact', None), (16490, 'exact', None),
    ],
}
# travel114：COUNT／FREE／DEF／WRAPPER 全部釘行（由測試檔讀出嚟，唔用人手抄）
t114 = (ROOT / 'tests/test_travel114_static.py').read_text(encoding='utf-8')

def _setnums(name):
    m = re.search(name + r' = \{(.*?)\n\}', t114, re.S)
    return [int(x) for x in re.findall(r'^\s*(\d+),', m.group(1), re.M)]

PINS['tests/test_travel114_static.py'] = []
for ln in _setnums('COUNT_LINES') + _setnums('FREE_LINES'):
    PINS['tests/test_travel114_static.py'].append((ln, 'exact', None))
for ln in (39854, 27864):
    PINS['tests/test_travel114_static.py'].append((ln, 'exact', None))

# 預期映射（刪區算術 cross-check；difflib 係準，但數字唔啱即停手查）
EXPECTED_CHANGED = {
    'tests/test_kwan151_static.py': {14380: 14372, 14389: 14381, 14390: 14382, 14428: 14417},
    'tests/test_rom176_static.py': {14843: 14775, 38274: 38205, 38647: 38578, 39785: 39716, 39885: 39816},
    'tests/test_tang152_static.py': {14772: 14704, 14894: 14826},
    'tests/test_text125_static.py': {16490: 16421},
    'tests/test_travel114_static.py': {
        15423: 15355, 18649: 18580, 20809: 20740, 22015: 21946, 22450: 22381,
        22453: 22384, 22484: 22415, 27295: 27226, 42964: 42895, 43176: 43107,
        43324: 43255, 43345: 43276, 24378: 24309, 26942: 26873, 26975: 26906,
        38074: 38005, 38193: 38124, 38266: 38197, 38489: 38420, 38533: 38464,
        38539: 38470, 38606: 38537, 38608: 38539, 38611: 38542, 38638: 38569,
        39748: 39679, 39795: 39726, 40128: 40059, 40150: 40081, 40302: 40233,
        40307: 40238, 41208: 41139, 42697: 42628, 42841: 42772, 42842: 42773,
        42886: 42817, 42887: 42818, 42912: 42843, 43795: 43726,
        39854: 39785, 27864: 27795},
}

mapping = {}  # 檔 -> {舊行: 新行}
n_checked = 0
for fname, pins in PINS.items():
    mapping[fname] = {}
    for old_n, mode, anchors in pins:
        assert old_n in shift, '%s 舊行 %d 無 difflib 對應（落咗刪除區？）' % (fname, old_n)
        new_n = shift[old_n]
        mapping[fname][old_n] = new_n
        oline, nline = old[old_n - 1], new[new_n - 1]
        if mode == 'exact':
            assert oline == nline, '%s %d→%d 內容唔同：\n舊：%s\n新：%s' % (fname, old_n, new_n, oline[:120], nline[:120])
        else:
            keep, gone = anchors
            for k in keep:
                assert k in nline, '%s %d→%d 保留句唔見：%s' % (fname, old_n, new_n, k)
            for k in gone:
                assert k not in nline, '%s %d→%d 應刪句仲喺度：%s' % (fname, old_n, new_n, k)
        n_checked += 1
print('difflib 映射核實：%d 處釘行全部對上（exact／contains），純漂移＋2 處行內刪條目' % n_checked)
for fname, m in mapping.items():
    print(fname, '：', ', '.join('%d→%d' % (a, b) for a, b in sorted(m.items()) if a != b), '（唔郁：%s）'
          % ', '.join(str(a) for a, b in sorted(m.items()) if a == b))
for fname, exp in EXPECTED_CHANGED.items():
    got = {a: b for a, b in mapping[fname].items() if a != b}
    assert got == exp, '%s 映射同預期唔啱：%s' % (fname, {k: (exp.get(k), got.get(k)) for k in set(exp) | set(got) if exp.get(k) != got.get(k)})
for old_n, new_n in mapping['tests/test_travel114_static.py'].items():
    assert 'openLoc' in new[new_n - 1], 'travel114 %d→%d 新行唔含 openLoc' % (old_n, new_n)
print('預期映射 cross-check 通過；travel114 47 處新行全部含 openLoc')

if CHECK:
    print('--check 模式：只核實，唔寫檔')
    sys.exit(0)

# ---- 3. 單次掃描 dict 查表一次過改 ----
# kwan151 / rom176：只改 line(N) 呼叫點（check 名入面嘅舊 L 號係歷史標籤，唔郁；歷史 resync 註解唔郁）
for fname in ('tests/test_kwan151_static.py', 'tests/test_rom176_static.py'):
    p = ROOT / fname
    txt = p.read_text(encoding='utf-8')
    m = mapping[fname]
    n_rep = [0]

    def _repl(mm, m=m, n_rep=n_rep):
        n = int(mm.group(1))
        assert n in m, '%s line(%d) 唔喺映射表' % (fname, n)
        n_rep[0] += 1
        return 'line(%d)' % m[n]

    txt2 = re.sub(r'line\((\d+)\)', _repl, txt)
    print('%s：改咗 %d 處 line() 呼叫' % (fname, n_rep[0]))
    p.write_text(txt2, encoding='utf-8')

# tang152：lines()[N] 0-based 索引（名入面嘅 L31610／L31754 係歷史標籤，唔郁）
for fname, pat in (('tests/test_tang152_static.py', r'lines\(\)\[(\d+)\]'),
                   ('tests/test_text125_static.py', r'ls\[(\d+)\]')):
    p = ROOT / fname
    txt = p.read_text(encoding='utf-8')
    m = mapping[fname]
    n_rep = [0]

    def _repl2(mm, m=m, n_rep=n_rep, fname=fname):
        n = int(mm.group(1)) + 1  # 0-based index -> 1-based line
        assert n in m, '%s index %d 唔喺映射表' % (fname, n)
        n_rep[0] += 1
        return mm.group(0).split('[')[0] + '[' + str(m[n] - 1) + ']'

    txt2 = re.sub(pat, _repl2, txt)
    print('%s：改咗 %d 處索引' % (fname, n_rep[0]))
    p.write_text(txt2, encoding='utf-8')

# text125：報錯字串入面嘅行號＋行尾 resync 註解一併更新
p = ROOT / 'tests/test_text125_static.py'
txt = p.read_text(encoding='utf-8')
assert txt.count('applyFamilySafeToNode 第 16489 行冇 b.text 分支') == 1
txt = txt.replace('applyFamilySafeToNode 第 16489 行冇 b.text 分支', 'applyFamilySafeToNode 第 16420 行冇 b.text 分支')
assert '；RW-7A resync' not in txt
assert txt.count('v20a242 resync：16644→16500（刪 LAN 覆寫表，−144）。') == 1, 'text125 註解錨點唔見咗'
txt = txt.replace('v20a242 resync：16644→16500（刪 LAN 覆寫表，−144）。',
                  'v20a242 resync：16644→16500（刪 LAN 覆寫表，−144）。；RW-7A resync：16489→16420（淨 −69，見 qa_rw7a/resync_rw7a.py）。')
p.write_text(txt, encoding='utf-8')
print('test_text125_static.py：報錯字串＋註解已更新')

# travel114：COUNT／FREE 集合成員＋DEF／WRAPPER，逐行單次掃描
p = ROOT / 'tests/test_travel114_static.py'
lines = p.read_text(encoding='utf-8').split('\n')
m = mapping['tests/test_travel114_static.py']
in_block = None
n_rep = 0
for i, l in enumerate(lines):
    if l.startswith('COUNT_LINES = {'):
        in_block = 'count'
        continue
    if l.startswith('FREE_LINES = {'):
        in_block = 'free'
        continue
    if in_block and l == '}':
        in_block = None
        continue
    if in_block:
        mm = re.match(r'^(\s*)(\d+),', l)
        if mm:
            n = int(mm.group(2))
            assert n in m, 'travel114 集合 %d 唔喺映射表' % n
            lines[i] = mm.group(1) + str(m[n]) + ',' + l[mm.end():]
            n_rep += 1
        continue
    mm = re.match(r'^(DEF_LINE = )(\d+)(.*)$', l)
    if mm:
        n = int(mm.group(2))
        assert n in m, 'DEF_LINE %d 唔喺映射表' % n
        lines[i] = mm.group(1) + str(m[n]) + mm.group(3)
        n_rep += 1
        continue
    mm = re.match(r'^(WRAPPER_LINE = )(\d+)(.*)$', l)
    if mm:
        n = int(mm.group(2))
        assert n in m, 'WRAPPER_LINE %d 唔喺映射表' % n
        lines[i] = mm.group(1) + str(m[n]) + mm.group(3)
        n_rep += 1
print('test_travel114_static.py：改咗 %d 處（COUNT 12＋FREE 35＋DEF／WRAPPER 2）' % n_rep)
assert n_rep == 49, 'travel114 改動數唔係 49'
p.write_text('\n'.join(lines), encoding='utf-8')

# ---- 4. 各加一行新 resync 註解（檔頭，最新喺頂） ----
COMMENTS = {
    'tests/test_kwan151_static.py':
        '# RW-7A resync：index.html 淨 −69 行（刪 TEXTFIX 死映射＋gig 清洗層；刪除區間舊 L14372–14379／14399／14402／14410／14558–14615／15884–15885）；13 個釘行按 difflib 映射重寫（14380→14372、14389→14381、14390→14382、14428→14417；＜14371 者唔郁），內容逐行核實（14389／14390 行內刪條目，保留句逐字相同；其餘純漂移）。',
    'tests/test_rom176_static.py':
        '# RW-7A resync：index.html 淨 −69 行（刪 TEXTFIX 死映射＋gig 清洗層）；6 個釘行按 difflib 映射重寫（14843→14775、38274→38205、38647→38578、39785→39716、39885→39816；6360 唔郁），內容逐字核實純漂移。',
    'tests/test_travel114_static.py':
        '# RW-7A resync：index.html 淨 −69 行（刪 TEXTFIX 死映射＋gig 清洗層）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（47 處錨點內容逐行相同，純漂移；openLoc( 呼叫點總數不變；DEF 39854→39785、WRAPPER 27864→27795）。',
    'tests/test_tang152_static.py':
        '# RW-7A resync：index.html 淨 −69 行（刪 TEXTFIX 死映射＋gig 清洗層）；3 個釘行按 difflib 映射重寫（14772→14704、14894→14826；9212 唔郁），內容逐字核實純漂移；另 EXACT #2（腕表句）因 tang152 釘死已還原，唔再刪。',
    'tests/test_text125_static.py':
        '# RW-7A resync：index.html 淨 −69 行（刪 TEXTFIX 死映射＋gig 清洗層）；applyFamilySafeToNode b.text 釘行按 difflib 映射重寫（16490→16421；11186／11323 唔郁），內容逐字核實純漂移。',
}
for fname, comment in COMMENTS.items():
    p = ROOT / fname
    txt = p.read_text(encoding='utf-8')
    assert comment not in txt, fname + ' 已有 RW-7A 頂註解'
    p.write_text(comment + '\n' + txt, encoding='utf-8')
    print(fname + '：已加 RW-7A resync 註解')
print('DONE')
