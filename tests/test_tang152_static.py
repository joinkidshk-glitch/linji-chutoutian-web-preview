# -*- coding: utf-8 -*-
# v20a152 靜態測試：鄧麗萍只刪感情線，留返排片 NPC。
# 刪：story_detail_romance_tang.json 停載（live 路徑）／R_tang_ending 抉擇（HE／BE＋flag_tang_commit／he／be）
#    ／DengLine HELD＋chrome＋selfCheck ending 項／BR89 收科回望／TEXTFIX55 開閘＋收尾條目／stub 開閘語言（載入正規化）。
# 留：DengLine 排片線 meet＋push1／push2／crisis（flag_tang_open ∧ rel_tang≥2 閘門）／stub 見面本身（純公事）
#    ／實用禮物反應／tang_laiping 角色登記／gift_prefs 見面閘。
# 反證：喺 pristine main（e08a070／v148）index 上行，刪項斷言會乾淨 FAIL（感情線仲喺度），唔會 crash。
# v20a160 M4 步 resync：walkup CSS 喺 L802 插入 5 行，三個錨點一律 ＋5（內容逐字核實，純漂移；其餘 M1／M6／M9 插入點全部喺 L44855 之後，唔影響本檔錨點）。
# v20a157 rebase 上 main 60b0a8f resync：splice 插入令三個錨點漂移（HELD ＋24、normaliser／loader ＋66；qa131/resync_rebase157.py difflib 對位核實內容逐字相同，純漂移；ok() 名全形括號標籤一併更新）。
# v20a149 rebase 上 main 6d08c7c（v171）resync：CSS ＋13，三個錨點一律 ＋13（qa149/resync_rebase149.py difflib 對位核實內容逐字相同，純漂移；ok() 名標籤一併更新）。
# 行號寫死（HELD 25725／normaliser 31387／loader 31531（v152 rebase 上 main 8409178：v155＋v161 令行號再移位） 等），rebase 要人手 resync。
# v20a153 第三輪 rebase 上 main a500536（v149）resync：HELD／normaliser／loader 三錨點 difflib 對位核實純漂移（見 qa153/resync_rebase153c.py）。
# v20a172 rebase 上 main a500536（v149）resync：v149 淨 ＋97，三個錨點一律 ＋13（HELD 25738／normaliser 31405／loader 31549；qa172/resync172b.py difflib 對位核實）。
# v20a172 rebase 上 main e2add29（v174）resync：HELD 唔郁（＜27080）、normaliser／loader ＋5（qa172/resync172c.py difflib 對位核實純漂移）。
# 用法：python3 tests/test_tang152_static.py [path-to-index.html]
# v20a176 resync：NPCS ＋7 行（插入點 L6017 之後），三個錨點一律 ＋7（qa176/resync176.py 逐行核實內容逐字相同，純漂移）。
# v20a183 resync：v183 淨 ＋117 行（C7 CSS ＋2／prefKind ＋1／TryIntercept ＋1／PlayEncounter ＋2／ROM183 block ＋107／確認 modal ＋3／goBit ＋1；difflib 對位核實純漂移，見 qa183/resync183.py）。
# v20a182 resync：v182 淨 ＋17 行全部喺錨點之前，三錨點一律 ＋2（qa182/resync182.py difflib 對位核實純漂移；ok() 名標籤一併更新）。
import json
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
ROOT = Path(__file__).resolve().parent.parent
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

def lines():
    return src.split('\n')

# --- 紀律：SAVE key／softRev／?v= 不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- 1. romance_tang pack 停載（live 路徑拎走，唔留死引用） ---
ok('停載：唔再 fetch story_detail_romance_tang.json', 'get("story_detail_romance_tang.json")' not in src)
ok('停載：romTang 變量已清', 'romTang' not in src)
ok('停載：STORY_WIRE.romance 冇 tang 槽', 'romance: { veraHiuChoi: null, lanXu: null }' in src)
ok('停載：iterNodes 冇 romance_tang', 'push("romance_tang"' not in src)
ok('停載：唔再報 romance tang 未載入', 'romance tang 未載入' not in src)
ok('停載：R 節點計數唔再含 romTang', '"R", [rom1,rom2].reduce' in src)
ok('停載：textfix／contra98／years66 呼叫冇 romTang',
   'textfix55StoryPack(romTang)' not in src and 'rom1, rom2, romTang, rival' not in src
   and 'romTang, rival, gateStub' not in src)

# --- 2. 感情線旗／節點已清（引號版＝程式碼引用；註解提及唔計） ---
ok('刪旗：程式碼再無 flag_tang_commit／he／be 引用',
   '"flag_tang_commit"' not in src and '"flag_tang_he"' not in src and '"flag_tang_be"' not in src
   and "'flag_tang_commit'" not in src and "'flag_tang_he'" not in src and "'flag_tang_be'" not in src
   and 'C_tang_ending_he' not in src and 'C_tang_ending_be' not in src)
