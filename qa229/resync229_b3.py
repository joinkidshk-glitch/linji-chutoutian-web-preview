#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v20a229 B3 resync：index.html 淨 −15,612 行（換庫——刪舊 pack 內嵌 fallback 137 張／
#   ENTRY＋WINTER 入口池／舊表 TIER110／REQ110／NAME93／LEADSTAR59／CLEAN100／海報舊表／
#   code-side 內容池 INTEL／FAVOR／RIVAL／EXODUS／WF3／BR89／MID／GIGS36／NAT92／
#   SOFT／WINTER 橋接／BRIDGE56；新庫併入 gigsByYear 單一來源＋entryGigPool229＋YearOf 唔再 +2）。
# 用法：python3 qa229/resync229_b3.py [--check]   （--check 只核實，唔寫檔）
# 做法（跟每版慣例，唔好人手估行號）：
#   1. 三段 difflib 對位：95baf7e → B1（9afc402）→ B2（d7c0e2f）→ 現況，逐段核實。
#      B3 段：全部 delete／replace opcode 嘅舊行必須落喺已知 B3 改動區（界外只准空行）；
#      全部 insert 嘅落點必須喺已知 B3 改動區附近。
#   2. 釘行以 B1／B2 腳本同一組 PINS（95baf7e 行號）起步，經三段映射推到 B3 行號；
#      全部釘行舊新內容逐字相同＝純漂移先改行號。落喺已刪區嘅釘會喺呢度斷言失敗，
#      嗰啲測試要做內容修復，唔係 resync。
# 改動範圍：tests/ 下面 8 檔（kwan151／gift185／rom176／tang152／tang171／tang173／
#   text125／travel114 釘行＋總行數；其餘靜態測試嘅內容失敗唔係 resync，另行處理）。
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = '--check' in sys.argv
BASE95_REF = '95baf7e'
BASEB1_REF = '9afc402'
BASEB2_REF = 'd7c0e2f'

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

old95 = load_ref(BASE95_REF)
mid1 = load_ref(BASEB1_REF)
mid2 = load_ref(BASEB2_REF)
new = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print('95baf7e 行數 %d（split）／B1 %d／B2 %d／現況 %d；\\n 數 %d／%d／%d／%d'
      % (len(old95), len(mid1), len(mid2), len(new),
         len(old95) - 1, len(mid1) - 1, len(mid2) - 1, len(new) - 1))
assert len(old95) - 1 == 63004, '95baf7e 總行數唔係 63004'
assert len(mid1) - 1 == 63045, 'B1 總行數唔係 63045'
assert len(mid2) - 1 == 63093, 'B2 總行數唔係 63093'
assert len(new) - 1 == 47481, '現況總行數唔係 47481（B3 淨 −15612）'

shift95, _, _ = build_shift(old95, mid1)
shiftB1, _, _ = build_shift(mid1, mid2)
shiftB2, opsB3, deletesB3 = build_shift(mid2, new, allow_delete=True)
print('B3 difflib：%d 舊行有對位；opcodes %d 段（delete %d 段，刪 %d 行）'
      % (len(shiftB2), len(opsB3),
         sum(1 for t, _, _, _, _ in opsB3 if t == 'delete'),
         sum(b - a + 1 for a, b in deletesB3)))

# B3 全部非 equal 段必須落喺已知改動區（B2 行號計）；界外只准空行
KNOWN_B3 = [(6371, 19820), (19880, 19895), (33440, 33470), (30700, 30800),
            (31430, 31440), (31645, 31655), (31810, 31965), (32705, 33015),
            (33150, 33405), (37015, 37025), (40125, 40405), (42225, 42625),
            (42940, 43615), (44000, 44080), (45000, 45010), (46765, 46775), (47975, 47985),
            (48055, 48065), (49165, 49175), (49250, 49265), (51080, 51555), (54980, 55005),
            (55235, 55250), (58265, 58335), (58510, 59100), (59110, 59440),
            (60090, 60680), (61260, 61280), (61405, 61425), (31580, 31585),
            (19280, 19300)]
