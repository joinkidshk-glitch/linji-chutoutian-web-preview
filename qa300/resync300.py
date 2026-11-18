# v20a300 resync：index.html 淨 +44 行（Q13 彭渠道台風減半：詳情頁鎖定分支 ＋7 @舊 L18723 後／
# v20a158 頭註解 ＋1 @舊 L45245 前後／pangHalvedStageReq158 等 3 helper＋favor158ChannelForGig 重寫 ＋36 淨 @舊 L45268 起；
# 總行數 47093→47137；其後釘行按段 ＋7（18724–45244）／＋44（≥45245）；內容逐字核實純漂移。
# 單次掃描 dict 查表（v160 教訓：唔逐對 re.sub；v162 教訓：45456→45500／45500→45544 重疊對要一次過換）。
import difflib, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work300"
old = subprocess.check_output(["git", "show", "HEAD:index.html"], cwd=ROOT, text=True).splitlines()
new = open(ROOT + "/index.html", encoding="utf-8").read().splitlines()
assert len(old) == 47093, len(old)
assert len(new) == 47137, len(new)

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
# rom159：4 釘（全部 18724–45244 段，＋7）
check(25459, 25466, "v20a159 ROM159 Phase 1")
check(26307, 26314, "COMMIT48_NODES.CMT_lan_commit")
check(26208, 26215, "function rom159SoMeetGate")
check(25487, 25494, "全佳 7 分")
# rom176：4 釘（＋7）
check(40574, 40581, "v20a176 ROM176")
check(40924, 40931, "function rom176ApplyGiftOverrides")
check(42224, 42231, "function addLocTalkGiftActs")
check(42380, 42387, "rom176TryIntercept(id)")
# travel114：DEF／WRAPPER（＋7）
check(42339, 42346, "function openLoc(id, opts){")
check(29096, 29103, "openLoc: function(id, opts){ openLoc(id, opts); }")
# travel114 COUNT（12 處：15363／18672 唔郁；20875–28527 ＋7；45578–45965 ＋44）
for o, n in [(20875, 20882), (22078, 22085), (22518, 22525), (22521, 22528),
             (22552, 22559), (28527, 28534), (45578, 45622), (45786, 45830),
             (45944, 45988), (45965, 46009)]:
    check(o, n, "openLoc(")
# travel114 FREE（40 處：6525–14341 唔郁；24714–45185 ＋7；45455–46415 ＋44）
for o, n in [(24714, 24721), (26058, 26065), (26059, 26066), (26135, 26142),
             (28335, 28342), (28368, 28375), (40372, 40379), (40491, 40498),
             (40566, 40573), (40766, 40773), (40810, 40817), (40816, 40823),
             (40883, 40890), (40885, 40892), (40888, 40895), (40915, 40922),
             (42187, 42194), (42234, 42241), (42604, 42611), (42626, 42633),
             (42778, 42785), (42783, 42790), (43708, 43715), (45185, 45192),
             (45455, 45499), (45456, 45500), (45500, 45544), (45501, 45545),
             (45526, 45570), (46415, 46459)]:
    check(o, n, "openLoc(")
# 總行數鏈（count('\n') 47093→47137）
print("OK 總行數 舊 47093 → 新 47137")

# --- 單次掃描 dict 查表改 6 檔（每條舊行出現且只出現一次） ---
HEADER = "# v20a300 resync：index.html 淨 +44 行（Q13：詳情頁 ＋7 @舊 L18723 後／158 頭註解 ＋1／helper＋重寫 ＋36 淨；總行數 47093→47137；其後釘行按段 ＋7／＋44，difflib 對位核實純漂移，見 qa300/resync300.py）。\n"

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

# gift185：總行數鏈尾 ＋v300 +44（47093→47137）
gift_total_old = None
for ln in open(ROOT + "/tests/test_gift185_static.py", encoding="utf-8"):
    if ln.startswith("ok('總行數 47093"):
        gift_total_old = ln.rstrip("\n")
assert gift_total_old
gift_total_new = gift_total_old.replace("總行數 47093（", "總行數 47137（", 1).replace(
    "＋v299 +280）', html.count('\\n') == 47093", "＋v299 +280＋v300 +44）', html.count('\\n') == 47137", 1)
assert gift_total_new != gift_total_old and "v300 +44" in gift_total_new and "47137" in gift_total_new
resync("tests/test_gift185_static.py", {gift_total_old: gift_total_new})

