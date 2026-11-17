// v20a229 B7：報紙分類 A10＋作品圖規則 A9＋忠告卡 Q6＋stub 債 Q11・邏輯／靜態測試
// A10 合約（SPEC §2.2.1A＋A10）：新庫 category 係報紙分類權威——作品→named（配角級以上出報），
//   臨記通告／補拍通告→base（殺青唔出報紙）。press94RoleClass 加 category 先行，唔改通告數據。
//   逐張驗新庫 282 張（mtv 37 張逐張定分類，唔成批預設）；舊數據（無 category）行返文字／scale 層。
//   v252：替身守門行先——9 張作品 roleLabel／title 有「替身」照樣 base（press94RoleClass 註解原文明寫）。
// A9 合約（v90 規則沿用）：接通告頁面唔出成品海報／主演名；完成後場合（殺青／作品牆／頒獎／結局）
//   保留海報位。B3 將 poster59Path 轉咗 stub（回 ""，D-12 出圖批先恢復）——呢批唔恢復海報圖。
// Q6 合約（支線補完 Q6，用戶 2026-11-15 21:43）：憑 S.flags.chungAdviceHeld229 旗，下一次文藝片試鏡
//   多一句鍾楚凝嘅忠告做提示；效果就係呢句提示本身，唔加數字加成；用一次即清。
//   文藝片＝genre 文藝＋電影／電視劇＋category 作品。派發層照舊（ENC79_BEATS chung_farewell），
//   v20a267：傳聞系統刪除，忠告卡改記旗（唔再寫 S.mockRumors 卡）。
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
  ok('A10_newlib_282', gigs.length===282, 'n='+gigs.length);
  // 逐張驗：category 作品→named（替身守門 9 張例外→base），其餘→base
  const isStunt = g=>((g.roleLabel||'').indexOf('替身')>=0 || (g.title||'').replace(/^《[^》]*》/, '').indexOf('替身')>=0);
  const expectClass = g=>((g.category==='作品' && !isStunt(g)) ? 'named' : 'base');
  const bad = gigs.filter(g=>press94RoleClass(g)!==expectClass(g));
  ok('A10_all282_category', bad.length===0, bad.slice(0,5).map(g=>g.id+':'+g.category+'->'+press94RoleClass(g)).join(','));
  ok('A10_named_150_base_132',
    gigs.filter(g=>press94RoleClass(g)==='named').length===150 &&
    gigs.filter(g=>press94RoleClass(g)==='base').length===132);
  const stuntWorks = gigs.filter(g=>g.category==='作品' && isStunt(g));
  ok('A10_stunt_gate_9', stuntWorks.length===9 && stuntWorks.every(g=>press94RoleClass(g)==='base'),
    stuntWorks.map(g=>g.id).join(','));
  // mtv 37 張逐張定分類：19 named（作品）／18 base（臨記通告），逐張對 category
  const mtv = gigs.filter(g=>g.roleScale==='mtv');
  ok('A10_mtv_37', mtv.length===37, 'n='+mtv.length);
  const mtvBad = mtv.filter(g=>press94RoleClass(g)!==expectClass(g));
  ok('A10_mtv_each', mtvBad.length===0, mtvBad.map(g=>g.id).join(','));
  ok('A10_mtv_19named_18base',
    mtv.filter(g=>press94RoleClass(g)==='named').length===19 &&
    mtv.filter(g=>press94RoleClass(g)==='base').length===18);
  // 抽 20 張驗分類（含文字層會誤判嗰啲）
  const sample = [
    ['gig_1990_ad_202', 'base'],   // 臨記通告寫「廣告主角」
    ['gig_1990_ad_201', 'base'],   // 臨記通告「平面模特兒」
    ['gig_1990_film_103', 'base'], // 作品但「動作替身」→替身守門恒 base（舊 film_117 臨記「配角」已無接班者）
    ['gig_1990_film_206', 'base'], // 臨記通告「搬運工人」
    ['gig_1990_rec_202', 'base'],  // mtv 臨記「幕後代唱歌手」
    ['gig_1990_rec_204', 'base'],  // mtv 臨記「酒廊歌手」
    ['gig_1991_variety_203', 'base'], // 臨記「台慶大騷台上助理」
    ['gig_1990_variety_202', 'base'], // 臨記歌舞劇助演（新庫 variety roleScale 已唔係 mtv）
    ['gig_1990_rec_201', 'base'],  // mtv 臨記「和音歌手」
    ['gig_1990_film_203', 'base'], // N4_b《水塘夜戲》，臨記通告
    ['gig_1990_rec_104', 'named'], // mtv 作品「合唱配唱歌手」
    ['gig_1990_rec_106', 'named'], // mtv 作品「快歌男主唱」
    ['gig_1992_rec_103', 'named'], // mtv 作品「合唱男歌手」
    ['gig_1991_film_106', 'named'],// 作品《龍虎夜廟街》男配角
    ['gig_1990_tv_105', 'named'],  // 作品《夜半來客》武師
    ['gig_1990_film_110', 'named'],// 作品《鐵血幹探》武打配角
    ['gig_1990_tv_216', 'base'],   // 臨記通告特約演員
    ['gig_1990_tv_201', 'base'],   // 臨記通告場務助手
    ['gig_1990_film_204', 'base'], // 臨記通告「路人」（新庫已無文藝 genre 臨記通告）
    ['gig_1992_film_104', 'named'],// 作品《笑爆賀歲》男配角
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

// ---- Q6：忠告（v20a267：卡改記旗，CHUNG_ADVICE_CARD_ID229 已刪） ----
const q6parts = [
  extractConst('CHUNG_ADVICE_TEXT229'),
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
  global.S = { flags:{ chungAdviceHeld229: 1 }, mockRumors:[] };
  ok('Q6_held_with_flag', chungAdviceCardHeld229()===true);
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
  ok('Q6_held_flag_kept_after_spend', S.flags.chungAdviceHeld229===1, '用完只記 spent，held 旗留返（唔刪除）');
  // 無旗唔出
  global.S = { flags:{}, mockRumors:[] };
  ok('Q6_no_flag_no_tip', chungAdviceTipForAudition229(wenyiWork)==='');
  ok('Q6_no_flag_not_held', chungAdviceCardHeld229()===false);
  // 掛點：兩條試鏡路都有接線；派發層照舊；唔掛拼合路
  const doAud = segFn('function doAudition');
  ok('Q6_hook_doAudition', doAud.includes('chungAdviceTipForAudition229') && doAud.includes('chungAdviceSpend229') && doAud.includes('鍾楚凝的忠告'));
  const spendSrc = extractFn('chungAdviceSpend229') || '';
  ok('Q6_spend_no_number_bonus', spendSrc.includes('chungAdviceSpent229') && !/acting|fame|chance|stress/.test(spendSrc));
  const planned = html.slice(html.indexOf('else if(id.startsWith("job:"))'), html.indexOf('else if(id.startsWith("job:"))')+6000);
  ok('Q6_hook_planned_job', planned.includes('chungAdviceTipForAudition229') && planned.includes('鍾楚凝的忠告'));
  ok('Q6_grant_is_flag', html.includes('S.flags.chungAdviceHeld229 = 1'), 'chung_farewell 派發改記旗，唔再派卡');
  ok('Q6_no_rumor_card', !html.includes('rumor_chung_advice'));
  ok('Q6_merge_pairs_gone', html.indexOf('MERGE_PAIRS')<0 && html.indexOf('pair_br89_chung_farewell')<0, '傳聞拼合系統已刪，Q6 唔掛拼合路係自然結果');
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
