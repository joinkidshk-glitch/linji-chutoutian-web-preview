# v361 P1-A：通告庫編輯（roleScale 轉換＋新增 3 張擔正級通告）
# 用 raw text 定點替換，唔 reformat 全檔；改完 json.loads 驗證。
import json, re, sys

PATH = 'content/gigs_new.json'
raw = open(PATH, encoding='utf-8').read()
data = json.loads(raw)
gigs = {g['id']: g for g in data['gigs']}

CONVERT = [
    ('gig_1992_ad_107', 'ad_av', 'ad_lead'),
    ('gig_1992_ad_203', 'ad_av', 'ad_lead'),
    ('gig_1991_variety_103', 'variety_special', 'variety_host_lead'),
    ('gig_1992_variety_102', 'variety_special', 'variety_host_lead'),
    ('gig_1992_variety_106', 'variety_special', 'variety_host_lead'),
    ('gig_1990_rec_110', 'rec_album', 'music_lead'),
    ('gig_1990_rec_303', 'rec_album', 'music_lead'),
    ('gig_1991_rec_107', 'rec_album', 'music_lead'),
    ('gig_1991_rec_108', 'rec_album', 'music_lead'),
    ('gig_1992_rec_105', 'rec_album', 'music_lead'),
    ('gig_1992_rec_109', 'rec_album', 'music_lead'),
]

for gid, old, new in CONVERT:
    g = gigs[gid]
    assert g['roleScale'] == old, (gid, g['roleScale'])
    assert not g.get('resolvedScale'), (gid, g.get('resolvedScale'))
    # 定點替換：id 之後 800 字元內第一個 roleScale
    pat = re.compile(r'("id": "' + re.escape(gid) + r'".{0,800}?"roleScale": ")' + re.escape(old) + r'(")', re.S)
    raw, n = pat.subn(r'\g<1>' + new + r'\g<2>', raw, count=1)
    assert n == 1, (gid, n)
    print('converted', gid, old, '->', new)

