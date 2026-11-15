#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v20a229 B1 resync：index.html 淨 +41 行（新通告庫地基——STORY_WIRE gigsByYearNew ＋1／
#   syncGigsForCalendarYear 新庫優先 ＋5／loader gigs_new.json fetch＋分組 ＋22／
#   normalizeGigRecord 年份守衛 ＋8／days→shootDaysHint 映射 ＋6；舊行 0 刪，全部係
#   插入＋原地改值）。difflib 對位核實：全部釘行舊新內容逐字相同＝純漂移先改行號。
# 用法：python3 qa229/resync229.py [--check]   （--check 只核實，唔寫檔）
# 改動範圍：tests/ 下面 11 檔（kwan151／gift185／rom176／tang152／tang171／tang173／
#   text125／travel114 釘行＋總行數；aud91fix122／aud91fix124／newspaper214_award
#   加 v229 content 豁免 gigs_new.json）。
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = '--check' in sys.argv
BASE_REF = '95baf7e'

def load_old():
    out = subprocess.check_output(['git', 'show', BASE_REF + ':index.html'], cwd=str(ROOT), text=True)
    return out.split('\n')
old = load_old()
new = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print('舊行數 %d（split）／新行數 %d（split）；舊 \\n 數 %d／新 %d'
      % (len(old), len(new), len(old) - 1, len(new) - 1))
assert len(old) - 1 == 63004, '舊總行數唔係 63004'
assert len(new) - 1 == 63045, '新總行數唔係 63045'

# ---- 1. difflib 映射核實 ----
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
shift = {}
replaces = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            shift[i1 + k + 1] = j1 + k + 1
    elif tag == 'replace':
        # 原地改值（等長 1:1 優先；不等長先對齊前段，餘下舊行視作改寫，唔當刪除）
        for k in range(min(i2 - i1, j2 - j1)):
            shift[i1 + k + 1] = j1 + k + 1
        replaces.append((i1 + 1, i2, j1 + 1, j2))
    elif tag == 'insert':
        pass
    else:
        raise SystemExit('非預期 opcode（本批 0 刪行）：%s 舊 %d-%d 新 %d-%d' % (tag, i1 + 1, i2, j1 + 1, j2))
print('difflib 映射：%d 舊行有對位；replace 段 %d 區（原地改值／擴寫）' % (len(shift), len(replaces)))
for a, b, c, d in replaces:
    print('  舊 L%d-%d → 新 L%d-%d：%s' % (a, b, c, d, old[a - 1][:80]))
# 全部 replace 段必須落喺已知改動區（sync／loader／normalize 附近）
KNOWN = [(30715, 30745), (31831, 31845), (33258, 33262)]
for a, b, c, d in replaces:
    assert any(a >= lo and b <= hi for lo, hi in KNOWN), 'replace 段落喺未知區：舊 L%d-%d' % (a, b)
print('replace 段全部落喺已知改動區（sync／loader／normalize）')

def mapline(n):
    m = shift.get(n)
    assert m is not None, '舊 L%d 無對位（落喺 replace／delete 段）' % n
    return m

FALLBACK125 = '(typeof b.text === "string" && b.text ? [b.text] : [])'
# ---- 2. 逐項核實釘行舊新內容逐字相同 ----
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
# travel114：FREE／COUNT 全部釘行（由測試檔讀出嚟，唔用人手抄）
t114 = (ROOT / 'tests/test_travel114_static.py').read_text(encoding='utf-8')
def _setnums(name):
    m = re.search(name + r' = \{(.*?)\n\}', t114, re.S)
    return [int(x) for x in re.findall(r'^\s*(\d+),', m.group(1), re.M)]
FREE_OLD = _setnums('FREE_LINES'); COUNT_OLD = _setnums('COUNT_LINES')
for ln in FREE_OLD + COUNT_OLD:
    PINS['tests/test_travel114_static.py'].append((ln, 'openLoc('))
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

# ---- 3. 寫檔 ----
def apply_line_edits(path, edits):
    """edits：(1-based 行號，舊片段，新片段)；每舊片段喺該行必須恰好出現指定次數（預設 1）。"""
    p = ROOT / path
    lines = p.read_text(encoding='utf-8').split('\n')
    for ln, old_frag, new_frag, *rest in edits:
        cnt = rest[0] if rest else 1
        assert lines[ln - 1].count(old_frag) == cnt, \
            '%s L%d 舊片段出現 %d 次（要 %d 次）：%r' % (path, ln, lines[ln - 1].count(old_frag), cnt, old_frag[:80])
        lines[ln - 1] = lines[ln - 1].replace(old_frag, new_frag)
    p.write_text('\n'.join(lines), encoding='utf-8')
    print('改 %s：%d 處行內編輯' % (path, len(edits)))

