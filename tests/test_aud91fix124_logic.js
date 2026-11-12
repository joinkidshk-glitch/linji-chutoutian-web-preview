// v20a124 AUD91FIX R2 邏輯測試：Pair A／Pair B 兩個 timer 各自 defer，直至 _aud91Presenting 清。
//   Pair A (a) 旗真 → _presentForcedEnding124 唔行 conseq61PresentForcedEnding，只排 300ms 再 check。
//   Pair A (b) 再 check 嗰陣旗仲真 → 繼續排 300ms，結局一次都唔出。
//   Pair A (c) 旗清 → 即刻行 conseq61PresentForcedEnding，唔再排 timer。
//   Pair A (d) 一開始旗假 → 即刻行結局，唔排 300ms。
//   Pair A (e) 三連撞：aud91 已清但結算未走（pending 真／done 假）→ 繼續 defer；done 真 → 即刻行結局。
//   Pair B (a) 旗真 → 結算 modal 唔開，只排 300ms 再 check。
//   Pair B (b) 旗清 → 即刻開「回家結算」modal（標題＋編排新一週行程掣＋唔重扣行字）。
//   Pair B (c) 一開始旗假 → 即刻開結算 modal，唔排 300ms。
//   Pair B (d) 結算 modal 掣 on／onDismiss 都記 done（掣撳／遮罩點走都計），等強制結局 guard 識得結算走咗。
// 反證：pristine main（v122）跑呢檔要 FAIL——抽唔到 _presentForcedEnding124／_presentSettlement124。
// 用法：node tests/test_aud91fix124_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = 0;
function ok(name, cond, extra){
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ' :: ' + extra : ''));
  if(!cond) fails++;
}
// 由 marker 起 brace-count 抽出 const _xxx124 = ()=>{ ... }; 成段
function extractGuard(marker){
  const i = html.indexOf(marker);
  if(i < 0) throw new Error('guard not found: ' + marker);
  let depth = 0, j = html.indexOf('{', i), started = false;
  for(; j < html.length; j++){
    if(html[j] === '{'){ depth++; started = true; }
    else if(html[j] === '}'){ depth--; if(started && depth === 0) break; }
  }
  if(!started || depth !== 0) throw new Error('guard brace mismatch: ' + marker);
  return html.slice(i, j + 2); // 包含收尾 '};'
}
let srcA, srcB;
try{
  srcA = extractGuard('const _presentForcedEnding124');
  srcB = extractGuard('const _presentSettlement124');
  ok('harness: 兩個 guard 抽得出', true);
}catch(e){
  ok('harness: 兩個 guard 抽得出', false, e.message);
  console.log('\nAUD91FIX124 LOGIC: ' + (fails + 1) + ' FAIL');
  process.exit(1);
}

/* ---------- 假 timer：記低排咗邊個 delay，等測試手動 fire ---------- */
function makeTimers(){
  const q = [];
  return {
    queue: q,
    setTimeout(fn, ms){ q.push({ fn: fn, ms: ms }); return q.length; },
    fireAll(){
      let n = 0;
      while(q.length && n < 20){ const t = q.shift(); t.fn(); n++; }
      return n;
    },
    fireOne(){
      if(!q.length) return null;
      const t = q.shift(); t.fn(); return t;
    }
  };
}

