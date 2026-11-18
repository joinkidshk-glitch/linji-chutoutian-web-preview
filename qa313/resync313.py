# v20a313 resync：index.html 淨 −19 行（Q26 高俊傑同場兩段刪：
# 結果卡 rivalHeadBit IIFE 14 行 @舊 L31295–31308＋模板插值 1 行改動 @舊 L31389；
# 典禮 koF208 block 5 行 @舊 L32169–32173；總行數 47285→47266）。
# 段邊界：＜31295 唔郁；31309–32168 −14；≥32174 −19。
# 本票 5 檔釘行全部喺 ＜31295 或 ≥32174 段（−14 段無釘行，difflib 逐個核實）。
# 單次掃描 dict 查表（v160 教訓：唔逐對 re.sub；v162 教訓：重疊對要一次過換——
# 本檔用逐行全文做 key，唔會撞值）。
import difflib, subprocess

ROOT = "/home/hatch/workspace/linji-work313"
old = subprocess.check_output(["git", "show", "HEAD:index.html"], cwd=ROOT, text=True).splitlines()
new = open(ROOT + "/index.html", encoding="utf-8").read().splitlines()
assert len(old) == 47285, len(old)
assert len(new) == 47266, len(new)

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

# --- 刪除區核實：用 opcodes（唔用 mapping——difflib 會將刪除區入面嘅 `}` 行
#     對位去附近相同內容行，`not in mapping` 斷言太嚴）---
ops = [(tag, a0, a1, b0, b1) for tag, a0, a1, b0, b1 in sm.get_opcodes() if tag != 'equal']
assert len(ops) == 3, "非 equal 區預期 3 處，實際 %d：%s" % (len(ops), ops)
assert ops[0] == ('delete', 31294, 31308, 31294, 31294), "第一處唔係 rivalHeadBit 刪除：%s" % (ops[0],)
assert ops[1] == ('replace', 31388, 31389, 31374, 31375), "第二處唔係模板行改動：%s" % (ops[1],)
assert ops[2] == ('delete', 32167, 32172, 32153, 32153), "第三處唔係 koF208 刪除：%s" % (ops[2],)
assert 'rivalHeadBit' in old[31388] and 'rivalHeadBit' not in new[31374], "模板行插值未清"
assert '${catsHtml}${felBit186}' in new[31374], new[31374][:90]
print("OK 刪除區＋模板行：唯一差異係兩段 19 行＋模板插值 1 行（opcodes 核實）")
# 段邊界核實（舊 L32168 `}` 喺刪除區內無映射；L32167 `});` 同 L32173 `}` 先係邊界）
check(31294, 31294)
check(31309, 31295)
check(32167, 32153, '});')
check(32173, 32154, '}')
check(32174, 32155, 'suspense')

# --- 逐字核實全部要改嘅釘行（純漂移） ---
# rom176：4 釘（全部 ≥32174，−19）
check(40726, 40707, '/* ===== v20a176 ROM176')
check(41076, 41057, 'function rom176ApplyGiftOverrides()')
check(42379, 42360, 'function addLocTalkGiftActs(add, L, npcId)')
check(42535, 42516, 'rom176TryIntercept(id)')
# rom176 其餘釘（＜31295，唔郁）
check(6321, 6321, 'lan:{ id:"lan"')
check(14781, 14781, 'rom176ApplyGiftOverrides()')
# travel114 DEF（42494→42475，−19）；WRAPPER 29103 唔郁
check(42494, 42475, 'function openLoc(id, opts){')
check(29103, 29103, 'openLoc: function(id, opts){ openLoc(id, opts); }')
# travel114 COUNT（8 處 ＜31295 唔郁；4 處 ≥32174，−19）
for o, n in [(15363, 15363), (18672, 18672), (20882, 20882), (22085, 22085),
             (22525, 22525), (22528, 22528), (22559, 22559), (28534, 28534),
             (45770, 45751), (45978, 45959), (46136, 46117), (46157, 46138)]:
    check(o, n, 'openLoc(')
# travel114 FREE（13 處 ＜31295 唔郁；24 處 ≥32174，−19）
for o, n in [(14215, 14215), (14216, 14216), (14228, 14228), (14229, 14229),
             (14240, 14240), (14241, 14241), (14341, 14341), (24721, 24721),
             (26065, 26065), (26066, 26066), (26142, 26142), (28342, 28342),
             (28375, 28375),
             (40524, 40505), (40643, 40624), (40718, 40699), (40918, 40899),
             (40962, 40943), (40968, 40949), (41035, 41016), (41037, 41018),
             (41040, 41021), (41067, 41048), (42342, 42323), (42389, 42370),
             (42759, 42740), (42781, 42762), (42933, 42914), (42938, 42919),
             (43863, 43844), (45340, 45321), (45647, 45628), (45648, 45629),
             (45692, 45673), (45693, 45674), (45718, 45699), (46607, 46588)]:
    check(o, n, 'openLoc(')
