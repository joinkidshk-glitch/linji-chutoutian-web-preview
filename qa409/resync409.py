#!/usr/bin/env python3
"""v409 resync：difflib 映射 HEAD(1a24cb1) index.html → 新版，更新釘行測試。"""
import difflib, os, re, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git","show","1a24cb1:index.html"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT,"index.html"), encoding="utf-8").read().split("\n")
print("OLD", len(OLD)-1, "NEW", len(NEW)-1)
_sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
_map = {}
for tag,i1,i2,j1,j2 in _sm.get_opcodes():
    if tag=="equal":
        for k in range(i2-i1): _map[i1+k]=j1+k
def map_line(n):
    m=_map.get(n-1); assert m is not None, f"line {n} not equal-mapped"
    assert OLD[n-1]==NEW[m], f"line {n} content changed"
    return m+1
def read(p): return open(os.path.join(ROOT,p),encoding="utf-8").read()
def write(p,s): open(os.path.join(ROOT,p),"w",encoding="utf-8").write(s)
NOTE="# v409 resync：釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa409/resync409.py。"
def patch(path, subs):
    src=read(path)
    if src.split("\n")[0].startswith("# v409 resync"): print("skip",path); return
    for old,new,n in subs:
        c=src.count(old); assert c==n, f"{path}: {old[:60]!r} count={c} expect={n}"
        src=src.replace(old,new)
    lines=src.split("\n"); lines.insert(0,NOTE); write(path,"\n".join(lines)); print("patched",path)

old_total=len(OLD)-1; new_total=len(NEW)-1
# gift185/tang171/tang173 total + pins (discover current pins)
for path in ("tests/test_gift185_static.py","tests/test_tang171_static.py","tests/test_tang173_static.py"):
    src=read(path); subs=[]
    if f"== {old_total}" in src: subs.append((f"== {old_total}", f"== {new_total}", src.count(f"== {old_total}")))
    if f"總行數 {old_total}（" in src: subs.append((f"總行數 {old_total}（", f"總行數 {new_total}（", 1))
    for m in re.finditer(r"lines\[(\d+)\]", src):
        n=int(m.group(1)); subs.append((f"lines[{n}]", f"lines[{map_line(n+1)-1}]", src.count(f"lines[{n}]")))
    # dedupe subs by old
    seen={}; 
    for o,nw,c in subs: seen[o]=(nw,c)
    patch(path, [(o,v[0],v[1]) for o,v in seen.items()])

# rom159 line_has + idx_lines
src=read("tests/test_rom159_static.py"); subs=[]
for m in re.finditer(r"line_has\((\d+),", src):
    n=int(m.group(1)); subs.append((f"line_has({n},", f"line_has({map_line(n)},", src.count(f"line_has({n},")))
for m in re.finditer(r"idx_lines\[(\d+)\]", src):
    n=int(m.group(1)); subs.append((f"idx_lines[{n}]", f"idx_lines[{map_line(n+1)-1}]", src.count(f"idx_lines[{n}]")))
seen={}
for o,nw,c in subs: seen[o]=(nw,c)
patch("tests/test_rom159_static.py", [(o,v[0],v[1]) for o,v in seen.items()])

# rom176 line()
src=read("tests/test_rom176_static.py"); subs=[]
for m in re.finditer(r"line\((\d+)\)", src):
    n=int(m.group(1)); subs.append((f"line({n})", f"line({map_line(n)})", src.count(f"line({n})")))
seen={}
for o,nw,c in subs: seen[o]=(nw,c)
patch("tests/test_rom176_static.py", [(o,v[0],v[1]) for o,v in seen.items()])

# tang152 lines()[]
src=read("tests/test_tang152_static.py"); subs=[]
for m in re.finditer(r"lines\(\)\[(\d+)\]", src):
    n=int(m.group(1)); subs.append((f"lines()[{n}]", f"lines()[{map_line(n+1)-1}]", src.count(f"lines()[{n}]")))
seen={}
for o,nw,c in subs: seen[o]=(nw,c)
patch("tests/test_tang152_static.py", [(o,v[0],v[1]) for o,v in seen.items()])

# text125 ls[] + message line numbers: current pins from failure (12604/12746/18462 in messages; ls pins = msg-1)
src=read("tests/test_text125_static.py"); subs=[]
for m in re.finditer(r"ls\[(\d+)\]", src):
    n=int(m.group(1))
    try: nw=map_line(n+1)-1
    except AssertionError: continue
    subs.append((f"ls[{n}]", f"ls[{nw}]", src.count(f"ls[{n}]")))
for label in ("currentLine","advance","applyFamilySafeToNode"):
    m=re.search(label+r" 第 (\d+) 行", src)
    if m:
        n=int(m.group(1)); subs.append((f"{label} 第 {n} 行", f"{label} 第 {map_line(n)} 行", 1))
seen={}
for o,nw,c in subs: seen[o]=(nw,c)
patch("tests/test_text125_static.py", [(o,v[0],v[1]) for o,v in seen.items()])

# travel114 sets single-scan dict + DEF/WRAPPER
p114="tests/test_travel114_static.py"; src=read(p114)
assert not src.split("\n")[0].startswith("# v409 resync")
for setname in ("COUNT_LINES","FREE_LINES"):
    m=re.search(setname+r" = \{(.*?)\n\}", src, re.S); assert m, setname
    body=m.group(1); nums=[int(x) for x in re.findall(r"^\s*(\d+),", body, re.M)]
    table={str(n):str(map_line(n)) for n in nums}
    newbody=re.sub(r"^(\s*)(\d+),", lambda mm: mm.group(1)+table[mm.group(2)]+",", body, flags=re.M)
    src=src[:m.start(1)]+newbody+src[m.end(1):]
    print(setname, len(nums), "mapped")
for name in ("DEF_LINE","WRAPPER_LINE"):
    m=re.search(name+r" = (\d+)", src)
    if m: src=src.replace(f"{name} = {m.group(1)}", f"{name} = {map_line(int(m.group(1)))}", 1)
lines=src.split("\n"); lines.insert(0,NOTE); write(p114,"\n".join(lines)); print("patched",p114)
print("RESYNC409 DONE")
