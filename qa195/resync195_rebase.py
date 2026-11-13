# -*- coding: utf-8 -*-
"""v20a195 rebase resync：difflib 對位新 main (b104f85, v192 NOTES) → work index.html，
核實漂移純粹係 v195 插入（5 處），再映射 5 檔衝突測試嘅行號釘。
用法：python3 qa195/resync195_rebase.py
"""
import difflib, subprocess

def git_show(rev, path):
    return subprocess.check_output(["git", "show", "%s:%s" % (rev, path)],
                                   cwd="/home/hatch/workspace/linji-work195",
                                   text=True).split("\n")

old = git_show("b104f85", "index.html")
new = open("/home/hatch/workspace/linji-work195/index.html", encoding="utf-8").read().split("\n")
print("old lines:", len(old) - 1, "new lines:", len(new) - 1, "net:", (len(new) - 1) - (len(old) - 1))

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

# 釘：(檔名, b104f85 1-based 行號)；0-based 索引用 1-based 行號 -1 轉換嗰陣另外計。
PINS = {
    "gift185_total": [60522],
    "rom176": [31583, 53448, 53816, 54955, 55049],
    "tang171_173_total": [60522],
    "tang171_173_DEF_1based": [55018],
    "travel114_COUNT": [32184, 35680, 37807, 38888, 39322, 39325, 39356, 43911, 59078, 59256, 59399, 59420],
    "travel114_FREE": [24686, 28228, 30851, 30852, 30864, 30865, 30876, 30877, 30980, 40866, 43568, 43591,
                       53271, 53390, 53440, 53663, 53702, 53708, 53775, 53777, 53780, 53807, 54918, 55292,
                       55314, 55465, 57102, 58846, 58964, 58965, 59000, 59001, 59026, 59870],
    "travel114_DEF_1based": [55018],
    "travel114_WRAPPER_1based": [44434],
}
print("\npin mapping (b104f85 -> work, content must match verbatim):")
bad = 0
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
        print("  %s L%d -> L%d %s :: %s" % (group, ln, nl, "OK" if same else "CONTENT DIFF!",
              old[ln - 1].strip()[:90]))
print("\nBAD:", bad)
raise SystemExit(1 if bad else 0)
