# v20a317 resync：index.html 淨 +2 行（BR89 加第 17 對：表頭註解 ＋1 @舊 L26702 後＋tv_114 映射行 ＋1 @舊 L26710 後；
# 總行數 47283→47285；錨點按段 shift（＜26702 唔郁、26702 同行改內容（v316 行尾 */ 移去新行）、26703–26710 ＋1、≥26711 ＋2），difflib 對位核實純漂移。
# 單次掃描 dict 查表（v160 教訓：唔逐對 re.sub；v162 教訓：重疊對要一次過換——
# 本檔用逐行全文做 key，唔會撞值）。
import difflib, re, subprocess

ROOT = "/home/hatch/workspace/linji-work317"
old = subprocess.check_output(["git", "show", "HEAD:index.html"], cwd=ROOT, text=True).splitlines()
new = open(ROOT + "/index.html", encoding="utf-8").read().splitlines()
assert len(old) == 47283, len(old)
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

def expect(old_n):
    # 按段 shift：＜26702 唔郁、26702 同行改內容、26703–26710 ＋1、≥26711 ＋2
    if old_n <= 26702:
        return old_n
    if old_n <= 26710:
        return old_n + 1
    return old_n + 2

# --- 插入區邊界 ---
check(26701, 26701, 'v20a284 R5-F')
check(26703, 26704, 'const BR89_PATRON_OF_GIG')
check(26710, 26711, 'gig_1992_film_206')
check(26711, 26713, 'gig_1992_film_202')
check(26714, 26716, '};')
check(26715, 26717, 'const BR89_GIGS')
# 舊 L26702 同行改內容（行尾 */ 移去新行），唔經 mapping，直接驗新行
assert old[26702 - 1].rstrip().endswith('*/') and new[26702 - 1].rstrip().endswith('名）。') and 'v20a316' in new[26702 - 1], new[26702 - 1][:90]
assert 'v20a317' in new[26703 - 1] and 'gig_1991_tv_114' in new[26703 - 1], new[26703 - 1][:90]
assert 'gig_1991_tv_114' in new[26712 - 1] and 'credit_enc83_chai_patron' in new[26712 - 1], new[26712 - 1][:90]
print("OK 新插入行在位：v317 表頭註解 新 L26703、tv_114 映射行 新 L26712；舊 L26702 行尾 */ 已移走")
print("OK 總行數 舊 47283 → 新 47285")

# --- 逐字核實全部錨點（純漂移） ---
# rom176：全部 line(N) 引用（6 處：6321／14781 唔郁、40722／41072／42375／42531 各 ＋2）
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
check(42492, 42494, 'function openLoc(id, opts){')
check(29105, 29107, 'openLoc: function(id, opts){ openLoc(id, opts); }')
# tang171／173：DEF 行（guard 行在測試檔，見下 resync 斷言）
check(42492, 42494, 'function openLoc(id, opts){')
print("OK 全部錨點純漂移核實完成")

# --- 單次掃描 dict 查表改 5 檔（每條舊行出現且只出現一次） ---
HEADER = "# v20a317 resync：index.html 淨 +2 行（BR89 加第 17 對：表頭註解 ＋1 @舊 L26702 後＋tv_114 映射行 ＋1 @舊 L26710 後；總行數 47283→47285；錨點按段 shift（＜26702 唔郁、26702 同行改內容、26703–26710 ＋1、≥26711 ＋2），difflib 對位核實純漂移，見 qa317/resync317.py）。\n"

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

# gift185：總行數鏈尾 ＋v317 +2（47283→47285）——已做過就跳過
lines = open(ROOT + "/tests/test_gift185_static.py", encoding="utf-8").read().splitlines()
tot_old = next((ln for ln in lines if ln.startswith("ok('總行數 47283")), None)
if tot_old:
    tot_new = tot_old.replace("總行數 47283（", "總行數 47285（", 1).replace(
        "＋v316 +2）'", "＋v316 +2＋v317 +2）'", 1).replace("== 47283", "== 47285", 1)
    assert tot_old != tot_new
    resync("tests/test_gift185_static.py", {tot_old: tot_new})