# tang171／tang173：總鏈 ＋v300 +44；DEF 鏈 ＋v300 +7（DEF 42339→42346，guard 42345→42352，index 42338→42345）
for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    lines = open(ROOT + "/" + fname, encoding="utf-8").read().splitlines()
    tot_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：總行數 47093"))
    def_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：openLoc DEF 行 42339"))
    guard_old = next(ln for ln in lines if "len(lines) >= 42345 and 'function openLoc(id, opts){' in lines[42338]" in ln)
    tot_new = tot_old.replace("總行數 47093（", "總行數 47137（", 1).replace(
        "＋v299 +280）', src.count('\\n') == 47093", "＋v299 +280＋v300 +44）', src.count('\\n') == 47137", 1)
    def_new = def_old.replace("openLoc DEF 行 42339（", "openLoc DEF 行 42346（", 1).replace(
        "＋v299 +280，travel114 釘行", "＋v299 +280＋v300 +7，travel114 釘行", 1)
    guard_new = guard_old.replace("len(lines) >= 42345", "len(lines) >= 42352", 1).replace("lines[42338]", "lines[42345]", 1)
    assert all(x != y for x, y in ((tot_old, tot_new), (def_old, def_new), (guard_old, guard_new)))
    resync(fname, {tot_old: tot_new, def_old: def_new, guard_old: guard_new})

# rom159：3 釘 ＋7＋全佳行 ＋7（ok() 名入面嘅 L 號係歷史標籤，唔郁）
resync("tests/test_rom159_static.py", {
    'ok("行號釘 ROM159 block 頭 25499", line_has(25459, "v20a159 ROM159 Phase 1"))':
    'ok("行號釘 ROM159 block 頭 25499", line_has(25466, "v20a159 ROM159 Phase 1"))',
    'ok("行號釘 CMT_lan_commit 26333", line_has(26307, "COMMIT48_NODES.CMT_lan_commit"))':
    'ok("行號釘 CMT_lan_commit 26333", line_has(26314, "COMMIT48_NODES.CMT_lan_commit"))',
    'ok("行號釘 rom159SoMeetGate 26248", line_has(26208, "function rom159SoMeetGate"))':
    'ok("行號釘 rom159SoMeetGate 26248", line_has(26215, "function rom159SoMeetGate"))',
    'ok("全佳只出現喺 ROM159 查實註解", idx.count("全佳") == 1 and "查實" in idx_lines[25487 - 1])  # v20a159 整合：B1＋B2 後行號 +86':
    'ok("全佳只出現喺 ROM159 查實註解", idx.count("全佳") == 1 and "查實" in idx_lines[25494 - 1])  # v20a159 整合：B1＋B2 後行號 +86',
})

# rom176：4 釘 ＋7（ok() 名入面嘅 L 號係歷史標籤，唔郁）
resync("tests/test_rom176_static.py", {
    "ok('釘：ROM176 block 起點 L55647', line(40574).startswith('/* ===== v20a176 ROM176'))":
    "ok('釘：ROM176 block 起點 L55647', line(40581).startswith('/* ===== v20a176 ROM176'))",
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(40924).startswith('function rom176ApplyGiftOverrides()'))":
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(40931).startswith('function rom176ApplyGiftOverrides()'))",
    "ok('釘：addLocTalkGiftActs L57154', line(42224).startswith('function addLocTalkGiftActs(add, L, npcId)'))":
    "ok('釘：addLocTalkGiftActs L57154', line(42231).startswith('function addLocTalkGiftActs(add, L, npcId)'))",
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42380))":
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42387))",
})

# travel114：DEF／WRAPPER／COUNT／FREE——逐行全文做 key（重疊對 45456→45500／45500→45544 一次過換，唔會撞值）
t114 = {}
t114["DEF_LINE = 42339      # function openLoc(id, opts){"] = "DEF_LINE = 42346      # function openLoc(id, opts){"
t114["WRAPPER_LINE = 29096  # window.__phase2.openLoc：轉發 opts"] = "WRAPPER_LINE = 29103  # window.__phase2.openLoc：轉發 opts"
count_map = {20875: 20882, 22078: 22085, 22518: 22525, 22521: 22528, 22552: 22559,
             28527: 28534, 45578: 45622, 45786: 45830, 45944: 45988, 45965: 46009}
free_map = {24714: 24721, 26058: 26065, 26059: 26066, 26135: 26142, 28335: 28342,
            28368: 28375, 40372: 40379, 40491: 40498, 40566: 40573, 40766: 40773,
            40810: 40817, 40816: 40823, 40883: 40890, 40885: 40892, 40888: 40895,
            40915: 40922, 42187: 42194, 42234: 42241, 42604: 42611, 42626: 42633,
            42778: 42785, 42783: 42790, 43708: 43715, 45185: 45192, 45455: 45499,
            45456: 45500, 45500: 45544, 45501: 45545, 45526: 45570, 46415: 46459}
for ln in open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read().splitlines():
    s = ln.strip()
    if s and (s.rstrip(",").split(",")[0].strip().isdigit()):
        num = int(s.split(",")[0].strip())
        if num in count_map or num in free_map:
            new_num = count_map.get(num, free_map.get(num))
            # 只換行首數字，保留註解
            t114[ln] = ln.replace(str(num), str(new_num), 1)
assert len(t114) == 2 + len(count_map) + len(free_map), len(t114)
resync("tests/test_travel114_static.py", t114)

print("resync300 完成：6 檔已改，全部錨點 difflib 核實純漂移。")
