# v20a206 B1：擴池新事件逐字抄舊事件——全池逐句去重＋模板腔打散。
# 用法：python3 tests/test_wf4_206_static.py [path-to-index.html]
# 反證：喺 v203 落地基線（main 165597e）上行 → 。級成句 20 撞、，級子句多撞、
#   「話佢識」28 次、8 對 review 引文全部 ≥2 單共享 → 多項乾淨 FAIL。
import os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

arr = re.search(r'DAILY_EVENTS_WF4\s*=\s*\[(.*?)\n\];', src, re.S)
ok('DAILY_EVENTS_WF4 陣列搵到', arr is not None)
chunks = {}
if arr:
    for chunk in re.split(r'(?=\{\s*id:"wf4_ev_)', arr.group(1)):
        im = re.match(r'\{\s*id:"(wf4_ev_\w+)"', chunk)
        if im:
            chunks[im.group(1)] = chunk
NEW41 = ['wf4_ev_day%02d' % d for d in range(17, 29)] + ['wf4_ev_set%02d' % s for s in range(26, 55)]
ok('事件總數 113', len(chunks) == 113)
ok('Phase 2 新事件 41 單齊', all(n in chunks for n in NEW41))

def texts(chunk):
    return re.findall(r'(?:tx|label|out):"([^"]*)"', chunk)

# --- (a) 。級成句去重（全池；split 。！？；＋全文，≥6 字） ---
by = {}
for eid, ch in chunks.items():
    ss = set()
    for t in texts(ch):
        for s in re.split(r'[。！？；]', t):
            s = s.strip()
            if len(s) >= 6:
                ss.add(s)
        if len(t.strip()) >= 6:
            ss.add(t.strip())
    for s in ss:
        by.setdefault(s, set()).add(eid)
coll = {s: sorted(v) for s, v in by.items() if len(v) >= 2}
ok('。級成句全池零共享（≥6 字）', not coll)
for s, evs in sorted(coll.items()):
    print('  COLLIDE [%s] %s' % (' / '.join(evs), s))

# --- (b) ，級子句去重（≥10 字；只計涉及新 41 單嘅對——舊池對舊池係 pre-existing，唔喺 B1 範圍） ---
by2 = {}
for eid, ch in chunks.items():
    ss = set()
    for t in texts(ch):
        for s in re.split(r'[，。、；！？\n]', t):
            s = s.strip()
            if len(s) >= 10:
                ss.add(s)
    for s in ss:
        by2.setdefault(s, set()).add(eid)
coll2 = {s: sorted(v) for s, v in by2.items()
         if len(v) >= 2 and any(e in NEW41 for e in v)}
ok('，級子句（≥10 字）凡涉新 41 單者零共享', not coll2)
for s, evs in sorted(coll2.items()):
    print('  COLLIDE2 [%s] %s' % (' / '.join(evs), s))

# --- (c) 模板腔：新 41 單入面每種 ≤3 次 ---
new_txt = ''.join(chunks[n] for n in NEW41 if n in chunks)
for p in ['話佢識', '成個人鬆晒', '聽到入晒神', '識食', '識做人', '眉飛色舞']:
    ok('模板「%s」新 41 單 ≤3 次（實 %d）' % (p, new_txt.count(p)), new_txt.count(p) <= 3)

# --- (d) 8 對 review 引文：每句最多喺 1 單出現（舊單保留嗰句計 1；兩單共享即 FAIL） ---
QUOTED = [
    ('1a set23 瞓覺 out', '佢瞓咗陣，落車嗰陣精神晒，司機話佢瞓得快，話呢行最緊要識得瞓'),
    ('1b set23 傾偈 out', '佢同車上面啲人傾偈，傾到去到嗰邊，成車人都熟晒，開工嗰陣特別齊心'),
    ('2a set15 望海 out', '佢望住個海，成個人靜落嚟，導演嗌開始嗰陣，佢嗰場戲一take就過'),
    ('2b set15 器材 out', '佢幫手望住啲器材，唔俾海風吹跌，場務話佢細心，收工嗰陣多謝咗佢'),
    ('3a set54 歌聲 beat', '做呢行，聽得多歌，把聲都會好啲'),
    ('3b set30 識聽歌 out', '職員話佢識聽歌，話呢行聽得多，把聲都會好啲'),
    ('4a set42 麵 out', '麵香到不得了，阿偉食到舐舐脷，師傅話佢識食，聽日再俾多啲佢'),
    ('4b set22 有口福', '後生仔，你今日有口福喇'),
    ('5 set27／33 識嘆', '話呢度啲風，係免費嘅福利嚟'),
    ('5b 免費福利（舊 set20 獨留）', '係免費嘅福利嚟'),
    ('6 set31／40 燈', '話聽日嗰場戲啲燈，幫佢打靚啲'),
    ('7 day24／set21 認可', '話佢嗰場戲做得好'),
    ('8 day11／set46 消息', '佢將啲消息記喺心入面，返到屋企再諗下邊啲啱自己，唔好白行一趟'),
]
for name, q in QUOTED:
    hit = [e for e, c in chunks.items() if q in c]
    ok('引文 ≤1 單：%s（實 %d：%s）' % (name, len(hit), ','.join(hit)), len(hit) <= 1)

# --- (e) 8 對重寫在位（新場景／新標題／新 choices，舊單原封不動） ---
ok('1 set32 係暈車（唔再係瞓覺＋傾偈）',
   '外景小巴嗰個暈車' in chunks.get('wf4_ev_set32', '')
   and '開窗畀暈車嗰個吹下風' in chunks.get('wf4_ev_set32', '')
   and '瞓陣養足精神' not in chunks.get('wf4_ev_set32', ''))