else:
    print("跳過 gift185（已 resync）")

# tang171／tang173：總行數鏈尾 ＋v317 +2、DEF 行 42492→42494、guard 行同步 ＋2——已做過就跳過
for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    lines = open(ROOT + "/" + fname, encoding="utf-8").read().splitlines()
    tot_old = next((ln for ln in lines if ln.startswith("ok('零行數漂移：總行數 47283")), None)
    if not tot_old:
        print("跳過 %s（已 resync）" % fname)
        continue
    def_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：openLoc DEF 行 42492"))
    guard_old = next(ln for ln in lines if "len(lines) >= 42498 and 'function openLoc(id, opts){' in lines[42491]" in ln)
    tot_new = tot_old.replace("總行數 47283（", "總行數 47285（", 1).replace(
        "＋v316 +2）'", "＋v316 +2＋v317 +2）'", 1).replace("== 47283", "== 47285", 1)
    def_new = def_old.replace("openLoc DEF 行 42492（", "openLoc DEF 行 42494（", 1).replace(
        "＋v316 +2，travel114 釘行", "＋v316 +2＋v317 +2，travel114 釘行", 1)
    guard_new = guard_old.replace("len(lines) >= 42498", "len(lines) >= 42500", 1).replace("lines[42491]", "lines[42493]", 1)
    assert all(x != y for x, y in ((tot_old, tot_new), (def_old, def_new), (guard_old, guard_new)))
    resync(fname, {tot_old: tot_new, def_old: def_new, guard_old: guard_new})

# rom176：4 釘 ＋2（ok() 名入面嘅 L 號係歷史標籤，唔郁；檔內現行數字已係 v316 移位後嘅 40724／41074／42377／42533）
resync("tests/test_rom176_static.py", {
    "ok('釘：ROM176 block 起點 L55647', line(40724).startswith('/* ===== v20a176 ROM176'))":
    "ok('釘：ROM176 block 起點 L55647', line(40726).startswith('/* ===== v20a176 ROM176'))",
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41074).startswith('function rom176ApplyGiftOverrides()'))":
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41076).startswith('function rom176ApplyGiftOverrides()'))",
    "ok('釘：addLocTalkGiftActs L57154', line(42377).startswith('function addLocTalkGiftActs(add, L, npcId)'))":
    "ok('釘：addLocTalkGiftActs L57154', line(42379).startswith('function addLocTalkGiftActs(add, L, npcId)'))",
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42533))":
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42535))",
})

# travel114：DEF／WRAPPER／COUNT／FREE——逐行全文做 key（重疊對一次過換，唔會撞值）
t114_map = {}
t114_map["DEF_LINE = 42492      # function openLoc(id, opts){"] = "DEF_LINE = 42494      # function openLoc(id, opts){"
t114_map["WRAPPER_LINE = 29105  # window.__phase2.openLoc：轉發 opts"] = "WRAPPER_LINE = 29107  # window.__phase2.openLoc：轉發 opts"
t114_lines = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read().splitlines()
for old_n in sorted(count_set | free_set):
    new_n = expect(old_n)
    if new_n == old_n:
        continue
    old_ln = next(ln for ln in t114_lines if ln.strip().startswith(str(old_n) + ","))
    assert mapping[old_n] == new_n, "映射唔啱：%d→%s（預期 %d）" % (old_n, mapping.get(old_n), new_n)
    t114_map[old_ln] = old_ln.replace(str(old_n) + ",", str(new_n) + ",", 1)
assert len(t114_map) == 2 + 5 + 26, len(t114_map)  # DEF＋WRAPPER 2＋COUNT 5 處＋FREE 26 處
resync("tests/test_travel114_static.py", t114_map)
print("resync317 完成")
