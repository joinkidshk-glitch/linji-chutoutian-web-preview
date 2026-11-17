# -*- coding: utf-8 -*-
# v20a98 CONTRA98 靜態測試：劇情矛盾修復在位檢查——
# 一、A-03 N1 頁首冬；A-01/A-02 正規化函數＋載入次序（contra98FixNodeWhen 喺 years66Walk 之前）
# 二、B-01 prepare 鉤入 StoryPlay.start＋B-02 Vera 危機幕錄影措辭（打歌稿清走）
# 三、C-01 N4 地點表 agency_ho＋兩句 hint 改事務所；C-04 GIG_EXACT 三條（兩 synopsis 值＋blurb）
# 四、C-02 caller 傳 locId＋sightings 葉敏芝行改唱片公司舞蹈房
# 五、紅線守恆：SAVE key／softRev／?v= 不變
# 反證：喺 v20a97 index 上行會 FAIL（冇 CONTRA98 標記、舊字眼仲喺度）。
# 用法：python3 tests/test_contra98_static.py [path-to-index.html]
import re
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# 一、A-01/A-02/A-03
ok('A-03: N1 頁首硬編碼改「冬」', ') || 1990)+"冬"' in src and ') || 1990)+"春"' not in src)
# v20a219：表加 R_tang_meet_stub 衞生行（22→23）；hiu／choi／xu 結局由冬改秋，winter_finale 11→8。
# v20a242：表加 R_lan_crisis／R_lan_ending 兩行（LAN 覆寫表已刪，JSON when 係顯示值，walk 後會越界；23→25）。
_m98 = re.search(r'const CONTRA98_WHEN_FIX = \{(.*?)\n\};', src, re.S)
_fix98 = re.findall(r'\b[A-Za-z_][A-Za-z_0-9]*:\["(?:1989|1990)[秋冬春夏]","era_[^"]+"\]', _m98.group(1)) if _m98 else []
ok('A-01/02: CONTRA98_WHEN_FIX 表在位（25 節點；v20a242 加 R_lan_crisis／R_lan_ending）',
   len(_fix98) == 25 and 'R_tang_meet_stub:["1989秋","era_1989_autumn_capital"]' in src
   and src.count('"1990冬","era_1990_winter_finale"') == 8)
ok('A-01/02: contra98FixNodeWhen 函數在位', 'function contra98FixNodeWhen(packs)' in src)
i_fix = src.find('contra98FixNodeWhen([main, rom1, rom2, rom3, rival])')  # v20a152：romTang 已停載，唔再入表；v20a159 ROM159：加 rom3
i_walk = src.find('rival, gateStub, dengMock')  # story pack 嗰次 walk（檔入面另有 gift pack walk，唔好混淆）
ok('A-01/02: 載入次序——正規化喺 story years66Walk 之前', 0 <= i_fix < i_walk)

# 二、B-01/B-02
ok('B-01: contra98PrepareNode 函數在位', 'function contra98PrepareNode(node)' in src)
ok('B-01: StoryPlay.start 已掛鉤', 'const pn98 = contra98PrepareNode(node)' in src)
ok('B-01: 坦白變體文案在位', '坦白心意：已經同采兒講明咗' in src and '坦白心意：已經同曉晴講明咗' in src)
ok('B-02: Vera 危機幕改錄影版 synopsis', '阿偉在電視台錄完影，Vera 在後台等他收工' in src)
# 注意：「你今晚打歌之後，還要…」係 TEXTFIX55_EXACT 嘅對照鍵（pack 原稿→清洗目標），合法在位；
# 要清走嘅係 WF2 覆寫自己嗰兩句（synopsis＋「仲要唔要」版首句）。
ok('B-02: WF2 覆寫打歌稿已清走', '"synopsis": "阿偉去電台打歌' not in src and '你今晚打歌之後，仲要唔要' not in src)
ok('B-02: Vera 首句改錄完影', '你今晚錄完影之後，仲要唔要趕下一個通告？' in src)

# 三、C-01/C-04
ok('C-01: STORY_LOC_SOFT.N4 改 agency_ho', 'N4: "agency_ho", /* v20a98 CONTRA98 C-01' in src)
ok('C-01: N3 nextHint 改事務所', '開啟後先去何生事務所。' in src)
ok('C-01: N4 lockedHint 改事務所', '開啟後再去事務所聽何生說。' in src)
ok('C-01: 舊「中環廣告聽何生講」已清走', '去中環廣告聽何生講' not in src)
# v20a243 RW-6：GIG_EXACT 已刪（舊通告庫專用；新庫無阿海／阿邦故事，0 命中）——C-04 修正無新庫目標，改為守衛舊錯字串唔再出現
ok('C-04: 舊「星河長篇正劇」已清走', '星河長篇正劇' not in src)
ok('C-04: 舊「星河電視台長篇」已清走', '星河電視台長篇' not in src)
ok('C-04: GIG_EXACT 已刪', 'const TEXTFIX55_GIG_EXACT' not in src)

# 四、C-02
ok('C-02: enc79BuildScript 收 locId', 'function enc79BuildScript(starId, forceFirst, locId)' in src)
ok('C-02: caller 傳 locId', 'enc79BuildScript(starId, !wasMet, locId)' in src)
ok('C-02: ENC79_FIRST_ALT98 表在位', 'const ENC79_FIRST_ALT98 = {' in src)
ok('C-02: sightings 葉敏芝行改唱片公司舞蹈房', '在唱片公司舞蹈房鏡前練舞' in src and 'locHint:"唱片公司舞蹈房"' in src)

# 五、守恆
ok('守恆: SAVE key 不變', 'starVolunteer_map_v19w' in src)
ok('守恆: softRev 不變', '"s107"' in src or "'s107'" in src or 's107' in src)
ok('守恆: ?v= 不變', 'v20a10' in src)

print('CONTRA98 STATIC: ' + ('%d FAIL' % len(fails) if fails else 'ALL PASS'))
sys.exit(1 if fails else 0)
