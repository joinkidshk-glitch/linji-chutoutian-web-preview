#!/usr/bin/env python3
"""v406 resync B：lines()[N]（0-based）／line(N)（1-based）釘行按內容重對。"""
import difflib, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git","show","6ee775f:index.html"],cwd=ROOT,capture_output=True,text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT,"index.html"),encoding="utf-8").read().split("\n")
sm = difflib.SequenceMatcher(a=OLD,b=NEW,autojunk=False)
mp={}
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=="equal":
        for k in range(i2-i1): mp[i1+k]=j1+k
def find0(old0, text):
    hits=[i for i,l in enumerate(NEW) if text in l]
    if not hits: return None
    if len(hits)==1: return hits[0]
    mapped=mp.get(old0)
    return min(hits, key=lambda h: abs(h-(mapped if mapped is not None else old0)))
for path in sys.argv[1:]:
    src=open(os.path.join(ROOT,path),encoding="utf-8").read()
    changed=0; missing=[]
    # lines()[N] ... startswith('text') / "text"
    def sub_lines(m):
        global changed
        n=int(m.group(1)); text=m.group(2)
        nl=find0(n,text)
        if nl is None: missing.append((n,text[:40])); return m.group(0)
        if nl!=n: changed+=1; return m.group(0).replace(f"lines()[{n}]", f"lines()[{nl}]",1)
        return m.group(0)
    src=re.sub(r"lines\(\)\[(\d+)\][^\n]*?startswith\(['\"]([^'\"]+)['\"]", sub_lines, src)
    # line(N).startswith("text") 1-based
    def sub_line(m):
        global changed
        n=int(m.group(1)); text=m.group(2)
        nl=find0(n-1,text)
        if nl is None: missing.append((n,text[:40])); return m.group(0)
        if nl+1!=n: changed+=1; return m.group(0).replace(f"line({n})", f"line({nl+1})",1)
        return m.group(0)
    src=re.sub(r"line\((\d+)\)\.startswith\(['\"]([^'\"]+)['\"]", sub_line, src)
    if changed:
        lines=src.split("\n"); lines.insert(0,"# v406 resync：釘行按內容重對（qa406/resync406b.py），純漂移。")
        open(os.path.join(ROOT,path),"w",encoding="utf-8").write("\n".join(lines))
    print(path,"changed",changed,"missing",missing)
