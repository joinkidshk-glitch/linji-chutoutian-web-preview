// v20a60 全弧校準包・邏輯測試：
// (1) 恆常增益遞減帶＋banking（fame/popularity/主屬性；負增益/壓力/錢唔縮；低值全額）；
// (2) 雙軌回放模擬：Arc A（慢速，143 週）＋Arc C×0.75（穩定，101 週）逐週真數據——
//     未校準基線 dual 125 到達 = A 23 週／C 18 週（對返全弧報告）；校準後 A 66／C 57、中位 ~61.5 入 60–75 帶；
//     1990 年尾 dual/ fame/ credit 全部過 E1 門檻有餘（唔改 resolveEnding410 門檻）；
// (3) 生活費年份＋名氣遞增：1988 全年（wk1–43）×soft×fame 同 v20a59 逐蚊一致（紅線：唔餓死新人）；
//     1989/1990 加幅正確；散工正薪 fame≥200 ×0.75、補場 $800 不變；
// (4) 節點漏失：過窗登記／完成除名／C17 收科豁免／normalizeSaveObj 舊檔靜靜補登；
// (5) 聲樂：預設計劃輪入 train_vocal（演技優先次序保留）、bestTrainJumpForGig frozenVocal 偵測；
// (6) tutorialFxFingerErr 顯式發布去 window＋fallback 行為。
// 反證：對 v20a59 index 行 → CALIB60 函數唔存在 → FAIL。
// 用法：node tests/test_calib60_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth = 0, started = false;
  for(let k=i; k<html.length; k++){
    const ch = html[k];
    if(ch==='{'||ch==='['){ depth++; started = true; }
    else if(ch==='}'||ch===']'){ depth--; if(started && depth===0) return html.slice(i, k+1)+';'; }
    else if(ch===';' && !started) return html.slice(i, k+1);
  }
  throw new Error('const end not found: '+name);
}

/* ---- 世界 stub ---- */
var window = {};
var location = { search: '' };
var localStorage = { getItem: ()=>null, setItem: ()=>{}, removeItem: ()=>{} };
var S = null;
var refreshMoneyHud = function(){};
var softPreviewOn = function(){ return false; };
eval("var START = { y:1988, m:3, d:7 };");
for(const c of ['STAT_LABEL','STAT_MAX','STRESS_MAX','LOCS','COURSE_DEFS']) eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));
for(const c of ['CALIB60_FAME_BANDS','CALIB60_ATTR_BANDS','CALIB60_SCALED_KEYS','CALIB60_NODE_WINDOWS','CALIB60_NODE_TITLES']) eval(extractConst(c).replace('const '+c+' =', 'var '+c+' ='));
const FNS = ['R','clamp','statHardMax','dualTrackNumbers','syncDualTracks','apply',
  'calib60BandScale','calib60ScaleFor','calib60BankedGain','calib60FameGain','calib60ScaleDelta','applyCalib60',
  'calib60YearOfWeek','weekNumNow','livingCostWeekNum','livingCostBand','livingCostRoll','livingCostEstimate','takeSoftBridgePay',
  'calib60SeasonIdx','calib60NowSeasonIdx','calib60NodeTitle','calib60MissedScan','normalizeSaveObj',
  'defaultWeekPlan','fameFloor','gigMissingReqGaps','courseForStatKey','preferredLocForTrainTarget','bestTrainJumpForGig',
  'tutorialFxFingerErr'];
for(const f of FNS) eval(extractFn(f));
Math.random = function(){ return 0; };

function baseSave(){
  return { dayIndex: 30, fame: 5, popularity: 3, acting: 18, stage: 14, vocal: 14, looks: 22, iq: 20, charm: 16,
    stress: 12, money: 12000, stamina: 75, industryCreditDelta: 0,
    flags: {}, npcs: {}, board: {}, booked: [], shoots: [], trainCount: {}, enrolled: {},
    story: { gigCount: 0, flags: {}, done: {} } };
}

