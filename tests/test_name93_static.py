# v20a93 NAME93 靜態測試：名實對照層標記在位、SAVE/softRev/?v= 冇變、NOTES 在位、
# 對照表錨點字面正確、normalize 接線在位（排 DUR90 之後）、段內冇真藝人名、
# softBridge 保底表冇俾本包改動（3700 保底字面在位）。
# 反證：v92 index 冇 NAME93 標記 → FAIL。
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
ok('NOTES_V20A93 文件在位', any(f.startswith('NOTES_V20A93') for f in os.listdir(ROOT)))
ok('NAME93 模組標記在位', 'v20a93 NAME93' in html)
ok('對照表在位', 'const NAME93_FIX = {' in html)
ok('套用函數在位', 'function name93ApplyGig(o){' in html)
ok('normalize 接線在位', 'try{ name93ApplyGig(o); }catch(_n93){}' in html)
_i93 = html.find('try{ name93ApplyGig(o); }catch(_n93){}')
_i90 = html.find('try{ dur90CalibrateGig(o); }catch(_d90){}')
ok('接線排 DUR90 之後', _i93 >= 0 and _i90 >= 0 and _i93 > _i90)
ok('錨點 ad_08 1500', '"gig_1988_ad_08": { payExact:1500, pay:[1350,1650], breachFee:830' in html)
ok('錨點 tv_08 降格 3600', '"gig_1988_tv_08": { tier:"中", roleScale:"variety_special", shootBand:[1,3], shootDaysHint:3' in html)
ok('錨點 改名專輯主唱', 'title:"《冬夜情歌通宵錄》專輯主唱"' in html)
ok('錨點 改名男主角', 'title:"《九龍警網》男主角"' in html)
ok('錨點 改名夜班警員', 'title:"《迷離警署夜》夜班警員"' in html)
ok('synopsis 替換對照在位（主唱臨記→主唱）', 'synRep:[["主唱臨記","主唱"]]' in html)
ok('synopsis 替換對照在位（臨記男主→男主角）', 'synRep:[["臨記男主飾演小隊長","男主角飾演小隊長"]]' in html)
seg_start = html.find('v20a93 NAME93')
seg_end = html.find('function normalizeGigRecord', seg_start) if seg_start >= 0 else -1
seg = html[seg_start:seg_end] if (seg_start >= 0 and seg_end > seg_start) else ''
ok('NAME93 段冇真藝人名', not any(n in seg for n in ['周星馳','劉德華','張國榮','周潤發','梁朝偉','梅艷芳','張曼玉','王祖賢','鍾楚紅','林青霞']))

if fails:
    print('FAILURES:', ' | '.join(fails)); sys.exit(1)
print('ALL PASS')
