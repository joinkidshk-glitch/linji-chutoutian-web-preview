#!/usr/bin/env python3
# qa161/resync161_rebase.py — rebase 版：對 origin/main (9346a8e) 核實純漂移。
# 改動：index.html 喺舊行 4771（/* === v20a53 完 === */）之後淨插入 14 行
# （v161 註解＋規則區塊），其餘逐字不變。以下驗證：
#  ① 刪走 14 行插入段 → 得出嘅 prev 同 git HEAD:index.html 逐字相同；
#  ② difflib 對位：test_travel114_static.py 全部釘行（COUNT 13／FREE 27／DEF／WRAPPER）
#     ＋ test_text125_static.py 3 個釘行（27800／27913／33516）映射去新行號，內容逐字相同；
#  ③ 44 個 openLoc( 呼叫點序列逐字一致。
# 用法：python3 qa161/resync161.py（在 ~/workspace/linji-work161 執行）
import difflib, re, subprocess, sys

new_src = open("index.html", encoding="utf-8").read()
new_lines = new_src.split("\n")

# 定位插入段（新行號）：由 /* === v20a161 開頭到 /* === v20a161 完 === */ 尾
start = next(i for i, l in enumerate(new_lines) if l.startswith("/* === v20a161"))
end = next(i for i, l in enumerate(new_lines) if l.startswith("/* === v20a161 完 === */"))
print("insert block new lines %d-%d (%d lines)" % (start + 1, end + 1, end - start + 1))
assert end - start + 1 == 14, "insert block must be exactly 14 lines"
prev_lines = new_lines[:start] + new_lines[end + 1:]
prev_src = "\n".join(prev_lines)

head_src = subprocess.check_output(["git", "show", "origin/main:index.html"], text=True)
print("prev == HEAD:index.html:", prev_src == head_src)
assert prev_src == head_src, "reconstructed prev differs from HEAD"

sm = difflib.SequenceMatcher(a=prev_lines, b=new_lines, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1
    else:
        print("CHANGE %s prev %d-%d -> new %d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))

fail = 0
def check(label, old_ln):
    global fail
    nl = mapping.get(old_ln)
    ok = nl is not None and prev_lines[old_ln - 1] == new_lines[nl - 1]
    if not ok:
        fail += 1
    print("%s %d -> %s %s | %s" % (label, old_ln, nl, "OK" if ok else "MISMATCH",
          (prev_lines[old_ln - 1].strip()[:60] if old_ln <= len(prev_lines) else "?")))

t114 = open("tests/test_travel114_static.py", encoding="utf-8").read()
def parse_set(name):
    m = re.search(name + r"\s*=\s*\{([^}]*)\}", t114, re.S)
    return sorted(int(x) for x in re.findall(r"\d+", m.group(1)))
for ln in parse_set("COUNT_LINES"):
    check("COUNT", ln)
for ln in parse_set("FREE_LINES"):
    check("FREE", ln)
check("DEF", int(re.search(r"DEF_LINE = (\d+)", t114).group(1)))
check("WRAP", int(re.search(r"WRAPPER_LINE = (\d+)", t114).group(1)))

for ln in (27815, 27928, 33550):  # rebase 版：舊釘行 = origin/main (9346a8e) 嗰組
    check("TEXT125", ln)

def calls(lines):
    return [(i + 1, l.strip()) for i, l in enumerate(lines) if "openLoc(" in l]
oc, nc = calls(prev_lines), calls(new_lines)
print("openLoc call sites: prev %d new %d" % (len(oc), len(nc)))
seq_ok = len(oc) == len(nc) and all(a[1] == b[1] for a, b in zip(oc, nc))
print("call-site content sequence identical:", seq_ok)
if not seq_ok:
    fail += 1
print("RESULT " + ("FAIL (%d)" % fail if fail else "PASS"))
sys.exit(1 if fail else 0)
