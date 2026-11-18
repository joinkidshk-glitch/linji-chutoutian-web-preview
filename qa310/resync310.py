# v20a310 resync：index.html 淨 +10 行（Q23 程 e4 N15 旗變體：enc79BuildScript 分流 block ＋10 @舊 L40244 前；
# 總行數 47275→47285；其後釘行一律 ＋10（插入點舊 L40244，全部錨點 ≥40244），difflib 對位核實純漂移。
# 單次掃描 dict 查表（v160 教訓：唔逐對 re.sub；v162 教訓：重疊對要一次過換——
# 本檔用逐行全文做 key，唔會撞值）。
import difflib, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work310"
old = subprocess.check_output(["git", "show", "HEAD:index.html"], cwd=ROOT, text=True).splitlines()
new = open(ROOT + "/index.html", encoding="utf-8").read().splitlines()
assert len(old) == 47275, len(old)
assert len(new) == 47285, len(new)

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
# 插入區邊界：chai_finale block 收尾行之前唔郁、pushSeg 之後 ＋10
check(40243, 40243, '}')
check(40244, 40254, 'pushSeg(beatSeg100')
# 新插入行本身在位（唔經 mapping，用新行號直接驗）
assert 'v20a310 Q23' in new[40244 - 1] and 'N15' in new[40244 - 1], new[40244 - 1][:90]
assert 'flag_vocal_train' in new[40249 - 1] and '你嗰晚都係咁揀，我信你' in new[40249 - 1], new[40249 - 1][:90]
assert 'flag_vocal_polish' in new[40250 - 1] and '你嗰晚都係靠部機交帶㗎' in new[40250 - 1], new[40250 - 1][:90]
print("OK 新插入行在位：v310 分流 block L40244–40253")
# rom176：4 釘（全部 ≥40244，＋10）
check(40716, 40726, 'v20a176 ROM176')
check(41066, 41076, 'function rom176ApplyGiftOverrides()')
check(42369, 42379, 'function addLocTalkGiftActs(add, L, npcId)')
check(42525, 42535, 'rom176TryIntercept(id)')
# travel114 DEF（＋10）；WRAPPER 29103 喺插入點之前，唔郁
check(42484, 42494, 'function openLoc(id, opts){')
check(29103, 29103, 'openLoc: function(id, opts){ openLoc(id, opts); }')
# travel114 COUNT（4 處，全部 ≥40244，＋10；15363–28534 嗰 8 處喺插入點之前，唔郁）
for o, n in [(15363, 15363), (18672, 18672), (20882, 20882), (22085, 22085),
             (22525, 22525), (22528, 22528), (22559, 22559), (28534, 28534),
             (45760, 45770), (45968, 45978), (46126, 46136), (46147, 46157)]:
    check(o, n, 'openLoc(')
# travel114 FREE（24 處 ≥40244，＋10；6525–28375 嗰 16 處喺插入點之前，唔郁）
for o, n in [(6525, 6525), (6526, 6526), (8217, 8217), (14215, 14215),
             (14216, 14216), (14228, 14228), (14229, 14229), (14240, 14240),
             (14241, 14241), (14341, 14341), (24721, 24721), (26065, 26065),
             (26066, 26066), (26142, 26142), (28342, 28342), (28375, 28375),
             (40514, 40524), (40633, 40643), (40708, 40718), (40908, 40918),
             (40952, 40962), (40958, 40968), (41025, 41035), (41027, 41037),
             (41030, 41040), (41057, 41067), (42332, 42342), (42379, 42389),
             (42749, 42759), (42771, 42781), (42923, 42933), (42928, 42938),
             (43853, 43863), (45330, 45340), (45637, 45647), (45638, 45648),
             (45682, 45692), (45683, 45693), (45708, 45718), (46597, 46607)]:
    check(o, n, 'openLoc(')
print("OK 總行數 舊 47275 → 新 47285")

# --- 單次掃描 dict 查表改 5 檔（每條舊行出現且只出現一次） ---
HEADER = "# v20a310 resync：index.html 淨 +10 行（Q23：enc79BuildScript ching_e4 N15 變體分流 ＋10 @舊 L40244 前；總行數 47275→47285；其後釘行一律 ＋10，difflib 對位核實純漂移，見 qa310/resync310.py）。\n"

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