NEW_GIGS = [
    {
        "id": "gig_1991_ad_109",
        "title": "《清涼一夏》廣告主角",
        "type": "廣告",
        "tier": "高級",
        "category": "作品",
        "genre": "電視廣告",
        "workTitle": "清涼一夏",
        "roleLabel": "廣告主角",
        "loc": "ad_central",
        "director": "廣告導演",
        "year": 1991,
        "season": "夏",
        "days": 2,
        "roleScale": "ad_lead",
        "req": {"acting": 70, "charm": 40},
        "hard": 0.6,
        "pay": [380, 460],
        "fame": [38, 55],
        "blurb": "恒昌電器夏季冷氣機電視廣告，你擔任廣告主角，在炎夏家居演繹清涼一夏的賣點。",
        "synopsis": "恒昌電器推出夏季冷氣機推廣，廣告在中環街頭與家居佈景拍攝。你飾演怕熱的年輕住客，回家開冷氣後由煩躁變成享受；蘇芷茵飾演同屋住客，彭少祺飾演電器店員，葉敏芝飾演鄰居。導演要求前後對比鮮明，表情轉換要自然。",
        "roleHint": "前半段要演得煩躁怕熱，開冷氣後放鬆享受，留意店員的提示節奏。",
        "posterBrief": "家居佈景內，男主角坐在冷氣機下享受涼風，女住客立於側旁，店員站在門口介紹，背景是夏日家居陳設，畫面清爽明亮。",
        "cast": {"leadM": None, "leadF": "so_jiyan", "supportM": "pang_siuki", "supportF": "yip_manji"},
        "product": "冷氣機",
        "productKind": "電器",
        "productGender": "N",
        "brand": "恒昌電器",
    },
    {
        "id": "gig_1991_ad_110",
        "title": "《穩健同行》廣告主角",
        "type": "廣告",
        "tier": "稀有",
        "category": "作品",
        "genre": "形象廣告",
        "workTitle": "穩健同行",
        "roleLabel": "廣告主角",
        "loc": "ad_adm",
        "director": "廣告導演",
        "year": 1991,
        "season": "秋",
        "days": 2,
        "roleScale": "ad_lead",
        "req": {"charm": 60, "stage": 55},
        "hard": 0.65,
        "pay": [520, 640],
        "fame": [45, 65],
        "blurb": "港城商業銀行形象廣告，你擔任廣告主角，演繹穩健同行的品牌形象。",
        "synopsis": "港城商業銀行推出形象廣告，在銀行大堂與維港海傍拍攝。你飾演年輕創業者，由街邊小店做到開分店，銀行職員一路陪伴；鍾楚凝飾演銀行經理，陸柏言飾演生意拍檔，藍若曦飾演顧客。導演要求沉穩可信，步伐與眼神要有分量。",
        "roleHint": "形象廣告要沉穩可信，步伐放慢，眼神望向遠方，留意經理的交接動作。",
        "posterBrief": "維港海傍，男主角站在銀行大堂門前，經理立於側旁，背景是維港海景與銀行招牌，畫面穩重明亮。",
        "cast": {"leadM": None, "leadF": "chung_choning", "supportM": "luk_baakyin", "supportF": "lan_ruoxi"},
        "product": "銀行形象宣傳",
        "productKind": "金融形象",
        "productGender": "N",
        "brand": "港城商業銀行",
    },
    {
        "id": "gig_1991_variety_110",
        "title": "《全港同心夜》慈善晚會主持",
        "type": "綜藝",
        "tier": "高級",
        "category": "作品",
        "genre": "晚會",
        "workTitle": "全港同心夜",
        "roleLabel": "慈善晚會主持",
        "loc": "tvb_longmen",
        "director": "晚會監製",
        "year": 1991,
        "season": "冬",
        "days": 3,
        "roleScale": "variety_host_lead",
        "req": {"stage": 65, "charm": 45},
        "hard": 0.62,
        "pay": [480, 580],
        "fame": [42, 62],
        "blurb": "星河電視台年度慈善晚會，你擔任慈善晚會主持，帶領全場為基層家庭籌款。",
        "synopsis": "星河電視台一年一度的慈善晚會《全港同心夜》，你擔任晚會主持，負責開場、拍賣環節與結尾大合唱。彭少祺、陸柏言與蘇芷茵擔任表演嘉賓。節目組要求主持熟讀流程，拍賣環節要帶動現場氣氛，留意監製的手勢調度。",
        "roleHint": "慈善晚會主持要帶動氣氛，拍賣環節節奏要快，留意監製的手勢。",
        "posterBrief": "慈善晚會舞台燈光溫暖，主持立於中央，嘉賓分立兩側，背景是慈善晚會佈景與現場觀眾席，氣氛熱鬧。",
        "host": None,
        "guests": ["pang_siuki", "luk_baakyin", "so_jiyan"],
        "segments": ["開場歌舞", "慈善拍賣", "大合唱"],
    },
]

for g in NEW_GIGS:
    assert g['id'] not in gigs, g['id']

# 插入新 gig：搵 gigs 陣列結尾（最後一個 gig 物件之後嘅 "\n  ]"）
insert = ',\n' + ',\n'.join(
    '    ' + json.dumps(g, ensure_ascii=False, indent=2).replace('\n', '\n    ')
    for g in NEW_GIGS
)
idx = raw.rfind('\n  ]')
assert idx > 0
raw = raw[:idx] + insert + raw[idx:]

# 驗證
data2 = json.loads(raw)
assert len(data2['gigs']) == 326, len(data2['gigs'])
gigs2 = {g['id']: g for g in data2['gigs']}
for gid, old, new in CONVERT:
    assert gigs2[gid]['roleScale'] == new, gid
for g in NEW_GIGS:
    assert gigs2[g['id']]['roleScale'] == g['roleScale']
ids = [g['id'] for g in data2['gigs']]
assert len(set(ids)) == 326

open(PATH, 'w', encoding='utf-8').write(raw)
print('OK: 326 gigs, conversions + 3 new gigs written')
