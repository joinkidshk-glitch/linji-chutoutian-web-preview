#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v20a229 B7 resync：index.html 淨 +54 行（報紙分類 A10＋忠告卡 Q6：press94 category 先行＋
# Q6 helper 32 行＋doAudition 接線＋手帳排程 job: 接線＋press94 註解）。
# 用法：python3 qa229/resync229_b7.py [--check]   （--check 只核實，唔寫檔）
# 做法（跟每版慣例，唔好人手估行號）：
#   1. 單段 difflib 對位：B6（HEAD）→ 現況，逐段核實。
#      B7 係純插入（+54／-0），唔應該有 delete／replace opcode。
#      全部 insert 嘅落點必須喺已知 B7 改動區附近。
#   2. 釘行以測試檔而家嘅 B6 行號起步，經映射推到 B7 行號；
#      全部釘行舊新內容逐字相同＝純漂移先改行號。
# 改動範圍：tests/ 下面 7 檔（kwan151／gift185／rom176／tang152／tang171／tang173／
#   text125／travel114 釘行＋總行數；content allowlist 三檔 aud91fix122／aud91fix124／
#   newspaper214_award 嘅 B7 豁免唔係釘行，唔喺呢度處理，另行加）。
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = '--check' in sys.argv
BASE_REF = 'HEAD'  # v20a229 B6

def load_ref(ref):
    out = subprocess.check_output(['git', 'show', ref + ':index.html'], cwd=str(ROOT), text=True)
    return out.split('\n')

def build_shift(old, new):
    """difflib 對位：舊行號（1-based）→ 新行號；回傳 (shift, opcodes)。
       B7 係純插入，delete／replace 出現即死。"""
    sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    shift = {}
    ops = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        ops.append((tag, i1, i2, j1, j2))
        if tag == 'equal':
            for k in range(i2 - i1):
                shift[i1 + k + 1] = j1 + k + 1
        elif tag in ('delete', 'replace'):
            raise SystemExit('非預期 %s opcode：舊 L%d-%d（B7 應該純插入）' % (tag, i1 + 1, i2))
        elif tag == 'insert':
            pass
    return shift, ops

old = load_ref(BASE_REF)
new = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print('B6 行數 %d（split）／現況 %d；\\n 數 %d／%d'
      % (len(old), len(new), len(old) - 1, len(new) - 1))
assert len(old) - 1 == 48166, 'B6 總行數唔係 48166'
assert len(new) - 1 == 48220, '現況總行數唔係 48220（B7 淨 +54）'

shiftB6, opsB7 = build_shift(old, new)
print('B7 difflib：%d 舊行有對位；opcodes %d 段（delete／replace 0 段）'
      % (len(shiftB6), len(opsB7)))

def find_b6(needle, start=1):
    for i in range(start - 1, len(old)):
        if needle in old[i]:
            return i + 1
    raise SystemExit('B6 搵唔到錨：%r' % needle)

# B7 已知改動區（B6 行號計；由錨字串定位，唔用人手抄行號）
A_JOB = find_b6('試鏡演完，評判只講咗句「返去等消息啦」。何生話：')  # job: 分支（＋4，插喺呢行之前）
A_PRESS_HDR = find_b6('預設 named：有 A 級海報')  # press94 註解（＋2）
A_PRESS_FN = find_b6('function press94RoleClass(gig, labelHint){')  # 分類器 category 先行（＋8）
A_Q6 = find_b6('function doAudition(gig, L){')  # Q6 helper 模組（＋34，插喺呢行之前）
A_GUARD = find_b6('const p=chance(gig); // 0..1 success probability')  # doAudition 忠告卡接線（＋5）
A_MODAL = find_b6('何生話：${aud91WaitPhrase(rec.wait)}')  # doAudition 完成 modal 提示行（＋1）
KNOWN_B7 = [(A_JOB - 5, A_JOB + 1),
            (A_PRESS_HDR - 1, A_PRESS_HDR + 3),
            (A_PRESS_FN - 1, A_PRESS_FN + 14),
            (A_Q6 - 2, A_Q6 + 1),
            (A_GUARD - 3, A_GUARD + 1),
            (A_MODAL - 2, A_MODAL + 1)]
