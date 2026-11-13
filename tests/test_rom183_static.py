# v20a183 ROM183 靜態測試：修 v176 review B1–B4＋C1–C9 接線／文案／對比度／行號釘。
# 用法：python3 tests/test_rom183_static.py [path-to-index.html]
# 反證：pristine main (6ed68f8) 冇 ROM183 標記 → 多項 FAIL。
import io, json, math, os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = io.open(path, encoding='utf-8').read()
lines = html.split('\n')
root = os.path.dirname(os.path.abspath(path))
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)
def line(n):
    return lines[n - 1] if 1 <= n <= len(lines) else ''
def seg(start, end):
    try:
        i = html.index(start)
    except ValueError:
        return ''
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + 40000)
    return html[i:j]

# ---- 紅線：SAVE key／softRev／?v= 不變；content pack JSON 唔郁（C1／C3 行 runtime 覆寫） ----
ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('softRev 冇變', '"s107"' in html or "'s107'" in html)
ok('?v= 冇變', 'v=20a10' in html)
prefs = json.loads(io.open(os.path.join(root, 'content/gift_prefs.json'), encoding='utf-8').read())
ok('gift_prefs.json 唔郁（npcs 仍係原有 6 項）',
   set(prefs.get('npcs', {}).keys()) == {'vera', 'hiu', 'choi', 'lan', 'xu', 'tang'})
react = json.loads(io.open(os.path.join(root, 'content/gift_react_copy.json'), encoding='utf-8').read())
ok('gift_react_copy.json 唔郁（55 條原封不動，仲有「是不是」——粵語化行 runtime）',
   len(react.get('entries', [])) == 55
   and sum(1 for e in react['entries'] for ln in e.get('lines', []) if '是不是' in ln or '什麼' in ln) == 10)
npc_lines = json.loads(io.open(os.path.join(root, 'content/npc_lines_core.json'), encoding='utf-8').read())
ok('npc_lines_core.json 唔郁（colleague greet[0] 仲係書面語原文——粵語化行 runtime）',
   npc_lines['colleague']['greet'][0] == '阿偉，今天在星河電視台廠房碰到你，真巧')
tut = json.loads(io.open(os.path.join(root, 'content/tutorial_zh_HK.json'), encoding='utf-8').read())
tut_npc = [s for s in tut['steps'] if s['id'] == 'TUT_NPC'][0]
ok('tutorial_zh_HK.json 唔郁（TUT_MAP body 冇巧遇句——行 runtime 注入）',
   not any('撞到' in (b or '') for st in tut['steps'] if st['id'] == 'TUT_MAP' for b in st.get('body', [])))
ok('tutorial_zh_HK.json 唔郁（TUT_NPC body 冇巧遇句——行 runtime 注入）',
   all('撞到' not in b for b in tut_npc['body']))

# ---- ROM183 模組在位＋呼叫點（pack 賦值＋TEXTFIX55 清洗之後） ----
ok('ROM183 模組標記', 'v20a183 ROM183' in html)
for fn in ('rom183XuMetBefore183', 'rom183RelVal183', 'rom183RelText183', 'rom183RelLine183',
           'rom183WhoLine183', 'rom183ApplyLineOverrides', 'rom183ApplyGiftReactFix'):
    ok('函數在位：' + fn, ('function ' + fn) in html)
ok('C1/C6 覆寫呼叫點喺 textfix55SimplePack(d) 之後',
   html.find('rom183ApplyLineOverrides()') > html.find('textfix55SimplePack(d)'))
ok('C3 覆寫呼叫點喺 textfix55Walk(giftReact) 之後',
   html.find('rom183ApplyGiftReactFix()') > html.find('textfix55Walk(giftReact'))
ok('冇自己寫排他鎖／約會系統', 'rom159DateGate' in html and 'function rom159DateGate' not in html)
ok('giveGift 回傳冇 costsDay:true 殘留', 'costsDay:true' not in html)

