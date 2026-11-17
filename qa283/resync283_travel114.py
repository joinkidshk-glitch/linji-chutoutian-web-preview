# qa283 resync: test_travel114_static.py 釘行重算（v283，index.html 淨 +76 行）。
# 插入點（舊行號）：殺青鉤通用分支 ＋2＠舊 L21490 之後；R5-A＋H 新函數＋對照表 ＋74＠舊 L26493 之後。
# 段規則：舊行 ＜21490 唔郁；21490–26492 ＋2；≥26493 ＋76。
# 單次掃描 dict 查表（只換 dict 區行首 key 數字，唔逐對 re.sub，免撞值）；改完逐行對內容核實。
import re

ROOT = '/home/hatch/workspace/linji-work283'
html_lines = open(ROOT + '/index.html', encoding='utf-8').read().split('\n')
p = ROOT + '/tests/test_travel114_static.py'
src = open(p, encoding='utf-8').read()

FREE = {24458: 24460, 25801: 25803, 25802: 25804, 25878: 25880, 27933: 28009,
        27966: 28042, 39568: 39644, 39687: 39763, 39762: 39838, 39970: 40046,
        40014: 40090, 40020: 40096, 40087: 40163, 40089: 40165, 40092: 40168,
        40119: 40195, 41263: 41339, 41310: 41386, 41680: 41756, 41702: 41778,
        41854: 41930, 41859: 41935, 42783: 42859, 44261: 44337, 44531: 44607,
        44532: 44608, 44576: 44652, 44577: 44653, 44602: 44678, 45495: 45571}
COUNT = {22197: 22199, 22637: 22639, 22640: 22642, 22671: 22673, 28124: 28200, 44654: 44730,
         44866: 44942, 45024: 45100, 45045: 45121}
DEF_NEW = 41491
WRAPPER_NEW = 28769


def resync_dict(text, start_marker, mapping):
    i = text.index(start_marker)
    j = text.index('\n}', i)
    region = text[i:j]

    def repl(m):
        n = int(m.group(2))
        return m.group(1) + str(mapping.get(n, n)) + m.group(3)

    return text[:i] + re.sub(r'^(\s*)(\d+)(,)', repl, region, flags=re.M) + text[j:]


src = resync_dict(src, 'FREE_LINES = {', FREE)
src = resync_dict(src, 'COUNT_LINES = {', COUNT)
if 'DEF_LINE = 41415' in src:
    src = src.replace('DEF_LINE = 41415', 'DEF_LINE = %d' % DEF_NEW, 1)
if 'WRAPPER_LINE = 28693' in src:
    src = src.replace('WRAPPER_LINE = 28693', 'WRAPPER_LINE = %d' % WRAPPER_NEW, 1)
comment = ("# v20a283 resync：index.html 淨 +76 行（殺青鉤通用分支 ＋2＠舊 L21490 之後／"
           "R5-A＋H 新函數＋對照表 ＋74＠舊 L26493 之後；COUNT／FREE／DEF／WRAPPER 按段重算："
           "＜21490 唔郁、21490–26492 ＋2、≥26493 ＋76；DEF 41415→41491、WRAPPER 28693→28769），"
           "內容逐行核實純漂移。\n")
src = comment + src if 'v20a283 resync' not in src else src
open(p, 'w', encoding='utf-8').write(src)

# ---- 逐行對內容核實（唔信算術，信內容） ----
FLAGS = ("travelFree:true", "encDone:true", "forceRestore:true", "wf4Done:true")
bad = []
for old, new in list(FREE.items()) + list(COUNT.items()):
    line = html_lines[new - 1]
    if 'openLoc(' not in line:
        bad.append((new, 'no openLoc(', line[:80]))
for old, new in FREE.items():
    if not any(f in html_lines[new - 1] for f in FLAGS):
        bad.append((new, 'FREE no flag', html_lines[new - 1][:80]))
for old, new in COUNT.items():
    if any(f in html_lines[new - 1] for f in FLAGS):
        bad.append((new, 'COUNT has flag', html_lines[new - 1][:80]))
for n in (6531, 6532, 8223, 14250, 14251, 14263, 14264, 14275, 14276, 14376):
    if not any(f in html_lines[n - 1] for f in FLAGS):
        bad.append((n, 'FREE untouched mismatch', html_lines[n - 1][:80]))
for n in (15395, 18794, 20995):
    if 'openLoc(' not in html_lines[n - 1] or any(f in html_lines[n - 1] for f in FLAGS):
        bad.append((n, 'COUNT untouched mismatch', html_lines[n - 1][:80]))
if 'function openLoc(id, opts){' not in html_lines[DEF_NEW - 1]:
    bad.append((DEF_NEW, 'DEF mismatch', html_lines[DEF_NEW - 1][:80]))
if 'openLoc: function(id, opts){ openLoc(id, opts); }' not in html_lines[WRAPPER_NEW - 1]:
    bad.append((WRAPPER_NEW, 'WRAPPER mismatch', html_lines[WRAPPER_NEW - 1][:80]))
print('MISMATCHES:', bad if bad else 'none')
print('resync done: FREE %d + COUNT %d + DEF + WRAPPER' % (len(FREE), len(COUNT)))