/* ================= (1) 遞減帶＋banking ================= */
ok('band: fame 4 全額 1.0', calib60ScaleFor('fame', 4) === 1);
ok('band: fame 10 → 0.30', calib60ScaleFor('fame', 10) === 0.30);
ok('band: fame 100 → 0.12', calib60ScaleFor('fame', 100) === 0.12);
ok('band: popularity 跟 fame 帶', calib60ScaleFor('popularity', 100) === 0.12);
ok('band: acting 20 全額', calib60ScaleFor('acting', 20) === 1);
ok('band: acting 60 → 0.25', calib60ScaleFor('acting', 60) === 0.25);
ok('band: vocal 150 → 0.19', calib60ScaleFor('vocal', 150) === 0.19);
ok('band: vocal 200 → 0.14（頂帶）', calib60ScaleFor('vocal', 200) === 0.14);
ok('band: stress 唔縮（1）', calib60ScaleFor('stress', 10) === 1);
ok('band: stamina 唔縮（1）', calib60ScaleFor('stamina', 10) === 1);

S = baseSave(); S.fame = 100;
let sum9 = 0; for(let i=0;i<9;i++) sum9 += calib60BankedGain('fame', 1, 100);
ok('banking: fame 100 連續 9 次 +1 → 合共 +1（0.12×9=1.08）', sum9 === 1);
S = baseSave(); S.fame = 500;
let sum25 = 0; for(let i=0;i<25;i++) sum25 += calib60BankedGain('fame', 1, 500);
ok('banking: fame 500 連續 25 次 +1 → 合共 +2（0.08×25=2）', sum25 === 2);

S = baseSave(); S.fame = 3; applyCalib60({ fame: 5 });
ok('applyCalib60: fame <5 全額 +5 → 8', S.fame === 8);
S = baseSave(); applyCalib60({ fame: 5 });
ok('applyCalib60: fame 5（開局值）+5 → ×0.30 落 +1、bank 0.5', S.fame === 6 && Math.abs((S.calib60Bank.fame||0) - 0.5) < 1e-9);
S = baseSave(); S.fame = 100; applyCalib60({ fame: -10 });
ok('applyCalib60: 負增益唔縮（100→90）', S.fame === 90);
S = baseSave(); applyCalib60({ stress: 30, money: 500 });
ok('applyCalib60: 壓力/錢唔縮', S.stress === 42 && S.money === 12500);
S = baseSave(); S.acting = 200; applyCalib60({ acting: 5 });
ok('applyCalib60: acting 200 +5 縮到 +0（×0.14，bank 0.7）', S.acting === 200 && Math.abs((S.calib60Bank.acting||0) - 0.7) < 1e-9);
applyCalib60({ acting: 5 });
ok('applyCalib60: 再 +5 → bank 1.4 落 +1（201）', S.acting === 201);
S = baseSave(); S.fame = 200;
ok('calib60FameGain: fame 200 +10 → +1（0.10 帶）', calib60FameGain(10) === 1);
S = baseSave(); S.fame = 300;
ok('calib60FameGain: fame 300 +10 → +0（0.08 帶，bank 0.8）', calib60FameGain(10) === 0 && Math.abs((S.calib60Bank.fame||0) - 0.8) < 1e-9);
ok('calib60FameGain: 再 +10 → bank 1.6 落 +1', calib60FameGain(10) === 1);
ok('calib60FameGain: 負數原樣', calib60FameGain(-4) === -4);

