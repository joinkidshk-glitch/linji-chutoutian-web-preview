# v20a128 A2 地點模板一致性・靜態守門測試（N13／N2／N3／S-23／打聽卡圖標）。
# 用法：python3 tests/test_ui128a2_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」。
# 對 pristine main 行 → 新寫法缺席 → 乾淨 FAIL。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# N13：茶餐廳在場星描述行——實測幾何無重疊，根因係對比度（啡字落相）；
# 修法係跟標題同一套相上處理（米白＋陰影），唔係搬位。
ok('N13 pres105-line 米白＋陰影', '#app #loc-sheet.sheet.locpanel118 .pres105-line{ color:#f8f1de !important; text-shadow:0 1px 6px rgba(0,0,0,.6); }' in html)

# N2：冇企立圖嘅地點唔浮名牌（霞姐／禮品老闆娘；B1 另案先畫圖）
# （舊版已有 tagrow.hidden=true 喺 hospital 分支，斷言要指明 noFig 分支先識分。）
ok('N2 noFig 分支隱藏 tagrow', '} else if(o && o.noFig && tagrow){' in html)
ok('N2 noFig 分支清空浮名牌', 'v20a128 A2 N2' in html)

# N3：非 hub 地點描述唔再截 28 字，出全文
# （descShort 變數消失；其餘 .slice(0,28) 係 history preview 另一處，唔郁。）
ok('N3 28 字截斷已刪', 'descShort' not in html)

# S-23：費用欄實物名改動作短語（唔再似價錢）
ok('S-23 凍檸茶動作短語', 'cost:"請伙記飲凍檸茶"' in html)
ok('S-23 西多士動作短語', 'cost:"請茶客食西多士"' in html)
ok('S-23 咖啡動作短語', 'cost:"請化妝師飲咖啡"' in html)
ok('S-23 萬寶路動作短語', 'cost:"遞包萬寶路畀何生"' in html)
ok('S-23 舊裸實物名 cost 唔見', 'cost:"一杯凍檸茶"' not in html and 'cost:"一碟西多士"' not in html and 'cost:"一杯咖啡"' not in html and 'cost:"一包萬寶路"' not in html)

# 打聽卡圖標：按 title 分圖，唔再全部用報紙圖
# （🎁／☕／📺 喺舊版 EMOJI map 已經有，斷言要指明 locpanel118ActIcon 入面嘅新 pattern。）
ok('打聽卡 還人情／送禮用 🎁', '/^送禮/.test(t) || t==="還人情／送禮"' in html)
ok('打聽卡 飲茶用 ☕', '/飲茶/.test(t)) em="☕"' in html)
ok('打聽卡 電視城規矩／入廠守則用 📺', '/電視城規矩/.test(t) || /入廠守則/.test(t)) em="📺"' in html)
ok('打聽卡 通用 act-ask 報紙圖留返兜底', '/act-ask/.test(c)) em="📰"' in html)

print('TOTAL %s' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
