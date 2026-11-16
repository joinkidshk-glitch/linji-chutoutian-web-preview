# Weave Phase 4-6（v20a29）靜態測試：主幹 1989 節點／結算 tick 接線／藍 PA 化／慣例不變
# v20a234：內嵌覆寫表已刪——N7–N11 由 content/story_detail_n1_to_n17.json 直出，唯一來源。
# 本檔改由 JSON pack 斷言同一批節點內容（標題／場地／紅星／旗／舊線清零），其餘部分不變。
# 用法：python3 tests/test_weave46_static.py [path-to-index.html]
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

# ---- 主幹節點本體（JSON pack，v20a234 唯一來源） ----
spine = json.dumps([nodes.get(k) for k in ('N7', 'N8', 'N9', 'N10', 'N11')], ensure_ascii=False)
ok('pack N7-N11 五節點在位', all(nodes.get(k) for k in ('N7', 'N8', 'N9', 'N10', 'N11')))
for cid, title, loc in [('N7','暴雨救場','film_harbour'), ('N8','選美後台','tvb_longmen'),
                        ('N9','茶餐廳度橋','cafe_cha'), ('N10','年尾追數','tvb_harbour'),
                        ('N11','戲路定型','tvb_longmen')]:
    ok('pack node present: '+cid, nodes.get(cid) is not None)
    ok('pack '+cid+' title '+title, nodes.get(cid, {}).get('title') == title)
    ok('pack '+cid+' locId '+loc, nodes.get(cid, {}).get('locId') == loc)
for star in ['魏詠男', '葉敏芝', '廖炳星', '顧明輝', '彭少祺']:
    ok('pack star present: '+star, star in spine)
for flag in ['flag_rain_rescue','flag_rain_shelter','flag_miss_cover','flag_miss_leak',
             'flag_bing_bridge','flag_bing_background','flag_chase_for_ho','flag_standup_crew',
             'flag_role_gangster','flag_role_cop']:
    ok('pack flag present: '+flag, flag in spine)
# 舊 pack 線關鍵字唔應入主幹內容（雷勁合約／藍若曦狗仔／商業文藝／台慶位）
for stale in ['雷勁', '藍若曦', '狗仔', '台慶位', '文藝線']:
    ok('pack free of stale pack line: '+stale, stale not in spine)

# ---- 內嵌覆寫已刪（v20a234） ----
for ident in ['const STORY_SPINE_NODES_1989 = {', 'function applyStorySpineOverrides46(',
              'try{ applyStorySpineOverrides46(); }catch(_sp46){}']:
    ok('inline override removed: '+ident, ident not in html)

# ---- 結算 tick＋債權＋禮物 ----
ok('story46SettleTick defined', 'function story46SettleTick(' in html)
ok('tick hooked in advanceDay after exodusFenTick',
   html.index('try{ if(typeof exodusFenTick==="function") exodusFenTick(); }catch(_ex){}')
   < html.index('try{ if(typeof story46SettleTick==="function") story46SettleTick(); }catch(_s46){}'))
ok('credit N7 const', 'id:"credit_c7_rain"' in html and '暴雨救場人情' in html)
ok('credit N10 const', 'id:"credit_c9_crew"' in html and '年尾出頭人情' in html)
ok('tick notes credits via favorLedgerNoteCredit', html.count('favorLedgerNoteCredit(credit.id, source)') >= 1)
ok('gift id const = gift_perfume_sample', 'const STORY46_GIFT_ID = "gift_perfume_sample";' in html)
ok('gift prepared flag handled', 'flag_miss_gift_prepared' in html)
ok('gift missed flag handled', 'flag_miss_gift_missed' in html)

# ---- 閘 registry 候選補齊（4-5 NOTES 預告） ----
gm = re.search(r'const STORY_GATE_3Y = \{(.*?)\n\};', html, re.S)
gate = gm.group(1) if gm else ''
c8line = next((ln for ln in gate.splitlines() if ln.strip().startswith('N9:')), '')
c15line = next((ln for ln in gate.splitlines() if ln.strip().startswith('N12:')), '')
for cand in ['"tag_comedy"', '"喜劇細胞"', '"tag_action"', '"身手好"']:
    ok('N9 tagAny candidate: '+cand, cand in c8line)
