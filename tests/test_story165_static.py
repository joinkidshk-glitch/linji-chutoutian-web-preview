# -*- coding: utf-8 -*-
# v20a165 STORY165 靜態測試：主線強制播放（用戶 2026-11-13 09:24 拍板）
# 一、強制播三函數在位（story165NextOpen／CanPlay／TryForcedPlay）
# 二、掛點：goToMapForBrowse 尾段——kickScheduleIfNeeded 之後、地圖顯示之前
# 三、守門：手帳未確定順延（唔靜默提交）、結局鎖／劇情進行中唔播
# 四、選幕：只取 C*／C6F 主線、N 次序、ignoreSheetLoc（唔驗地點）
# 五、普通 StoryPlay.start（唔用 opts.force）；omit 節點先寫 offer；唔經 openLoc／唔食額度
# 六、進度頁「播呢幕」掣拎走（v155 B1 三態根除）；委派一併拎走
# 七、（刪）home-story-hint 係死碼（v20a71 PART3C 起 enterHome 唔再渲染 storyHomeHintHtml，
#    wireHomeStoryHint 嘅掣永遠唔存在）——本票唔郁佢，實時提示係地圖提示行（storyMapHintHtml，
#    掣入進度頁，唔使改）；死碼留返原樣，唔做無謂 churn。
# 八、頒獎禮：推辭都播典禮——電視直播版（gallery 旁聽弧重用）；得主規則唔變
# 九、閘條件唔變：C17 weekMin 153＋backstopDay 1096、C18 48、C19 61、額度 cap 2
# 反證：喺 pristine main（v160，276ffa1）上行會 FAIL（冇 story165 函數／掛點／
# declined165，進度頁仲有播掣）。
# 用法：python3 tests/test_story165_static.py [path-to-index.html]
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

def seg(a, b, span=6000):
    i = src.find(a)
    if i < 0: return ''
    j = src.find(b, i + len(a)) if b else -1
    return src[i:j] if j > i else src[i:i + span]

# --- 一、強制播函數在位 ---
ok('強制播三函數在位',
   'function story165NextOpen(){' in src and 'function story165CanPlay(){' in src
   and 'function story165TryForcedPlay(){' in src)

# --- 二、掛點：goToMapForBrowse 尾段 ---
g = seg('function goToMapForBrowse(){', '/* v19z8', 12000)
ok('掛點在位：kick 之後即試強制播、地圖顯示之前',
   'if(kickScheduleIfNeeded()) return;' in g and 'story165TryForcedPlay()' in g
   and 'show("v-map")' in g
   and g.index('if(kickScheduleIfNeeded()) return;') < g.index('story165TryForcedPlay()')
   < g.index('show("v-map")'))
ok('掛點有 try/catch 跌返地圖（強制播出事唔阻返地圖）',
   'catch(_s165){}' in g)

# --- 三、守門 ---
c = seg('function story165CanPlay(){', 'function story165TryForcedPlay(){', 2000)
ok('守門：手帳未確定順延（唔靜默提交）', 'if(S.homeEditable) return null;' in c)
ok('守門：結局鎖唔播', 'ending78Locked' in c and 'ending78Gate' in c)
ok('守門：劇情進行中唔播', 'isStoryPlayActive' in c and '_storyPlayLocked' in c)

# --- 四、選幕 ---
n = seg('function story165NextOpen(){', 'function story165CanPlay(){', 2500)
ok('選幕：用 ignoreSheetLoc 嘅 open 快照（唔驗地點）',
   'listOpen({ checkNodePhase:true, player:true, ignoreSheetLoc:true })' in n)
ok('選幕：只取 C*／C6F 主線（唔取 R_／WF4／巧遇）',
   'r.id==="C6F" || /^C\\d+$/.test(r.id)' in n)
ok('選幕：N 次序 C1..C6、C6F、C18、C19、C7..C17',
   '"C1","C2","C3","C4","C5","C6","C6F","C18","C19","C7"' in n)

# --- 五、普通 start，唔用 force；唔經 openLoc ---
t = seg('function story165TryForcedPlay(){', '/** v17p PLAN 9.1', 3000)
ok('omit 節點先寫 offer（forced165，同 openLoc 入場同一動作）',
   'openMeetOffer(next.id, "forced165")' in t)
