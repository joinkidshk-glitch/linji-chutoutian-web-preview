# v20a89 BR89 靜態測試：分支補完——紀律（SAVE/softRev/?v= 不變）、模組標記在位、
# 新內容冇真藝人名、C6F 全套註冊齊、dead-flag 白名單每條有理由。
# 反證：v88 index 冇 BR89 標記 → FAIL。
import io, os, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('softRev 冇變', '"s107"' in html or "'s107'" in html)
ok('產品 ?v= 冇變', 'v20a10' in html)
ok('NOTES_V20A89 文件在位', os.path.exists(os.path.join(ROOT, 'NOTES_V20A89_BRANCHFIX.md')))
ok('BR89 標記在位', 'v20a89 BR89' in html)
ok('ripple 消費者在位', 'BR89：ripple 消費者' in html and 'debt_c4_ho_ripple' in html)
ok('grants 條件派發在位', 'fx:"liu_decline"' in html and 'fx:"mak_accept"' in html)
ok('C6F 節點＋閘＋注入器齊', 'STORY_SPINE_NODES_BR89' in html and 'C6F: { route: "route_film", weekMin: 15 }' in html and 'applyStoryBr89Nodes89' in html)
ok('BR89 條件通告齊（5 張）', all(('id:"gig_br89_%s"' % g) in html for g in ['patron_luk','patron_pang','patron_ching','stunt_ngai','liu_priority']))
ok('八線結局回收表在位', 'ARC_END89' in html and 'flag_ko_rival_respect' in html and 'flag_lei_ally' in html)
ok('手帳八線狀態句在位', 'br89ArcStatusHtml' in html and 'BR89_ARC_LINES' in html)
ok('新拼合 pair 在位', 'pair_br89_lok_truth' in html and 'pair_br89_chung_farewell' in html)
ok('A_ho 寫返 npcs 在位', 'HO89' in html and 'bumpNpc("agent", dv)' in html)
# 新內容冇真藝人名（抽 BR89 新寫段落粗查常見真名）
for real in ['陳百強', '張國榮', '梅艷芳', '周潤發', '劉德華', '梁朝偉', '王祖賢', '林青霞', '鍾楚紅', '張曼玉']:
    ok('冇真藝人名：' + real, real not in html)
# 白名單每條有理由
wl = json.load(io.open(os.path.join(ROOT, 'tests', 'br89_flag_whitelist.json'), encoding='utf-8'))
ok('白名單每條有理由（≥10 字）', all(isinstance(v, str) and len(v) >= 10 for v in wl.values()) and len(wl) >= 15)

print('FAILURES: ' + str(len(fails)))
raise SystemExit(1 if fails else 0)
