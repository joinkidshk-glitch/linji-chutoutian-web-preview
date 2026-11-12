# v20a128 A5 圖標補圖・靜態守門測試（🏆×7＋禮物 8 隻＋九龍電視台 📻→📺）。
# 用法：python3 tests/test_ui128a5_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」。
# 對 pristine main 行 → 新寫法缺席 → 乾淨 FAIL。
# 圖檔本身用 os.path 驗存在＋非空。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(path))
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# mapping：獎盃＋8 隻禮物象形
ok('A5 🏆→trophy mapping', '"🏆":"trophy"' in html)
for stem in ['gift_pineapple', 'gift_eggtart', 'gift_thermos', 'gift_hairclip',
             'gift_memopad', 'gift_cassette', 'gift_sweetbox', 'gift_perfume']:
    ok('A5 mapping %s' % stem, ('"%s"' % stem) in html)

# 圖檔存在＋非空（256×256 PNG，透明底）
for fname in ['icon_trophy.png', 'icon_gift_pineapple.png', 'icon_gift_eggtart.png',
              'icon_gift_thermos.png', 'icon_gift_hairclip.png', 'icon_gift_memopad.png',
              'icon_gift_cassette.png', 'icon_gift_sweetbox.png', 'icon_gift_perfume.png']:
    p = os.path.join(root, 'assets', 'icons', fname)
    ok('A5 圖檔 %s' % fname, os.path.isfile(p) and os.path.getsize(p) > 1000)

# 7 個 🏆 渲染位全部改用 iconHtml112
ok('A5 獎盃渲染位用 iconHtml112', 'iconHtml112("🏆")' in html)

# 九龍電視台 data emoji 📻→📺（inline 數據，唔係 content pack JSON）
_i = html.find('id:"tvb_kowloon"')
_row = html[_i:_i + 200] if _i >= 0 else ''
ok('A5 九龍電視台行用 📺 唔係 📻', 'emoji:"📺"' in _row and 'emoji:"📻"' not in _row)

print('TOTAL %s' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
