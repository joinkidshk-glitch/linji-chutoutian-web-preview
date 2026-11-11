# -*- coding: utf-8 -*-
# v20a100 CLEAN100 靜態測試：矛盾審計清理包——
#   (1) B-10 芬姐分名守門：茶水檔字串清零、珍姐三處到位；任何「芬姐」行唔准同
#       茶水／糖水／探病／醫院語境同行（CLEAN100 註解行除外）；
#   (2) B-12/C-05 稱呼線分類器：全 index 嘅「偉翔」（NPC 對白，唔計陳偉翔全名指稱）
#       只准出現在 T4 opener／pool、king、heart、patron／finale beat 語境；
#   (3) 檔案層衛生：protagonist／worldview／cast_main／gift_react 正規化；
#       SP_SPEAKER_REG 關海媚 display＝稱號；LOCS 海港廣播 desc 有電台交代；
#   (4) A-09：NEWS82 E5 第一段已改傳聞框架（盛傳／有傳／密斟），冇直述「相繼過檔」；
#   (5) TEXTFIX55_EXACT 新五條（C5 秋日×3、C1 星河電視城、C4 一筆勾銷）齊；
#       pack 原文仍然存在（證明行緊覆寫層、冇直改 pack）；
#   (6) B-04/B-06 掛點存在（chungPre91 年份閘、gu_n10after 三路換句）；
#   (7) B-05/B-07/B-08/B-09 結局呈現掛點存在（exodus 鍾楚凝段、GH 三路、E5 新句、曉晴 awardsLog 分版）。
# 反證：喺 v20a99 index 上行 → 多項 FAIL。
# 用法：python3 tests/test_cleanup100_static.py [path-to-index.html]
import io, json, os, re, sys

html_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'index.html')
root = os.path.dirname(os.path.abspath(html_path))
html = io.open(html_path, encoding='utf-8').read()
lines = html.split('\n')
fails = []
def ok(name, cond):
    if not cond: fails.append(name)
    print(('PASS ' if cond else 'FAIL ') + name)

# (1) B-10
ok('B10 茶水芬姐清零', '茶水芬姐' not in html)
ok('B10 茶水檔芬姐清零', '茶水檔芬姐' not in html)
ok('B10 珍姐 C9 糧單句', '茶水珍姐個仔開學要交學費' in html)
ok('B10 珍姐 C9 糖水句', '珍姐嗰日仲專登留咗碗糖水俾你' in html)
ok('B10 珍姐 醫院糖水句', '茶水檔珍姐唔知喺邊度收到風' in html)
bad_fen = []
for i, l in enumerate(lines, 1):
    # 茶水「帳」係片場地點（副導演芬姐鏈 F 相識場喺嗰度，屬合法語境）；
    # 要守嘅係茶水「檔」營運者身份同糖水／探病／醫院呢啲珍姐標誌動作。
    if '芬姐' in l and ('茶水檔' in l or '糖水' in l or '探病' in l or '醫院' in l):
        if 'CLEAN100' in l or 'v20a100' in l or 'B-10' in l: continue
        bad_fen.append(i)
ok('B10 芬姐唔同茶水檔語境同行', not bad_fen)
ok('B10 副導演芬姐鏈F保留', '副導演芬姐' in html and 'EXODUS_FEN' in html)

# (2) 稱呼線分類器
keypat = re.compile(r'^\s*(T[0-4]|king|heart|extra|support|lead|first|openers|pool|address|beats)\s*:')
beatpat = re.compile(r'^\s*([a-z][a-z0-9_]*):\s*\{\s*$')
injectpat = re.compile(r'\.beats\.([a-z0-9_]+)\s*=')
starpat = re.compile(r'const (ENC\w+?(?:DLG|FRAME)_\w+)\s*=')
cur_key, cur_beat, violations, total = None, None, [], 0
for i, l in enumerate(lines, 1):
    if starpat.search(l): cur_key, cur_beat = None, None
    m = injectpat.search(l)
    if m: cur_beat = m.group(1); cur_key = 'beats'
    km = keypat.match(l)
    if km: cur_key = km.group(1)
    bm = beatpat.match(l)
    if bm and cur_key == 'beats': cur_beat = bm.group(1)
    if '偉翔' in l and '陳偉翔' not in l:
        total += 1
        allowed = cur_key in ('T4', 'king', 'heart') or (cur_beat and re.search(r'patron|finale', cur_beat))
        if not allowed: violations.append((i, cur_key, cur_beat, l.strip()[:50]))
ok('B12 偉翔出現處全數合段位線 (%d 處)' % total, total >= 10 and not violations)
if violations: print('  violations:', violations)

