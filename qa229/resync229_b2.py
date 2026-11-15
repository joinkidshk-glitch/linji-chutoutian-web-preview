#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎——textfix55 ＋1／DUR90_DAILY ＋9／
#   fameFloor ＋3／chance ＋2／gigTierKey＋canon ＋15／gigBreachFee ＋2／難度星 ＋2／
#   resolveRoleScale ＋5／nat92Gig ＋1／板面 doc＋tierOrder ＋7／tipGig ＋2／aud91 ＋3／
#   failShoot ＋1；舊行 0 刪，全部係插入＋原地改值）。
# 用法：python3 qa229/resync229_b2.py [--check]   （--check 只核實，唔寫檔）
# 做法（跟每版慣例，唔好人手估行號）：
#   1. 兩段 difflib 對位：95baf7e → B1（9afc402）→ 現況，逐段核實 replace／insert 全部落喺
#      已知 B2 改動區，0 刪行；全部釘行舊新內容逐字相同＝純漂移先改行號。
#   2. 釘行以 B1 腳本同一組 PINS（95baf7e 行號）起步，經兩段映射推到 B2 行號。
# 改動範圍：tests/ 下面 8 檔（kwan151／gift185／rom176／tang152／tang171／tang173／
#   text125／travel114 釘行＋總行數；test_dur90_logic.js 嘅 SPEC_DAILY 係 B2 內容改動，
#   唔係 resync，唔喺呢度處理）。
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = '--check' in sys.argv
BASE95_REF = '95baf7e'
BASEB1_REF = '9afc402'

def load_ref(ref):
    out = subprocess.check_output(['git', 'show', ref + ':index.html'], cwd=str(ROOT), text=True)
    return out.split('\n')

def build_shift(old, new):
    """difflib 對位：舊行號（1-based）→ 新行號；回傳 (shift, replaces)。"""
    sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    shift = {}
    replaces = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                shift[i1 + k + 1] = j1 + k + 1
        elif tag == 'replace':
            for k in range(min(i2 - i1, j2 - j1)):
                shift[i1 + k + 1] = j1 + k + 1
            replaces.append((i1 + 1, i2, j1 + 1, j2))
        elif tag == 'insert':
            replaces.append((i1 + 1, i1, j1 + 1, j2))
        else:
            raise SystemExit('非預期 opcode（本批 0 刪行）：%s 舊 %d-%d 新 %d-%d' % (tag, i1 + 1, i2, j1 + 1, j2))
    return shift, replaces

old95 = load_ref(BASE95_REF)
mid = load_ref(BASEB1_REF)
new = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print('95baf7e 行數 %d（split）／B1 行數 %d／現況行數 %d；\\n 數 %d／%d／%d'
      % (len(old95), len(mid), len(new), len(old95) - 1, len(mid) - 1, len(new) - 1))
assert len(old95) - 1 == 63004, '95baf7e 總行數唔係 63004'
assert len(mid) - 1 == 63045, 'B1 總行數唔係 63045'
assert len(new) - 1 == 63093, '現況總行數唔係 63093（B2 淨 +48）'

shift95, _rep95 = build_shift(old95, mid)
shiftB1, repB2 = build_shift(mid, new)
print('B2 difflib：%d 舊行有對位；非 equal 段 %d 區' % (len(shiftB1), len(repB2)))
# B2 全部非 equal 段必須落喺已知改動區（B1 行號計）
KNOWN_B2 = [(31630, 31645), (33085, 33105), (34885, 34900), (35080, 35100),
            (35165, 35200), (35330, 35370), (35480, 35525), (36235, 36310),
            (59185, 59195), (59390, 59465), (60015, 60070), (61050, 61110),
            (61808, 61865)]
for a, b, c, d in repB2:
    lo, hi = (a, b) if b >= a else (c, d)
    assert any(klo <= lo <= khi or klo <= hi <= khi for klo, khi in KNOWN_B2), \
        'B2 非 equal 段落喺未知區：舊 L%d-%d 新 L%d-%d' % (a, b, c, d)
print('B2 非 equal 段全部落喺已知改動區（textfix55／DUR90／fameFloor／chance／gigTierKey／'
      'breachFee／難度星／resolveRoleScale／nat92Gig／板面／tipGig／aud91／failShoot）')

