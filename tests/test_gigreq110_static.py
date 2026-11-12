# v20a110 OVR110 靜態測試：級別 vs 要求對齊層標記在位、SAVE/softRev/?v= 冇變、
# content pack JSON 冇俾本包改動、normalize 接線在位（NAME93 之後）、NOTES 在位、
# 對照表錨點字面正確、段內冇真藝人名。
# 反證：pristine main（v109）冇 OVR110 標記 → 多項 FAIL。
import io, os, subprocess, sys
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
ok('NOTES_V20A110 文件在位', any(f.startswith('NOTES_V20A110') for f in os.listdir(ROOT)))
ok('NOTES_V20A110_IMPLEMENT 文件在位', any(f.startswith('NOTES_V20A110_IMPLEMENT') for f in os.listdir(ROOT)))
ok('OVR110 模組標記在位', 'v20a110 OVR110' in html)
ok('TIER110 對照表在位', 'var TIER110 = {' in html)
ok('REQ110 對照表在位', 'var REQ110 = {' in html)
ok('套用函數在位', 'function ovr110Apply(o){' in html)
ok('normalize 接線在位', 'try{ ovr110Apply(o); }catch(_o110){}' in html)
_i110 = html.find('try{ ovr110Apply(o); }catch(_o110){}')
_i93 = html.find('try{ name93ApplyGig(o); }catch(_n93){}')
ok('接線排 NAME93 之後', _i110 >= 0 and _i93 >= 0 and _i110 > _i93)
_i90 = html.find('try{ dur90CalibrateGig(o); }catch(_d90){}')
ok('接線排 DUR90 之後', _i110 >= 0 and _i90 >= 0 and _i110 > _i90)
ok('TIER110 錨點：夜更和唱升格無（rec_hk_spring_mid 高）', '"gig_1988_rec_hk_spring_mid": "高"' in html)
ok('TIER110 錨點：櫥窗過場模特升中', '"gig_1990_film_01": "中"' in html)
ok('TIER110 錨點：exodus 急聘降初', '"gig_exodus_tv_senior": "初"' in html)
ok('REQ110 錨點：夜更和音 {vocal: 10}', '"gig_1988_rec_01": {"vocal": 10' in html)
ok('REQ110 錨點：賀年大碟和唱 {vocal: 20, stage: 20}', '"gig_1988_nat92_rechk_win_album": {"vocal": 20, "stage": 20' in html)
ok('REQ110 錨點：剔走項用 null', '"gig_1988_rec_01": {"vocal": 10, "stage": null, "charm": null}' in html)
ok('對照表只出現一次（TIER110）', html.count('var TIER110 = {') == 1)
ok('對照表只出現一次（REQ110）', html.count('var REQ110 = {') == 1)
ok('接線只出現一次', html.count('try{ ovr110Apply(o); }catch(_o110){}') == 1)
seg_start = html.find('v20a110 OVR110')
seg_end = html.find('function normalizeGigRecord', seg_start) if seg_start >= 0 else -1
seg = html[seg_start:seg_end] if (seg_start >= 0 and seg_end > seg_start) else ''
ok('OVR110 段冇真藝人名', not any(n in seg for n in ['周星馳','劉德華','張國榮','周潤發','梁朝偉','梅艷芳','張曼玉','王祖賢','鍾楚紅','林青霞']))
# content pack JSON 唔准俾本包改動（OVR110 一律行 normalize 層）
# v151 例外：三檔 DENG mock 准許淨刪 guanHaimeiUpgradeForbidden 一行（名禁令退役）。
def _v151_flag_only(p):
    try:
        d = subprocess.run(['git', '-C', ROOT, 'diff', 'HEAD', '--', p],
                           capture_output=True, text=True, timeout=30).stdout
    except Exception:
        return False
    removed = [l for l in d.splitlines() if l.startswith('-') and not l.startswith('---')]
    added = [l for l in d.splitlines() if l.startswith('+') and not l.startswith('+++')]
    return len(removed) in (1, 2) and all(r == '-    "guanHaimeiUpgradeForbidden": true,' for r in removed) and added == []
try:
    out = subprocess.run(['git', '-C', ROOT, 'diff', '--name-only', 'HEAD', '--', 'content/'],
                         capture_output=True, text=True, timeout=60)
    changed = [l for l in out.stdout.splitlines() if l.strip() and not _v151_flag_only(l)]
    ok('content/*.json 零改動', changed == [])
except Exception as e:
    ok('content/*.json 零改動（git 檢查失敗：%s）' % e, False)

if fails:
    print('FAILURES:', ' | '.join(fails)); sys.exit(1)
print('ALL PASS')
