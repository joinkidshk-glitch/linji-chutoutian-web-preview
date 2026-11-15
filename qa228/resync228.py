#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v20a228 resync：index.html 淨 -170 行（拎走四個存檔遷移函數，見 qa228/delete228.py）。
# 實際刪除區間（舊行號，difflib 對位核實；delete228.py 報告嘅行號係 0-based
#   切片口徑，比實際 1-based 區間各偏 −1——內容一樣，只係邊界 `}`／空行
#   撞款令 difflib 將邊界認做另一邊嘅相同行，結果檔案內容無分別）：
#   L31647 單行（YEARS66 頭行註解刪一行）／L31696-31735
#   years66MigrateSave 40 行／L31744-31797 jan67MigrateSave 機械 54 行／
#   L32142 LEVELS75_MID_OF 單行／L33783-33793 normalizeSaveObj 呼叫點 11 行／
#   L36706-36768 levels75MigrateSave 27 行＋c2n210MigrateSave 36 行。
# 另有 6 處原地改值（行數不變）：YEARS66 頭行、JAN67 頭行、COURSE_DEFS 註解、
#   LEVELS75 註解、fresh() 兩印註解。difflib 對位核實：被刪行集合必須恰好係
#   上述 170 行；其餘舊行按分段映射（<=31646 不變／31648-31695 -1／
#   31736-31743 -41／31798-32141 -95／32143-33782 -96／33794-36705 -107／
#   >=36769 -170），內容逐字相同（原地改值行除外）。
# 用法：python3 qa228/resync228.py [--check]   （--check 只核實，唔寫檔）
# 改動範圍：只改 tests/ 下面 7 檔（gift185／rom176／tang152／tang171／tang173／
#   text125／travel114）。
import difflib, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = '--check' in sys.argv

def load_old():
    out = subprocess.check_output(['git', 'show', 'a58c0b9:index.html'], cwd=str(ROOT), text=True)
    return out.split('\n')
old = load_old()
new = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print('舊行數 %d（split）／新行數 %d（split）；舊 \\n 數 %d／新 %d'
      % (len(old), len(new), len(old) - 1, len(new) - 1))
assert len(old) - 1 == 63174, '舊總行數唔係 63174'
assert len(new) - 1 == 63004, '新總行數唔係 63004'

def mapline(n):
    if n <= 31646: return n
    if n == 31647: raise ValueError('舊 L31647 已刪')
    if 31648 <= n <= 31695: return n - 1
    if 31696 <= n <= 31735: raise ValueError('舊 L31696-31735 已刪（years66）')
    if 31736 <= n <= 31743: return n - 41
    if 31744 <= n <= 31797: raise ValueError('舊 L31744-31797 已刪（jan67）')
    if 31798 <= n <= 32141: return n - 95
    if n == 32142: raise ValueError('舊 L32142 已刪（LEVELS75_MID_OF）')
    if 32143 <= n <= 33782: return n - 96
    if 33783 <= n <= 33793: raise ValueError('舊 L33783-33793 已刪（呼叫點）')
    if 33794 <= n <= 36705: return n - 107
    if 36706 <= n <= 36768: raise ValueError('舊 L36706-36768 已刪（levels75＋c2n210）')
    return n - 170

EXPECTED_DELETED = ({31647} | set(range(31696, 31736)) | set(range(31744, 31798))
                    | {32142} | set(range(33783, 33794)) | set(range(36706, 36769)))
assert len(EXPECTED_DELETED) == 170, len(EXPECTED_DELETED)

# ---- 1. difflib 映射核實 ----
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
shift = {}
deleted = set()
replaces = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            shift[i1 + k + 1] = j1 + k + 1
    elif tag == 'replace' and (i2 - i1) >= (j2 - j1):
        # 原地改值（等長 1:1）＋縮減（YEARS66 頭行 2 舊→1 新）
        for k in range(j2 - j1):
            shift[i1 + k + 1] = j1 + k + 1
        for k in range(j2 - j1, i2 - i1):
            deleted.add(i1 + k + 1)
        replaces.append((i1 + 1, i2, j1 + 1, j2))
    elif tag == 'delete':
        for k in range(i2 - i1):
            deleted.add(i1 + k + 1)
    else:
        raise SystemExit('非預期 opcode：%s 舊 %d-%d 新 %d-%d' % (tag, i1 + 1, i2, j1 + 1, j2))
