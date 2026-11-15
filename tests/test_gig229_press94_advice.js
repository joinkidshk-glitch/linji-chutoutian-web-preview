// v20a229 B7：報紙分類 A10＋作品圖規則 A9＋忠告卡 Q6＋stub 債 Q11・邏輯／靜態測試
// A10 合約（SPEC §2.2.1A＋A10）：新庫 category 係報紙分類權威——作品→named（配角級以上出報），
//   臨記通告／補拍通告→base（殺青唔出報紙）。press94RoleClass 加 category 先行，唔改通告數據。
//   逐張驗新庫 241 張（mtv 50 張逐張定分類，唔成批預設）；舊數據（無 category）行返文字／scale 層。
// A9 合約（v90 規則沿用）：接通告頁面唔出成品海報／主演名；完成後場合（殺青／作品牆／頒獎／結局）
//   保留海報位。B3 將 poster59Path 轉咗 stub（回 ""，D-12 出圖批先恢復）——呢批唔恢復海報圖。
// Q6 合約（支線補完 Q6，用戶 2026-11-15 21:43）：憑 rumor_chung_advice 卡，下一次文藝片試鏡
//   多一句鍾楚凝嘅忠告做提示；效果就係呢句提示本身，唔加數字加成；用一次即清。
//   文藝片＝genre 文藝＋電影／電視劇＋category 作品。派發層照舊（ENC79_BEATS chung_farewell），
//   唔掛傳聞拼合路（MERGE_PAIRS／INTEL_USE_POINTS）。
// Q11 合約（支線補完 Q11，用戶 2026-11-15 21:46）：刪 debt_slot_ngai_01 stub 債。
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
function segFn(startMarker){
  const i = html.indexOf(startMarker);
  if(i<0) return '';
  const j = html.indexOf('\nfunction ', i + 100);
  return html.slice(i, j<0 ? html.length : j);
}
let fails = 0;
function ok(name, cond, extra){
  if(cond){ console.log('PASS', name); }
  else { fails++; console.log('FAIL', name, extra||''); }
}

// ---- A10：抽取分類器 ----
const parts = [
  extractConst('PRESS94_STRONG_NAMED'), extractConst('PRESS94_BASE_LABEL'),
  extractConst('PRESS94_NAMED_LABEL'), extractConst('PRESS94_BASE_SCALES'),
  extractConst('PRESS94_NAMED_SCALES'),
  extractFn('press94ScaleOf'), extractFn('press94RoleClass'), extractFn('press94IsBaseRole'),
];
ok('A10_extract', parts.every(Boolean));
if(parts.every(Boolean)){
  eval(parts.join('\n'));
  const gigs = JSON.parse(fs.readFileSync(path.join(ROOT, 'content/gigs_new.json'), 'utf8')).gigs;
  ok('A10_newlib_241', gigs.length===241, 'n='+gigs.length);
  // 逐張驗：category 作品→named，其餘→base
  const bad = gigs.filter(g=>press94RoleClass(g)!==(g.category==='作品'?'named':'base'));
  ok('A10_all241_category', bad.length===0, bad.slice(0,5).map(g=>g.id+':'+g.category+'->'+press94RoleClass(g)).join(','));
  ok('A10_named_141_base_100',
    gigs.filter(g=>press94RoleClass(g)==='named').length===141 &&
    gigs.filter(g=>press94RoleClass(g)==='base').length===100);
  // mtv 50 張逐張定分類：22 named（作品）／28 base（臨記通告），逐張對 category
  const mtv = gigs.filter(g=>g.roleScale==='mtv');
  ok('A10_mtv_50', mtv.length===50, 'n='+mtv.length);
  const mtvBad = mtv.filter(g=>press94RoleClass(g)!==(g.category==='作品'?'named':'base'));
  ok('A10_mtv_each', mtvBad.length===0, mtvBad.map(g=>g.id).join(','));
  ok('A10_mtv_22named_28base',
    mtv.filter(g=>press94RoleClass(g)==='named').length===22 &&
    mtv.filter(g=>press94RoleClass(g)==='base').length===28);
  // 抽 20 張驗分類（含文字層會誤判嗰啲）
  const sample = [
    ['gig_1990_ad_110', 'base'],   // 臨記通告寫「廣告主角」
    ['gig_1990_ad_109', 'base'],   // 臨記通告「平面模特兒」
    ['gig_1992_film_117', 'base'], // 臨記通告 roleLabel「配角」（N13 觸發試鏡場）
    ['gig_1990_film_121', 'base'], // 臨記通告「搬運工人」
    ['gig_1990_rec_114', 'base'],  // mtv 臨記「幕後代唱歌手」
    ['gig_1990_rec_116', 'base'],  // mtv 臨記「酒廊歌手」
    ['gig_1991_variety_108', 'base'], // 臨記「台慶大騷台上助理」
    ['gig_1990_variety_107', 'base'], // mtv 臨記歌舞劇助演
    ['gig_1990_rec_111', 'base'],  // mtv 臨記「和音歌手」
    ['gig_1990_film_114', 'base'], // N-1 種子，臨記通告
    ['gig_1990_rec_104', 'named'], // mtv 作品「情歌男主唱」
    ['gig_1990_rec_106', 'named'], // mtv 作品「搖滾主唱」
    ['gig_1992_rec_103', 'named'], // mtv 作品「MV男主角」
    ['gig_1991_film_106', 'named'],// 作品《江河歲月》男配角（文藝片）
    ['gig_1990_tv_105', 'named'],  // N-3 種子，作品固定配角
    ['gig_1990_film_110', 'named'],// N-4 種子，作品男配角
    ['gig_1990_tv_122', 'base'],   // N-2 種子，臨記通告特約演員
    ['gig_1990_tv_121', 'base'],   // N-5 種子，臨記通告場務助手
    ['gig_1990_film_120', 'base'], // 文藝 genre 但臨記通告「路人」
    ['gig_1992_film_104', 'named'],// 作品《離港那天》男配角
  ];
  const byId = {};
  gigs.forEach(g=>{ byId[g.id]=g; });
  let sampleBad = [];
  sample.forEach(([id, exp])=>{
    if(!byId[id] || press94RoleClass(byId[id])!==exp) sampleBad.push(id+' exp '+exp+' got '+(byId[id]?press94RoleClass(byId[id]):'missing'));
  });
  ok('A10_sample20', sampleBad.length===0, sampleBad.join('; '));
  // 補拍通告→base
  const reshoot = gigs.filter(g=>g.category==='補拍通告');
  ok('A10_reshoot_6_base', reshoot.length===6 && reshoot.every(g=>press94RoleClass(g)==='base'), 'n='+reshoot.length);
  // 舊數據（無 category）行返文字／scale 層，唔回歸
  ok('A10_legacy_stunt_base', press94RoleClass({roleLabel:'男主角主要替身', resolvedScale:'film_support_main', band:[10,18]})==='base');
  ok('A10_legacy_cameo_base', press94RoleClass({roleLabel:'', roleScale:'tv_cameo_short', title:'《某劇》'})==='base');
  ok('A10_legacy_lead_named', press94RoleClass({roleLabel:'男主角', roleScale:'tv_lead_long'})==='named');
  ok('A10_legacy_default_named', press94RoleClass(null)==='named');
  ok('A10_legacy_softbridge_base', press94RoleClass({softBridge:true, roleLabel:'廣告熟手', roleScale:'ad_av'})==='base');
}

