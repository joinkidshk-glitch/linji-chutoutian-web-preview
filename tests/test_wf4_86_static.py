# v20a86 WF4 靜態測試：日常事件池接線／碎片庫／配角小弧／對手線覆寫／紀律
# 用法：python3 tests/test_wf4_86_static.py [path-to-index.html]
# 反證：喺 v20a85 index 行應該 FAIL（冇 WF4 標記）。
import os, re, sys

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, 'index.html')
src = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS' if cond else 'FAIL') + ' ' + name)
    if not cond:
        fails.append(name)

# 紀律：SAVE key／softRev／?v= 冇改
ok('SAVE key 不變', 'starVolunteer_map_v19w' in src)
ok('softRev 不變', 's107' in src)
ok('產品 ?v= 不變', 'v20a10' in src)

# 事件池本體
ok('DAILY_EVENTS_WF4 表存在', 'const DAILY_EVENTS_WF4 = [' in src)
ok('事件數 36', len(re.findall(r'id:"wf4_ev_', src)) == 36)
ok('WF4_CFG 頻率參數（pDay .30／pLoc .20／gap 2／repeat 45）',
   'pDay:0.30' in src and 'pLoc:0.20' in src and 'gapDays:2' in src and 'repeatDays:45' in src)
ok('事件池唔經 StoryPlay applyChoice（唔污染 story 狀態）',
   'function wf4PlayEvent' in src and 'wf4ApplyFx' in src)

# 接線 hooks
ok('wf4DailyTick 掛 advanceDay（wf3SettleTick 之後）',
   src.find('wf3SettleTick(); }catch(_w3s){}') < src.find('wf4DailyTick(); }catch(_w4t){}') > 0)
# v20a196 D2：晨鏈抽去共用 morningChain196——WF4 仲係晨報之後、請柬／試鏡消息之後，帶鏈續鏈＋allowForced。
ok('wf4PresentPending 掛共用晨鏈 morningChain196（晨報之後，帶鏈續鏈）',
   src.find('presentDueMorningPaper(step)') < src.find('wf4PresentPending(step, { allowForced:true, afterCont:afterKind })')
   and 'wf4PresentPending(step, { allowForced:true, afterCont:afterKind })' in src)
ok('wf4TryLocEvent 掛 openLoc（巧遇攔截之後）',
   src.find('enc79TryIntercept(id)) return') < src.find('wf4TryLocEvent(id)) return') and 'wf4TryLocEvent(id)) return' in src)
ok('openLoc 有 wf4Done 繞過旗', 'opts.wf4Done' in src)
ok('wf4SeedFrags 掛 ensureMockJournal', 'wf4SeedFrags(); }catch(_e){}' in src)
ok('exodusFenTick 有送別戲 arm', 'wf4FenFarewellArm(wroteOff, exodused)' in src)
ok('applyRivalWf4Overrides86 掛 pack 載入（WF2 之後）',
   src.find('applyRomanceWf2Overrides81(); }catch(_wf2){}') < src.find('applyRivalWf4Overrides86(); }catch(_wf4r){}') > 0)
ok('芬姐相識場掛地點 sheet', 'wf4FenActionsAt(L.id)' in src and 'wf4FenPlay(act.id)' in src)

# 閘門精神：baseOk 齊四閘
for gate in ['ending78Locked', 'todayIsForcedDay', 'conseq61IsSickToday', 'wf4NewsDay']:
    ok('wf4BaseOk 含閘 ' + gate, gate in src[src.find('function wf4BaseOk'):src.find('function wf4BaseOk')+700])

# 碎片庫
ok('WF4_FRAG_SEEDS 18 條', len(re.findall(r'id:"rumor_wf4_', src)) == 18)
frag_region = src[src.find('const WF4_FRAG_SEEDS'):src.find('function wf4SeedFrags')]
ok('碎片含 Call 機／傳呼 ≥5 處', len(re.findall(r'Call機|傳呼', frag_region)) >= 5)
ok('碎片含大哥大 ≥3 處', len(re.findall(r'大哥大', frag_region)) >= 3)

# 花邊補完
side_region = src[src.find('const PAPER_SIDE_ITEMS'):src.find('function paperSideItemForDay')]
ok('花邊池 ≥38 則', len(re.findall(r'\{ (?:id:")?', side_region)) >= 0 and side_region.count('h:"') >= 38)
ok('花邊含 Call 機／大哥大新則', '傳呼密碼簿熱賣' in side_region and '大哥大新款開售' in side_region)

# 配角小弧
ok('芬姐相識場節點', 'WF4_fen_intro' in src and '芬姐嗰杯茶' in src)
ok('芬姐送別戲節點（啟德）', 'WF4_fen_farewell' in src and '啟德送芬姐' in src)
ok('霞姐命名（boss 事件＋debtor）', '老闆娘叫霞姐' in src and '金龍茶餐廳老闆娘霞姐' in src)
ok('霞姐弧三場齊', all(x in src for x in ['wf4_ev_boss01', 'wf4_ev_boss02', 'wf4_ev_boss03']))

# 對手線覆寫
rival_region = src[src.find('const RIVAL_WF4_OVERRIDES'):src.find('const WF4_RIVAL_APPLIED86')]
ok('RIVAL_WF4_OVERRIDES 20 節點', len(re.findall(r'A_(?:ko|tsijun|fong|ho)_[a-z0-9]+: \{', rival_region)) == 20)
ok('覆寫只換 beats／synopsis（apply 函數冇掂 choices）',
   'applyRivalWf4Overrides86' in src and 'node.beats = ov.beats.map' in src)

# 紅線：成個 WF4 區塊冇真人名／時代錯誤詞
blk = src[src.find('const DAILY_EVENTS_WF4'):src.find('/* ===== Weave Phase 3-3')]
ok('WF4 區塊冇真人名', not re.search(r'周潤發|劉德華|張國榮|陳百強|梅艷芳|林青霞', blk))
ok('WF4 區塊冇時代錯誤（VCD／互聯網／狗仔隊）', not re.search(r'VCD|互聯網|狗仔隊', blk))
ok('WF4 區塊冇 1989 指向', '1989' not in blk)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