assert deleted == EXPECTED_DELETED, '被刪行集合唔符：多 %s、少 %s' % (
    sorted(deleted - EXPECTED_DELETED)[:10], sorted(EXPECTED_DELETED - deleted)[:10])
bad = [(n, m) for n, m in sorted(shift.items()) if m != mapline(n)]
assert not bad, '映射唔係分段預期：%s' % bad[:10]
print('difflib 映射核實：被刪 170 行恰好係預期集合；其餘 %d 行全部跟分段映射' % len(shift))
print('原地改值／縮減 opcode（%d 區）：' % len(replaces))
for a, b, c, d in replaces:
    print('  舊 L%d-%d → 新 L%d-%d：%s' % (a, b, c, d, old[a - 1][:80]))

# ---- 2. 逐項核實釘行舊新內容逐字相同 ----
PINS = {
 'tests/test_rom176_static.py': [
    (6360, 'lan:{ id:"lan"'), (31963, 'GIFT_REACT = giftReact'),
    (55999, '/* ===== v20a176 ROM176'),
    (56367, 'function rom176ApplyGiftOverrides()'),
    (57506, 'function addLocTalkGiftActs(add, L, npcId)'),
    (57600, 'rom176TryIntercept(id)')],
 'tests/test_tang152_static.py': [
    (31888, 'function normaliseTangStub152(pack){'),
    (32034, 'try{ normaliseTangStub152(rom2);')],
 'tests/test_tang171_static.py': [(57569, 'function openLoc(id, opts){')],
 'tests/test_tang173_static.py': [(57569, 'function openLoc(id, opts){')],
 'tests/test_text125_static.py': [(33956, 'if(typeof b.text === "string" && b.text){')],
 'tests/test_travel114_static.py': [
    (57569, 'function openLoc(id, opts){'),
    (45683, 'openLoc: function(id, opts){ openLoc(id, opts); }')],
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
    print('改 %s：加 v228 resync 註解 1 行' % path)

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

V228_NOTE = '（拎走四個存檔遷移函數，見 qa228/delete228.py；刪除區間舊 L31647／31696–31735／31744–31797／32142／33783–33793／36706–36768）'

# gift185：總行數
apply_line_edits('tests/test_gift185_static.py', [
    (61, '總行數 63174', '總行數 63004'),
    (61, '＋v210 +40）', '＋v210 +40＋v228 −170）'),
    (61, "html.count('\\n') == 63174", "html.count('\\n') == 63004"),
])
append_comment_after('tests/test_gift185_static.py',
    '# v20a210 resync：index.html 淨 +40 行（舊存檔遷移 c2n210MigrateSave 函數 ＋36 行＠舊 L36730 之後＋呼叫點 ＋4 行＠舊 L33790；difflib 對位核實純漂移），總行數 63134→63174。',
    '# v20a228 resync：index.html 淨 −170 行' + V228_NOTE + '，總行數 63174→63004（difflib 對位核實純漂移，見 qa228/resync228.py）。')

# rom176：釘行（L31712／L6152 等名係歷史標籤，唔郁；只改實際查嘅行號）
apply_line_edits('tests/test_rom176_static.py', [
    (83, 'line(31963)', 'line(31868)', 2),
    (84, 'line(55999)', 'line(55829)'),
    (85, 'line(56367)', 'line(56197)'),
    (86, 'line(57506)', 'line(57336)'),
    (87, 'line(57600)', 'line(57430)'),
])
append_comment_after('tests/test_rom176_static.py',
    '# v20a210 resync：index.html 淨 +40 行（c2n210MigrateSave ＋36 行＠舊 L36730 之後＋呼叫點 ＋4 行＠舊 L33790）；釘行按 difflib 映射重算（55959→55999、56327→56367、57466→57506、57560→57600；6360／31963 唔郁），difflib 對位核實純漂移。',
    '# v20a228 resync：index.html 淨 −170 行' + V228_NOTE + '；釘行按 difflib 映射重寫（31963→31868、55999→55829、56367→56197、57506→57336、57600→57430；6360 唔郁），difflib 對位核實純漂移，見 qa228/resync228.py。')

# tang152：0-based index（標籤 L31610／L31754 係歷史名，唔郁）
apply_line_edits('tests/test_tang152_static.py', [
    (94, 'lines()[31887]', 'lines()[31792]'),
    (95, 'lines()[32033]', 'lines()[31938]'),
])
append_comment_after('tests/test_tang152_static.py',
    '# v20a219 resync：index.html 淨 +3 行（CONTRA98 stub，插入點舊 L31845 之後）；winter_finale 11→8（hiu／choi／xu 結局改秋）；normaliseTangStub152 31899→31902、stub 呼叫行 32045→32048（difflib 對位核實純漂移，見 qa219/resync219.py）。',
    '# v20a228 resync：index.html 淨 −170 行' + V228_NOTE + '；normaliseTangStub152 31888→31793、stub 呼叫行 32034→31939（difflib 對位核實純漂移，見 qa228/resync228.py）。')

# tang171／tang173：總行數＋openLoc DEF 行
for fname, tline, dline in (('tests/test_tang171_static.py', 101, 102),
                            ('tests/test_tang173_static.py', 98, 99)):
    apply_line_edits(fname, [
        (tline, '總行數 63174', '總行數 63004'),
        (tline, '＋v210 +40）', '＋v210 +40＋v228 −170）'),
        (tline, "src.count('\\n') == 63174", "src.count('\\n') == 63004"),
        (dline, 'openLoc DEF 行 57569', 'openLoc DEF 行 57399'),
        (dline, '＋v210 +40，travel114 釘行', '＋v210 +40＋v228 −170，travel114 釘行'),
        (dline + 1, 'len(lines) >= 57569', 'len(lines) >= 57399'),
        (dline + 1, 'lines[57568]', 'lines[57398]'),
    ])
    append_comment_after(fname,
        '# v20a210 resync：index.html 淨 +40 行（舊存檔遷移 c2n210MigrateSave 函數 ＋36 行＠舊 L36730 之後＋呼叫點 ＋4 行＠舊 L33790；difflib 對位核實純漂移）。總行數 63134→63174、DEF 57529→57569。',
        '# v20a228 resync：index.html 淨 −170 行' + V228_NOTE + '，總行數 63174→63004、DEF 57569→57399（difflib 對位核實純漂移，見 qa228/resync228.py）。')

# text125：applyFamilySafeToNode b.text 分支行
apply_line_edits('tests/test_text125_static.py', [
    (63, 'ls[33955]', 'ls[33848]'),
    (64, '第 33956 行冇 b.text 分支', '第 33849 行冇 b.text 分支'),
    (64, '唔影響）', '唔影響）；v20a228 resync：33956→33849（遷移刪除淨 −170，difflib 對位核實純漂移，見 qa228/resync228.py）。'),
])

# travel114：FREE／COUNT set＋DEF／WRAPPER
PINMAP = {ln: mapline(ln) for ln in FREE_OLD + COUNT_OLD}
resync_region('tests/test_travel114_static.py', 'FREE_LINES', PINMAP)
resync_region('tests/test_travel114_static.py', 'COUNT_LINES', PINMAP)
apply_line_edits('tests/test_travel114_static.py', [
    (215, 'DEF_LINE = 57569', 'DEF_LINE = 57399'),
    (216, 'WRAPPER_LINE = 45683', 'WRAPPER_LINE = 45513'),
])
append_comment_after('tests/test_travel114_static.py',
    '# v20a210 resync：index.html 淨 +40 行（c2n210MigrateSave ＋36 行＠舊 L36730 之後＋呼叫點 ＋4 行＠舊 L33790）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（FREE ＞36729 者各 +40、＜33790 者唔郁；COUNT 36071→36075（＋4 帶）、其餘 10 處各 +40、32564 唔郁；DEF 57529→57569、WRAPPER 45643→45683），核實純漂移。',
    '# v20a228 resync：index.html 淨 −170 行' + V228_NOTE + '；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（DEF 57569→57399、WRAPPER 45683→45513），核實純漂移。')

print('全部寫檔完成')
