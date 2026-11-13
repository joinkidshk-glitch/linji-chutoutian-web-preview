#!/usr/bin/env python3
"""v20a152 travel114 resync：v152 刪鄧麗萍感情線令 index.html 行號漂移，核實 openLoc( 呼叫點係純漂移再出新行號。
用法：python3 qa152/resync_travel114_152.py
舊版 = pristine e08a070（~/workspace/pristine152-tmp/index.html），新版 = 工作副本 index.html。
方法：抽兩版全部含 openLoc( 嘅行，逐行內容對位（difflib）；錨點（COUNT／FREE／DEF／WRAPPER）
按內容＋次序映射去新行號。"""
import difflib, sys

OLD = "/home/hatch/workspace/pristine152-tmp/index.html"
NEW = "/home/hatch/workspace/linji-work152/index.html"

COUNT_OLD = [32132, 35613, 37740, 38734, 39168, 39171, 39202, 43748, 57592, 57759, 57902, 57923, 58373]
FREE_OLD = [24772, 28267, 30853, 30854, 30866, 30867, 30878, 30879, 30982, 40707, 43405, 43428,
            52437, 52556, 53449, 53831, 53853, 53988, 55625, 57036, 57369, 57487, 57488, 57523,
            57524, 57543, 57558]
DEF_OLD = 53562
WRAPPER_OLD = 44171

def load(p):
    return open(p, encoding="utf-8").read().split("\n")

old, new = load(OLD), load(NEW)
old_calls = [(i + 1, l) for i, l in enumerate(old) if "openLoc(" in l]
new_calls = [(i + 1, l) for i, l in enumerate(new) if "openLoc(" in l]
print(f"old calls: {len(old_calls)}, new calls: {len(new_calls)}")
old_texts = [l for _, l in old_calls]
new_texts = [l for _, l in new_calls]
sm = difflib.SequenceMatcher(a=old_texts, b=new_texts, autojunk=False)
ops = sm.get_opcodes()
print("opcodes:", [(t, a1, a2, b1, b2) for t, a1, a2, b1, b2 in ops if t != "equal"])
# 映射：equal 段逐行對位
mapping = {}
for tag, a1, a2, b1, b2 in ops:
    if tag == "equal":
        for k in range(a2 - a1):
            mapping[old_calls[a1 + k][0]] = new_calls[b1 + k][0]
missing = [n for n in COUNT_OLD + FREE_OLD + [DEF_OLD, WRAPPER_OLD] if n not in mapping]
print("unmapped anchors:", missing)
# 印出 delete/insert 段內容（應該只係註解／非 openLoc 行，唔係呼叫點本身）
for tag, a1, a2, b1, b2 in ops:
    if tag != "equal":
        print(f"-- {tag} old[{a1}:{a2}] new[{b1}:{b2}]")
        for ln, l in old_calls[a1:a2]:
            print(f"   OLD {ln}: {l.strip()[:100]}")
        for ln, l in new_calls[b1:b2]:
            print(f"   NEW {ln}: {l.strip()[:100]}")
print("COUNT new:", sorted(mapping[n] for n in COUNT_OLD))
print("FREE new:", sorted(mapping[n] for n in FREE_OLD))
print("DEF new:", mapping.get(DEF_OLD), "WRAPPER new:", mapping.get(WRAPPER_OLD))
# 驗證：新版 DEF／WRAPPER 行內容
print("DEF line now:", new[mapping[DEF_OLD] - 1].strip()[:80] if DEF_OLD in mapping else "?")
print("WRAPPER line now:", new[mapping[WRAPPER_OLD] - 1].strip()[:80] if WRAPPER_OLD in mapping else "?")
sys.exit(0 if not missing and all(t == "equal" for t, *_ in ops) else 1)
