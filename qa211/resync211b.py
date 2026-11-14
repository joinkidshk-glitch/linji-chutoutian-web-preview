#!/usr/bin/env python3
# qa211/resync211b.py — v20a211 第二輪 resync：全套 A/B 跑出 9 項新增 FAIL，
# 全部係我 +42 行引起嘅機械漂移（行數釘／幾何字面）＋v200 C2 同 C3 刻意行為改動。
# 做法：difflib 對位 pristine（worktree linji-pristine211，b7ddb37）vs 工作版，
# 每個釘行內容逐字核實純漂移，先至重寫行號／字面。
import difflib, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = open(os.path.expanduser("~/workspace/linji-pristine211/index.html"), encoding="utf-8").read().split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
print("old lines %d new lines %d delta %+d" % (len(OLD), len(NEW), len(NEW) - len(OLD)))

sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k  # 1-based
    else:
        print("opcode %s old %d-%d new %d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))

def map_line(old_ln):
    assert old_ln in mapping, "anchor %d not in equal block" % old_ln
    nl = mapping[old_ln]
    assert OLD[old_ln - 1] == NEW[nl - 1], "anchor %d content differs:\nOLD %r\nNEW %r" % (old_ln, OLD[old_ln - 1], NEW[nl - 1])
    return nl

anchors = {
    # travel114
    "travel114_COUNT": [32313, 35813, 37964, 39134, 39566, 39569, 39600, 44611, 60044, 60222, 60368, 60389],
    "travel114_FREE": [24765, 30980, 30981, 30993, 30994, 31005, 31006, 31109, 41554, 44268, 44291, 54216, 54335, 54385, 54608, 54647, 54653, 54720, 54722, 54725, 54752, 55863, 56237, 56259, 56410, 58047, 59812, 59930, 59931, 59966, 59967, 59992, 60839],
    "travel114_DEF": [55963],
    "travel114_WRAPPER": [45180],
    # rom176
    "rom176": [54393, 54761, 55900, 55994],
    # tang171/173 DEF
    "tang_DEF": [55963],
}
mapped = {}
for group, lns in anchors.items():
    for ln in lns:
        mapped[(group, ln)] = map_line(ln)
        print("%s %d -> %d" % (group, ln, mapped[(group, ln)]))

def repl(path, old, new, count=1):
    p = os.path.join(ROOT, path)
    s = open(p, encoding="utf-8").read()
    n = s.count(old)
    assert n == count, "%s: %r count %d != %d" % (path, old[:70], n, count)
    open(p, "w", encoding="utf-8").write(s.replace(old, new))
    print("OK %s: %r -> %r" % (path, old[:60], new[:60]))

# ---- travel114：行號按映射重寫（只改 set 內行首數字＋DEF/WRAPPER 行） ----
t114 = os.path.join(ROOT, "tests/test_travel114_static.py")
t = open(t114, encoding="utf-8").read().split("\n")
# COUNT_LINES block：由 "COUNT_LINES = {" 到下一個 "}"
def resync_set(lines, start_pat, group):
    i = next(k for k, l in enumerate(lines) if l.startswith(start_pat))
    j = next(k for k in range(i, len(lines)) if lines[k].strip() == "}")
    for k in range(i + 1, j):
        m = re.match(r"^(\s*)(\d+)(,.*)$", lines[k])
        if not m:
            continue
        old = int(m.group(2))
        new = mapped[(group, old)]
        lines[k] = "%s%d%s" % (m.group(1), new, m.group(3))
    return lines
t = resync_set(t, "COUNT_LINES = {", "travel114_COUNT")
t = resync_set(t, "FREE_LINES = {", "travel114_FREE")
for k, l in enumerate(t):
    if l.startswith("DEF_LINE = "):
        t[k] = re.sub(r"DEF_LINE = \d+", "DEF_LINE = %d" % mapped[("travel114_DEF", 55963)], l)
    if l.startswith("WRAPPER_LINE = "):
        t[k] = re.sub(r"WRAPPER_LINE = \d+", "WRAPPER_LINE = %d" % mapped[("travel114_WRAPPER", 45180)], l)
t.insert(0, "# v20a211 resync：index.html 淨 +42 行（A1 hideToast211 ＋8／B1 HS211＋HSC211 ＋5／B2＋C1＋C3 註解／分流 ＋9／B7 spotlight 梯形 ＋20）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫，內容逐字核實純漂移（見 qa211/resync211b.py）。")
open(t114, "w", encoding="utf-8").write("\n".join(t))
print("OK travel114 resynced")

# ---- rom176：4 釘行 ----
for old, new in [(54393, mapped[("rom176", 54393)]), (54761, mapped[("rom176", 54761)]),
                 (55900, mapped[("rom176", 55900)]), (55994, mapped[("rom176", 55994)])]:
    repl("tests/test_rom176_static.py", "L%d" % old, "L%d" % new)
    repl("tests/test_rom176_static.py", "line(%d)" % old, "line(%d)" % new)
repl("tests/test_rom176_static.py",
     "# v20a176",
     "# v20a211 resync：index.html 淨 +42 行，4 釘行按 difflib 映射重寫（純漂移，見 qa211/resync211b.py）。\n# v20a176", 1)

# ---- tang171 / tang173 / gift185：總行數＋DEF 行 ----
new_total = len(NEW) - 1  # count('\n')
new_def = mapped[("tang_DEF", 55963)]
for f in ["tests/test_tang171_static.py", "tests/test_tang173_static.py"]:
    repl(f, "總行數 61491（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34）",
         "總行數 %d（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v211 +42）" % new_total)
    repl(f, "src.count('\\n') == 61491", "src.count('\\n') == %d" % new_total)
    repl(f, "openLoc DEF 行 55963（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34，travel114 釘行）",
         "openLoc DEF 行 %d（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v211 +42，travel114 釘行）" % new_def)
    repl(f, "len(lines) >= 55963 and 'function openLoc(id, opts){' in lines[55962]",
         "len(lines) >= %d and 'function openLoc(id, opts){' in lines[%d]" % (new_def, new_def - 1))
repl("tests/test_gift185_static.py",
     "總行數 61491（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34）",
     "總行數 %d（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v211 +42）" % new_total)
repl("tests/test_gift185_static.py", "html.count('\\n') == 61491", "html.count('\\n') == %d" % new_total)

# ---- 160_m4：glyph −129 → 高舞台縮放 ----
repl("tests/test_awards160_m4_static.py",
     "'drawTrophyGlyph(targetX, FLOOR - 129)' in play_fn) # v20a187 C6 resync：舊 −112；v20a207 B2：−110→−129",
     "'drawTrophyGlyph(targetX, FLOOR - Math.round(129 * HSC211))' in play_fn) # v20a187 C6 resync：舊 −112；v20a207 B2：−110→−129；v20a211 B1：高舞台 ×HSC211（短 129／高 161）")

# ---- 166：glamHtml 加咗 inline aspect-ratio（v211 B1） ----
repl("tests/test_awards166_static.py",
     "chk('B1 glamHtml 包 .awd63-glamour-panel', '<div class=\\\"awd63-glamour\\\"><div class=\\\"awd63-glamour-panel\\\">' in play_fn)",
     "chk('B1 glamHtml 包 .awd63-glamour-panel', '<div class=\\\"awd63-glamour\\\" style=\\\"aspect-ratio:480/\\' + HS211 + \\'\"><div class=\\\"awd63-glamour-panel\\\">' in play_fn) # v20a211 B1：glamour overlay 高跟 HS211")

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

print("ALL RESYNC DONE")
