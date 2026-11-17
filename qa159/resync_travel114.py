"""Re-sync tests/test_travel114_static.py line allowlists after v20a159 ROM159 Phase 1.
OLD = pristine base e08a070 (~/workspace/linji-pristine159/index.html),
NEW = work159 index.html. Insertions vs base:
  - bumpRel 凍結鉤 +8 行（24796 後）
  - GiftShop 分層／覆寫呼叫淨 +29 行（30440–31594 段）
  - endingRomanceState48 flag_choi_public 讀取 +4 行（41656 後）
  - ROM159 主 block＋CMT_vera_commit（41675 後，含 Vera 節點）
  - doTalk／addLocTalkGiftActs／people72Html／openLoc＋enterHome flush 鉤（其後）
  - 3 個新 openLoc( 呼叫點（rom159ConfirmDate 約會撞期 modal，全部 travelFree:true，
    返去而家身處地點——同禮物店／送禮 modal 嗰批 FREE 理據一致）→ 歸入 FREE_LINES。
Method (same as v122/v128/v131): positional alignment of ALL openLoc( lines —
OLD 44 行必須係 NEW 47 行嘅子序列，插入嗰 3 行全部帶 travelFree:true；
其餘逐行內容逐字相同，先至係純漂移＋合法新增。
Usage: python3 qa159/resync_travel114.py [--apply]
Without --apply: print only. With --apply: rewrite the test file's sets
+ append a v20a159 resync note to the header comment.
"""
import re, sys

OLD = open("/home/hatch/workspace/linji-pristine159/index.html", encoding="utf-8").read().split("\n")
NEW = open("/home/hatch/workspace/linji-work159/index.html", encoding="utf-8").read().split("\n")
TEST_PATH = "/home/hatch/workspace/linji-work159/tests/test_travel114_static.py"
TEST = open(TEST_PATH, encoding="utf-8").read()

def parse_set(name):
    m = re.search(name + r" = \{([^}]*)\}", TEST, re.S)
    nums, comments = [], {}
    for line in m.group(1).split("\n"):
        code = line.split("#", 1)[0]
        found = [int(x) for x in re.findall(r"\d+", code)]
        if not found:
            continue
        nums.extend(found)
        if "#" in line:
            comments[found[-1]] = line.split("#", 1)[1].strip()
    return nums, comments

count_nums, count_c = parse_set("COUNT_LINES")
free_nums, free_c = parse_set("FREE_LINES")
def_line_old = int(re.search(r"DEF_LINE = (\d+)", TEST).group(1))
wrap_line_old = int(re.search(r"WRAPPER_LINE = (\d+)", TEST).group(1))

old_hits = [(i + 1, l.strip()) for i, l in enumerate(OLD) if "openLoc(" in l]
new_hits = [(i + 1, l.strip()) for i, l in enumerate(NEW) if "openLoc(" in l]
print("old openLoc( lines:", len(old_hits), " new:", len(new_hits))
assert len(old_hits) == 44, "expected 44 old call sites"
assert len(new_hits) == 47, "expected 47 new call sites"

# 序列對位：OLD 必須係 NEW 嘅子序列；插入行全部帶 travelFree:true
pos = {}
inserted = []
oi = 0
for (nl, ns) in new_hits:
    if oi < len(old_hits) and ns == old_hits[oi][1]:
        pos[old_hits[oi][0]] = nl
        oi += 1
    else:
        inserted.append((nl, ns))
assert oi == len(old_hits), "OLD sequence is not a subsequence of NEW — not a pure shift"
print("inserted lines:", [n for n, _ in inserted])
assert len(inserted) == 3, "expected exactly 3 inserted call sites"
for nl, ns in inserted:
    assert "travelFree:true" in ns, "inserted line %d lacks travelFree:true: %s" % (nl, ns)
    assert OLD[nl - 1].strip() != ns  # sanity: truly new, not a moved old line
print("insertions all travelFree:true — legit FREE additions")
for n in count_nums + free_nums:
    assert OLD[n - 1].strip() == NEW[pos[n] - 1].strip(), "content mismatch at old %d" % n
print("content verified identical for all %d listed lines" % (len(count_nums) + len(free_nums)))

def show(name, nums, comments, extra=None):
    print("\n%s = {" % name)
    all_nums = sorted(nums + ([n for n, _ in extra] if extra else []))
    for n in all_nums:
        nn = pos[n] if n in pos else n
        c = comments.get(n, "") or (dict(extra or {}).get(n, ""))
        print("    %d,%s" % (nn, ("  # " + c) if c else ""))
    print("}")

NEW_FREE_EXTRA = [(nl, "約會撞期 modal（rom159ConfirmDate），返去而家身處地點") for nl, _ in inserted]
show("COUNT_LINES", count_nums, count_c)
show("FREE_LINES", free_nums, free_c, extra=NEW_FREE_EXTRA)
print("\nDEF_LINE =", pos[def_line_old], " #", OLD[def_line_old - 1].strip()[:60])
print("WRAPPER_LINE =", pos[wrap_line_old], " #", OLD[wrap_line_old - 1].strip()[:60])
d = [i + 1 for i, l in enumerate(NEW) if "function openLoc(id, opts){" in l]
w = [i + 1 for i, l in enumerate(NEW) if "openLoc: function(id, opts){ openLoc(id, opts); }" in l]
print("direct-search DEF_LINE:", d, " WRAPPER_LINE:", w)
assert d == [pos[def_line_old]] and w == [pos[wrap_line_old]]
print("counts: free %d count %d" % (len(free_nums) + 3, len(count_nums)))

if "--apply" in sys.argv:
    out = TEST
    out = re.sub(r"COUNT_LINES = \{[^}]*\}",
                 "COUNT_LINES = {\n" + "\n".join("    %d,%s" % (pos[n], ("  # " + count_c[n]) if n in count_c else "") for n in sorted(count_nums)) + "\n}",
                 out, count=1, flags=re.S)
    free_all = sorted([(pos[n], count_c.get(n, "")) for n in free_nums] + [(nl, c) for nl, c in NEW_FREE_EXTRA])
    out = re.sub(r"FREE_LINES = \{[^}]*\}",
                 "FREE_LINES = {\n" + "\n".join("    %d,%s" % (nn, ("  # " + c) if c else "") for nn, c in free_all) + "\n}",
                 out, count=1, flags=re.S)
    out = re.sub(r"DEF_LINE = \d+", "DEF_LINE = %d" % pos[def_line_old], out, count=1)
    out = re.sub(r"WRAPPER_LINE = \d+", "WRAPPER_LINE = %d" % pos[wrap_line_old], out, count=1)
    note = ("# v20a159 resync：ROM159 Phase 1（bumpRel ＋8／GiftShop 淨 ＋29／endingRomanceState48 ＋4／"
            "ROM159 block＋CMT_vera／對話＋手帳＋flush 鉤）；qa159/resync_travel114.py 核實："
            "44 個舊 openLoc( 呼叫點逐字對位純漂移，另加 3 個新呼叫點（rom159ConfirmDate 約會撞期 modal，"
            "全部 travelFree:true，返去而家身處地點）歸入 FREE；COUNT 13 不變，FREE 27→30，"
            "DEF %d、WRAPPER %d。\n" % (pos[def_line_old], pos[wrap_line_old]))
    anchor = "# 計清單（玩家主動導航，預設計數，唔加旗）：13 處"
    assert anchor in out
    out = out.replace(anchor, note + anchor, 1)
    open(TEST_PATH, "w", encoding="utf-8").write(out)
    print("\nAPPLIED: test_travel114_static.py resynced")
