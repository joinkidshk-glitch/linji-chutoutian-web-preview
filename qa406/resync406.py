#!/usr/bin/env python3
"""v406 resync：釘行按內容重對（line_has(N, "text") → text 喺新 index.html 嘅行號）。
內容逐字核實：text 必須喺新檔出現；多處出現時用 difflib 映射揀最近舊行嗰處。"""
import difflib, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git","show","6ee775f:index.html"],cwd=ROOT,capture_output=True,text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT,"index.html"),encoding="utf-8").read().split("\n")
print("old lines", len(OLD)-1, "new lines", len(NEW)-1)
sm = difflib.SequenceMatcher(a=OLD,b=NEW,autojunk=False)
mp={}
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=="equal":
        for k in range(i2-i1): mp[i1+k]=j1+k
def new_line(old1, text):
    hits=[i+1 for i,l in enumerate(NEW) if text in l]
    if not hits: return None
    if len(hits)==1: return hits[0]
    mapped = mp.get(old1-1)
    if mapped is not None:
        return min(hits, key=lambda h: abs(h-(mapped+1)))
    return min(hits, key=lambda h: abs(h-old1))
files = sys.argv[1:]
for path in files:
    src = open(os.path.join(ROOT,path),encoding="utf-8").read()
    out=[]; last=0; changed=0; missing=[]
    for m in re.finditer(r'line_has\((\d+),\s*"((?:[^"\\]|\\.)*)"\)', src):
        old1=int(m.group(1)); text=m.group(2)
        nl=new_line(old1,text)
        if nl is None: missing.append((old1,text[:40])); continue
        if nl!=old1:
            out.append(src[last:m.start()]); out.append(f'line_has({nl}, "{text}")'); last=m.end(); changed+=1
    if changed:
        out.append(src[last:]); src="".join(out)
        lines=src.split("\n"); lines.insert(0,"# v406 resync：釘行按內容重對（qa406/resync406.py），純漂移。")
        open(os.path.join(ROOT,path),"w",encoding="utf-8").write("\n".join(lines))
    print(path, "changed", changed, "missing", missing)