ok('刪節點：R_tang_ending 只剩載入過濾嗰一次（filter 謂詞）', src.count('"R_tang_ending"') == 1)
ok('刪節點：R_tang_ending: 冒號式引用已清', 'R_tang_ending:' not in src)
ok('刪節點：pushSrc("R_tang_ending") 已清', 'pushSrc("R_tang_ending")' not in src)
ok('刪節點：WF2 覆寫表冇 tang 條目', '"R_tang_meet": {' not in src and '"R_tang_ending": {' not in src)
ok('刪節點：WF5 覆寫表冇 R_tang_ending 條目', '  R_tang_ending: {' not in src)
ok('刪節點：收科回望「盟友以上／嗰個紅圈」已清', '盟友以上' not in src and '嗰個紅圈' not in src)
ok('刪節點：CONTRA98_WHEN_FIX 冇 R_tang_ending', 'R_tang_ending:["1990' not in src)
ok('刪節點：CONTRA98 winter_finale 由 12 減到 11', src.count('"1990冬","era_1990_winter_finale"') == 11)

# --- 3. DengLine 排片線留返（meet＋push1／push2／crisis，閘門唔郁） ---
ok('留線：HELD 縮到 3 節（L25777）', lines()[25778].startswith('  const HELD = ["R_tang_push1","R_tang_push2","R_tang_crisis"];'))
ok('留線：PUSH_CHROME 有 push1／push2／crisis，冇 ending',
   'R_tang_push1: { chromeSeason:"winter"' in src and 'R_tang_push2: { chromeSeason:"spring"' in src
   and 'R_tang_crisis: { chromeSeason:"autumn"' in src)
ok('留線：selfCheck 簽名表留返 push1／push2／crisis 三行，冇 ending 行',
   'R_tang_push1: "C_tang_push1_exchange|flag_tang_push1_exchange|1' in src
   and 'R_tang_crisis: "C_tang_crisis_data|flag_tang_crisis_data|1' in src
   and 'R_tang_ending: "C_tang_ending_he' not in src)
ok('留線：push 閘門 flag_tang_open ∧ rel_tang≥2 唔郁',
   'pushGate("R_tang_push1", { ctx:{ flags:{ flag_tang_open:true }, rel_tang:2 } }).ok!==true' in src
   and 'if((b.openConditions||[]).join(",")!=="flag_tang_open,rel_tang_threshold")' in src)
ok('留線：debugUnlockTangPush（排片閘 debug）仲喺度', 'function debugUnlockTangPush()' in src)
ok('留線：事務所排片掣只列 push1／push2／crisis',
   '["R_tang_push1","R_tang_push2","R_tang_crisis"].forEach(beatId=>' in src)
ok('留線：WF5 業務覆寫 meet／push1／push2／crisis 仲喺度',
   '  R_tang_meet: {' in src and '  R_tang_push1: {' in src and '  R_tang_crisis: {' in src)
ok('留線：DengLine.loadMock／loadPushMock 呼叫仲喺度',
   'DengLine.loadMock(dengMock)' in src and 'DengLine.loadPushMock(dengPushMock)' in src)

# --- 4. 載入機制：stub 正規化＋push mock 過濾 ---
ok('機制：normaliseTangStub152 函數在位（L31460）', lines()[31462].startswith('function normaliseTangStub152(pack){'))
ok('機制：stub 正規化喺 TEXTFIX 之前行（L31604）', lines()[31606].strip().startswith('try{ normaliseTangStub152(rom2);'))
ok('機制：stub 新 synopsis＝純公事（排片聯絡）；舊開閘句只剩 v152 註解引文 1 次',
   '交換電話方便日後排片聯絡。' in src and src.count('正式開線需同時滿足') == 1
   and '交換聯絡與否' not in src)
ok('機制：stub 新抉擇 label／notes（唔留「深交／開閘」）',
   'keep.label = "留下聯絡：交換電話號碼"' in src
   and 'hold.label = "暫時唔留電話"' in src
   and '日後排片可以直接聯絡。' in src)
ok('機制：push mock 載入過濾 R_tang_ending 在位',
   'dengPushMock.beats = dengPushMock.beats.filter(function(b){ return b && b.id!=="R_tang_ending"; });' in src)

# --- 5. TEXTFIX55：開閘＋收尾條目已清，玫瑰改純公事，錶句改純公事 ---
ok('TEXTFIX：stub 開閘 synopsis／label 條目已清（舊句只剩 normaliser 註解引文各 1 次）',
   src.count('將影響日後感情線能否正式開啟') == 1
   and src.count('寫入 flag_tang_met（不開正式閘）') == 0)
