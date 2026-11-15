#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v20a229 B5 resync：index.html 淨 +250 行（觸發系統＋BR89 擴充＋獎項級紀錄＋D-14 改源＋rival 次序修正＋板面過濾＋引薦／邀約標籤）。
# 用法：python3 qa229/resync229_b5.py [--check]   （--check 只核實，唔寫檔）
# 做法（跟每版慣例，唔好人手估行號）：
#   1. 單段 difflib 對位：B4（HEAD）→ 現況，逐段核實。
#      全部 delete／replace opcode 嘅舊行必須落喺已知 B5 改動區（界外只准空行）；
#      全部 insert 嘅落點必須喺已知 B5 改動區附近。B5 得 insert＋replace，唔應該有 delete。
#   2. 釘行以測試檔而家嘅 B4 行號起步，經映射推到 B5 行號；
#      全部釘行舊新內容逐字相同＝純漂移先改行號。
# 改動範圍：tests/ 下面 7 檔（kwan151／gift185／rom176／tang152／tang171／tang173／
#   text125／travel114 釘行＋總行數；nat92 E2 唔係釘行，係沙盒未抽 triggerGigOn＋MAXED 未觸發，
#   另行修 tests/test_nat92_logic.js，唔喺呢度處理）。
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = '--check' in sys.argv
BASE_REF = 'HEAD'  # v20a229 B4

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

old = load_ref(BASE_REF)
new = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print('B4 行數 %d（split）／現況 %d；\\n 數 %d／%d'
      % (len(old), len(new), len(old) - 1, len(new) - 1))
assert len(old) - 1 == 47584, 'B4 總行數唔係 47584'
assert len(new) - 1 == 47834, '現況總行數唔係 47834（B5 淨 +250）'

shiftB4, opsB5, deletesB5 = build_shift(old, new)
print('B5 difflib：%d 舊行有對位；opcodes %d 段（delete %d 段）'
      % (len(shiftB4), len(opsB5),
         sum(1 for t, _, _, _, _ in opsB5 if t == 'delete')))

def find_b4(needle, start=1):
    for i in range(start - 1, len(old)):
        if needle in old[i]:
            return i + 1
    raise SystemExit('B4 搵唔到錨：%r' % needle)

# B5 已知改動區（B4 行號計；由錨字串定位，唔用人手抄行號）
A_SDEFAULT = find_b4('awardsFlags:{},')                       # S 預設 awardsResults（＋4：註解 3＋屬性 1）
A_GIGCARD = find_b4('function gigCardHtml(g, opts){')         # 詳情卡引薦／邀約標籤（＋3）
A_TEASER = find_b4('function gigBoardTeaserHtml(g, opts){')   # 短卡引薦／邀約標籤（＋4）
A_INTEL_CMT = find_b4('v20a229 B3：隱藏通告內容已刪')          # D-14 註解（＋4）
A_INTEL_FN = find_b4('function mergeIntelGigs(){')            # D-14 改源 T2（＋3）
A_FAVOR = find_b4('const FAVOR_DUE_CFG')                      # FAVOR_DUE 註解（0 行，replace）
A_RIVALCFG = find_b4('const RIVAL_CFG = ')                    # RIVAL_CFG gigId＋rivalryGigForRound（＋12）
A_TICK = find_b4('function rivalryTick(){')                   # 次序修正（＋3）
A_NEWSTICK = find_b4('function rivalryNewsTick')              # 註解（＋2）
A_BR89MAP = find_b4('const BR89_PATRON_OF_GIG')               # BR89 映射 4→13＋br89GigOn R-4 OR（＋23）
A_BRONCOMPLETE = find_b4('function br89OnGigComplete(gigId){')# 兌現標題反查＋其後通用 trigger block 插入（＋154）
A_INTEL_USE = find_b4('情報卡使用點', A_BRONCOMPLETE)          # trigger block 插入點之後嗰行註解
A_AWARDS = find_b4('function ensureAwardsFlags(){')           # ensureAwardsResults＋recordAwardResult（＋28）
A_COMMIT = find_b4('function commitAwardToLog(pack){')        # 呼叫 recordAwardResult（＋3）
A_BOARD = find_b4('function gigsForLocSeasonBoard(locId, curSeason){')  # mergeTriggerGigs＋過濾＋NAT92 保底（＋7）
KNOWN_B5 = [(A_SDEFAULT - 2, A_SDEFAULT + 7),
            (A_GIGCARD - 1, A_GIGCARD + 100),
            (A_TEASER - 1, A_TEASER + 60),
            (A_INTEL_CMT - 3, A_INTEL_CMT + 5),
            (A_INTEL_FN - 1, A_INTEL_FN + 10),
            (A_FAVOR - 4, A_FAVOR + 4),
            (A_RIVALCFG - 12, A_RIVALCFG + 28),
            (A_TICK - 1, A_TICK + 22),
            (A_NEWSTICK - 1, A_NEWSTICK + 30),
            (A_BR89MAP - 2, A_INTEL_USE + 8),
            (A_AWARDS - 2, A_AWARDS + 35),
            (A_COMMIT - 1, A_COMMIT + 30),
            (A_BOARD - 1, A_BOARD + 35)]
