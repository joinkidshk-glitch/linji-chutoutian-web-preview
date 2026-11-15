#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v20a229 B4 resync：index.html 淨 +103 行（提名計數改讀 category＋擔正累計式計數器 LEAD229）。
# 用法：python3 qa229/resync229_b4.py [--check]   （--check 只核實，唔寫檔）
# 做法（跟每版慣例，唔好人手估行號）：
#   1. 單段 difflib 對位：B3（e6cc582）→ 現況，逐段核實。
#      全部 delete／replace opcode 嘅舊行必須落喺已知 B4 改動區（界外只准空行）；
#      全部 insert 嘅落點必須喺已知 B4 改動區附近。B4 得 insert＋replace，唔應該有 delete。
#   2. 釘行以測試檔而家嘅 B3 行號起步，經映射推到 B4 行號；
#      全部釘行舊新內容逐字相同＝純漂移先改行號。
# 改動範圍：tests/ 下面 8 檔（kwan151／gift185／rom176／tang152／tang171／tang173／
#   text125／travel114 釘行＋總行數；其餘靜態測試嘅內容失敗唔係 resync，另行處理）。
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = '--check' in sys.argv
BASEB3_REF = 'e6cc582'

def load_ref(ref):
    out = subprocess.check_output(['git', 'show', ref + ':index.html'], cwd=str(ROOT), text=True)
    return out.split('\n')

def build_shift(old, new, allow_delete=False):
    """difflib 對位：舊行號（1-based）→ 新行號；回傳 (shift, opcodes)。
       replace 段按位置對齊較短嗰邊；delete 段（allow_delete 時）唔映射，記入 deletes。"""
    sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    shift = {}
    ops = []
    deletes = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        ops.append((tag, i1, i2, j1, j2))
        if tag == 'equal':
            for k in range(i2 - i1):
                shift[i1 + k + 1] = j1 + k + 1
        elif tag == 'replace':
            for k in range(min(i2 - i1, j2 - j1)):
                shift[i1 + k + 1] = j1 + k + 1
        elif tag == 'delete':
            if not allow_delete:
                raise SystemExit('非預期 delete opcode：舊 L%d-%d' % (i1 + 1, i2))
            deletes.append((i1 + 1, i2))
        elif tag == 'insert':
            pass
    return shift, ops, deletes

old = load_ref(BASEB3_REF)
new = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print('B3 行數 %d（split）／現況 %d；\\n 數 %d／%d'
      % (len(old), len(new), len(old) - 1, len(new) - 1))
assert len(old) - 1 == 47481, 'B3 總行數唔係 47481'
assert len(new) - 1 == 47584, '現況總行數唔係 47584（B4 淨 +103）'

shiftB3, opsB4, deletesB4 = build_shift(old, new)
print('B4 difflib：%d 舊行有對位；opcodes %d 段（delete %d 段）'
      % (len(shiftB3), len(opsB4),
         sum(1 for t, _, _, _, _ in opsB4 if t == 'delete')))

def find_b3(needle, start=1):
    for i in range(start - 1, len(old)):
        if needle in old[i]:
            return i + 1
    raise SystemExit('B3 搵唔到錨：%r' % needle)

# B4 已知改動區（B3 行號計；由錨字串定位，唔用人手抄行號）
A_END95AW = find_b3('function end95Awards(st){')          # LEAD229 區塊插喺佢前面
A_LEADMEDIA = find_b3('const leadMedia95 = ')             # resolveEnding410 擔正讀取區起點
A_LEADMEDIA_END = find_b3('leadMedia: leadMedia95.slice()')  # 快照區終點
A_SDEFAULT = find_b3('careerStats95: null,')               # 存檔預設 leadStats229
A_NORM = find_b3('if(!o.careerStats95 || typeof o.careerStats95')  # normalizeSaveObj 回填區
A_KILL = find_b3('if(_g95 && typeof end95AddWrap')         # 殺青結算呼叫點
A_WRAP = find_b3('S.wrapHistory.unshift({')                # wrapHistory 寫入
A_ENSURE = find_b3('S.wrapHistory.push({')                 # ensureWrapHistoryFromFlags 補記
A_PSR = find_b3('id: "psr_"+gigId')                        # PSR pack 回傳區
A_COUNT = find_b3('function countYearMediumWraps(matchTypes, year){')  # 提名計數函數起點
A_COUNT_END = find_b3('function awardsGigCount(){')        # 提名計數函數終點
KNOWN_B4 = [(A_END95AW - 2, A_END95AW + 1),
            (A_LEADMEDIA, A_LEADMEDIA_END),
            (A_SDEFAULT - 1, A_SDEFAULT + 1),
            (A_NORM, A_NORM + 10),
            (A_KILL - 4, A_KILL + 4),
            (A_WRAP - 1, A_WRAP + 6),
            (A_ENSURE - 1, A_ENSURE + 6),
            (A_PSR, A_PSR + 12),
            (A_COUNT, A_COUNT_END)]