def mapline95(n):
    m1 = shift95.get(n)
    assert m1 is not None, '95baf7e L%d 無對位去 B1' % n
    m2 = shiftB1.get(m1)
    assert m2 is not None, 'B1 L%d 無對位去 B2' % m1
    return m2

def maplineB1(n):
    m = shiftB1.get(n)
    assert m is not None, 'B1 L%d 無對位去 B2' % n
    return m

FALLBACK125 = '(typeof b.text === "string" && b.text ? [b.text] : [])'
# ---- PINS（同 B1 腳本一樣，95baf7e 行號） ----
PINS = {
 'tests/test_kwan151_static.py': [
    (25943, '陳淑芬'), (26284, '["陳淑芬","施南生","Ho哥"]'),
    (26332, 'nextHint'), (26551, '["陳淑芬","施南生","Ho哥","Ho 哥"]'),
    (26289, 'v151 退役'), (26287, '雙女主改讀 devAppendix'),
    (26288, 'bad("dual_note")'), (31404, '星河電視城'),
    (31394, '關海媚提醒頭條係雙刃'), (27585, 'kwan_hoimei: { artId:"char_kwan"'),
    (31446, '["rel_mei","關海媚"]'), (31403, '采兒同關海媚嗰邊都近咗啲'),
    (27552, '"關海媚":"kwan_hoimei"')],
 'tests/test_rom176_static.py': [
    (6360, 'lan:{ id:"lan"'), (31868, 'GIFT_REACT = giftReact'),
    (55829, '/* ===== v20a176 ROM176'),
    (56197, 'function rom176ApplyGiftOverrides()'),
    (57336, 'function addLocTalkGiftActs(add, L, npcId)'),
    (57430, 'rom176TryIntercept(id)')],
 'tests/test_tang152_static.py': [
    (26103, 'const HELD = ["R_tang_push1"'),
    (31793, 'function normaliseTangStub152(pack){'),
    (31939, 'try{ normaliseTangStub152(rom2);')],
 'tests/test_tang171_static.py': [(57399, 'function openLoc(id, opts){')],
 'tests/test_tang173_static.py': [(57399, 'function openLoc(id, opts){')],
 'tests/test_text125_static.py': [
    (28077, FALLBACK125), (28214, FALLBACK125),
    (33849, 'if(typeof b.text === "string" && b.text){')],
 'tests/test_travel114_static.py': [
    (57399, 'function openLoc(id, opts){'),
    (45513, 'openLoc: function(id, opts){ openLoc(id, opts); }')],
}
# travel114：FREE／COUNT 全部釘行（由測試檔讀出嚟，B1 行號，唔用人手抄）
t114 = (ROOT / 'tests/test_travel114_static.py').read_text(encoding='utf-8')
def _setnums(name):
    m = re.search(name + r' = \{(.*?)\n\}', t114, re.S)
    return [int(x) for x in re.findall(r'^\s*(\d+),', m.group(1), re.M)]
FREE_B1 = _setnums('FREE_LINES'); COUNT_B1 = _setnums('COUNT_LINES')
for ln in FREE_B1 + COUNT_B1:
    PINS['tests/test_travel114_static.py'].append((ln, 'openLoc('))
FREE_FLAGS = ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')

n_checked = 0
for fname, pins in PINS.items():
    for ln, anchor in pins:
        if fname == 'tests/test_travel114_static.py' and ln in FREE_B1 + COUNT_B1:
            b1 = ln
        else:
            b1 = shift95.get(ln)
            assert b1 is not None, '%s 95baf7e L%d 無對位去 B1' % (fname, ln)
        nl = maplineB1(b1)
        assert mid[b1 - 1] == new[nl - 1], \
            '%s B1 L%d ≠ B2 L%d：\n舊：%s\n新：%s' % (fname, b1, nl, mid[b1 - 1][:120], new[nl - 1][:120])
        assert anchor in mid[b1 - 1], '%s B1 L%d 冇錨 %r：%s' % (fname, b1, anchor, mid[b1 - 1][:120])
        n_checked += 1
print('釘行逐字核實：%d 項全部 B1→B2 內容相同（含 travel114 FREE %d＋COUNT %d＋DEF／WRAPPER）'
      % (n_checked, len(FREE_B1), len(COUNT_B1)))
