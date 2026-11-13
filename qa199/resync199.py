# -*- coding: utf-8 -*-
"""v20a199 resync：difflib 對位 pristine main (b1633e6) → work index.html，
核實漂移純粹係 v199 改動，再映射 8 檔靜態測試嘅行號釘。
v199 改動（淨 +44 行，60602→60646）：
  (1) DLG199 參考 AR＋輔助函數（DLG108 模組，dlg108FitPct 之前，約 L26985）＋30 行；
  (2) dlg108FitApply 單人步／雙人步正規化＋天花板（約 L27030–27070）＋14 行；
  (3) window.DLG108 匯出加 4 鍵（同區，＋1 行，計入 (2) 嗰 +14 入面）；
  (4) WF4 對話圖加 onload（約 L40760，＋1 行：註解＋onload，淨 +1）；
  (5) 兩 bust data URI 換值（PORTRAITS.hero_awi／BUST109_EXTRA.awi_s3，行數不變，內容換）。
用法：python3 qa199/resync199.py [--apply]
  無 --apply：淨係印映射＋核實（BAD 必須係 0 先可以 --apply）。
  有 --apply：按映射更新測試檔（單次掃描 dict 查表，唔逐對 re.sub）。
"""
import ast, difflib, os, re, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work199"
APPLY = "--apply" in sys.argv

# 沙箱寫入限制（2026-11-13 15:0x 起）：單次 write() ≥8192 bytes 俾 EPERM。
# 所以檔案寫入一律用 4096-byte chunk + temp + os.replace，唔好直接 open(p, "w").write()。
CHUNK = 4096
def write_file(path, text):
    tmp = path + ".tmp199"
    data = text.encode("utf-8")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        off = 0
        while off < len(data):
            off += os.write(fd, data[off:off + CHUNK])
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, path)

def git_show(rev, path):
    return subprocess.check_output(["git", "show", "%s:%s" % (rev, path)],
                                   cwd=ROOT, text=True).split("\n")

old = git_show("b1633e6", "index.html")
new = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
print("old lines:", len(old) - 1, "new lines:", len(new) - 1,
      "net:", (len(new) - 1) - (len(old) - 1))

sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
hunks = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1
    else:
        hunks.append((tag, i1 + 1, i2, j1 + 1, j2))
print("change hunks (old 1-based range -> new 1-based range):")
for tag, a1, a2, b1, b2 in hunks:
    print("  %s old L%d-%d -> new L%d-%d" % (tag, a1, a2, b1, b2))

# 釘（1-based 舊行號；0-based 嗰啲另外註明）
PINS = {
    "rom176": [6072, 31586, 53525, 53893, 55032, 55126],
    "tang152_0based": [25819, 31513, 31657],  # test 用 lines()[idx]（0-based）；呢度存 1-based 行號，apply 嗰陣先 −1
    "kwan151": [25659, 26000, 26003, 26004, 26005, 26048, 26267, 27217, 27250,
                31023, 31031, 31032, 31074],
    "travel114_DEF": [55095],
    "travel114_WRAPPER": [44436],
    "tang171_173_DEF_0based": [55095],  # test 用 lines[55094]（0-based）；呢度存 1-based
    "text125_0based": [27742, 27871, 33574],  # test 用 ls[idx]（0-based）；呢度存 1-based
}
# travel114 COUNT／FREE 由 test 檔本身 parse（唔手抄，防抄錯）
_t = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read()
def _parse_set(name):
    m = re.search(name + r"\s*=\s*(\{[^}]*\})", _t, re.S)
    return sorted(ast.literal_eval(m.group(1)))
PINS["travel114_COUNT"] = _parse_set("COUNT_LINES")
PINS["travel114_FREE"] = _parse_set("FREE_LINES")
print("travel114 COUNT %d 項／FREE %d 項（由 test 檔 parse）"
      % (len(PINS["travel114_COUNT"]), len(PINS["travel114_FREE"])))

print("\npin mapping (b1633e6 -> work, content must match verbatim):")
bad = 0
mapped = {}
for group, lines in PINS.items():
    for ln in lines:
        nl = mapping.get(ln)
        if nl is None:
            print("  %s L%d -> ??? (line itself changed!)" % (group, ln))
            bad += 1
            continue
        same = old[ln - 1] == new[nl - 1]
        if not same:
            bad += 1
        mapped[(group, ln)] = nl
        print("  %s L%d -> L%d %s :: %s" % (group, ln, nl, "OK" if same else "CONTENT DIFF!",
              old[ln - 1].strip()[:80]))
print("\nBAD:", bad)
if bad:
    raise SystemExit(1)

# 總行數
print("total lines: old 60602 -> new %d" % (len(new) - 1))
assert (len(new) - 1) == 60646

if not APPLY:
    print("\n(dry run；加 --apply 先會寫測試檔）")
    raise SystemExit(0)

