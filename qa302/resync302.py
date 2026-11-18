# v20a302 resync：index.html 淨 +19 行（Q15 鍾楚凝告別報紙花邊：buildNewspaperEdition 注入 ＋14 @舊 L34343 後／
# commitMorningPaper 記已出旗 ＋5 @舊 L34621 後；總行數 47137→47156；其後釘行按段 ＋14（34344–34621）／＋19（≥34622）；內容逐字核實純漂移。
# 單次掃描 dict 查表（v160 教訓：唔逐對 re.sub；v162 教訓：重疊對要一次過換）。
import difflib, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work302"
old = subprocess.check_output(["git", "show", "HEAD:index.html"], cwd=ROOT, text=True).splitlines()
new = open(ROOT + "/index.html", encoding="utf-8").read().splitlines()
assert len(old) == 47137, len(old)
assert len(new) == 47156, len(new)

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
# 插入區邊界：第一 hunk 之前唔郁、之後 ＋14；第二 hunk 之後 ＋19
check(34341, 34341, "shorts.push(side2)")
check(34343, 34357, "const fameDelta")
check(34620, 34634, "enc79PaperWhisper(sh.sideId)")
check(34621, 34640, "S.pendingMorningPaper = null")
# rom176：4 釘（全部 ≥34622，＋19）
check(40581, 40600, "v20a176 ROM176")
check(40931, 40950, "function rom176ApplyGiftOverrides")
check(42231, 42250, "function addLocTalkGiftActs")
check(42387, 42406, "rom176TryIntercept(id)")
# travel114：DEF／WRAPPER（DEF ＋19；WRAPPER 喺插入點之前，唔郁）
check(42346, 42365, "function openLoc(id, opts){")
check(29103, 29103, "openLoc: function(id, opts){ openLoc(id, opts); }")
# travel114 COUNT（12 處：15363–28534 唔郁；45622–46009 ＋19）
for o, n in [(15363, 15363), (18672, 18672), (20882, 20882), (22085, 22085),
             (22525, 22525), (22528, 22528), (22559, 22559), (28534, 28534),
             (45622, 45641), (45830, 45849), (45988, 46007), (46009, 46028)]:
    check(o, n, "openLoc(")
# travel114 FREE（40 處：6525–28375 唔郁；40379–46459 ＋19）
for o, n in [(6525, 6525), (6526, 6526), (8217, 8217), (14215, 14215),
             (14216, 14216), (14228, 14228), (14229, 14229), (14240, 14240),
             (14241, 14241), (14341, 14341), (24721, 24721), (26065, 26065),
             (26066, 26066), (26142, 26142), (28342, 28342), (28375, 28375),
             (40379, 40398), (40498, 40517), (40573, 40592), (40773, 40792),
             (40817, 40836), (40823, 40842), (40890, 40909), (40892, 40911),
             (40895, 40914), (40922, 40941), (42194, 42213), (42241, 42260),
             (42611, 42630), (42633, 42652), (42785, 42804), (42790, 42809),
             (43715, 43734), (45192, 45211), (45499, 45518), (45500, 45519),
             (45544, 45563), (45545, 45564), (45570, 45589), (46459, 46478)]:
    check(o, n, "openLoc(")
print("OK 總行數 舊 47137 → 新 47156")

# --- 單次掃描 dict 查表改 5 檔（每條舊行出現且只出現一次） ---
HEADER = "# v20a302 resync：index.html 淨 +19 行（Q15：buildNewspaperEdition 告別花邊注入 ＋14 @舊 L34343 後／commitMorningPaper 記已出旗 ＋5 @舊 L34621 後；總行數 47137→47156；其後釘行按段 ＋14／＋19，difflib 對位核實純漂移，見 qa302/resync302.py）。\n"

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

