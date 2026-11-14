# -*- coding: utf-8 -*-
# v20a99 VENUE99 靜態測試：古典大樓場地化——金禧大酒店・大禮堂。
# 反證：喺 v20a98 index 上行會 FAIL（冇 VENUE99、冇場地接線、地圖冇酒店標籤）。
# v20a137 更新：地區名 12 個已刪（地圖淨低會場標籤）；會場標籤計數改數 div
# （v137 JS 換算函數亦引用 .md97-venue99 類名，裸字串計數會多）。
# 用法：python3 tests/test_venue99_static.py [path-to-index.html]
import re, sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- (1) VENUE99 本體 ---
ok('場地常量存在（金禧大酒店・大禮堂）', 'const VENUE99_LINE = "金禧大酒店・大禮堂";' in src)
ok('台慶場地＝星河電視台（唔搬）', 'award_singho_tv: "星河電視台"' in src)
ok('venue99ForCeremony 存在', 'function venue99ForCeremony(id)' in src)
ok('venue99ApplyOverlay 存在', 'function venue99ApplyOverlay(FW)' in src)
i_tf = src.find('textfix55Freeplay(FREEPLAY_FW)')
i_v99 = src.find('venue99ApplyOverlay(FREEPLAY_FW)')
ok('覆寫喺 loadFreeplayFramework 內、textfix55 之後呼叫', 0 < i_tf < i_v99)
ok('覆寫表齊：inviteDek×3／press×3／news×3／朝早報紙×6',
   all(k in src for k in ['VENUE99_INVITE_DEK', 'VENUE99_PRESS_DEK', 'VENUE99_NEWS_LINE', 'VENUE99_NP_DEK'])
   and 'np_win_film_02' in src and 'np_nom_ad_01' in src)

# --- (2) 頒獎流程接線 ---
ok('buildAwardResultPack 掛 venue99', 'venue99: (typeof venue99ForCeremony==="function") ? venue99ForCeremony(ceremonyId) : ""' in src)
ok('請柬卡出場地行', '場地：${pack.venue99}' in src)
ok('結果卡副題帶場地', '[pack.displayName||"", pack.year||"", pack.venue99||""]' in src and 'np214-kicker' in src)
ok('典禮 beats 開場帶場地行', '(venue99 ? ("\\n" + venue99) : "")' in src)
ok('頒獎 log 記錄場地（手帳獎項頁用）', 'venue99: pack.venue99 || "",' in src)
ok('獎項頁 when 行帶場地', '(e.venue99 ? (" · " + e.venue99) : "")' in src)
ok('__awards 暴露 venue99（駕駛／除錯）', 'venue99: function(id)' in src)

# --- (3) 地圖景物標籤：唔開 LOCS、只加細字標籤 ---
ok('地圖有酒店細字標籤恰好一個', src.count('<div class="md97 md97-venue99"') == 1 and '>金禧大酒店</div>' in src)
md = re.findall(r'<div class="md97"[^>]*>([^<]+)</div>', src)
ok('地區名恰好 0 個（v137 已拎走；酒店標籤唔計入地區名）', len(md) == 0)
locs_seg = src.split('const LOCS')[1].split('const NPCS')[0] if 'const LOCS' in src else ''
ok('LOCS 冇金禧（唔開新地點、冇熱區）', '金禧' not in locs_seg and 'venue99' not in locs_seg)
ok('LOCS 仍 15 個地點', locs_seg.count('{ id:"') == 15)

# --- (4) pack JSON 冇直改（場地只經 index 覆寫） ---
stub = (p.resolve().parent / 'content' / 'STUB_AWARDS_CEREMONY_v1.json').read_text(encoding='utf-8')
news = (p.resolve().parent / 'content' / 'STUB_NEWSPAPER_MORNING_SOFT_v1.json').read_text(encoding='utf-8')
ok('awards stub JSON 冇金禧（冇直改 pack）', '金禧' not in stub)
ok('報紙 stub JSON 冇金禧（冇直改 pack）', '金禧' not in news)

# --- (5) 禁忌：VENUE99 數據表零真酒店名（註解入面嘅避開清單唔計） ---
m = re.search(r'const VENUE99_HOTEL[\s\S]*?function venue99ApplyOverlay', src)
tables = m.group(0) if m else ''
FORBIDDEN = ['半島酒店', '文華東方', '文華酒店', '富麗華', '帝苑', '香格里拉', '凱悅', '喜來登',
             '萬豪', '君悅', '港麗', '朗廷', '九龍酒店', '富豪酒店', '怡東酒店', '柏寧', '麗豪酒店']
ok('VENUE99 數據表零真酒店名', bool(tables) and all(n not in tables for n in FORBIDDEN))

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
