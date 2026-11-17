"""Re-sync 5 釘行靜態測試 after v20a269 第一批（廖／顧／麥三線，index.html 淨 +73 行）。
OLD = 分支 base main 3ab2e22（v268），NEW = 工作副本 index.html。
方法（v158／v162 precedent）：difflib SequenceMatcher 對位，全部釘行舊內容必須喺
equal block 入面逐字相同先算純漂移，否則停手唔改。
- test_travel114_static.py：openLoc( 呼叫點序列逐字一致先 remap COUNT／FREE／DEF／WRAPPER。
- test_rom176_static.py：4 個釘行按映射重寫（內容逐字核實）。
- test_gift185_static.py／test_tang171_static.py／test_tang173_static.py：
  總行數 45307→45380（鏈尾加 ＋v269 +73）；openLoc DEF 40549→40622（全部改動喺 DEF 之前，＋73）。
Usage: python3 qa269/resync269.py [--apply]
"""
import difflib
import re
import subprocess
import sys

ROOT = "/home/hatch/workspace/linji-work269"
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
print("OLD lines:", len(OLD) - 1, " NEW lines:", len(NEW) - 1,
      " net:", (len(NEW) - 1) - (len(OLD) - 1))
assert (len(NEW) - 1) - (len(OLD) - 1) == 73, "net delta != +73"

sm = difflib.SequenceMatcher(None, OLD, NEW, autojunk=False)
pos = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            pos[i1 + k + 1] = j1 + k + 1  # 1-indexed

def mapped(old_line):
    assert old_line in pos, "old line %d not in equal block — NOT pure drift!" % old_line
    return pos[old_line]

def check_content(old_line, pred, what):
    new_line = mapped(old_line)
    assert OLD[old_line - 1] == NEW[new_line - 1], \
        "content mismatch old %d -> new %d" % (old_line, new_line)
    assert pred(NEW[new_line - 1]), "predicate failed at new %d (%s)" % (new_line, what)
    print("  %s: old %d -> new %d (content identical)" % (what, old_line, new_line))
    return new_line

# ---- 1. travel114：openLoc( 序列一致先 remap ----
TEST114 = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read()
old_hits = [(i + 1, l.strip()) for i, l in enumerate(OLD) if "openLoc(" in l]
new_hits = [(i + 1, l.strip()) for i, l in enumerate(NEW) if "openLoc(" in l]
print("openLoc( lines: old %d new %d" % (len(old_hits), len(new_hits)))
assert [s for _, s in old_hits] == [s for _, s in new_hits], \
    "openLoc sequence DIFFERS — not a pure shift, stop!"
print("openLoc sequence identical: pure line shift confirmed")

def parse_set(name):
    # 行式 parse：由 "NAME = {" 起，到獨佔一行嘅 "}" 為止（set 內註解有 "{travelFree}"，
    # regex [^}]* 會喺註解嗰個 } 提前截斷——v158 腳本同一寫法喺而家會錯）。
    lines = TEST114.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith(name + " = {"))
    end = next(i for i in range(start + 1, len(lines)) if lines[i] == "}")
    nums, comments = [], {}
    for line in lines[start + 1:end]:
        code = line.split("#", 1)[0]
        found = [int(x) for x in re.findall(r"\d+", code)]
        if not found:
            continue
        nums.extend(found)
        if "#" in line:
            comments[found[-1]] = line.split("#", 1)[1].strip()
    return nums, comments

def replace_set(text, name, nums, comments):
    lines = text.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith(name + " = {"))
    end = next(i for i in range(start + 1, len(lines)) if lines[i] == "}")
    new_block = [name + " = {"] + [
        "    %d,%s" % (n, ("  # " + comments[n]) if n in comments else "")
        for n in sorted(nums)
    ] + ["}"]
    return "\n".join(lines[:start] + new_block + lines[end + 1:])

count_nums, count_c = parse_set("COUNT_LINES")
free_nums, free_c = parse_set("FREE_LINES")
def_old = int(re.search(r"DEF_LINE = (\d+)", TEST114).group(1))
wrap_old = int(re.search(r"WRAPPER_LINE = (\d+)", TEST114).group(1))
for n in count_nums + free_nums + [def_old, wrap_old]:
    assert OLD[n - 1].strip() == NEW[mapped(n) - 1].strip(), "content mismatch at old %d" % n
