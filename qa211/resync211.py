# -*- coding: utf-8 -*-
"""v20a211 resync：B1 雙幾何（矮 viewport 480×432／高 viewport 480×540，HS211/HSC211）
令舊測試嘅硬編碼幾何斷言失效——按 v207 B2 resync 前例，更新斷言到新形式，意圖不變：
短 viewport 基準值不變（FLOOR 314／dispH 136/140／glyph -129/-61／光池 120／彩紙 436），
高 viewport 全部 ×HSC211（＝HS211/432＝1.25）。純算術斷言（牌底 179.3／地板深 98px 比率）
描述短幾何，唔郁。逐檔核實替換次數；邏輯檔（.js）同理。"""
import sys

# (old, new, {file: expected_count})
RULES = [
    ("'const FLOOR = 314'",
     "'const FLOOR = Math.round(314 * HSC211)'",
     {"tests/test_awards170_static.py": 1, "tests/test_awards174_static.py": 1,
      "tests/test_awards177_static.py": 2, "tests/test_awards181_static.py": 2,
      "tests/test_awards187_static.py": 1, "tests/test_awards190_static.py": 1,
      "tests/test_awards207_static.py": 1}),
    ("'const W = 480, H = 432'",
     "'const W = 480, H = HS211'",
     {"tests/test_awards170_static.py": 1, "tests/test_awards174_static.py": 2,
      "tests/test_awards177_static.py": 2, "tests/test_awards181_static.py": 2,
      "tests/test_awards207_static.py": 1}),
    ("'<canvas class=\"awd62-canvas\" width=\"720\" height=\"648\">'",
     "'Math.round(HS211 * 1.5)'",
     {"tests/test_awards160_m1_static.py": 1, "tests/test_awards174_static.py": 2,
      "tests/test_awards177_static.py": 1, "tests/test_awards181_static.py": 1,
      "tests/test_awards207_static.py": 1}),
    ("'? 140 : 136'",
     "'Math.round(140 * HSC211)'",
     {"tests/test_awards170_static.py": 1, "tests/test_awards174_static.py": 1,
      "tests/test_awards177_static.py": 1, "tests/test_awards181_static.py": 1,
      "tests/test_awards207_static.py": 1}),
    ("'dispH: 136'",
     "'dispH: Math.round(136 * HSC211)'",
     {"tests/test_awards170_static.py": 1, "tests/test_awards174_static.py": 1,
      "tests/test_awards177_static.py": 1, "tests/test_awards207_static.py": 1}),
    ("play_fn.count('dispH: 136')",
     "play_fn.count('dispH: Math.round(136 * HSC211)')",
     {"tests/test_awards181_static.py": 1}),
    ("'FLOOR + fp.y - 129'",
     "'FLOOR + fp.y - Math.round(129 * HSC211)'",
     {"tests/test_awards170_static.py": 1, "tests/test_awards174_static.py": 1,
      "tests/test_awards177_static.py": 1, "tests/test_awards181_static.py": 1,
      "tests/test_awards187_static.py": 1, "tests/test_awards190_static.py": 1,
      "tests/test_awards207_static.py": 1}),
    ("'FLOOR - 129'",
     "'FLOOR - Math.round(129 * HSC211)'",
     {"tests/test_awards187_static.py": 1, "tests/test_awards190_static.py": 1,
      "tests/test_awards207_static.py": 1}),
    ("'FLOOR + fp.y - 61'",
     "'FLOOR + fp.y - Math.round(61 * HSC211)'",
     {"tests/test_awards170_static.py": 1, "tests/test_awards174_static.py": 1,
      "tests/test_awards177_static.py": 1, "tests/test_awards181_static.py": 1,
      "tests/test_awards187_static.py": 1, "tests/test_awards207_static.py": 1}),
    ("'F - 120'",
     "'F - Math.round(120 * HSC211)'",
     {"tests/test_awards170_static.py": 1, "tests/test_awards174_static.py": 1,
      "tests/test_awards177_static.py": 1, "tests/test_awards207_static.py": 1}),
    ("'p.y > 436'",
     "'p.y > HS211 + 4'",
     {"tests/test_awards174_static.py": 1, "tests/test_awards177_static.py": 1,
      "tests/test_awards207_static.py": 1}),
    # .js 檔：includes(...) 形式
    ("playSrc.includes('const FLOOR = 314')",
     "playSrc.includes('const FLOOR = Math.round(314 * HSC211)')",
     {"tests/test_awards187_logic.js": 1, "tests/test_awards190_logic.js": 1}),
    ("playSrc.includes('FLOOR + fp.y - 129')",
     "playSrc.includes('FLOOR + fp.y - Math.round(129 * HSC211)')",
     {"tests/test_awards187_logic.js": 1, "tests/test_awards190_logic.js": 1}),
    ("playSrc.includes('FLOOR - 129')",
     "playSrc.includes('FLOOR - Math.round(129 * HSC211)')",
     {"tests/test_awards187_logic.js": 1, "tests/test_awards190_logic.js": 1}),
    ("playSrc.includes('FLOOR + fp.y - 61')",
     "playSrc.includes('FLOOR + fp.y - Math.round(61 * HSC211)')",
     {"tests/test_awards187_logic.js": 1}),
]