print('B4 已知改動區（B3 行號）：%s' % (KNOWN_B4,))
def in_known(n):
    return any(a <= n <= b for a, b in KNOWN_B4)
for tag, i1, i2, j1, j2 in opsB4:
    if tag in ('delete', 'replace'):
        bad = [n for n in range(i1 + 1, i2 + 1)
               if not in_known(n) and old[n - 1].strip() != '']
        assert not bad, 'B4 %s 段有舊行落喺已知區之外：舊 L%d-%d，界外行 %s' % (
            tag, i1 + 1, i2, bad[:5])
    elif tag == 'insert':
        anchor = i1 + 1  # 插入點前面嗰行（B3 行號）
        assert any(a - 2 <= anchor <= b + 2 for a, b in KNOWN_B4), \
            'B4 insert 落點喺未知區：B3 L%d 附近，新 L%d-%d' % (anchor, j1 + 1, j2)
print('B4 非 equal 段全部落喺已知改動區（界外只得空行；insert 落點全部喺已知區附近）')

def maplineB3(n):
    m = shiftB3.get(n)
    assert m is not None, 'B3 L%d 無對位去 B4' % n
    return m

# ---- PINS（測試檔而家嘅 B3 行號） ----
def _nums_from_file(path, pattern):
    txt = (ROOT / path).read_text(encoding='utf-8')
    return sorted(set(int(x) for x in re.findall(pattern, txt)))
KWAN_PINS = _nums_from_file('tests/test_kwan151_static.py', r'line\((\d+)\)')
ROM_PINS = _nums_from_file('tests/test_rom176_static.py', r'line\((\d+)\)')
TANG_PINS = _nums_from_file('tests/test_tang152_static.py', r'lines\(\)\[(\d+)\]')
T125_LS = _nums_from_file('tests/test_text125_static.py', r'ls\[(\d+)\]')
T125_MSG = _nums_from_file('tests/test_text125_static.py', r'第 (\d+) 行')
t114 = (ROOT / 'tests/test_travel114_static.py').read_text(encoding='utf-8')
def _setnums(name):
    m = re.search(name + r' = \{(.*?)\n\}', t114, re.S)
    return [int(x) for x in re.findall(r'^\s*(\d+),', m.group(1), re.M)]
FREE_B3 = _setnums('FREE_LINES'); COUNT_B3 = _setnums('COUNT_LINES')
FREE_FLAGS = ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')

n_checked = 0
for ln in KWAN_PINS + ROM_PINS:
    nl = maplineB3(ln)
    assert old[ln - 1] == new[nl - 1], 'B3 L%d ≠ B4 L%d：\n舊：%s\n新：%s' % (ln, nl, old[ln - 1][:120], new[nl - 1][:120])
    n_checked += 1
for ln in TANG_PINS + T125_LS:
    nl = maplineB3(ln + 1)  # 0-based index → 1-based 行號
    assert old[ln] == new[nl - 1], 'B3 L%d (0-based %d) ≠ B4 L%d' % (ln + 1, ln, nl)
    n_checked += 1
for ln in T125_MSG:
    nl = maplineB3(ln)
    assert old[ln - 1] == new[nl - 1], 'text125 B3 L%d ≠ B4 L%d' % (ln, nl)
    n_checked += 1
for ln in FREE_B3 + COUNT_B3:
    nl = maplineB3(ln)
    assert old[ln - 1] == new[nl - 1], 'travel114 B3 L%d ≠ B4 L%d' % (ln, nl)
    n_checked += 1
print('釘行逐字核實：%d 項全部 B3→B4 內容相同（kwan %d／rom %d／tang152 %d／text125 %d／travel114 FREE %d＋COUNT %d）'
      % (n_checked, len(KWAN_PINS), len(ROM_PINS), len(TANG_PINS),
         len(T125_LS) + len(T125_MSG), len(FREE_B3), len(COUNT_B3)))