ok('普通 StoryPlay.start（唔用 opts.force／allowDuringPlanner，等 start 自己再驗）',
   'StoryPlay.start(next.id)' in t and 'StoryPlay.start(next.id, {' not in t
   and 'force:true' not in t and 'allowDuringPlanner' not in t)
ok('強制播唔經 openLoc／唔食出行額度', 'openLoc(' not in t and 'travel114TrySpend' not in t)

# --- 六、進度頁掣拎走 ---
rp = seg('function renderProgressPane71(){', '/* === v20a71', 9000)
ok('進度頁：冇「播呢幕」掣（data-prog77-play／here77 清零）',
   'data-prog77-play="' not in rp and '>播呢幕</button>' not in rp and 'here77' not in rp)
ok('進度頁：已開放行寫「返地圖嗰陣就會播出」', '返地圖嗰陣就會播出' in rp)
ok('進度頁：舊「去 X 就會觸發」／「你而家喺」文案清零',
   '"去"+prog71Esc(r.locName)+"就會觸發。"' not in rp and '你而家喺' not in rp)
ok('播掣委派已拎走', 'closest("[data-prog77-play]")' not in src and '_progList77' not in src)

# --- 七、home-story-hint 係死碼（v20a71 PART3C 起停用）---
# 實時提示係地圖提示行 storyMapHintHtml（掣入進度頁，唔寫「到現場先可播」，唔使改）；
# 死碼留返原樣——斷言佢冇被本票郁過（唔係本票範圍）。
wh = seg('function wireHomeStoryHint(){', '', 2500)
ok('home-story-hint 死碼留返原樣（v71 起停用，本票唔郁）',
   '（到現場先可播）。<button type="button" id="home-story-open">去現場播劇情</button>' in src
   and 'openLoc(locId);' in wh and 'goToMapForBrowse()' not in wh)

# --- 八、頒獎禮：推辭都播典禮 ---
s = seg('function presentAwardInvite(pack, thenFn){', 'function presentPendingAward(thenFn){', 4000)
ok('推辭：先播 gallery 直播版典禮，播完先入 log／報紙／toast／cont',
   'awards62PlayCeremony(Object.assign({}, pack, { bestOutcome:"gallery", declined165:true }), finishSkip)' in s
   and 'finishSkip' in s)
ok('推辭 bookkeeping 唔變：skipped＋rewards 歸零＋declined 報紙＋toast',
   'pack.skipped = true;' in s and 'commitAwardToLog(pack);' in s
   and '{ declined:true }' in s and 'toast("已推辭席位"' in s)
ok('推辭有 try/catch 跌返舊 skip 路徑', 'catch(_e){ finishSkip(); }' in s)
b = seg('function awards62CeremonyBeats(pack){', 'function awards62PlayCeremony(pack, doneFn){', 5000)
ok('推辭直播版：pan 字幕電視 framing（唔寫「坐喺觀禮席」）',
   'pack.declined165 ? "今晚你喺屋企睇電視轉播' in b)
ok('得主規則唔變：gallery 唱名只列 fellows、得主＝fellows[0]（動態，唔寫死）',
   'gWin = fellows.length ? fellows[0] : null;' in b)

# --- 九、閘條件唔變 ---
ok('C17 結局閘唔變：weekMin 153＋backstopDay 1096',
   'weekMin: 153' in src and 'backstopDay: 1096' in src)
ok('C18／C19 前置唔變：weekMin 48／61', 'weekMin: 48' in src and 'weekMin: 61' in src)
ok('出行額度唔變：cap 2，計數只喺 openLoc（travel114TrySpend 只一處呼叫）',
   'TRAVEL114_DAILY_CAP = 2' in src and src.count('travel114TrySpend(') == 2)

