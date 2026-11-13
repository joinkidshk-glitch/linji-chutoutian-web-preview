#!/usr/bin/env python3
# qa161/resolve_rebase161_v155.py — v20a161 第二次 rebase：v155（bf612bc）落地嗰陣 main 郁咗，
# 分支由 9346a8e 改 rebase 上 bf612bc。index.html 自動合併乾淨，淨係三份測試行號衝突（純漂移）。
# 已核實：工作版 index.html 刪走 14 行 v161 插入段 == origin/main(bf612bc):index.html 逐字相同，
# 插入段新行 4793-4806；全部釘行都喺插入點之後，一律 +14。
# 做法：difflib 對位核實每個舊釘行映射去舊+14 且內容逐字相同，先至逐行換號＋補註解。
# 注意：換號要跳過 v155 嗰行歷史註解（入面「25744→25761」係 v155 嘅舊映射，唔可以跟住變）；
# 其餘 L25761 式註解係現行行號引用，要跟住變。
# 取代 qa161/resync161_rebase.py（嗰份係第一次 rebase 上 9346a8e 嘅，硬計舊釘行，唔適用於 bf612bc）。
# 用法：python3 qa161/resolve_rebase161_v155.py（在 ~/workspace/linji-work161 執行，rebase 衝突狀態）
import difflib, io, re, subprocess, sys

new_src = open("index.html", encoding="utf-8").read()
new_lines = new_src.split("\n")
start = next(i for i, l in enumerate(new_lines) if l.startswith("/* === v20a161"))
end = next(i for i, l in enumerate(new_lines) if l.startswith("/* === v20a161 完 === */"))
assert end - start + 1 == 14, "insert block must be exactly 14 lines"
print("insert block new lines %d-%d (14 lines)" % (start + 1, end + 1))
prev_lines = new_lines[:start] + new_lines[end + 1:]
head_src = subprocess.check_output(["git", "show", "origin/main:index.html"], text=True)
assert "\n".join(prev_lines) == head_src, "reconstructed prev differs from origin/main"
print("prev == origin/main(bf612bc):index.html: True")

sm = difflib.SequenceMatcher(a=prev_lines, b=new_lines, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1
    else:
        print("CHANGE %s prev %d-%d -> new %d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))
        assert tag == "insert" and i1 == start and j2 - j1 == 14, "unexpected change outside insert block"

fail = 0
def check(label, old_ln):
    global fail
    nl = mapping.get(old_ln)
    ok = nl == old_ln + 14 and prev_lines[old_ln - 1] == new_lines[nl - 1]
    if not ok:
        fail += 1
    print("%s %d -> %s %s" % (label, old_ln, nl, "OK" if ok else "MISMATCH"))

# ---- travel114：由檔讀釘行 ----
t114_path = "tests/test_travel114_static.py"
t114 = io.open(t114_path, encoding="utf-8").read()
def parse_set(name):
    m = re.search(name + r"\s*=\s*\{([^}]*)\}", t114, re.S)
    # 先剝走 # 註解再抽數字，唔係 "ux68GoLoc"／"wf4Fire" 呢啲註解字會誤抽 68／72／4
    body = "\n".join(ln.split("#", 1)[0] for ln in m.group(1).split("\n"))
    return sorted(int(x) for x in re.findall(r"\d+", body))
count_pins = parse_set("COUNT_LINES")
free_pins = parse_set("FREE_LINES")
def_pin = int(re.search(r"DEF_LINE = (\d+)", t114).group(1))
wrap_pin = int(re.search(r"WRAPPER_LINE = (\d+)", t114).group(1))
for ln in count_pins:
    check("COUNT", ln)
for ln in free_pins:
    check("FREE", ln)
check("DEF", def_pin)
check("WRAP", wrap_pin)

# ---- text125：三組釘行（含 ls[] 索引 = 行號-1）----
text125_pins = [27832, 27831, 27945, 27944, 33567, 33569, 33566]
for ln in text125_pins:
    check("TEXT125", ln)

# ---- kwan151：13 個釘行＋內容錨點（條件沿用 resolve_kwan151_rebase.py）----
idx = new_lines
def line(n):
    return idx[n - 1]
kwan_checks = [
    (25761, lambda s: "關海媚" not in s and "/Ho\\s*哥|陳淑芬|施南生/" in s),
    (26098, lambda s: "關海媚" not in s and '["陳淑芬","施南生","Ho哥"]' in s),
    (26146, lambda s: '["陳淑芬","施南生","Ho哥","Ho 哥","nextHint"]' in s),
    (26366, lambda s: '["陳淑芬","施南生","Ho哥","Ho 哥"]' in s),
    (26103, lambda s: "v151 退役" in s),
    (26101, lambda s: "關海媚禁令" not in s and "雙女主改讀 devAppendix" in s),
    (26102, lambda s: 'bad("dual_note")' in s),
    (31063, lambda s: '["星河電視城", "星河電視台"]' in s and '["送命題", "辣手問題"]' in s),
    (31054, lambda s: "關海媚提醒頭條係雙刃" in s),
    (27340, lambda s: 'kwan_hoimei: { artId:"char_kwan", portraitsKey:null, display:"關海媚" }' in s),
    (31105, lambda s: '["rel_mei","關海媚"]' in s),
    (31062, lambda s: "采兒同關海媚嗰邊都近咗啲" in s and "但采兒同關海媚嗰邊，都冷淡咗" in s),
    (27307, lambda s: '"關海媚":"kwan_hoimei"' in s),
]
for old, cond in kwan_checks:
    check("KWAN151", old)
    new = old + 14
    assert cond(line(new)), "kwan151 anchor %d -> %d mismatch: %r" % (old, new, line(new)[:100])
    print("kwan151 anchor %d -> %d OK" % (old, new))

if fail:
    print("RESULT FAIL (%d)" % fail)
    sys.exit(1)
print("all anchors verified: every pin maps to old+14 with identical content")

# ---- 套用換號（逐行；skip_pred 行唔郁，通常係 v155 歷史註解）----
# 單次 regex pass：同一行內舊號一次過映射，唔會出現 30885→30899 再被當成 30899→30913 嘅連鎖誤換。
def replace_numbers(path, pairs, skip_pred=None):
    mapping = {old: new for old, new in pairs}
    pat = re.compile(r"\d+")
    lines = io.open(path, encoding="utf-8").read().split("\n")
    counts = {}
    for i, ln in enumerate(lines):
        if skip_pred and skip_pred(ln):
            continue
        def sub(m):
            v = int(m.group(0))
            if v in mapping:
                counts[v] = counts.get(v, 0) + 1
                return str(mapping[v])
            return m.group(0)
        lines[i] = pat.sub(sub, ln)
    for old, new in pairs:
        assert counts.get(old, 0) >= 1, "%s: pin %d not found" % (path, old)
        print("%s: %d -> %d (%d occurrences)" % (path, old, new, counts[old]))
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))

