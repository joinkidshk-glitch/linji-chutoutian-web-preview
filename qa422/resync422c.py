# v422C resync: map HEAD(53391) -> new(53420) pins via difflib, single-pass dict per file.
import difflib, subprocess, re
OLD = subprocess.run(["git","show","HEAD:index.html"],capture_output=True,text=True).stdout.split("\n")
NEW = open("index.html",encoding="utf-8").read().split("\n")
sm = difflib.SequenceMatcher(a=OLD,b=NEW,autojunk=False)
MP = {}
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2-i1): MP[i1+k] = j1+k
def m1(old1):
    n = MP.get(old1-1)
    return (n+1) if n is not None else None
def m0(old0):
    return MP.get(old0)
assert len(NEW)-1 == 53420, len(NEW)-1
hdr = "# v422C resync：index.html 淨 +29 行（53391→53420）；釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa422/resync422c.py。\n"

def patch(path, fn):
    s = open(path,encoding="utf-8").read()
    if s.startswith("# v422C resync"):
        print("skip", path); return
    s2 = fn(s)
    if not s2.startswith("# v422C resync"):
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
    def fn(s, f=f):
        def rf(mm):
            n = int(mm.group(2)); nn = m1(n)
            assert nn is not None, (f, n)
            return mm.group(1) + str(nn) + mm.group(3)
        s = sub_once(s, r"(line(?:_has)?\()(\d+)([,\))])", rf, f)
        def rf0(mm):
            n = int(mm.group(1)); nn = m0(n)
            assert nn is not None, (f, n)
            return "idx_lines[" + str(nn) + "]"
        return sub_once(s, r"idx_lines\[(\d+)\]", rf0, f + " idx_lines")
    patch(f, fn)

# travel114: COUNT_LINES/FREE_LINES sets + DEF/WRAPPER
def fn_travel(s):
    def rf(n):
        nn = m1(n)
        assert nn is not None, ("travel", n)
        assert "openLoc" in NEW[nn-1], (n, nn, NEW[nn-1][:80])
        return nn
    for name in ["COUNT_LINES","FREE_LINES"]:
        i = s.index(name + " = {"); j = s.index("}", i)
        seg = re.sub(r"(?m)^(\s+)(\d+)(,)", lambda mm: mm.group(1)+str(rf(int(mm.group(2))))+mm.group(3), s[i:j])
        s = s[:i] + seg + s[j:]
    for name in ["DEF_LINE","WRAPPER_LINE"]:
        mm = re.search(name + r" = (\d+)", s); n = int(mm.group(1)); nn = m1(n)
        assert nn is not None, name
        s = s[:mm.start(1)] + str(nn) + s[mm.end(1):]
        print(f"  {name}: {n}->{nn}")
    return s
patch("tests/test_travel114_static.py", fn_travel)

# tang171/173 + gift185: total 53391->53420, label +v422C +27; openLoc DEF mapped; tang lines[] 0-based
for f in ["tests/test_tang171_static.py","tests/test_tang173_static.py","tests/test_gift185_static.py"]:
    def fn(s, f=f):
        s = s.replace("＋v422B +179）", "＋v422B +179＋v422C +29）").replace("＋v422B +163，travel114 釘行）", "＋v422B +163＋v422C +29，travel114 釘行）")
        s = s.replace("總行數 53391（", "總行數 53420（").replace("== 53391", "== 53420")
        def rf(mm):
            n = int(mm.group(1)); nn = m0(n)
            assert nn is not None, (f, n)
            return "lines[" + str(nn) + "]"
        return sub_once(s, r"lines\[(\d+)\]", rf, f)
    patch(f, fn)

# tang152: lines()[17100]/[17225] 0-based pins
def fn152(s):
    def rf(mm):
        n = int(mm.group(1)); nn = m0(n)
        assert nn is not None, ("tang152", n)
        return "lines()[" + str(nn) + "]"
    return sub_once(s, r"lines\(\)\[(\d+)\]", rf, "tang152")
patch("tests/test_tang152_static.py", fn152)

# text125: ls[] 0-based pins
def fn_text(s):
    def rf(mm):
        n = int(mm.group(1)); nn = m0(n)
        assert nn is not None, ("text125", n)
        return "ls[" + str(nn) + "]"
    return sub_once(s, r"ls\[(\d+)\]", rf, "text125")
patch("tests/test_text125_static.py", fn_text)
print("done")