for ln in FREE_B3:
    assert any(f in old[ln - 1] for f in FREE_FLAGS), 'FREE B3 L%d 唔帶旗：%s' % (ln, old[ln - 1][:100])
for ln in COUNT_B3:
    assert not any(f in old[ln - 1] for f in FREE_FLAGS), 'COUNT B3 L%d 帶旗：%s' % (ln, old[ln - 1][:100])
print('travel114 語義核實：FREE %d 行全部帶旗、COUNT %d 行全部冇旗' % (len(FREE_B3), len(COUNT_B3)))

if CHECK:
    print('CHECK 模式：核實全部通過，冇寫檔')
    sys.exit(0)

# ---- 寫檔（單次掃描 dict 查表，唔逐對 re.sub） ----
def resync_numbers(path, pattern, mapping, zero_based=False):
    """pattern：re.compile，group(1) 係行號；mapping：{舊行號: 新行號}。
       只改 mapping 入面有嘅數字，其餘唔郁；回傳改動數。"""
    p = ROOT / path
    txt = p.read_text(encoding='utf-8')
    n = [0]
    def repl(mo):
        v = int(mo.group(1))
        key = v if not zero_based else v + 1
        if key in mapping:
            nv = mapping[key] - 1 if zero_based else mapping[key]
            if nv == v:
                return mo.group(0)
            n[0] += 1
            return mo.group(0).replace(str(v), str(nv), 1)
        return mo.group(0)
    txt2 = pattern.sub(repl, txt)
    p.write_text(txt2, encoding='utf-8')
    print('改 %s：%d 個數字改動' % (path, n[0]))
    return n[0]

def replace_once(path, old_frag, new_frag):
    p = ROOT / path
    txt = p.read_text(encoding='utf-8')
    assert txt.count(old_frag) == 1, '%s 錨出現 %d 次：%r' % (path, txt.count(old_frag), old_frag[:80])
    p.write_text(txt.replace(old_frag, new_frag, 1), encoding='utf-8')
    print('改 %s：1 處行內編輯' % path)

def append_comment_after(path, anchor_frag, comment):
    p = ROOT / path
    txt = p.read_text(encoding='utf-8')
    assert txt.count(anchor_frag) == 1, '%s 錨出現 %d 次：%r' % (path, txt.count(anchor_frag), anchor_frag[:60])
    p.write_text(txt.replace(anchor_frag, anchor_frag + '\n' + comment, 1), encoding='utf-8')
    print('改 %s：加 B4 resync 註解 1 行' % path)

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
    new_region, cnt = re.subn(r'^(\s*)(\d+),', repl, region, flags=re.M)
    assert cnt == len(re.findall(r'^\s*\d+,', region, re.M))
    txt = txt[:m.start(1)] + new_region + txt[m.end(1):]
    p.write_text(txt, encoding='utf-8')
    changed = sum(1 for v in mapping if v in [int(x) for x in re.findall(r'^\s*(\d+),', region, re.M)])
    print('改 %s %s 區：%d 個數字改動（其餘唔郁）' % (path, start_pat, changed))

NEW_TOTAL = 47584
NEW_DEF = maplineB3(42947)
NEW_WRAP = maplineB3(31063)
print('新總行數 %d、新 DEF %d、新 WRAPPER %d' % (NEW_TOTAL, NEW_DEF, NEW_WRAP))
MAP_B3 = {b3: maplineB3(b3) for b3 in sorted(shiftB3.keys())}
_k = lambda n: maplineB3(n)

# kwan151：line(N) 釘
kw_map = {n: _k(n) for n in KWAN_PINS}
resync_numbers('tests/test_kwan151_static.py', re.compile(r'line\((\d+)\)'), kw_map)
append_comment_after('tests/test_kwan151_static.py',
    '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py）；13 個釘行全部喺首個刪區（ENTRY L6371）之前，行號唔郁（difflib 對位核實純漂移）。',
    '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py）；13 個釘行按 difflib 映射重寫（%s），difflib 對位核實純漂移。' % (
        '、'.join('%d→%d' % (n, _k(n)) for n in KWAN_PINS if _k(n) != n) or '全部唔郁'))

# gift185：總行數
replace_once('tests/test_gift185_static.py',
    '總行數 47481（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612）',
    '總行數 47584（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612＋v229 B4 +103）')
