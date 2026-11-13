#!/usr/bin/env python3
# v20a200 rebase 上 main 2c1a680 resync：index.html 淨 +12 行（v200 本身；
# C1 註解＋2／提示註解＋1／C2 註解＋分流＋6／nominee 標籤註解＋3；
# 插入點 main L46187／46680／46767／47609，全部喺 L47609 之前）。
# OLD＝main index（/tmp/main200_index.html），NEW＝工作副本 index.html。
# 用法：python3 qa200/resync200_rebase.py            （報告模式，唔寫檔）
#       python3 qa200/resync200_rebase.py --apply    （核實純漂移後寫入 5 檔釘行）
import difflib
import re
import sys

OLD = open('/tmp/main200_index.html', encoding='utf-8').read().split('\n')
NEW = open('index.html', encoding='utf-8').read().split('\n')
print('old lines: %d, new lines: %d, net: %+d' % (len(OLD) - 1, len(NEW) - 1, (len(NEW) - 1) - (len(OLD) - 1)))

sm = difflib.SequenceMatcher(None, OLD, NEW, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
    else:
        print('  %s old L%d-%d -> new L%d-%d' % (tag, i1 + 1, i2, j1 + 1, j2))

apply = '--apply' in sys.argv
bad = []


def map_line(old):
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


# --- 逐檔核實釘行（數字＝main 行號） ---
for f in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    check_pin(f, 55204, 'openLoc DEF')
check_pin('tests/test_gift185_static.py', 60711, 'total lines (count)')
for n in (53634, 54002, 55141, 55235):
    check_pin('tests/test_rom176_static.py', n, 'rom176 line()')
check_pin('tests/test_travel114_static.py', 55204, 'DEF_LINE')
check_pin('tests/test_travel114_static.py', 44480, 'WRAPPER_LINE（應唔郁）')
t = open('tests/test_travel114_static.py', encoding='utf-8').read()
for sec in ('COUNT_LINES', 'FREE_LINES'):
    seg = t.split(sec + ' = {', 1)[1].split('}', 1)[0]
    nums = [int(x) for x in re.findall(r'^\s+(\d+),', seg, re.M)]
    for n in nums:
        check_pin('tests/test_travel114_static.py', n, sec)

if bad:
    print('BAD %d 處，唔寫檔：%s' % (len(bad), bad))
    sys.exit(1)
if not apply:
    print('報告模式：全部純漂移，未寫檔，加 --apply 先寫')
    sys.exit(0)


def rewrite(fname, subs):
    text = open(fname, encoding='utf-8').read()
    for old_s, new_s in subs:
        assert text.count(old_s) == 1, '%s: %r 出現 %d 次' % (fname, old_s, text.count(old_s))
        text = text.replace(old_s, new_s)
    open(fname, 'w', encoding='utf-8').write(text)
    print('%s 寫入 %d 處' % (fname, len(subs)))


for f in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    rewrite(f, [
        ("總行數 60711（v199 rebase 上 main a1a6681：v194 60667＋44）",
         "總行數 60723（v200 rebase 上 main 2c1a680：v199 60711＋12）"),
        ("openLoc DEF 行 55204（v199 rebase 上 main a1a6681：v194 55160＋44，travel114 釘行）",
         "openLoc DEF 行 55216（v200 rebase 上 main 2c1a680：v199 55204＋12，travel114 釘行）"),
        ("len(lines) >= 55204 and 'function openLoc(id, opts){' in lines[55203]",
         "len(lines) >= 55216 and 'function openLoc(id, opts){' in lines[55215]"),
    ])
    # 總行數斷言數值（檔案實際係 count('\n') 單反斜線；用純字串換，唔掂 regex）
    rewrite(f, [("== 60711)", "== 60723)")])
rewrite('tests/test_gift185_static.py', [
    ("總行數 60711（v199 rebase 上 main a1a6681：v194 60667＋44）",
     "總行數 60723（v200 rebase 上 main 2c1a680：v199 60711＋12）"),
    ("== 60711)", "== 60723)"),
])
rewrite('tests/test_rom176_static.py', [
    ("line(53634)", "line(53646)"),
    ("line(54002)", "line(54014)"),
    ("line(55141)", "line(55153)"),
    ("line(55235)", "line(55247)"),
])
# travel114：DEF 行＋set 內裸數字（按 difflib 映射逐個重算）
t = open('tests/test_travel114_static.py', encoding='utf-8').read()
t = t.replace("DEF_LINE = 55204      # function openLoc(id, opts){",
              "DEF_LINE = 55216      # function openLoc(id, opts){  # v20a200 rebase：＋12")
assert "DEF_LINE = 55216" in t
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
# travel114 檔頭補一行 resync 註解（放喺 v20a199 resync 嗰行之後）
t = open('tests/test_travel114_static.py', encoding='utf-8').read()
anchor = "# v20a199 resync：index.html 淨 +44 行（DLG199 ＋30／fitApply ＋13／WF4 onload ＋1）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重算，內容逐字核實純漂移。"
assert anchor in t
t = t.replace(anchor, anchor + "\n# v20a200 rebase resync：index.html 淨 ＋12 行（C1 註解＋2／提示註解＋1／C2 註解＋分流＋6／nominee 標籤註解＋3；插入點 main L46187／46680／46767／47609；COUNT 12／FREE 34 不變，DEF 55204→55216、WRAPPER 44480 唔郁；qa200/resync200_rebase.py difflib 對位核實純漂移）。")
open('tests/test_travel114_static.py', 'w', encoding='utf-8').write(t)
print('resync 完成')
