# Weave Phase 4-8（v20a31）靜態測試：主幹 1990 節點／N6 對齊／commit 機制／藍 PA 線／債權／預熱／慣例不變
# v20a234：內嵌覆寫表已刪——N12–N16／N6 由 content/story_detail_n1_to_n17.json 直出，唯一來源；
# v20a242：藍 PA 覆寫（ROMANCE_LAN_PA_OVERRIDES＋applyRomanceLanOverrides48）已刪——
#   R_lan_* 五節點由 content/story_detail_romance_lan_xu.json 直出，唯一來源。
# 用法：python3 tests/test_weave48_static.py [path-to-index.html]
import sys, pathlib, re, json
p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'index.html'
html = p.read_text(encoding='utf-8')
pack = json.loads((pathlib.Path(__file__).resolve().parent.parent / 'content' / 'story_detail_n1_to_n17.json').read_text(encoding='utf-8'))
nodes = {n['id']: n for n in pack.get('nodes', [])}
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

# ---- 1990 主幹節點（JSON pack，v20a234 唯一來源） ----
spine = json.dumps([nodes.get(k) for k in ('N12', 'N13', 'N14', 'N15', 'N16')], ensure_ascii=False)
ok('pack N12-N16 五節點在位', all(nodes.get(k) for k in ('N12', 'N13', 'N14', 'N15', 'N16')))
for cid, title, loc in [('N12','墊','film_harbour'), ('N13','高爾夫球','tvb_longmen'),  # v253：N13／N15／N16 新短詞標題（pack 側；STORY_TITLE_SOFT fallback 表唔郁，見下）
                        ('N14','樂壇前哨','rec_star'), ('N15','錄音室','rec_star'),
                        ('N16','飛紙仔','film_cotton')]:
    ok('pack node present: '+cid, nodes.get(cid) is not None)
    ok('pack '+cid+' title '+title, nodes.get(cid, {}).get('title') == title)
    ok('pack '+cid+' locId '+loc, nodes.get(cid, {}).get('locId') == loc)
for star in ['麥震東', '齊鎮海', '陸柏言', '程天諾', '廖炳星']:
    ok('pack star present: '+star, star in spine)
for flag in ['flag_stunt_double','flag_stunt_refuse','flag_side_tv','flag_side_film',
             'flag_fans_support','flag_fans_avoid','flag_vocal_polish','flag_vocal_train',
             'flag_newyear_improv','flag_newyear_script']:
    ok('pack flag present: '+flag, flag in spine)
for tag in ['搏命','惜身','親和力','高冷','偶像派','實力派','執生']:
    ok('pack tag present: '+tag, tag in spine)
spine_nc = spine
# 注意：「緋聞」一詞本身唔喺此列——N14 主幹內容正係陸柏言俾緋聞纏身（Qwen 原案前提），屬正當劇情字眼；
# 要驗嘅係 pack 自創節點「緋聞公關真假」成個唔喺度（邏輯測試另有標題級斷言）。
for stale in ['賀歲搶位','緋聞公關真假','徐寶珊','聯姻','舊底片','金九','關海媚']:
    ok('pack1990 free of pack-line/banned text: '+stale, stale not in spine_nc)

# ---- N6 對齊（JSON pack） ----
c6blk = json.dumps(nodes.get('N6'), ensure_ascii=False)
ok('pack N6 defined', nodes.get('N6') is not None)
ok('N6 title 角落那張枱 + loc tvb_longmen（v250 新短詞標題，舊「角落那張桌子」）', nodes.get('N6', {}).get('title') == '角落那張枱' and nodes.get('N6', {}).get('locId') == 'tvb_longmen')
ok('N6 flags canteen pair', 'flag_canteen_grind' in c6blk and 'flag_canteen_quit' in c6blk)
ok('N6 no date flags / no rel stats', 'date_' not in c6blk and 'rel_' not in c6blk)

# ---- 藍 PA 線（v20a242：覆寫表已刪，R_lan_* 由 content JSON 直出，唯一來源） ----
ok('ROMANCE_LAN_PA_OVERRIDES 已刪（去註解後）', 'ROMANCE_LAN_PA_OVERRIDES' not in nocomment)
ok('applyRomanceLanOverrides48 已刪（去註解後）', 'applyRomanceLanOverrides48' not in nocomment)
ok('lan override hook 已刪', 'applyRomanceLanOverrides48();' not in html)
lanpack = json.loads((pathlib.Path(__file__).resolve().parent.parent / 'content' / 'story_detail_romance_lan_xu.json').read_text(encoding='utf-8'))
lan_nodes = {n['id']: n for n in lanpack.get('nodes', []) if n['id'].startswith('R_lan_')}
for nid in ['R_lan_meet','R_lan_push1','R_lan_push2','R_lan_crisis','R_lan_ending']:
    ok('lan JSON node present: '+nid, nid in lan_nodes)
