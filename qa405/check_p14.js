// v405 P1-4: chance() uses effective stat (costume bonus) same caliber as reqGap.
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
function extractFn(name){
  const i = html.indexOf('function '+name+'(');
  if(i<0) throw new Error('fn not found: '+name);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){ if(html[j]==='{') depth++; else if(html[j]==='}'){ depth--; if(depth===0) break; } }
  return html.slice(i, j+1);
}
function extractConst(name){
  const i = html.indexOf('const '+name+' =');
  if(i<0) throw new Error('const not found: '+name);
  let depth=0, started=false;
  for(let k=i;k<html.length;k++){ const ch=html[k];
    if(ch==='{'||ch==='['){ depth++; started=true; }
    else if(ch==='}'||ch===']'){ depth--; if(started&&depth===0) return html.slice(i,k+1)+';'; }
    else if(ch===';'&&!started) return html.slice(i,k+1); }
  throw new Error('const end: '+name);
}
var S = { acting:47, stage:40, vocal:40, looks:40, charm:40, iq:40, stamina:80, fame:50, npcs:{}, wardrobe:{ owned:[], equipped:null } };
var clamp = function(v,a,b){ return Math.max(a, Math.min(b, v)); };
for(const c of ['COSTUME265','COSTUME265_MAX_PER_STAT','GIG_REQ_KEYS88']) eval(extractConst(c).replace('const '+c+' =','var '+c+' ='));
for(const f of ['costume265ById','costume265EnsureWardrobe','costume265EquippedDef','costume265BonusMap','costume265EffStat','chance','reqGap']) eval(extractFn(f));
const gig = { req:{ acting:50 }, tier:'中級', hard:0.45, type:'電影' };
const bare = chance(gig);
const gapBare = reqGap(gig);
const best = COSTUME265.filter(c=>c.bonus && c.bonus.acting).sort((a,b)=>b.bonus.acting-a.bonus.acting)[0];
S.wardrobe.owned = [best.id]; S.wardrobe.equipped = best.id;
const eff = costume265EffStat('acting');
const boosted = chance(gig);
const gapBoosted = reqGap(gig);
S.acting = 50; S.wardrobe.equipped = null;
const atReq = chance(gig);
console.log(JSON.stringify({ costume:best.id, bonus:best.bonus.acting, bare, gapBare, eff, boosted, gapBoosted, atReq }));
const pass = gapBare.missing>0 && gapBoosted.missing===0 && Math.abs(boosted-atReq)<1e-9 && boosted>bare;
console.log(pass ? 'P14 PASS' : 'P14 FAIL');
process.exit(pass?0:1);
