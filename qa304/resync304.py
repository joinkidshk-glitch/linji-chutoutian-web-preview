# v20a304 resync：index.html 淨 +38 行（Q17 駱／魏／齊冷版 heart 交心：
# ngai heartCold ＋11 @舊 L36673 後／lok heartCold ＋11 @舊 L37305 後／
# chai heartCold ＋11 @舊 L37648 後／dispatch 冷版分支 ＋5 @舊 L40140 前；
# 總行數 47156→47194；其後釘行按段 ＋11（36673–37304）／＋22（37305–37647）／
# ＋33（37648–40139）／＋38（≥40140），difflib 對位核實純漂移。
# 單次掃描 dict 查表（v160 教訓：唔逐對 re.sub；v162 教訓：重疊對要一次過換——
# 本檔用逐行全文做 key，唔會撞值）。
import difflib, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work304"
old = subprocess.check_output(["git", "show", "HEAD:index.html"], cwd=ROOT, text=True).splitlines()
new = open(ROOT + "/index.html", encoding="utf-8").read().splitlines()
assert len(old) == 47156, len(old)
assert len(new) == 47194, len(new)

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
# 插入區邊界：魏 heartCold 之前唔郁、之後 ＋11；駱 ＋22；齊 ＋33；dispatch ＋38
check(36669, 36669, 'ngai_heart_shy')
check(36673, 36684, 'pool: {')
check(37301, 37312, 'lok_praised_song')
check(37305, 37327, 'pool: {')
check(37644, 37666, 'chai_comfort')
check(37648, 37681, 'pool: {')
check(40139, 40172, 'pushSeg(beatSeg100')
# 舊 L40140（暖版 heart 閘行）本身改咗行尾註解（v20a278「冷版由 patron 冷版承接」→ v20a304「冷版 heart 見上」），
# difflib 視為 replace 而非 equal，故唔經 mapping，改為逐字核實閘條件相同＋新行號在位
assert old[40140 - 1].startswith('  } else if(tier>=3 && !st.heartDone && D.heart && !(starId==="chung_choning"'), old[40140 - 1][:90]
assert new[40178 - 1].startswith('  } else if(tier>=3 && !st.heartDone && D.heart && !(starId==="chung_choning"'), new[40178 - 1][:90]
assert old[40140 - 1].split('){')[0] == new[40178 - 1].split('){')[0], "暖版 heart 閘條件唔同"
assert 'v20a304' in new[40178 - 1] and '冷版 heart 見上' in new[40178 - 1]
print("OK 錨點 舊 L40140 → 新 L40178（暖版 heart 閘逐字相同，只改行尾註解）：%s" % new[40178 - 1].strip()[:80])
# 新插入行本身在位（唔經 mapping，用新行號直接驗）
assert '魏冷版交心' in new[36673 - 1], new[36673 - 1][:90]
assert '駱冷版交心' in new[37316 - 1], new[37316 - 1][:90]
assert '齊冷版交心' in new[37670 - 1], new[37670 - 1][:90]
assert 'D.heartCold && ((starId==="lok_gasing"' in new[40173 - 1], new[40173 - 1][:90]
assert 'heartCold:"+starId' in new[40177 - 1], new[40177 - 1][:90]
print("OK 新插入行在位：魏 heartCold L36673／駱 L37316／齊 L37670／dispatch 冷版分支 L40173–40177")
# rom176：4 釘（全部 ≥40140，＋38）
check(40600, 40638, 'v20a176 ROM176')
check(40950, 40988, 'function rom176ApplyGiftOverrides')
check(42250, 42288, 'function addLocTalkGiftActs')
check(42406, 42444, 'rom176TryIntercept(id)')
# travel114：DEF ＋38；WRAPPER 喺插入點之前，唔郁
check(42365, 42403, 'function openLoc(id, opts){')
check(29103, 29103, 'openLoc: function(id, opts){ openLoc(id, opts); }')
# travel114 COUNT（12 處：15363–28534 唔郁；45641–46028 ＋38）
for o, n in [(15363, 15363), (18672, 18672), (20882, 20882), (22085, 22085),
             (22525, 22525), (22528, 22528), (22559, 22559), (28534, 28534),
             (45641, 45679), (45849, 45887), (46007, 46045), (46028, 46066)]:
    check(o, n, 'openLoc(')
# travel114 FREE（40 處：6525–28375 唔郁；40398–46478 ＋38）
for o, n in [(6525, 6525), (6526, 6526), (8217, 8217), (14215, 14215),
             (14216, 14216), (14228, 14228), (14229, 14229), (14240, 14240),
             (14241, 14241), (14341, 14341), (24721, 24721), (26065, 26065),
             (26066, 26066), (26142, 26142), (28342, 28342), (28375, 28375),
             (40398, 40436), (40517, 40555), (40592, 40630), (40792, 40830),
             (40836, 40874), (40842, 40880), (40909, 40947), (40911, 40949),
             (40914, 40952), (40941, 40979), (42213, 42251), (42260, 42298),
             (42630, 42668), (42652, 42690), (42804, 42842), (42809, 42847),
             (43734, 43772), (45211, 45249), (45518, 45556), (45519, 45557),
             (45563, 45601), (45564, 45602), (45589, 45627), (46478, 46516)]:
    check(o, n, 'openLoc(')
