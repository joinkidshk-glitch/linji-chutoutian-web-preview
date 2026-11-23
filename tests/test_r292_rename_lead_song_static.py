# -*- coding: utf-8 -*-
# v20a292 Q4 兩張《主打歌》唱片通告改名：靜態測試（只讀 content/gigs_new.json）——
#   rec_108 →《只差一步》MV 男主角、rec_111 →《銅鑼灣》MV 男主角；兩名唔同；
#   全庫再無 workTitle「主打歌」；其餘欄位（singer／pay／tier／season／year／req）不變；
#   新 workTitle 各自只出現一次；blurb／synopsis 跟新名。
# 用法：python3 tests/test_r292_rename_lead_song_static.py [path-to-repo-root]
import json
import sys
from pathlib import Path
root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
gigs = json.loads((root / 'content' / 'gigs_new.json').read_text(encoding='utf-8'))['gigs']
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

by_id = {g['id']: g for g in gigs}
g108 = by_id.get('gig_1992_rec_108')
g111 = by_id.get('gig_1992_rec_111')

ok('rec_108 title 係《只差一步》MV 男主角', bool(g108) and g108['title'] == '《只差一步》MV 男主角')
ok('rec_108 workTitle 係只差一步', bool(g108) and g108['workTitle'] == '只差一步')
ok('rec_111 title 係《銅鑼灣》MV 男主角', bool(g111) and g111['title'] == '《銅鑼灣》MV 男主角')
ok('rec_111 workTitle 係銅鑼灣', bool(g111) and g111['workTitle'] == '銅鑼灣')
ok('兩張 title 唔同', bool(g108 and g111) and g108['title'] != g111['title'])
ok('全庫再無 workTitle 係「主打歌」', all(g.get('workTitle') != '主打歌' for g in gigs))
ok('只差一步喺全庫只出現一次', sum(1 for g in gigs if g.get('workTitle') == '只差一步') == 1)
ok('銅鑼灣喺全庫只出現一次', sum(1 for g in gigs if g.get('workTitle') == '銅鑼灣') == 1)

def same_fields(g, season):
    return (bool(g) and g.get('singer') == 'luk_baakyin' and g.get('singerGender') == 'M'
            and g.get('pay') == [840, 1008] and g.get('tier') == '高級'  # v390：片酬 ×1.4（600,720 → 840,1008）
            and g.get('year') == 1992 and g.get('season') == season
            and g.get('req') == {'acting': 85, 'stage': 65, 'vocal': 55}
            and g.get('genre') == '情歌' and g.get('format') == 'MTV' and g.get('days') == 3
            and g.get('fame') == [42, 60] and g.get('type') == '唱片通告'
            and g.get('category') == '作品' and g.get('loc') == 'rec_star'
            and g.get('storyKeys') == ['N14'])
ok('rec_108 其餘欄位不變', same_fields(g108, '秋'))
ok('rec_111 其餘欄位不變', same_fields(g111, '春'))
ok('rec_111 trigger 照舊（駱家聲人情）', bool(g111) and g111.get('trigger') == {
    'kind': 'credit', 'creditId': 'credit_enc83_lok_patron', 'creditOwner': '駱家聲'})
ok('rec_108 blurb／synopsis 提《只差一步》、唔提《主打歌》',
   bool(g108) and '《只差一步》' in g108['blurb'] and '《只差一步》' in g108['synopsis']
   and '主打歌' not in g108['blurb'] and '主打歌' not in g108['synopsis'])
ok('rec_111 blurb 提《銅鑼灣》、唔提《主打歌》',
   bool(g111) and '《銅鑼灣》' in g111['blurb'] and '主打歌' not in g111['blurb'])
ok('全庫 workTitle「主打歌」清零後，剩低「主打歌」字眼只係 rec_109 synopsis 通用詞',
   sum(1 for g in gigs if '主打歌' in json.dumps(g, ensure_ascii=False)) == 1)

if fails:
    print('FAILURES: ' + ' | '.join(fails))
    sys.exit(1)
print('ALL PASS')
