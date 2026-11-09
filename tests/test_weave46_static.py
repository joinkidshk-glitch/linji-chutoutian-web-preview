# Weave Phase 4-6（v20a29）靜態測試：主幹 1989 節點覆寫／結算 tick 接線／藍 PA 化／慣例不變
# 用法：python3 tests/test_weave46_static.py [path-to-index.html]
import sys, pathlib, re
p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'index.html'
html = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS' if cond else 'FAIL') + ' ' + name)
    if not cond:
        fails.append(name)

# ---- 覆寫表本體 ----
ok('STORY_SPINE_NODES_1989 defined', 'const STORY_SPINE_NODES_1989 = {' in html)
m = re.search(r'const STORY_SPINE_NODES_1989 = \{(.*?)\n\};', html, re.S)
spine = m.group(1) if m else ''
ok('spine block extractable', bool(spine))
for cid, title, loc in [('C7','暴雨救場','film_harbour'), ('C11','選美後台','tvb_longmen'),
                        ('C8','茶餐廳度橋','cafe_cha'), ('C9','年尾追數','tvb_harbour'),
                        ('C10','戲路定型','tvb_longmen')]:
    ok('spine node present: '+cid, re.search(r'^\s*'+cid+r': \{', spine, re.M) is not None)
    seg = spine[spine.index(cid+': {'):] if (cid+': {') in spine else ''
    seg = seg[:1200]
    ok('spine '+cid+' title '+title, ('title: "'+title+'"') in seg)
    ok('spine '+cid+' locId '+loc, ('locId: "'+loc+'"') in seg)
for star in ['魏詠男', '葉敏芝', '廖炳星', '顧明輝', '彭兆基']:
    ok('spine star present: '+star, star in spine)
for flag in ['flag_rain_rescue','flag_rain_shelter','flag_miss_cover','flag_miss_leak',
             'flag_bing_bridge','flag_bing_background','flag_chase_for_ho','flag_standup_crew',
             'flag_role_gangster','flag_role_cop']:
    ok('spine flag present: '+flag, flag in spine)
# 舊 pack 線關鍵字唔應入覆寫內容（雷勁合約／藍若曦狗仔／商業文藝／台慶位）
for stale in ['雷勁', '藍若曦', '狗仔', '台慶位', '文藝線']:
    ok('spine free of stale pack line: '+stale, stale not in spine)

# ---- 套用函數＋掛點 ----
ok('applyStorySpineOverrides46 defined', 'function applyStorySpineOverrides46(' in html)
ok('override hook present', 'try{ applyStorySpineOverrides46(); }catch(_sp46){}' in html)
ok('override hook after STORY_WIRE.main assignment',
   html.index('STORY_WIRE.main = main;') < html.index('try{ applyStorySpineOverrides46(); }catch(_sp46){}'))

# ---- 結算 tick＋債權＋禮物 ----
ok('story46SettleTick defined', 'function story46SettleTick(' in html)
ok('tick hooked in advanceDay after exodusFenTick',
   html.index('try{ if(typeof exodusFenTick==="function") exodusFenTick(); }catch(_ex){}')
   < html.index('try{ if(typeof story46SettleTick==="function") story46SettleTick(); }catch(_s46){}'))
ok('credit C7 const', 'id:"credit_c7_rain"' in html and '暴雨救場人情' in html)
ok('credit C9 const', 'id:"credit_c9_crew"' in html and '年尾出頭人情' in html)
ok('tick notes credits via favorLedgerNoteCredit', html.count('favorLedgerNoteCredit(credit.id, source)') >= 1)
ok('gift id const = gift_perfume_sample', 'const STORY46_GIFT_ID = "gift_perfume_sample";' in html)
ok('gift prepared flag handled', 'flag_miss_gift_prepared' in html)
ok('gift missed flag handled', 'flag_miss_gift_missed' in html)