print('B5 已知改動區（B4 行號）：%s' % (KNOWN_B5,))
def in_known(n):
    return any(a <= n <= b for a, b in KNOWN_B5)
for tag, i1, i2, j1, j2 in opsB5:
    if tag in ('delete', 'replace'):
        bad = [n for n in range(i1 + 1, i2 + 1)
               if not in_known(n) and old[n - 1].strip() != '']
        assert not bad, 'B5 %s 段有舊行落喺已知區之外：舊 L%d-%d，界外行 %s' % (
            tag, i1 + 1, i2, bad[:5])
    elif tag == 'insert':
        anchor = i1 + 1  # 插入點前面嗰行（B4 行號）
        assert any(a - 2 <= anchor <= b + 2 for a, b in KNOWN_B5), \
            'B5 insert 落點喺未知區：B4 L%d 附近，新 L%d-%d' % (anchor, j1 + 1, j2)
print('B5 非 equal 段全部落喺已知改動區（界外只得空行；insert 落點全部喺已知區附近）')

def maplineB4(n):
    m = shiftB4.get(n)
    assert m is not None, 'B4 L%d 無對位去 B5' % n
    return m

# ---- PINS（測試檔而家嘅 B4 行號） ----
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
FREE_B4 = _setnums('FREE_LINES'); COUNT_B4 = _setnums('COUNT_LINES')
FREE_FLAGS = ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')
DEF_B4 = 43049; WRAP_B4 = 31141

n_checked = 0
for ln in KWAN_PINS + ROM_PINS:
    nl = maplineB4(ln)
    assert old[ln - 1] == new[nl - 1], 'B4 L%d ≠ B5 L%d：\n舊：%s\n新：%s' % (ln, nl, old[ln - 1][:120], new[nl - 1][:120])
    n_checked += 1
for ln in TANG_PINS + T125_LS:
    nl = maplineB4(ln + 1)  # 0-based index → 1-based 行號
    assert old[ln] == new[nl - 1], 'B4 L%d (0-based %d) ≠ B5 L%d' % (ln + 1, ln, nl)
    n_checked += 1
for ln in T125_MSG:
    nl = maplineB4(ln)
    assert old[ln - 1] == new[nl - 1], 'text125 B4 L%d ≠ B5 L%d' % (ln, nl)
    n_checked += 1
for ln in FREE_B4 + COUNT_B4 + [DEF_B4, WRAP_B4]:
    nl = maplineB4(ln)
    assert old[ln - 1] == new[nl - 1], 'travel114 B4 L%d ≠ B5 L%d' % (ln, nl)
    n_checked += 1
print('釘行逐字核實：%d 項全部 B4→B5 內容相同（kwan %d／rom %d／tang152 %d／text125 %d／travel114 FREE %d＋COUNT %d＋DEF／WRAPPER）'
      % (n_checked, len(KWAN_PINS), len(ROM_PINS), len(TANG_PINS),
         len(T125_LS) + len(T125_MSG), len(FREE_B4), len(COUNT_B4)))
