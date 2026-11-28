# v422 七系統加強・靜態測試：查 req 保證／引薦槽／進度歸因／負標籤後果。
import sys
path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)
def seg(start, end):
    i = html.index(start)
    j = html.index(end, i) if end else len(html)
    return html[i:j]

ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('v422 模組標記', 'v422 七系統加強' in html)
ok('可試鏡判定 helper', 'function v422Auditionable(g)' in html and 'canAudition(g).ok' in html)

ip = seg('function intel381PickGig(){', 'function intel381Buy(def){')
ok('情報站查 req', 'v422Auditionable(g)' in ip)
ok('情報站擴低級別', 'ti>=0&&ti<=hi' in ip)
ok('情報站無空缺不收費文案', '現時未有符合你現時條件的補位空缺，情報費不收' in html)
ok('茶餐廳開閘線索', '陸柏言好感達 25 後' in html)

tp = seg('function tape383PickGig(type){', 'function tape383FmtDay')
ok('試鏡帶查 req', 'v422Auditionable(g)' in tp)
ok('試鏡帶付款前列明通告', '可試鏡：《' in html and '暫無符合條件通告（不收費）' in html)
ok('試鏡帶確認列明截止', '已按你現時條件核對，可前往試鏡' in html)

ok('引薦槽三格', 'REF422_LABELS' in html and '何生引薦' in html and '幕後引薦' in html and '彭少祺引薦' in html)
ok('引薦舊檔兼容', 'o.ref422' in html)
ok('引薦板面豁免', 'isRef422' in html)
ok('何生引薦閘 60', 'rel>=60' in seg('function ho422Tick(){', 'function pang422Tick(){'))
ok('何生進度常駐行動', '何生信任 ' in html and '信任達 60，何生會親自引薦一次機會' in html)
ok('彭引薦閘 70', 'fav>=70' in seg('function pang422Tick(){', 'function duty422ProgressText(){'))
ok('彭拍檔線索', '彭少祺已當你是拍檔' in html)

ok('幕後進度文案', 'function duty422ProgressText()' in html and '集齊兩種職務與兩個製作' in html)
ok('幕後成形派引薦', 'dutyRef422Done' in html)
ok('幕後卡進度', 'duty422Note' in html)

ok('武師班 hint 連結動作', '動作戲底子' in html)
ok('武師班進度顯示', '動作底子 ' in html and '／5 堂' in html)
ok('武師班成形提示', '武師班底子已成形' in html)
ok('試鏡歸因 src422', 'src422' in html and '此試鏡經「' in html)
ok('動作試鏡歸因', 'function stamina422AudNote(g)' in html)

ok('負標籤警告點名', '負面印記「' in html)
ok('負標籤頁後果', '負面印記：天王與巨星兩格最多容許一個' in html)
lad = seg('function resolveEnding410(st, opts){', 'function endingEveOptions410')
ok('SS 兜底次序（ID 在 SS 前）', lad.index('career = "ID"') < lad.index('career = "SS"'))
ok('E3 在 SS 前', lad.index('career = "E3"') < lad.index('career = "SS"'))
ok('E5 在 SS 前', lad.index('career = "E5"') < lad.index('career = "SS"'))

print('FAILURES:', fails)
sys.exit(1 if fails else 0)
