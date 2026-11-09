// v20a55 TEXTFIX logic tests: extract the TEXTFIX55 block from index.html and
// run audit-original fixture strings through the cleaners.
// 反證: run against a pre-v55 index (no TEXTFIX55 block) -> extraction fails.
const fs = require('fs');
const path = process.argv[2] || 'index.html';
const s = fs.readFileSync(path, 'utf8');
const a = s.indexOf('/* ==== v20a55 TEXTFIX');
const b = s.indexOf('async function refreshCopyPacksFromDisk(){');
if (a < 0 || b < 0 || b <= a) { console.log('FAIL TEXTFIX55 block not found'); process.exit(1); }
const TF = eval(s.slice(a, b) + '\n;({ TEXTFIX55_OPTS_STORY, TEXTFIX55_OPTS_SIMPLE, textfix55Str, textfix55Walk, textfix55Note, textfix55Label, textfix55GigRecord });');
let fails = [];
function chk(name, cond) { if (!cond) fails.push(name); }

// A10: rumor id leak line -> natural line
chk('A10 rumor line', TF.textfix55Str('你啱啱聽完關於星河電視台嘅傳聞 tvb_rules_gossip，心入面有好多問號。', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '你啱啱聽完星河電視台嗰啲規矩傳聞，心入面有好多問號。');
// A6: tutorial softBehaviorGate body -> natural wording
chk('A6 tutorial body', TF.textfix55Str('正式版同熟人「傾談／送禮」耗一日；試玩閘（softBehaviorGate）下傾談／送禮不耗日（茶錢仍可能扣費；訓練／試鏡／休息／行程表演仍耗日）。', 'body', null, TF.TEXTFIX55_OPTS_SIMPLE) === '而家同熟人傾談／送禮唔會計一日（茶錢照扣）；訓練、試鏡、休息同跟行程開工先會計日。');
// C11: sent-death-question phrase swap
chk('C11 phrase', TF.textfix55Str('接送命題嗰陣', 'lines', null, TF.TEXTFIX55_OPTS_STORY) === '接辣手問題嗰陣');
// KHM: name scrubbed to title in display fields
const w1 = TF.textfix55Walk({ beats: [{ speaker: '關海媚', lines: ['關海媚企喺窗邊。'] }] }, null, null, TF.TEXTFIX55_OPTS_STORY);
chk('KHM speaker+lines', w1.beats[0].speaker === '當紅花旦' && w1.beats[0].lines[0] === '當紅花旦企喺窗邊。');
// A16/A17: effects.notes engine shorthand -> human text
chk('note ending-parallel strip', TF.textfix55Note('張子駿／文藝線；craft 高。愛情結局另表並存。') === '跟張子駿行文藝線，手藝夠硬。');
chk('note flag write', TF.textfix55Note('你拒絕咗，信用加一，寫入 flag_ho_trust') === '你拒絕咗，信用加一。');
chk('note prefix strip', TF.textfix55Note('連 C9；你企出嚟撐佢，信用升。') === '你企出嚟撐佢，信用升。');
chk('note rel map', TF.textfix55Note('你幫佢頂住；rel_hiu 大升。') === '你幫佢頂住；曉晴大升。');
chk('note label strip', TF.textfix55Label('HE：天王接班（連 T6）') === '天王接班');
// C20: 1990 flash-mob ad gig (real pack strings), whole-field rewrites
const ad = TF.textfix55GigRecord({ id: 'gig_1990_ad_01', title: '「金時鐘」手錶商場快閃廣告', roleHint: '飾演商場快閃展示手錶的都市青年', blurb: '虛構手錶品牌春檔商場快閃，要乾淨利落的商業臉。', boardNote: '春主推・商場快閃', synopsis: '虛構品牌「金時鐘」在大型商場拍快閃廣告。你戴上手錶走過中庭、對鏡校時間、轉身離去。創意只要「錢可以買時間」的消費節奏，不出現真實商標，也不要現代叫賣口播腔。' });
chk('C20 title', ad.title === '「金時鐘」手錶商場推廣');
chk('C20 boardNote', ad.boardNote === '春・商場推廣枱');
chk('C20 no anachronism', !/快閃|口播|虛構/.test(ad.title + ad.roleHint + ad.blurb + ad.boardNote + ad.synopsis));
// softBridge embedded gig: flash wording -> quick-shoot wording
const brg = TF.textfix55GigRecord({ id: 'g36_90_brg_spr_central', workTitle: '中環快閃檔', title: '《中環快閃檔》廣告熟手', roleHint: '中環快閃拍攝，人流中偷鏡，企位反應要快。', blurb: '中環廣告春季快閃檔，要熟手面孔一日拍晒。', synopsis: '快閃檔全部係偷鏡：人流唔會停，鏡頭唔會等。' });
chk('softBridge flash scrubbed', !/快閃/.test(brg.workTitle + brg.title + brg.roleHint + brg.blurb + brg.synopsis) && brg.workTitle === '中環快拍檔');
// C10-adjacent: shoot hint screenshot -> production stills
chk('shootHint stills', TF.textfix55GigRecord({ id: 'x', shootHint: '開工前睇返上一集截圖，道具唔好擺錯位。' }).shootHint === '開工前睇返上一集劇照，道具唔好擺錯位。');
// B63: wire-work accident line removed when not an action production
const wrong = TF.textfix55GigRecord({ id: 'w', type: '廣告', title: '清涼飲品廣告', synopsis: '海灘拍攝，陽光充沛。近年吊威也意外頻生，開工前檢查清楚。' });
chk('B63 wrong genre removed', !/吊威也/.test(wrong.synopsis));
const right = TF.textfix55GigRecord({ id: 'r', type: '電影', title: '飛車追逐戰', synopsis: '飛車場面連場。近年吊威也意外頻生，開工前檢查清楚。' });
chk('B63 action kept', /吊威也/.test(right.synopsis));
// B58: tier role labels de-extra-fied
chk('B58 role', TF.textfix55GigRecord({ id: 'z', tier: '高', roleLabel: '臨記男主' }).roleLabel === '男主角');

if (fails.length) { console.log('FAILURES:', fails.join(' | ')); process.exit(1); }
console.log('ALL PASS');