replace_once('tests/test_gift185_static.py', "html.count('\\n') == 47481", "html.count('\\n') == 47584")
append_comment_after('tests/test_gift185_static.py',
    '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py），總行數 63093→47481（difflib 對位核實純漂移）。',
    '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py），總行數 47481→47584（difflib 對位核實純漂移）。')

# rom176：line(N) 釘
rom_map = {n: _k(n) for n in ROM_PINS}
resync_numbers('tests/test_rom176_static.py', re.compile(r'line\((\d+)\)'), rom_map)
append_comment_after('tests/test_rom176_static.py',
    '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py）；釘行按 difflib 映射重寫（31868→18430、55829→41377、56197→41745、57336→42884、57430→42978；6360 唔郁），difflib 對位核實純漂移。',
    '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py）；釘行按 difflib 映射重寫（%s；6360 唔郁），difflib 對位核實純漂移。' % (
        '、'.join('%d→%d' % (n, _k(n)) for n in ROM_PINS if n != 6360)))

# tang152：0-based index
tang_map = {n: _k(n) for n in [x + 1 for x in TANG_PINS]}
resync_numbers('tests/test_tang152_static.py', re.compile(r'lines\(\)\[(\d+)\]'), tang_map, zero_based=True)
append_comment_after('tests/test_tang152_static.py',
    '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py）；HELD 26104→12667、normaliseTangStub152 31800→18359、stub 呼叫行 31967→18486（difflib 對位核實純漂移）。',
    '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py）；HELD 12667→%d、normaliseTangStub152 18359→%d、stub 呼叫行 18486→%d（difflib 對位核實純漂移）。' % (
        _k(12667) - 1, _k(18359) - 1, _k(18486) - 1))

# tang171／tang173：總行數＋openLoc DEF 行
for fname in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    replace_once(fname,
        '總行數 47481（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612）',
        '總行數 47584（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612＋v229 B4 +103）')
    replace_once(fname, "src.count('\\n') == 47481", "src.count('\\n') == 47584")
    replace_once(fname, 'openLoc DEF 行 42947', 'openLoc DEF 行 %d' % NEW_DEF)
    replace_once(fname, '＋v229 B3 −15612，travel114 釘行', '＋v229 B3 −15612＋v229 B4 +103，travel114 釘行')
    replace_once(fname, 'len(lines) >= 42947', 'len(lines) >= %d' % NEW_DEF)
    replace_once(fname, 'lines[42946]', 'lines[%d]' % (NEW_DEF - 1))
    append_comment_after(fname,
        '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py），總行數 63093→47481、DEF 57477→42947（difflib 對位核實純漂移）。',
        '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py），總行數 47481→47584、DEF 42947→%d（difflib 對位核實純漂移）。' % NEW_DEF)

# text125：ls[] index＋「第 N 行」訊息
t125_map = {n: _k(n) for n in [x + 1 for x in T125_LS] + T125_MSG}
resync_numbers('tests/test_text125_static.py', re.compile(r'ls\[(\d+)\]'), t125_map, zero_based=True)
resync_numbers('tests/test_text125_static.py', re.compile(r'第 (\d+) 行'), t125_map)
replace_once('tests/test_text125_static.py',
    '；v20a229 B3 resync：33899→20067（淨 −15612，difflib 對位核實純漂移，見 qa229/resync229_b3.py）。',
    '；v20a229 B3 resync：33899→20067（淨 −15612，difflib 對位核實純漂移，見 qa229/resync229_b3.py）。；v20a229 B4 resync：20067→%d（淨 +103，difflib 對位核實純漂移，見 qa229/resync229_b4.py）。' % _k(20067))

# travel114：FREE／COUNT set＋DEF／WRAPPER
PINMAP = {ln: maplineB3(ln) for ln in FREE_B3 + COUNT_B3}
resync_region('tests/test_travel114_static.py', 'FREE_LINES', PINMAP)
resync_region('tests/test_travel114_static.py', 'COUNT_LINES', PINMAP)
replace_once('tests/test_travel114_static.py', 'DEF_LINE = 42947', 'DEF_LINE = %d' % NEW_DEF)
replace_once('tests/test_travel114_static.py', 'WRAPPER_LINE = 31063', 'WRAPPER_LINE = %d' % NEW_WRAP)
append_comment_after('tests/test_travel114_static.py',
    '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 57477→42947、WRAPPER 45591→31063），核實純漂移。',
    '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 42947→%d、WRAPPER 31063→%d），核實純漂移。' % (NEW_DEF, NEW_WRAP))

print('全部寫檔完成')
