# -*- coding: utf-8 -*-
"""v20a145 resync 核實：BOOK145 CSS 段淨 +67 行（舊行 5393 嘅 BOOK143 完＋</style>
行換做 68 行：BOOK143 完＋BOOK145 段＋</style>），其餘逐行相同（difflib 對位
pristine main c881530）；舊測試錨點凡 >5393 者一律 +67。
用法：python3 qa145/resync_travel114.py
"""
import difflib, subprocess, sys

def git_show(spec):
    return subprocess.check_output(["git", "show", spec], text=True, encoding="utf-8")

old = git_show("HEAD:index.html").split("\n")
new = open("index.html", encoding="utf-8").read().split("\n")
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
ops = [op for op in sm.get_opcodes() if op[0] != "equal"]
print("non-equal opcodes:", ops)
assert len(ops) == 1 and ops[0][0] == "replace", "唔係單一替換，唔係純漂移"
tag, i1, i2, j1, j2 = ops[0]
print("replace old lines %d-%d -> new lines %d-%d (net +%d)" % (i1 + 1, i2, j1 + 1, j2, (j2 - j1) - (i2 - i1)))
assert (i1, i2, j1, j2) == (5392, 5393, 5392, 5460), "替換範圍唔係預期（舊 5393、淨 +67）"
ins = new[j1:j2]
assert ins[0].startswith("/* === v20a143 BOOK143 完 === */"), "替換頭唔係 BOOK143 完"
assert ins[1].startswith("/* === v20a145 BOOK145"), "插入頭唔係 BOOK145"
assert ins[-1].endswith("BOOK145 完 === */</style>"), "插入尾唔係 BOOK145 完"
assert "v20a145 BOOK145" in "\n".join(ins) and "BOOK145 完" in "\n".join(ins)

# 舊測試錨點內容對位：舊行 L 嘅內容 == 新行 L+67 嘅內容（L > 5393）
def check(old_line, expect_snippet):
    assert old[old_line - 1].strip() == new[old_line + 67 - 1].strip(), \
        "行 %d 內容對唔上（舊→新+67）" % old_line
    assert expect_snippet in new[old_line + 67 - 1], "行 %d 新內容缺預期片段" % old_line
    print("OK old %d -> new %d: %s" % (old_line, old_line + 67, new[old_line + 67 - 1].strip()[:60]))

# text125 三個錨點（內容逐行相同；FALLBACK 常數喺附近行，唔係正嗰行，唔用佢做 snippet）
check(27674, "b.lines")
check(27787, "b.lines")
check(33385, "b.text")
# travel114：COUNT 13＋FREE 27＋DEF＋WRAPPER
for ln in (32006, 35477, 37604, 38598, 39032, 39035, 39066, 43597, 57252, 57419, 57562, 57583, 58033):
    check(ln, "openLoc(")
for ln in (24672, 28141, 30727, 30728, 30740, 30741, 30752, 30753, 30856, 40556,
           43254, 43277, 52097, 52216, 53109, 53491, 53513, 53648, 55285, 56696,
           57029, 57147, 57148, 57183, 57184, 57203, 57218):
    check(ln, "openLoc(")
check(53222, "function openLoc(id, opts){")
check(44009, "openLoc: function(id, opts){ openLoc(id, opts); }")
print("RESYNC PASS：純漂移核實完成，全部錨點 +67 對位一致")
