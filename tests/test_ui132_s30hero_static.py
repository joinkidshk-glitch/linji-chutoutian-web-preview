# v20a132 S-30 詳情卡英雄區高度還原・靜態守門測試。
# 用法：python3 tests/test_ui132_s30hero_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」。
# 對 pristine main 行 → height:auto 仍在 → 乾淨 FAIL。
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

m = re.search(r'#mask\.casting-sheet-on #modal-inner \.cn-issuer30v2\{([^}]*)\}', html)
ok('S30 英雄區規則存在', m is not None)
rule = m.group(1) if m else ''
ok('S30 英雄區高度 240px（還原 v116 胸口以上 crop）', 'height:240px' in rule)
ok('S30 英雄區唔再 height:auto（v128 回歸寫法）', 'height:auto' not in rule)
ok('S30 英雄區 overflow:hidden 保留（由底裁走）', 'overflow:hidden' in rule)
ok('S30 英雄區負 margin -100px 保留（卡疊上嚟）', 'margin-bottom:-100px' in rule)
ok('S30 名牌 bottom:106px 唔郁（為 240px 高設計）', '.cn-issuer-cap30v2{ position:absolute; left:12px; bottom:106px;' in html)
ok('S30 英雄圖闊 60%／上限 230px 唔郁', 'width:60%; max-width:230px' in html)

print('TOTAL ' + ('PASS' if not fails else 'FAIL %d' % len(fails)))
sys.exit(1 if fails else 0)
