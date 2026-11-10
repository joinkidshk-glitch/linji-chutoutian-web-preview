# v20a82 WF3 靜態測試：報紙事件系統接線／紅線／圖包／紀律
# 用法：python3 tests/test_wf3_82_static.py [path-to-index.html]
# 反證：喺 v20a81 index 行應該 FAIL（冇 WF3 標記）。
import json, os, re, sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, 'index.html')
src = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS' if cond else 'FAIL') + ' ' + name)
    if not cond:
        fails.append(name)

# 紀律：SAVE key／softRev／?v= 冇改
ok('SAVE key 不變', 'starVolunteer_map_v19w' in src)
ok('softRev 不變', 's107' in src)
ok('產品 ?v= 不變', 'v20a10' in src)

# 報紙事件系統接線
ok('NEWS82_EVENTS 表存在', 'const NEWS82_EVENTS = [' in src)
ok('enqueue 接受 world source', '"world" ? "world"' in src or 'srcRaw==="world"' in src)
ok('news82Tick 掛 advanceDay', src.count('news82Tick') >= 3)  # 定義＋tick 呼叫＋防衛呼叫
ok('wf3SettleTick 掛 advanceDay', src.count('wf3SettleTick') >= 3)
ok('圖包 fetch 接線', 'get("news_images_v82.json")' in src and 'NEWS82_IMGS' in src)
ok('頭版渲染有圖位＋段落', 'paper-img' in src and 'paper-para' in src)
ok('剪報渲染世界事件', 'clip-img' in src and 'clip-para' in src)
ok('世界事件優先排版', 'news82IsHead' in src)
ok('舊報留底標籤', '舊報留底' in src)

# 圖包本體
pack_path = os.path.join(root, 'content', 'news_images_v82.json')
ok('圖包檔案存在', os.path.exists(pack_path))
if os.path.exists(pack_path):
    pack = json.load(open(pack_path, encoding='utf-8'))
    imgs = pack.get('images', {})
    ok('圖包有六圖 E1–E6', sorted(imgs.keys()) == ['E1', 'E2', 'E3', 'E4', 'E5', 'E6'])
    ok('六圖皆 WebP data URI', all(v.startswith('data:image/webp;base64,') for v in imgs.values()))
    total = sum(len(v) for v in imgs.values())
    ok('圖包總量 < 300KB（實測 ~235KB）', total < 300000)
    ok('圖包唔入主檔（主檔冇圖包 base64 pfx）', len(imgs['E1'][:60]) > 0 and imgs['E1'][:80] not in src)

# 報紙紅線（只查 NEWS82_EVENTS 段）
m = re.search(r'const NEWS82_EVENTS = \[(.*?)\n\];', src, re.S)
ok('NEWS82_EVENTS 段可抽出', bool(m))
if m:
    blk = m.group(1)
    ok('冇用現實集體封號原字', '四大天王' not in blk)
    ok('城中四子（原創封號）', '城中四子' in blk)
    ok('E4 新創背景名在場', '杜朗軒' in blk and '簡柏霖' in blk)
    e1 = re.search(r'id:"E1".*?echo:', blk, re.S)
    ok('E1 段可抽出', bool(e1))
    if e1:
        # 只查玩家可見文字列（標題＋三段正文＋echo 句），唔計 day/imgKey 等結構欄
        texts = re.findall(r'headline:"([^"]*)"|"([^"]{20,})"', e1.group(0))
        visible = ''.join(a or b for a, b in texts)
        ok('E1 可見文字冇數字（唔寫人數）', not re.search(r'[0-9０-９]', visible))
    e3 = re.search(r'id:"E3".*?echo:', blk, re.S)
    ok('E3 段可抽出', bool(e3))
    if e3:
        ok('E3 只准一個數字講法（逾十二億元）', e3.group(0).count('億元') == 1 and '逾十二億元' in e3.group(0))
    ok('頭版正文冇主角名（阿偉）', all('阿偉' not in re.search(r'id:"%s".*?echo:' % i, blk, re.S).group(0) for i in ['E1', 'E2', 'E3'] if re.search(r'id:"%s".*?echo:' % i, blk, re.S)))
    ok('冇真人名（抽查清單）', not any(n in blk for n in ['劉德華', '張學友', '黎明', '郭富城', '周星馳', '成龍', '周潤發']))

# 鏈 B/C/D 接線
ok('鏈 B 隱藏通告', 'gig_wf3_liao_stage' in src and 'WF3_LIAO_GIG' in src)
ok('鏈 B 收割通告', 'gig_wf3_liao_harvest' in src)
ok('mergeWf3Gigs 掛通告板', src.count('mergeWf3Gigs') >= 3)
ok('試鏡前抉擇（steady/steal）', 'liaoChoice' in src and '企呢個位之前' in src)
ok('記仇債', 'debt_wf3_liao_grudge' in src and '面子債' in src)
ok('鏈 A 債權', 'credit_wf3_lu_team' in src)
ok('鏈 D 提點抉擇 C11_d', '"C11_d"' in src and 'flag_yip_warned82' in src)
ok('鏈 D 經理人債權（同 enc79 分開）', 'credit_wf3_yip_manager' in src)
ok('wf3PrepareNode82 掛 StoryPlay', src.count('wf3PrepareNode82') >= 3)
ok('WF3_TALK 六節點', all(('W3_' + s) in src for s in ['ho_liao', 'ho_m27', 'liao_m27', 'lu_pa', 'fong_jump', 'fong_hold']))
ok('WF3_TALK 掛地點 sheet', 'wf3TalkActionsAt' in src)
ok('方小龍情報卡', 'rumor_wf3_fong_mid' in src and 'rumor_wf3_fong_high' in src)

# 花邊池／碎片（同 logic 測試分工：呢度只查存在性，數量喺 logic／weave32 查）
ok('花邊新登記 9 則 id 齊', all(('id:"side_' + s + '"') in src for s in ['yip_swimsuit', 'ku_wrap', 'boxoffice_record', 'poach_rumor', 'comedy_king', 'singer_contest', 'astronaut_family', 'taiwan_money', 'own_studio']))

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
