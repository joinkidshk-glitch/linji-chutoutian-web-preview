# v20a319 resync：index.html 淨 +1 行（BR89 加第 18 對：表頭註解 ＋1 @舊 L26703 後（舊 v317 行尾 */ 移去新行）；總行數 47285→47286；
# 錨點按段 shift（≤26702 唔郁、舊 L26703 同行改內容、≥26704 ＋1），difflib 對位核實純漂移。
# 單次掃描 dict 查表（v160 教訓：唔逐對 re.sub；v162 教訓：重疊對要一次過換——
# 本檔用逐行全文做 key，唔會撞值）。
import difflib, re, subprocess

ROOT = "/home/hatch/workspace/linji-work319"
old = subprocess.check_output(["git", "show", "HEAD:index.html"], cwd=ROOT, text=True).splitlines()
new = open(ROOT + "/index.html", encoding="utf-8").read().splitlines()
assert len(old) == 47285, len(old)
assert len(new) == 47286, len(new)

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

def expect(old_n):
    # 按段 shift：≤26702 唔郁、舊 L26703 同行改內容、≥26704 ＋1
    if old_n <= 26702:
        return old_n
    return old_n + 1

# --- 插入區邊界 ---
check(26701, 26701, 'v20a284 R5-F')
check(26704, 26705, 'const BR89_PATRON_OF_GIG')
# 舊 L26705 同行改內容（行尾加 variety_106 對），唔經 mapping，直接驗新行
assert 'gig_1992_variety_106' not in old[26705 - 1] and 'gig_1991_variety_203' in old[26705 - 1], old[26705 - 1][:90]
assert 'gig_1992_variety_106' in new[26706 - 1] and 'gig_1991_variety_203' in new[26706 - 1] and 'credit_enc84_pang_patron' in new[26706 - 1], new[26706 - 1][:90]
print("OK 新映射行在位：variety_106 對 新 L26706（排 variety_203 隔籬）")
check(42494, 42495, 'function openLoc(id, opts){')
check(29107, 29108, 'openLoc: function(id, opts){ openLoc(id, opts); }')
# 舊 L26703 同行改內容（行尾 */ 移去新行），唔經 mapping，直接驗新行
assert old[26703 - 1].rstrip().endswith('*/') and new[26703 - 1].rstrip().endswith('名）。') and 'v20a317' in new[26703 - 1], new[26703 - 1][:90]
assert 'v20a319' in new[26704 - 1] and 'gig_1992_variety_106' in new[26704 - 1], new[26704 - 1][:90]
print("OK 新插入行在位：v319 表頭註解 新 L26704；舊 L26703 行尾 */ 已移走")
print("OK 總行數 舊 47285 → 新 47286")

# --- 逐字核實全部錨點（純漂移） ---
# rom176：全部 line(N) 引用（6321／14781 唔郁、40726／41076／42379／42535 各 ＋1）
rom = open(ROOT + "/tests/test_rom176_static.py", encoding="utf-8").read()
for m in re.finditer(r"line\((\d+)\)", rom):
    o = int(m.group(1))
    check(o, expect(o))
# travel114：COUNT 12 處＋FREE 40 處＋DEF／WRAPPER
t114 = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read()
count_set = set(int(x) for x in re.search(r"COUNT_LINES = \{([^}]*)\}", t114, re.S).group(1).replace(",", " ").split() if x.isdigit())
free_set = set(int(x) for x in re.search(r"FREE_LINES = \{([^}]*)\}", t114, re.S).group(1).replace(",", " ").split() if x.isdigit())
assert len(count_set) == 12, len(count_set)
assert len(free_set) == 40, len(free_set)
for o in sorted(count_set | free_set):
    check(o, expect(o), 'openLoc(')
check(42494, 42495, 'function openLoc(id, opts){')
check(29107, 29108, 'openLoc: function(id, opts){ openLoc(id, opts); }')
# tang171／173：DEF 行（guard 行在測試檔，見下 resync 斷言）
check(42494, 42495, 'function openLoc(id, opts){')
print("OK 全部錨點純漂移核實完成")

# --- 單次掃描 dict 查表改 5 檔（每條舊行出現且只出現一次） ---
HEADER = "# v20a319 resync：index.html 淨 +1 行（BR89 加第 18 對：表頭註解 ＋1 @舊 L26703 後；總行數 47285→47286；錨點按段 shift（≤26702 唔郁、≥26704 ＋1），difflib 對位核實純漂移，見 qa319/resync319.py）。\n"

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

