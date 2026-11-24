#!/usr/bin/env python3
"""v395 resync：index.html 淨 +1 行（檔尾 <script src="minigame395.js"></script> 一行；
小遊戲本體、CSS、鉤子邏輯全部喺 minigame395.js，index.html 其餘改動全部等行數寫法）。
影響：總行數 50511→50512（tang171／tang173／gift185 行數鏈 ＋v395 +1）；
檔尾 script 由 2 個變 3 個（tail270：soft-rev head script＋主 script＋minigame395.js）。
其餘釘行一律唔郁（插入點喺檔尾，所有錨點之前）。
用法：python3 qa395/resync395.py（已跑過，冪等檢查：每處錨點必須恰好出現一次）。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTE_TOTAL = "# v395 resync：index.html 淨 +1 行（檔尾 minigame395.js script 標籤）；總行數 50511→50512，行數鏈 ＋v395 +1；其餘釘行唔郁。"
NOTE_TAIL = "# v395 resync：index.html 淨 +1 行（檔尾 minigame395.js script 標籤）；script 3 個、檔尾加 src 行；其餘唔郁。"


def patch(path, subs, note):
    p = os.path.join(ROOT, path)
    src = open(p, encoding="utf-8").read()
    if src.startswith(note):
        print(f"skip {path}（已註記）")
        return
    for old, new in subs:
        assert src.count(old) == 1, f"{path}: {old[:50]!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, note)
    open(p, "w", encoding="utf-8").write("\n".join(lines))
    print(f"patched {path}")


for path in ["tests/test_tang171_static.py", "tests/test_tang173_static.py"]:
    patch(path, [("總行數 50511（", "總行數 50512（"),
                 ("＋v394 +5）", "＋v394 +5＋v395 +1）"),
                 ("== 50511)", "== 50512)")], NOTE_TOTAL)
patch("tests/test_gift185_static.py", [("總行數 50511（", "總行數 50512（"),
      ("＋v394 +5）", "＋v394 +5＋v395 +1）"),
      ("== 50511)", "== 50512)")], NOTE_TOTAL)
patch("tests/test_tail270_static.py", [
    ("ok('two script blocks', html.count('<script') == 2)",
     "ok('three script blocks (v395: +minigame395.js src)', html.count('<script') == 3)"),
    ("ok('two </script>', html.count('</script>') == 2)",
     "ok('three </script> (v395: +minigame395.js src)', html.count('</script>') == 3)"),
    ("ok('tail ends refresh -> })(); -> </script> -> </body> -> </html>',",
     "ok('tail ends refresh -> })(); -> </script> -> minigame395.js -> </body> -> </html> (v395)',"),
    (r"re.search(r'refreshCopyPacksFromDisk\(\);\n\}\)\(\);\n\n</script>\n</body>\n</html>\n$', html)",
     r"re.search(r'refreshCopyPacksFromDisk\(\);\n\}\)\(\);\n\n</script>\n<script src=\"minigame395.js\"></script>\n</body>\n</html>\n$', html)"),
], NOTE_TAIL)
print("done")