# ---- B1：感情進度顯示（讀 S.story.rel，淨顯示） ----
ppl = seg('function people72Html(){', 'function br89ArcStatusHtml')
ok('B1 人脈頁女角行有感情進度行', 'rom183RelLine183(rk176)' in ppl and '感情：好感 ' in html and '／5</div>' in seg('function rom183RelLine183', 'function rom183WhoLine183'))
ok('B1 rel 讀 S.story.rel（唔讀 S.npcs）',
   'S.story.rel["rel_"+key]' in html or "S.story.rel['rel_'+key]" in html or 'S.story.rel' in seg('function rom183RelVal183', 'function rom183RelText183'))
ok('B1 巧遇 modal 有好感細字', 'rom183RelText183(key)' in html and '而家好感 ' in html)
ok('B1 冇改鎖邏輯（flag_romance_locked 零新增）', html.count('flag_romance_locked') == 0)

# ---- B2：最愛獨立標記 ----
ok('B2 prefKind 最愛回 favorite', 'if((pref.favorites||[]).indexOf(itemId)>=0) return "favorite";' in html)
ok('B2 calcDelta 最愛同喜歡同數', '(kind==="liked" || kind==="favorite")' in html)
ok('B2 reactionEntry 最愛查 :liked', '(pref==="favorite" ? "liked" : pref)' in html)
ok('B2 選擇器標記「★ 最愛」', '"★ 最愛"' in html)
ok('B2 確認 modal 有最愛句', '★ 最愛：佢最鍾意呢樣禮物。' in html)

# ---- B3：行開後在場行跟返巧遇盤 ----
ok('B3 doneToday 記地點（唔係 1）', 'sd.doneToday[pick.key] = locId;' in html)
ok('B3 openLoc 在場行行 rom183WhoLine183', 'rom183WhoLine183(L, npcId)' in html)
ok('B3 在場行有「今日已經撞過佢，聽日再嚟」', '今日已經撞過佢，聽日再嚟' in html)
ok('B3 撞過嗰位優先（doneToday 逐個對地點）', 'S.romDay.doneToday[k]!==L.id' in html)

# ---- B4：海媚未解鎖掣唔生效 ----
ok('B4 goBit 受 rom176MeiUnlocked 閘住', 'lockedMeiGo183' in ppl and 'rom176MeiUnlocked()' in ppl)
ok('B4 未解鎖顯示「主線再行前啲先撞到佢」（冇掣）', '主線再行前啲先撞到佢' in ppl)
go_seg = ppl[ppl.find('lockedMeiGo183'):]
ok('B4 鎖定分支係純文字 div（唔係掣）',
   '<div class="people-next">主線再行前啲先撞到佢</div>' in go_seg)

# ---- C1：三人 greet 粵語版（runtime 覆寫表） ----
ok('C1 ROM183_PACK_GREET 三句齊', all(x in html for x in
   ['咦，阿偉？咁啱嘅，喺呢度撞到你。', '咁啱。你今日呢身……算啦，唔講住，行埋嚟傾兩句。',
    '阿偉！啱啱好，我有單嘢想問你——唔係訪問，純粹八卦。']))
ok('C1 覆寫表經 NPC_LINES greet[0] 注入', 'NL[id].greet[0] = ROM183_PACK_GREET[id]' in html)

# ---- C2：徐寶珊分見過／未見過 ----
ok('C2 ROM176_GREET.xu 係初遇版（冇春茗）',
   'xu:"徐寶珊：「後生仔，行路望路呀。咦，係你——啱啱先撞到，唔好意思。」"' in html)
ok('C2 見過版喺 ROM183_GREET_MET', 'ROM183_GREET_MET' in html and '上次春茗撞過嗰個' in html)
ok('C2 PlayEncounter 分版（metBefore183）', 'metBefore183' in html and 'ROM183_GREET_MET.xu' in html)
ok('C2 TryIntercept 設旗前捕捉見過未', 'const metBefore183 = rom176WomanMet(pick.key);' in html)

# ---- C3：反應句粵語 filter（runtime，10 句逐字＋通用 fallback） ----
ok('C3 EXACT183 覆蓋 10 句（係咪見到／唔該你）',
   '係咪見到我冬天抱住紙杯震' in html and '比咩名牌都實際，唔該你' in html)
