#!/usr/bin/env python3
# v20a200 resync：index.html 淨 +12 行（C1 閘句註解 +2／季前提示註解 +1／
# C2 rep 行註解＋分流 +6／nominee 標籤註解 +3；插入點 L46143／46636／46725／47568，
# 全部喺 L47571 之前，其後釘行一律 +12，之前唔郁）。
# 用法：python3 qa200/resync200.py            （報告模式，唔寫檔）
#       python3 qa200/resync200.py --apply    （核實純漂移後寫入 5 檔釘行）
# OLD＝pristine main a1a6681 index（/tmp/pristine200_index.html），NEW＝工作副本 index.html。
# 核實：difflib 映射每個釘行，舊行內容同新行內容逐字相同先叫純漂移；唔同即停，唔寫檔。
import difflib
import re
import sys

OLD = open('/tmp/pristine200_index.html', encoding='utf-8').read().split('\n')
NEW = open('index.html', encoding='utf-8').read().split('\n')
print('old lines: %d, new lines: %d, net: %+d' % (len(OLD) - 1, len(NEW) - 1, (len(NEW) - 1) - (len(OLD) - 1)))

sm = difflib.SequenceMatcher(None, OLD, NEW, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
print('equal-mapped lines: %d' % len(mapping))
print('change hunks (old 1-based -> new 1-based):')
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        print('  %s old L%d-%d -> new L%d-%d' % (tag, i1 + 1, i2, j1 + 1, j2))

apply = '--apply' in sys.argv
bad = []
edits = []  # (fname, old_text, new_text, note)


def map_line(old):
    """回 new 行號；落喺改動區回 None；內容唔同回 'DIFF'。"""
    new = mapping.get(old)
    if new is None:
        return None
    if OLD[old - 1] != NEW[new - 1]:
        return 'DIFF'
    return new


def check_pin(fname, old, note):
    new = map_line(old)
    print('%-32s %6d -> %-6s %s :: %s' % (fname, old, new, note, OLD[old - 1].strip()[:60]))
    if new in (None, 'DIFF'):
        bad.append((fname, old, new))
    return new


# --- 逐檔核實釘行（數字＝舊行號） ---
# tang171／tang173：總行數＋openLoc DEF 行
for f in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    check_pin(f, 55160, 'openLoc DEF')
# gift185：總行數（檔內無行號釘，只驗總數）
# rom176：4 個 line(N) 釘
for n in (53590, 53958, 55097, 55191):
    check_pin('tests/test_rom176_static.py', n, 'rom176 line()')
# travel114：DEF＋COUNT／FREE set 內裸數字
check_pin('tests/test_travel114_static.py', 55160, 'DEF_LINE')
check_pin('tests/test_travel114_static.py', 44436, 'WRAPPER_LINE（應唔郁）')
for n in (32187, 35686, 37813, 38855, 39287, 39290, 39321, 43888,
          59220, 59398, 59544, 59565):
    check_pin('tests/test_travel114_static.py', n, 'COUNT_LINES')
for n in (24686, 28232, 30854, 30855, 30867, 30868, 30879, 30880, 30983,
          40843, 43545, 43568, 53413, 53532, 53582, 53805, 53844, 53850,
          53917, 53919, 53922, 53949, 55060, 55434, 55456, 55607, 57244,
          58988, 59106, 59107, 59142, 59143, 59168, 60015):
    check_pin('tests/test_travel114_static.py', n, 'FREE_LINES')

total_old = len(OLD) - 1
total_new = len(NEW) - 1
print('total lines %d -> %d' % (total_old, total_new))

if bad:
    print('BAD %d 處（內容唔同／落喺改動區），唔寫檔：%s' % (len(bad), bad))
    sys.exit(1)
if not apply:
    print('報告模式：全部純漂移，未寫檔，加 --apply 先寫')
    sys.exit(0)

# --- 寫入（只改數字，唔郁其他嘢） ---
def rewrite(fname, subs):
    text = open(fname, encoding='utf-8').read()
    for old_s, new_s in subs:
        assert text.count(old_s) == 1, '%s: %r 出現 %d 次' % (fname, old_s, text.count(old_s))
        text = text.replace(old_s, new_s)
    open(fname, 'w', encoding='utf-8').write(text)
    print('%s 寫入 %d 處' % (fname, len(subs)))

for f in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    rewrite(f, [
        ("總行數 60667（v194 合併：v198 60602＋65）', src.count('\\n') == 60667",
         "總行數 60679（v200 合併：v194 60667＋12）', src.count('\\n') == 60679"),
        ("openLoc DEF 行 55160（v194 合併：v198 55095 映射，travel114 釘行）",
         "openLoc DEF 行 55172（v200 合併：v194 55160＋12，travel114 釘行）"),
        ("len(lines) >= 55160 and 'function openLoc(id, opts){' in lines[55159]",
         "len(lines) >= 55172 and 'function openLoc(id, opts){' in lines[55171]"),
    ])
rewrite('tests/test_gift185_static.py', [
    ("總行數 60667（v194 合併：v198 60602＋65）', html.count('\\n') == 60667",
     "總行數 60679（v200 合併：v194 60667＋12）', html.count('\\n') == 60679"),
])
rewrite('tests/test_rom176_static.py', [
    ("line(53590)", "line(53602)"),
    ("line(53958)", "line(53970)"),
    ("line(55097)", "line(55109)"),
    ("line(55191)", "line(55203)"),
])
# travel114：DEF 行＋set 內裸數字（只改 ≥47572 嗰啲；之前唔郁）
t = open('tests/test_travel114_static.py', encoding='utf-8').read()
t = t.replace("DEF_LINE = 55160      # function openLoc(id, opts){",
              "DEF_LINE = 55172      # function openLoc(id, opts){  # v20a200 resync：＋12")
assert "DEF_LINE = 55172" in t
lines = t.split('\n')
in_count = in_free = False
n_changed = 0
for i, ln in enumerate(lines):
    if ln.startswith('COUNT_LINES = {'):
        in_count = True
    elif ln.startswith('FREE_LINES = {'):
        in_free = True
    elif ln.startswith('}'):
        in_count = in_free = False
    if (in_count or in_free) and i > 0:
        m = re.match(r"^(\s+)(\d+)(,.*)$", ln)
        if m:
            old = int(m.group(2))
            new = map_line(old)
            assert new not in (None, 'DIFF'), 'travel114 bare %d' % old
            if new != old:
                lines[i] = m.group(1) + str(new) + m.group(3)
                n_changed += 1
open('tests/test_travel114_static.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('tests/test_travel114_static.py 寫入 DEF＋%d 個 set 數字' % n_changed)
# travel114 檔頭補一行 resync 註解（放喺 v20a198 resync 嗰行之後）
t = open('tests/test_travel114_static.py', encoding='utf-8').read()
anchor = "# v20a198 resync：index.html 淨 −7 行（C1 死 code 刪 −43／B1 守衛 ＋12／C2＋C3 ＋24）；/tmp/resync198.py difflib 對位核實 73 個錨點內容逐行相同，純漂移；COUNT 12／FREE 34 不變。"
assert anchor in t
t = t.replace(anchor, anchor + "\n# v20a200 resync：index.html 淨 ＋12 行（C1 註解＋2／提示註解＋1／C2 註解＋分流＋6／nominee 標籤註解＋3；插入點 L46143／46636／46725／47568，全部喺 L47571 之前，其後釘行一律 ＋12；COUNT 12／FREE 34 不變，DEF 55160→55172、WRAPPER 44436 唔郁；qa200/resync200.py difflib 對位核實純漂移）。")
open('tests/test_travel114_static.py', 'w', encoding='utf-8').write(t)
print('resync 完成')