for ln in FREE_B4:
    assert any(f in old[ln - 1] for f in FREE_FLAGS), 'FREE B4 L%d 唔帶旗：%s' % (ln, old[ln - 1][:100])
for ln in COUNT_B4:
    assert not any(f in old[ln - 1] for f in FREE_FLAGS), 'COUNT B4 L%d 帶旗：%s' % (ln, old[ln - 1][:100])
print('travel114 語義核實：FREE %d 行全部帶旗、COUNT %d 行全部冇旗' % (len(FREE_B4), len(COUNT_B4)))

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
    print('改 %s：加 B5 resync 註解 1 行' % path)

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

NEW_TOTAL = 47834
NEW_DEF = maplineB4(DEF_B4)
NEW_WRAP = maplineB4(WRAP_B4)
print('新總行數 %d、新 DEF %d（＋%d）、新 WRAPPER %d（＋%d）' % (NEW_TOTAL, NEW_DEF, NEW_DEF - DEF_B4, NEW_WRAP, NEW_WRAP - WRAP_B4))
MAP_B4 = {b4: maplineB4(b4) for b4 in sorted(shiftB4.keys())}
_k = lambda n: maplineB4(n)

# kwan151：line(N) 釘（全部喺首個 B5 插入點 19849 之前，應唔郁）
kw_map = {n: _k(n) for n in KWAN_PINS}
resync_numbers('tests/test_kwan151_static.py', re.compile(r'line\((\d+)\)'), kw_map)
append_comment_after('tests/test_kwan151_static.py',
    '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py）；13 個釘行按 difflib 映射重寫（17959→18028、17968→18037、17969→18038、18011→18080），difflib 對位核實純漂移。',
    '# v20a229 B5 resync：index.html 淨 +250 行（觸發系統＋BR89 擴充，見 qa229/resync229_b5.py）；13 個釘行全部喺首個 B5 插入點（S 預設 awardsResults，B4 L19849）之前，行號唔郁（difflib 對位核實純漂移）。')

# gift185：總行數
replace_once('tests/test_gift185_static.py',
    '總行數 47584（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612＋v229 B4 +103）',
    '總行數 47834（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612＋v229 B4 +103＋v229 B5 +250）')
replace_once('tests/test_gift185_static.py', "html.count('\\n') == 47584", "html.count('\\n') == 47834")
append_comment_after('tests/test_gift185_static.py',
    '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py），總行數 47481→47584（difflib 對位核實純漂移）。',
    '# v20a229 B5 resync：index.html 淨 +250 行（觸發系統＋BR89 擴充，見 qa229/resync229_b5.py），總行數 47584→47834（difflib 對位核實純漂移）。')

# rom176：line(N) 釘
rom_map = {n: _k(n) for n in ROM_PINS}
resync_numbers('tests/test_rom176_static.py', re.compile(r'line\((\d+)\)'), rom_map)
append_comment_after('tests/test_rom176_static.py',
    '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py）；釘行按 difflib 映射重寫（18430→18499、41377→41479、41745→41847、42884→42986、42978→43080；6360 唔郁），difflib 對位核實純漂移。',
    '# v20a229 B5 resync：index.html 淨 +250 行（觸發系統＋BR89 擴充，見 qa229/resync229_b5.py）；釘行按 difflib 映射重寫（%s；6360 唔郁），difflib 對位核實純漂移。' % (
        '、'.join('%d→%d' % (n, _k(n)) for n in ROM_PINS if n != 6360)))

# tang152：0-based index（全部喺首個 B5 插入點之前，應唔郁）
tang_map = {n: _k(n) for n in [x + 1 for x in TANG_PINS]}
resync_numbers('tests/test_tang152_static.py', re.compile(r'lines\(\)\[(\d+)\]'), tang_map, zero_based=True)
append_comment_after('tests/test_tang152_static.py',
    '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py）；HELD 12667→12666、normaliseTangStub152 18359→18427、stub 呼叫行 18486→18554（difflib 對位核實純漂移）。',
    '# v20a229 B5 resync：index.html 淨 +250 行（觸發系統＋BR89 擴充，見 qa229/resync229_b5.py）；3 個釘行全部喺首個 B5 插入點（S 預設 awardsResults，B4 L19849）之前，行號唔郁（difflib 對位核實純漂移）。')