ok('C3 通用 fallback（是不是→係咪／什麼→咩）',
   'split("是不是").join("係咪")' in html and 'split("什麼").join("咩")' in html)
ok('C3 覆寫 byKey＋entries 兩份', '(R.entries||[]).forEach(fixEnt);' in html and 'for(const k in R.byKey) fixEnt(R.byKey[k]);' in html)

# ---- C4：海媚開場白冇舞台指示 ----
greet_seg = seg('const ROM176_GREET = {', 'const ROM176_TEA_LINES')
ok('C4 ROM176_GREET.mei 冇括號', '（佢望咗你一眼' not in greet_seg)
ok('C4 NL176 mei greet[1] 淨留「有嘢搵我？」', '"有嘢搵我？"' in html and '（佢望咗你一眼，冇即刻行開。）有嘢搵我？' not in html)

# ---- C5：.people-go 對比度 ≥4.5:1（WCAG 計法；底＝rgba(201,162,39,.28) 混米紙 #F2EBD8） ----
def lum(rgb):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)
m = re.search(r'\.people-go, \.debt-empty \.debt-repay-btn\{\s*margin-top:6px;[^}]*?background:rgba\(201,162,39,([\d.]+)\);\s*color:(#[0-9a-fA-F]{6});', html)
ok('C5 .people-go 規則讀到（深啡字＋加深底）', bool(m))
if m:
    a = float(m.group(1))
    fg = tuple(int(m.group(2)[i:i+2], 16) for i in (1, 3, 5))
    paper = (242, 235, 216)
    bg = tuple(round(a * c + (1 - a) * p) for c, p in zip((201, 162, 39), paper))
    l1, l2 = lum(fg), lum(bg)
    ratio = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
    print('INFO C5 對比度 %.2f:1（字 %s／底 rgb%s）' % (ratio, m.group(2), bg))
    ok('C5 對比度 ≥4.5:1', ratio >= 4.5)
else:
    ok('C5 對比度 ≥4.5:1', False)

# ---- C6：教學提隨機巧遇 ----
ok('C6 教學 inline TUT_NPC 有巧遇句', '去佢哋常出沒嘅地方，有機會撞到佢哋——撞到先可以傾談／送禮。' in html)
ok('C6 runtime 覆寫補 live pack TUT_NPC', 'st.id!=="TUT_NPC"' in html and 'LINE183' in html)
ok('C6 修正：inline TUT_MAP body 第三句係巧遇句（live 只行四步，TUT_NPC 唔顯示）',
   '"去佢哋常出沒嘅地方，有機會撞到佢哋——撞到先可以傾談／送禮。"]' in html)
ok('C6 runtime 覆寫補 live pack TUT_MAP', 'st.id==="TUT_MAP"' in html and 'st.body.push(LINE183)' in html)

# ---- C7：700 禮物選擇器兩欄 ----
ok('C7 700 media query 兩欄（#gift-pick-list grid 2 欄）',
   '@media (max-height:720px)' in html and '#gift-pick-list{ display:grid; grid-template-columns:1fr 1fr;' in html)

# ---- C8：掣名「去找」改「行下」 ----
ok('C8 掣名改「去 X 行下」', '去 ${homeName||"地圖"} 行下' in html)
ok('C8 「去找 · 」掣名零殘留', '去找 · ' not in html)
ok('C8 人脈 sub 句同新掣名一致（撞佢）', '去佢常出沒嘅地方撞佢；撞到先可以傾談／送禮。' in html)

# ---- C9：開局 intro 入場唔計額度；travel114 上限唔郁 ----
ok('C9 intro 入場帶 travelFree:true', 'openLoc(locId, {travelFree:true});' in html)
ok('C9 TRAVEL114_DAILY_CAP 仲係 2', 'const TRAVEL114_DAILY_CAP = 2;' in html)
ok('C9 額度閘本身唔郁（被擋 toast 逐字）',
   'toast("今日出行額度用完——今日已經去咗 2 個地方，聽日再去。")' in html)

print('---')
print('FAILURES: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