/* ---------- Pair A ---------- */
(function(){
  // (a) 旗真 → 唔行結局，只排 300ms
  let T = makeTimers();
  var _aud91Presenting = true;
  var _week105SettlePending124 = false;
  var _week105SettleDone124 = false;
  let conseqCalls = 0;
  function conseq61PresentForcedEnding(){ conseqCalls++; }
  const setTimeout = T.setTimeout.bind(T);
  var _presentForcedEnding124;
  // eval 入面嘅 const 唔會漏出外層：將聲明改做賦值去外層 var（函數體內自引用 setTimeout 遞歸不受影響）
  eval(srcA.replace('const _presentForcedEnding124 =', '_presentForcedEnding124 ='));
  _presentForcedEnding124();
  ok('A-a 旗真：結局唔出', conseqCalls === 0);
  ok('A-a 旗真：只排一個 300ms 再 check', T.queue.length === 1 && T.queue[0].ms === 300);
  // (b) 再 check 旗仲真 → 繼續 defer
  T.fireOne();
  ok('A-b 再 check 旗仲真：結局仍然唔出', conseqCalls === 0);
  ok('A-b 再 check 旗仲真：又排一個 300ms', T.queue.length === 1 && T.queue[0].ms === 300);
  // (c) 旗清 → 即刻行結局，唔再排
  _aud91Presenting = false;
  T.fireOne();
  ok('A-c 旗清：結局即刻出一次', conseqCalls === 1);
  ok('A-c 旗清：唔再排 timer', T.queue.length === 0);
  // (d) 一開始旗假 → 即刻行，唔排 300ms
  T = makeTimers();
  _aud91Presenting = false;
  conseqCalls = 0;
  const setTimeout2 = T.setTimeout.bind(T);
  // 用新 binding 再 eval 一次（setTimeout 係 const binding，eval 內引用當時 scope 嗰個）
  (function(){
    const setTimeout = setTimeout2;
    eval(srcA.replace('const _presentForcedEnding124 =', '_presentForcedEnding124 ='));
    _presentForcedEnding124();
  })();
  ok('A-d 一開始旗假：結局即刻出', conseqCalls === 1);
  ok('A-d 一開始旗假：冇排 300ms', T.queue.length === 0);
  // (e) 三連撞：aud91 已清但結算未走 → 繼續 defer；結算走咗 → 即刻行結局
  _week105SettlePending124 = true; _week105SettleDone124 = false;
  T = makeTimers();
  _aud91Presenting = false;
  conseqCalls = 0;
  (function(){
    const setTimeout = T.setTimeout.bind(T);
    eval(srcA.replace('const _presentForcedEnding124 =', '_presentForcedEnding124 ='));
    _presentForcedEnding124();
  })();
  ok('A-e 三連撞結算未走：結局唔出', conseqCalls === 0);
  ok('A-e 三連撞結算未走：排 300ms 再 check', T.queue.length === 1 && T.queue[0].ms === 300);
  T.fireOne();
  ok('A-e 三連撞結算仲未走：結局仍然唔出', conseqCalls === 0);
  _week105SettleDone124 = true;
  T.fireOne();
  ok('A-e 三連撞結算走咗：結局即刻出一次', conseqCalls === 1);
  ok('A-e 三連撞結算走咗：唔再排 timer', T.queue.length === 0);
})();

/* ---------- Pair B ---------- */
(function(){
  var wp105 = { week: 1, html: '<p>R2 測試結算內容：第 1 週結算。</p>' };
  var _week105SettleDone124 = false;
  // (a) 旗真 → 結算 modal 唔開，只排 300ms
  let T = makeTimers();
  var _aud91Presenting = true;
  const __modals = [];
  function modal(body, btns, opts){ __modals.push({ body: String(body || ''), btns: btns || [], opts: opts || {} }); }
  const setTimeout = T.setTimeout.bind(T);
  var _presentSettlement124;
  eval(srcB.replace('const _presentSettlement124 =', '_presentSettlement124 ='));
  _presentSettlement124();
  ok('B-a 旗真：結算 modal 唔開', __modals.length === 0);
  ok('B-a 旗真：只排一個 300ms 再 check', T.queue.length === 1 && T.queue[0].ms === 300);
  // (b) 旗清 → 即刻開結算 modal，內容不變
  _aud91Presenting = false;
  T.fireOne();
  ok('B-b 旗清：結算 modal 即刻開', __modals.length === 1);
  ok('B-b 結算 modal 標題啱', __modals[0] && __modals[0].body.indexOf('回家結算 · 第 1 週') >= 0);
  ok('B-b 結算 modal 有「編排新一週行程」掣', __modals[0] && __modals[0].btns.some(b => b.label === '編排新一週行程'));
  ok('B-b 結算 modal 有唔重扣行字', __modals[0] && __modals[0].body.indexOf('唔會重扣') >= 0);
  ok('B-b 旗清：唔再排 timer', T.queue.length === 0);
  // (d) 掣 on／onDismiss 都記 done
  _week105SettleDone124 = false;
  const settleBtn = __modals[0].btns.find(b => b.label === '編排新一週行程');
  ok('B-d 結算掣有 on', settleBtn && typeof settleBtn.on === 'function');
  if(settleBtn && typeof settleBtn.on === 'function') settleBtn.on();
  ok('B-d 撳結算掣：done 記真', _week105SettleDone124 === true);
  _week105SettleDone124 = false;
  ok('B-d 結算 modal 有 onDismiss', __modals[0] && typeof __modals[0].opts.onDismiss === 'function');
  if(__modals[0] && typeof __modals[0].opts.onDismiss === 'function') __modals[0].opts.onDismiss();
  ok('B-d 遮罩點走（onDismiss）：done 記真', _week105SettleDone124 === true);
  // (c) 一開始旗假 → 即刻開，唔排 300ms
  T = makeTimers();
  _aud91Presenting = false;
  __modals.length = 0;
  const setTimeout2 = T.setTimeout.bind(T);
  (function(){
    const setTimeout = setTimeout2;
    eval(srcB.replace('const _presentSettlement124 =', '_presentSettlement124 ='));
    _presentSettlement124();
  })();
  ok('B-c 一開始旗假：結算 modal 即刻開', __modals.length === 1);
  ok('B-c 一開始旗假：冇排 300ms', T.queue.length === 0);
})();

console.log('\nAUD91FIX124 LOGIC: ' + (fails ? fails + ' FAIL' : 'ALL PASS'));
process.exit(fails ? 1 : 0);
