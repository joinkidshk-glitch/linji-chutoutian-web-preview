#!/usr/bin/env python3
# qa211/resync211c.py — resync211b.py 中途喺 166 斷咗（轉義問題），補返 166／64_chibi／200。
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BS = chr(92)  # backslash，避免 JSON／Python 兩層轉義食咗

def repl(path, old, new, count=1):
    p = os.path.join(ROOT, path)
    s = open(p, encoding="utf-8").read()
    n = s.count(old)
    assert n == count, "%s: %r count %d != %d" % (path, old[:70], n, count)
    open(p, "w", encoding="utf-8").write(s.replace(old, new))
    print("OK %s" % path)

# ---- 166：glamHtml 加咗 inline aspect-ratio（v211 B1） ----
old166 = ("chk('B1 glamHtml 包 .awd63-glamour-panel', '<div class=" + BS + '"awd63-glamour' + BS + '"><div class=' + BS + '"awd63-glamour-panel' + BS + '">' + "' in play_fn)")
new166 = ("chk('B1 glamHtml 包 .awd63-glamour-panel', '<div class=" + BS + '"awd63-glamour' + BS + '" style=' + BS + '"aspect-ratio:480/' + BS + "' + HS211 + " + BS + "'\"><div class=" + BS + '"awd63-glamour-panel' + BS + '">' + "' in play_fn) # v20a211 B1：glamour overlay 高跟 HS211")
repl("tests/test_awards166_static.py", old166, new166)

# ---- 64_chibi：FLOOR／dispH 高舞台縮放 ----
repl("tests/test_awards64_chibi_static.py",
     "chk('地板線 FLOOR=314（木地板 y274–372；v20a207 B2）', 'const FLOOR = 314' in play_fn)",
     "chk('地板線 FLOOR=314×HSC211（木地板 y274–372；v20a207 B2；v20a211 B1 高舞台 393）', 'const FLOOR = Math.round(314 * HSC211)' in play_fn)")
repl("tests/test_awards64_chibi_static.py",
     "chk('人物高度 136／玩家 140（v20a207 B2）', '? 140 : 136' in play_fn)",
     "chk('人物高度 136／玩家 140 ×HSC211（v20a207 B2；v20a211 B1 高舞台 170／175）', 'Math.round(140 * HSC211) : Math.round(136 * HSC211)' in play_fn)")

# ---- 200 logic：C2 gallery 席位去重係 v211 C3 刻意改動，唔係回歸 ----
repl("tests/test_awards200_logic.js",
     "ok('C2：gallery 請柬席位＋全 slate＋（觀禮）唔郁',\n  galInvite.indexOf('席位：旁聽席') >= 0 &&\n  galInvite.indexOf('今晚獎項：最佳男主角、最佳女主角、最佳男配角、最佳女配角（觀禮）') >= 0);",
     "ok('C2：gallery 請柬席位去重（v211 C3：刪「席位：旁聽席」，只留閘句「今晚席位：觀禮。」）＋全 slate＋（觀禮）唔郁',\n  galInvite.indexOf('席位：旁聽席') < 0 &&\n  galInvite.indexOf('今晚席位：觀禮。') >= 0 &&\n  galInvite.indexOf('今晚獎項：最佳男主角、最佳女主角、最佳男配角、最佳女配角（觀禮）') >= 0);")

print("ALL RESYNC C DONE")
