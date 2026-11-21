# v20a207 resync：index.html 淨 +34 行（見 qa207/resync207.py，73 錨點對位零 mismatch，純漂移）。
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
ok('A2a 填補區塊有未完成口吻', '都是之後那幕的伏線' in html)
ok('A2a 填補區塊有走完口吻', '十七幕走完了' in html)
ok('A2a 填補區塊 CSS 存在', '.prog71-next142{' in html)
ok('A2a 填補區塊係虛線框（唔係實色佔位卡）', 'border:1px dashed' in html and '.prog71-next142' in html)
ok('A2a 進度頁遠幕合併卡原文唔郁', '完成前面幕數後逐幕揭曉' in html)

# --- A2b：作品牆空畫框；兩段機制說明一字唔郁 ---
OLD_P = '還未有作品入牆。有作品圖的製作，殺青之後，它的作品圖就會黐在這面牆上；沒有海報的製作（例如電視特輯），完成了只會記入拍攝簿，不會上牆。由臨記做到主角，整幅牆就是阿偉的履歷。'
ok('A2b 作品牆空狀態文案（RW-5 書面語）', OLD_P in html)
ok('A2b 空狀態有示意畫框容器', 'works-frames142' in html)
ok('A2b 示意畫框係 3 個', html.count('class="works-frame142"') == 3)
ok('A2b 示意畫框有「黐在這裡」一句', '完成作品後，它的作品圖會黐在這裡' in html)
ok('A2b 畫框 CSS 存在（虛線金框＋3/4 比例）', '.works-frames142{' in html and 'aspect-ratio:3/4' in html)
ok('A2b 空畫框只喺空狀態出現（有作品嗰陣唔出）', 'worksWallHtml59' in html and 'works-frames142' in html.split('worksWallHtml59')[1][:1500])

# --- B1：5 張錨新值；其餘 10 張唔郁；LOCS 熱區座標唔郁（v20a207 C5：中環廣告 60%→51%，避開藍塔） ---
def mn(name):
    mm = re.search(r'<div class="mn68[^"]*" style="([^"]*)">' + re.escape(name) + r'</div>', html)  # v20a373：容許額外 class（mn68-ask373 副註）
    return mm.group(1) if mm else None
ok('B1 香江唱片錨＝40%／40% +34px（v366）', mn('香江唱片') == 'left:40%;top:calc(40% + 34px)')
ok('B1 廟街禮品錨＝24%／16% -52px（v366）', mn('廟街禮品') == 'left:24%;top:calc(16% - 52px)')
ok('B1 海港廣播錨＝51%／37% -52px（v366）', mn('海港廣播') == 'left:51%;top:calc(37% - 52px)')
ok('B1 金龍茶餐廳錨＝29%／27% +34px（v366）', mn('金龍茶餐廳') == 'left:29%;top:calc(27% + 34px)')
ok('B1 中環廣告錨＝40%／63% +30px（v366 新圖對位）', mn('中環廣告') == 'left:40%;top:calc(63% + 30px)')
UNCHANGED = {
    # v366：換 v10 新圖後全部標籤按新圖金邊建築重對（見 NOTES_V20A366）
    '獅子山製片': 'left:56%;top:calc(19% - 52px)',
    '星河電視台': 'left:23%;top:calc(34% - 44px)',
    '九龍電視台': 'left:42%;top:calc(30% - 52px)',
    '紅棉影業': 'left:70%;top:calc(17% + 34px)',
    '維港電影': 'left:10%;top:calc(81% - 52px)',
    '金鐘創意': 'left:17%;top:calc(89% + 34px)',
    '灣仔唱片': 'left:56%;top:calc(83% + 34px)',
    '天星音樂': 'left:70%;top:calc(81% - 52px)',
    '何生事務所': 'left:29%;top:calc(84% - 52px)',
    '仁康醫院': 'left:86%;top:calc(78% + 34px)',
}
for name, want in UNCHANGED.items():
    ok('B1 其餘標籤（v364 對位）：' + name, mn(name) == want)
ok('B1 LOCS rec_hk 熱區座標（v366）', 'id:"rec_hk"' in html and 'x:40, y:40' in html)
ok('B1 LOCS tvb_harbour 熱區座標（v366）', 'x:51, y:37' in html)
ok('B1 LOCS cafe_cha 熱區座標（v366）', 'x:29, y:27' in html)
ok('B1 LOCS gift_shop 熱區座標（v366）', 'x:24, y:16' in html)

print('TOTAL ' + ('PASS' if not fails else 'FAIL %d' % len(fails)))
sys.exit(1 if fails else 0)
