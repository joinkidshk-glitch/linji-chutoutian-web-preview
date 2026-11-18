# v20a315 resync：index.html 淨 +15 行（Q25 鍾 Beat 3 泄漏花邊：build block ＋13 @舊 L34338 前（v302 block 之後）＋commit 記旗 ＋2 @舊 L34621 前；
# 總行數 47266→47281；錨點按段 shift（＜34338 唔郁、34338–34620 ＋13、≥34621 ＋15），difflib 對位核實純漂移。
# 單次掃描 dict 查表（v160 教訓：唔逐對 re.sub；v162 教訓：重疊對要一次過換——
# 本檔用逐行全文做 key，唔會撞值）。
import difflib, re, subprocess

ROOT = "/home/hatch/workspace/linji-work315"
old = subprocess.check_output(["git", "show", "HEAD:index.html"], cwd=ROOT, text=True).splitlines()
new = open(ROOT + "/index.html", encoding="utf-8").read().splitlines()
assert len(old) == 47266, len(old)
assert len(new) == 47281, len(new)

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
    # 按段 shift：＜34338 唔郁、34338–34620 ＋13、≥34621 ＋15
    if old_n < 34338:
        return old_n
    if old_n <= 34620:
        return old_n + 13
    return old_n + 15

# --- 插入區邊界 ---
check(34337, 34337, '}catch(_e302){}')
check(34338, 34351, 'const fameDelta')
check(34620, 34633, 'side_chung_farewell302')
check(34621, 34636, 'S.pendingMorningPaper = null;')
# 新插入行本身在位（唔經 mapping，用新行號直接驗）
assert 'v20a315 Q25' in new[34338 - 1] and 'chung_loose_talk' in new[34338 - 1], new[34338 - 1][:90]
assert 'side_chung_loose315' in new[34349 - 1] and '聽聞有女星赴加手續辦緊' in new[34349 - 1], new[34349 - 1][:90]
assert 'v20a315 Q25' in new[34634 - 1], new[34634 - 1][:90]
assert 'side_chung_loose315' in new[34635 - 1] and 'chungLooseTalkPaper315' in new[34635 - 1], new[34635 - 1][:90]
print("OK 新插入行在位：v315 build block 新 L34338–34350、commit 記旗 新 L34634–34635")
print("OK 總行數 舊 47266 → 新 47281")

# --- 逐字核實全部錨點（純漂移） ---
# rom176：全部 line(N) 引用（6 處：6321／14781 唔郁、40707／41057／42360／42516 各 ＋15）
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
check(42475, 42490, 'function openLoc(id, opts){')
check(29103, 29103, 'openLoc: function(id, opts){ openLoc(id, opts); }')
# tang171／173：DEF 行（guard 行在測試檔，見下 resync 斷言）
check(42475, 42490, 'function openLoc(id, opts){')
print("OK 全部錨點純漂移核實完成")

# --- 單次掃描 dict 查表改 5 檔（每條舊行出現且只出現一次） ---
HEADER = "# v20a315 resync：index.html 淨 +15 行（Q25：鍾 Beat 3 泄漏花邊 build block ＋13 @舊 L34338 前＋commit 記旗 ＋2 @舊 L34621 前；總行數 47266→47281；錨點按段 shift（＜34338 唔郁、34338–34620 ＋13、≥34621 ＋15），difflib 對位核實純漂移，見 qa315/resync315.py）。\n"

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

# gift185：總行數鏈尾 ＋v315 +15（47266→47281）
lines = open(ROOT + "/tests/test_gift185_static.py", encoding="utf-8").read().splitlines()
tot_old = next(ln for ln in lines if ln.startswith("ok('總行數 47266"))
tot_new = tot_old.replace("總行數 47266（", "總行數 47281（", 1).replace(
    "＋v313 −19）'", "＋v313 −19＋v315 +15）'", 1).replace("== 47266", "== 47281", 1)
assert tot_old != tot_new
resync("tests/test_gift185_static.py", {tot_old: tot_new})

# tang171／tang173：總行數鏈尾 ＋v315 +15、DEF 行 42475→42490、guard 行同步 ＋15
for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    lines = open(ROOT + "/" + fname, encoding="utf-8").read().splitlines()
    tot_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：總行數 47266"))
    def_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：openLoc DEF 行 42475"))
    guard_old = next(ln for ln in lines if "len(lines) >= 42481 and 'function openLoc(id, opts){' in lines[42474]" in ln)
    tot_new = tot_old.replace("總行數 47266（", "總行數 47281（", 1).replace(
        "＋v313 −19）'", "＋v313 −19＋v315 +15）'", 1).replace("== 47266", "== 47281", 1)
    def_new = def_old.replace("openLoc DEF 行 42475（", "openLoc DEF 行 42490（", 1).replace(
        "＋v313 −19，travel114 釘行", "＋v313 −19＋v315 +15，travel114 釘行", 1)
    guard_new = guard_old.replace("len(lines) >= 42481", "len(lines) >= 42496", 1).replace("lines[42474]", "lines[42489]", 1)
    assert all(x != y for x, y in ((tot_old, tot_new), (def_old, def_new), (guard_old, guard_new)))
    resync(fname, {tot_old: tot_new, def_old: def_new, guard_old: guard_new})

# rom176：4 釘 ＋15（ok() 名入面嘅 L 號係歷史標籤，唔郁）
resync("tests/test_rom176_static.py", {
    "ok('釘：ROM176 block 起點 L55647', line(40707).startswith('/* ===== v20a176 ROM176'))":
    "ok('釘：ROM176 block 起點 L55647', line(40722).startswith('/* ===== v20a176 ROM176'))",
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41057).startswith('function rom176ApplyGiftOverrides()'))":
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41072).startswith('function rom176ApplyGiftOverrides()'))",
    "ok('釘：addLocTalkGiftActs L57154', line(42360).startswith('function addLocTalkGiftActs(add, L, npcId)'))":
    "ok('釘：addLocTalkGiftActs L57154', line(42375).startswith('function addLocTalkGiftActs(add, L, npcId)'))",
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42516))":
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42531))",
})

# travel114：DEF／COUNT／FREE——逐行全文做 key（重疊對一次過換，唔會撞值）
t114_map = {}
t114_map["DEF_LINE = 42475      # function openLoc(id, opts){"] = "DEF_LINE = 42490      # function openLoc(id, opts){"
t114_lines = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read().splitlines()
for old_n in sorted(count_set | free_set):
    new_n = expect(old_n)
    if new_n == old_n:
        continue
    old_ln = next(ln for ln in t114_lines if ln.strip().startswith(str(old_n) + ","))
    assert mapping[old_n] == new_n, "映射唔啱：%d→%s（預期 %d）" % (old_n, mapping.get(old_n), new_n)
    t114_map[old_ln] = old_ln.replace(str(old_n) + ",", str(new_n) + ",", 1)
assert len(t114_map) == 1 + 4 + 24, len(t114_map)  # DEF 1＋COUNT 4 處＋FREE 24 處
resync("tests/test_travel114_static.py", t114_map)
print("resync315 完成")
