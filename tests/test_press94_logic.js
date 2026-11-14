// v20a94 PRESS94 見報門檻＋「臨」徽章・邏輯測試
// 合約（用戶 2026-11-11 13:36／13:44）：
//   A 分類器（press94RoleClass，見報門檻與卡面「臨」徽章共用）：
//     基層崗位（臨記/群演/路人/幫工/和音/伴舞/替身/班底/特約/常駐散工/cameo 帶）→ base；
//     配角級或以上（主角/主唱/配角/嘉賓/模特/support_main/lead 帶）→ named；
//     替身唔出樣恆 base；support_main 短帶（≤8 日，v93 A4 單場戲型）→ base。
//   B 徽章（press94TierBadge）：base → {key:"extra", label:"臨"}；其餘照 tier（初/中/高）。
//   C 填位已退役（v20a214 NP214，用戶 2026-11-14 18:14 拍板）：press94FillLines 已刪，
//     base 殺青唔出報紙（連製作消息填位都唔出），報紙路徑唔留死 code；base 入閘行為
//     改由 test_newspaper214_wrap_logic.js 經 enqueueNewspaperFromWrap 真路徑驗。
// 反證：v93 index 冇 press94* → 抽取失敗 FAIL。
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) return null;
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) return null;
  let depth=0, started=false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  return null;
}
let fails = 0;
function ok(name, cond, extra){
  if(cond){ console.log('PASS', name); }
  else { fails++; console.log('FAIL', name, extra||''); }
}

const parts = [
  extractConst('PRESS94_STRONG_NAMED'), extractConst('PRESS94_BASE_LABEL'),
  extractConst('PRESS94_NAMED_LABEL'), extractConst('PRESS94_BASE_SCALES'),
  extractConst('PRESS94_NAMED_SCALES'),
  extractFn('press94ScaleOf'), extractFn('press94RoleClass'), extractFn('press94IsBaseRole'),
  extractFn('press94TierBadge'),
  extractFn('gigTierKey'), extractFn('newspaperMediumFromGigType')
];
ok('extract_all', parts.every(Boolean), parts.map((p,i)=>i+':'+!!p).join(','));
if(parts.every(Boolean)){
  eval(parts.join('\n'));
  const cls = (g, hint)=> press94RoleClass(g, hint||'');

  // A 分類錨點
  ok('A01_ad08_機場臨記_base', cls({roleLabel:'機場臨記', roleScale:'ad_av', tier:'中', title:'《離境大堂一封信》機場臨記'})==='base');
  ok('A02_用戶原案_唱片幫工_base', cls({roleLabel:'唱片幫工', roleScale:'rec_album', tier:'初', title:'《賀年歌精選》試聽包裝幫工'})==='base');
  ok('A03_和唱_base', cls({roleLabel:'和唱', roleScale:'mtv', title:'《賀年歌》錄音室和唱'})==='base');
  ok('A04_softBridge_base', cls({softBridge:true, roleLabel:'廣告熟手', roleScale:'ad_av'})==='base');
  ok('A05_男主角替身_base', cls({roleLabel:'男主角主要替身', resolvedScale:'film_support_main', band:[10,18]})==='base');
  ok('A06_cameo帶_base', cls({roleLabel:'', roleScale:'tv_cameo_short', title:'《某劇》'})==='base');
  ok('A07_夜班警員_named', cls({roleLabel:'夜班警員', resolvedScale:'tv_support_main', band:[12,20]})==='named');
  ok('A08_專輯主唱_named', cls({roleLabel:'專輯主唱', roleScale:'rec_album'})==='named');
  ok('A09_男主角_named', cls({roleLabel:'男主角', roleScale:'tv_lead_long'})==='named');
  ok('A10_駐場伴舞_base', cls({roleLabel:'駐場伴舞', resolvedScale:'tv_support_main', band:[12,20]})==='base');
  ok('A11_A4群演_base', cls({roleLabel:'', resolvedScale:'film_support_main', band:[2,2], title:'《檔期》賀歲搶位前哨：製片會議群演'})==='base');
  ok('A12_A4短帶配角_base', cls({roleLabel:'遠房表弟', resolvedScale:'film_support_main', band:[3,3]})==='base');
  ok('A13_武打模特_named', cls({roleLabel:'武打模特兒', roleScale:'photobook'})==='named');
  ok('A14_模糊帶預設_named', cls({roleLabel:'', roleScale:'rec_album', title:'《新碟》錄音'})==='named');
  ok('A15_null_named', cls(null)==='named');
  ok('A16_hint路人_base', cls({roleLabel:'', roleScale:'ad_av'}, '過海路人')==='base');
  ok('A17_跟組特約_base', cls(null, '跟組特約')==='base');
  ok('A18_嘉賓_named', cls({roleLabel:'遊戲嘉賓', roleScale:'variety_ep'})==='named');

  // B 徽章
  const b1 = press94TierBadge({roleLabel:'機場臨記', roleScale:'ad_av', tier:'中'});
  ok('B01_臨徽章', b1.key==='extra' && b1.label==='臨', JSON.stringify(b1));
  const b2 = press94TierBadge({roleLabel:'', roleScale:'film_support_small', tier:'初', title:'《片》小配角'});
  ok('B02_初照舊', b2.key==='junior' && b2.label==='初', JSON.stringify(b2));
  const b3 = press94TierBadge({roleLabel:'重要配角', resolvedScale:'film_support_main', band:[10,18], tier:'中'});
  ok('B03_中照舊', b3.key==='mid' && b3.label==='中', JSON.stringify(b3));
  const b4 = press94TierBadge({roleLabel:'男主角', roleScale:'tv_lead_long', tier:'高'});
  ok('B04_高照舊', b4.key==='senior' && b4.label==='高', JSON.stringify(b4));

  // C 填位已退役（v20a214 NP214）：函數已刪、入閘標記已清
  ok('C01_fill_fn_gone', html.indexOf('function press94FillLines(') < 0);
  ok('C02_no_fill_mark', html.indexOf('press94: "fill"') < 0);
  ok('C03_gate_still_wired', html.indexOf('press94IsBaseRole(gig94, labelHint94)') >= 0);
}
console.log(fails ? ('RESULT FAIL '+fails) : 'RESULT PASS');
process.exit(fails ? 1 : 0);
