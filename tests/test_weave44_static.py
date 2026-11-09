# Weave Phase 4-4（v20a27）靜態測試：鏈 G 第 2 拍接線＋舊檔安全＋排序跟進＋慣例不變
# 用法：python3 tests/test_weave44_static.py [path-to-index.html]
import sys, pathlib
p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'index.html'
html = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS' if cond else 'FAIL') + ' ' + name)
    if not cond:
        fails.append(name)

# 回音本體
ok('echo tick fn defined', 'function familyPaperEchoTick(' in html)
ok('echo note text fn defined', 'function familyEchoNoteText(' in html)
ok('echo toast main const', 'const FAMILY_ECHO_TOAST_MAIN = "茶餐廳伙記轉告：你阿媽打嚟，話喺報紙見到你個名。"' in html)
ok('echo toast sub const (剪報頁提示)', 'const FAMILY_ECHO_TOAST_SUB' in html and '剪報頁有得睇返' in html)
ok('echo note const （阿媽剪報紙）', 'const FAMILY_ECHO_NOTE' in html and '夾喺本電話簿入面' in html and '較剪' in html)
ok('echo toast is two-part (sub)', 'toast(FAMILY_ECHO_TOAST_MAIN, { sub:FAMILY_ECHO_TOAST_SUB })' in html)

# 偵測規則（狀態欄＋跨級條件）
ok('familyHome gains paperTier/echoNote/echoDay defaults', 'paperTier:"", echoNote:"", echoDay:-1' in html)
ok('state normalises new fields', 'if(typeof st.paperTier!=="string") st.paperTier = "";' in html
   and 'if(typeof st.echoNote!=="string") st.echoNote = "";' in html
   and 'if(typeof st.echoDay!=="number") st.echoDay = -1;' in html)
tick = html.split('function familyPaperEchoTick(')[1].split('\n}')[0] if 'function familyPaperEchoTick(' in html else ''
ok('tick: first observation initialises only', 'if(!st.paperTier){ st.paperTier = tier; return false; }' in tick)
ok('tick: crossing = anon -> named|titled and no prior echo',
   'st.paperTier==="anon" && (tier==="named" || tier==="titled") && !st.echoNote' in tick)
ok('tick: reads live newspaperNameTier', 'newspaperNameTier()' in tick)
ok('tick: writes echoNote + echoDay on fire', 'st.echoNote = FAMILY_ECHO_NOTE;' in tick and 'st.echoDay = (S.dayIndex|0);' in tick)

# 掛點：commitMorningPaper 主流程、saveQ 之前、只呼叫一次
ok('hook: commitMorningPaper calls tick once', html.count('familyPaperEchoTick();') == 1)
ok('hook: tick runs before saveQ in commit', 
   html.index('familyPaperEchoTick();') < html.index('if(opts.persist!==false){ try{ saveQ(); }catch(_e){} }', html.index('function commitMorningPaper(')))
commit_block = html.split('function commitMorningPaper(')[1].split('function presentDueMorningPaper(')[0] if 'function commitMorningPaper(' in html else ''
ok('hook: tick inside commit main flow (after clippings presented-day stamp)',
   'S.newspaperLastPresentedDay = S.dayIndex|0;' in commit_block and 'familyPaperEchoTick' in commit_block)

# 呈現：屋企卡回音字條（同態度字條分開、喺態度字條之後）
ok('render: family-echo line in debt pane', 'family-echo' in html and 'familyEchoNoteText()' in html)
ok('render: echo after attitude in card template',
   html.index('family-attitude') < html.index('family-echo'))

# 4-3 覆檢跟進：顯示排序（只改顯示、唔郁數據）
ok('order: family cards extracted for front placement', 'famCardsHtml' in html and 'debtCards.filter(c=>c.id==="debt_family_home")' in html)
ok('order: family html placed before season/credit/debt html',
   # v20a30（Phase 4-7）拼合串更新：屋企卡後加 choice47Html 行動卡（鏈 G 第 4 拍），
   # 屋企卡仍然排喺季節／債權／其餘債卡之前，本斷言嘅語義不變，只同步新拼合串。
   'box.innerHTML=banner+famCardsHtml+choice47Html+cardHtml+creditHtml+debtHtml+emptyHtml;' in html)
ok('order: render builds card objects (data array untouched)', 'const debtCards=rows.map(d=>' in html)

# 唔好改嘅嘢：點名三級本體不變
ok('newspaperNameTier thresholds untouched', 'const PAPER_NAME_TIER_NAMED = 15;' in html and 'const PAPER_NAME_TIER_TITLED = 40;' in html)
ok('player ref stays 阿偉；全名只留標題畫面＋口徑註解（共 2 處）', '人氣新人阿偉' in html and html.count('陳偉翔') == 2)

# 慣例不變＋玩家面守則
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('softRev unchanged', 's111' in html)
echo_block = html.split('const FAMILY_ECHO_TOAST_MAIN')[1].split('function familyPaperEchoTick')[0] if 'const FAMILY_ECHO_TOAST_MAIN' in html else ''
ok('no real artist names in echo copy', all(x not in echo_block for x in ['張國榮','陳百強','梅艷芳','周潤發','劉德華']))
ok('echo copy does not use full name 陳偉翔', '陳偉翔' not in echo_block)

print('\nFAILED: ' + ' | '.join(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
