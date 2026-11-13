# -*- coding: utf-8 -*-
# v20a191：前置句改行共用幕號 storyActLabel（渲染字不變，見 test_story179_logic.js）；source 檢查跟新寫法。
# v20a179 STORY179 靜態測試：v172 review 唯一新項 C1（用戶已拍板）
#
# 鎖行嘅「（場景：X）」係一句無動詞嘅孤兒括號，隔籬四項全部係條件句，初睇要
# 諗一諗佢即係咩。修法：拎走括號，改做標籤式「場景：X」，同條件句分返開。
# 三種鎖行都要改齊（全部喺 prog71StubItems）：
#   C3 單地點鎖行：「（場景：X）」→「場景：X」
#   C4 OR 行：「或（場景：X）」→「或場景：X」
#   C5 多地點鎖行：同 C3 同一 lm 分支（raw「到 A 或 B 播」）
# 已開放行完整句式「返地圖嗰陣就會播出。（場景：X）」唔郁——v175 C1 已先刪
#   「已經開放——」四隻字（v153 review C1，用戶 2026-11-13 14:14 拍板；openBody
#   同行改，見 NOTES_V20A175 §1）。v179 嗰句「唔郁」指場景括號寫法＋句式
#   唔郁，唔包呢四隻字：兩版合併嗰陣呢個斷言要跟 v175 走（舊字串留返做
#   反向守衛：合併後樹唔可以再有「已經開放——返地圖嗰陣就會播出。」）。
#   見 NOTES_V20A175 §8（第二次 rebase 衝突處理）。
# 反證：喺 pristine main（v172，7801a72）上行會 FAIL（鎖行仲係括號寫法；
#   NOTES_V20A179.md 未有），唔會 crash。
# 用法：python3 tests/test_story179_static.py [path-to-index.html]
import re
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
repo_root = Path(__file__).resolve().parent.parent
try:
    notes = (repo_root / 'NOTES_V20A179.md').read_text(encoding='utf-8')
except Exception:
    notes = ''
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

def seg(a, b, span=6000):
    i = src.find(a)
    if i < 0: return ''
    j = src.find(b, i + len(a)) if b else -1
    return src[i:j] if j > i else src[i:i + span]

stub = seg('function prog71StubItems(id){', 'function prog71Rows(){', 4000)

# --- 一、C3／C5：單地點＋多地點鎖行改做標籤式 ---
ok('C1：鎖行單地點／多地點改做標籤式「場景：X」（拎走括號）',
   '"場景："+lm[1]' in stub and '"（場景："+lm[1]+"）"' not in stub)
ok('C1：鎖行成段冇括號寫法嘅 code 字面殘留（註解引用舊寫法唔計）',
   '"（場景：' not in stub and '（場景：$1）' not in stub)

# --- 二、C4：OR 行改做標籤式 ---
ok('C1：OR 行改做標籤式「或場景：X」（拎走括號）',
   '或場景：$1' in stub and '或（場景：$1）' not in stub)
# 「或到」原料本身唔郁（progressToward 照舊生產，攔截喺渲染層）——輸出層
# 「冇或到」由 logic test 斷言（真 prog71StubItems 跑出嚟嘅字串）。
ok('C1：OR 原料「或到」繼續由 progressToward 生產（渲染層攔截，唔改原料）',
   'orBits.push("或到"' in src)

# --- 三、已開放行完整句式唔郁（場景括號寫法＋「返地圖嗰陣就會播出。」句式；
#   「已經開放——」已由 v175 C1 刪走，見檔頭；呢度反向守衛埋，唔准返生） ---
ok('C1：已開放行「返地圖嗰陣就會播出。（場景：X）」唔變（v175 C1 已刪「已經開放——」）',
   '返地圖嗰陣就會播出。' in src
   and '已經開放——返地圖嗰陣就會播出。' not in src
   and '（場景：" + prog71Esc(r.locName) + "）' in src)
ok('C1：全檔只剩已開放行一處用「（場景：」括號寫法（code 字面計）',
   src.count('（場景："') == 1)

# --- 四、其餘條件句唔變（v172 C1 守衛照舊） ---
ok('C1：鎖行其餘條件句唔變（前置／週數／通告／聲望／季節）',
   '"先完成"+(storyActLabel(d)' in stub and '到第 ' in stub and '接通告 ' in stub
   and '要多於' in stub and '等到啱嘅季節' in stub)
ok('C1：傳聞提示「聽到傳聞」刻意保留', '聽到傳聞：' in stub)
ok('C1：鎖行舊觸發句繼續清零（去 X 先播到／就會觸發）',
   '先播到呢幕' not in stub and '就會觸發' not in stub)

# --- 五、NOTES 紀錄 ---
ok('NOTES：NOTES_V20A179.md 在位，寫明三種鎖行＋已開放行唔郁',
   notes != '' and '場景：' in notes and '已開放' in notes)

# --- 六、範圍守衛：唔郁嘅嘢 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
