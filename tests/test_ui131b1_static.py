# v20a131 B1 地點負責人企立圖（霞姐／禮品老闆娘）・靜態守門測試。
# 用法：python3 tests/test_ui131b1_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」。
# 對 pristine main 行 → 新圖路徑缺席＋noFig 仍在 → 乾淨 FAIL。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(path))
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# B1：locpanel118OwnerFor 回企立圖，唔再 noFig
ok('B1 霞姐企立圖路徑', 'assets/story/fullbody/xia_jie_base.webp?v=20a131' in html)
ok('B1 禮品老闆娘企立圖路徑', 'assets/story/fullbody/gift_lady_base.webp?v=20a131' in html)
ok('B1 霞姐唔再 noFig', '{ name:"霞姐", sub:"金龍茶餐廳老闆娘", noFig:true }' not in html)
ok('B1 禮品老闆娘唔再 noFig', '{ name:"老闆娘", sub:"廟街禮品檔", noFig:true }' not in html)
ok('B1 noFig 分支留返做後備', '} else if(o && o.noFig && tagrow){' in html)

# B1：實體檔存在、透明底、尺寸合理（全身企立，闊高比 0.25–0.45）
try:
    from PIL import Image
    for stem, lo, hi in [('xia_jie_base', 0.25, 0.45), ('gift_lady_base', 0.25, 0.45)]:
        p = os.path.join(root, 'assets', 'story', 'fullbody', stem + '.webp')
        exists = os.path.isfile(p) and os.path.getsize(p) > 50000
        ok('B1 實體檔存在 ' + stem, exists)
        if not exists:
            continue
        im = Image.open(p)
        w, h = im.size
        ok('B1 透明底 RGBA ' + stem, im.mode == 'RGBA')
        ok('B1 闊高比全身企立 ' + stem, lo <= w / h <= hi)
except ImportError:
    print('SKIP PIL 尺寸檢查（冇 PIL）')

# B1：名牌文案不變（只加圖，唔改名）
ok('B1 霞姐名牌文案不變', 'name:"霞姐", sub:"金龍茶餐廳老闆娘"' in html)
ok('B1 禮品老闆娘名牌文案不變', 'name:"老闆娘", sub:"廟街禮品檔"' in html)
ok('B1 禮品老闆娘唔憑空起名', 'gift_lady_base' in html and '老闆娘' in html)

print('TOTAL %s' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