# (3) 檔案層衛生
pj = json.load(io.open(os.path.join(root, 'content', 'protagonist.json'), encoding='utf-8'))
ok('H protagonist startDate 1990-01-01', pj.get('startDate') == '1990-01-01')
ok('H protagonist 三年目標', '三年內' in pj.get('goals', {}).get('long', ''))
ok('H protagonist 冇1988', '1988' not in json.dumps(pj, ensure_ascii=False))
wj = json.load(io.open(os.path.join(root, 'content', 'worldview.json'), encoding='utf-8'))
ok('H worldview 新名', wj.get('title') == '臨記埋位')
ok('H worldview 1990-1992', wj.get('settingYears') == '1990–1992')
ok('H worldview 冇八九後字眼', '八九後' not in json.dumps(wj, ensure_ascii=False))
cj = json.load(io.open(os.path.join(root, 'content', 'cast_main.json'), encoding='utf-8'))
def find_cast(o, cid):
    if isinstance(o, dict):
        if o.get('id') == cid: return o
        for v in o.values():
            r = find_cast(v, cid)
            if r: return r
    if isinstance(o, list):
        for v in o:
            r = find_cast(v, cid)
            if r: return r
    return None
lan = find_cast(cj, 'lan_ruoxi') or {}
kwan = find_cast(cj, 'kwan_hoimei') or {}
gao = find_cast(cj, 'gao_wenhan') or {}
ok('H 藍 role PA', 'PA' in lan.get('role', '') and '歌手' not in lan.get('role', ''))
ok('H 關海媚 role 花旦', '花旦' in kwan.get('role', '') and '總編' not in kwan.get('role', ''))
ok('H 高文瀚 role 冇經理人', '經理人' not in gao.get('role', ''))
gj = io.open(os.path.join(root, 'content', 'gift_react_copy.json'), encoding='utf-8').read()
ok('H gift 藍冇錄音前/練歌', '今晚錄音前' not in gj and '練歌時' not in gj)
ok('H gift 藍 PA 措辭到位', '今晚開工前先偷吃一粒' in gj and '跟場成晚' in gj)
ok('H gift 冇聯姻壓力標籤', '聯姻壓力' not in gj)
ok('H speaker 關海媚稱號', 'kwan_hoimei: { artId:"char_kwan", portraitsKey:null, display:"當紅花旦" }' in html)
ok('H speaker 冇原名display', 'display:"關海媚"' not in html)
ok('H 海港廣播 desc 電台交代', '海港電台嘅錄音室' in html)

# (3b) B-11 自檢夾具：seed/calendar 四條期望值已對返 START 1990；when 分支 p3when 維持 1988（節點自帶年份）
ok('B11 dualSeedChrome 1990', '"支線 · 1990春"' in html and 'dualSeedChrome' in html)
ok('B11 dualNoSeed 1990', '"支線 · 1990夏"' in html)
ok('B11 choiAutumnCal 1990', '"支線 · 1990秋"' in html)
ok('B11 p3when 維持1988（when自帶年份）', '"主線 · 1988秋"' in html)

# (4) A-09
i5 = html.find('"E5", day:532')
seg5 = html[i5:i5 + 1600] if i5 >= 0 else ''
ok('A09 E5 傳聞框架', '盛傳人事變動' in seg5 and '密斟過檔' in seg5)
ok('A09 E5 冇直述過檔句', '相繼過檔，星河電視' not in seg5)

# (5) TEXTFIX 五條 + pack 原文保留
for k in ['秋日午後片場休息，周采兒攞住筆記本', '秋日午後，片場休息角。', '窗外走廊間中有人行過，帶住幾分星河電視城特有嘅急促。',
          '我特登留畀你。做埋呢單，啲數一筆勾銷。', '片場休息角小訪桌（摺椅、筆記本）；秋日午後；訪問向——周采兒小訪阿偉']:
    ok('T EXACT key: ' + k[:14], k in html)
packmain = io.open(os.path.join(root, 'content', 'story_detail_c1_to_c17.json'), encoding='utf-8').read()
ok('T pack 原文保留（覆寫層）', '秋日午後，片場休息角。' in packmain and '啲數一筆勾銷' in packmain)

# (6) B-04/B-06 掛點
ok('B04 chungPre91 閘存在', 'chungPre91' in html and 'Math.min(tier,2)' in html)
ok('B04 heart 閘引用 chungPre91', 'D.heart && !(starId==="chung_choning" && chungPre91)' in html)
ok('B06 gu_n10after 三路換句', 'beatSeg100' in html and 'flag_standup_crew' in html and '嗰排台慶前後嘅事過咗之後' in html)

# (7) 結局呈現掛點
ok('B05 結局回收鍾楚凝段', '鍾楚凝嗰班機，你冇去送' in html and 'bdC100.chung_farewell' in html)
ok('B07 GH 三路歸因', 'ghOrigin100' in html and '彭少祺留低嗰份提攜' in html)
ok('B09 E5 冇無中生有句', '你手底下兩個新人，一個入圍，一個攞咗新人獎' not in html and '嗰種光，你認得' in html)
ok('B08 曉晴按awardsLog分版', 'won100' in html and 'end95Awards' in html and '你哋兩個一個攞獎、一個入圍' not in html)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
