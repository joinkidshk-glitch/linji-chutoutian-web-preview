# v20a59 作品圖＋主演接入 static tests: POSTER59 區塊在位、137 表完整、接線齊（normalize／卡／詳情／
# 殺青／手帳作品頁）、海報以 POSTER59_DATA data URI 內嵌（10 條齊、解碼係 WebP；推送通道唔收 binary，
# 外部圖檔入唔到 repo）、600w master 檔保留喺 assets/posters/、硬規則（SAVE key）冇郁。
# 反證: run against a pre-v59 index -> POSTER59 block missing -> FAIL.
import sys, re, os, base64

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(idx_path, encoding='utf-8').read()
root = os.path.dirname(os.path.abspath(idx_path))
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def slice_fn(name):
    i = src.find('function ' + name + '(')
    if i < 0: return ''
    j = src.find('\nfunction ', i + 10)
    return src[i: j if j > 0 else len(src)]

# --- 區塊與對照表 ---
a = src.find('/* ===== v20a59 POSTER59')
chk('POSTER59 block present', a >= 0)
la = src.find('const LEADSTAR59 = {')
lb = src.find('};', la)
table = src[la:lb] if 0 <= la < lb else ''
chk('LEADSTAR59 has 137 gig keys', len(re.findall(r'"gig_1988_[a-z0-9_]+":', table)) == 137)
chk('LEADSTAR59 null-star entry （秋裝街頭隨拍輯）', '"gig_1988_ad_adm_autumn_low": null' in table)
pa = src.find('const POSTER59_IDS = {')
pb = src.find('};', pa)
pids = src[pa:pb] if 0 <= pa < pb else ''
chk('POSTER59_IDS has 10 pilot ids', len(re.findall(r'"gig_1988_[a-z0-9_]+": 1', pids)) == 10)
chk('star id map present', 'const POSTER59_STAR_IDS = {' in src and '"luk_baakyin"' in src)

# --- 接線 ---
norm = slice_fn('normalizeGigRecord')
chk('normalize hook wired', 'leadStar59Apply(o)' in norm)
card = slice_fn('gigCardHtml')
chk('card renders lead star line', 'leadStarLine59(g)' in card and '${leadStar}' in card)
detail = slice_fn('castingNoticeDetailHtml')
chk('detail has lead row', 'leadRow59' in detail and '主演' in detail)
chk('detail has poster figure', 'poster59fig' in detail and 'cn-poster59' in detail)
chk('wrap pushes poster figure', 'wrapPoster59Html(sh.gigId)' in src)
chk('wrap snapshots work fields', 'workTitle: _wg59w' in src and 'roleLabel: _wg59w' in src)

# --- 手帳作品頁 ---
chk('works tab button', 'data-htab="works"' in src and 'id="htab-works"' in src)
chk('works pane', 'id="home-pane-works"' in src and 'id="works-list"' in src)
tab_fn = slice_fn('setHomeTab')
chk('setHomeTab allows + renders works', 'works:1' in tab_fn and 'renderWorksPane()' in tab_fn)
chk('works renderer present', 'function renderWorksPane()' in src and 'function worksWallHtml59()' in src)

# --- CSS ---
for cls in ['.gig-card .lead-star{', '.cn-poster59{', '.wrap-poster59{', '.works-wall59{',
            '.work-card59{', '.work-csscard59{', '.work-name59{']:
    chk('css ' + cls, cls in src)

# --- 資產：POSTER59_DATA 內嵌（推送通道唔收 binary）、程式唔再引用相對路徑 ---
chk('poster59Path reads POSTER59_DATA', 'return POSTER59_DATA[gigId] || "";' in slice_fn('poster59Path'))
chk('no relative poster path in code', 'assets/posters/poster-' not in src)
da = src.find('const POSTER59_DATA = {')
db = src.find('\n};', da)
dblk = src[da:db] if 0 <= da < db else ''
entries = re.findall(r'"(gig_1988_[a-z0-9_]+)": "data:image/webp;base64,([A-Za-z0-9+/=]+)"', dblk)
chk('POSTER59_DATA has 10 entries', len(entries) == 10)
chk('POSTER59_DATA keys match POSTER59_IDS whitelist',
    sorted(k for k, _ in entries) == sorted(re.findall(r'"(gig_1988_[a-z0-9_]+)": 1', pids)))
def webp_ok(b64):
    try:
        raw = base64.b64decode(b64)
    except Exception:
        return False
    return len(raw) > 5000 and raw[:4] == b'RIFF' and raw[8:12] == b'WEBP'
chk('POSTER59_DATA entries decode to WebP RIFF', len(entries) == 10 and all(webp_ok(b) for _, b in entries))
blk59 = src[a:src.find('function normalizeGigRecord', a)] if a >= 0 else ''
chk('poster59 block embeds exactly 10 poster data URIs', blk59.count('data:image/webp;base64,') == 10)
# baseline 本身有 10 處 data:image/webp（舊 UI 內嵌圖）＋海報 10 條 = 20
# v20a62：+1 頒獎像素舞台底圖 AWARDS62_STAGE_PX（24,872 base64 字元，NOTES_V20A62 有帳）= 21
chk('webp data URI count = baseline 10 + posters 10 + stage62 1', src.count('data:image/webp') == 21)
expected = ['poster-1988-ad_central_spring_high.webp', 'poster-1988-film_03.webp',
            'poster-1988-film_cotton_autumn_low.webp', 'poster-1988-film_cotton_spring_high.webp',
            'poster-1988-film_harbour_high.webp', 'poster-1988-film_lion_summer_high.webp',
            'poster-1988-rec_03.webp', 'poster-1988-tv_03.webp', 'poster-1988-tv_06.webp',
            'poster-1988-var_04.webp']
for f in expected:
    p = os.path.join(root, 'assets', 'posters', f)
    good = os.path.isfile(p) and os.path.getsize(p) > 5000
    if good:
        with open(p, 'rb') as fh:
            magic = fh.read(12)
        good = magic[:4] == b'RIFF' and magic[8:12] == b'WEBP'
    chk('master asset retained ' + f, good)

# --- 硬規則 ---
chk('SAVE key unchanged', 'starVolunteer_map_v19w' in src)
chk('no pack JSON edit markers in block', 'gigs_1989' not in table and 'gig_1990' not in table)

if fails:
    print('FAILURES:', ' | '.join(fails))
    sys.exit(1)
print('ALL PASS')