// ---- A9：作品圖規則靜態驗 ----
const detail = segFn('function castingNoticeDetailHtml');
ok('A9_detail_no_poster_fig', !detail.includes('${poster59fig}') && !detail.includes('cn-poster59'));
ok('A9_detail_no_lead_row', !detail.includes('${leadRow59}') && !detail.includes('<span class="k">主演</span>'));
ok('A9_detail_poster90_note', detail.includes('POSTER90'));
const opener = segFn('function openCastingNoticeDetail');
ok('A9_opener_no_poster', !opener.includes('poster59Path') && !opener.includes('leadStar59Of') && !opener.includes('${poster59fig}'));
const card = segFn('function gigCardHtml');
ok('A9_card_no_lead_star', !card.includes('lead-star') && !card.includes('${leadStar}'));
const wrap = segFn('function wrapPoster59Html');
ok('A9_wrap_keeps_poster_slot', wrap.includes('poster59Path') && wrap.includes('主演'));
const wall = segFn('function worksWallEntries59');
ok('A9_wall_keeps_poster_slot', wall.includes('poster59Path') && wall.includes('leadStar59Of'));
const wrapPoster = segFn('function np214WrapPoster214');
ok('A9_np214_wrap_guarded', wrapPoster.includes('if(!src) return null'));
ok('A9_poster59Path_stub_empty', /function poster59Path\(gigId\)\{\s*\/\*[\s\S]*?\*\/\s*return "";\s*\}/.test(html), 'B3 stub 未恢復（D-12 出圖批先恢復）為預期');
// 完成後場合有海報位（就算而家係空圖位都唔可以爛版）：workCard59Html 有 CSS 卡降級，冇裸 <img src="">
const workCard = segFn('function workCard59Html');
ok('A9_workcard_css_fallback', workCard.includes('work-csscard59') && !workCard.includes('<img class="work-poster59" src=""'));