/* ================= (2) 雙軌回放模擬 ================= */
/* 每行 = [fame, stage, acting, stress, credit] 逐週快照（fullarc weeks.csv） */
const ARC_A = [[5,14,18,12,10],[9,16,24,21,15],[5,17,28,38,14],[12,20,31,64,17],[22,23,31,66,22],[26,27,32,62,26],[30,33,36,64,31],[32,36,36,39,35],[37,40,39,63,42],[37,42,41,42,45],[46,45,42,28,51],[48,48,42,0,53],[49,51,42,0,54],[49,54,42,0,55],[49,57,42,0,56],[50,60,42,0,57],[50,63,42,0,58],[51,66,42,0,60],[52,69,42,0,61],[53,72,42,0,62],[54,75,42,0,64],[56,78,42,0,66],[58,81,42,0,68],[59,84,42,0,69],[60,87,42,0,71],[61,90,42,0,72],[63,93,42,0,74],[64,96,42,0,75],[64,99,42,0,76],[64,102,42,0,77],[65,105,42,0,78],[66,108,42,0,80],[66,111,42,0,81],[67,114,42,0,82],[69,117,42,0,84],[69,120,42,0,85],[70,123,42,0,86],[72,126,42,0,88],[74,129,42,0,90],[76,132,42,0,92],[77,135,42,0,93],[78,138,42,0,95],[79,141,42,0,96],[80,144,42,0,98],[80,147,48,44,99],[80,150,59,66,100],[80,153,68,61,103],[95,156,76,62,113],[97,158,83,68,116],[97,163,92,67,119],[114,165,96,64,129],[141,171,97,60,145],[139,172,98,60,145],[154,173,101,63,153],[166,180,107,75,162],[184,185,111,63,174],[194,190,114,63,182],[194,199,114,60,185],[207,205,114,63,193],[207,207,123,62,195],[207,212,134,65,198],[222,214,137,61,208],[235,217,143,66,216],[235,218,150,67,217],[256,220,158,65,230],[257,224,165,61,234],[268,226,173,68,243],[268,231,184,61,247],[268,237,192,62,250],[268,239,200,64,252],[289,243,209,64,267],[289,246,216,60,270],[312,249,223,66,283],[312,255,227,75,284],[312,258,234,75,287],[325,265,238,75,296],[325,270,244,75,299],[325,272,252,75,301],[327,277,257,75,307],[329,288,257,61,312],[339,299,257,67,320],[359,305,258,67,332],[369,313,258,63,340],[369,322,258,61,343],[369,331,258,66,345],[386,335,263,65,356],[386,338,273,63,359],[396,340,280,62,366],[406,343,285,65,372],[419,347,289,61,381],[425,349,293,67,385],[425,352,304,60,389],[425,354,312,64,391],[425,358,321,61,394],[425,359,330,62,396],[500,362,334,63,435],[500,364,342,61,440],[500,367,351,65,442],[520,370,358,62,454],[520,372,368,65,457],[542,374,374,63,470],[546,381,374,64,474],[547,390,374,65,477],[559,395,379,63,486],[559,399,387,62,488],[568,404,395,60,496],[576,409,396,62,502],[577,416,396,60,505],[578,425,396,61,508],[606,428,401,60,524],[607,436,402,63,526],[608,445,402,67,529],[618,451,407,63,537],[618,453,415,64,540],[618,455,423,62,542],[631,457,426,75,548],[650,464,427,75,560],[645,467,431,75,561],[638,469,439,75,560],[638,472,448,68,563],[646,474,456,64,570],[646,478,457,75,570],[664,484,457,75,581],[657,491,457,65,581],[657,494,465,60,584],[657,498,473,65,586],[677,501,481,66,598],[683,504,489,65,604],[694,507,490,65,611],[695,516,490,67,614],[695,524,490,64,616],[713,530,495,68,628],[713,532,506,60,631],[713,535,514,68,633],[713,537,523,68,635],[733,541,530,61,651],[733,545,539,60,654],[745,548,545,63,662],[745,550,553,65,664],[745,552,561,61,666],[745,556,571,67,669],[805,561,576,67,701],[827,562,576,62,713]];
const ARC_C = [[5,14,18,12,10],[10,19,24,17,17],[11,21,31,46,18],[19,24,36,62,23],[22,25,41,67,25],[32,29,44,60,33],[38,32,44,33,40],[45,35,45,47,44],[49,38,45,7,48],[50,41,45,0,49],[51,44,45,0,51],[53,47,45,0,53],[53,50,45,0,54],[59,53,47,16,58],[63,57,49,50,60],[68,59,50,65,62],[81,62,54,60,72],[89,65,57,62,77],[97,69,60,63,83],[104,73,63,65,88],[104,77,64,68,89],[109,79,69,61,94],[118,82,71,67,99],[126,86,75,63,106],[136,90,78,60,113],[145,93,82,63,119],[150,95,86,63,122],[161,98,90,66,129],[173,101,92,67,138],[180,105,96,64,143],[192,109,98,66,151],[201,112,102,68,157],[211,115,104,68,163],[219,119,109,65,170],[226,124,112,64,175],[235,128,114,64,181],[242,132,117,64,187],[250,135,120,67,192],[257,139,125,66,198],[262,142,127,64,202],[277,145,127,66,210],[279,148,127,37,214],[278,151,127,6,215],[279,154,127,0,216],[286,158,133,38,222],[302,165,137,68,230],[303,167,146,61,234],[318,169,154,68,243],[328,172,159,60,250],[338,177,161,61,257],[344,181,164,65,262],[363,183,168,67,272],[374,188,169,64,281],[375,196,169,64,284],[376,205,169,61,287],[388,206,175,65,294],[388,210,183,63,297],[410,212,190,62,310],[417,216,193,64,316],[420,219,200,68,319],[432,225,205,75,328],[456,229,207,68,342],[461,234,211,67,347],[471,237,216,63,355],[475,241,220,60,359],[475,244,230,68,361],[482,245,239,61,367],[499,251,239,75,378],[501,258,242,75,382],[505,265,245,75,387],[505,273,245,75,389],[515,283,245,75,397],[527,288,251,75,406],[528,290,261,68,409],[528,292,270,65,412],[528,295,278,67,414],[554,299,280,68,429],[560,302,284,64,434],[565,308,287,65,439],[565,318,287,66,442],[566,325,287,60,445],[584,330,288,67,457],[588,334,290,60,461],[589,344,290,68,464],[590,353,290,65,467],[615,357,291,68,481],[634,358,293,62,492],[645,362,295,68,498],[646,368,295,63,501],[646,375,295,62,503],[659,381,296,61,512],[659,384,304,60,515],[671,389,313,62,524],[673,390,313,65,525],[695,393,316,68,537],[695,395,324,68,539],[705,397,331,65,546],[707,402,332,65,551],[707,411,332,66,554],[716,418,332,68,560],[744,424,333,62,577]];
function backedDelta(row){
  const base = Math.round(row[0]*0.5 + row[1]*0.3 + row[2]*0.2 - Math.max(0, row[3]-40)*0.1);
  return Math.max(0, row[4] - base);
}
function replay(rows, dilute, scaled){
  const st = { fame: rows[0][0], stage: rows[0][1], acting: rows[0][2], stress: rows[0][3], industryCreditDelta: 0, calib60Bank: {} };
  let crossDual = -1, crossFame60 = -1, crossCredit55 = -1, atEnd = null;
  for(let w = 1; w < rows.length; w++){
    const prev = rows[w-1], cur = rows[w];
    const dF = (cur[0]-prev[0]) * dilute, dS = (cur[1]-prev[1]) * dilute, dA = (cur[2]-prev[2]) * dilute;
    if(scaled){
      S = st;
      st.fame   += calib60BankedGain('fame',   dF, st.fame);
      st.stage  += calib60BankedGain('stage',  dS, st.stage);
      st.acting += calib60BankedGain('acting', dA, st.acting);
    } else { st.fame += dF; st.stage += dS; st.acting += dA; }
    st.stress = cur[3];
    st.industryCreditDelta = backedDelta(cur);
    const dual = dualTrackNumbers(st);
    const wk = w + 1;
    if(crossDual < 0 && dual.stageVolume + dual.industryCredit >= 125) crossDual = wk;
    if(crossFame60 < 0 && dual.stageVolume >= 60) crossFame60 = wk;
    if(crossCredit55 < 0 && dual.industryCredit >= 55) crossCredit55 = wk;
    atEnd = { fame: dual.stageVolume, credit: dual.industryCredit, dual: dual.stageVolume + dual.industryCredit, week: wk };
  }
  return { crossDual, crossFame60, crossCredit55, atEnd };
}
const baseA = replay(ARC_A, 1, false), baseC = replay(ARC_C, 0.75, false);
ok('回放基線（未校準）Arc A dual 125 到達 = 23 週（報告數）', baseA.crossDual === 23);
ok('回放基線（未校準）Arc C×0.75 dual 125 到達 = 18 週', baseC.crossDual === 18);
const calA = replay(ARC_A, 1, true), calC = replay(ARC_C, 0.75, true);
ok('校準後 Arc A（慢速）dual 125 到達喺 60–75 週（實得 ' + calA.crossDual + '）', calA.crossDual >= 60 && calA.crossDual <= 75);
ok('校準後 Arc C（穩定）dual 125 到達喺 50–75 週（實得 ' + calC.crossDual + '）', calC.crossDual >= 50 && calC.crossDual <= 75);
const med = (calA.crossDual + calC.crossDual) / 2;
ok('校準後兩情境中位喺 60–75 週（實得 ' + med + '）', med >= 60 && med <= 75);
ok('Arc A 1990 年尾（143 週）dual ≥ 240（實得 ' + calA.atEnd.dual + '，門檻 125）', calA.atEnd.week === 143 && calA.atEnd.dual >= 240);
ok('Arc A fame 60 到達 ≤ 100 週（實得 ' + calA.crossFame60 + '）', calA.crossFame60 > 0 && calA.crossFame60 <= 100);
ok('Arc A credit 55 到達 ≤ 65 週（實得 ' + calA.crossCredit55 + '）', calA.crossCredit55 > 0 && calA.crossCredit55 <= 65);
ok('Arc C 結局週（101）dual ≥ 180（實得 ' + calC.atEnd.dual + '）', calC.atEnd.week === 101 && calC.atEnd.dual >= 180);
ok('Arc C fame/credit 終點過 E1 單項門檻（60/55）', calC.atEnd.fame >= 60 && calC.atEnd.credit >= 55);

