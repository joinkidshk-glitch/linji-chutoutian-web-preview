# v20a160 M9 頒獎禮贏分支音效 static tests：
# (1) 資產：take 1 fanfare（用戶 2026-11-13 07:15 試聽揀咗）＋掌聲 MP3（WAV 557KB 轉 MP3 慳位）入咗
#     assets/audio/；take 2 唔准入 repo（檔名／sha／字串三重堵）。
# (2) helper：awards160PlayWinAudio 典禮專用、最小——按需要先建 Audio 元素；play() 一律
#     .catch 靜默吞（自動播放政策拒絕唔可以令典禮停低）；跟 prefs 靜音（fanfare↔bgmMuted、
#     掌聲↔sfxMuted；設定頁嗰行而家未開掣，預設 false）。
# (3) 觸發：只喺 awards62PlayCeremony 嘅 advance() 入面、reveal beat＋best==="won" 嗰行呼叫
#     一次；全檔 new Audio 只得一個（helper 入面），冇其他地方播音。
# (4) 時序：fanfare 揭曉嗰刻起，掌聲 900ms 後疊上去。
# (5) 硬規則：SAVE key／softRev／?v= 一律唔郁。
# 反證：run against pristine main (e08a070) index -> 資產＋helper＋觸發全部缺 -> FAIL。
import sys, os, hashlib, re

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
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

FANFARE_SHA256 = '442b2676a15606177ddda4c42e5ccc6ce85938a57abff4bec13d74e7cbdfb040'
FANFARE_SIZE = 462979
TAKE2_SHA256 = '25e691cff4365f82b24a93b0d03aa5c11c723e1f4389bba169bcce7c327a168c'

# --- (1) 資產本體 ---
fan_path = os.path.join('assets', 'audio', 'awards_fanfare.mp3')
app_path = os.path.join('assets', 'audio', 'awards_applause.mp3')
chk('fanfare 入咗 assets/audio/awards_fanfare.mp3', os.path.isfile(fan_path))
fan_sha = ''
if os.path.isfile(fan_path):
    fan_sha = hashlib.sha256(open(fan_path, 'rb').read()).hexdigest()
    chk('fanfare 係 take 1（sha256 吻合）', fan_sha == FANFARE_SHA256)
    chk('fanfare 大細 462979 bytes（原檔，冇重編）', os.path.getsize(fan_path) == FANFARE_SIZE)
else:
    chk('fanfare 係 take 1（sha256 吻合）', False)
    chk('fanfare 大細 462979 bytes（原檔，冇重編）', False)
chk('fanfare 唔係 take 2（sha256 唔同）', fan_sha != TAKE2_SHA256)
chk('掌聲入咗 assets/audio/awards_applause.mp3', os.path.isfile(app_path))
if os.path.isfile(app_path):
    head = open(app_path, 'rb').read(4)
    chk('掌聲係 MP3（ID3／幀同步頭，唔係 WAV）', head[:3] == b'ID3' or (len(head) >= 2 and head[0] == 0xFF and (head[1] & 0xE0) == 0xE0))
    chk('掌聲唔係 WAV 原檔（頭 4 bytes 唔係 RIFF）', head != b'RIFF')
    sz = os.path.getsize(app_path)
    chk('掌聲 MP3 細過 200KB（WAV 557KB 已轉換慳位）', 10000 < sz < 200 * 1024)
else:
    chk('掌聲係 MP3（ID3／幀同步頭，唔係 WAV）', False)
    chk('掌聲唔係 WAV 原檔（頭 4 bytes 唔係 RIFF）', False)
    chk('掌聲 MP3 細過 200KB（WAV 557KB 已轉換慳位）', False)
# take 2 三重堵：repo 入面冇 take2 檔、index.html 冇 take2 字串、fanfare sha 唔係 take2（上面已驗）
take2_files = []
for root, _dirs, files in os.walk('assets'):
    for f in files:
        if 'take2' in f:
            take2_files.append(os.path.join(root, f))
chk('assets/ 入面冇任何 take2 檔案', take2_files == [])
chk('index.html 冇 take2 字串', 'take2' not in src)

# --- (2) helper ---
helper = slice_fn('awards160PlayWinAudio')
chk('helper awards160PlayWinAudio 在位', helper != '')
chk('fanfare 路徑常數指去 assets/audio/awards_fanfare.mp3', 'const AWARDS160_FANFARE_SRC = "assets/audio/awards_fanfare.mp3"' in src)
chk('掌聲路徑常數指去 assets/audio/awards_applause.mp3', 'const AWARDS160_APPLAUSE_SRC = "assets/audio/awards_applause.mp3"' in src)
chk('helper 用 new Audio 按需要建元素', 'new Audio(' in helper)
chk('helper play() 有 .catch 兜底（自動播放拒絕靜默吞）', '.catch(' in helper)
chk('helper 跟 prefs 靜音（bgmMuted／sfxMuted）', 'bgmMuted' in helper and 'sfxMuted' in helper)
chk('helper 讀 prefs 音量（volume）', 'p.volume' in helper)
chk('掌聲延遲常數 900ms', 'const AWARDS160_APPLAUSE_DELAY_MS = 900' in src)
chk('helper 用 900ms 延遲疊掌聲', 'AWARDS160_APPLAUSE_DELAY_MS' in helper)
chk('helper 有 QA 旗標 window.__awards160Audio', '__awards160Audio' in helper)

# --- (3) 觸發：只此一處 ---
chk('helper 全檔只定義一次', src.count('function awards160PlayWinAudio(') == 1)
chk('helper 全檔只呼叫一次（advance 嗰行）', src.count('awards160PlayWinAudio();') == 1)
play_fn = slice_fn('awards62PlayCeremony')
chk('呼叫位喺 awards62PlayCeremony 入面', 'awards160PlayWinAudio();' in play_fn)
call_lines = [ln for ln in src.split('\n') if 'awards160PlayWinAudio();' in ln]
chk('呼叫行係 reveal＋won 條件（同 spawnConfetti 一行）',
    len(call_lines) == 1 and 'beats[beatIdx].id === "reveal" && best === "won"' in call_lines[0]
    and 'spawnConfetti()' in call_lines[0])
chk('呼叫包喺 try/catch 入面（唔可以拖垮典禮）', len(call_lines) == 1 and 'try{ awards160PlayWinAudio(); }catch' in call_lines[0])
chk('全檔 new Audio 只得一個（helper 獨家）', src.count('new Audio(') == 1)
chk('new Audio 嗰個喺 helper 入面', 'new Audio(' in helper)
chk('兩條音源常數各只用一次（helper 內）', src.count('AWARDS160_FANFARE_SRC') == 2 and src.count('AWARDS160_APPLAUSE_SRC') == 2)
m9_block_i = src.find('/* v20a160 M9')
m9_block = src[m9_block_i:src.find('function awards62PlayCeremony')] if m9_block_i >= 0 else ''
chk('QA 旗標只喺 M9 註解＋helper 區塊出現',
    src.count('__awards160Audio') == m9_block.count('__awards160Audio') and src.count('__awards160Audio') == 4)
chk('冇其他 awards160 呼叫點（定義＋呼叫共 2 次）', src.count('awards160PlayWinAudio') == 2)

# --- (4) 時序註解在位（規格寫死喺 code 註解，唔係齋口頭） ---
chk('註解寫明 fanfare 揭曉起、掌聲 900ms 後疊', '掌聲 900ms 後疊上去' in src)

# --- (5) 硬規則 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('softRev s107 不變', 'var SOFT_REV = "s107"' in src)
chk('產品 ?v= v20a10 不變', 'version:"v20a10"' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