# tang171／tang173：總行數＋openLoc DEF 行
for fname in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    replace_once(fname,
        '總行數 47584（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612＋v229 B4 +103）',
        '總行數 47834（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263＋v217 +3＋v218 +136＋v219 +3＋v222 −37＋v225 +272＋v227 +2＋v210 +40＋v228 −170＋v229 +41＋v229 B2 +48＋v229 B3 −15612＋v229 B4 +103＋v229 B5 +250）')
    replace_once(fname, "src.count('\\n') == 47584", "src.count('\\n') == 47834")
    replace_once(fname, 'openLoc DEF 行 43049', 'openLoc DEF 行 %d' % NEW_DEF)
    replace_once(fname, '＋v229 B3 −15612＋v229 B4 +103，travel114 釘行', '＋v229 B3 −15612＋v229 B4 +103＋v229 B5 +%d，travel114 釘行' % (NEW_DEF - DEF_B4))
    replace_once(fname, 'len(lines) >= 43049', 'len(lines) >= %d' % NEW_DEF)
    replace_once(fname, 'lines[43048]', 'lines[%d]' % (NEW_DEF - 1))
    append_comment_after(fname,
        '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py），總行數 47481→47584、DEF 42947→43049（difflib 對位核實純漂移）。',
        '# v20a229 B5 resync：index.html 淨 +250 行（觸發系統＋BR89 擴充，見 qa229/resync229_b5.py），總行數 47584→47834、DEF 43049→%d（difflib 對位核實純漂移）。' % NEW_DEF)

# text125：ls[] index＋「第 N 行」訊息
t125_map = {n: _k(n) for n in [x + 1 for x in T125_LS] + T125_MSG}
resync_numbers('tests/test_text125_static.py', re.compile(r'ls\[(\d+)\]'), t125_map, zero_based=True)
resync_numbers('tests/test_text125_static.py', re.compile(r'第 (\d+) 行'), t125_map)
replace_once('tests/test_text125_static.py',
    '；v20a229 B4 resync：20067→20142（淨 +103，difflib 對位核實純漂移，見 qa229/resync229_b4.py）。',
    '；v20a229 B4 resync：20067→20142（淨 +103，difflib 對位核實純漂移，見 qa229/resync229_b4.py）。；v20a229 B5 resync：20142→%d（淨 +4，S 預設 awardsResults 註解 3＋屬性 1，difflib 對位核實純漂移，見 qa229/resync229_b5.py）。' % _k(20142))

# travel114：FREE／COUNT set＋DEF／WRAPPER
PINMAP = {ln: maplineB4(ln) for ln in FREE_B4 + COUNT_B4}
resync_region('tests/test_travel114_static.py', 'FREE_LINES', PINMAP)
resync_region('tests/test_travel114_static.py', 'COUNT_LINES', PINMAP)
replace_once('tests/test_travel114_static.py', 'DEF_LINE = 43049', 'DEF_LINE = %d' % NEW_DEF)
replace_once('tests/test_travel114_static.py', 'WRAPPER_LINE = 31141', 'WRAPPER_LINE = %d' % NEW_WRAP)
append_comment_after('tests/test_travel114_static.py',
    '# v20a229 B4 resync：index.html 淨 +103 行（提名計數＋LEAD229，見 qa229/resync229_b4.py）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 42947→43049、WRAPPER 31063→31141），核實純漂移。',
    '# v20a229 B5 resync：index.html 淨 +250 行（觸發系統＋BR89 擴充，見 qa229/resync229_b5.py）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 43049→%d、WRAPPER 31141→%d），核實純漂移。' % (NEW_DEF, NEW_WRAP))

print('全部寫檔完成')