# travel114 額外語義核實：FREE 行 B1 內容帶旗、COUNT 行 B1 內容冇旗
for ln in FREE_B1:
    assert any(f in mid[ln - 1] for f in FREE_FLAGS), 'FREE B1 L%d 唔帶旗：%s' % (ln, mid[ln - 1][:100])
for ln in COUNT_B1:
    assert not any(f in mid[ln - 1] for f in FREE_FLAGS), 'COUNT B1 L%d 帶旗：%s' % (ln, mid[ln - 1][:100])
print('travel114 語義核實：FREE %d 行全部帶旗、COUNT %d 行全部冇旗' % (len(FREE_B1), len(COUNT_B1)))

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
    print('改 %s：加 B2 resync 註解 1 行' % path)

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

NEW_TOTAL = 63093
NEW_DEF = maplineB1(57440)
NEW_WRAP = maplineB1(45554)
print('新總行數 %d、新 DEF %d、新 WRAPPER %d' % (NEW_TOTAL, NEW_DEF, NEW_WRAP))
assert NEW_DEF == 57477, 'DEF 預期 57477，實得 %d' % NEW_DEF

# 全檔 1-based 映射（B1→B2），供各檔查表
MAP_B1 = {b1: maplineB1(b1) for b1 in sorted(shiftB1.keys())}
# 測試檔入面而家係 B1 行號：映射 key 一律用 B1 數（shift95[95baf7e 釘]），值係 B2 數。
def b1key(n95):
    return shift95[n95]
_k = lambda n: mapline95(n)

# kwan151：13 粒 line() 釘（名入面嘅 L25608 等歷史標籤唔郁；只改 line(N) 查嘅行號）
kw_map = {b1key(n): _k(n) for n in [25943, 26284, 26332, 26551, 26289, 26287, 26288,
                             31404, 31394, 27585, 31446, 31403, 27552]}
resync_numbers('tests/test_kwan151_static.py', re.compile(r'line\((\d+)\)'), kw_map)
append_comment_after('tests/test_kwan151_static.py',
    '# v20a229 resync：index.html 淨 +41 行（新通告庫地基 B1：STORY_WIRE ＋1／sync 新庫優先 ＋5／loader ＋22／normalize ＋14；淨 +41）；13 個釘行按 difflib 映射重寫（25xxx／27xxx 者 ＋1、31xxx 者 ＋6；名入面嘅 L25608 等歷史標籤唔郁），difflib 對位核實純漂移，見 qa229/resync229.py。',
    '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py）；13 個釘行全部喺首個改動點（舊 L31637）之前，行號唔郁（difflib 對位核實純漂移）。')

# gift185：總行數
replace_once('tests/test_gift185_static.py',
    '總行數 63045（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41）',
    '總行數 63093（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48）')
replace_once('tests/test_gift185_static.py', "html.count('\\n') == 63045", "html.count('\\n') == 63093")
append_comment_after('tests/test_gift185_static.py',
    '# v20a229 resync：index.html 淨 +41 行（新通告庫地基 B1：STORY_WIRE ＋1／sync 新庫優先 ＋5／loader ＋22／normalize ＋14；淨 +41），總行數 63004→63045（difflib 對位核實純漂移，見 qa229/resync229.py）。',
    '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py），總行數 63045→63093（difflib 對位核實純漂移）。')

# rom176：釘行（L31712／L6152 等名係歷史標籤，唔郁；只改 line(N) 查嘅行號）
rom_map = {b1key(n): _k(n) for n in [6360, 31868, 55829, 56197, 57336, 57430]}
resync_numbers('tests/test_rom176_static.py', re.compile(r'line\((\d+)\)'), rom_map)
append_comment_after('tests/test_rom176_static.py',
    '# v20a229 resync：index.html 淨 +41 行（新通告庫地基 B1：STORY_WIRE ＋1／sync 新庫優先 ＋5／loader ＋22／normalize ＋14；淨 +41）；釘行按 difflib 映射重寫（31868→31875、55829→55870、56197→56238、57336→57377、57430→57471；6360 唔郁），difflib 對位核實純漂移，見 qa229/resync229.py。',
    '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py）；釘行按 difflib 映射重寫（31875→%d、55870→%d、56238→%d、57377→%d、57471→%d；6360 唔郁），difflib 對位核實純漂移。' % (
        _k(31868), _k(55829), _k(56197), _k(57336), _k(57430)))

