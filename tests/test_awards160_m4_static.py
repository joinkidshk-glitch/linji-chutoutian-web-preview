# v20a181：M4 walkup GIF 退役 static tests（原 v20a160-m4 檔成份改寫）。
# v181 起行上台改由 canvas 畫：walkup beat 內阿偉用 PixelLab east 幀由台左行到中央（1400ms 行完），
# 再換燕尾服企定捧杯；M4 修好版 GIF（assets/fx/awd_walkup_m4.gif）＋DOM overlay 層
# .awd62-walkup160＋syncWalkup 一併撤走。walkup beat 本身（2200ms、caption ""、只限 won、
# reveal 之後）唔郁；文案改由 draw() walkup 分支 setCaption。詳細見 tests/test_awards181_static.py。
# 反證：run against pristine main 91f264a -> 「已撤」斷言全部 FAIL（GIF／overlay／syncWalkup 仲在），
#   beats 守衛 pristine 應 PASS。
import sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'index.html')
src = open(idx_path, encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def slice_fn(name):
    i = src.find('function ' + name + '(')
    if i < 0: return ''
    depth = 0
    j = src.find('{', i)
    for k in range(j, len(src)):
        if src[k] == '{': depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0: return src[i:k+1]
    return ''

GIF_REL = 'assets/fx/awd_walkup_m4.gif'
GIF_PATH = os.path.join(ROOT, GIF_REL)
beats_fn = slice_fn('awards62CeremonyBeats')
play_fn = slice_fn('awards62PlayCeremony')

# --- M4 GIF 退役 ---
chk('修好版 GIF 已刪（assets/fx/awd_walkup_m4.gif 唔存在）', not os.path.isfile(GIF_PATH))
chk('index.html 唔再引用 GIF 檔名', GIF_REL not in src)
chk('原版檔名繼續唔喺度', 'm4_walkup.gif' not in src)
chk('walkup overlay CSS 已撤', '.awd62-walkup160' not in src)
chk('walkup overlay HTML 已撤（walkupHtml 消失）', 'walkupHtml' not in play_fn)
chk('syncWalkup 已撤（定義＋呼叫齊消失）', 'syncWalkup' not in play_fn)

# --- walkup beat 本身唔郁 ---
chk('beats：walkup 2200ms', 'id: "walkup", ms: 2200' in beats_fn)
# v20a208：beats 分兩條分支（多格夜＋舊單格 fallback），walkup push 各一處，兩處都喺 won guard 入面
# （多格：if(nc.isFocus && best === "won")；舊單格：if(best === "won")）；「只限 won」意圖不變。
chk('beats：walkup 只限 won 分支', 'if(nc.isFocus && best === "won") beats.push({ id: "walkup"' in beats_fn and 'if(best === "won")' in beats_fn)
chk('beats：walkup 喺 reveal 之後', beats_fn.find('id: "walkup"') > beats_fn.find('id: "reveal"'))
chk('beats：walkup beat caption 係空（文案改由 draw() setCaption）', 'id: "walkup", ms: 2200, caption: ""' in beats_fn)
chk('beats：gallery／nominated 唔行 walkup（walkup 喺 won guard 入面，兩處 push 都係 won 條件）',
    beats_fn.count('id: "walkup"') == 2)

# --- walkup 改由 canvas 畫（px east 幀） ---
chk('play：draw 有 walkup case', 'id === "walkup"' in play_fn)
chk('play：walkup 用 px east 幀行入場', 'frame: "east"' in play_fn)
chk('play：walkup 1400ms 行完（由台左 -40 行到中央）', 'beatElapsed / 1400' in play_fn)
chk('play：walkup 行完換燕尾服捧杯', 'tuxedo: true' in play_fn and 'drawTrophyGlyph(targetX, FLOOR - 129)' in play_fn) # v20a187 C6 resync：舊 −112；v20a207 B2：−110→−129
chk('play：walkup 文案經 setCaption（唔喺 beat caption，免同台下字幕重複）', 'setCaption("阿偉行上台，接過獎盃，高高舉起。")' in play_fn)

# --- 硬規則冇郁 ---
chk('SAVE key 冇郁', 'starVolunteer_map_v19w' in src)
chk('softRev 冇郁', 's107' in src)

if fails:
    print('FAILURES: %d' % len(fails))
    sys.exit(1)
print('ALL PASS')
