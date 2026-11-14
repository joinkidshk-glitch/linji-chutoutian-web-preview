"""Apply part of resync212_rebase: rewrite pins in the 5 conflicted test files
from their v212-side versions using the difflib mapping computed in
resync212_rebase.py. Run: python3 qa212/resync212_rebase_apply.py
Writes corrected files into the worktree (resolving the rebase conflicts).
"""
import difflib
import re
import subprocess
import sys

REPO = "/home/hatch/workspace/linji-work212"
OLD_HTML = "/tmp/resync212r/index_v212.html"


def show(rev, path):
    return subprocess.check_output(["git", "show", f"{rev}:{path}"],
                                   cwd=REPO, text=True)


old = open(OLD_HTML).read().split("\n")
new = open(REPO + "/index.html").read().split("\n")
sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1

TOTAL_NEW = len(new) - 1  # split('\n') trailing element
assert TOTAL_NEW == 61795, TOTAL_NEW


def m(n):
    assert n in mapping, f"line {n} not in an equal block"
    return mapping[n]


def load_v212(path):
    return show("30d07fb", path)


def write(path, text):
    with open(REPO + "/" + path, "w") as f:
        f.write(text)


# ---------- gift185 ----------
p = "tests/test_gift185_static.py"
t = load_v212(p)
t2 = t.replace(
    "ok('總行數 61753（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v212 +39）', html.count('\\n') == 61753)",
    "ok('總行數 61795（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39）', html.count('\\n') == 61795)  # v20a212 rebase 上 main b1ca47a resync：v211 +42＋v212 +39，qa212/resync212_rebase.py difflib 核實純漂移")
assert t2 != t
write(p, t2)
print("gift185: total 61753 -> 61795")

# ---------- tang171 / tang173 ----------
for p in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    t = load_v212(p)
    ol = m(56225)
    t2 = t.replace(
        "ok('零行數漂移：總行數 61753（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v212 +39）', src.count('\\n') == 61753)",
        "ok('零行數漂移：總行數 61795（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39）', src.count('\\n') == 61795)  # v20a212 rebase 上 main b1ca47a resync，qa212/resync212_rebase.py difflib 核實純漂移")
    t2 = t2.replace(
        "   len(lines) >= 56186 and 'function openLoc(id, opts){' in lines[56224])",
        f"   len(lines) >= {ol} and 'function openLoc(id, opts){{' in lines[{ol - 1}])")
    assert t2 != t, p
    assert "61753" not in t2.split("v193 61167")[1][:200], p
    write(p, t2)
    print(f"{p.split('/')[-1]}: total -> 61795, openLoc -> {ol}")

# ---------- rom176 ----------
p = "tests/test_rom176_static.py"
t = load_v212(p)
repl = [
    ("ok('釘：NPCS lan 條目 L6151', line(6152).startswith('  lan:{ id:\"lan\", name:\"藍若曦\"'))",
     "ok('釘：NPCS lan 條目 L6152', line(6152).startswith('  lan:{ id:\"lan\", name:\"藍若曦\"'))"),
    ("'GIFT_REACT = giftReact' in line(31713) and 'rom176ApplyGiftOverrides()' in line(31713))",
     "'GIFT_REACT = giftReact' in line(31713) and 'rom176ApplyGiftOverrides()' in line(31713))"),
    ("ok('釘：ROM176 block 起點 L54616', line(54655).startswith('/* ===== v20a176 ROM176'))",
     "ok('釘：ROM176 block 起點 L54697', line(54697).startswith('/* ===== v20a176 ROM176'))"),
    ("ok('釘：rom176ApplyGiftOverrides 定義 L54984', line(55023).startswith('function rom176ApplyGiftOverrides()'))",
     "ok('釘：rom176ApplyGiftOverrides 定義 L55065', line(55065).startswith('function rom176ApplyGiftOverrides()'))"),
    ("ok('釘：addLocTalkGiftActs L56123', line(56162).startswith('function addLocTalkGiftActs(add, L, npcId)'))",
     "ok('釘：addLocTalkGiftActs L56204', line(56204).startswith('function addLocTalkGiftActs(add, L, npcId)'))"),
    ("ok('釘：openLoc rom176 攔截 L56217', 'rom176TryIntercept(id)' in line(56256))",
     "ok('釘：openLoc rom176 攔截 L56298', 'rom176TryIntercept(id)' in line(56298))"),
    ("# v20a212 resync：釘行按 difflib 映射重寫（6151→6152、31712→31713、54616→54655、54984→55023、56123→56162、56217→56256），qa212/resync212.py 核實純漂移。",
     "# v20a212 rebase 上 main b1ca47a resync：釘行按 difflib 映射重寫（6152→6152、31713→31713、54655→54697、55023→55065、56162→56204、56256→56298），qa212/resync212_rebase.py 核實純漂移。"),
]
for a, b in repl:
    assert a in t, f"rom176 anchor missing: {a[:60]}"
    t = t.replace(a, b)
write(p, t)
print("rom176: 54655->54697, 55023->55065, 56162->56204, 56256->56298 (6152/31713 unchanged)")

# ---------- travel114 ----------
p = "tests/test_travel114_static.py"
t = load_v212(p)
lines = t.split("\n")


def remap_block(ls, start_marker, end_marker):
    out = []
    in_block = False
    for ln in ls:
        if start_marker in ln:
            in_block = True
            out.append(ln)
            continue
        if in_block and ln.strip() == end_marker:
            in_block = False
            out.append(ln)
            continue
        if in_block:
            # replace standalone integers (line numbers) via mapping
            def sub_num(mo):
                n = int(mo.group(0))
                return str(m(n))
            ln = re.sub(r"\b\d{5}\b", sub_num, ln)
        out.append(ln)
    return out


lines = remap_block(lines, "COUNT_LINES = {", "}")
lines = remap_block(lines, "FREE_LINES = {", "}")
t = "\n".join(lines)
t = t.replace("DEF_LINE = 56225      # function openLoc(id, opts){",
              f"DEF_LINE = {m(56225)}      # function openLoc(id, opts){{")
t = t.replace("WRAPPER_LINE = 45181  # window.__phase2.openLoc：轉發 opts",
              f"WRAPPER_LINE = {m(45181)}  # window.__phase2.openLoc：轉發 opts")
# add a resync note after the COUNT_LINES v211 comment is gone (v212 side has none);
# append note to the DEF_LINE comment area instead: insert after WRAPPER_LINE line
t = t.replace(
    f"WRAPPER_LINE = {m(45181)}  # window.__phase2.openLoc：轉發 opts",
    f"WRAPPER_LINE = {m(45181)}  # window.__phase2.openLoc：轉發 opts\n# v20a212 rebase 上 main b1ca47a resync：COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫，qa212/resync212_rebase.py 核實純漂移（v211 +42 段內逐段 shift）。")
assert "56225" not in t.split("DEF_LINE")[0][-200:], "stale DEF"
write(p, t)
print(f"travel114: DEF -> {m(56225)}, WRAPPER -> {m(45181)}, COUNT/FREE remapped")

print("done")
