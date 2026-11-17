# v20a89 BR89 靜態測試：分支補完——紀律（SAVE/softRev/?v= 不變）、模組標記在位、
# 新內容冇真藝人名、N6F 全套註冊齊、dead-flag 白名單每條有理由。
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
ok('N6F 節點由 JSON 出＋閘有 needDone N5＋內嵌表／注入器已刪（v20a250）',
   'N6F: { needDone: ["N5"], route: "route_film", weekMin: 15 }' in html
   and 'const STORY_SPINE_NODES_BR89' not in html and 'function applyStoryBr89Nodes89' not in html
   and any(n.get('id') == 'N6F' for n in json.load(open(os.path.join(ROOT, 'content', 'story_detail_n1_to_n17.json'), encoding='utf-8'))['nodes']))
BR89_13 = [('1991_film_101', 'enc83_luk_patron'), ('1991_variety_203', 'enc84_pang_patron'),
  ('1992_rec_106', 'enc84_ching_patron'), ('1991_film_103', 'enc79_liu_priority'),
  ('1992_film_103', 'enc83_liu_patron'), ('1991_film_110', 'enc83_mak_patron'),
  ('1992_tv_105', 'enc83_yip_patron'), ('1992_rec_105', 'enc83_gu_patron'),
  ('1991_ad_102', 'enc84_so_patron'), ('1991_tv_108', 'enc84_chung_patron'),
  ('1992_rec_102', 'enc83_lok_patron'), ('1991_film_111', 'enc83_ngai_patron'),
  ('1992_tv_104', 'enc83_chai_patron')]
ok('B5 BR89 提攜映射 13 張（新庫 id；SPEC §3.5A；舊 gig_br89_* 已清）',
   all(('gig_%s:"credit_%s"' % (g, c)) in html for g, c in BR89_13) and 'gig_br89_' not in html)
ok('B5 R-4 雙觸發在位（還錢結算 enc83_gu_loan_result＝1 亦開）', 'enc83_gu_loan_result' in html and 'gig_1992_rec_105' in html)
ok('八線結局回收表在位', 'ARC_END89' in html and 'flag_ko_rival_respect' in html and 'flag_lei_ally' in html)
ok('手帳八線狀態句在位', 'br89ArcStatusHtml' in html and 'BR89_ARC_LINES' in html)
ok('v267 新拼合 pair 已刪（MERGE_PAIRS 隨傳聞系統刪除）', 'pair_br89_lok_truth' not in html and 'pair_br89_chung_farewell' not in html and 'MERGE_PAIRS' not in html)
ok('A_ho 寫返 npcs 在位', 'HO89' in html and 'bumpNpc("agent", dv)' in html)
# 新內容冇真藝人名（抽 BR89 新寫段落粗查常見真名）
for real in ['陳百強', '張國榮', '梅艷芳', '周潤發', '劉德華', '梁朝偉', '王祖賢', '林青霞', '鍾楚紅', '張曼玉']:
    ok('冇真藝人名：' + real, real not in html)
# 白名單每條有理由
wl = json.load(io.open(os.path.join(ROOT, 'tests', 'br89_flag_whitelist.json'), encoding='utf-8'))
ok('白名單每條有理由（≥10 字）', all(isinstance(v, str) and len(v) >= 10 for v in wl.values()) and len(wl) >= 15)

print('FAILURES: ' + str(len(fails)))
raise SystemExit(1 if fails else 0)
