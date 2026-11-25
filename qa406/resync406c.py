#!/usr/bin/env python3
"""v406 resync C：travel114 FREE/COUNT/DEF/WRAPPER 集合行號 difflib 映射（單次掃描 dict，內容逐行核實）。"""
import difflib, os, re, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git","show","6ee775f:index.html"],cwd=ROOT,capture_output=True,text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT,"index.html"),encoding="utf-8").read().split("\n")
sm = difflib.SequenceMatcher(a=OLD,b=NEW,autojunk=False)
mp={}
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=="equal":
        for k in range(i2-i1): mp[i1+k]=j1+k
path="tests/test_travel114_static.py"
src=open(os.path.join(ROOT,path),encoding="utf-8").read()
# find set blocks
def map_set(m):
    body=m.group(2)
    def sub(mm):
        n=int(mm.group(0))
        j=mp.get(n-1)
        assert j is not None, f"line {n} not in equal blocks"
        assert OLD[n-1]==NEW[j], f"line {n} content changed"
        return str(j+1)
    newbody=re.sub(r"\b\d{4,5}\b", sub, body)
    return m.group(1)+newbody+m.group(3)
src2=re.sub(r"((?:FREE_LINES|COUNT_LINES|DEF_LINES|WRAPPER_LINES)\s*=\s*\{)(.*?)(\})", map_set, src, flags=re.S)
assert src2!=src
lines=src2.split("\n"); lines.insert(0,"# v406 resync：FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；見 qa406/resync406c.py。")
open(os.path.join(ROOT,path),"w",encoding="utf-8").write("\n".join(lines))
print("ok")
