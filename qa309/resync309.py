# v20a309 resync：index.html 淨 +33 行（Q22 彭 n17 冷版場面：pang_n17_cold ＋29 @舊 L38159 前／
# buildScript 分流 ＋4 @舊 L40117 前；總行數 47242→47275；其後釘行按段 ＋29（38159–40116）／
# ＋33（≥40117），difflib 對位核實純漂移。
# 單次掃描 dict 查表（v160 教訓：唔逐對 re.sub；v162 教訓：重疊對要一次過換——
# 本檔用逐行全文做 key，唔會撞值）。
import difflib, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work309"
old = subprocess.check_output(["git", "show", "HEAD:index.html"], cwd=ROOT, text=True).splitlines()
new = open(ROOT + "/index.html", encoding="utf-8").read().splitlines()
assert len(old) == 47242, len(old)
assert len(new) == 47275, len(new)

sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for a0, b0, n in sm.get_matching_blocks():
    for k in range(n):
        mapping[a0 + k + 1] = b0 + k + 1  # 1-based

def check(old_n, exp_new_n, must_contain=None):
    got = mapping.get(old_n)
    assert got == exp_new_n, "difflib 映射 %d→%s（預期 %d）" % (old_n, got, exp_new_n)
    assert old[old_n - 1] == new[exp_new_n - 1], "內容唔同：舊 L%d %r vs 新 L%d %r" % (
        old_n, old[old_n - 1][:90], exp_new_n, new[exp_new_n - 1][:90])
    if must_contain:
        assert must_contain in new[exp_new_n - 1], "新 L%d 唔含 %r：%r" % (exp_new_n, must_contain, new[exp_new_n - 1][:90])
    print("OK 錨點 舊 L%d → 新 L%d：%s" % (old_n, exp_new_n, new[exp_new_n - 1].strip()[:80]))

# --- 逐字核實全部錨點（純漂移） ---
# 插入區邊界：pang_n17 收尾行之前唔郁、之後 ＋29；buildScript swap 之前 ＋29、之後 ＋33
check(38158, 38158, '},')
check(38159, 38188, 'pang_finale: {')
check(40116, 40145, 'let beatSeg100 = D.beats[beat.id];')
check(40117, 40150, 'beat.id==="gu_n10after"')
# 新插入行本身在位（唔經 mapping，用新行號直接驗）
assert 'pang_n17_cold' in new[38159 - 1], new[38159 - 1][:90]
assert 'v20a309 Q22' in new[40146 - 1] and 'pang_brushed_off' in new[40146 - 1], new[40146 - 1][:90]
assert 'beat.id==="pang_n17" && (S.flags||{}).pang_brushed_off' in new[40147 - 1], new[40147 - 1][:90]
print("OK 新插入行在位：pang_n17_cold L38159／dispatch 冷版分支 L40146–40149")
# rom176：4 釘（全部 ≥40117，＋33）
check(40683, 40716, 'v20a176 ROM176')
check(41033, 41066, 'function rom176ApplyGiftOverrides()')
check(42336, 42369, 'function addLocTalkGiftActs(add, L, npcId)')
check(42492, 42525, 'rom176TryIntercept(id)')
# travel114 DEF（＋33）；WRAPPER 29103 喺插入點之前，唔郁
check(42451, 42484, 'function openLoc(id, opts){')
check(29103, 29103, 'openLoc: function(id, opts){ openLoc(id, opts); }')
# travel114 COUNT（12 處：15363–28534 唔郁；45727–46114 ＋33）
for o, n in [(15363, 15363), (18672, 18672), (20882, 20882), (22085, 22085),
             (22525, 22525), (22528, 22528), (22559, 22559), (28534, 28534),
             (45727, 45760), (45935, 45968), (46093, 46126), (46114, 46147)]:
    check(o, n, 'openLoc(')
# travel114 FREE（40 處：6525–28375 唔郁；40481–46564 ＋33）
for o, n in [(6525, 6525), (6526, 6526), (8217, 8217), (14215, 14215),
             (14216, 14216), (14228, 14228), (14229, 14229), (14240, 14240),
             (14241, 14241), (14341, 14341), (24721, 24721), (26065, 26065),
             (26066, 26066), (26142, 26142), (28342, 28342), (28375, 28375),
             (40481, 40514), (40600, 40633), (40675, 40708), (40875, 40908),
             (40919, 40952), (40925, 40958), (40992, 41025), (40994, 41027),
             (40997, 41030), (41024, 41057), (42299, 42332), (42346, 42379),
             (42716, 42749), (42738, 42771), (42890, 42923), (42895, 42928),
             (43820, 43853), (45297, 45330), (45604, 45637), (45605, 45638),
             (45649, 45682), (45650, 45683), (45675, 45708), (46564, 46597)]:
    check(o, n, 'openLoc(')
print("OK 總行數 舊 47242 → 新 47275")

# --- 單次掃描 dict 查表改 5 檔（每條舊行出現且只出現一次） ---
HEADER = "# v20a309 resync：index.html 淨 +33 行（Q22：pang_n17_cold ＋29 @舊 L38159 前／dispatch 冷版分支 ＋4 @舊 L40117 前；總行數 47242→47275；其後釘行按段 ＋29／＋33，difflib 對位核實純漂移，見 qa309/resync309.py）。\n"