ok('1 set48 係爆胎（唔再係傾偈）',
   '外景車半路爆胎' in chunks.get('wf4_ev_set48', '')
   and '幫手遞工具畀司機' in chunks.get('wf4_ev_set48', '')
   and '同車上面啲人傾偈' not in chunks.get('wf4_ev_set48', ''))
ok('1 set23 舊單原封不動（對照）',
   '瞓陣養足精神' in chunks.get('wf4_ev_set23', '')
   and '同車上面啲人傾偈' in chunks.get('wf4_ev_set23', ''))
ok('2 set35 係潮水搶拍（唔再係望海入戲／望器材）',
   '捲起褲腳行去水邊' in chunks.get('wf4_ev_set35', '')
   and '幫手搬啲道具上岸' in chunks.get('wf4_ev_set35', '')
   and '望住個海入戲' not in chunks.get('wf4_ev_set35', ''))
ok('2 set15 舊單原封不動（對照）',
   '望住個海入戲' in chunks.get('wf4_ev_set15', ''))
ok('3 set54 係排話劇對白（唔再係練歌）',
   '收工嗰陣嗰段對白' in chunks.get('wf4_ev_set54', '')
   and '企喺度聽埋成段對白' in chunks.get('wf4_ev_set54', '')
   and '練緊新歌' not in chunks.get('wf4_ev_set54', ''))
ok('4 set42 係排骨飯（唔再係麵）',
   '電視台飯堂嗰碟排骨飯' in chunks.get('wf4_ev_set42', '')
   and '嗌碟排骨飯慢慢食' in chunks.get('wf4_ev_set42', '')
   and '今日嗰碗麵特別香' not in chunks.get('wf4_ev_set42', ''))
ok('5 set33 天台 out 已換（唔再係識嘆＋免費福利）',
   '話呢度啲風，係免費嘅福利嚟' not in chunks.get('wf4_ev_set33', '')
   and '佢哋兩個吹住水' in chunks.get('wf4_ev_set33', ''))
ok('6 set40 遞工具 out 已換（唔再係燈打靚啲）',
   '話聽日嗰場戲啲燈，幫佢打靚啲' not in chunks.get('wf4_ev_set40', '')
   and '燈光師較好燈' in chunks.get('wf4_ev_set40', ''))
ok('7 day24 係冇名信失物（唔再係認可來信）',
   '電視台嗰封冇名信' in chunks.get('wf4_ev_day24', '')
   and '幫手貼張告示等人認' in chunks.get('wf4_ev_day24', '')
   and '話佢嗰場戲做得好' not in chunks.get('wf4_ev_day24', '')
   and 'tierMin:1' in chunks.get('wf4_ev_day24', '')
   and 'yearMin:1992' in chunks.get('wf4_ev_day24', ''))
ok('8 set46 佈告板 out 已換（唔再係記喺心入面）',
   '佢將啲消息記喺心入面' not in chunks.get('wf4_ev_set46', '')
   and '佢將啲通告逐張睇' in chunks.get('wf4_ev_set46', ''))

# --- (f) fx 數值／schema 唔郁：money ±5..120、stress ±8 以內、其餘 ±1..2 ---
# 新 41 單必須全合規；舊池有 4 例 pre-existing 例外（v203 前已存在，唔喺 B1 範圍，釘死數目唔多唔少）
def fx_bad(eid, ch):
    bad = []
    for fxm in re.finditer(r'fx:\{([^}]*)\}', ch):
        for kv in re.finditer(r'(\w+):(-?\d+)', fxm.group(1)):
            k, v = kv.group(1), int(kv.group(2))
            if k == 'money':
                good = v == 0 or 5 <= abs(v) <= 120
            elif k == 'stress':
                good = abs(v) <= 8
            else:
                good = abs(v) <= 2
            if not good:
                bad.append('%s %s:%d' % (eid, k, v))
    return bad
bad_new = [b for n in NEW41 if n in chunks for b in fx_bad(n, chunks[n])]
ok('fx 新 41 單全合規（money ±5..120、stress ±8、其餘 ±1..2）', not bad_new)
for b in bad_new:
    print('  BADFX ' + b)
bad_old = sorted(b for e, c in chunks.items() if e not in NEW41 for b in fx_bad(e, c))
ok('fx 舊池例外維持 4 例 pre-existing（set04／cha03／home01／day01）',
   bad_old == ['wf4_ev_cha03 money:-2', 'wf4_ev_day01 stamina:4',
               'wf4_ev_home01 stamina:4', 'wf4_ev_set04 stamina:3'])
for b in bad_old:
    print('  OLDFX ' + b)

# --- (g) 禁詞零命中（全池 WF4 chunk） ---
banned = ['VCD', '互聯網', '手機', '狗仔隊', '1989', '1993', '手提電話', '傳呼機']
all_txt = ''.join(chunks.values())
for w in banned:
    ok('禁詞零命中：%s' % w, w not in all_txt)

# --- (h) 陣列內零註解（v193／v203 教訓：註解整爛 dlg108_static naive 解析） ---
ok('DAILY_EVENTS_WF4 陣列內零註解', arr and '//' not in arr.group(1) and '/*' not in arr.group(1))

print('TOTAL ' + ('PASS' if not fails else 'FAIL %d' % len(fails)))
sys.exit(1 if fails else 0)
