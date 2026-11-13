# -*- coding: utf-8 -*-
# v20a172 STORY172 靜態測試：v165 review B1＋C1 修復（用戶 2026-11-13 12:33 拍板修晒）
#
# B1(a) 耐久記錄——驗強制播必須行 LIVE 模式（無 ?softPreview=1）：
#   softPreview 之下，強制播（story165TryForcedPlay 經 StoryPlay.start）喺 v165 嗰陣
#   會俾 soft stepLoc 擋住（地圖上 atLoc=null）；v172 起 code 上已修（見 B1(b)），
#   但 review／QA 慣例仍然係：soft 模式只驗文案／靜態，唔可以作強制播 pass/fail
#   依據——強制播 pass/fail 一律以 live 模式實駕為準。呢條規則寫喺 NOTES_V20A172.md
#   §2（本測試斷言佢在位），唔好淨係放喺對話。
# B1(b) start() 帶 ignoreSheetLoc 評估結論：可行，已改（見 NOTES §3）。
#   鏈已經全程打通，只差 StoryPlay.start 嗰一格唔傳 opts——stepLoc／stepFavor
#   早已識 opts.ignoreSheetLoc；evalNode soft 支路原樣轉交 opts；選幕嗰陣
#   listOpen 已經用 ignoreSheetLoc。改法係 opt-in：只有 story165TryForcedPlay
#   傳 { ignoreSheetLoc:true }；其餘 start() call sites 唔傳，行為同以前完全一樣；
#   普通玩家路徑（掣／autoPushC1IfNeeded）soft 閘原封不動。
# C1：進度頁鎖行「去 X 先播到呢幕」改做場景資料 framing「（場景：X）」，
#   同已開放行同一寫法；OR 條件入面嘅「或到 X」一併改做「或（場景：X）」。
#   傳聞提示「（去金龍茶餐廳打聽）」刻意保留——佢講嘅係點滿足「聽到傳聞」呢個
#   條件（要去邊度打聽），唔係講去邊度觸發呢幕；v20a34 P0-3 刻意將兩者分開寫。
# 反證：喺 pristine main（v171，6d08c7c）上行會 FAIL（鎖行仲係舊觸發句；
#   story165TryForcedPlay 仲係無 opts 嘅普通 start；NOTES_V20A172.md 未有）。
# 用法：python3 tests/test_story172_static.py [path-to-index.html]
import re
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
repo_root = Path(__file__).resolve().parent.parent
try:
    notes = (repo_root / 'NOTES_V20A172.md').read_text(encoding='utf-8')
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

# --- 一、C1：鎖行「去 X 先播到呢幕」清零，改做場景資料 framing ---
stub = seg('function prog71StubItems(id){', 'function prog71Rows(){', 4000)
ok('C1：鎖行舊觸發句「去 X 先播到呢幕」全檔清零',
   '"去"+lm[1]+"先播到呢幕"' not in src and '先播到呢幕' not in src)
ok('C1：「到 X 播」改做場景資料「（場景：X）」（同已開放行同一寫法）',
   '"（場景："+lm[1]+"）"' in stub)
ok('C1：已開放行「（場景：X）」寫法唔變（鎖行同佢對齊，唔係另創新寫法）',
   '（場景：" + prog71Esc(r.locName) + "）' in src)

# --- 二、C1 掃埋：同一 checklist 其他 remain 項唔留觸發句 ---
ok('C1：OR 條件「或到 X」改做「或（場景：X）」',
   '或（場景：$1）' in stub and '以下任一達標："+s }' not in stub
   and '以下任一達標："+s.replace(/或到([^／]+)/g, "或（場景：$1）")' in stub)
gate = seg('function prog71GateItems(id){', 'function prog71StubItems(id){', 5000)
ok('C1：兩條 checklist（GateItems C6–C17／StubItems C1–C5）入面無觸發句殘留',
   '先播到呢幕' not in gate and '先播到呢幕' not in stub
   and '就會觸發' not in gate and '就會觸發' not in stub
   and '先可以播這幕' not in gate and '先可以播這幕' not in stub)
ok('C1：傳聞提示「聽到傳聞」刻意保留（條件提示，唔係觸發句——見檔頭註解）',
   '聽到傳聞：' in stub and 'rumorHearHint' in src)