def append_comment_after(path, anchor_frag, comment):
    p = ROOT / path
    txt = p.read_text(encoding='utf-8')
    assert txt.count(anchor_frag) == 1, '%s 錨出現 %d 次：%r' % (path, txt.count(anchor_frag), anchor_frag[:60])
    txt = txt.replace(anchor_frag, anchor_frag + '\n' + comment, 1)
    p.write_text(txt, encoding='utf-8')
    print('改 %s：加 v229 resync 註解 1 行' % path)

def insert_before_line(path, line_no, new_lines, must_contain):
    """喺指定行之前插入幾行（該行內容必須含 must_contain，防行號漂移誤插）。"""
    p = ROOT / path
    lines = p.read_text(encoding='utf-8').split('\n')
    assert must_contain in lines[line_no - 1], '%s L%d 內容唔符：%s' % (path, line_no, lines[line_no - 1][:80])
    lines[line_no - 1:line_no - 1] = new_lines
    p.write_text('\n'.join(lines), encoding='utf-8')
    print('改 %s：L%d 之前插入 %d 行' % (path, line_no, len(new_lines)))

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

V229_NOTE = '（新通告庫地基 B1：STORY_WIRE ＋1／sync 新庫優先 ＋5／loader ＋22／normalize ＋14；淨 +41）'
NEW_TOTAL = 63045
NEW_DEF = mapline(57399)
NEW_WRAP = mapline(45513)
print('新總行數 %d、新 DEF %d、新 WRAPPER %d' % (NEW_TOTAL, NEW_DEF, NEW_WRAP))

# kwan151：13 粒 line() 釘（名入面嘅 L25608 等歷史標籤唔郁；只改實際查嘅行號）
_k = lambda n: mapline(n)
apply_line_edits('tests/test_kwan151_static.py', [
    (54, 'line(25943)', 'line(%d)' % _k(25943), 2),
    (55, 'line(26284)', 'line(%d)' % _k(26284), 2),
    (56, 'line(26332)', 'line(%d)' % _k(26332), 2),
    (57, 'line(26551)', 'line(%d)' % _k(26551), 2),
    (61, 'line(26289)', 'line(%d)' % _k(26289)),
    (62, 'line(26287)', 'line(%d)' % _k(26287), 2),
    (63, 'line(26288)', 'line(%d)' % _k(26288)),
    (68, 'line(31404)', 'line(%d)' % _k(31404), 2),
    (71, 'line(31394)', 'line(%d)' % _k(31394)),
    (72, 'line(31394)', 'line(%d)' % _k(31394)),
    (73, 'line(31394)', 'line(%d)' % _k(31394)),
    (74, 'line(31394)', 'line(%d)' % _k(31394)),
    (77, 'line(27585)', 'line(%d)' % _k(27585)),
    (79, 'line(31446)', 'line(%d)' % _k(31446)),
    (80, 'line(31403)', 'line(%d)' % _k(31403), 2),
    (81, 'line(31403)', 'line(%d)' % _k(31403)),
    (99, 'line(27552)', 'line(%d)' % _k(27552)),
])
append_comment_after('tests/test_kwan151_static.py',
    '# v20a216 resync：index.html 淨 +263 行（見 qa216/resync216.py difflib 對位核實純漂移），13 個釘行按映射重寫（＋38，名入面嘅 L25608 等歷史標籤唔郁）。',
    '# v20a229 resync：index.html 淨 +41 行' + V229_NOTE + '；13 個釘行按 difflib 映射重寫（25xxx／27xxx 者 ＋1、31xxx 者 ＋6；名入面嘅 L25608 等歷史標籤唔郁），difflib 對位核實純漂移，見 qa229/resync229.py。')

# gift185：總行數
apply_line_edits('tests/test_gift185_static.py', [
    (62, '總行數 63004', '總行數 %d' % NEW_TOTAL),
    (62, '＋v228 −170）', '＋v228 −170＋v229 +41）'),
    (62, "html.count('\\n') == 63004", "html.count('\\n') == %d" % NEW_TOTAL),
])
append_comment_after('tests/test_gift185_static.py',
    '# v20a228 resync：index.html 淨 −170 行（拎走四個存檔遷移函數，見 qa228/delete228.py；刪除區間舊 L31647／31696–31735／31744–31797／32142／33783–33793／36706–36768），總行數 63174→63004（difflib 對位核實純漂移，見 qa228/resync228.py）。',
    '# v20a229 resync：index.html 淨 +41 行' + V229_NOTE + '，總行數 63004→63045（difflib 對位核實純漂移，見 qa229/resync229.py）。')

