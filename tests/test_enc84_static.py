# v20a84 ENC84 靜態測試：巧遇 Phase 3 四星註冊字串、樞紐/凍結/解鎖過濾接線喺 index.html 在位；
# 紅線：ENC84 兩段（對話數據＋模組）內冇真藝人名、冇關海媚、冇 1989 指向、冇系統字眼；
# NOTES 文件在位。反證：v83 index 冇呢啲標記 → FAIL。
import io, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('softRev 冇變', "s107" in html)
ok('產品 ?v= 冇變', 'v20a10' in html)
ok('NOTES_V20A84 文件在位', os.path.exists(os.path.join(ROOT, 'NOTES_V20A84_ENCOUNTER_P3.md')))

P3 = ['pang_siuki','so_jiyan','chung_choning','ching_tinlok']
ok('四星對話數據 const 在位', all(('const ENC84_DLG_' + s + ' =') in html and ('const ENC84_FRAME_' + s + ' =') in html for s in P3))
ok('四星名冊字面在註冊模組', all(('ENC84_DLG_' + s) in html[html.index('v20a84 ENC84：紅星巧遇 Phase 3'):] for s in P3))
ok('四星註冊入 ENC79_DIALOG', all(('ENC79_DIALOG.' + s + ' = ENC84_DLG_' + s) in html for s in P3))
ok('四星節拍表註冊', all(('ENC79_BEATS.' + s + ' = [') in html for s in P3))
ok('ENC84 模組標記在位', 'v20a84 ENC84：紅星巧遇 Phase 3' in html and 'ENC84 模組完' in html)
ok('T4 提攜四星債權 id', all(('credit_enc84_' + s.split('_')[0] + '_patron') in html for s in P3))
ok('彭慈善債權 id', 'credit_enc84_pang_charity' in html)
ok('傳聞卡 id 齊（情報×3／F 伏筆／告別／程預知／蘇緋聞）', all(x in html for x in ['rumor_pang_show_tip','rumor_so_ad_tip','rumor_chung_director_tip','rumor_chung_canada_heard','rumor_chung_advice','rumor_ching_rehearse','rumor_so_gossip_risk']))
ok('樞紐標記在位（enc84Hub）', 'enc84Hub' in html)
ok('蘇收斂凍結：旗設定＋攔截過濾', 'enc84_so_cool_until' in html and html.count('enc84_so_cool_until') >= 2)
ok('未解鎖星過濾（漏料／茶餐廳／事務所共 3 處 unlockYear）', html.count('s.unlockYear') >= 3)
ok('程 E4 節拍用 enc83NewsOut("E4")', 'enc83NewsOut("E4")' in html)
ok('程 C16 旗回收（flag_vocal_train/polish）', 'flag_vocal_train' in html and 'flag_vocal_polish' in html)
ok('鍾告別窗 gate（1992 秋／冬＋1992）', 'chung_farewell' in html and 'ys.year===1992 && (ys.season==="秋" || ys.season==="冬")' in html)
ok('fx key 在位（pang_helped/so_cool/so_risk_news）', all(x in html for x in ['pang_helped','so_cool','so_risk_news']))

# 紅線：掃 ENC84 兩段——數據段（玩家面對白）＋模組段；系統字眼只驗數據段
# （模組段係程式碼，enc79TierOf 等識別字同 DEV 註解唔算玩家面文字）
i1 = html.index('v20a84 ENC84 對話數據')
i2 = html.index('/* ===== v20a79 ENC79：紅星巧遇系統 Phase 1')
j1 = html.index('v20a84 ENC84：紅星巧遇 Phase 3')
j2 = html.index('/* ===== ENC84 模組完 ===== */')
data_seg = html[i1:i2]
seg = data_seg + html[j1:j2]
REAL_NAMES = ['劉德華','周潤發','張國榮','梅艷芳','王祖賢','林青霞','周星馳','成龍','李連杰','梁朝偉','張曼玉','鍾楚紅','關之琳','劉嘉玲','黎明','郭富城','張學友','陳百強','譚詠麟','林子祥','鄭裕玲','汪明荃','肥姐','沈殿霞']
ok('紅線：ENC84 段冇真藝人名', not any(n in seg for n in REAL_NAMES))
ok('紅線：ENC84 段冇關海媚', '關海媚' not in seg)
ok('紅線：ENC84 段冇 1989 指向', '1989' not in seg and '一九八九' not in seg)
ok('紅線：對白數據段冇系統字眼（好感度/解鎖）', all(w not in data_seg for w in ['好感度', '解鎖']))

print('\n' + ('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS'))
sys.exit(1 if fails else 0)