# ---- 閘 registry 候選補齊（4-5 NOTES 預告） ----
gm = re.search(r'const STORY_GATE_3Y = \{(.*?)\n\};', html, re.S)
gate = gm.group(1) if gm else ''
c8line = next((ln for ln in gate.splitlines() if ln.strip().startswith('C8:')), '')
c15line = next((ln for ln in gate.splitlines() if ln.strip().startswith('C15:')), '')
for cand in ['"tag_comedy"', '"喜劇細胞"', '"tag_action"', '"動作演員"']:
    ok('C8 tagAny candidate: '+cand, cand in c8line)
for cand in ['"tag_action"', '"動作演員"']:
    ok('C15 tagAny candidate: '+cand, cand in c15line)
ok('gate thresholds unchanged (C7 creditGt 20 / C8 fameGt 28 / C10 dualGt 70)',
   'creditGt: 20' in gate and 'fameGt: 28' in gate and 'dualGt: 70' in gate)

# ---- SOFT 表對齊 ----
lm = re.search(r'const STORY_LOC_SOFT = \{(.*?)\n\};', html, re.S)
locs = lm.group(1) if lm else ''
for cid, loc in [('C7','film_harbour'), ('C8','cafe_cha'), ('C9','tvb_harbour'), ('C10','tvb_longmen'), ('C11','tvb_longmen')]:
    ok('STORY_LOC_SOFT '+cid+' -> '+loc, re.search(cid+r': "'+loc+r'"', locs) is not None)
tm = re.search(r'const STORY_TITLE_SOFT = \{(.*?)\n\};', html, re.S)
titles = tm.group(1) if tm else ''
for cid, t in [('C7','暴雨救場'), ('C8','茶餐廳度橋'), ('C9','年尾追數'), ('C10','戲路定型'), ('C11','選美後台')]:
    ok('STORY_TITLE_SOFT '+cid+' = '+t, (cid+': "'+t+'"') in titles)

# ---- 藍 PA 化：提示表 C7–C11 段清走歌手向 ----
nocomment = re.sub(r'/\*.*?\*/', '', html, flags=re.S)
hm = re.search(r'const STORY_HINT_SOFT = \{(.*?)\n\};', nocomment, re.S)
hints = hm.group(1) if hm else ''
ok('STORY_HINT_SOFT extractable (comments stripped)', bool(hints))
seg_start = hints.index('C7: { playerHint: "黑雨殺到') if 'C7: { playerHint: "黑雨殺到' in hints else -1
seg = hints[seg_start:] if seg_start >= 0 else ''
ok('hint C7-C11 segment found', bool(seg))
ok('hint segment has C11 entry', 'C11: { playerHint:' in seg)
for stale in ['藍若曦', '擋狗仔', '狗仔', '雷勁', '唱片', '台慶', '文藝']:
    ok('hint C7-C11 free of singer-era text: '+stale, stale not in seg)

# ---- 藍若曦全檔核實（去註解後）：只准剩引擎基建出現處，唔准帶歌手向字眼 ----
lan_lines = [ln for ln in nocomment.splitlines() if '藍若曦' in ln]
ok('藍若曦 remaining occurrences are engine infra only',
   all(('lan_ruoxi' in ln) or ('lan:"藍若曦"' in ln) for ln in lan_lines) and len(lan_lines) <= 4)
ok('藍若曦 occurrences carry no singer framing',
   all(not any(w in ln for w in ['歌手', '唱片', '狗仔', '宣傳場', '玉女']) for ln in lan_lines))

# ---- 玩家面真名掃描（現有 QA 禁用表） ----
for w in ['張國榮', '陳百強', '梅艷芳', '周潤發', '劉德華']:
    ok('no real star name in file: '+w, w not in html)
spine_nc = re.sub(r'/\*.*?\*/', '', spine, flags=re.S)
for w in ['關海媚', '陳淑芬', '施南生', 'Ho哥', 'Ho 哥']:
    ok('spine player text free of QA-banned: '+w, w not in spine_nc)

# ---- 慣例不變 ----
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('version marker v20a29', 'v20a29' in html)
ok('content pack not edited inline (override mechanism only)', 'STORY_SPINE_NODES_1989[node.id]' in html)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
