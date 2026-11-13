# 補 resync188.py 漏咗嘅 travel114 帶註解數字行（^ 數字, # 註解 格式唔 match 舊 regex）。
# 純字串操作，唔用 regex。shift dict 嚟自 resync188.py difflib 核實結果。
SHIFT = {
    58711: 58936, 58889: 59114, 59032: 59257, 59053: 59278,
    53023: 53248, 53073: 53298, 53296: 53521, 53335: 53560, 53341: 53566,
    53408: 53633, 53410: 53635, 53413: 53638, 53440: 53665, 54551: 54776,
    54947: 55172, 55098: 55323, 56735: 56960, 58479: 58704,
    58634: 58859, 58659: 58884, 59503: 59728,
}
p = "/home/hatch/workspace/linji-work188/tests/test_travel114_static.py"
lines = open(p, encoding="utf-8").read().split("\n")
in_count = in_free = False
changed = []
for idx, ln in enumerate(lines):
    if ln.startswith("COUNT_LINES"):
        in_count = True
    elif ln.startswith("FREE_LINES"):
        in_free = True
    elif ln.startswith("FREE_FLAGS"):
        in_count = in_free = False
    if not (in_count or in_free):
        continue
    stripped = ln.strip()
    if "," not in stripped:
        continue
    head = stripped.split(",", 1)[0].strip()
    if not head.isdigit():
        continue
    n = int(head)
    if n in SHIFT:
        indent = ln[:len(ln) - len(ln.lstrip())]
        rest = ln[ln.index(","):]
        lines[idx] = indent + str(SHIFT[n]) + rest
        changed.append((n, SHIFT[n]))
print("changed:", changed)
open(p, "w", encoding="utf-8").write("\n".join(lines))