# tang152：0-based index（標籤 L25817／L31610／L31754 係歷史名，唔郁）
tang_map = {b1key(n): _k(n) for n in [26103, 31793, 31939]}
resync_numbers('tests/test_tang152_static.py', re.compile(r'lines\(\)\[(\d+)\]'), tang_map, zero_based=True)
append_comment_after('tests/test_tang152_static.py',
    '# v20a229 resync：index.html 淨 +41 行（新通告庫地基 B1：STORY_WIRE ＋1／sync 新庫優先 ＋5／loader ＋22／normalize ＋14；淨 +41）；HELD 26103→26104、normaliseTangStub152 31793→31799、stub 呼叫行 31939→31966（difflib 對位核實純漂移，見 qa229/resync229.py）。',
    '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py）；HELD 26104 唔郁、normaliseTangStub152 31799→%d、stub 呼叫行 31966→%d（difflib 對位核實純漂移）。' % (_k(31793), _k(31939)))

# tang171／tang173：總行數＋openLoc DEF 行
for fname in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    replace_once(fname,
        '總行數 63045（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41）',
        '總行數 63093（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48）')
    replace_once(fname, "src.count('\\n') == 63045", "src.count('\\n') == 63093")
    replace_once(fname, 'openLoc DEF 行 57440', 'openLoc DEF 行 %d' % NEW_DEF)
    replace_once(fname, '＋v228 −170＋v229 +41，travel114 釘行', '＋v228 −170＋v229 +41＋v229 B2 +48，travel114 釘行')
    replace_once(fname, 'len(lines) >= 57440', 'len(lines) >= %d' % NEW_DEF)
    replace_once(fname, 'lines[57439]', 'lines[%d]' % (NEW_DEF - 1))
    append_comment_after(fname,
        '# v20a229 resync：index.html 淨 +41 行（新通告庫地基 B1：STORY_WIRE ＋1／sync 新庫優先 ＋5／loader ＋22／normalize ＋14；淨 +41），總行數 63004→63045、DEF 57399→57440（difflib 對位核實純漂移，見 qa229/resync229.py）。',
        '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py），總行數 63045→63093、DEF 57440→%d（difflib 對位核實純漂移）。' % NEW_DEF)

# text125：三錨點 ls[] index＋「第 N 行」訊息（len() 下限守衛仍然成立，唔郁）
t125_map = {b1key(n): _k(n) for n in [28077, 28214, 33849]}
resync_numbers('tests/test_text125_static.py', re.compile(r'ls\[(\d+)\]'), t125_map, zero_based=True)
resync_numbers('tests/test_text125_static.py', re.compile(r'第 (\d+) 行'), t125_map)
replace_once('tests/test_text125_static.py',
    '；v20a229 resync：33849→33890（淨 +41，difflib 對位核實純漂移，見 qa229/resync229.py）。',
    '；v20a229 resync：33849→33890（淨 +41，difflib 對位核實純漂移，見 qa229/resync229.py）。；v20a229 B2 resync：33890→%d（淨 +48，difflib 對位核實純漂移，見 qa229/resync229_b2.py）。' % _k(33849))

# travel114：FREE／COUNT set＋DEF／WRAPPER
PINMAP = {ln: maplineB1(ln) for ln in FREE_B1 + COUNT_B1}
resync_region('tests/test_travel114_static.py', 'FREE_LINES', PINMAP)
resync_region('tests/test_travel114_static.py', 'COUNT_LINES', PINMAP)
replace_once('tests/test_travel114_static.py', 'DEF_LINE = 57440', 'DEF_LINE = %d' % NEW_DEF)
replace_once('tests/test_travel114_static.py', 'WRAPPER_LINE = 45554', 'WRAPPER_LINE = %d' % NEW_WRAP)
append_comment_after('tests/test_travel114_static.py',
    '# v20a229 resync：index.html 淨 +41 行（新通告庫地基 B1：STORY_WIRE ＋1／sync 新庫優先 ＋5／loader ＋22／normalize ＋14；淨 +41）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 57399→57440、WRAPPER 45513→45554），核實純漂移。',
    '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 57440→%d、WRAPPER 45554→%d），核實純漂移。' % (NEW_DEF, NEW_WRAP))

print('全部寫檔完成')