for cand in ['"tag_action"', '"身手好"']:
    ok('N12 tagAny candidate: '+cand, cand in c15line)
ok('gate thresholds unchanged (N7 creditGt 20 / N9 fameGt 28 / N11 dualGt 70)',
   'creditGt: 20' in gate and 'fameGt: 28' in gate and 'dualGt: 70' in gate)

# ---- SOFT 表對齊 ----
lm = re.search(r'const STORY_LOC_SOFT = \{(.*?)\n\};', html, re.S)
locs = lm.group(1) if lm else ''
for cid, loc in [('N7','film_harbour'), ('N9','cafe_cha'), ('N10','tvb_harbour'), ('N11','tvb_longmen'), ('N8','tvb_longmen')]:
    ok('STORY_LOC_SOFT '+cid+' -> '+loc, re.search(cid+r': "'+loc+r'"', locs) is not None)
tm = re.search(r'const STORY_TITLE_SOFT = \{(.*?)\n\};', html, re.S)
titles = tm.group(1) if tm else ''
for cid, t in [('N7','暴雨救場'), ('N9','茶餐廳度橋'), ('N10','年尾追數'), ('N11','戲路定型'), ('N8','選美後台')]:
    ok('STORY_TITLE_SOFT '+cid+' = '+t, (cid+': "'+t+'"') in titles)

# ---- 藍 PA 化：提示表 N7–N8 段清走歌手向 ----
nocomment = re.sub(r'/\*.*?\*/', '', html, flags=re.S)
hm = re.search(r'const STORY_HINT_SOFT = \{(.*?)\n\};', nocomment, re.S)
hints = hm.group(1) if hm else ''
ok('STORY_HINT_SOFT extractable (comments stripped)', bool(hints))
seg_start = hints.index('N7: { playerHint: "暴雨殺到') if 'N7: { playerHint: "暴雨殺到' in hints else -1  # v157：黑雨→暴雨（時代用語修正）
seg = hints[seg_start:] if seg_start >= 0 else ''
# v20a31（Phase 4-8）申報：STORY_HINT_SOFT 之後加咗 N14–N15 entry，其中 N14／N15 係樂壇節點，
# 提示正當地引用「唱片公司」場地（陸柏言／程天諾本業，唔關藍事）。呢段斷言嘅原意係驗
# N7–N8 段冇藍歌手向殘留，所以範圍收窄到 N12 entry 之前，語義不變。
seg_end = seg.index('N12: { playerHint:') if 'N12: { playerHint:' in seg else len(seg)
seg = seg[:seg_end]
ok('hint N7-N8 segment found', bool(seg))
ok('hint segment has N8 entry', 'N8: { playerHint:' in seg)
for stale in ['藍若曦', '擋狗仔', '狗仔', '雷勁', '唱片', '台慶', '文藝']:
    ok('hint N7-N8 free of singer-era text: '+stale, stale not in seg)