// ---- Q6：忠告卡 ----
const q6parts = [
  extractConst('CHUNG_ADVICE_CARD_ID229'), extractConst('CHUNG_ADVICE_TEXT229'),
  extractFn('chungAdviceCardHeld229'), extractFn('isWenyiAuditionGig229'),
  extractFn('chungAdviceTipForAudition229'), extractFn('chungAdviceSpend229'),
];
ok('Q6_extract', q6parts.every(Boolean));
if(q6parts.every(Boolean)){
  eval(q6parts.join('\n'));
  // eval 入面嘅 const 留喺 eval 專屬詞法環境，唔會漏出嚟——用 regex 直接由 html 攞字串值
  const ADVICE_TEXT229 = (html.match(/const CHUNG_ADVICE_TEXT229 = "((?:[^"\\]|\\.)*)";/)||[])[1] || '';
  const wenyiWork = {genre:'文藝', type:'電影', category:'作品', roleLabel:'男配角'};
  const wenyiTv = {genre:'文藝', type:'電視劇', category:'作品', roleLabel:'男配角'};
  const wenyiExtra = {genre:'文藝', type:'電影', category:'臨記通告', roleLabel:'路人'};
  const comedyWork = {genre:'喜劇', type:'電影', category:'作品', roleLabel:'男主角'};
  const wenyiAd = {genre:'文藝', type:'廣告', category:'作品', roleLabel:'男主角'};
  global.S = { flags:{}, mockRumors:[{id:'rumor_chung_advice', source:'鍾楚凝', title:'鍾楚凝的忠告', text:'x'}] };
  ok('Q6_held_with_card', chungAdviceCardHeld229()===true);
  ok('Q6_wenyi_film_is_wenyi', isWenyiAuditionGig229(wenyiWork)===true);
  ok('Q6_wenyi_tv_is_wenyi', isWenyiAuditionGig229(wenyiTv)===true);
  ok('Q6_wenyi_extra_not_wenyi', isWenyiAuditionGig229(wenyiExtra)===false);
  ok('Q6_comedy_not_wenyi', isWenyiAuditionGig229(comedyWork)===false);
  ok('Q6_wenyi_ad_not_wenyi', isWenyiAuditionGig229(wenyiAd)===false);
  ok('Q6_tip_shows', chungAdviceTipForAudition229(wenyiWork)===ADVICE_TEXT229 && ADVICE_TEXT229.indexOf('唔好學人哋點演')===0);
  ok('Q6_tip_tv_shows', chungAdviceTipForAudition229(wenyiTv)===ADVICE_TEXT229);
  ok('Q6_tip_not_for_extra', chungAdviceTipForAudition229(wenyiExtra)==='');
  ok('Q6_tip_not_for_comedy', chungAdviceTipForAudition229(comedyWork)==='');
  // 用一次即清：spend 後再問，唔再出
  chungAdviceSpend229();
  ok('Q6_spent_flag_set', S.flags.chungAdviceSpent229===1);
  ok('Q6_second_wenyi_no_tip', chungAdviceTipForAudition229(wenyiWork)==='');
  ok('Q6_card_kept_in_rumors', S.mockRumors.some(r=>r.id==='rumor_chung_advice'), '卡本身留喺 S.mockRumors，唔刪除');
  // 無卡唔出
  global.S = { flags:{}, mockRumors:[] };
  ok('Q6_no_card_no_tip', chungAdviceTipForAudition229(wenyiWork)==='');
  ok('Q6_no_card_not_held', chungAdviceCardHeld229()===false);
  // 掛點：兩條試鏡路都有接線；派發層照舊；唔掛拼合路
  const doAud = segFn('function doAudition');
  ok('Q6_hook_doAudition', doAud.includes('chungAdviceTipForAudition229') && doAud.includes('chungAdviceSpend229') && doAud.includes('鍾楚凝的忠告'));
  const spendSrc = extractFn('chungAdviceSpend229') || '';
  ok('Q6_spend_no_number_bonus', spendSrc.includes('chungAdviceSpent229') && !/acting|fame|chance|stress/.test(spendSrc));
  const planned = html.slice(html.indexOf('else if(id.startsWith("job:"))'), html.indexOf('else if(id.startsWith("job:"))')+6000);
  ok('Q6_hook_planned_job', planned.includes('chungAdviceTipForAudition229') && planned.includes('鍾楚凝的忠告'));
  ok('Q6_grant_unchanged', html.includes('enc79GrantRumorCard({ id:"rumor_chung_advice"'));
  const mergeSeg = html.slice(html.indexOf('pair_br89_chung_farewell')-200, html.indexOf('pair_br89_chung_farewell')+1200);
  ok('Q6_merge_pairs_untouched', mergeSeg.includes('rumor_chung_advice') && !mergeSeg.includes('chungAdviceTipForAudition229') && !mergeSeg.includes('CHUNG_ADVICE'));
  ok('Q6_advice_text_is_chung_line', ADVICE_TEXT229.indexOf('諗通咗')>=0);
}

// ---- Q11：stub 債 ----
const stub = JSON.parse(fs.readFileSync(path.join(ROOT, 'content/STUB_FAVOR_DEBT_SEASON_v1.json'), 'utf8'));
ok('Q11_stub_parses', Array.isArray(stub.debts));
ok('Q11_ngai_gone', !stub.debts.some(d=>d.id==='debt_slot_ngai_01'));
ok('Q11_ho_kept', stub.debts.some(d=>d.id==='debt_slot_ho_01') && stub.debts.length===1, 'debts='+stub.debts.map(d=>d.id).join(','));
ok('Q11_no_hit_in_code', !html.includes('debt_slot_ngai_01'));
// 紀律
ok('Q11_save_key_intact', html.includes('starVolunteer_map_v19w'));

if(fails>0){ console.log('TOTAL FAIL '+fails); process.exit(1); }
console.log('TOTAL PASS');
