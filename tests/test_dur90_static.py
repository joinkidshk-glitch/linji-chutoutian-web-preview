# v20a90 DUR90 靜態測試：校準標記在位、SAVE/softRev/?v= 冇變、NOTES 在位、
# 校準帶字面正確、normalize 接線在位、冇真藝人名。
# 反證：v89 index 冇 DUR90 標記 → FAIL。
import io, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ipath = os.path.join(ROOT, 'index.html')
html = io.open(ipath, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('softRev 冇變', '"s107"' in html or "'s107'" in html)
ok('產品 ?v= 冇變', 'v20a10' in html)
ok('NOTES_V20A90 文件在位', any(f.startswith('NOTES_V20A90') for f in os.listdir(ROOT)))
ok('DUR90 模組標記在位', 'v20a90 DUR90' in html)
ok('舊帶指紋在位', 'const DUR90_OLD_BAND = {' in html and 'film_lead_big:[28,30]' in html)
ok('日薪帶在位', 'const DUR90_DAILY = {' in html and '"高": [[1000,3000],[1500,8000]]' in html)
ok('校準函數在位', 'function dur90CalibrateGig(o){' in html)
ok('normalize 接線在位', 'try{ dur90CalibrateGig(o); }catch(_d90){}' in html)
ok('電影主角帶 22–28', 'film_lead_big:[22,28]' in html)
ok('電視主角帶 24–36', 'tv_lead_long:[24,36]' in html)
ok('客串帶 1–5', 'tv_cameo_short:[1,5]' in html)
ok('廣告帶 1–2', 'ad_av:[1,2]' in html and '"廣告":[1,2]' in html)
ok('寫真帶 1–2', 'photobook:[1,2]' in html)
ok('大碟帶 6–14', 'rec_album:[6,14]' in html)
ok('綜藝特輯帶 1–3', 'variety_special:[1,3]' in html)
seg_start = html.index('v20a90 DUR90 工期/片酬校準')
seg_end = html.index('function normalizeGigRecord', seg_start)
seg = html[seg_start:seg_end]
ok('DUR90 段冇真藝人名', not any(n in seg for n in ['周星馳','劉德華','張國榮','周潤發','梁朝偉','梅艷芳','張曼玉','王祖賢','鍾楚紅','林青霞']))

if fails:
    print('FAILURES:', ' | '.join(fails)); sys.exit(1)
print('ALL PASS')