# rom176：釘行（L31712／L6152 等名係歷史標籤，唔郁；只改實際查嘅行號）
apply_line_edits('tests/test_rom176_static.py', [
    (83, 'line(31868)', 'line(%d)' % _k(31868), 2),
    (84, 'line(55829)', 'line(%d)' % _k(55829)),
    (85, 'line(56197)', 'line(%d)' % _k(56197)),
    (86, 'line(57336)', 'line(%d)' % _k(57336)),
    (87, 'line(57430)', 'line(%d)' % _k(57430)),
])
append_comment_after('tests/test_rom176_static.py',
    '# v20a228 resync：index.html 淨 −170 行（拎走四個存檔遷移函數，見 qa228/delete228.py；刪除區間舊 L31647／31696–31735／31744–31797／32142／33783–33793／36706–36768）；釘行按 difflib 映射重寫（31963→31868、55999→55829、56367→56197、57506→57336、57600→57430；6360 唔郁），difflib 對位核實純漂移，見 qa228/resync228.py。',
    '# v20a229 resync：index.html 淨 +41 行' + V229_NOTE + '；釘行按 difflib 映射重寫（31868→%d、55829→%d、56197→%d、57336→%d、57430→%d；6360 唔郁），difflib 對位核實純漂移，見 qa229/resync229.py。' % (_k(31868), _k(55829), _k(56197), _k(57336), _k(57430)))

# tang152：0-based index（標籤 L25817／L31610／L31754 係歷史名，唔郁）
apply_line_edits('tests/test_tang152_static.py', [
    (72, 'lines()[26102]', 'lines()[%d]' % (_k(26103) - 1)),
    (95, 'lines()[31792]', 'lines()[%d]' % (_k(31793) - 1)),
    (96, 'lines()[31938]', 'lines()[%d]' % (_k(31939) - 1)),
])
append_comment_after('tests/test_tang152_static.py',
    '# v20a228 resync：index.html 淨 −170 行（拎走四個存檔遷移函數，見 qa228/delete228.py；刪除區間舊 L31647／31696–31735／31744–31797／32142／33783–33793／36706–36768）；normaliseTangStub152 31888→31793、stub 呼叫行 32034→31939（difflib 對位核實純漂移，見 qa228/resync228.py）。',
    '# v20a229 resync：index.html 淨 +41 行' + V229_NOTE + '；HELD 26103→%d、normaliseTangStub152 31793→%d、stub 呼叫行 31939→%d（difflib 對位核實純漂移，見 qa229/resync229.py）。' % (_k(26103), _k(31793), _k(31939)))

# tang171／tang173：總行數＋openLoc DEF 行
for fname, tline, dline in (('tests/test_tang171_static.py', 102, 103),
                            ('tests/test_tang173_static.py', 99, 100)):
    apply_line_edits(fname, [
        (tline, '總行數 63004', '總行數 %d' % NEW_TOTAL),
        (tline, '＋v228 −170）', '＋v228 −170＋v229 +41）'),
        (tline, "src.count('\\n') == 63004", "src.count('\\n') == %d" % NEW_TOTAL),
        (dline, 'openLoc DEF 行 57399', 'openLoc DEF 行 %d' % NEW_DEF),
        (dline, '＋v228 −170，travel114 釘行', '＋v228 −170＋v229 +41，travel114 釘行'),
        (dline + 1, 'len(lines) >= 57399', 'len(lines) >= %d' % NEW_DEF),
        (dline + 1, 'lines[57398]', 'lines[%d]' % (NEW_DEF - 1)),
    ])
    append_comment_after(fname,
        '# v20a228 resync：index.html 淨 −170 行（拎走四個存檔遷移函數，見 qa228/delete228.py；刪除區間舊 L31647／31696–31735／31744–31797／32142／33783–33793／36706–36768），總行數 63174→63004、DEF 57569→57399（difflib 對位核實純漂移，見 qa228/resync228.py）。',
        '# v20a229 resync：index.html 淨 +41 行' + V229_NOTE + '，總行數 63004→63045、DEF 57399→%d（difflib 對位核實純漂移，見 qa229/resync229.py）。' % NEW_DEF)