# gift185：總行數鏈尾 ＋v302 +19（47137→47156）
lines = open(ROOT + "/tests/test_gift185_static.py", encoding="utf-8").read().splitlines()
tot_old = next(ln for ln in lines if ln.startswith("ok('總行數 47137"))
tot_new = tot_old.replace("總行數 47137（", "總行數 47156（", 1).replace(
    "＋v300 +44）', html.count('\\n') == 47137", "＋v300 +44＋v302 +19）', html.count('\\n') == 47156", 1)
assert tot_old != tot_new
resync("tests/test_gift185_static.py", {tot_old: tot_new})

# tang171／tang173：總行數鏈尾 ＋v302 +19、DEF 行 42346→42365、guard 行同步 ＋19
for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    lines = open(ROOT + "/" + fname, encoding="utf-8").read().splitlines()
    tot_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：總行數 47137"))
    def_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：openLoc DEF 行 42346"))
    guard_old = next(ln for ln in lines if "len(lines) >= 42352 and 'function openLoc(id, opts){' in lines[42345]" in ln)
    tot_new = tot_old.replace("總行數 47137（", "總行數 47156（", 1).replace(
        "＋v300 +44）', src.count('\\n') == 47137", "＋v300 +44＋v302 +19）', src.count('\\n') == 47156", 1)
    def_new = def_old.replace("openLoc DEF 行 42346（", "openLoc DEF 行 42365（", 1).replace(
        "＋v300 +7，travel114 釘行", "＋v300 +7＋v302 +19，travel114 釘行", 1)
    guard_new = guard_old.replace("len(lines) >= 42352", "len(lines) >= 42371", 1).replace("lines[42345]", "lines[42364]", 1)
    assert all(x != y for x, y in ((tot_old, tot_new), (def_old, def_new), (guard_old, guard_new)))
    resync(fname, {tot_old: tot_new, def_old: def_new, guard_old: guard_new})

# rom176：4 釘 ＋19（ok() 名入面嘅 L 號係歷史標籤，唔郁）
resync("tests/test_rom176_static.py", {
    "ok('釘：ROM176 block 起點 L55647', line(40581).startswith('/* ===== v20a176 ROM176'))":
    "ok('釘：ROM176 block 起點 L55647', line(40600).startswith('/* ===== v20a176 ROM176'))",
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(40931).startswith('function rom176ApplyGiftOverrides()'))":
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(40950).startswith('function rom176ApplyGiftOverrides()'))",
    "ok('釘：addLocTalkGiftActs L57154', line(42231).startswith('function addLocTalkGiftActs(add, L, npcId)'))":
    "ok('釘：addLocTalkGiftActs L57154', line(42250).startswith('function addLocTalkGiftActs(add, L, npcId)'))",
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42387))":
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42406))",
})

# travel114：DEF／COUNT／FREE——逐行全文做 key（重疊對一次過換，唔會撞值）
t114 = {}
t114["DEF_LINE = 42346      # function openLoc(id, opts){"] = "DEF_LINE = 42365      # function openLoc(id, opts){"
count_map = {45622: 45641, 45830: 45849, 45988: 46007, 46009: 46028}
free_map = {40379: 40398, 40498: 40517, 40573: 40592, 40773: 40792,
            40817: 40836, 40823: 40842, 40890: 40909, 40892: 40911,
            40895: 40914, 40922: 40941, 42194: 42213, 42241: 42260,
            42611: 42630, 42633: 42652, 42785: 42804, 42790: 42809,
            43715: 43734, 45192: 45211, 45499: 45518, 45500: 45519,
            45544: 45563, 45545: 45564, 45570: 45589, 46459: 46478}
for ln in open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read().splitlines():
    s = ln.strip()
    if s and (s.rstrip(",").split(",")[0].strip().isdigit()):
        num = int(s.split(",")[0].strip())
        if num in count_map or num in free_map:
            new_num = count_map.get(num, free_map.get(num))
            # 只換行首數字，保留註解
            t114[ln] = ln.replace(str(num), str(new_num), 1)
assert len(t114) == 1 + len(count_map) + len(free_map), len(t114)
resync("tests/test_travel114_static.py", t114)

print("resync302 完成：5 檔已改，全部錨點 difflib 核實純漂移。")