/* ================= (3) 經濟 ================= */
function livingCostBandV59(w, soft){
  if(w>=1 && w<=4) return 1600;
  if(soft && w>=5 && w<=8) return 1900;
  if(soft && w>=9 && w<=12) return 2100;
  return 2400;
}
let econOk = true;
for(let wk = 1; wk <= 43; wk++){
  for(const soft of [false, true]){
    for(const f of [0, 130, 300]){
      S = baseSave(); S.fame = f; softPreviewOn = function(){ return soft; };
      if(livingCostBand(wk).mid !== livingCostBandV59(wk, soft)) econOk = false;
    }
  }
}
softPreviewOn = function(){ return false; };
ok('紅線：1988（wk1–43）×soft×fame 生活費同 v59 逐蚊一致', econOk);
S = baseSave(); S.fame = 0;
ok('1989 wk50 生活費 2400+300 = 2700', livingCostBand(50).mid === 2700);
S.fame = 130; ok('1989 wk50 fame 130 → 2900（+成名 200）', livingCostBand(50).mid === 2900);
S.fame = 300; ok('1989 wk50 fame 300 → 3100（+成名 400）', livingCostBand(50).mid === 3100);
S.fame = 0;   ok('1990 wk100 生活費 2400+600 = 3000', livingCostBand(100).mid === 3000);
S.fame = 260; ok('1990 wk100 fame 260 → 3400', livingCostBand(100).mid === 3400);
S.fame = 0;   ok('1989 標籤講明物價', livingCostBand(50).label.indexOf('1989 年物價') >= 0);
ok('livingCostEstimate = band mid（預覽/扣款一致）', livingCostEstimate(50) === livingCostBand(50).mid);

