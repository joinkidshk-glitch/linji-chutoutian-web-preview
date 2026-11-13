#!/usr/bin/env python3
"""v20a160 M6 resync test_travel114_static.py：M6 淨 ＋30 行（tuxRec 預載 ＋8／drawTuxedo＋drawFigure 分流 ＋10／
reveal won 燕尾服＋獎盃 glyph ＋5／glamour ＋1／常量 ＋7，減 4 行舊＝淨 ＋30；全部插入點喺 L46232–46501 之間）。
核實：difflib 對位只得插入段、44 個 openLoc( 呼叫點逐字一致、42 個釘行內容逐行相同，純漂移。
用法：python3 qa160-m6/resync_travel114.py"""
import difflib, sys

OLD = "/home/hatch/workspace/pristine160m6/index.html"  # e08a070
NEW = "/home/hatch/workspace/linji-work160-m6/index.html"
old = open(OLD, encoding="utf-8").read().splitlines()
new = open(NEW, encoding="utf-8").read().splitlines()
print("old lines %d new lines %d delta %+d" % (len(old), len(new), len(new) - len(old)))

sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
ops = [op for op in sm.get_opcodes() if op[0] != "equal"]
print("non-equal opcodes:", [(o[0], o[1], o[2], o[3], o[4]) for o in ops])
# M6 改動唔係純插入：dispH 行改寫（1→1）、reveal won 重組（2→7）、glamour 行改寫（1→2）——
# 三個 replace 段全部喺 M6 編輯區（舊行 46232–46509，awards62PlayCeremony 內），且無一段掂 openLoc( 行。
M6_LO, M6_HI = 46232, 46509
for tag, i1, i2, j1, j2 in ops:
    assert tag in ("insert", "replace"), "非插入／改寫！"
    if tag == "replace":
        assert M6_LO <= i1 + 1 and i2 <= M6_HI, "replace 段超出 M6 區！"
        assert not any("openLoc(" in l for l in old[i1:i2]), "replace 段掂到 openLoc(！"
    else:
        assert M6_LO <= i1 + 1 <= M6_HI, "insert 段超出 M6 區！"
print("opcodes OK：全部插入／改寫都喺 M6 區，無掂 openLoc( 行")

COUNT = [32132, 35613, 37740, 38734, 39168, 39171, 39202, 43748, 57592, 57759, 57902, 57923, 58373]
FREE = [24772, 28267, 30853, 30854, 30866, 30867, 30878, 30879, 30982, 40707, 43405, 43428,
        52437, 52556, 53449, 53831, 53853, 53988, 55625, 57036, 57369, 57487, 57488, 57523,
        57524, 57543, 57558]
pins = [("COUNT", n) for n in COUNT] + [("FREE", n) for n in FREE] + \
       [("DEF", 53562), ("WRAPPER", 44171)]
bad = []
for kind, n in pins:
    txt = old[n - 1]
    expect = n + 30 if n >= 46232 else n
    # 喺新檔搵返逐字相同嘅行；重複行（舊檔已有兩處相同）就揀最接近預期位置嗰個
    hits = [i + 1 for i, l in enumerate(new) if l == txt]
    if not hits:
        bad.append((kind, n, "hits=0"))
        continue
    new_n = min(hits, key=lambda h: abs(h - expect))
    status = "OK" if new_n == expect else "SHIFT!=expect"
    if new_n != expect:
        bad.append((kind, n, "new=%d expect=%d hits=%s" % (new_n, expect, hits)))
    print("%-7s old %d -> new %d (expect %d) %s :: %s" % (kind, n, new_n, expect, status, txt.strip()[:70]))

old_calls = sum(1 for l in old if "openLoc(" in l)
new_calls = sum(1 for l in new if "openLoc(" in l)
print("openLoc( 行數 old %d new %d" % (old_calls, new_calls))
assert old_calls == new_calls
print("BAD:", bad if bad else "none — 42 釘行全部純漂移 ＋30（≥46232）／不變（＜46232）")
sys.exit(1 if bad else 0)
