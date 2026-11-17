// v20a282 支線補完第 ④ 組 §14 決議落地（遊戲 code 部分）：Q3／Q4／Q11／Q12／Q13。
// 用法：node tests/test_sideline282_logic.js [path-to-index.html]
// 核心結論（Q4）：N15 1992 年秋末 code 側唔使改——source 寫舊曆 1990，YEARS66 walk
//   載入嗰陣 +2 顯示 1992；手改 source 做 1992 會 double-shift 顯示 1994。
//   唯一實質 code 改動係 Q12 殘留：ECHO89 三句「站隊那場波」→「企邊那場波」。
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const root = path.join(__dirname, '..');
let fails = [];
function ok(name, cond, extra){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name + (extra ? ' :: ' + extra : '')); }
function extractFn(name){
  const i = html.indexOf('function ' + name + '(');
  if(i < 0) throw new Error('fn not found: ' + name);
  let depth = 0, j = html.indexOf('{', i);
  for(; j < html.length; j++){
    if(html[j] === '{') depth++;
    else if(html[j] === '}'){ depth--; if(depth === 0) break; }
  }
  return html.slice(i, j + 1);
}
// 載入 index.html 入面真實嘅 YEARS66 block（唔係重寫一份），等斷言行真 code。
const y66Start = html.indexOf('const YEARS66_SHIFT');
const y66End = html.indexOf('/* gig 專用');
if(y66Start < 0 || y66End < 0) throw new Error('YEARS66 block not found in index.html');
eval(html.slice(y66Start, y66End)); // defines years66ShiftText / years66Walk

// ---------- (1) Q4：N15 1992 年秋末——source 舊曆，walk 顯示 1992，唔改 source ----------
const storyJson = JSON.parse(fs.readFileSync(path.join(root, 'content/story_detail_n1_to_n17.json'), 'utf8'));
const n15src = storyJson.nodes.find(n => n.id === 'N15');
ok('(1) Q4_source_N15_when_old_calendar', n15src.when === '1990秋末', 'source when 必須留舊曆 1990，唔好手改 1992');
ok('(1) Q4_source_N15_eraTag_untouched', n15src.eraTag === 'era_1990_autumn_idol', 'eraTag 係舊曆編碼，walk 跳過，顯示嗰陣先 +2');
const pack = JSON.parse(fs.readFileSync(path.join(root, 'content/story_detail_n1_to_n17.json'), 'utf8'));
years66Walk(pack, null);
const n15 = pack.nodes.find(n => n.id === 'N15');
ok('(1) Q4_walk_N15_when_displays_1992', n15.when === '1992秋末', 'walk 後 when 顯示 1992秋末');
const dlg = n15.beats.flatMap(b => b.lines || []).find(l => l.includes('秋末'));
ok('(1) Q4_walk_N15_dialogue_displays_1992', typeof dlg === 'string' && dlg.startsWith('1992 年秋末'), 'walk 後對白首句顯示 1992 年秋末');
ok('(1) Q4_hint_lockedHint_displays_1992', years66ShiftText('1990 年秋末才開啟，還要完成樂壇前哨、聲望和信用總和足夠。未到之前照常跑通告；開啟後去天星音樂舞蹈室。').startsWith('1992 年秋末才開啟'), 'STORY_HINT_SOFT N15 lockedHint 經 walk 顯示 1992');
ok('(1) Q4_hint_N14_nextHint_displays_1992', years66ShiftText('下一幕「錄音室」——1990 年秋末，完成樂壇前哨、聲望和信用總和足夠才開啟；開啟後去天星音樂舞蹈室。').includes('——1992 年秋末'), 'STORY_HINT_SOFT N14 nextHint 經 walk 顯示 1992');
ok('(1) Q4_double_shift_guard', years66ShiftText('1992 年秋末，天星音樂舞蹈室。') === '1994 年秋末，天星音樂舞蹈室。', '若 source 改 1992，walk 會顯示 1994——證明 source 絕對唔郁');
ok('(1) Q4_source_1990_hits_unchanged', (html.match(/1990 年秋末/g) || []).length === 2, 'index.html「1990 年秋末」留返 2 處（N14 nextHint＋N15 lockedHint），唔改');
const jsonText = fs.readFileSync(path.join(root, 'content/story_detail_n1_to_n17.json'), 'utf8');
ok('(1) Q4_json_source_1990_hit_unchanged', (jsonText.match(/1990 年秋末/g) || []).length === 1, 'JSON「1990 年秋末」留返 1 處（N15 對白首句），唔改');