S = baseSave(); S.dayIndex = 7 * 30; S.fame = 10;
const bp1 = takeSoftBridgePay(3600);
ok('散工正薪：fame 10 全額 3600', bp1.pay === 3600 && bp1.stipend === false);
const bp2 = takeSoftBridgePay(3600);
ok('散工補場：同週第二單 $800 不變', bp2.pay === 800 && bp2.stipend === true);
S = baseSave(); S.dayIndex = 7 * 30; S.fame = 250;
const bp3 = takeSoftBridgePay(3600);
ok('散工正薪：fame 250 → ×0.75 = 2700', bp3.pay === 2700 && bp3.stipend === false);

/* ================= (4) 節點漏失 ================= */
const DAY = (y, m, d)=> Math.round((Date.UTC(y, m-1, d) - Date.UTC(1988, 2, 7)) / 864e5);
function missState(dayIndex, done){
  return { dayIndex, story: { done: done || {} }, flags: {} };
}
let ms = missState(DAY(1989, 10, 15));
let newly = calib60MissedScan(ms);
const newlyIds = newly.map(x => x.id).sort();
ok('1989 秋中：C6（1988 窗）＋C7（夏窗）登記漏失', newlyIds.join() === 'C6,C7');
ok('漏失紀錄帶標題＋時期（唔劇透）', ms.calib60Missed.C7.title === '暴雨救場' && ms.calib60Missed.C7.whenLabel === '1989 年夏');
ok('C11（夏／秋窗）秋未完窗唔登記', !ms.calib60Missed.C11);
ok('C8（秋窗）身處秋季唔登記', !ms.calib60Missed.C8);
ms.story.done.C7 = true;
calib60MissedScan(ms);
ok('其後完成 → 自動除名', !ms.calib60Missed.C7 && !!ms.calib60Missed.C6);
let ms2 = missState(DAY(1989, 6, 1));
calib60MissedScan(ms2);
ok('1989 夏初：得 C6 過窗，C7 未', !!ms2.calib60Missed.C6 && !ms2.calib60Missed.C7);
let ms3 = missState(DAY(1991, 3, 15)); ms3.ending410 = { kind: 'E1' };
calib60MissedScan(ms3);
ok('已收科（ending410）→ C17 唔登記', !ms3.calib60Missed.C17);
let ms4 = missState(DAY(1991, 3, 15));
calib60MissedScan(ms4);
ok('未收科過 1990 冬 → C17 登記', !!ms4.calib60Missed.C17);
const oldSave = { dayIndex: DAY(1989, 10, 15), story: { done: { C6: true } }, stress: 50, fame: 10, stage: 5, acting: 5, industryCreditDelta: 0 };
const normed = normalizeSaveObj(JSON.parse(JSON.stringify(oldSave)));
ok('舊檔 normalize 靜靜補登：C7 入回憶、C6（已完成）唔入', !!normed.calib60Missed && !!normed.calib60Missed.C7 && !normed.calib60Missed.C6);