def in_known(n):
    return any(a <= n <= b for a, b in KNOWN_B3)
for tag, i1, i2, j1, j2 in opsB3:
    if tag in ('delete', 'replace'):
        bad = [n for n in range(i1 + 1, i2 + 1)
               if not in_known(n) and mid2[n - 1].strip() != '']
        assert not bad, 'B3 %s 段有舊行落喺已知區之外：舊 L%d-%d，界外行 %s' % (
            tag, i1 + 1, i2, bad[:5])
    elif tag == 'insert':
        anchor = i1 + 1  # 插入點前面嗰行（B2 行號）
        assert any(a - 2 <= anchor <= b + 2 for a, b in KNOWN_B3), \
            'B3 insert 落點喺未知區：B2 L%d 附近，新 L%d-%d' % (anchor, j1 + 1, j2)
print('B3 非 equal 段全部落喺已知改動區（界外只得空行；insert 落點全部喺已知區附近）')

def mapline95(n):
    m1 = shift95.get(n)
    assert m1 is not None, '95baf7e L%d 無對位去 B1' % n
    m2 = shiftB1.get(m1)
    assert m2 is not None, 'B1 L%d 無對位去 B2' % m1
    m3 = shiftB2.get(m2)
    assert m3 is not None, 'B2 L%d 無對位去 B3（可能落喺已刪區）' % m2
    return m3

def maplineB1(n):
    m = shiftB1.get(n)
    assert m is not None, 'B1 L%d 無對位去 B2' % n
    m3 = shiftB2.get(m)
    assert m3 is not None, 'B2 L%d 無對位去 B3（可能落喺已刪區）' % m
    return m3

def maplineB2(n):
    m = shiftB2.get(n)
    assert m is not None, 'B2 L%d 無對位去 B3（可能落喺已刪區）' % n
    return m

FALLBACK125 = '(typeof b.text === "string" && b.text ? [b.text] : [])'
# ---- PINS（同 B1／B2 腳本一樣，95baf7e 行號） ----
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
# travel114：FREE／COUNT 全部釘行（由測試檔讀出嚟，B2 行號，唔用人手抄）
t114 = (ROOT / 'tests/test_travel114_static.py').read_text(encoding='utf-8')
def _setnums(name):
    m = re.search(name + r' = \{(.*?)\n\}', t114, re.S)
    return [int(x) for x in re.findall(r'^\s*(\d+),', m.group(1), re.M)]
FREE_B2 = _setnums('FREE_LINES'); COUNT_B2 = _setnums('COUNT_LINES')
for ln in FREE_B2 + COUNT_B2:
    PINS['tests/test_travel114_static.py'].append((ln, 'openLoc('))
FREE_FLAGS = ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')

n_checked = 0
for fname, pins in PINS.items():
    for ln, anchor in pins:
        if fname == 'tests/test_travel114_static.py' and ln in FREE_B2 + COUNT_B2:
            b2 = ln
            nl = maplineB2(b2)
            assert mid2[b2 - 1] == new[nl - 1], \
                '%s B2 L%d ≠ B3 L%d：\n舊：%s\n新：%s' % (fname, b2, nl, mid2[b2 - 1][:120], new[nl - 1][:120])
            assert anchor in mid2[b2 - 1], '%s B2 L%d 冇錨 %r：%s' % (fname, b2, anchor, mid2[b2 - 1][:120])
        else:
            nl = mapline95(ln)
            b2 = shiftB1[shift95[ln]]
            assert mid2[b2 - 1] == new[nl - 1], \
                '%s 95baf7e L%d (B2 L%d) ≠ B3 L%d：\n舊：%s\n新：%s' % (fname, ln, b2, nl, mid2[b2 - 1][:120], new[nl - 1][:120])
            assert anchor in mid2[b2 - 1], '%s B2 L%d 冇錨 %r：%s' % (fname, b2, anchor, mid2[b2 - 1][:120])
        n_checked += 1
print('釘行逐字核實：%d 項全部 B2→B3 內容相同（含 travel114 FREE %d＋COUNT %d＋DEF／WRAPPER）'
      % (n_checked, len(FREE_B2), len(COUNT_B2)))
