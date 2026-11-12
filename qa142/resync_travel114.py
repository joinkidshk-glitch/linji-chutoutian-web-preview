# v20a142 resync travel114：對位 pristine bcac846 → 修後 index.html，核實 44 個 openLoc( 呼叫點
# 純漂移（內容逐行相同、分類不變），輸出新行號供 test_travel114_static.py 更新。
# 用法：python3 qa142/resync_travel114.py
import difflib, re, sys

OLD = "/tmp/linji142-pristine-index.html"
NEW = "index.html"
a = open(OLD, encoding="utf-8").read().split("\n")
b = open(NEW, encoding="utf-8").read().split("\n")
sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
old2new = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            old2new[i1 + k + 1] = j1 + k + 1  # 1-based
print("net lines: %d -> %d (%+d)" % (len(a), len(b), len(b) - len(a)))

COUNT_OLD = [31903, 35374, 37499, 38493, 38927, 38930, 38961, 43464, 57111, 57278, 57421, 57442, 57892]
FREE_OLD = [24569, 28038, 30624, 30625, 30637, 30638, 30649, 30650, 30753, 40423, 43121, 43144,
            51956, 52075, 52968, 53350, 53372, 53507, 55144, 56555, 56888, 57006, 57007, 57042,
            57043, 57062, 57077]
DEF_OLD, WRAP_OLD = 53081, 43876
FREE_FLAGS = ("travelFree:true", "encDone:true", "forceRestore:true", "wf4Done:true")

def show(name, old_lines):
    new_lines = []
    for ln in old_lines:
        nl = old2new.get(ln)
        assert nl is not None, "%s 舊行 %d 唔係 equal 區（內容郁咗？）" % (name, ln)
        assert a[ln - 1].strip() == b[nl - 1].strip(), "%s 舊行 %d 內容唔同：%r vs %r" % (name, ln, a[ln - 1][:80], b[nl - 1][:80])
        new_lines.append(nl)
    print("%s_OLD %s" % (name, old_lines))
    print("%s_NEW %s" % (name, new_lines))
    return new_lines

count_new = show("COUNT", COUNT_OLD)
free_new = show("FREE", FREE_OLD)
def_new = show("DEF", [DEF_OLD])[0]
wrap_new = show("WRAPPER", [WRAP_OLD])[0]

# 分類不變核實：新 FREE 行全部帶旗、新 COUNT 行全部冇旗
for ln in free_new:
    assert any(f in b[ln - 1] for f in FREE_FLAGS), "FREE 新行 %d 唔帶旗" % ln
for ln in count_new:
    assert not any(f in b[ln - 1] for f in FREE_FLAGS), "COUNT 新行 %d 帶旗" % ln
assert "function openLoc(id, opts){" in b[def_new - 1]
assert "openLoc: function(id, opts){ openLoc(id, opts); }" in b[wrap_new - 1]

# 呼叫點總數不變：修後樹 openLoc( 行數 == 舊樹（COUNT 13＋FREE 27＋DEF 1＋WRAPPER 1＋測試區 2＝44）
old_calls = [i + 1 for i, l in enumerate(a) if "openLoc(" in l]
new_calls = [i + 1 for i, l in enumerate(b) if "openLoc(" in l]
print("openLoc( 行數：舊 %d → 新 %d" % (len(old_calls), len(new_calls)))
assert len(old_calls) == len(new_calls) == 44, "openLoc( 行數變咗，唔係純漂移"
mapped = set(count_new) | set(free_new) | {def_new, wrap_new}
# 測試區 runSoftP0Checks 內 2 行唔靠死行號，用函數範圍驗（同測試本身一樣 brace-match）
def fn_range(lines, start_pat):
    s = "\n".join(lines)
    st = s.find(start_pat)
    d, j = 0, s.find("{", st)
    for k in range(j, len(s)):
        if s[k] == "{": d += 1
        elif s[k] == "}":
            d -= 1
            if d == 0: j = k; break
    return (s[:st].count("\n") + 1, s[:j].count("\n") + 1)
TEST_START, TEST_END = fn_range(b, "function runSoftP0Checks(){")
test_lines = [ln for ln in new_calls if ln not in mapped]
print("測試區 runSoftP0Checks 行 %d–%d，區內 openLoc( 行：%s（應為 2 行）" % (TEST_START, TEST_END, test_lines))
assert len(test_lines) == 2 and all(TEST_START <= ln <= TEST_END for ln in test_lines)
print("RESYNC OK：44 呼叫點純漂移，分類不變")
print("DEF_LINE = %d  WRAPPER_LINE = %d" % (def_new, wrap_new))
