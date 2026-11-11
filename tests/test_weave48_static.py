# Weave Phase 4-8（v20a31）靜態測試：主幹 1990 覆寫／C6 對齊／commit 機制／藍 PA 化／債權／預熱／慣例不變
# 用法：python3 tests/test_weave48_static.py [path-to-index.html]
import sys, pathlib, re
p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'index.html'
html = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS' if cond else 'FAIL') + ' ' + name)
    if not cond:
        fails.append(name)

nocomment = re.sub(r'/\*.*?\*/', '', html, flags=re.S)

def block(decl, endmark):
    i = html.find(decl)
    if i < 0: return ''
    j = html.find(endmark, i)
    return html[i:j] if j > i else ''

# ---- 1990 覆寫表 ----
ok('STORY_SPINE_NODES_1990 defined', 'const STORY_SPINE_NODES_1990 = {' in html)
spine = block('const STORY_SPINE_NODES_1990 = {', '/* C6 覆寫（Qwen 原案')
ok('spine1990 block extractable', bool(spine))
for cid, title, loc in [('C15','高危替身','film_harbour'), ('C14','站隊','tvb_longmen'),
                        ('C12','樂壇前哨','rec_star'), ('C16','偶像實力之爭','rec_star'),
                        ('C13','賀歲片','film_cotton')]:
    ok('spine node present: '+cid, re.search(r'^\s*'+cid+r': \{', spine, re.M) is not None)
    seg = spine[spine.index(cid+': {'):][:900] if (cid+': {') in spine else ''
    ok('spine '+cid+' title '+title, ('title: "'+title+'"') in seg)
    ok('spine '+cid+' locId '+loc, ('locId: "'+loc+'"') in seg)
for star in ['麥震東', '齊鎮海', '陸柏言', '程天諾', '廖炳星']:
    ok('spine star present: '+star, star in spine)
for flag in ['flag_stunt_double','flag_stunt_refuse','flag_side_tv','flag_side_film',
             'flag_fans_support','flag_fans_avoid','flag_vocal_polish','flag_vocal_train',
             'flag_newyear_improv','flag_newyear_script']:
    ok('spine flag present: '+flag, flag in spine)
for tag in ['搏命','惜身','親和力','高冷','偶像派','實力派','執生']:
    ok('spine tag present: '+tag, tag in spine)
spine_nc = re.sub(r'/\*.*?\*/', '', spine, flags=re.S)
# 注意：「緋聞」一詞本身唔喺此列——C12 主幹內容正係陸柏言俾緋聞纏身（Qwen 原案前提），屬正當劇情字眼；
# 要驗嘅係 pack 自創節點「緋聞公關真假」成個唔喺度（邏輯測試另有標題級斷言）。
for stale in ['賀歲搶位','緋聞公關真假','徐寶珊','聯姻','舊底片','金九','關海媚']:
    ok('spine1990 free of pack-line/banned text: '+stale, stale not in spine_nc)

# ---- C6 對齊 ----
c6blk = block('const STORY_SPINE_NODES_C6 = {', '/* v20a31 WEAVE_PHASE4_8：藍若曦感情線')
ok('STORY_SPINE_NODES_C6 defined', bool(c6blk))
ok('C6 title 飯堂閒角 + loc tvb_longmen', 'title: "飯堂閒角"' in c6blk and 'locId: "tvb_longmen"' in c6blk)
ok('C6 flags canteen pair', 'flag_canteen_grind' in c6blk and 'flag_canteen_quit' in c6blk)
ok('C6 no date flags / no rel stats', 'date_' not in c6blk and 'rel_' not in c6blk)

# ---- 藍 PA 覆寫 ----
lan = block('const ROMANCE_LAN_PA_OVERRIDES = {', '/* 載入後套用（4-8）')
ok('ROMANCE_LAN_PA_OVERRIDES defined', bool(lan))
for nid in ['R_lan_meet','R_lan_push1','R_lan_push2','R_lan_crisis','R_lan_ending']:
    ok('lan PA node present: '+nid, re.search(r'^\s*'+nid+r': \{', lan, re.M) is not None)
ok('lan PA block touches neither Vera nor Xu', 'R_vera' not in lan and 'R_xu' not in lan)
lan_nc = re.sub(r'/\*.*?\*/', '', lan, flags=re.S)
for stale in ['唱片店','錄音室','合唱','狗仔','緋聞','聯姻','豪門','退圈','登機證','玉女','歌手']:
    ok('lan PA free of singer-version text: '+stale, stale not in lan_nc)
for pa in ['場記', '通告牌']:
    ok('lan PA carries PA framing: '+pa, pa in lan_nc)

# ---- 套用函數＋掛點 ----
ok('applyStorySpineOverrides48 defined', 'function applyStorySpineOverrides48(' in html)
ok('override48 hook present', 'try{ applyStorySpineOverrides48(); }catch(_sp48){}' in html)
ok('override48 hook after romance.lanXu assignment',
   html.index('STORY_WIRE.romance.lanXu = rom2;') < html.index('try{ applyStorySpineOverrides48(); }catch(_sp48){}'))

# ---- commit 機制 ----
ok('COMMIT48_NODES defined', 'const COMMIT48_NODES = {' in html)
ok('COMMIT48_DEFS defined', 'const COMMIT48_DEFS = {' in html)
ok('COMMIT48_REL_MIN = 6', 'const COMMIT48_REL_MIN = 6;' in html)
cmt = block('const COMMIT48_NODES = {', '/* ===== Weave Phase 4-8（v20a31）：主幹節點債權結算 tick')
ok('commit block extractable', bool(cmt))
for flag in ['flag_hiu_commit','flag_choi_commit']:
    ok('commit flag present: '+flag, flag in cmt)
