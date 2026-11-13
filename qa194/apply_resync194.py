# -*- coding: utf-8 -*-
"""v20a194 resync apply：將 qa194/resync194.py 核實咗嘅新行號寫入 5 檔釘行測試。
只改 live 數據（COUNT／FREE／DEF／總行數斷言），唔郁 header 歷史註解（另加一行 v194 resync 註解）。
用法：python3 qa194/apply_resync194.py
"""
import re

ROOT = "/home/hatch/workspace/linji-work194"
MAP = {
    53532: 53597, 53900: 53965, 55039: 55104, 55133: 55198, 55102: 55167,
    59162: 59227, 59340: 59405, 59486: 59551, 59507: 59572,
    53355: 53420, 53474: 53539, 53524: 53589, 53747: 53812, 53786: 53851,
    53792: 53857, 53859: 53924, 53861: 53926, 53864: 53929, 53891: 53956,
    55002: 55067, 55376: 55441, 55398: 55463, 55549: 55614, 57186: 57251,
    58930: 58995, 59048: 59113, 59049: 59114, 59084: 59149, 59085: 59150,
    59110: 59175, 59957: 60022,
}
NOTE = ("# v20a194 resync：index.html 淨 +65 行（meta tip 覆寫 ＋25／拆閘 ＋2／"
        "awardsCheck 探針 ＋37／load 呼叫 ＋1，插入點舊 L45754／46070／46305／49384；"
        "difflib 對位核實純漂移，見 qa194/resync194.py）；其後釘行各 +65，之前唔郁；總行數 60609→60674。\n")


def sub_block(path, var, mapping):
    txt = open(path, encoding="utf-8").read()
    m = re.search(re.escape(var) + r"\s*=\s*\{([^}]*)\}", txt, re.S)
    assert m, var
    block = m.group(1)

    def repl(mn):
        return str(mapping.get(int(mn.group(0)), int(mn.group(0))))
    new_block = re.sub(r"\b\d+\b", repl, block)
    assert new_block != block or var == "COUNT_LINES", var
    open(path, "w", encoding="utf-8").write(txt[:m.start(1)] + new_block + txt[m.end(1):])


def sub_lines(path, linenos, mapping):
    lines = open(path, encoding="utf-8").read().split("\n")
    for ln in linenos:
        old = lines[ln - 1]
        new = re.sub(r"\b\d+\b", lambda m: str(mapping.get(int(m.group(0)), int(m.group(0)))), old)
        assert new != old, (path, ln, old)
        lines[ln - 1] = new
    open(path, "w", encoding="utf-8").write("\n".join(lines))


def prepend_note(path):
    txt = open(path, encoding="utf-8").read()
    assert "v20a194 resync" not in txt
    open(path, "w", encoding="utf-8").write(NOTE + txt)


# travel114：COUNT／FREE 兩個 live set＋DEF 行（WRAPPER 44443 喺插入點之前，唔郁）
t114 = ROOT + "/tests/test_travel114_static.py"
sub_block(t114, "COUNT_LINES", MAP)
sub_block(t114, "FREE_LINES", MAP)
lines = open(t114, encoding="utf-8").read().split("\n")
for i, l in enumerate(lines):
    if l.startswith("DEF_LINE = 55102"):
        lines[i] = "DEF_LINE = 55167      # function openLoc(id, opts){"
        break
else:
    raise SystemExit("DEF_LINE not found")
open(t114, "w", encoding="utf-8").write("\n".join(lines))
prepend_note(t114)

# rom176：4 條釘行斷言（第 76–79 行；31587 喺插入點之前，唔郁）
sub_lines(ROOT + "/tests/test_rom176_static.py", [76, 77, 78, 79], MAP)
prepend_note(ROOT + "/tests/test_rom176_static.py")

# tang171／173：總行數＋DEF 兩條斷言（第 81–83 行）。
# 注意：第 82 行「55018→55102」係 v195 歷史，唔郁——只換第一個 55102（釘值）；
# 第 83 行 lines[55101] 係 0-indexed，要跟住變 lines[55166]。
for f in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    p = ROOT + "/" + f
    lines = open(p, encoding="utf-8").read().split("\n")
    assert "60609" in lines[80] and "55102" in lines[81] and "55102" in lines[82]
    lines[80] = lines[80].replace("60609", "60674")
    lines[81] = lines[81].replace("55102", "55167", 1)
    lines[82] = lines[82].replace("55102", "55167").replace("55101", "55166")
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    prepend_note(p)

# gift185：總行數斷言（第 42 行）
sub_lines(ROOT + "/tests/test_gift185_static.py", [42], {60609: 60674})
prepend_note(ROOT + "/tests/test_gift185_static.py")

print("applied")
