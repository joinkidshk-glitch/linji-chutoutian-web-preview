"""v20a158 resync：index.html 行號漂移重對（test_travel114_static.py 釘行）。
插入點（相對 HEAD 947cf56；淨 +165 行）：
  gigCardHtml favor158 提示＋4 行（舊 L17912 附近）；
  openCastingNoticeDetail 渠道掣＋11 行（舊 L18895 附近）；
  GRANT229_ENC79 加 8 行＋註解 7 行＝＋15（舊 L27001 附近）；
  aud91CreatePending revealDay 覆寫＋2 行、favorLabel＋1 行＝＋3（舊 L43907 附近）；
  aud91PendingHint favor158 分支＋2 行（舊 L43943 附近）；
  aud91PresentOne favor158 分支＋1 行（notes 行 1→2；何生嗰行原地改，行數不變；舊 L44095／L44125 附近）；
  v20a158 渠道 block＋129 行（舊 L44214 doAudition 之前）。
方法：difflib 全文對位映射舊釘行→新行號，逐行核實內容逐字相同（純漂移）；
openLoc( 呼叫點總數不變（無增減 openLoc 行）。用法：python3 qa158/resync158.py [--apply]
"""
import difflib, re, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work158r"
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
TEST_PATH = ROOT + "/tests/test_travel114_static.py"
TEST = open(TEST_PATH, encoding="utf-8").read()

sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based
    elif tag in ("replace", "delete", "insert"):
        pass
print("mapped equal lines:", len(mapping), "of old", len(OLD))

def parse_set(name):
    # 區塊尾係獨行 }（註解入面有 {travelFree}，唔可以用 [^}]* 停）
    lines = TEST.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith(name + " = {"))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "}")
    nums = []
    for line in lines[start + 1:end]:
        code = line.split("#", 1)[0]
        nums.extend(int(x) for x in re.findall(r"\d+", code))
    return nums, start, end

problems = []
def remap(old_no):
    if old_no not in mapping:
        problems.append(f"line {old_no} not in equal mapping: {OLD[old_no-1].strip()[:80]!r}")
        return None
    new_no = mapping[old_no]
    if OLD[old_no-1].strip() != NEW[new_no-1].strip():
        problems.append(f"line {old_no}->{new_no} content differs")
        return None
    return new_no

for name in ("COUNT_LINES", "FREE_LINES"):
    nums, _, _ = parse_set(name)
    print(name, "old:", sorted(nums))
    new_nums = [remap(n) for n in nums]
    print(name, "new:", sorted(x for x in new_nums if x))
for name in ("DEF_LINE", "WRAPPER_LINE"):
    old_no = int(re.search(name + r" = (\d+)", TEST).group(1))
    print(name, old_no, "->", remap(old_no))

old_hits = [l.strip() for l in OLD if "openLoc(" in l]
new_hits = [l.strip() for l in NEW if "openLoc(" in l]
print("openLoc( lines old/new:", len(old_hits), len(new_hits), "identical seq:", old_hits == new_hits)
if old_hits != new_hits:
    problems.append("openLoc( sequence differs")

if problems:
    print("PROBLEMS:"); [print(" -", p) for p in problems]
    sys.exit(1)

if "--apply" in sys.argv:
    out = TEST
    out_lines = out.split("\n")
    for name in ("COUNT_LINES", "FREE_LINES"):
        nums, start, end = parse_set(name)  # 舊 TEST 嘅行號（未改前）
        # 以 out_lines 當前狀態重搵區塊（前一個 set 改完行數不變，行號唔郁）
        start = next(i for i, l in enumerate(out_lines) if l.startswith(name + " = {"))
        end = next(i for i in range(start + 1, len(out_lines)) if out_lines[i].strip() == "}")
        for li in range(start + 1, end):
            code = out_lines[li].split("#", 1)[0]
            comment = out_lines[li][len(code):]
            def repl_num(mm):
                return str(mapping[int(mm.group(0))])
            out_lines[li] = re.sub(r"\d+", repl_num, code) + comment
    out = "\n".join(out_lines)
    for name in ("DEF_LINE", "WRAPPER_LINE"):
        old_no = int(re.search(name + r" = (\d+)", out).group(1))
        out = re.sub(name + r" = \d+", name + " = " + str(mapping[old_no]), out, count=1)
    header = "# v20a158 resync：index.html 淨 +177 行（gigCardHtml 提示＋4／詳情頁渠道掣＋11／GRANT229_ENC79 8 行＋註解 8／aud91CreatePending＋3／aud91PendingHint＋2／aud91PresentOne＋2／v20a158 渠道 block＋約 130；見 qa158/resync158.py difflib 對位核實內容逐字相同，純漂移；openLoc( 呼叫點總數不變）。\n"
    out = out.replace("# v20a243 resync：", header + "# v20a243 resync：", 1)
    open(TEST_PATH, "w", encoding="utf-8").write(out)
    print("APPLIED:", TEST_PATH)
else:
    print("dry run only; pass --apply to rewrite")