ok('TEXTFIX：收尾 HE／BE label／notes 條目已清',
   '應承佢，一齊面對往後嘅事' not in src and '跨過合作嗰條線，關係唔再只係生意。' not in src
   and '守住界線，婉拒感情發展' not in src and '合作照舊，感情就到此為止。' not in src)
ok('TEXTFIX：開閘 notes 條目已清（meet 兩條＋stub 兩條；「不寫 flag_tang_open」只剩 normaliser 註解引文 1 次）',
   '打開同鄧麗萍合作的第一道閘' not in src and '暫緩開閘，鄧麗萍覺得你至少不是亂衝' not in src
   and '正式開閘見 R_tang_meet' not in src and src.count('不寫 flag_tang_open') == 1)
ok('TEXTFIX：玫瑰改做純公事拒絕（舊「心軟」句已清）',
   '玫瑰？呢度係排片部，唔係花店。想傾檔期，帶數據嚟。' in src
   and '你想我心軟，定係想拖住唔傾數？' not in src)
ok('TEXTFIX：腕表「感情條款」句改做純公事',
   '錶係錶，檔期係檔期——我哋先把場次談清楚。' in src
   and '就可以談感情條款' not in src.replace('别以為送完表就可以談感情條款；我們先把場次談清楚。', ''))
ok('TEXTFIX：共用條目「可與事業結局並存。」留返（lan／xu／vera 線共用，唔係 tang 專屬）',
   '"可與事業結局並存。": "呢段感情點收尾，事業嗰邊照常行落去。' in src)
ok('TEXTFIX：實用禮物句留返', '鄧麗萍：「實用。我鍾意睇得見、計得到嘅誠意。」' in src)
ok('TEXTFIX：relMap 冇 rel_tang 項', '["rel_tang","鄧麗萍"]' not in src)

# --- 6. content pack JSON 冇直改（原檔照有舊數據，證明係停載／過濾唔係改檔） ---
def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))
rom_tang = load_json('content/story_detail_romance_tang.json')
ok('pack 唔郁：romance_tang.json 照有 R_tang_ending＋commit／he／be（停載，唔係刪檔）',
   any(n.get('id') == 'R_tang_ending' for n in rom_tang.get('nodes', []))
   and 'flag_tang_commit' in json.dumps(rom_tang, ensure_ascii=False))
push_mock = load_json('content/MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json')
ok('pack 唔郁：push mock 照有 4 節連 R_tang_ending（載入過濾，唔係改檔）',
   len(push_mock.get('beats', [])) == 4 and any(b.get('id') == 'R_tang_ending' for b in push_mock.get('beats', [])))
lan_xu = load_json('content/story_detail_romance_lan_xu.json')
stub = [n for n in lan_xu.get('nodes', []) if n.get('id') == 'R_tang_meet_stub'][0]
ok('pack 唔郁：lan_xu stub 原稿照有開閘字（正規化喺載入嗰陣做，唔係改檔）',
   '感情線能否正式開啟' in stub.get('synopsis', ''))
gift_react = load_json('content/gift_react_copy.json')
rose = [e for e in gift_react.get('entries', []) if e.get('id', '').startswith('GR-tang-rose')][0]
ok('pack 唔郁：gift_react 玫瑰原句照喺度（TEXTFIX 改輸出，唔係改檔）',
   any('綁架我的情緒' in ln for ln in rose.get('lines', [])))
gift_prefs = load_json('content/gift_prefs.json')
ok('pack 唔郁：gift_prefs tang 見面閘留返（flag_tang_open）',
   gift_prefs.get('npcs', {}).get('tang', {}).get('requireFlagsAny') == ['flag_tang_open'])
seed = load_json('content/SOFT_PROGRESS_SEED_C3_C5_DENG_v1.json')
seed_txt = json.dumps(seed, ensure_ascii=False)
ok('seed：冇任何種子播 commit／he／be 旗',
   'flag_tang_commit' not in seed_txt and 'flag_tang_he' not in seed_txt and 'flag_tang_be' not in seed_txt)
ok('seed：push-ready 種子留返（播排片閘 flag_tang_open＋rel_tang 2，唔係感情線旗）',
   any(s.get('id') == 'seed_deng_push_ready' and s.get('state', {}).get('flags', {}).get('flag_tang_open') is True
       and s.get('state', {}).get('rel', {}).get('rel_tang') == 2 for s in seed.get('seeds', [])))

# --- 7. 角色／NPC 層留返 ---
ok('留角：tang_laiping 角色登記仲喺度', '"tang_laiping": {' in src and 'tang_laiping: { artId:"char_tang_opt"' in src)
ok('留角：R_tang_meet 仲喺無季節閘名單', '"R_tang_meet","R_xu_meet"' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