print('B7 已知改動區（B6 行號）：%s' % (KNOWN_B7,))
for tag, i1, i2, j1, j2 in opsB7:
    if tag == 'insert':
        anchor = i1 + 1  # 插入點前面嗰行（B6 行號）
        assert any(a - 2 <= anchor <= b + 2 for a, b in KNOWN_B7), \
            'B7 insert 落點喺未知區：B6 L%d 附近，新 L%d-%d' % (anchor, j1 + 1, j2)
print('B7 insert 段全部落喺已知改動區附近')

def maplineB6(n):
    m = shiftB6.get(n)
    assert m is not None, 'B6 L%d 無對位去 B7' % n
    return m

# ---- PINS（測試檔而家嘅 B6 行號） ----
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
FREE_B6 = _setnums('FREE_LINES'); COUNT_B6 = _setnums('COUNT_LINES')
FREE_FLAGS = ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')
DEF_B6 = 43624; WRAP_B6 = 31683

n_checked = 0
for ln in KWAN_PINS + ROM_PINS:
    nl = maplineB6(ln)
    assert old[ln - 1] == new[nl - 1], 'B6 L%d ≠ B7 L%d：\n舊：%s\n新：%s' % (ln, nl, old[ln - 1][:120], new[nl - 1][:120])
    n_checked += 1
for ln in TANG_PINS + T125_LS:
    nl = maplineB6(ln + 1)  # 0-based index → 1-based 行號
    assert old[ln] == new[nl - 1], 'B6 L%d (0-based %d) ≠ B7 L%d' % (ln + 1, ln, nl)
    n_checked += 1
for ln in T125_MSG:
    nl = maplineB6(ln)
    assert old[ln - 1] == new[nl - 1], 'text125 B6 L%d ≠ B7 L%d' % (ln, nl)
    n_checked += 1
for ln in FREE_B6 + COUNT_B6 + [DEF_B6, WRAP_B6]:
    nl = maplineB6(ln)
    assert old[ln - 1] == new[nl - 1], 'travel114 B6 L%d ≠ B7 L%d' % (ln, nl)
    n_checked += 1
print('釘行逐字核實：%d 項全部 B6→B7 內容相同（kwan %d／rom %d／tang152 %d／text125 %d／travel114 FREE %d＋COUNT %d＋DEF／WRAPPER）'
      % (n_checked, len(KWAN_PINS), len(ROM_PINS), len(TANG_PINS),
         len(T125_LS) + len(T125_MSG), len(FREE_B6), len(COUNT_B6)))
for ln in FREE_B6:
    assert any(f in old[ln - 1] for f in FREE_FLAGS), 'FREE B6 L%d 唔帶旗：%s' % (ln, old[ln - 1][:100])
for ln in COUNT_B6:
    assert not any(f in old[ln - 1] for f in FREE_FLAGS), 'COUNT B6 L%d 帶旗：%s' % (ln, old[ln - 1][:100])
print('travel114 語義核實：FREE %d 行全部帶旗、COUNT %d 行全部冇旗' % (len(FREE_B6), len(COUNT_B6)))

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
    print('改 %s：加 B7 resync 註解 1 行' % path)

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

NEW_TOTAL = 48220
NEW_DEF = maplineB6(DEF_B6)
NEW_WRAP = maplineB6(WRAP_B6)
print('新總行數 %d、新 DEF %d（＋%d）、新 WRAPPER %d（＋%d）' % (NEW_TOTAL, NEW_DEF, NEW_DEF - DEF_B6, NEW_WRAP, NEW_WRAP - WRAP_B6))
MAP_B6 = {b6: maplineB6(b6) for b6 in sorted(shiftB6.keys())}
_k = lambda n: maplineB6(n)
def _moved(pins):
    moved = ['%d→%d' % (n, _k(n)) for n in pins if _k(n) != n]
    same = sum(1 for n in pins if _k(n) == n)
    return moved, same

