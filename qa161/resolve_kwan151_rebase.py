#!/usr/bin/env python3
# qa161/resolve_kwan151_rebase.py — v20a161 rebase 上 9346a8e 之後，
# test_kwan151_static.py 嘅 13 個釘行全部要 +14（v161 喺舊行 4771 之後淨插入 14 行 CSS，
# 全部釘行都喺插入點之後）。test_handbook156 唔寫死行號、kwan151_textfix.js 冇釘行，唔使郁。
# 做法：先逐行核實新行號喺新 index.html 嘅內容啱（用 test 本身嘅條件），再全局換號＋補註解。
# 用法：python3 qa161/resolve_kwan151_rebase.py（在 ~/workspace/linji-work161 執行）
import io

idx = io.open("index.html", encoding="utf-8").read().split("\n")
def line(n):
    return idx[n - 1]

# (舊釘行, 新釘行, 預期內容檢查)
checks = [
    (25744, 25758, lambda s: "關海媚" not in s and "/Ho\\s*哥|陳淑芬|施南生/" in s),
    (26081, 26095, lambda s: "關海媚" not in s and '["陳淑芬","施南生","Ho哥"]' in s),
    (26129, 26143, lambda s: '["陳淑芬","施南生","Ho哥","Ho 哥","nextHint"]' in s),
    (26349, 26363, lambda s: '["陳淑芬","施南生","Ho哥","Ho 哥"]' in s),
    (26086, 26100, lambda s: "v151 退役" in s),
    (26084, 26098, lambda s: "關海媚禁令" not in s and "雙女主改讀 devAppendix" in s),
    (26085, 26099, lambda s: 'bad("dual_note")' in s),
    (31046, 31060, lambda s: '["星河電視城", "星河電視台"]' in s and '["送命題", "辣手問題"]' in s),
    (31037, 31051, lambda s: "關海媚提醒頭條係雙刃" in s),
    (27323, 27337, lambda s: 'kwan_hoimei: { artId:"char_kwan", portraitsKey:null, display:"關海媚" }' in s),
    (31088, 31102, lambda s: '["rel_mei","關海媚"]' in s),
    (31045, 31059, lambda s: "采兒同關海媚嗰邊都近咗啲" in s and "但采兒同關海媚嗰邊，都冷淡咗" in s),
    (27290, 27304, lambda s: '"關海媚":"kwan_hoimei"' in s),
]
for old, new, cond in checks:
    assert cond(line(new)), "anchor %d -> %d mismatch: %r" % (old, new, line(new)[:100])
    print("anchor %d -> %d OK" % (old, new))

path = "tests/test_kwan151_static.py"
txt = io.open(path, encoding="utf-8").read()
for old, new, _ in checks:
    assert txt.count(str(old)) >= 1, "pin %d not found" % old
    txt = txt.replace(str(old), str(new))
# 註解補 v161 resync 記錄
anchor = "# v151 落地 resync：v156（9c850f9）先落地，main 行號 +15（L733 插入 15 行），錨點由 e08a070 版 +15。\n"
assert anchor in txt
txt = txt.replace(anchor, anchor +
    "# v161 rebase resync：rebase 上 9346a8e，START161 淨 +14 行（舊行 4771 之後插入），全部錨點再 +14（逐行錨點核實，見 qa161/resolve_kwan151_rebase.py）。\n")
io.open(path, "w", encoding="utf-8").write(txt)
print("kwan151 resolved: 13 pins +14")
