# v20a207 resync：index.html 淨 +34 行（C3 +12／cap +5／modal +1／closeModal +1／drawBase +7／spotlight +8；見 qa207/resync207.py，72 錨點對位零 mismatch，純漂移）。
# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），釘行按段 +4／+10 重算。
# -*- coding: utf-8 -*-
# v20a197 resync：index.html 淨 +94 行，全部錨點 difflib 對位核實純漂移（見 qa197/resync197.py）：25659→25714、26000→26055、26003→26058、26004→26059、26005→26060、26048→26103、26267→26322、27213→27268、27246→27301、31020→31075、31028→31083、31029→31084、31071→31126。（B4 補丁再 +9 行，見同檔。）
# v20a191 resync：index.html 淨 +47 行（CSS +2／StoryPlay head +7／其後 +38），13 個錨點按段 +2／+9 重算，內容逐字核實純漂移。
# v20a191 rebase 上 main b3db32f resync：v189 淨 +34 行＋v191 淨 +47 行，13 個錨點按段 +2／+9 重算，內容逐字核實純漂移。
# v20a151 靜態測試：關海媚名禁令退役——
#   (1) 4 個 banned-list 檢查唔再含「關海媚」（L25569 regex／L26112／L26160／L26380），
#       其餘禁令（陳淑芬／施南生／Ho哥／Ho 哥）全部留返；
#   (2) kwan_note check 退役（註解化，行數不變；L25909 註解唔再提「關海媚禁令」）；
#   v20a155 rebase 上 main 9346a8e resync：v155 淨 ＋17（B1 註解 ＋6／B2 註解 ＋7／B3 ＋4），全部錨點再 ＋17；v20a161 rebase 上 bf612bc ＋14（插入段新行 4793-4806，全部錨點再 ＋14，見 qa161/resolve_rebase161_v155.py）。（25744→25761、26081→26098、26129→26146、26349→26366、26084→26101、26085→26102、26086→26103、27290→27307、27323→27340、31037→31054、31045→31062、31046→31063、31088→31105）；內容逐行核實，純漂移。
#   (3) TEXTFIX55_PHRASES 嗰對 ["關海媚","當紅花旦"] 已拎走，其餘配對唔郁；
#   (4) TEXTFIX55_EXACT C13 條映射保留，只係 value 改返「關海媚提醒頭條係雙刃」，
#       其餘 live 修正（1991年冬→1990年冬、虛構娛樂周刊→娛樂週刊）原封不動；
#   (5) UI 顯示名：SP_SPEAKER_REG display＝「關海媚」、relMap rel_mei＝「關海媚」、
#       TEXTFIX55_NOTE_EXACT 兩句 outcome note 同樣改返真名；
#   (6) content JSON 四處 guanHaimeiUpgradeForbidden 已清，mvpDualHeroineProtected 留返；
#   (7) 唔郁嘅嘢：speaker registry、故事散文稱號句、12 星名冊規則、SAVE key／softRev／?v=。
# 反證：喺 pristine main (9c850f9) index 上行 → 多項 FAIL（唔 crash）。
# v151 落地 resync：v156（9c850f9）先落地，main 行號 +15（L733 插入 15 行），錨點由 e08a070 版 +15。
# v20a183 resync：v183 淨 ＋117 行（C7 CSS ＋2／prefKind ＋1／TryIntercept ＋1／PlayEncounter ＋2／ROM183 block ＋107／確認 modal ＋3／goBit ＋1；difflib 對位核實純漂移，見 qa183/resync183.py）。
# v20a196 resync：showResult 淨 −1 行，行號 ≥27974 者 −1（31020→31019、31028→31027、31029→31028、31071→31070），difflib 對位核實內容逐字相同，純漂移。
# v20a182 resync：v182 淨 ＋17 行（B1 CSS＋1／C1 CSS 淨＋1／請柬＋4／presentAwardInvite＋6／C1 JS＋5），十三錨點一律 ＋2（qa182/resync182.py difflib 對位核實純漂移；A8／B2–B5／C1／C3／C4／E1 嗰 7 粒 line() 釘喺第一輪 head -6 截斷睇漏，補核實後一併更新）。
# v20a160 M4 步 resync：walkup CSS 喺 L802 插入 5 行，全部錨點 ＋5（17 個錨點逐行核實，內容逐字相同，純漂移；其餘 M1／M6／M9 插入點全部喺 L44855 之後，唔影響本檔錨點）。
# v20a157 rebase 上 main 60b0a8f resync：splice 插入令錨點漂移（＜30831 者 ＋24、≥30831 者 ＋66；qa131/resync_rebase157.py difflib 對位核實：13 個錨點內容逐字相同，純漂移）。
# v20a149 rebase 上 main 6d08c7c（v171）resync：CSS ＋13，13 個錨點一律 ＋13（qa149/resync_rebase149.py difflib 對位核實內容逐字相同，純漂移）。
# v20a153 第三輪 rebase 上 main a500536（v149）resync：difflib 對位核實純漂移，code 行錨點按映射重寫（見 qa153/resync_rebase153c.py）。
# v20a172 rebase 上 main a500536（v149）resync：v149 淨 ＋97（CSS L778／L794 ＋8、L4457 ＋5、典禮區 ＋84），13 個錨點一律 ＋13（qa172/resync172b.py difflib 對位核實，內容逐字相同，純漂移）。
# v20a172 rebase 上 main e2add29（v174）resync：A 系列唔郁（＜27080）、C1／E1 ＋5、B／C3／C4／C5 ＋5（qa172/resync172c.py difflib 對位核實純漂移）。
# 用法：python3 tests/test_kwan151_static.py [path-to-index.html]
# v20a176 resync：NPCS ＋7 行（藍／徐／海媚條目，插入點 L6017 之後），全部錨點再 ＋7（qa176/resync176.py 逐行核實內容逐字相同，純漂移）。
# v20a181 resync：index.html 淨 ＋8（awards CSS ＋13／頒獎禮區淨 −26／尾段 ＋8）；13 個錨點一律 ＋13（difflib 對位核實內容逐字相同，純漂移）。
# v20a181 rebase 上 main 9640c6f（v183）resync：13 個錨點 ＋11（＜30523 者）／＋12（≥30523 者，ROM176／183 插入段之後），difflib 對位核實內容逐字相同，純漂移。
# v20a189 resync：index.html 淨 ＋34 行（accel-link CSS ＋15 @~1831／day-res 92dvh media ＋10 @~3235／hint 刪除 −10 @37990／soft map 掣 ＋3／accel link push ＋12／day-res class ＋4；difflib 對位核實純漂移，見 qa189/resync189.py）。
import io, json, os, sys