# gift185：總行數鏈尾 ＋v310 +10（47275→47285）
lines = open(ROOT + "/tests/test_gift185_static.py", encoding="utf-8").read().splitlines()
tot_old = next(ln for ln in lines if ln.startswith("ok('總行數 47275"))
tot_new = tot_old.replace("總行數 47275（", "總行數 47285（", 1).replace(
    "＋v309 +33）'", "＋v309 +33＋v310 +10）'", 1).replace("== 47275", "== 47285", 1)
assert tot_old != tot_new
resync("tests/test_gift185_static.py", {tot_old: tot_new})

# tang171／tang173：總行數鏈尾 ＋v310 +10、DEF 行 42484→42494、guard 行同步 ＋10
for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    lines = open(ROOT + "/" + fname, encoding="utf-8").read().splitlines()
    tot_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：總行數 47275"))
    def_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：openLoc DEF 行 42484"))
    guard_old = next(ln for ln in lines if "len(lines) >= 42490 and 'function openLoc(id, opts){' in lines[42483]" in ln)
    tot_new = tot_old.replace("總行數 47275（", "總行數 47285（", 1).replace(
        "＋v309 +33）'", "＋v309 +33＋v310 +10）'", 1).replace("== 47275", "== 47285", 1)
    def_new = def_old.replace("openLoc DEF 行 42484（", "openLoc DEF 行 42494（", 1).replace(
        "＋v309 +33，travel114 釘行", "＋v309 +33＋v310 +10，travel114 釘行", 1)
    guard_new = guard_old.replace("len(lines) >= 42490", "len(lines) >= 42500", 1).replace("lines[42483]", "lines[42493]", 1)
    assert all(x != y for x, y in ((tot_old, tot_new), (def_old, def_new), (guard_old, guard_new)))
    resync(fname, {tot_old: tot_new, def_old: def_new, guard_old: guard_new})

# rom176：4 釘 ＋10（ok() 名入面嘅 L 號係歷史標籤，唔郁）
resync("tests/test_rom176_static.py", {
    "ok('釘：ROM176 block 起點 L55647', line(40716).startswith('/* ===== v20a176 ROM176'))":
    "ok('釘：ROM176 block 起點 L55647', line(40726).startswith('/* ===== v20a176 ROM176'))",
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41066).startswith('function rom176ApplyGiftOverrides()'))":
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41076).startswith('function rom176ApplyGiftOverrides()'))",
    "ok('釘：addLocTalkGiftActs L57154', line(42369).startswith('function addLocTalkGiftActs(add, L, npcId)'))":
    "ok('釘：addLocTalkGiftActs L57154', line(42379).startswith('function addLocTalkGiftActs(add, L, npcId)'))",
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42525))":
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42535))",
})

# travel114：DEF／COUNT／FREE——逐行全文做 key（重疊對一次過換，唔會撞值）
t114 = {}
t114["DEF_LINE = 42484      # function openLoc(id, opts){"] = "DEF_LINE = 42494      # function openLoc(id, opts){"
count_map = {45760: 45770, 45968: 45978, 46126: 46136, 46147: 46157}
free_map = {40514: 40524, 40633: 40643, 40708: 40718, 40908: 40918,
            40952: 40962, 40958: 40968, 41025: 41035, 41027: 41037,
            41030: 41040, 41057: 41067, 42332: 42342, 42379: 42389,
            42749: 42759, 42771: 42781, 42923: 42933, 42928: 42938,
            43853: 43863, 45330: 45340, 45637: 45647, 45638: 45648,
            45682: 45692, 45683: 45693, 45708: 45718, 46597: 46607}
t114_lines = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read().splitlines()
for old_n, new_n in list(count_map.items()) + list(free_map.items()):
    old_ln = next(ln for ln in t114_lines if ln.strip().startswith(str(old_n) + ","))
    assert mapping[old_n] == new_n, "映射唔啱：%d→%s（預期 %d）" % (old_n, mapping.get(old_n), new_n)
    t114[old_ln] = old_ln.replace(str(old_n) + ",", str(new_n) + ",", 1)
assert len(t114) == 1 + len(count_map) + len(free_map)
resync("tests/test_travel114_static.py", t114)
print("resync310 完成")
