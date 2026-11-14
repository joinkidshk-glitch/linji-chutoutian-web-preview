# v20a203 WF4 迎新期＋Phase 2＋B3／C1／C2／C3 靜態測試。
# 用法：python3 tests/test_wf4_203_static.py [path-to-index.html]
# 反證：喺 pristine main（6e45cdb）上行 → 冇迎新欄位／helpers、池 72、舊文案、
#   day15 moneyMax 1000、story165CanPlay 冇典禮閘 → 多項乾淨 FAIL。
import os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(path))
src = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# --- B1：迎新期 CFG＋helpers＋兩個擲骰位用咗佢哋 ---
cfg = re.search(r'const WF4_CFG = \{([^}]*)\};', src)
ok('WF4_CFG 存在', cfg is not None)
cfg_body = cfg.group(1) if cfg else ''
ok('WF4_CFG pDayWelcome 0.12', 'pDayWelcome:0.12' in cfg_body)
ok('WF4_CFG pLocWelcome 0.08', 'pLocWelcome:0.08' in cfg_body)
ok('WF4_CFG welcomeDays 30', 'welcomeDays:30' in cfg_body)
ok('WF4_CFG 基線 pDay／pLoc 仲係 0.03', 'pDay:0.03' in cfg_body and 'pLoc:0.03' in cfg_body)
ok('wf4EffPDay 存在（線性漸降，day 0 最高、day 30 回基線）',
   'function wf4EffPDay(day)' in src and 'pDayWelcome' in src and '(w - d) / w' in src)
ok('wf4EffPLoc 存在', 'function wf4EffPLoc(day)' in src and 'pLocWelcome' in src)
tick = src[src.find('function wf4DailyTick'):src.find('function wf4TryLocEvent')]
ok('wf4DailyTick 用 wf4EffPDay（唔再直讀 WF4_CFG.pDay）',
   'wf4EffPDay(day)' in tick and 'WF4_CFG.pDay) return' not in tick)
loc = src[src.find('function wf4TryLocEvent'):src.find('function wf4PresentPending')]
ok('wf4TryLocEvent 用 wf4EffPLoc（唔再直讀 WF4_CFG.pLoc）',
   'wf4EffPLoc(day)' in loc and 'WF4_CFG.pLoc) return false' not in loc)

# --- B2：池 113（day 48／loc 65）已喺 193 測試釘死，呢度釘新 id 齊 ---
ev_ids = re.findall(r'id:"(wf4_ev_\w+)"', src)
ok('事件總數 113', len(ev_ids) == 113)
for nid in ['wf4_ev_day17', 'wf4_ev_day28', 'wf4_ev_set26', 'wf4_ev_set54']:
    ok('Phase 2 新事件在位：' + nid, nid in ev_ids)

# --- B3／C1：文案去重（逐單 chunk 計，唔係全檔數） ---
arr = re.search(r'DAILY_EVENTS_WF4\s*=\s*\[(.*?)\n\];', src, re.S)
ok('DAILY_EVENTS_WF4 陣列搵到', arr is not None)
chunks = {}
if arr:
    for chunk in re.split(r'(?=\{\s*id:"wf4_ev_)', arr.group(1)):
        im = re.match(r'\{\s*id:"(wf4_ev_\w+)"', chunk)
        if im:
            chunks[im.group(1)] = chunk
ok('B3「我喊埋一份」全池得 1 處（day12 保留，set17 已改寫）',
   sum(c.count('我喊埋一份') for c in chunks.values()) == 1
   and '我喊埋一份' in chunks.get('wf4_ev_day12', ''))
ok('B3「廿四味」全池得 1 處（day04 保留，st17 已換士多豆漿）',
   sum(c.count('廿四味') for c in chunks.values()) == 1
   and '廿四味' in chunks.get('wf4_ev_day04', ''))
ok('B3「涼茶」全池只喺 day04（st17 已換場景）',
   [k for k, c in chunks.items() if '涼茶' in c] == ['wf4_ev_day04'])
ok('B3 st17 係士多豆漿（唔再係涼茶舖）',
   '樓下士多嗰支豆漿' in chunks.get('wf4_ev_st17', '')
   and '士多阿叔' in chunks.get('wf4_ev_st17', ''))
ok('C1「點歌」全池只喺 set21 一單（st15 已改做司機追星往事）',
   [k for k, c in chunks.items() if '點歌' in c] == ['wf4_ev_set21'])
ok('C1 st15 係司機追星往事',
   '的士司機嗰段追星往事' in chunks.get('wf4_ev_st15', ''))
ok('C1 day15 閘 moneyMax 200', 'moneyMax:200' in chunks.get('wf4_ev_day15', ''))
ok('C1 day03 閘仲係 moneyMax 1000（分層對照）', 'moneyMax:1000' in chunks.get('wf4_ev_day03', ''))

# --- C2：覆寫表 7 單重映射＋12 單新 day 事件 ---
m = re.search(r'const WF4_SCENE_OVERRIDE134 = \{(.*?)\};', src, re.S)
ok('WF4_SCENE_OVERRIDE134 存在', m is not None)
table = {}
if m:
    for em in re.finditer(r'(wf4_ev_\w+):"([^"]+)"', m.group(1)):
        table[em.group(1)] = em.group(2)
for ev, f in [('wf4_ev_day05', 'bg_loc_cafe_cha.jpg'), ('wf4_ev_day07', 'bg_wf4_taxi.jpg'),
              ('wf4_ev_day09', 'bg_loc_gift_shop.jpg'), ('wf4_ev_day11', 'bg_loc_cafe_cha.jpg'),
              ('wf4_ev_day14', 'bg_loc_film_lion.jpg'), ('wf4_ev_day15', 'bg_loc_cafe_cha.jpg'),
              ('wf4_ev_st17', 'bg_loc_gift_shop.jpg')]:
    ok('C2 重映射 %s → %s' % (ev, f), f in table.get(ev, ''))
for nid in ['wf4_ev_day17', 'wf4_ev_day28']:
    ok('C2 新 day 事件入覆寫表：' + nid, nid in table)
ok('C2 覆寫表 48 行', len(table) == 48)
for ev, f in [('wf4_ev_day05', 'bg_loc_cafe_cha.jpg'), ('wf4_ev_day09', 'bg_loc_gift_shop.jpg'),
              ('wf4_ev_day14', 'bg_loc_film_lion.jpg')]:
    ok('C2 重映射目標檔案存在：%s' % f, os.path.isfile(os.path.join(root, 'assets/story/locs', f)))

# --- C3：典禮進行中閘住強制播 ---
ok('awards62CeremonyActive 存在（查 .awd62-stage）',
   'function awards62CeremonyActive()' in src and '".awd62-stage"' in src)
can = src[src.find('function story165CanPlay'):src.find('function story165ModalOpen')]
ok('story165CanPlay 有典禮閘（awards62CeremonyActive）', 'awards62CeremonyActive()' in can)
ok('C3 典禮閘排喺 story165NextOpen 之前（閘住先，唔係播完先驗）',
   0 <= can.find('awards62CeremonyActive()') < can.find('return story165NextOpen()'))
ok('C3 典禮舞台係全屏 overlay（真人玩家撳唔穿：position:fixed inset:0）',
   '.awd62-stage{position:fixed;inset:0' in src)

print('TOTAL ' + ('PASS' if not fails else 'FAIL %d' % len(fails)))
sys.exit(1 if fails else 0)