// ---------- (2) Q11：debt_slot_ngai_01 stub 債，code 側 0 命中 ----------
ok('(2) Q11_no_hit_in_code', !html.includes('debt_slot_ngai_01'), 'index.html 0 命中');
const stub = JSON.parse(fs.readFileSync(path.join(root, 'content/STUB_FAVOR_DEBT_SEASON_v1.json'), 'utf8'));
const stubDebts = Array.isArray(stub) ? stub : (stub.debts || []);
ok('(2) Q11_no_hit_in_stub_json', !stubDebts.some(d => d && d.id === 'debt_slot_ngai_01'), 'STUB_FAVOR_DEBT_SEASON_v1.json 0 命中');

// ---------- (3) Q13：廖面子債過期未做當壞帳，唔計 settled，信用 −2 ----------
const tick = extractFn('wf3SettleTick');
ok('(3) Q13_overdue_not_settled_note', tick.includes('唔入帳本 settled'), '過期分支註明唔入帳本 settled');
ok('(3) Q13_overdue_credit_minus2', tick.includes('S.industryCredit = Math.max(0, (Number(S.industryCredit)||0) - 2);'), '過期分支信用 −2 在位');
const settledCalls = (tick.match(/favorLedgerNoteSettled\(/g) || []).length;
ok('(3) Q13_settled_called_once_completion_only', settledCalls === 1, 'favorLedgerNoteSettled 呼叫全函數只出現 1 次（收割完成分支；typeof 守衛唔計）');
const tail = tick.slice(tick.indexOf('liaoHarvestExpired'));
ok('(3) Q13_overdue_branch_no_settled_call', !tail.includes('favorLedgerNoteSettled'), '過期分支（liaoHarvestExpired 之後）無 settled 呼叫');

// ---------- (4) Q12：齊線「企邊」，舊詞清零 ----------
ok('(4) Q12_chai_repay_qi_bian', html.includes('企邊嗰場風波，台入面個個都睇風向'), 'chai_repay 第二句係「企邊嗰場風波」');
ok('(4) Q12_echo89_three_qi_bian', (html.match(/企邊那場波/g) || []).length === 3, 'ECHO89 三句「企邊那場波」');
ok('(4) Q12_no_zhan_dui_anywhere', !html.includes('站隊'), 'index.html「站隊」0 命中（玩家面＋註釋）');
const jsonFiles = fs.readdirSync(path.join(root, 'content')).filter(f => f.endsWith('.json'));
let zhanDuiJson = 0;
for(const f of jsonFiles){ if(fs.readFileSync(path.join(root, 'content', f), 'utf8').includes('站隊')) zhanDuiJson++; }
ok('(4) Q12_no_zhan_dui_in_content_json', zhanDuiJson === 0, 'content/*.json「站隊」0 命中');

// ---------- (5) Q3：鍾楚凝支線五幕齊全 ----------
const chungStart = html.indexOf('ENC79_BEATS.chung_choning = [');
const chungEnd = html.indexOf('];', chungStart);
const chung = html.slice(chungStart, chungEnd);
for(const beat of ['chung_review', 'chung_intel', 'chung_f_clue', 'chung_farewell', 'chung_patron']){
  ok('(5) Q3_chung_beat_' + beat, chung.includes('id:"' + beat + '"'), '鍾線 Beat 在位：' + beat);
}
ok('(5) Q3_chung_five_beats', ['chung_review', 'chung_intel', 'chung_f_clue', 'chung_farewell', 'chung_patron'].every(b => chung.includes('id:"' + b + '"')), 'Beat 1–5 共五幕，維持 5 幕唔剪');

// ---------- (6) L5023：程線時段 (1992 年–1992 年冬) 證據 ----------
const chingM = html.match(/\{ id:"ching_tinlok"[^}]*\}/);
ok('(6) L5023_ching_unlock_1992', !!chingM && chingM[0].includes('unlockYear:1992'), 'ENC79 程線 unlockYear:1992');
ok('(6) L5023_ching_window_1992_autumn_winter', !!chingM && chingM[0].includes('[1992,"秋"]') && chingM[0].includes('[1992,"冬"]'), '程巧遇窗 1992 秋／冬');
ok('(6) L5023_N15_is_1992_late_autumn', n15.when === '1992秋末', 'N15 顯示 1992 秋末（Q4 組已證），程線起點 1992 年夾得埋');

console.log(fails.length === 0 ? 'ALL PASS' : 'FAILURES: ' + fails.join(', '));
process.exit(fails.length === 0 ? 0 : 1);