/* ================= (5) 聲樂 ================= */
function planState(dayIndex, enrolled, trainCount){
  return { dayIndex, fame: 5, popularity: 3, acting: 18, stage: 14, vocal: 14, looks: 22, iq: 20, charm: 16,
    stress: 10, money: 5000, stamina: 60, industryCreditDelta: 0, flags: {}, npcs: {}, board: {}, booked: [], shoots: [],
    trainCount: trainCount || {}, enrolled: enrolled || {}, mockDebts: [], story: { gigCount: 0, flags: {}, done: {} } };
}
S = planState(14, { train_acting: true, train_vocal: true }, { train_acting: 3, train_vocal: 0 });
ok('預設計劃：演技夠 2＋已報歌藝 0 堂 → 星期二排 train_vocal', defaultWeekPlan()[1] === 'train_vocal');
S = planState(14, { train_acting: true, train_vocal: true }, { train_acting: 1, train_vocal: 0 });
ok('預設計劃：演技未夠 2 → 照舊 train_acting 優先', defaultWeekPlan()[1] === 'train_acting');
S = planState(14, { train_acting: true }, { train_acting: 3, train_vocal: 0 });
ok('預設計劃：未報歌藝 → 唔排 train_vocal', defaultWeekPlan()[1] !== 'train_vocal');
S = planState(14, { train_acting: true, train_vocal: true, train_looks: true }, { train_acting: 3, train_vocal: 2, train_looks: 0 });
ok('預設計劃：歌藝夠 2 → 輪返 train_looks（舊次序）', defaultWeekPlan()[1] === 'train_looks');
S = planState(0, { train_acting: true, train_vocal: true }, { train_acting: 0, train_vocal: 0 });
ok('預設計劃：第 1 週 base 不變（星期二 rest）', defaultWeekPlan()[1] === 'rest');