HEADER_NOTE = "# v20a211 B1 resync：雙幾何（矮 480×432／高 480×540，HS211／HSC211＝×1.25）——短基準值不變，高 viewport 按比例換算；見 NOTES_V20A211。\n"

for old, new, counts in RULES:
    for f, want in counts.items():
        s = open(f, encoding="utf-8").read()
        got = s.count(old)
        if got == 0 and new in s:
            print(f"skip (already) {f}: {old[:44]!r}")
            continue
        assert got == want, f"{f}: {old!r} expected {want}, found {got}"
        open(f, "w", encoding="utf-8").write(s.replace(old, new))
        print(f"ok {f}: {old[:44]!r} x{want}")

# 181 檔 '? 140 : 136' 替換後，chk 內仲要補 136 嗰半（原式只驗玩家 140，fellow 136 由 'dispH: 136' 嗰行驗——
# 181 檔 dispH 嗰行係 count 形式，已換；但 L172 chk 本身 '? 140 : 136' 只得一半——補埋 fellow 半邊）
f = "tests/test_awards181_static.py"
s = open(f, encoding="utf-8").read()
old = "chk('人物 dispH 136（fellow）／140（玩家；v20a207 B2）', 'Math.round(140 * HSC211)' in play_fn)"
assert s.count(old) == 1
s = s.replace(old, "chk('人物 dispH 136（fellow）／140（玩家；v20a207 B2；v20a211 B1 resync：按 HSC211 換算）', 'Math.round(140 * HSC211)' in play_fn and 'Math.round(136 * HSC211)' in play_fn)")
open(f, "w", encoding="utf-8").write(s)
print("ok 181 fellow half")

# 170／174／177／207 檔 '? 140 : 136' 嗰行同理：原式 '? 140 : 136' in play_fn 其實一次過驗兩邊；
# 換咗做 'Math.round(140 * HSC211)' 之後，fellow 136 嗰邊要補——嗰幾檔同一 chk 入面仲有 'dispH: 136' 已換做 scaled，
# 所以 fellow 136 已經由 dispH 嗰半驗緊，唔使再補。核實：
for f in ["tests/test_awards170_static.py", "tests/test_awards174_static.py",
          "tests/test_awards177_static.py", "tests/test_awards207_static.py"]:
    s = open(f, encoding="utf-8").read()
    assert "Math.round(136 * HSC211)" in s, f
    print("ok fellow covered:", f)

# 檔頭加 resync 註
for f in ["tests/test_awards160_m1_static.py", "tests/test_awards170_static.py",
          "tests/test_awards174_static.py", "tests/test_awards177_static.py",
          "tests/test_awards181_static.py", "tests/test_awards187_static.py",
          "tests/test_awards190_static.py", "tests/test_awards207_static.py",
          "tests/test_awards187_logic.js", "tests/test_awards190_logic.js"]:
    s = open(f, encoding="utf-8").read()
    if "v20a211 B1 resync" not in s:
        open(f, "w", encoding="utf-8").write(HEADER_NOTE + s)
        print("header:", f)
print("RESYNC DONE")