print("OK 總行數 舊 47156 → 新 47194")

# --- 單次掃描 dict 查表改 5 檔（每條舊行出現且只出現一次） ---
HEADER = "# v20a304 resync：index.html 淨 +38 行（Q17：ngai heartCold ＋11 @舊 L36673 後／lok heartCold ＋11 @舊 L37305 後／chai heartCold ＋11 @舊 L37648 後／dispatch 冷版分支 ＋5 @舊 L40140 前；總行數 47156→47194；其後釘行按段 ＋11／＋22／＋33／＋38，difflib 對位核實純漂移，見 qa304/resync304.py）。\n"

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

# gift185：總行數鏈尾 ＋v304 +38（47156→47194）
lines = open(ROOT + "/tests/test_gift185_static.py", encoding="utf-8").read().splitlines()
tot_old = next(ln for ln in lines if ln.startswith("ok('總行數 47156"))
tot_new = tot_old.replace("總行數 47156（", "總行數 47194（", 1).replace(
    "＋v302 +19）', html.count('\\n') == 47156", "＋v302 +19＋v304 +38）', html.count('\\n') == 47194", 1)
assert tot_old != tot_new
resync("tests/test_gift185_static.py", {tot_old: tot_new})

# tang171／tang173：總行數鏈尾 ＋v304 +38、DEF 行 42365→42403、guard 行同步 ＋38
for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    lines = open(ROOT + "/" + fname, encoding="utf-8").read().splitlines()
    tot_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：總行數 47156"))
    def_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：openLoc DEF 行 42365"))
    guard_old = next(ln for ln in lines if "len(lines) >= 42371 and 'function openLoc(id, opts){' in lines[42364]" in ln)
    tot_new = tot_old.replace("總行數 47156（", "總行數 47194（", 1).replace(
        "＋v302 +19）', src.count('\\n') == 47156", "＋v302 +19＋v304 +38）', src.count('\\n') == 47194", 1)
    def_new = def_old.replace("openLoc DEF 行 42365（", "openLoc DEF 行 42403（", 1).replace(
        "＋v302 +19，travel114 釘行", "＋v302 +19＋v304 +38，travel114 釘行", 1)
    guard_new = guard_old.replace("len(lines) >= 42371", "len(lines) >= 42409", 1).replace("lines[42364]", "lines[42402]", 1)
    assert all(x != y for x, y in ((tot_old, tot_new), (def_old, def_new), (guard_old, guard_new)))
    resync(fname, {tot_old: tot_new, def_old: def_new, guard_old: guard_new})

# rom176：4 釘 ＋38（ok() 名入面嘅 L 號係歷史標籤，唔郁）
resync("tests/test_rom176_static.py", {
    "ok('釘：ROM176 block 起點 L55647', line(40600).startswith('/* ===== v20a176 ROM176'))":
    "ok('釘：ROM176 block 起點 L55647', line(40638).startswith('/* ===== v20a176 ROM176'))",
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(40950).startswith('function rom176ApplyGiftOverrides()'))":
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(40988).startswith('function rom176ApplyGiftOverrides()'))",
    "ok('釘：addLocTalkGiftActs L57154', line(42250).startswith('function addLocTalkGiftActs(add, L, npcId)'))":
    "ok('釘：addLocTalkGiftActs L57154', line(42288).startswith('function addLocTalkGiftActs(add, L, npcId)'))",
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42406))":
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42444))",
})

# travel114：DEF／COUNT／FREE——逐行全文做 key（重疊對一次過換，唔會撞值）
t114 = {}
t114["DEF_LINE = 42365      # function openLoc(id, opts){"] = "DEF_LINE = 42403      # function openLoc(id, opts){"
count_map = {45641: 45679, 45849: 45887, 46007: 46045, 46028: 46066}
free_map = {40398: 40436, 40517: 40555, 40592: 40630, 40792: 40830,
            40836: 40874, 40842: 40880, 40909: 40947, 40911: 40949,
            40914: 40952, 40941: 40979, 42213: 42251, 42260: 42298,
            42630: 42668, 42652: 42690, 42804: 42842, 42809: 42847,
            43734: 43772, 45211: 45249, 45518: 45556, 45519: 45557,
            45563: 45601, 45564: 45602, 45589: 45627, 46478: 46516}
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

print("resync304 完成：5 檔已改，全部錨點 difflib 核實純漂移。")