# ---- 藍若曦全檔核實（去註解後）：引擎基建＋v20a31 PA 線內容（WF2 覆寫表入面嘅 R_lan_* 五節點）之外唔准出現，全部唔准帶歌手向字眼 ----
# v20a31 申報：藍感情線已按拍板 PA 版上線，佢個名正當地出現喺 PA 覆寫內容入面（場記身份）；
# 原斷言「只准引擎基建」按新現實放寬到「基建＋PA 覆寫表」，「零歌手向」嗰半保留不變。
# v20a242：ROMANCE_LAN_PA_OVERRIDES 已刪，PA 線內容而家喺 WF2 覆寫表（R_lan_* 五節點）＋content JSON；
#   呢段改用 WF2 表做容器（synopsis／beats 同 JSON 一致）。
_lan_i = nocomment.find('const ROMANCE_WF2_OVERRIDES = {')
_lan_j = nocomment.find('function applyRomanceWf2Overrides81', _lan_i) if _lan_i >= 0 else -1
lan_block = nocomment[_lan_i:_lan_j] if (_lan_i >= 0 and _lan_j > _lan_i) else ''
lan_lines = [ln for ln in nocomment.splitlines() if '藍若曦' in ln]
# v20a33 申報：Phase 4-10 結局「差一步」場景（藍 PA 版：收尾加班戲撳通告牌）正當地用佢個名一次，
# 屬 PA 線內容，斷言放寬到包含嗰句（以「撳住個通告牌」標誌句識別）；「零歌手向」嗰半保留不變。
# v20a176 申報：ROM176 巧遇系統正當地用佢個名——出沒表註冊（name:"藍若曦"）、開場白（lan:"藍若曦…）、
# 茶餐廳風聲線（通告牌，PA 線內容）；NPCS 註冊條目同理。斷言放寬到包含呢三個模式；
# 「零歌手向」嗰半保留不變（通告牌係場記職責，唔係歌手向）。
# v20a183 申報：ROM183 粵語覆寫表（N3 禮物反應句正規化）正當地引用佢個名一次——覆寫鍵／值都係
# 原 pack 句嘅逐字粵語版，唔係新寫嘅歌手向內容。斷言放寬到包含 ROM183 block 入面嘅行。
_lan183_i = nocomment.find('const ROM183_GREET_MET')
_lan183_j = nocomment.find('function enc79OnWrap', _lan183_i) if _lan183_i >= 0 else -1
lan_block183 = nocomment[_lan183_i:_lan183_j] if (_lan183_i >= 0 and _lan183_j > _lan183_i) else ''
# v20a218 申報：TEXTFIX55_EXACT 正規化表（A1 加 6 條 when＋N12 synopsis 1 條）正當地引用佢個名一次——
# 嗰行係新舊文對照鍵值（「站哪邊」→「企邊」＋年份 1991→1990），唔係新寫嘅歌手向內容；
# 同行仲有幾十條無關映射（「唱片」等字眼屬於其他條目嘅舊／新文，唔係藍若曦內容）。斷言放寬到包含 TEXTFIX55_EXACT block 入面嘅行。
_tfix_i = nocomment.find('const TEXTFIX55_EXACT = {')
_tfix_j = nocomment.find('const TEXTFIX55_OPTS_STORY', _tfix_i) if _tfix_i >= 0 else -1
tfix_block = nocomment[_tfix_i:_tfix_j] if (_tfix_i >= 0 and _tfix_j > _tfix_i) else ''
ok('藍若曦 remaining occurrences are engine infra or PA-line content (v20a31)',
   all(('lan_ruoxi' in ln) or ('lan:"藍若曦' in ln) or ('name:"藍若曦"' in ln) or (ln in lan_block) or ('通告牌' in ln) or (ln in lan_block183) or (ln in tfix_block) for ln in lan_lines))
ok('藍若曦 occurrences carry no singer framing',
   all(not any(w in ln for w in ['歌手', '唱片', '狗仔', '宣傳場', '玉女']) for ln in lan_lines if ln not in tfix_block))

# ---- 玩家面真名掃描（現有 QA 禁用表） ----
for w in ['張國榮', '陳百強', '梅艷芳', '周潤發', '劉德華']:
    ok('no real star name in file: '+w, w not in html)
spine_nc = re.sub(r'/\*.*?\*/', '', spine, flags=re.S)
for w in ['關海媚', '陳淑芬', '施南生', 'Ho哥', 'Ho 哥']:
    ok('spine player text free of QA-banned: '+w, w not in spine_nc)

# ---- 慣例不變 ----
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('version marker v20a29', 'v20a29' in html)
ok('no inline override mechanism remains (v20a234: JSON pack is sole source)',
   'applyStorySpineOverrides' not in html and 'STORY_SPINE_NODES_1989' not in html)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