html_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'index.html')
root = os.path.dirname(os.path.abspath(html_path))
html = io.open(html_path, encoding='utf-8').read()
lines = html.split('\n')
fails = []
def ok(name, cond):
    if not cond: fails.append(name)
    print(('PASS ' if cond else 'FAIL ') + name)

def line(n):
    return lines[n - 1] if 1 <= n <= len(lines) else ''

# (1) banned-list 檢查：關海媚已清，其餘禁令留返
ok('A1 L25608 regex 冇關海媚', '關海媚' not in line(25739) and '/Ho\\s*哥|陳淑芬|施南生/' in line(25739))
ok('A2 L25949 list 冇關海媚', '關海媚' not in line(26080) and '["陳淑芬","施南生","Ho哥"]' in line(26080))
ok('A3 L25997 list 冇關海媚', '關海媚' not in line(26128) and '["陳淑芬","施南生","Ho哥","Ho 哥","nextHint"]' in line(26128))
ok('A4 L26216 list 冇關海媚', '關海媚' not in line(26347) and '["陳淑芬","施南生","Ho哥","Ho 哥"]' in line(26347))
ok('A5 其餘禁令仲喺度', all(w in html for w in ['陳淑芬', '施南生', 'Ho哥']))

# (2) kwan_note check 退役
ok('A6 kwan_note check 已註解', 'bad("kwan_note")' not in html and 'v151 退役' in line(26085))
ok('A7 L25952 註解唔留「關海媚禁令」字眼', '關海媚禁令' not in line(26083) and '雙女主改讀 devAppendix' in line(26083))
ok('A8 dual_note 唔郁', 'bad("dual_note")' in line(26084))
ok('A9 guanHaimeiUpgradeForbidden 全檔清零', 'guanHaimeiUpgradeForbidden' not in html)

# (3) TEXTFIX55_PHRASES
ok('B1 PHRASES 關海媚配對已拎走', '["關海媚", "當紅花旦"]' not in html)
ok('B2 PHRASES 其餘配對唔郁', '["星河電視城", "星河電視台"]' in line(31159) and '["送命題", "辣手問題"]' in line(31159))

# (4) TEXTFIX55_EXACT C13 映射：保留映射，只改 value
ok('B3 EXACT C13 value 有關海媚', '關海媚提醒頭條係雙刃' in line(31150))
ok('B4 EXACT C13 value 冇當紅花旦', '嗰位當紅花旦亦提過佢' not in line(31150))
ok('B5 EXACT 其餘修正原封不動', '1990年冬，娛樂週刊已經寫好緋聞草稿' in line(31150)
   and '1991年冬，虛構娛樂周刊已寫好緋聞草稿' in line(31150))

# (5) UI 顯示名
ok('C1 speaker display 改真名', 'kwan_hoimei: { artId:"char_kwan", portraitsKey:null, display:"關海媚" }' in line(27373))
ok('C2 唔再有稱號 display', 'display:"當紅花旦"' not in html)
ok('C3 relMap rel_mei 改真名', '["rel_mei","關海媚"]' in line(31201))
ok('C4 NOTE_EXACT 兩句改真名', '采兒同關海媚嗰邊都近咗啲' in line(31158) and '但采兒同關海媚嗰邊，都冷淡咗' in line(31158))
ok('C5 NOTE_EXACT 冇殘留稱號', '嗰位當紅花旦' not in line(31158))

# (6) content JSON flag
for rel in ['content/MOCK_STORY_DENG_LINE_MEET_SOFT_v1.1.json',
            'content/MOCK_STORY_DENG_LINE_MEET_SOFT_v1.json',
            'content/MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json']:
    p = os.path.join(root, rel)
    txt = io.open(p, encoding='utf-8').read()
    try:
        json.loads(txt); valid = True
    except Exception:
        valid = False
    ok('D1 %s JSON 有效＋flag 已清' % os.path.basename(rel),
       valid and 'guanHaimeiUpgradeForbidden' not in txt)
    ok('D2 %s mvpDualHeroineProtected 留返' % os.path.basename(rel),
       'mvpDualHeroineProtected' in txt)

# (7) 唔郁嘅嘢
ok('E1 speaker registry 留返', '"關海媚":"kwan_hoimei"' in line(27340))
ok('E2 故事散文稱號句唔郁', '嗰位當紅花旦向你微微點咗下頭' in html and '嗰位當紅花旦同你擦身而過' in html)
ok('E3 12 星名冊規則唔郁', '當紅花旦唔入名冊' in html)
ok('E4 台柱係指阿偉，唔郁', '成行都嗌你做台柱喇' in html)
ok('E5 SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in html and 's107' in html and 'v20a10' in html)

print('\n' + ('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS'))
sys.exit(1 if fails else 0)