lan_txt = json.dumps([{k: n[k] for k in ('title', 'setting', 'synopsis', 'beats', 'choices') if k in n} for n in lan_nodes.values()], ensure_ascii=False)
for stale in ['唱片店','錄音室','合唱','狗仔','緋聞','聯姻','豪門','退圈','登機證','玉女','歌手']:
    ok('lan JSON free of singer-version text: '+stale, stale not in lan_txt)
for pa in ['場記', '通告牌']:
    ok('lan JSON carries PA framing: '+pa, pa in lan_txt)
ok('lan JSON beats 6/5/5/6/9', [len(lan_nodes[n].get('beats', [])) for n in ['R_lan_meet','R_lan_push1','R_lan_push2','R_lan_crisis','R_lan_ending']] == [6,5,5,6,9])  # v20a159 ROM159：crisis 重寫加一拍（阿爸親自到電視台），5→6
ok('lan JSON playerOffer 全部 false', all(lan_nodes[n].get('playerOffer') is False for n in lan_nodes))
ok('lan JSON push1 stage（唔係 music）', all('music' not in json.dumps(c.get('effects', {}).get('stats', {}), ensure_ascii=False) for n in lan_nodes.values() for c in n.get('choices', [])))
ok('no main-line override remains', 'STORY_SPINE_NODES_1990' not in html and 'STORY_SPINE_NODES_N6' not in html and 'applyStorySpineOverrides' not in html)

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
ok('credit N12 const', 'id:"credit_c15_stunt"' in html and '高危替身人情' in html)
ok('credit N16 const', 'id:"credit_c13_newyear"' in html and '賀歲片頂場人情' in html)
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
for cid, loc in [('N14','rec_star'), ('N16','film_cotton'), ('N13','tvb_longmen'), ('N12','film_harbour'), ('N15','rec_star'), ('N6','tvb_longmen')]:
    ok('STORY_LOC_SOFT '+cid+' -> '+loc, re.search(cid+r': "'+loc+r'"', locs) is not None)
tm = re.search(r'const STORY_TITLE_SOFT = \{(.*?)\n\};', html, re.S)
titles = tm.group(1) if tm else ''
for cid, t in [('N6','角落那張枱'), ('N14','樂壇前哨'), ('N16','飛紙仔'), ('N13','高爾夫球'), ('N12','墊'), ('N15','錄音室')]:  # v253：SOFT 表跟新短詞標題；v20a254：N12 高危替身→墊、N6 飯堂閒角→角落那張枱
    ok('STORY_TITLE_SOFT '+cid+' = '+t, (cid+': "'+t+'"') in titles)
hm = re.search(r'const STORY_HINT_SOFT = \{(.*?)\n\};', nocomment, re.S)
hints = hm.group(1) if hm else ''
for cid in ['N14','N16','N13','N12','N15']:
    ok('STORY_HINT_SOFT has '+cid, (cid+': { playerHint:') in hints)
ok('hints free of old N6 date-line title', '首次正式約會對象' not in hints)
ok('N5 nextHint 兩線並陳（v89 BR89 有意改版：N1 film 支補返 N6F 片場跟班，唔再只提飯堂閒角）', '走電影線有「片場跟班」' in hints and '走電視線有「飯堂閒角」' in hints)

# ---- 閘不變（4-5 門檻；v20a113 例外：N12 補 needDone N11，見下） ----
gm = re.search(r'const STORY_GATE_3Y = \{(.*?)\n\};', html, re.S)
gate = gm.group(1) if gm else ''
for frag in ['N12: { needDone: ["N11"], tagAny:', 'creditGt: 42', 'fameGt: 50', 'dualGt: 125', 'N6:  { needDone: ["N5"], route: "route_tv", weekMin: 15 }']:
    ok('gate unchanged fragment: '+frag, frag in gate)

# ---- 玩家面真名掃描（現有 QA 禁用表）＋新 block 禁字 ----
for w in ['張國榮', '陳百強', '梅艷芳', '周潤發', '劉德華']:
    ok('no real star name in file: '+w, w not in html)
newblocks_nc = re.sub(r'/\*.*?\*/', '', spine + c6blk + lan_txt + cmt, flags=re.S)
for w in ['關海媚', '陳淑芬', '施南生', 'Ho哥', 'Ho 哥']:
    ok('new player text free of QA-banned: '+w, w not in newblocks_nc)

# ---- 慣例不變 ----
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('version marker v20a31', 'v20a31' in html)
ok('softRev unchanged s107', 's107' in html)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