# gift185：總行數鏈尾 ＋v319 +1（47285→47286）——已做過就跳過
lines = open(ROOT + "/tests/test_gift185_static.py", encoding="utf-8").read().splitlines()
tot_old = next((ln for ln in lines if ln.startswith("ok('總行數 47285")), None)
if tot_old:
    tot_new = tot_old.replace("總行數 47285（", "總行數 47286（", 1).replace(
        "＋v316 +2＋v317 +2）'", "＋v316 +2＋v317 +2＋v319 +1）'", 1).replace("== 47285", "== 47286", 1)
    assert tot_old != tot_new
    resync("tests/test_gift185_static.py", {tot_old: tot_new})
else:
    print("跳過 gift185（已 resync）")

# tang171／tang173：總行數鏈尾 ＋v319 +1、DEF 行 42494→42495、guard 行同步 ＋1——已做過就跳過
for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    lines = open(ROOT + "/" + fname, encoding="utf-8").read().splitlines()
    tot_old = next((ln for ln in lines if ln.startswith("ok('零行數漂移：總行數 47285")), None)
    if not tot_old:
        print("跳過 %s（已 resync）" % fname)
        continue
    def_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：openLoc DEF 行 42494"))
    guard_old = next(ln for ln in lines if "len(lines) >= 42500 and 'function openLoc(id, opts){' in lines[42493]" in ln)
    tot_new = tot_old.replace("總行數 47285（", "總行數 47286（", 1).replace(
        "＋v316 +2＋v317 +2）'", "＋v316 +2＋v317 +2＋v319 +1）'", 1).replace("== 47285", "== 47286", 1)
    def_new = def_old.replace("openLoc DEF 行 42494（", "openLoc DEF 行 42495（", 1).replace(
        "＋v316 +2＋v317 +2，travel114 釘行", "＋v316 +2＋v317 +2＋v319 +1，travel114 釘行", 1)
    guard_new = guard_old.replace("len(lines) >= 42500", "len(lines) >= 42501", 1).replace("lines[42493]", "lines[42494]", 1)
    assert all(x != y for x, y in ((tot_old, tot_new), (def_old, def_new), (guard_old, guard_new)))
    resync(fname, {tot_old: tot_new, def_old: def_new, guard_old: guard_new})

# rom176：4 釘 ＋1（ok() 名入面嘅 L 號係歷史標籤，唔郁）
resync("tests/test_rom176_static.py", {
    "ok('釘：ROM176 block 起點 L55647', line(40726).startswith('/* ===== v20a176 ROM176'))":
    "ok('釘：ROM176 block 起點 L55647', line(40727).startswith('/* ===== v20a176 ROM176'))",
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41076).startswith('function rom176ApplyGiftOverrides()'))":
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41077).startswith('function rom176ApplyGiftOverrides()'))",
    "ok('釘：addLocTalkGiftActs L57154', line(42379).startswith('function addLocTalkGiftActs(add, L, npcId)'))":
    "ok('釘：addLocTalkGiftActs L57154', line(42380).startswith('function addLocTalkGiftActs(add, L, npcId)'))",
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42535))":
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42536))",
})

# travel114：DEF／WRAPPER／COUNT／FREE——逐行全文做 key（重疊對一次過換，唔會撞值）
t114_map = {}
t114_map["DEF_LINE = 42494      # function openLoc(id, opts){"] = "DEF_LINE = 42495      # function openLoc(id, opts){"
t114_map["WRAPPER_LINE = 29107  # window.__phase2.openLoc：轉發 opts"] = "WRAPPER_LINE = 29108  # window.__phase2.openLoc：轉發 opts"
t114_lines = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read().splitlines()
shifted = 0
for old_n in sorted(count_set | free_set):
    new_n = expect(old_n)
    if new_n == old_n:
        continue
    old_ln = next(ln for ln in t114_lines if ln.strip().startswith(str(old_n) + ","))
    assert mapping[old_n] == new_n, "映射唔啱：%d→%s（預期 %d）" % (old_n, mapping.get(old_n), new_n)
    t114_map[old_ln] = old_ln.replace(str(old_n) + ",", str(new_n) + ",", 1)
    shifted += 1
assert len(t114_map) == 2 + shifted, len(t114_map)
print("travel114 換咗 DEF＋WRAPPER＋%d 處 COUNT／FREE 行" % shifted)
resync("tests/test_travel114_static.py", t114_map)
print("resync319 完成")
