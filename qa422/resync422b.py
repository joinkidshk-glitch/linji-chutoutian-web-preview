# v422B resync: map HEAD(53212) -> new(53391) pins via difflib, single-pass dict per file.
import difflib, subprocess, re, sys
OLD = subprocess.run(["git","show","HEAD:index.html"],capture_output=True,text=True).stdout.split("\n")
NEW = open("index.html",encoding="utf-8").read().split("\n")
sm = difflib.SequenceMatcher(a=OLD,b=NEW,autojunk=False)
MP = {}
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2-i1): MP[i1+k] = j1+k
def m1(old1):  # 1-based
    n = MP.get(old1-1)
    return (n+1) if n is not None else None
def m0(old0):  # 0-based index
    return MP.get(old0)
assert len(NEW)-1 == 53391, len(NEW)-1
hdr = "# v422B resync：index.html 淨 +179 行（53212→53391）；釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa422/resync422b.py。\n"

def patch(path, fn):
    s = open(path,encoding="utf-8").read()
    if s.startswith("# v422B resync"):
        print("skip", path); return
    s2 = fn(s)
    if not s2.startswith("# v422B resync"):
        s2 = hdr + s2
    open(path,"w",encoding="utf-8").write(s2)
    print("patched", path)

def sub_once(s, pat, repl_fn, name):
    ms = list(re.finditer(pat, s))
    out, last = [], 0
    for mm in ms:
        out.append(s[last:mm.start()]); out.append(repl_fn(mm)); last = mm.end()
    out.append(s[last:])
    print(f"  {name}: {len(ms)} sites")
    return "".join(out)

# rom159 / rom176: line(N) / line_has(N,
for f in ["tests/test_rom159_static.py","tests/test_rom176_static.py"]:
    def fn(s):
        def rf(mm):
            n = int(mm.group(2)); nn = m1(n)
            assert nn is not None, (f, n)
            return mm.group(1) + str(nn) + mm.group(3)
        return sub_once(s, r"(line(?:_has)?\()(\d+)([,\)])", rf, f)
    patch(f, fn)

# travel114: COUNT_LINES/FREE_LINES sets + DEF/WRAPPER
def fn_travel(s):
    def rf(mm):
        n = int(mm.group(0)); nn = m1(n)
        assert nn is not None, ("travel", n)
        assert "openLoc(" in NEW[nn-1] or "openLoc" in NEW[nn-1], (n, nn, NEW[nn-1][:80])
        return str(nn)
    for name in ["COUNT_LINES","FREE_LINES"]:
        i = s.index(name + " = {"); j = s.index("}", i)
        seg = re.sub(r"(?m)^(\s+)(\d+)(,)", lambda mm: mm.group(1)+rf(type("M",(),{"group":lambda self,k=0: mm.group(2)})())+mm.group(3), s[i:j])
        s = s[:i] + seg + s[j:]
    for name in ["DEF_LINE","WRAPPER_LINE"]:
        mm = re.search(name + r" = (\d+)", s); n = int(mm.group(1)); nn = m1(n)
        assert nn is not None, name
        s = s[:mm.start(1)] + str(nn) + s[mm.end(1):]
        print(f"  {name}: {n}->{nn}")
    return s
patch("tests/test_travel114_static.py", fn_travel)

# tang171/173 + gift185: total 53212->53391, label +v422B +179; tang lines[47980] 0-based
for f in ["tests/test_tang171_static.py","tests/test_tang173_static.py","tests/test_gift185_static.py"]:
    def fn(s):
        s = s.replace("＋v422 +113）", "＋v422 +113＋v422B +179）").replace("＋v422 +111，travel114 釘行）", "＋v422 +111＋v422B +163，travel114 釘行）")
        s = s.replace("總行數 53212（", "總行數 53391（").replace("== 53212", "== 53391")
        def rf(mm):
            n = int(mm.group(1)); nn = m0(n)
            assert nn is not None, (f, n)
            return "lines[" + str(nn) + "]"
        return sub_once(s, r"lines\[(\d+)\]", rf, f)
    patch(f, fn)

# text125: ls[13099]/ls[13241]/ls[18989] 0-based pins
def fn_text(s):
    def rf(mm):
        n = int(mm.group(1)); nn = m0(n)
        assert nn is not None, ("text125", n)
        return "ls[" + str(nn) + "]"
    return sub_once(s, r"ls\[(\d+)\]", rf, "text125")
patch("tests/test_text125_static.py", fn_text)

# s30: widen body span (detail fn grew by v422B rows)
def fn_s30(s):
    assert "body_of('function castingNoticeDetailHtml', 12000)" in s
    return s.replace("body_of('function castingNoticeDetailHtml', 12000)", "body_of('function castingNoticeDetailHtml', 15000)")
patch("tests/test_s30text115_static.py", fn_s30)

# p361: negTagWarn361 copy updated by v422B
def fn_p361(s):
    old = "'這是負面印記，會影響結局' in ntw and '負面印記已有兩個' in ntw"
    assert old in s
    return s.replace(old, "'這是負面印記' in ntw and '天王與巨星那兩格最多容許一個' in ntw and '負面印記已有' in ntw")
patch("tests/test_p361_static.py", fn_p361)

# stamina58: hint copy updated
def fn_st(s):
    print("  stamina58 hint sites:", s.count("拳腳／體能"))
    return s.replace("拳腳／體能", "拳腳／體能 · 動作戲底子")
patch("tests/test_stamina58_static.py", fn_st)

# tape383_logic: harness needs canAudition-based v422 helpers (extract real fns)
def fn_tape(s):
    old = "  extractFn('tape383PickGig'),"
    assert old in s
    new = "  extractFn('reqGap'), extractFn('canAudition'), extractFn('v422Auditionable'), extractFn('v422PickAuditionable'),\n" + old
    return s.replace(old, new)
patch("tests/test_tape383_logic.js", fn_tape)
print("done")
