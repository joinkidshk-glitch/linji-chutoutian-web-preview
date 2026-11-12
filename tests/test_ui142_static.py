# -*- coding: utf-8 -*-
# v20a142 靜態守門測試：A1 老闆 bust 髮頂被切（#app 捲動拖郁 #mask）＋
# A2 空狀態死位（進度頁星途寄語／作品牆空畫框）＋B1 地圖標籤壓紋底（4 張錨微調）。
# 反證：喺 pristine main（bcac846）index 上行 → A1／A2／B1 新寫法全部唔在 → 乾淨 FAIL。
# 用法：python3 tests/test_ui142_static.py [path-to-index.html]
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in html and 's107' in html and 'v20a10' in html)

# --- A1：modal() 歸零＋focus 唔捲；英雄區 240px／名牌唔郁 ---
m = re.search(r'function modal\(html, buttons, opts\)\{(.*?)\nfunction closeModal\(\)', html, re.S)
ok('modal() 存在', m is not None)
modal_body = m.group(1) if m else ''
ok('A1 modal() 開 modal 歸零 #app.scrollTop', "getElementById(\"app\").scrollTop=0" in modal_body or 'getElementById("app"); if(_app142) _app142.scrollTop=0' in modal_body)
ok('A1 modal() 開 modal 歸零 #modal-inner.scrollTop', '_mi142.scrollTop=0' in modal_body)
ok('A1 modal() focus 用 preventScroll', 'focus({preventScroll:true})' in modal_body)
ok('A1 modal() focus 後再歸零 #app.scrollTop 兜底', modal_body.count('scrollTop=0') >= 3)
ok('A1 英雄區高度 240px 唔郁（v132 定案）', 'height:240px' in html)
ok('A1 名牌 bottom:106px 唔郁', '.cn-issuer-cap30v2{ position:absolute; left:12px; bottom:106px;' in html)
ok('A1 英雄區負 margin -100px 唔郁', 'margin-bottom:-100px' in html)

# --- A2a：進度頁星途寄語 ---
ok('A2a renderProgress71 有星途寄語填補區塊', 'prog71-next142' in html)
ok('A2a 填補區塊有未完成口吻', '都係之後嗰幕嘅伏線' in html)
ok('A2a 填補區塊有行晒口吻', '十七幕行晒' in html)
ok('A2a 填補區塊 CSS 存在', '.prog71-next142{' in html)
ok('A2a 填補區塊係虛線框（唔係實色佔位卡）', 'border:1px dashed' in html and '.prog71-next142' in html)
ok('A2a 進度頁遠幕合併卡原文唔郁', '完成前面幕數後逐幕揭曉' in html)

# --- A2b：作品牆空畫框；兩段機制說明一字唔郁 ---
OLD_P = '仲未有作品入牆。有作品圖嘅製作，殺青之後，佢嘅作品圖就會黐喺呢面牆度；冇海報嘅製作（例如電視特輯），完成咗只會記入拍攝簿，唔會上牆。由臨記做到主角，成幅牆就係你嘅履歷。'
ok('A2b 作品牆空狀態原文一字唔郁', OLD_P in html)
ok('A2b 空狀態有示意畫框容器', 'works-frames142' in html)
ok('A2b 示意畫框係 3 個', html.count('class="works-frame142"') == 3)
ok('A2b 示意畫框有「黐喺呢度」一句', '完成作品後，佢嘅作品圖會黐喺呢度' in html)
ok('A2b 畫框 CSS 存在（虛線金框＋3/4 比例）', '.works-frames142{' in html and 'aspect-ratio:3/4' in html)
ok('A2b 空畫框只喺空狀態出現（有作品嗰陣唔出）', 'worksWallHtml59' in html and 'works-frames142' in html.split('worksWallHtml59')[1][:1500])

# --- B1：4 張錨新值；其餘 11 張唔郁；LOCS 熱區座標唔郁 ---
def mn(name):
    mm = re.search(r'<div class="mn68" style="([^"]*)">' + re.escape(name) + r'</div>', html)
    return mm.group(1) if mm else None
ok('B1 香江唱片錨＝29.2%／24% +31px', mn('香江唱片') == 'left:29.2%;top:calc(24% + 31px)')
ok('B1 廟街禮品錨＝28.4%／35% -104px', mn('廟街禮品') == 'left:28.4%;top:calc(35% - 104px)')
ok('B1 海港廣播錨＝88%／15% -44px', mn('海港廣播') == 'left:88%;top:calc(15% - 44px)')
ok('B1 金龍茶餐廳錨＝16%／16% -56px', mn('金龍茶餐廳') == 'left:16%;top:calc(16% - 56px)')
UNCHANGED = {
    '獅子山製片': 'left:54%;top:calc(12% - 52px)',
    '星河電視台': 'left:26%;top:2%',
    '九龍電視台': 'left:36%;top:calc(45% - 52px)',
    '紅棉影業': 'left:74%;top:calc(11% - 44px)',
    '維港電影': 'left:80%;top:calc(18% + 38px)',
    '中環廣告': 'left:60%;top:calc(57% + 30px)',
    '金鐘創意': 'left:85%;top:calc(60% + 28px)',
    '灣仔唱片': 'left:68%;top:calc(77% + 34px)',
    '天星音樂': 'left:86%;top:calc(82% + 30px)',
    '何生事務所': 'left:15%;top:calc(86% - 20px)',
    '仁康醫院': 'left:43%;top:calc(73% + 52px)',
}
for name, want in UNCHANGED.items():
    ok('B1 其餘標籤唔郁：' + name, mn(name) == want)
ok('B1 LOCS rec_hk 熱區座標唔郁', 'id:"rec_hk"' in html and 'x:30, y:24' in html)
ok('B1 LOCS tvb_harbour 熱區座標唔郁', 'x:90, y:15' in html)
ok('B1 LOCS cafe_cha 熱區座標唔郁', 'x:15, y:16' in html)
ok('B1 LOCS gift_shop 熱區座標唔郁', 'x:43, y:35' in html)

print('TOTAL ' + ('PASS' if not fails else 'FAIL %d' % len(fails)))
sys.exit(1 if fails else 0)