# text125：三錨點 ls[] index＋「第 N 行」訊息（len() 下限守衛仍然成立，唔郁）
_c = mapline(28077); _a = mapline(28214); _f = mapline(33849)
apply_line_edits('tests/test_text125_static.py', [
    (54, 'ls[28076]', 'ls[%d]' % (_c - 1)),
    (55, '第 28077 行冇 text fallback', '第 %d 行冇 text fallback' % _c),
    (60, 'ls[28213]', 'ls[%d]' % (_a - 1)),
    (61, '第 28214 行冇 text fallback', '第 %d 行冇 text fallback' % _a),
    (63, 'ls[33848]', 'ls[%d]' % (_f - 1)),
    (64, '第 33849 行冇 b.text 分支', '第 %d 行冇 b.text 分支' % _f),
    (64, '唔影響）', '唔影響）；v20a229 resync：%d→%d（淨 +41，difflib 對位核實純漂移，見 qa229/resync229.py）。' % (33849, _f)),
])

# travel114：FREE／COUNT set＋DEF／WRAPPER
PINMAP = {ln: mapline(ln) for ln in FREE_OLD + COUNT_OLD}
resync_region('tests/test_travel114_static.py', 'FREE_LINES', PINMAP)
resync_region('tests/test_travel114_static.py', 'COUNT_LINES', PINMAP)
apply_line_edits('tests/test_travel114_static.py', [
    (215, 'DEF_LINE = 57399', 'DEF_LINE = %d' % NEW_DEF),
    (216, 'WRAPPER_LINE = 45513', 'WRAPPER_LINE = %d' % NEW_WRAP),
])
append_comment_after('tests/test_travel114_static.py',
    '# v20a228 resync：index.html 淨 −170 行（拎走四個存檔遷移函數，見 qa228/delete228.py；刪除區間舊 L31647／31696–31735／31744–31797／32142／33783–33793／36706–36768）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 57569→57399、WRAPPER 45683→45513），核實純漂移。',
    '# v20a229 resync：index.html 淨 +41 行' + V229_NOTE + '；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 57399→%d、WRAPPER 45513→%d），核實純漂移。' % (NEW_DEF, NEW_WRAP))

# content 豁免：v229 新增 content/gigs_new.json 一檔（240 張新庫，B1 已拍板有意新增）
V229_DEF = [
    '    # v229 豁免（新通告庫 B1，已拍板）：新增 content/gigs_new.json 一檔（240 張新庫，顯示年直寫；舊 pack 唔郁）。',
    "    _v229_allowed = {'content/gigs_new.json'}",
]
for fname, ok_line, union_old, union_new, msg_old, msg_new in (
    ('tests/test_aud91fix122_static.py', 77,
     'all(p in _v157_allowed | _v217_allowed | _v218_allowed | _v210_allowed',
     'all(p in _v157_allowed | _v217_allowed | _v218_allowed | _v210_allowed | _v229_allowed',
     '（v157＋v217＋v218＋v210 豁免以外一律唔准郁）', '（v157＋v217＋v218＋v210＋v229 豁免以外一律唔准郁）'),
    ('tests/test_aud91fix124_static.py', 78,
     'all(p in _v157_allowed | _v217_allowed | _v218_allowed | _v210_allowed',
     'all(p in _v157_allowed | _v217_allowed | _v218_allowed | _v210_allowed | _v229_allowed',
     '（v157＋v217＋v218＋v210 豁免以外一律唔准郁）', '（v157＋v217＋v218＋v210＋v229 豁免以外一律唔准郁）'),
):
    insert_before_line(fname, ok_line, V229_DEF, "ok('content pack JSON")
    apply_line_edits(fname, [
        (ok_line + 2, msg_old, msg_new),
        (ok_line + 3, union_old, union_new),
    ])
# newspaper214：X05 用 l[3:]，豁免集係 _v217｜_v210
insert_before_line('tests/test_newspaper214_award_static.py', 189,
    ['    # v229 豁免（新通告庫 B1，已拍板）：新增 content/gigs_new.json 一檔（240 張新庫，顯示年直寫；舊 pack 唔郁）。',
     "    _v229_allowed = {'content/gigs_new.json'}"],
    "ok('X05_content_json_untouched'")
apply_line_edits('tests/test_newspaper214_award_static.py', [
    (191, 'all(l[3:] in _v217_allowed | _v210_allowed for l in touched)',
     'all(l[3:] in _v217_allowed | _v210_allowed | _v229_allowed for l in touched)'),
])

print('全部寫檔完成')