S = planState(30, {}, {}); S.vocal = 14;
const jumpV = bestTrainJumpForGig({ req: { vocal: 30 } });
ok('目標建議：歌藝缺口 → train_vocal', !!jumpV && jumpV.target.courseId === 'train_vocal' && jumpV.target.mode === 'train');
const jumpLoc = LOCS.find(l => l.id === (jumpV && jumpV.target.locId));
ok('目標建議：指去音樂地點', !!jumpLoc && jumpLoc.type === 'music');
ok('目標建議：從未練歌藝 → frozenVocal = true', !!jumpV && jumpV.frozenVocal === true);
S.trainCount = { train_vocal: 1 };
const jumpV2 = bestTrainJumpForGig({ req: { vocal: 30 } });
ok('目標建議：練過 1 堂 → frozenVocal = false', !!jumpV2 && jumpV2.frozenVocal === false);
S = planState(30, {}, {}); S.acting = 10; S.vocal = 14;
const jumpA = bestTrainJumpForGig({ req: { acting: 80, vocal: 20 } });
ok('目標建議：最大缺口係演技 → frozenVocal = false', !!jumpA && jumpA.gap.key === 'acting' && jumpA.frozenVocal === false);

/* ================= (6) tutorialFx ================= */
const assignStmt = (function(){
  const i = html.indexOf('try{ window.tutorialFxFingerErr = tutorialFxFingerErr; }');
  return i >= 0 ? html.slice(i, html.indexOf('catch(_e){}', i) + 'catch(_e){}'.length) : '';
})();
ok('tutorialFx: window 發布句存在', assignStmt.length > 0);
window = {};
eval(assignStmt);
ok('tutorialFx: window.tutorialFxFingerErr 係函數', typeof window.tutorialFxFingerErr === 'function');
const fakeImg = { src: 'assets/ui-physical/tutorial-fx/fx_drag_finger.png',
  getAttribute(k){ return k === 'src' ? this.src : (k === 'data-fx-fallback' ? 'assets/ui-physical/tutorial-fx/fx_drag_finger_proc.png' : null); } };
window.tutorialFxFingerErr(fakeImg);
ok('tutorialFx: 404 時換去 fallback 圖', fakeImg.src.indexOf('fx_drag_finger_proc.png') >= 0);
window.tutorialFxFingerErr(fakeImg);
ok('tutorialFx: 已係 fallback 唔再loop', fakeImg.src.indexOf('fx_drag_finger_proc.png') >= 0);

console.log(fails.length ? ('\nFAILURES: ' + fails.length) : '\nALL PASS');
process.exit(fails.length ? 1 : 0);