ok('C1：鎖行其餘條件句唔變（前置／週數／通告／聲望／季節）',
   '先完成第 ' in stub and '到第 ' in stub and '接通告 ' in stub
   and '要多於' in stub and '等到啱嘅季節' in stub)

# --- 三、B1(a)：live 模式驗證要求有耐久記錄 ---
ok('B1(a)：NOTES 寫明驗強制播必須行 live 模式（無 softPreview）',
   notes != '' and 'softPreview' in notes and 'live' in notes
   and ('live 模式' in notes or 'LIVE 模式' in notes))
ok('B1(a)：NOTES 講明 soft 只驗文案／靜態，唔作強制播 pass/fail 依據',
   '只驗文案' in notes or '唔作強制播' in notes or '唔可以作強制播' in notes)

# --- 四、B1(b)：start() 帶 ignoreSheetLoc（評估可行，已改） ---
sp = seg('function start(idOrNode, opts){', '/* v18h', 6000)
ok('B1(b)：StoryPlay.start 原樣轉交 ignoreSheetLoc 去 evalNode',
   'StoryOC.evalNode(node, { checkNodePhase:true, ignoreSheetLoc: !!opts.ignoreSheetLoc })' in sp)
t = seg('function story165TryForcedPlay(){', '/** v17p PLAN 9.1', 3000)
ok('B1(b)：強制播經 start() 嗰陣帶 { ignoreSheetLoc:true }',
   'StoryPlay.start(next.id, { ignoreSheetLoc:true })' in t)
ok('B1(b)：強制播仍然唔用 opts.force／allowDuringPlanner（只繞地點一步）',
   'force:true' not in t and 'allowDuringPlanner' not in t)
ok('B1(b)：全檔只有強制播一路傳 ignoreSheetLoc 入 StoryPlay.start（普通路徑唔郁）',
   len(re.findall(r"StoryPlay\.start\([^)]*ignoreSheetLoc[^)]*\)", src)) == 1
   and 'StoryPlay.start(next.id, { ignoreSheetLoc:true })' in src)
ap = seg('function autoPushC1IfNeeded(opts){', '/* v20a165 STORY165', 1500)
ok('B1(b)：autoPushC1IfNeeded 普通路徑唔帶 ignoreSheetLoc（soft 閘對玩家路徑原封不動）',
   'ignoreSheetLoc' not in ap and 'StoryPlay.start("C1")' in ap)

# --- 五、B1(b) 評估嘅承重前提：eval 鏈本身早已識 ignoreSheetLoc ---
ok('B1(b) 前提：stepLoc 識 opts.ignoreSheetLoc（唔傳就等於以前）',
   'function stepLoc(trig, ctx, opts){' in src
   and 'if(opts && opts.ignoreSheetLoc) return true;' in src)
ok('B1(b) 前提：stepFavor（OR／AND 人情＋地點）同樣識 opts.ignoreSheetLoc',
   'function stepFavor(trig, ctx, opts){' in src
   and '(opts && opts.ignoreSheetLoc)' in src)
ok('B1(b) 前提：evalNode soft 支路原樣轉交 opts 去 evalTrigger_AND_softRumor',
   'BehaviorGate.evalTrigger_AND_softRumor(node, opts)' in src)
ok('B1(b) 前提：選幕 listOpen 早已用 ignoreSheetLoc（播出同選幕一致，唔係新語義）',
   'listOpen({ checkNodePhase:true, player:true, ignoreSheetLoc:true })' in src)

# --- 六、範圍守衛：唔郁嘅嘢 ---
ok('範圍：第三條返地圖路 #home-back-map 仍然係 bypass（等用戶決定，呢票唔掂）',
   'story165TryForcedPlay' not in seg('function leaveHomeFromNotebook(mode){', 'document.getElementById("home-back-map").onclick', 2000))
ok('範圍：closeSheet() 本體仍然唔掛強制播',
   'story165TryForcedPlay' not in seg('function closeSheet(opts){', '/* ===== v20a35', 2500))
ok('範圍：普通 eval 只剩 enterLoc／doTalk 兩處寫 offer（start 已轉交 ignoreSheetLoc，見 §四）',
   src.count('StoryOC.evalNode(node, { checkNodePhase:true })') == 2)
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