# ---------- 寫入：單次掃描 dict 查表 ----------
def sub_numbers_span(text, start_pat, end_pat, table):
    """只喺 start_pat…end_pat 區間內，將整數 token 按 table 換（單次掃描）。"""
    a = text.index(start_pat)
    b = text.index(end_pat, a) + len(end_pat)
    span = text[a:b]
    def rep(m):
        n = int(m.group(0))
        return str(table[n]) if n in table else m.group(0)
    return text[:a] + re.sub(r"\d+", rep, span) + text[b:]

def sub_exact(text, pairs):
    """pairs：(舊字串, 新字串)；每個舊字串必須至少出現一次，全部換走
    （同一釘可以喺同一行出現多次，例如 line(31586) 兩次、line(31023) 四次）。
    冪等：如果舊字串已唔見而新字串已在，就跳過（上一輪已更新，重跑唔會死）。"""
    for o, n in pairs:
        if text.count(o) == 0:
            assert text.count(n) >= 1, "pattern not found (and new not present): %r" % o
            continue
        text = text.replace(o, n)
    return text

# rom176 已喺上一輪 --apply 更新兼 PASS，呢輪跳過（sub_exact 冪等都會跳過）。
# tang152：lines()[idx]（0-based → 0-based）
# （上一輪 EPERM 截斷咗呢個檔，之後 rm 咗；如果唔見咗，先由 git blob 還原再 resync。）
p = ROOT + "/tests/test_tang152_static.py"
if not os.path.exists(p):
    blob = subprocess.check_output(["git", "show", "HEAD:tests/test_tang152_static.py"],
                                   cwd=ROOT)
    write_file(p, blob.decode("utf-8"))
    print("restored test_tang152_static.py from HEAD (%d bytes)" % len(blob))
s = open(p, encoding="utf-8").read()
for ln1 in PINS["tang152_0based"]:
    nl1 = mapped[("tang152_0based", ln1)]
    s = sub_exact(s, [("lines()[%d]" % (ln1 - 1), "lines()[%d]" % (nl1 - 1))])
write_file(p, s)
print("updated test_tang152_static.py")

# kwan151：line(N)
p = ROOT + "/tests/test_kwan151_static.py"
s = open(p, encoding="utf-8").read()
for ln in PINS["kwan151"]:
    s = sub_exact(s, [("line(%d)" % ln, "line(%d)" % mapped[("kwan151", ln)])])
write_file(p, s)
print("updated test_kwan151_static.py")

# travel114：FREE_LINES／COUNT_LINES 區間內換數＋DEF／WRAPPER 賦值
p = ROOT + "/tests/test_travel114_static.py"
s = open(p, encoding="utf-8").read()
free_table = {ln: mapped[("travel114_FREE", ln)] for ln in PINS["travel114_FREE"]}
count_table = {ln: mapped[("travel114_COUNT", ln)] for ln in PINS["travel114_COUNT"]}
s = sub_numbers_span(s, "FREE_LINES = {", "}", free_table)
s = sub_numbers_span(s, "COUNT_LINES = {", "}", count_table)
s = sub_exact(s, [
    ("DEF_LINE = 55095", "DEF_LINE = %d" % mapped[("travel114_DEF", 55095)]),
    ("WRAPPER_LINE = 44436", "WRAPPER_LINE = %d" % mapped[("travel114_WRAPPER", 44436)]),
])
s = s.replace("# v20a198 resync：",
              "# v20a199 resync：index.html 淨 +44 行（DLG199 ＋30／fitApply ＋13／WF4 onload ＋1）；"
              "COUNT／FREE／DEF／WRAPPER 按 difflib 映射重算，內容逐字核實純漂移。\n# v20a198 resync：", 1)
write_file(p, s)
print("updated test_travel114_static.py")

# tang171／tang173：總行數＋openLoc DEF（0-based lines[55094]）
for fn in ("test_tang171_static.py", "test_tang173_static.py"):
    p = ROOT + "/tests/" + fn
    s = open(p, encoding="utf-8").read()
    nl1 = mapped[("tang171_173_DEF_0based", 55095)]
    s = sub_exact(s, [
        ("總行數 60602", "總行數 60646"),
        ("== 60602", "== 60646"),
        ("lines[55094]", "lines[%d]" % (nl1 - 1)),
    ])
    write_file(p, s)
    print("updated", fn)

# gift185：總行數
p = ROOT + "/tests/test_gift185_static.py"
s = open(p, encoding="utf-8").read()
s = sub_exact(s, [("總行數 60602", "總行數 60646"), ("== 60602", "== 60646")])
write_file(p, s)
print("updated test_gift185_static.py")

# text125：ls[idx]（0-based）＋報錯字串入面嘅 1-based 行號
p = ROOT + "/tests/test_text125_static.py"
s = open(p, encoding="utf-8").read()
pairs = []
for ln1 in PINS["text125_0based"]:
    nl1 = mapped[("text125_0based", ln1)]
    pairs.append(("ls[%d]" % (ln1 - 1), "ls[%d]" % (nl1 - 1)))
    pairs.append(("第 %d 行" % ln1, "第 %d 行" % nl1))
s = sub_exact(s, pairs)
write_file(p, s)
print("updated test_text125_static.py")

print("APPLY DONE")
