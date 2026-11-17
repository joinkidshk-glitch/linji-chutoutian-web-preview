"""Re-sync 釘行靜態測試 after v20a271 第二批（WORKORDER 1.10-1.17＋陸頂一晚新機制，index.html 淨 +91 行）。
OLD = 分支 base main e1bf9cc（v269），NEW = 工作副本 index.html。
方法（v269 precedent）：difflib SequenceMatcher 對位，全部釘行舊內容必須喺
equal block 入面逐字相同先算純漂移，否則停手唔改。
- test_travel114_static.py：openLoc( 呼叫點序列逐字一致先 remap COUNT／FREE／DEF／WRAPPER。
- test_rom176_static.py：4 個釘行按映射重寫（內容逐字核實）。
- test_rom159_static.py：4 個釘行按映射重寫（block 頭／CMT／SoMeetGate／全佳註解行）。
- test_gift185_static.py／test_tang171_static.py／test_tang173_static.py：
  總行數 45380→45471（鏈尾加 ＋v271 +91）；openLoc DEF 40622→40713（全部改動喺 DEF 之前，＋91）。
- test_awei195_static.py：唔使 resync——S4 窗口問題已喺 production 側修好
  （wrap hook 改一行寫法，record call 仲喺 done_ 行之後 3 行內），直接跑 PASS。
替換一律單次掃描 dict 查表（re.sub alternation 一次過），唔逐對 re.sub。
Usage: python3 qa271/resync271.py [--apply]
"""
import difflib
import re
import subprocess
import sys

ROOT = "/home/hatch/workspace/linji-work271"
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
print("OLD lines:", len(OLD) - 1, " NEW lines:", len(NEW) - 1,
      " net:", (len(NEW) - 1) - (len(OLD) - 1))
assert (len(NEW) - 1) - (len(OLD) - 1) == 91, "net delta != +91"

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

def single_pass_replace(text, table):
    """一次掃描、多對替換：按長度由長到短排 alternation，dict 查表取值；
    唔逐對 re.sub，避免一對嘅輸出撞入另一對嘅輸入。"""
    keys = sorted(table, key=len, reverse=True)
    pat = re.compile("|".join(re.escape(k) for k in keys))
    found = set()
    def _sub(m):
        found.add(m.group(0))
        return table[m.group(0)]
    out = pat.sub(_sub, text)
    missing = [k for k in keys if k not in found]
    assert not missing, "replacement keys not found: %r" % missing
    return out

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
rom_new[39005] = check_content(39005, lambda s: s.startswith("/* ===== v20a176 ROM176"), "ROM176 block")
rom_new[39363] = check_content(39363, lambda s: s.startswith("function rom176ApplyGiftOverrides()"), "rom176ApplyGiftOverrides")
rom_new[40507] = check_content(40507, lambda s: s.startswith("function addLocTalkGiftActs(add, L, npcId)"), "addLocTalkGiftActs")
rom_new[40663] = check_content(40663, lambda s: "rom176TryIntercept(id)" in s, "openLoc rom176 intercept")

# ---- 3. rom159：4 釘行 ----
TEST159 = open(ROOT + "/tests/test_rom159_static.py", encoding="utf-8").read()
rom159_new = {}
rom159_new[25195] = check_content(25195, lambda s: "v20a159 ROM159 Phase 1" in s, "ROM159 block head")
rom159_new[26029] = check_content(26029, lambda s: "COMMIT48_NODES.CMT_lan_commit" in s, "CMT_lan_commit")
rom159_new[25944] = check_content(25944, lambda s: "function rom159SoMeetGate" in s, "rom159SoMeetGate")
rom159_new[25223] = check_content(25223, lambda s: "查實" in s, "全佳查實註解行")
assert OLD and NEW and sum("全佳" in l for l in NEW) == 1, "全佳 count != 1 in NEW"

# ---- 4. 總行數＋DEF（gift185／tang171／tang173） ----
def_new = check_content(40622, lambda s: "function openLoc(id, opts){" in s, "openLoc DEF")
print("total lines NEW:", open(ROOT + "/index.html", encoding="utf-8").read().count("\n"))
assert open(ROOT + "/index.html", encoding="utf-8").read().count("\n") == 45471

if "--apply" not in sys.argv:
    print("\nDRY RUN — no files changed. Re-run with --apply.")
    sys.exit(0)

HDR271 = "# v20a271 resync：index.html 淨 +91 行（支線第二批：交心旗＋陸頂一晚新機制＋初遇好感差異；插入點舊 L19690–39960；awei195 S4 wrap hook 改一行寫法保 3 行窗）；釘行按 difflib 映射重寫，內容逐字核實純漂移，見 qa271/resync271.py。\n"

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
out = HDR271 + out
open(ROOT + "/tests/test_travel114_static.py", "w", encoding="utf-8").write(out)
print("APPLIED: test_travel114_static.py")

# rom176（單次掃描 dict 查表）
out = single_pass_replace(TEST176, {"line(%d)" % o: "line(%d)" % n for o, n in rom_new.items()})
out = HDR271 + out
open(ROOT + "/tests/test_rom176_static.py", "w", encoding="utf-8").write(out)
print("APPLIED: test_rom176_static.py pins", rom_new)

# rom159（單次掃描 dict 查表；ok() 名內歷史行號唔郁）
rom159_table = {
    'line_has(25195, "v20a159 ROM159 Phase 1")': 'line_has(%d, "v20a159 ROM159 Phase 1")' % rom159_new[25195],
    'line_has(26029, "COMMIT48_NODES.CMT_lan_commit")': 'line_has(%d, "COMMIT48_NODES.CMT_lan_commit")' % rom159_new[26029],
    'line_has(25944, "function rom159SoMeetGate")': 'line_has(%d, "function rom159SoMeetGate")' % rom159_new[25944],
    'idx_lines[25223 - 1]': 'idx_lines[%d - 1]' % rom159_new[25223],
}
out = single_pass_replace(TEST159, rom159_table)
out = HDR271 + out
open(ROOT + "/tests/test_rom159_static.py", "w", encoding="utf-8").write(out)
print("APPLIED: test_rom159_static.py pins", rom159_new)

# gift185 / tang171 / tang173 — total + DEF（單次掃描 dict 查表）
for fname, is_tang in [("test_gift185_static.py", False),
                       ("test_tang171_static.py", True),
                       ("test_tang173_static.py", True)]:
    p = ROOT + "/tests/" + fname
    txt = open(p, encoding="utf-8").read()
    table = {
        "總行數 45380（": "總行數 45471（",
        "＋v269 +73）": "＋v269 +73＋v271 +91）",
        "== 45380": "== 45471",
    }
    if is_tang:
        table["openLoc DEF 行 40622（"] = "openLoc DEF 行 %d（" % def_new
        table["＋v269 +73，travel114 釘行"] = "＋v269 +73＋v271 +91，travel114 釘行"
        table["len(lines) >= 40628"] = "len(lines) >= %d" % (def_new + 6)
        table["lines[40621]"] = "lines[%d]" % (def_new - 1)
    txt = single_pass_replace(txt, table)
    txt = HDR271 + txt
    open(p, "w", encoding="utf-8").write(txt)
    print("APPLIED:", fname)
print("\nALL APPLIED")