# travel114 額外語義核實：FREE 行 B2 內容帶旗、COUNT 行 B2 內容冇旗
for ln in FREE_B2:
    assert any(f in mid2[ln - 1] for f in FREE_FLAGS), 'FREE B2 L%d 唔帶旗：%s' % (ln, mid2[ln - 1][:100])
for ln in COUNT_B2:
    assert not any(f in mid2[ln - 1] for f in FREE_FLAGS), 'COUNT B2 L%d 帶旗：%s' % (ln, mid2[ln - 1][:100])
print('travel114 語義核實：FREE %d 行全部帶旗、COUNT %d 行全部冇旗' % (len(FREE_B2), len(COUNT_B2)))

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
    print('改 %s：加 B3 resync 註解 1 行' % path)

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

NEW_TOTAL = 47481
NEW_DEF = maplineB2(57477)
NEW_WRAP = maplineB2(45591)
print('新總行數 %d、新 DEF %d、新 WRAPPER %d' % (NEW_TOTAL, NEW_DEF, NEW_WRAP))
# DEF／WRAPPER 都喺 B3 刪區之後（ENTRY 13731 行刪區喺佢哋之前），行號會大移位，
# 以 difflib 映射為準，唔預設數值。

# 全檔 1-based 映射（B2→B3），供各檔查表
MAP_B2 = {b2: maplineB2(b2) for b2 in sorted(shiftB2.keys())}
# 測試檔入面而家係 B2 行號：映射 key 一律用 B2 數（shift95／shiftB1 推算），值係 B3 數。
def b2key(n95):
    return shiftB1[shift95[n95]]
_k = lambda n: mapline95(n)

# kwan151：13 粒 line() 釘（名入面嘅 L25608 等歷史標籤唔郁；只改 line(N) 查嘅行號）
kw_map = {b2key(n): _k(n) for n in [25943, 26284, 26332, 26551, 26289, 26287, 26288,
                             31404, 31394, 27585, 31446, 31403, 27552]}
resync_numbers('tests/test_kwan151_static.py', re.compile(r'line\((\d+)\)'), kw_map)
append_comment_after('tests/test_kwan151_static.py',
    '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py）；13 個釘行全部喺首個改動點（舊 L31637）之前，行號唔郁（difflib 對位核實純漂移）。',
    '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py）；13 個釘行全部喺首個刪區（ENTRY L6371）之前，行號唔郁（difflib 對位核實純漂移）。')

# gift185：總行數
replace_once('tests/test_gift185_static.py',
    '總行數 63093（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48）',
    '總行數 47481（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612）')
replace_once('tests/test_gift185_static.py', "html.count('\\n') == 63093", "html.count('\\n') == 47481")
append_comment_after('tests/test_gift185_static.py',
    '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py），總行數 63045→63093（difflib 對位核實純漂移）。',
    '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py），總行數 63093→47481（difflib 對位核實純漂移）。')

# rom176：釘行（L31712／L6152 等名係歷史標籤，唔郁；只改 line(N) 查嘅行號）
rom_map = {b2key(n): _k(n) for n in [6360, 31868, 55829, 56197, 57336, 57430]}
resync_numbers('tests/test_rom176_static.py', re.compile(r'line\((\d+)\)'), rom_map)
append_comment_after('tests/test_rom176_static.py',
    '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py）；釘行按 difflib 映射重寫（31875→%d、55870→%d、56238→%d、57377→%d、57471→%d；6360 唔郁），difflib 對位核實純漂移。' % (
        b2key(31868), b2key(55829), b2key(56197), b2key(57336), b2key(57430)),
    '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py）；釘行按 difflib 映射重寫（31868→%d、55829→%d、56197→%d、57336→%d、57430→%d；6360 唔郁），difflib 對位核實純漂移。' % (
        _k(31868), _k(55829), _k(56197), _k(57336), _k(57430)))