print("travel114 pins remapped: COUNT %s FREE %d lines DEF %d->%d WRAPPER %d->%d" % (
    [mapped(n) for n in sorted(count_nums)], len(free_nums),
    def_old, mapped(def_old), wrap_old, mapped(wrap_old)))
d = [i + 1 for i, l in enumerate(NEW) if "function openLoc(id, opts){" in l]
w = [i + 1 for i, l in enumerate(NEW) if "openLoc: function(id, opts){ openLoc(id, opts); }" in l]
print("direct-search DEF:", d, "WRAPPER:", w)
assert d == [mapped(def_old)] and w == [mapped(wrap_old)]

# ---- 2. rom176：4 釘行 ----
TEST176 = open(ROOT + "/tests/test_rom176_static.py", encoding="utf-8").read()
rom_new = {}
rom_new[38933] = check_content(38933, lambda s: s.startswith("/* ===== v20a176 ROM176"), "ROM176 block")
rom_new[39291] = check_content(39291, lambda s: s.startswith("function rom176ApplyGiftOverrides()"), "rom176ApplyGiftOverrides")
rom_new[40434] = check_content(40434, lambda s: s.startswith("function addLocTalkGiftActs(add, L, npcId)"), "addLocTalkGiftActs")
rom_new[40590] = check_content(40590, lambda s: "rom176TryIntercept(id)" in s, "openLoc rom176 intercept")

# ---- 3. 總行數＋DEF（gift185／tang171／tang173） ----
def_new = check_content(40549, lambda s: "function openLoc(id, opts){" in s, "openLoc DEF")
assert def_new == 40622, "DEF new != 40622 (got %d)" % def_new
print("total newlines NEW:", open(ROOT + "/index.html", encoding="utf-8").read().count("\n"))

if "--apply" not in sys.argv:
    print("\nDRY RUN — no files changed. Re-run with --apply.")
    sys.exit(0)

HDR269 = "# v20a269 resync：index.html 淨 +73 行（廖／顧／麥第一批：flags 欄位＋冷版 beats＋registry 閘＋BuildScript 變體；插入點舊 L35391–39885）；釘行按 difflib 映射重寫，內容逐字核實純漂移，見 qa269/resync269.py。\n"

# travel114
out = TEST114
out = replace_set(out, "COUNT_LINES",
                  [mapped(n) for n in count_nums],
                  {mapped(n): c for n, c in count_c.items()})
out = replace_set(out, "FREE_LINES",
                  [mapped(n) for n in free_nums],
                  {mapped(n): c for n, c in free_c.items()})
out = re.sub(r"DEF_LINE = \d+", "DEF_LINE = %d" % mapped(def_old), out, count=1)
out = re.sub(r"WRAPPER_LINE = \d+", "WRAPPER_LINE = %d" % mapped(wrap_old), out, count=1)
out = HDR269 + out
open(ROOT + "/tests/test_travel114_static.py", "w", encoding="utf-8").write(out)
print("APPLIED: test_travel114_static.py")

# rom176
out = TEST176
for old, new in sorted(rom_new.items()):
    out = out.replace("line(%d)" % old, "line(%d)" % new)
out = HDR269 + out
open(ROOT + "/tests/test_rom176_static.py", "w", encoding="utf-8").write(out)
print("APPLIED: test_rom176_static.py pins", rom_new)

# gift185 / tang171 / tang173 — total + DEF
for fname, is_tang in [("test_gift185_static.py", False),
                       ("test_tang171_static.py", True),
                       ("test_tang173_static.py", True)]:
    p = ROOT + "/tests/" + fname
    txt = open(p, encoding="utf-8").read()
    assert "45307" in txt and "＋v268 −236" in txt
    txt = txt.replace("總行數 45307（", "總行數 45380（", 1)
    txt = txt.replace("＋v268 −236）", "＋v268 −236＋v269 +73）", 1)
    txt = txt.replace("== 45307", "== 45380", 1)
    if is_tang:
        assert "openLoc DEF 行 40549" in txt and "lines[40548]" in txt
        txt = txt.replace("openLoc DEF 行 40549（", "openLoc DEF 行 40622（", 1)
        txt = txt.replace("＋v268 −236，travel114 釘行", "＋v268 −236＋v269 +73，travel114 釘行", 1)
        txt = txt.replace("len(lines) >= 40555", "len(lines) >= 40628", 1)
        txt = txt.replace("lines[40548]", "lines[40621]", 1)
    txt = HDR269 + txt
    open(p, "w", encoding="utf-8").write(txt)
    print("APPLIED:", fname)
print("\nALL APPLIED")
