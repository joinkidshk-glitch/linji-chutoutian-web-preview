# v20a188 resync：index.html 淨 +225 行（AWARDS188 覆寫表＋角色閘，插入點全部喺 L45380–46310
# 頒獎區內：awardsEvalTier +9／覆寫表 +178／awardsStubCategory +9／buildAwardResultPack +9／
# __awards +2／gate line +5；VENUE99 報紙 dek 兩行原地改，行數不變）。
# 方法（沿用 qa131/resync_rebase157.py）：difflib SequenceMatcher 對位，基底行內容 vs 工作版行內容
# 逐字相同先叫純漂移；單次掃描 dict 查表一次過換，唔逐對 re.sub（v160 教訓：逐對 re.sub 會撞值）。
# 預期：釘行 <45380 者 +0，>46310 者 +225；總行數 60155→60380。
# 用法：python3 qa188/resync188.py [--apply]
# 無 --apply：只驗證＋印新數。--apply：改寫 5 份測試檔（只改 code 數字＋加 resync 註解；
# ok() 名標籤舊數字留返，同 v181／v186 做法一致；header 歷史註解唔郁）。
import difflib
import re
import subprocess
import sys

ROOT = "/home/hatch/workspace/linji-work188"
OLD = subprocess.run(["git", "show", "fc76b9e:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
print("old lines:", len(OLD) - 1, "new lines:", len(NEW) - 1, "net:", (len(NEW) - 1) - (len(OLD) - 1))

sm = difflib.SequenceMatcher(autojunk=False, a=OLD, b=NEW)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based
print("mapped equal lines:", len(mapping))

# 釘行清單：(檔, 舊行, 預期新行)
PINS = [
    ("gift185", 60155, 60380),  # 總行數（count('\n')，非行號，用總數驗）
    ("rom176", 6045, 6045), ("rom176", 31549, 31549),
    ("rom176", 53081, 53306), ("rom176", 53449, 53674),
    ("rom176", 54588, 54813), ("rom176", 54682, 54907),
    ("tang171", 54651, 54876), ("tang173", 54651, 54876),
    ("travel114", 32150, 32150), ("travel114", 35646, 35646), ("travel114", 37773, 37773),
    ("travel114", 38844, 38844), ("travel114", 39278, 39278), ("travel114", 39281, 39281),
    ("travel114", 39312, 39312), ("travel114", 43866, 43866),
    ("travel114", 58711, 58936), ("travel114", 58889, 59114),
    ("travel114", 59032, 59257), ("travel114", 59053, 59278),
    ("travel114", 24659, 24659), ("travel114", 28194, 28194),
    ("travel114", 30817, 30817), ("travel114", 30818, 30818),
    ("travel114", 30830, 30830), ("travel114", 30831, 30831),
    ("travel114", 30842, 30842), ("travel114", 30843, 30843),
    ("travel114", 30946, 30946), ("travel114", 40821, 40821),
    ("travel114", 43523, 43523), ("travel114", 43546, 43546),
    ("travel114", 52904, 53129), ("travel114", 53023, 53248),
    ("travel114", 53073, 53298), ("travel114", 53296, 53521),
    ("travel114", 53335, 53560), ("travel114", 53341, 53566),
    ("travel114", 53408, 53633), ("travel114", 53410, 53635),
    ("travel114", 53413, 53638), ("travel114", 53440, 53665),
    ("travel114", 54551, 54776), ("travel114", 54925, 55150),
    ("travel114", 54947, 55172), ("travel114", 55098, 55323),
    ("travel114", 56735, 56960), ("travel114", 58479, 58704),
    ("travel114", 58597, 58822), ("travel114", 58598, 58823),
    ("travel114", 58633, 58858), ("travel114", 58634, 58859),
    ("travel114", 58659, 58884), ("travel114", 59503, 59728),
    ("travel114", 54651, 54876),  # DEF_LINE
    ("travel114", 44353, 44353),  # WRAPPER_LINE
]
bad = []
for name, old, new in PINS:
    if name == "gift185":
        continue  # 總數另外驗
    got = mapping.get(old)
    ok = got == new and OLD[old - 1] == NEW[new - 1]
    print(("OK  " if ok else "BAD ") + f"{name} {old} -> {new} (difflib: {got}) :: {OLD[old-1].strip()[:70]}")
    if not ok:
        bad.append((name, old, new, got))
assert (len(NEW) - 1) - (len(OLD) - 1) == 225, "net drift is not +225"
assert not bad, f"{len(bad)} pins failed difflib verification"

# openLoc( 序列一致（travel114 分類之前提）
old_seq = [l.strip() for l in OLD if "openLoc(" in l]
new_seq = [l.strip() for l in NEW if "openLoc(" in l]
assert old_seq == new_seq, "openLoc( sequence differs — not a pure shift!"
print(f"openLoc( sequence identical: {len(old_seq)} call sites, pure shift confirmed")

# gift185 總數
print("total newlines new:", open(ROOT + "/index.html", encoding="utf-8").read().count("\n"))

if "--apply" not in sys.argv:
    print("\nDRY RUN — no files changed. Re-run with --apply to rewrite the 5 test files.")
    sys.exit(0)

# ---- apply：單次掃描 dict 查表 ----
def resync_file(rel, replacements, header_note):
    """replacements: list of (old_literal, new_literal) — 只換完全相符嘅行內字面，逐行掃一次。"""
    p = ROOT + "/" + rel
    lines = open(p, encoding="utf-8").read().split("\n")
    rep = dict(replacements)
    out = []
    n_changed = 0
    for ln in lines:
        done = ln
        for old, new in rep.items():
            if old in done:
                done = done.replace(old, new)
                n_changed += 1
        out.append(done)
    txt = "\n".join(out)
    if header_note:
        # 加喺第一個 # v20a186 resync 註解之後（每檔都有），唔郁其他歷史註解
        anchor = "# v20a186 resync："
        i = txt.find(anchor)
        assert i >= 0, rel + " has no v186 resync anchor"
        j = txt.find("\n", i)
        txt = txt[:j + 1] + header_note + txt[j + 1:]
    open(p, "w", encoding="utf-8").write(txt)
    print(f"applied {rel}: {n_changed} replacements")

NOTE188 = ("# v20a188 resync：index.html 淨 +225 行（AWARDS188 覆寫表＋角色閘，插入點 L45380–46310）；"
           "其後釘行各 +225，之前唔郁；總行數 60155→60380。\n")
resync_file("tests/test_gift185_static.py",
            [("html.count('\\\\n') == 60155", "html.count('\\\\n') == 60380")], NOTE188)
resync_file("tests/test_rom176_static.py",
            [("line(53081)", "line(53306)"), ("line(53449)", "line(53674)"),
             ("line(54588)", "line(54813)"), ("line(54682)", "line(54907)")], NOTE188)
resync_file("tests/test_tang171_static.py",
            [("src.count('\\\\n') == 60155", "src.count('\\\\n') == 60380"),
             ("len(lines) >= 54651 and 'function openLoc(id, opts){' in lines[54650]",
              "len(lines) >= 54876 and 'function openLoc(id, opts){' in lines[54875]")], NOTE188)
resync_file("tests/test_tang173_static.py",
            [("src.count('\\\\n') == 60155", "src.count('\\\\n') == 60380"),
             ("len(lines) >= 54651 and 'function openLoc(id, opts){' in lines[54650]",
              "len(lines) >= 54876 and 'function openLoc(id, opts){' in lines[54875]")], NOTE188)
# travel114：只換 set 入面裸數行（行首數字＋逗號）同 DEF_LINE 賦值行，唔掂 header 註解
p = ROOT + "/tests/test_travel114_static.py"
lines = open(p, encoding="utf-8").read().split("\n")
shift = {}
for name, old, new in PINS:
    if name == "travel114" and old != new:
        shift[old] = new
in_count = in_free = False
changed = 0
for idx, ln in enumerate(lines):
    if ln.startswith("COUNT_LINES"):
        in_count = True
    elif ln.startswith("FREE_LINES"):
        in_free = True
    elif ln.startswith("FREE_FLAGS"):
        in_count = in_free = False
    if (in_count or in_free) and re.match(r"^\s*\d+,$", ln):
        n = int(ln.strip().rstrip(","))
        if n in shift:
            lines[idx] = ln.replace(str(n), str(shift[n]))
            changed += 1
    if ln.startswith("DEF_LINE = 54651"):
        lines[idx] = ln.replace("54651", "54876")
        changed += 1
txt = "\n".join(lines)
anchor = "# v20a181 resync："
i = txt.find(anchor)
assert i >= 0
j = txt.find("\n", i)
txt = txt[:j + 1] + NOTE188 + txt[j + 1:]
open(p, "w", encoding="utf-8").write(txt)
print(f"applied tests/test_travel114_static.py: {changed} replacements")
print("\nAPPLIED. Re-run the 5 tests to confirm.")