av = block('function commit48Available(', 'function commit48ActionsAt(')
ok('commit availability checks window 1992/autumn', 'choice47SeasonReached(1992, "秋")' in av)
ok('commit availability checks rel threshold', 'COMMIT48_REL_MIN' in av)
ok('commit availability checks crisis done + mutex flags', 'def.crisis' in av and 'def.otherFlag' in av and 'def.flag' in av)
ok('commit48Play uses StoryPlay force', 'StoryPlay.start(node, { force:true })' in html)
ok('openLoc hook for commit48ActionsAt after choice47 block',
   html.index('if(typeof choice47ActionsAt==="function")') < html.index('if(typeof commit48ActionsAt==="function")'))
ok('endingRomanceState48 reader defined', 'function endingRomanceState48(' in html)
for k in ['rel_hiu','rel_choi','rel_vera','rel_lan','rel_xu']:
    ok('romance state covers rel key: '+k, k in html[html.index('function endingRomanceState48('):html.index('function endingRomanceState48(')+1400])

# ---- 債權 tick ----
ok('story48SettleTick defined', 'function story48SettleTick(' in html)
ok('tick48 hooked in advanceDay after story46SettleTick',
   html.index('try{ if(typeof story46SettleTick==="function") story46SettleTick(); }catch(_s46){}')
   < html.index('try{ if(typeof story48SettleTick==="function") story48SettleTick(); }catch(_s48){}'))
ok('credit C15 const', 'id:"credit_c15_stunt"' in html and '高危替身人情' in html)
ok('credit C13 const', 'id:"credit_c13_newyear"' in html and '賀歲片頂場人情' in html)
ok('tick48 grants on spine flags', 'grant("flag_stunt_double"' in html and 'grant("flag_newyear_improv"' in html)

# ---- 程天諾預熱 ----
_sm = re.search(r'const PAPER_SIDE_ITEMS = \[(.*?)\n\];', html, re.S)
side = re.sub(r'/\*.*?\*/', '', _sm.group(1), flags=re.S) if _sm else ''
ok('PAPER_SIDE_ITEMS extractable', bool(side))
cheng = [ln for ln in side.splitlines() if '程天諾' in ln and 'h:"' in ln]
ok('preheat: exactly 3 程天諾 side items', len(cheng) == 3)
ok('preheat: all 程天諾 items fromYear 1992', all('fromYear:1992' in ln or 'fromYear: 1992' in ln for ln in cheng))

# ---- SOFT 表對齊 ----
lm = re.search(r'const STORY_LOC_SOFT = \{(.*?)\n\};', html, re.S)
locs = lm.group(1) if lm else ''
for cid, loc in [('C12','rec_star'), ('C13','film_cotton'), ('C14','tvb_longmen'), ('C15','film_harbour'), ('C16','rec_star'), ('C6','tvb_longmen')]:
    ok('STORY_LOC_SOFT '+cid+' -> '+loc, re.search(cid+r': "'+loc+r'"', locs) is not None)
tm = re.search(r'const STORY_TITLE_SOFT = \{(.*?)\n\};', html, re.S)
titles = tm.group(1) if tm else ''
for cid, t in [('C6','飯堂閒角'), ('C12','樂壇前哨'), ('C13','賀歲片'), ('C14','站隊'), ('C15','高危替身'), ('C16','偶像實力之爭')]:
    ok('STORY_TITLE_SOFT '+cid+' = '+t, (cid+': "'+t+'"') in titles)
hm = re.search(r'const STORY_HINT_SOFT = \{(.*?)\n\};', nocomment, re.S)
hints = hm.group(1) if hm else ''
for cid in ['C12','C13','C14','C15','C16']:
    ok('STORY_HINT_SOFT has '+cid, (cid+': { playerHint:') in hints)
ok('hints free of old C6 date-line title', '首次正式約會對象' not in hints)
ok('C5 nextHint 兩線並陳（v89 BR89 有意改版：C1 film 支補返 C6F 片場跟班，唔再只提飯堂閒角）', '行電影線有「片場跟班」' in hints and '行電視線有「飯堂閒角」' in hints)

# ---- 閘不變（4-5 門檻） ----
gm = re.search(r'const STORY_GATE_3Y = \{(.*?)\n\};', html, re.S)
gate = gm.group(1) if gm else ''
for frag in ['C15: { tagAny:', 'creditGt: 42', 'fameGt: 50', 'dualGt: 125', 'C6:  { route: "route_tv", weekMin: 15 }']:
    ok('gate unchanged fragment: '+frag, frag in gate)

# ---- 玩家面真名掃描（現有 QA 禁用表）＋新 block 禁字 ----
for w in ['張國榮', '陳百強', '梅艷芳', '周潤發', '劉德華']:
    ok('no real star name in file: '+w, w not in html)
newblocks_nc = re.sub(r'/\*.*?\*/', '', spine + c6blk + lan + cmt, flags=re.S)
for w in ['關海媚', '陳淑芬', '施南生', 'Ho哥', 'Ho 哥']:
    ok('new player text free of QA-banned: '+w, w not in newblocks_nc)

# ---- 慣例不變 ----
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('version marker v20a31', 'v20a31' in html)
ok('softRev unchanged s107', 's107' in html)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