def resync(path, line_map, header=True):
    p = ROOT + "/" + path
    with open(p, encoding="utf-8") as f:
        lines = f.read().splitlines(keepends=True)
    body = [ln.rstrip("\n") for ln in lines]
    for old_ln in line_map:
        assert body.count(old_ln) == 1, "%s：舊行出現 %d 次（預期 1）：%r" % (path, body.count(old_ln), old_ln[:100])
    out = []
    for ln in lines:
        stripped = ln.rstrip("\n")
        out.append((line_map[stripped] + "\n") if stripped in line_map else ln)
    if header:
        out.insert(0, HEADER)
    with open(p, "w", encoding="utf-8") as f:
        f.writelines(out)
    print("已寫 %s（%d 行換咗）" % (path, len(line_map)))

# gift185：總行數鏈尾 ＋v309 +33（47242→47275）
lines = open(ROOT + "/tests/test_gift185_static.py", encoding="utf-8").read().splitlines()
tot_old = next(ln for ln in lines if ln.startswith("ok('總行數 47242"))
tot_new = tot_old.replace("總行數 47242（", "總行數 47275（", 1).replace(
    "＋v308 +3）', html.count('\\n') == 47242", "＋v308 +3＋v309 +33）', html.count('\\n') == 47275", 1)
assert tot_old != tot_new
resync("tests/test_gift185_static.py", {tot_old: tot_new})

# tang171／tang173：總行數鏈尾 ＋v309 +33、DEF 行 42451→42484、guard 行同步 ＋33
for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    lines = open(ROOT + "/" + fname, encoding="utf-8").read().splitlines()
    tot_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：總行數 47242"))
    def_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：openLoc DEF 行 42451"))
    guard_old = next(ln for ln in lines if "len(lines) >= 42457 and 'function openLoc(id, opts){' in lines[42450]" in ln)
    tot_new = tot_old.replace("總行數 47242（", "總行數 47275（", 1).replace(
        "＋v308 +3）', src.count('\\n') == 47242", "＋v308 +3＋v309 +33）', src.count('\\n') == 47275", 1)
    def_new = def_old.replace("openLoc DEF 行 42451（", "openLoc DEF 行 42484（", 1).replace(
        "＋v308 +3，travel114 釘行", "＋v308 +3＋v309 +33，travel114 釘行", 1)
    guard_new = guard_old.replace("len(lines) >= 42457", "len(lines) >= 42490", 1).replace("lines[42450]", "lines[42483]", 1)
    assert all(x != y for x, y in ((tot_old, tot_new), (def_old, def_new), (guard_old, guard_new)))
    resync(fname, {tot_old: tot_new, def_old: def_new, guard_old: guard_new})

# rom176：4 釘 ＋33（ok() 名入面嘅 L 號係歷史標籤，唔郁）
resync("tests/test_rom176_static.py", {
    "ok('釘：ROM176 block 起點 L55647', line(40683).startswith('/* ===== v20a176 ROM176'))":
    "ok('釘：ROM176 block 起點 L55647', line(40716).startswith('/* ===== v20a176 ROM176'))",
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41033).startswith('function rom176ApplyGiftOverrides()'))":
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41066).startswith('function rom176ApplyGiftOverrides()'))",
    "ok('釘：addLocTalkGiftActs L57154', line(42336).startswith('function addLocTalkGiftActs(add, L, npcId)'))":
    "ok('釘：addLocTalkGiftActs L57154', line(42369).startswith('function addLocTalkGiftActs(add, L, npcId)'))",
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42492))":
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42525))",
})

# travel114：DEF／COUNT／FREE——逐行全文做 key（重疊對一次過換，唔會撞值）
t114 = {}
t114["DEF_LINE = 42451      # function openLoc(id, opts){"] = "DEF_LINE = 42484      # function openLoc(id, opts){"
count_map = {45727: 45760, 45935: 45968, 46093: 46126, 46114: 46147}
free_map = {40481: 40514, 40600: 40633, 40675: 40708, 40875: 40908,
            40919: 40952, 40925: 40958, 40992: 41025, 40994: 41027,
            40997: 41030, 41024: 41057, 42299: 42332, 42346: 42379,
            42716: 42749, 42738: 42771, 42890: 42923, 42895: 42928,
            43820: 43853, 45297: 45330, 45604: 45637, 45605: 45638,
            45649: 45682, 45650: 45683, 45675: 45708, 46564: 46597}
t114_lines = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read().splitlines()
for old_n, new_n in list(count_map.items()) + list(free_map.items()):
    old_ln = next(ln for ln in t114_lines if ln.strip().startswith(str(old_n) + ","))
    assert mapping[old_n] == new_n, "映射唔啱：%d→%s（預期 %d）" % (old_n, mapping.get(old_n), new_n)
    t114[old_ln] = old_ln.replace(str(old_n) + ",", str(new_n) + ",", 1)
assert len(t114) == 1 + len(count_map) + len(free_map)
resync("tests/test_travel114_static.py", t114)
print("resync309 完成")