# kwan151：line(N) 釘
kw_map = {n: _k(n) for n in KWAN_PINS}
resync_numbers('tests/test_kwan151_static.py', re.compile(r'line\((\d+)\)'), kw_map)
_moved_k, _same_k = _moved(KWAN_PINS)
append_comment_after('tests/test_kwan151_static.py',
    '# v20a229 B6 resync：index.html 淨 +332 行（抉擇即派＋定期合約制，見 qa229/resync229_b6.py）；13 個釘行按 difflib 映射重寫（12507→12509、12848→12850、12851→12853、12852→12854、12853→12855、12896→12898、13115→13117、14116→14118、14149→14151、18028→18030、18037→18039、18038→18040、18080→18082；0 個唔郁），difflib 對位核實純漂移。',
    '# v20a229 B7 resync：index.html 淨 +54 行（報紙分類 A10＋忠告卡 Q6，見 qa229/resync229_b7.py）；13 個釘行按 difflib 映射重寫（%s；%d 個唔郁），difflib 對位核實純漂移。' % (
        '、'.join(_moved_k) if _moved_k else '全部唔郁', _same_k))

# gift185：總行數
replace_once('tests/test_gift185_static.py',
    '總行數 48166（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612＋v229 B4 +103＋v229 B5 +250＋v229 B6 +332）',
    '總行數 48220（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612＋v229 B4 +103＋v229 B5 +250＋v229 B6 +332＋v229 B7 +54）')
replace_once('tests/test_gift185_static.py', "html.count('\\n') == 48166", "html.count('\\n') == 48220")
append_comment_after('tests/test_gift185_static.py',
    '# v20a229 B6 resync：index.html 淨 +332 行（抉擇即派＋定期合約制，見 qa229/resync229_b6.py），總行數 47834→48166（difflib 對位核實純漂移）。',
    '# v20a229 B7 resync：index.html 淨 +54 行（報紙分類 A10＋忠告卡 Q6，見 qa229/resync229_b7.py），總行數 48166→48220（difflib 對位核實純漂移）。')

# rom176：line(N) 釘
rom_map = {n: _k(n) for n in ROM_PINS}
resync_numbers('tests/test_rom176_static.py', re.compile(r'line\((\d+)\)'), rom_map)
_moved_r, _same_r = _moved(ROM_PINS)
append_comment_after('tests/test_rom176_static.py',
    '# v20a229 B6 resync：index.html 淨 +332 行（抉擇即派＋定期合約制，見 qa229/resync229_b6.py）；釘行按 difflib 映射重寫（18499→18501、41722→42054、42090→42422、43229→43561、43323→43655；1 個唔郁），difflib 對位核實純漂移。',
    '# v20a229 B7 resync：index.html 淨 +54 行（報紙分類 A10＋忠告卡 Q6，見 qa229/resync229_b7.py）；釘行按 difflib 映射重寫（%s；%d 個唔郁），difflib 對位核實純漂移。' % (
        '、'.join('%d→%d' % (n, _k(n)) for n in ROM_PINS if _k(n) != n), _same_r))

# tang152：0-based index
tang_map = {n: _k(n) for n in [x + 1 for x in TANG_PINS]}
resync_numbers('tests/test_tang152_static.py', re.compile(r'lines\(\)\[(\d+)\]'), tang_map, zero_based=True)
_moved_t, _same_t = _moved([x + 1 for x in TANG_PINS])
append_comment_after('tests/test_tang152_static.py',
    '# v20a229 B6 resync：index.html 淨 +332 行（抉擇即派＋定期合約制，見 qa229/resync229_b6.py）；3 個釘行按 difflib 映射重寫（12667→12669、18428→18430、18555→18557；0 個唔郁），difflib 對位核實純漂移。',
    '# v20a229 B7 resync：index.html 淨 +54 行（報紙分類 A10＋忠告卡 Q6，見 qa229/resync229_b7.py）；3 個釘行按 difflib 映射重寫（%s；%d 個唔郁），difflib 對位核實純漂移。' % (
        '、'.join(_moved_t) if _moved_t else '全部唔郁', _same_t))

