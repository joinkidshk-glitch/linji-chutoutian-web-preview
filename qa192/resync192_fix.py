# -*- coding: utf-8 -*-
"""v20a192 resync 執行：按 qa192/resync192_verify.py 核實結果改 5 檔舊測試行號。
只改數字參數本身（斷言字面／dict 數字／line() 參數），label／歷史註解一律唔郁。
shift 規則：插入點（L45296–46530）之前 +0，之後 +32；WRAPPER 44387 同 tang173 CSS
L4887（1-based 4887，0-based lines[4886]）喺插入點前，唔郁。
用法：python3 qa192/resync192_fix.py
"""
import re

def sub(path, old, new, count=1):
    s = open(path, encoding='utf-8').read()
    n = s.count(old)
    assert n == count, f"{path}: {old!r} 出現 {n} 次，預期 {count} 次"
    open(path, 'w', encoding='utf-8').write(s.replace(old, new))
    print(f"  {path}: {old.strip()[:60]!r} -> {new.strip()[:60]!r}")

# ---- travel114：COUNT／FREE dict 內 >46530 者 +32；DEF +32；WRAPPER 唔郁 ----
p = 'tests/test_travel114_static.py'
s = open(p, encoding='utf-8').read()
def bump_block(src, block_re):
    m = re.search(block_re, src, re.S)
    blk = m.group(1)
    new_blk, n = re.subn(r"^(\s*)(\d+),",
                         lambda mm: mm.group(1) + str(int(mm.group(2)) + 32) + ","
                         if int(mm.group(2)) > 46530 else mm.group(0),
                         blk, flags=re.M)
    return src[:m.start(1)] + new_blk + src[m.end(1):], n
s, n1 = bump_block(s, r"COUNT_LINES = \{([^}]*)\}")
s, n2 = bump_block(s, r"FREE_LINES = \{([^}]*)\}")
open(p, 'w', encoding='utf-8').write(s)
print(f"  {p}: COUNT/FREE dicts 已掃（插入點後者 +32）")
sub(p, "DEF_LINE = 54939", "DEF_LINE = 54971")
s = open(p, encoding='utf-8').read()
assert "WRAPPER_LINE = 44387" in s, "travel114 WRAPPER 唔應該郁"
print("  travel114 WRAPPER 44387 保持不變（插入點前）")

# ---- rom176：4 個 line() 參數 +32 ----
p = 'tests/test_rom176_static.py'
for old, new in [("line(53369)", "line(53401)"), ("line(53737)", "line(53769)"),
                 ("line(54876)", "line(54908)"), ("line(54970)", "line(55002)")]:
    sub(p, old, new)

# ---- tang171／tang173：總行數＋DEF 行 +32；tang173 CSS lines[4886] 唔郁 ----
for p in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    sub(p, "src.count('\\n') == 60443", "src.count('\\n') == 60475")
    sub(p, "len(lines) >= 54940 and 'function openLoc(id, opts){' in lines[54938])",
        "len(lines) >= 54972 and 'function openLoc(id, opts){' in lines[54970])")
    s = open(p, encoding='utf-8').read()
    if 'tang173' in p:
        assert "lines[4886]" in s, "tang173 CSS lines[4886] 唔應該郁"
        print("  tang173 CSS lines[4886] 保持不變（插入點前）")

# ---- gift185：總行數 +32 ----
sub('tests/test_gift185_static.py', "html.count('\\n') == 60443", "html.count('\\n') == 60475")

print("resync192_fix 完成")
