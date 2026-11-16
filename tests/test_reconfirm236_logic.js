// v20a236 reconfirm 邏輯測試：共用確認 helper＋WF4 兩步流程（確認／返去）。
// 段一：confirmChoice236 本體——標記／文案／掣序／確定／返去／dismiss／esc。
// 段二：wf4FxLine236 後果提示——數值譯做書面語、空 fx、未知鍵。
// 段三：WF4 真路徑兩步——撳選項先出確認框（fx 未入帳）→ 返去返抉擇 → 再撳 → 確定先結算入帳。
// StoryPlay pickChoice 兩步見 test_verify37_logic.js 段一（真 StoryPlay＋真 confirmChoice236）。
// 用法：node tests/test_reconfirm236_logic.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); }
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
function extractConst(name){
  const i = html.indexOf('const ' + name + ' =');
  if(i < 0) throw new Error('const not found: ' + name);
  let depth = 0, started = false;
  for(let k = i; k < html.length; k++){
    const ch = html[k];
    if(ch === '{' || ch === '['){ depth++; started = true; }
    else if(ch === '}' || ch === ']'){ depth--; if(started && depth === 0) return html.slice(i, k + 1) + ';'; }
    else if(ch === ';' && !started) return html.slice(i, k + 1);
  }
  throw new Error('const end not found: ' + name);
}

/* ---- 段一：confirmChoice236 本體 ---- */
let modalCalls = [];
function modal(h, buttons, opts){ modalCalls.push({ html: String(h || ''), buttons: buttons || [], opts: opts || {} }); }
eval(extractFn('confirmChoice236'));
{
  let confirmed = 0, cancelled = 0;
  modalCalls = [];
  confirmChoice236({ choiceLabel: '留低', consequence: '去留決定一旦落定，不可更改。', onConfirm: ()=>{ confirmed++; }, onCancel: ()=>{ cancelled++; } });
  ok('236 確認框出一次', modalCalls.length === 1);
  const m = modalCalls[0];
  ok('236 確認框帶 reconfirm236 標記', m.html.indexOf('reconfirm236') >= 0);
  ok('236 確認框顯示選項原文＋後果', m.html.indexOf('留低') >= 0 && m.html.indexOf('不可更改') >= 0);
  ok('236 掣序：返去揀過行先、確定行後', (m.buttons || []).map(b=>b.label).join('/') === '返去揀過/確定');
  m.buttons[1].on();
  ok('236 撳確定：onConfirm 行一次，onCancel 唔行', confirmed === 1 && cancelled === 0);

  confirmed = 0; cancelled = 0; modalCalls = [];
  confirmChoice236({ choiceLabel: '走', onConfirm: ()=>{ confirmed++; }, onCancel: ()=>{ cancelled++; } });
  modalCalls[0].buttons[0].on();
  ok('236 撳返去：onCancel 行一次，onConfirm 唔行', confirmed === 0 && cancelled === 1);

  confirmed = 0; cancelled = 0; modalCalls = [];
  confirmChoice236({ choiceLabel: '收山', onConfirm: ()=>{ confirmed++; }, onCancel: ()=>{ cancelled++; } });
  modalCalls[0].opts.onDismiss();
  ok('236 撳遮罩 dismiss：等同返去（onCancel 行，onConfirm 唔行）', confirmed === 0 && cancelled === 1);

  modalCalls = [];
  confirmChoice236({ choiceLabel: '<script>alert(1)</script>', onConfirm: ()=>{}, onCancel: ()=>{} });
  ok('236 選項原文有 esc（唔會直出 HTML）', modalCalls[0].html.indexOf('<script>') < 0 && modalCalls[0].html.indexOf('&lt;script&gt;') >= 0);

  let threw = false;
  try{ confirmChoice236({ choiceLabel: 'x' }); }catch(e){ threw = true; }
  ok('236 冇 onConfirm／onCancel 都唔 crash', !threw);
}