# --- 十、(c) 兩條返回路徑都掛強制播（用戶 2026-11-13 11:11 拍板）---
# 調查結論（見 NOTES §8.7／§9）：closeSheet() 本體唔可以掛——佢有 ~30 個 call sites，
# modal() 每次開 modal 都先 call 佢，掛本體會喺每個 modal 之前誤播；story 同 modal
# 共用同一個 #mask／#modal-inner（StoryPlay.render() 經 modal() 行），會冚 modal。
# 設計選擇：只掛兩個真正「返回地圖」嘅用戶動作——book70ExitHome 函數本體＋
# #loc-close 撳掣包裝；modal 閘集中喺 story165CanPlay（所有掛點共用）。
bh = seg('function book70ExitHome(){', 'function setHomeTab(tab){', 3000)
ok('(c) book70ExitHome 掛強制播：返地圖之後試播，播到就 return', 
   'show("v-map"); paintBar(); drawMap();' in bh and 'story165TryForcedPlay()' in bh
   and bh.index('show("v-map"); paintBar(); drawMap();') < bh.index('story165TryForcedPlay()')
   and 'catch(_s165b){}' in bh)
ok('(c) book70ExitHome 結局閘留返（唔經呢度繞過）', 'ending78Gate()' in bh)
ok('(c) #loc-close 掛強制播：包裝先 closeSheet、問 modal 閘、再試播',
   'document.getElementById("loc-close").onclick=()=>{ try{ closeSheet(); }catch(_e){} try{ if(typeof story165ModalOpen!=="function" || !story165ModalOpen()){ if(typeof story165TryForcedPlay==="function") story165TryForcedPlay(); } }catch(_s165c){} };' in src)
ok('(c) #loc-close 舊直綁清零（唔再係 onclick=closeSheet）', 
   'document.getElementById("loc-close").onclick=closeSheet;' not in src)
ok('(c) closeSheet 本體唔掛強制播（~30 個 call sites，modal() 都會 call 佢）',
   'story165TryForcedPlay' not in seg('function closeSheet(opts){', '/* ===== v20a35', 2500))
ok('(c) book70ExitHome 掛點先問 modal 閘再試播（ux68GoLoc 經 modal 掣 on() 嗰陣唔冚 modal）',
   'story165ModalOpen()' in bh and 'story165TryForcedPlay()' in bh)
mh = seg('function story165ModalOpen(){', 'function story165TryForcedPlay(){', 1500)
ok('(c) modal 閘 helper 在位：#mask 有 on 但無 story-play-on 嗰陣先算 modal 開緊',
   'function story165ModalOpen(){' in src
   and 'classList.contains("on")' in mh and 'story-play-on' in mh
   and '_m165 && _m165.classList' in mh)
_c165i = src.find('function story165CanPlay(){')
_c165j = src.find('\n}\n', _c165i)
_c165 = src[_c165i:_c165j] if _c165i >= 0 and _c165j > _c165i else ''
ok('(c) modal 閘唔喺 story165CanPlay——晨鏈續鏈嗰陣 modal 技術上仲開緊（掣 on() 行先、closeModal 行後），擺嗰度會誤擋聽朝強制播（實駕 case C 捉到）；goToMap 掛點靠 render() 重用 #mask，唔使閘',
   _c165 != '' and 'story-play-on' not in _c165 and 'story165ModalOpen' not in _c165
   and 'classList.contains("on")' not in _c165)
ok('(c) 兩條新掛點都有 try/catch 跌返地圖（強制播出事唔阻返地圖）',
   'catch(_s165b){}' in bh and 'catch(_s165c){}' in src)
ok('(c) 新掛點唔經 openLoc／唔食額度／唔用 opts.force',
   'openLoc(' not in bh and 'travel114TrySpend' not in bh
   and 'StoryPlay.start(next.id, {' not in src.split('function story165TryForcedPlay(){')[1][:3000])
ok('(c) leaveHomeFromNotebook 唔喺呢票（第三條返地圖路，留返統籌決定——見 NOTES §9）',
   'story165TryForcedPlay' not in seg('function leaveHomeFromNotebook(mode){', 'document.getElementById("home-back-map").onclick', 2000))

# --- 十一、基線不變＋範圍 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('巧遇／WF4 流程原封不動（唔喺呢票）',
   'enc79TryIntercept' in src and 'wf4PresentPending' in src and 'enc79StoryPendingAt' in src)
ok('.prog71-play CSS 留返（死規則，v155 測試照過）',
   '.prog71-play{ margin-top:6px; min-height:36px; padding:8px 16px;' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