# tang152：0-based index（標籤 L25817／L31610／L31754 係歷史名，唔郁）
tang_map = {b2key(n): _k(n) for n in [26103, 31793, 31939]}
resync_numbers('tests/test_tang152_static.py', re.compile(r'lines\(\)\[(\d+)\]'), tang_map, zero_based=True)
append_comment_after('tests/test_tang152_static.py',
    '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py）；HELD 26104 唔郁、normaliseTangStub152 31799→%d、stub 呼叫行 31966→%d（difflib 對位核實純漂移）。' % (b2key(31793), b2key(31939)),
    '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py）；HELD 26104→%d、normaliseTangStub152 %d→%d、stub 呼叫行 %d→%d（difflib 對位核實純漂移）。' % (
        _k(26103), b2key(31793), _k(31793), b2key(31939), _k(31939)))

# tang171／tang173：總行數＋openLoc DEF 行
for fname in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    replace_once(fname,
        '總行數 63093（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48）',
        '總行數 47481（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612）')
    replace_once(fname, "src.count('\\n') == 63093", "src.count('\\n') == 47481")
    replace_once(fname, 'openLoc DEF 行 57477', 'openLoc DEF 行 %d' % NEW_DEF)
    replace_once(fname, '＋v228 −170＋v229 +41＋v229 B2 +48，travel114 釘行', '＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612，travel114 釘行')
    replace_once(fname, 'len(lines) >= 57477', 'len(lines) >= %d' % NEW_DEF)
    replace_once(fname, 'lines[57476]', 'lines[%d]' % (NEW_DEF - 1))
    append_comment_after(fname,
        '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py），總行數 63045→63093、DEF 57440→57477（difflib 對位核實純漂移）。',
        '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py），總行數 63093→47481、DEF 57477→%d（difflib 對位核實純漂移）。' % NEW_DEF)

# text125：三錨點 ls[] index＋「第 N 行」訊息（len() 下限守衛仍然成立，唔郁）
t125_map = {b2key(n): _k(n) for n in [28077, 28214, 33849]}
resync_numbers('tests/test_text125_static.py', re.compile(r'ls\[(\d+)\]'), t125_map, zero_based=True)
resync_numbers('tests/test_text125_static.py', re.compile(r'第 (\d+) 行'), t125_map)
replace_once('tests/test_text125_static.py',
    '；v20a229 resync：33849→33890（淨 +41，difflib 對位核實純漂移，見 qa229/resync229.py）。；v20a229 B2 resync：33890→%d（淨 +48，difflib 對位核實純漂移，見 qa229/resync229_b2.py）。' % b2key(33849),
    '；v20a229 resync：33849→33890（淨 +41，difflib 對位核實純漂移，見 qa229/resync229.py）。；v20a229 B2 resync：33890→%d（淨 +48，difflib 對位核實純漂移，見 qa229/resync229_b2.py）。；v20a229 B3 resync：%d→%d（淨 −15612，difflib 對位核實純漂移，見 qa229/resync229_b3.py）。' % (b2key(33849), b2key(33849), _k(33849)))

# travel114：FREE／COUNT set＋DEF／WRAPPER
PINMAP = {ln: maplineB2(ln) for ln in FREE_B2 + COUNT_B2}
resync_region('tests/test_travel114_static.py', 'FREE_LINES', PINMAP)
resync_region('tests/test_travel114_static.py', 'COUNT_LINES', PINMAP)
replace_once('tests/test_travel114_static.py', 'DEF_LINE = 57477', 'DEF_LINE = %d' % NEW_DEF)
replace_once('tests/test_travel114_static.py', 'WRAPPER_LINE = 45591', 'WRAPPER_LINE = %d' % NEW_WRAP)
append_comment_after('tests/test_travel114_static.py',
    '# v20a229 B2 resync：index.html 淨 +48 行（真五級引擎，見 qa229/resync229_b2.py）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 57440→57477、WRAPPER 45554→45591），核實純漂移。',
    '# v20a229 B3 resync：index.html 淨 −15612 行（換庫，見 qa229/resync229_b3.py）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 57477→%d、WRAPPER 45591→%d），核實純漂移。' % (NEW_DEF, NEW_WRAP))

print('全部寫檔完成')