/* ---- 段二：wf4FxLine236 ---- */
eval(extractFn('wf4FxLine236'));
{
  const line = wf4FxLine236({ stress: -2, fame: 1 });
  ok('236 fx 後果：壓力 -2／聲望 +1 譯做書面語', line.indexOf('壓力 -2') >= 0 && line.indexOf('聲望 +1') >= 0);
  ok('236 fx 空：跌返即時生效', wf4FxLine236({}).indexOf('即時生效') >= 0 && wf4FxLine236(null).indexOf('即時生效') >= 0);
  ok('236 fx 未知鍵照出唔吞', wf4FxLine236({ weirdKey: 3 }).indexOf('weirdKey +3') >= 0);
}

/* ---- 段三：WF4 真路徑兩步（set01：兩句＋兩選項） ---- */
let S;
function freshS(){ return { dayIndex: 0, money: 1000, stress: 30, stamina: 60, fame: 10, popularity: 10, acting: 10, charm: 10, stage: 10, looks: 10, iq: 10 }; }
function apply(fx){ const notes = []; for(const k of Object.keys(fx || {})){ const v = fx[k]; if(typeof v !== 'number' || !v) continue; S[k] = Math.max(0, (S[k] || 0) + v); notes.push(k + v); } return notes; }
function saveQ(){}
function wf4OnTableIds108(){ return []; } /* 本測試行舊路徑（set01 冇阿偉講者），唔抽 DLG106 模組 */
var LOC_SHEET_BG = {};
global.document = { getElementById: function(){ return { classList: { add: function(){}, remove: function(){} } }; } };
function clickBtn(idx){ const c = modalCalls[modalCalls.length - 1]; const b = c.buttons[idx || 0]; if(b && b.on) b.on(); }
const evs = eval(extractConst('DAILY_EVENTS_WF4').replace('const DAILY_EVENTS_WF4', 'let __evs236') + '\n;__evs236');
eval(['wf4Scene105', 'wf4PlayEvent', 'wf4ApplyFx', 'wf4Esc'].map(n => extractFn(n)).join('\n')); /* 頂層一次過 eval，function 宣告先入模組作用域 */
{
  const ev = evs.find(e => e.id === 'wf4_ev_set01');
  ok('236 set01 有兩選項', !!ev && Array.isArray(ev.choices) && ev.choices.length === 2);
  S = freshS(); modalCalls = [];
  let done = false;
  wf4PlayEvent(ev, () => { done = true; });
  clickBtn(0);
  ok('236 set01 beat1', modalCalls.length === 2);
  clickBtn(0);
  ok('236 set01 到抉擇', modalCalls.length === 3 && modalCalls[2].buttons.length === 2);
  const firstLabel = ev.choices[0].label;
  clickBtn(0);
  ok('236 撳選項後先出確認框（未結算）', modalCalls.length === 4 && modalCalls[3].html.indexOf('reconfirm236') >= 0);
  ok('236 確認框顯示選項原文＋壓力後果', modalCalls[3].html.indexOf(firstLabel) >= 0 && modalCalls[3].html.indexOf('壓力') >= 0);
  ok('236 確認前 fx 未入帳（stress 仲係 30）', S.stress === 30 && S.fame === 10);
  clickBtn(0); /* 返去揀過 */
  ok('236 撳返去：返返抉擇列（兩選項再出）', modalCalls.length === 5 && modalCalls[4].buttons.length === 2);
  ok('236 返去零副作用（fx 仲未入帳）', S.stress === 30 && S.fame === 10);
  clickBtn(0); /* 再撳同一選項 */
  ok('236 再撳又出確認框', modalCalls.length === 6 && modalCalls[5].html.indexOf('reconfirm236') >= 0);
  clickBtn(1); /* 確定 */
  ok('236 撳確定：出結算', modalCalls.length === 7 && modalCalls[6].html.includes('好意頭'));
  ok('236 確定後 fx 入帳（stress 30→28、fame 10→11）', S.stress === 28 && S.fame === 11);
  clickBtn(0);
  ok('236 播完 doneCb 有叫', done === true);
}

console.log(`\nRECONFIRM236 logic: ${fails.length ? 'FAIL ' + fails.length : 'ALL PASS'}`);
process.exit(fails.length ? 1 : 0);