# tang171／tang173：總行數＋openLoc DEF 行
for fname in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    replace_once(fname,
        '總行數 48166（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612＋v229 B4 +103＋v229 B5 +250＋v229 B6 +332）',
        '總行數 48220（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612＋v229 B4 +103＋v229 B5 +250＋v229 B6 +332＋v229 B7 +54）')
    replace_once(fname, "src.count('\\n') == 48166", "src.count('\\n') == 48220")
    replace_once(fname, 'openLoc DEF 行 43624', 'openLoc DEF 行 %d' % NEW_DEF)
    replace_once(fname, '＋v229 B5 +243＋v229 B6 +332，travel114 釘行', '＋v229 B5 +243＋v229 B6 +332＋v229 B7 +54，travel114 釘行')
    replace_once(fname, 'len(lines) >= 43624', 'len(lines) >= %d' % NEW_DEF)
    replace_once(fname, 'lines[43623]', 'lines[%d]' % (NEW_DEF - 1))
    append_comment_after(fname,
        '# v20a229 B6 resync：index.html 淨 +332 行（抉擇即派＋定期合約制，見 qa229/resync229_b6.py），總行數 47834→48166、DEF 43292→43624（difflib 對位核實純漂移）。',
        '# v20a229 B7 resync：index.html 淨 +54 行（報紙分類 A10＋忠告卡 Q6，見 qa229/resync229_b7.py），總行數 48166→48220、DEF 43624→%d（difflib 對位核實純漂移）。' % NEW_DEF)

# text125：ls[] index＋「第 N 行」訊息
t125_map = {n: _k(n) for n in [x + 1 for x in T125_LS] + T125_MSG}
resync_numbers('tests/test_text125_static.py', re.compile(r'ls\[(\d+)\]'), t125_map, zero_based=True)
resync_numbers('tests/test_text125_static.py', re.compile(r'第 (\d+) 行'), t125_map)
_t125_old = _k(20153)
replace_once('tests/test_text125_static.py',
    '；v20a229 B6 resync：20146→20153（淨 +7，applyChoice hook＋fresh 欄位＋normalize 回填，difflib 對位核實純漂移，見 qa229/resync229_b6.py）。',
    '；v20a229 B6 resync：20146→20153（淨 +7，applyChoice hook＋fresh 欄位＋normalize 回填，difflib 對位核實純漂移，見 qa229/resync229_b6.py）。；v20a229 B7 resync：20153→%d（淨 +%d，B7 插入點全部喺 L25067 之後，呢行唔郁，difflib 對位核實純漂移，見 qa229/resync229_b7.py）。' % (_t125_old, _t125_old - 20153))

# travel114：FREE／COUNT set＋DEF／WRAPPER
PINMAP = {ln: maplineB6(ln) for ln in FREE_B6 + COUNT_B6}
resync_region('tests/test_travel114_static.py', 'FREE_LINES', PINMAP)
resync_region('tests/test_travel114_static.py', 'COUNT_LINES', PINMAP)
replace_once('tests/test_travel114_static.py', 'DEF_LINE = 43624', 'DEF_LINE = %d' % NEW_DEF)
replace_once('tests/test_travel114_static.py', 'WRAPPER_LINE = 31683', 'WRAPPER_LINE = %d' % NEW_WRAP)
append_comment_after('tests/test_travel114_static.py',
    '# v20a229 B6 resync：index.html 淨 +332 行（抉擇即派＋定期合約制，見 qa229/resync229_b6.py）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 43292→43624、WRAPPER 31353→31683），核實純漂移。',
    '# v20a229 B7 resync：index.html 淨 +54 行（報紙分類 A10＋忠告卡 Q6，見 qa229/resync229_b7.py）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 43624→%d、WRAPPER 31683→%d），核實純漂移。' % (NEW_DEF, NEW_WRAP))

print('全部寫檔完成')