def is_v155_hist(ln):
    return "v20a155 rebase 上 main 9346a8e" in ln

replace_numbers(t114_path, [(ln, ln + 14) for ln in count_pins + free_pins + [def_pin, wrap_pin]], skip_pred=is_v155_hist)
t114_txt = io.open(t114_path, encoding="utf-8").read()
t114_note = "# v20a155 rebase 上 main 9346a8e"
assert t114_note in t114_txt
t114_txt = t114_txt.replace(t114_note,
    "# v20a161 rebase 上 bf612bc（v155 先落地）resync：START161 淨 +14 行（插入段新行 4793-4806），\n# 行號 ≥4793 者 +14；本檔釘行全部喺插入點之後，一律 +14（difflib 對位＋逐行錨點核實，見 qa161/resolve_rebase161_v155.py）。\n" + t114_note, 1)
io.open(t114_path, "w", encoding="utf-8").write(t114_txt)

t125_path = "tests/test_text125_static.py"
replace_numbers(t125_path, [(ln, ln + 14) for ln in text125_pins])
t125_txt = io.open(t125_path, encoding="utf-8").read()
n = t125_txt.count("v155 rebase ＋17，同 currentLine）")
assert n == 2, "expected 2 v155 notes (advance/applyFamily), got %d" % n
t125_txt = t125_txt.replace("v155 rebase ＋17，同 currentLine）", "v155 rebase ＋17，同 currentLine；v161 rebase 上 bf612bc ＋14）")
assert "v155 rebase ＋17：B1 註解 ＋6／B2 註解 ＋7／B3 ＋4）" in t125_txt
t125_txt = t125_txt.replace("v155 rebase ＋17：B1 註解 ＋6／B2 註解 ＋7／B3 ＋4）",
                            "v155 rebase ＋17：B1 註解 ＋6／B2 註解 ＋7／B3 ＋4；v161 rebase 上 bf612bc ＋14）", 1)
io.open(t125_path, "w", encoding="utf-8").write(t125_txt)
print("text125 notes updated")

kwan_path = "tests/test_kwan151_static.py"
replace_numbers(kwan_path, [(old, old + 14) for old, _ in kwan_checks], skip_pred=is_v155_hist)
kwan_txt = io.open(kwan_path, encoding="utf-8").read()
anchor = "#   v20a155 rebase 上 main 9346a8e resync：v155 淨 ＋17（B1 註解 ＋6／B2 註解 ＋7／B3 ＋4），全部錨點再 ＋17"
assert anchor in kwan_txt
kwan_txt = kwan_txt.replace(anchor, anchor +
    "；v20a161 rebase 上 bf612bc ＋14（插入段新行 4793-4806，全部錨點再 ＋14，見 qa161/resolve_rebase161_v155.py）。", 1)
io.open(kwan_path, "w", encoding="utf-8").write(kwan_txt)
print("kwan151 note updated")
print("RESULT PASS")