print("OK 總行數 舊 47285 → 新 47266")

# --- 單次掃描 dict 查表改 5 檔（每條舊行出現且只出現一次） ---
HEADER = "# v20a313 resync：index.html 淨 −19 行（Q26：結果卡 rivalHeadBit 14 行＋典禮 koF208 5 行刪；總行數 47285→47266；＜31295 唔郁、≥32174 −19，difflib 對位核實純漂移，見 qa313/resync313.py）。\n"

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

# gift185：總行數鏈尾 ＋v313 −19（47285→47266）
lines = open(ROOT + "/tests/test_gift185_static.py", encoding="utf-8").read().splitlines()
tot_old = next(ln for ln in lines if ln.startswith("ok('總行數 47285"))
tot_new = tot_old.replace("總行數 47285（", "總行數 47266（", 1).replace(
    "＋v310 +10）'", "＋v310 +10＋v313 −19）'", 1).replace("== 47285", "== 47266", 1)
assert tot_old != tot_new
resync("tests/test_gift185_static.py", {tot_old: tot_new})

# tang171／tang173：總行數鏈尾 ＋v313 −19、DEF 行 42494→42475、guard 行同步 −19
for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    lines = open(ROOT + "/" + fname, encoding="utf-8").read().splitlines()
    tot_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：總行數 47285"))
    def_old = next(ln for ln in lines if ln.startswith("ok('零行數漂移：openLoc DEF 行 42494"))
    guard_old = next(ln for ln in lines if "len(lines) >= 42500 and 'function openLoc(id, opts){' in lines[42493]" in ln)
    tot_new = tot_old.replace("總行數 47285（", "總行數 47266（", 1).replace(
        "＋v310 +10）'", "＋v310 +10＋v313 −19）'", 1).replace("== 47285", "== 47266", 1)
    def_new = def_old.replace("openLoc DEF 行 42494（", "openLoc DEF 行 42475（", 1).replace(
        "＋v310 +10，travel114 釘行", "＋v310 +10＋v313 −19，travel114 釘行", 1)
    guard_new = guard_old.replace("len(lines) >= 42500", "len(lines) >= 42481", 1).replace("lines[42493]", "lines[42474]", 1)
    assert all(x != y for x, y in ((tot_old, tot_new), (def_old, def_new), (guard_old, guard_new)))
    resync(fname, {tot_old: tot_new, def_old: def_new, guard_old: guard_new})

# rom176：4 釘 −19（ok() 名入面嘅 L 號係歷史標籤，唔郁）
resync("tests/test_rom176_static.py", {
    "ok('釘：ROM176 block 起點 L55647', line(40726).startswith('/* ===== v20a176 ROM176'))":
    "ok('釘：ROM176 block 起點 L55647', line(40707).startswith('/* ===== v20a176 ROM176'))",
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41076).startswith('function rom176ApplyGiftOverrides()'))":
    "ok('釘：rom176ApplyGiftOverrides 定義 L56015', line(41057).startswith('function rom176ApplyGiftOverrides()'))",
    "ok('釘：addLocTalkGiftActs L57154', line(42379).startswith('function addLocTalkGiftActs(add, L, npcId)'))":
    "ok('釘：addLocTalkGiftActs L57154', line(42360).startswith('function addLocTalkGiftActs(add, L, npcId)'))",
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42535))":
    "ok('釘：openLoc rom176 攔截 L57248', 'rom176TryIntercept(id)' in line(42516))",
})

# travel114：DEF／COUNT／FREE——逐行全文做 key（重疊對一次過換，唔會撞值）
t114 = {}
t114["DEF_LINE = 42494      # function openLoc(id, opts){"] = "DEF_LINE = 42475      # function openLoc(id, opts){"
count_map = {45770: 45751, 45978: 45959, 46136: 46117, 46157: 46138}
free_map = {40524: 40505, 40643: 40624, 40718: 40699, 40918: 40899,
            40962: 40943, 40968: 40949, 41035: 41016, 41037: 41018,
            41040: 41021, 41067: 41048, 42342: 42323, 42389: 42370,
            42759: 42740, 42781: 42762, 42933: 42914, 42938: 42919,
            43863: 43844, 45340: 45321, 45647: 45628, 45648: 45629,
            45692: 45673, 45693: 45674, 45718: 45699, 46607: 46588}
t114_lines = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read().splitlines()
for old_n, new_n in list(count_map.items()) + list(free_map.items()):
    old_ln = next(ln for ln in t114_lines if ln.strip().startswith(str(old_n) + ","))
    assert mapping[old_n] == new_n, "映射唔啱：%d→%s（預期 %d）" % (old_n, mapping.get(old_n), new_n)
    t114[old_ln] = old_ln.replace(str(old_n) + ",", str(new_n) + ",", 1)
assert len(t114) == 1 + len(count_map) + len(free_map)
resync("tests/test_travel114_static.py", t114)
print("resync313 完成")
