/* ===== v20a176 ROM176：全面隨機巧遇（用戶 2026-11-13 拍板：全部人隨機撞到，連紅星都可以送禮）。
   女角出沒盤（照抄 ENC79 機制，獨立一盤：P=0.50、主場 share 0.65、每日 1 次／每週 3 次／冷卻 2 日、
   初遇保底 5 日、風聲窗 P≥0.80）＋女角巧遇 modal（傾談／送禮／約會 defensive／行開）
   ＋紅星送禮（喜好注入＋enc79AddFav "gift"＋每日限＋重複減半）＋48 條星反應句注入。
   唔改 SAVE key／softRev／?v=，唔直改 content pack JSON（注入行 rom176ApplyGiftOverrides，GIFT 賦值之後呼叫）。
   唔將星寫入 S.npcs；唔自己寫排他鎖／約會／分層（行 bumpRel／giveGift／canGive／doTalk 中央路徑，等 v159 落地自動生效）。
   N10 旗核實：spine N10＝C9（1991 冬，年尾追數），海媚閘＝StoryOC.isDone("C9")；
   dayIndex≥699（1991-12-01＝1991 年冬開始）只係 done-state 讀唔到嗰陣嘅退路（舊 335＝1990-12-01 錯計 +2 年份推移，rebase fix，見 NOTES §9）。
   傾談經現行 doTalk——注意：main 入面 doTalk 加嘅係 S.npcs 人情，唔係 S.story.rel；rel 只靠送禮＋劇情節點升（見 NOTES／模擬）。 ===== */
const ROM176_WOMEN = [
  { key:"hiu",  npcId:"colleague", name:"林曉晴", primary:"tvb_longmen", secondary:"tvb_kowloon" },
  { key:"choi", npcId:"reporter",  name:"周采兒", primary:"rec_star",    secondary:"film_cotton" },
  { key:"vera", npcId:"stylist",   name:"Vera",   primary:"ad_central",  secondary:"ad_adm" },
  { key:"lan",  npcId:"lan",       name:"藍若曦", primary:"tvb_longmen", secondary:"tvb_kowloon" },
  { key:"xu",   npcId:"xu",        name:"徐寶珊", primary:"ad_central",  secondary:"ad_adm" },
  { key:"mei",  npcId:"mei",       name:"關海媚", primary:"ad_adm",      secondary:"rec_hk" },
];
const ROM176_P = 0.50, ROM176_SHARE = 0.65, ROM176_DAILY_CAP = 1, ROM176_WEEKLY_CAP = 3, ROM176_COOLDOWN = 2, ROM176_PITY_DAYS = 5;
const ROM176_MEET_NODES = { hiu:["R_hiu_meet"], choi:["R_choi_meet"], vera:["R_vera_meet"], lan:["R_lan_meet"], xu:["R_xu_meet"], mei:[] };
const ROM176_GREET = {
  hiu:"曉晴：「咦，阿偉？咁啱嘅，喺呢度撞到你。」",
  choi:"采兒：「阿偉！啱啱好，我有單嘢想問你——唔係訪問，純粹八卦。」",
  vera:"Vera：「咁啱。你今日呢身……算啦，唔講住，行埋嚟傾兩句。」",
  lan:"藍若曦：「阿偉？通告牌嗰邊啱啱先改完，你咁啱行過嚟……係咪有嘢想問？」",
  xu:"徐寶珊：「後生仔，行路望路呀。咦，係你——上次春茗撞過嗰個。」",
  mei:"關海媚：「咁啱，喺呢度撞到你。」（佢望咗你一眼，冇即刻行開。）",
};
const ROM176_TEA_LINES = {
  hiu:"化妝師話，林曉晴呢排多數喺星河電視台廠景出沒，收工會喺附近行下。",
  choi:"有個娛樂版同事漏口風：周采兒呢幾日成日喺天星音樂嗰頭蒲，話跟緊一單料。",
  vera:"造型助理講，Vera 呢排多數喺中環廣告嗰邊出沒，話接咗幾單急妝。",
  lan:"場務話，藍若曦呢排成日喺星河電視台通告牌前面企，話幫手執位。",
  xu:"廣告公司樓下個看更話，徐寶珊呢幾日多數喺中環廣告嗰邊出入，行得好急。",
  mei:"金鐘創意嗰邊有人講，關海媚呢排會喺金鐘嗰頭出現——台柱行蹤，唔係日日有。",
};
/* 巧遇返程守衛：由女角／紅星巧遇入面行出嚟嘅傾談／送禮，返地點嗰陣唔可以再擲一次巧遇
   （同一入場只觸發一個）。rom176BackOpts() 喺 doTalk／doGiveGift／openGiftPick 嘅返程共用：
   旗在就食咗佢返 { encDone:true }，唔在就原樣 { travelFree:true }。 */
let rom176InEncounter = null;
function rom176SetEncounter(v){ try{ rom176InEncounter = v || null; }catch(_e){} return rom176InEncounter; }
function rom176BackOpts(){
  try{ if(rom176InEncounter){ rom176InEncounter = null; return { encDone:true }; } }catch(_e){}
  return { travelFree:true };
}
function rom176WomanDef(key){ return ROM176_WOMEN.find(w=>w.key===key) || null; }
function rom176WomanName(key){ const d = rom176WomanDef(key); return d ? d.name : key; }
function rom176IsWomanNpc(npcId){ return ROM176_WOMEN.some(w=>w.npcId===npcId); }
function rom176WomanMet(key){
  try{
    if(S && S.flags && (S.flags["gift_met_"+key] || S.flags["gift_talked_"+key])) return true;
    if(typeof StoryOC!=="undefined"){ StoryOC.ensure(); if(StoryOC.getFlag("flag_"+key+"_talk_met")) return true; }
    const nodes = ROM176_MEET_NODES[key] || [];
    if(typeof StoryOC!=="undefined" && StoryOC.isDone){ for(const n of nodes){ if(StoryOC.isDone(n)) return true; } }
    if(S && S.story && S.story.done){ for(const n of nodes){ if(S.story.done[n]) return true; } }
  }catch(_e){}
  return false;
}
function rom176MeiUnlocked(){
  try{
    if(typeof StoryOC!=="undefined" && StoryOC.isDone) return !!StoryOC.isDone("C9");
  }catch(_e){}
  try{ if(S && S.story && S.story.done) return !!S.story.done["C9"]; }catch(_e2){}
  return ((typeof S!=="undefined" && S) ? (Number(S.dayIndex)||0) : 0) >= 699; /* 退路＝1991-12-01（1991 年冬開始，C9 閘對應；舊 335＝1990-12-01 錯計 +2 年份推移，rebase fix） */
}
function rom176WhisperActive(key){
  try{ const w = (S && S.romWhispers && S.romWhispers[key]) || null; return !!(w && (Number(w.until)||0) >= ((S && S.dayIndex)|0)); }catch(_e){ return false; }
}
function rom176BeatOpen(key){
  try{
    if(typeof StoryOC==="undefined" || !StoryOC.findNodeRaw || !StoryOC.evalNode) return false;
    const ids = [];
    (ROM176_MEET_NODES[key]||[]).forEach(n=>ids.push(n));
    ["push1","push2","crisis","ending"].forEach(s=>ids.push("R_"+key+"_"+s));
    for(const id of ids){
      if(StoryOC.isDone && StoryOC.isDone(id)) continue;
      const n = StoryOC.findNodeRaw(id);
      if(!n) continue;
      const ev = StoryOC.evalNode(n, { checkNodePhase:true });
      if(ev && ev.ok) return true;
    }
  }catch(_e){}
  return false;
}
function rom176PresenceP(key, day){
  let p = ROM176_P, share = ROM176_SHARE;
  try{
    if(key==="mei" && !rom176MeiUnlocked()) return { p:0, share:0 };
    if(rom176BeatOpen(key)) p = Math.min(0.85, p + 0.10);
    if(rom176WhisperActive(key)){ p = Math.max(p, 0.80); share = 0.85; }
  }catch(_e){}
  return { p, share };
}
function rom176EnsureDay(){
  if(typeof S==="undefined" || !S) return null;
  if(!S.romWeek || typeof S.romWeek!=="object" || Array.isArray(S.romWeek)) S.romWeek = { week:-1, count:0 };
  if(!S.romPity || typeof S.romPity!=="object" || Array.isArray(S.romPity)) S.romPity = {};
  if(!S.romWhispers || typeof S.romWhispers!=="object" || Array.isArray(S.romWhispers)) S.romWhispers = {};
  if(!S.romLast || typeof S.romLast!=="object" || Array.isArray(S.romLast)) S.romLast = {};
  if(!S.starGiftDay || typeof S.starGiftDay!=="object" || Array.isArray(S.starGiftDay)) S.starGiftDay = { day:-1, given:{} };
  const day = S.dayIndex|0;
  if(S.romDay && typeof S.romDay==="object" && !Array.isArray(S.romDay) && S.romDay.day===day) return S.romDay;
  const presence = {};
  for(const w of ROM176_WOMEN){
    const ps = rom176PresenceP(w.key, day);
    if(!(ps.p>0)) continue;
    if(enc79Rand("rom176:"+day+":"+w.key+":out") >= ps.p) continue;
    const loc = (enc79Rand("rom176:"+day+":"+w.key+":loc") < ps.share) ? w.primary : w.secondary;
    (presence[loc] = presence[loc] || []).push(w.key);
  }
  S.romDay = { day, presence, triggered:0, doneToday:{} };
  try{
    for(const k in S.romWhispers){ const x = S.romWhispers[k]; if(x && (Number(x.until)||0) < day) delete S.romWhispers[k]; }
    if(Array.isArray(S.mockRumors)){
      for(const r of S.mockRumors){
        if(r && r.wind && r.id && String(r.id).indexOf("romwind:")===0 && typeof r.windUntil==="number" && r.windUntil < day && !r.windOld){ r.windOld = true; r.season = "舊聞（已過期）"; }
      }
    }
  }catch(_e){}
  return S.romDay;
}
function rom176PresenceAt(locId){
  const sd = rom176EnsureDay();
  if(!sd || !sd.presence) return [];
  return (sd.presence[locId] || []).slice();
}
function rom176GrantWhisper(key, sourceKind, leakerName){
  try{
    if(typeof S==="undefined" || !S) return false;
    const def = rom176WomanDef(key); if(!def) return false;
    if(typeof ensureMockJournal==="function") ensureMockJournal();
    const day = S.dayIndex|0;
    const until = day + 2;
    const had = rom176WhisperActive(key);
    if(!S.romWhispers || typeof S.romWhispers!=="object") S.romWhispers = {};
    S.romWhispers[key] = { until, src: sourceKind || "tea" };
    if(had) return true;
    const locName = (typeof enc79LocName==="function") ? enc79LocName(def.primary) : def.primary;
    const text = (sourceKind==="tea" && ROM176_TEA_LINES[key])
      ? ROM176_TEA_LINES[key]
      : (sourceKind==="woman"
        ? ((leakerName||"有人")+"臨走漏咗句：「"+def.name+"呢排會喺"+locName+"出現。」")
        : ("茶餐廳伙記漏口風：聽講"+def.name+"呢幾日會喺"+locName+"出沒，想撞佢就趁早。"));
    if(Array.isArray(S.mockRumors)){
      S.mockRumors.unshift({ id:"romwind:"+key+":"+day, source:"風聲", title:"風聲："+def.name+"行蹤", text, state:"teased", season:"風聲 · 3 日內有效", wind:true, windUntil:until, fromAsk:true });
    }
    try{ if(typeof syncNotebookMirror==="function") syncNotebookMirror(); }catch(_m){}
    return true;
  }catch(_e){ return false; }
}
function rom176TeaTargets(){
  try{
    return ROM176_WOMEN.filter(w=> (w.key!=="mei" || rom176MeiUnlocked()) && !rom176WhisperActive(w.key)).map(w=>w.key);
  }catch(_e){ return []; }
}
function rom176TryIntercept(locId){
  try{
    if(typeof S==="undefined" || !S) return false;
    if(typeof ending78Gate==="function" && ending78Gate()) return false;
    const sd = rom176EnsureDay();
    const day = S.dayIndex|0;
    const wk = (typeof weekNumNow==="function") ? weekNumNow() : 0;
    if(!S.romWeek || typeof S.romWeek!=="object") S.romWeek = { week:-1, count:0 };
    if(S.romWeek.week!==wk){ S.romWeek.week = wk; S.romWeek.count = 0; }
    /* 初遇保底：入主場但嗰位女角今日唔在場 → 計一日（未見過先計；5 日即下次保證出沒；撞到即清零） */
    for(const w of ROM176_WOMEN){
      if(w.primary!==locId) continue;
      if(rom176WomanMet(w.key)) continue;
      const present = (sd.presence[locId]||[]).indexOf(w.key)>=0;
      if(!present){
        const rec = (S.romPity[w.key] && typeof S.romPity[w.key]==="object") ? S.romPity[w.key] : { days:0, day:-1 };
        if(rec.day!==day){ rec.day = day; rec.days = (Number(rec.days)||0)+1; S.romPity[w.key] = rec; }
      }
      if(!present && ((S.romPity[w.key] && Number(S.romPity[w.key].days))||0) >= ROM176_PITY_DAYS){
        (sd.presence[locId] = sd.presence[locId] || []).push(w.key);
      }
    }
    const here = sd.presence[locId] || [];
    if(!here.length) return false;
    if((sd.triggered||0) >= ROM176_DAILY_CAP) return false;
    if((S.romWeek.count||0) >= ROM176_WEEKLY_CAP) return false;
    /* 揀人：未做節拍 > 有風聲 > 名冊序（同星同一套） */
    const cands = here.filter(k=> !(sd.doneToday||{})[k]).map(k=>{
      let score = 0;
      if(rom176BeatOpen(k)) score += 2;
      if(rom176WhisperActive(k)) score += 1;
      return { key:k, score };
    }).filter(c=>{
      const last = Number((S.romLast||{})[c.key]);
      if(!isNaN(last) && day - last <= ROM176_COOLDOWN) return false;
      return true;
    });
    if(!cands.length) return false;
    cands.sort((a,b)=> b.score - a.score);
    const pick = cands[0];
    if(typeof enc79StoryPendingAt==="function" && enc79StoryPendingAt(locId)) return false; /* 主線待播優先：出沒留返同日下次入場 */
    /* 觸發入帳（跳過都計，防刷）：冷卻／上限／次數即時生效；撞到呢次即計見過 */
    sd.triggered = (sd.triggered||0) + 1;
    S.romWeek.count = (S.romWeek.count||0) + 1;
    sd.doneToday[pick.key] = 1;
    S.romLast[pick.key] = day;
    if(S.romPity) S.romPity[pick.key] = { days:0, day:day };
    try{
      S.flags = S.flags || {};
      S.flags["gift_met_"+pick.key] = true;
      S.flags["gift_talked_"+pick.key] = true;
      if(typeof StoryOC!=="undefined" && StoryOC.setFlag){ StoryOC.ensure(); StoryOC.setFlag("flag_"+pick.key+"_talk_met", true); }
    }catch(_f){}
    try{ saveQ(); }catch(_e){}
    rom176PlayEncounter(pick.key, locId);
    return true;
  }catch(_e){ return false; }
}
function rom176PlayEncounter(key, locId){
  const def = rom176WomanDef(key);
  if(!def){ try{ openLoc(locId, { encDone:true }); }catch(_e){} return; }
  rom176SetEncounter({ kind:"woman", key:key, locId:locId });
  const L = (typeof LOCS!=="undefined" ? LOCS : []).find(x=>x && x.id===locId) || { id:locId, name:locId };
  let portrait = "";
  try{
    const npc = (typeof NPCS!=="undefined") ? NPCS[def.npcId] : null;
    const face = npc && npc.face;
    portrait = (face && typeof PORTRAITS!=="undefined") ? (PORTRAITS[face] || "") : "";
  }catch(_p){}
  let greet = ROM176_GREET[key] || "";
  try{
    const pack = ((typeof NPC_LINES!=="undefined" ? NPC_LINES : null) || {})[def.npcId]
      || ((typeof NPC_LINES_CORE!=="undefined" ? NPC_LINES_CORE : null) || {})[def.npcId];
    if(pack && Array.isArray(pack.greet) && pack.greet.length) greet = pack.greet[0];
  }catch(_g){}
  /* 收尾漏風聲：種子定 30%，漏另一位未有風聲嘅女角行蹤（照星嘅「紅星帶紅星」） */
  let leakLine = "";
  try{
    const day = (S && S.dayIndex)|0;
    if(enc79Rand("rom176leak:"+day+":"+key) < 0.30){
      const others = ROM176_WOMEN.filter(w=> w.key!==key && (w.key!=="mei" || rom176MeiUnlocked()) && !rom176WhisperActive(w.key));
      if(others.length){
        const t = others[enc79Hash("rom176leaktarget:"+day+":"+key) % others.length];
        rom176GrantWhisper(t.key, "woman", def.name);
        leakLine = "<p class=\"sub\">臨走，"+def.name+"漏咗句：「"+t.name+"呢排會喺"+enc79LocName(t.primary)+"出現。」</p>";
      }
    }
  }catch(_l){}
  let canGift = false;
  try{ if(typeof GiftShop!=="undefined") canGift = !!GiftShop.canGive(key).ok; }catch(_e){ canGift = false; }
  const hasDate = (typeof rom159DateGate==="function");
  const btns = [
    { label:"傾談", role:"p", on:()=>{ rom176SetEncounter({ kind:"woman", key:key, locId:locId }); doTalk(def.npcId, L); } },
  ];
  if(canGift) btns.push({ label:"送禮", role:"p", on:()=>{ rom176SetEncounter({ kind:"woman", key:key, locId:locId }); openGiftPick(key, L); } });
  /* 約會入口只喺 v159 已落地嗰陣先出（defensive check；v176 唔自己寫約會系統）。落地嗰陣駁返 rom159DateGate 實簽名。 */
  if(hasDate) btns.push({ label:"約佢出街", role:"p", on:()=>{ rom176SetEncounter({ kind:"woman", key:key, locId:locId }); try{ rom159DateGate(key, L); }catch(_e2){ toast("約會未開放"); } } });
  btns.push({ label:"行開", role:"g", on:()=>{ rom176SetEncounter(null); try{ openLoc(locId, { encDone:true }); }catch(_e){} } });
  modal("<h3>巧遇 · "+def.name+"</h3>\n    <div class=\"dlg\"><div class=\"dlg-stage\">"
    + (portrait ? "<img class=\"dlg-portrait\" src=\""+portrait+"\" alt=\""+def.name+"\"/>" : "")
    + "<div class=\"dlg-side\"><div class=\"dlg-name\">"+def.name+"</div><div class=\"dlg-bubble\">"+greet+"</div></div></div></div>\n    "
    + leakLine
    + "<p class=\"sub\">喺"+(L.name||locId)+"撞到佢。傾談／送禮唔耗日；今日唔會再撞到佢。</p>",
    btns, { onDismiss:()=>{ rom176SetEncounter(null); try{ openLoc(locId, { encDone:true }); }catch(_e){} } });
}

/* ---------- 紅星送禮（§4）：接駁定案見 NOTES §1 —— giveGift／canGive／openGiftPick 唔假設 NPCS 存在
   （openGiftPick 只用 prefFor＋canGive＋庫存；reactionEntry 只用 GIFT_REACT.byKey），星 id 可以直接做 npcKey；
   但 giveGift 本身唔可以用：calcDelta 夾死 +2／−1、經 bumpRel 整出假 rel_<star>、另有每週 +2 軟頂。
   所以星送禮行獨立路徑：揀禮物行 openGiftPick，數值經 enc79AddFav(starId, delta, "gift")。 ---------- */
function rom176StarPrefKind(starId, itemId){
  try{
    const pref = (typeof GiftShop!=="undefined" && GiftShop.prefFor) ? GiftShop.prefFor(starId) : null;
    if(!pref) return "neutral";
    if((pref.favorites||[]).indexOf(itemId)>=0) return "favorite";
    if((pref.likes||[]).indexOf(itemId)>=0) return "liked";
    if((pref.dislikes||[]).indexOf(itemId)>=0) return "dislike";
  }catch(_e){}
  return "neutral";
}
function rom176StarDelta(starId, itemId){
  const kind = rom176StarPrefKind(starId, itemId);
  let delta = kind==="favorite" ? 4 : kind==="liked" ? 2 : kind==="dislike" ? -2 : 1;
  try{
    const st = (typeof enc79StarState==="function") ? enc79StarState(starId) : null;
    const hist = (st && st.giftHist) || {};
    if(delta>0 && (Number(hist[itemId])||0) >= 1) delta = Math.floor(delta/2);
  }catch(_e){}
  return { delta, kind };
}
function rom176CanGiveStarGift(starId){
  try{
    if(typeof S==="undefined" || !S) return false;
    if(typeof enc79StarDef==="function" && !enc79StarDef(starId)) return false;
    const st = (typeof enc79StarState==="function") ? enc79StarState(starId) : null;
    if(!st || !st.met) return false;
    const gd = (S.starGiftDay && typeof S.starGiftDay==="object") ? S.starGiftDay : null;
    if(gd && Number(gd.day)===(S.dayIndex|0) && gd.given && gd.given[starId]) return false;
    if(typeof GiftShop!=="undefined" && GiftShop.inventoryList){ if(!GiftShop.inventoryList().length) return false; }
    else if(!S.inventory || !Object.keys(S.inventory).some(id=> (Number(S.inventory[id])||0)>0)) return false;
    return true;
  }catch(_e){ return false; }
}
function rom176StarReactionLine(starId, itemId, kind){
  try{
    const by = (typeof GIFT_REACT!=="undefined" && GIFT_REACT && GIFT_REACT.byKey) || {};
    const fmt = (ent)=>{
      if(!ent) return "";
      const parts = [];
      (ent.lines||[]).forEach(ln=>{ if(ln) parts.push("<p>"+ln+"</p>"); });
      if(ent.narration) parts.push("<p class=\"sub\">"+ent.narration+"</p>");
      return parts.join("");
    };
    let ent = null;
    if(kind==="favorite") ent = by[starId+":"+itemId+":favorite"];
    else if(kind==="liked") ent = by[starId+"::liked"];
    else if(kind==="dislike") ent = by[starId+"::dislike"];
    if(ent){ const h = fmt(ent); if(h) return h; }
    if(kind==="favorite" || kind==="liked"){
      ent = by[starId+":"+itemId+":liked"] || by[starId+"::liked"];
      const h = fmt(ent); if(h) return h;
    }
    const ph = (typeof GIFT_PREFS!=="undefined" && GIFT_PREFS && GIFT_PREFS.placeholderLines) || {};
    if(kind==="liked" || kind==="favorite") return ph.liked || "佢接過禮物，笑住講：「你記性真好。」";
    if(kind==="dislike") return ph.dislike || "佢接過禮物，皺一皺眉，冇出聲。";
    return ph.neutral || "謝謝，我收下。";
  }catch(_e){ return "謝謝，我收下。"; }
}
function rom176DoGiveStarGift(starId, itemId, L){
  try{
    if(!rom176CanGiveStarGift(starId)){ toast("而家送唔到畀佢——聽日再撞到先啦。"); if(L) openLoc(L.id, { encDone:true }); return; }
    const item = (typeof GiftShop!=="undefined" && GiftShop.itemById) ? GiftShop.itemById(itemId) : null;
    if(!item){ toast("庫存冇呢件禮物。"); if(L) openLoc(L.id, { encDone:true }); return; }
    if(typeof GiftShop!=="undefined" && GiftShop.ensureSave) GiftShop.ensureSave();
    const have = (S.inventory && Number(S.inventory[itemId])) || 0;
    if(have<=0){ toast("庫存冇呢件禮物。"); if(L) openLoc(L.id, { encDone:true }); return; }
    const res176 = rom176StarDelta(starId, itemId);
    const delta = res176.delta, kind = res176.kind;
    S.inventory[itemId] = have - 1;
    if(S.inventory[itemId]<=0) delete S.inventory[itemId];
    const day = S.dayIndex|0;
    if(!S.starGiftDay || typeof S.starGiftDay!=="object" || Array.isArray(S.starGiftDay)) S.starGiftDay = { day:day, given:{} };
    if(Number(S.starGiftDay.day)!==day){ S.starGiftDay.day = day; S.starGiftDay.given = {}; }
    S.starGiftDay.given[starId] = itemId;
    const pref = (typeof GiftShop!=="undefined" && GiftShop.prefFor) ? GiftShop.prefFor(starId) : null;
    const relKey = (pref && pref.relKey) || ("rel_"+starId);
    if(S.giftMeta && S.giftMeta.lastGiveDay) S.giftMeta.lastGiveDay[relKey] = day;
    const st = enc79StarState(starId);
    if(!st.giftHist || typeof st.giftHist!=="object") st.giftHist = {};
    st.giftHist[itemId] = (Number(st.giftHist[itemId])||0) + 1;
    const before = Number(st.fav)||0;
    const applied = (typeof enc79AddFav==="function") ? enc79AddFav(starId, delta, "gift") : 0;
    const line = rom176StarReactionLine(starId, itemId, kind);
    const cap = (typeof enc79FavCap==="function") ? enc79FavCap() : 100;
    let deltaTxt;
    if(applied>0) deltaTxt = "好感 +"+applied;
    else if(applied<0) deltaTxt = "好感 "+applied;
    else if(delta>0 && before>=cap) deltaTxt = "交情已到頂（+0）";
    else if(delta>0) deltaTxt = "本週心領（+0）";
    else deltaTxt = "好感 ±0";
    try{ paintBar(); }catch(_e){} try{ drawMap(); }catch(_e){}
    const lineHtml = /<p[\s>]/.test(String(line||"")) ? String(line) : "<p>"+(line||"")+"</p>";
    const go = ()=>{ if(L) openLoc(L.id, { encDone:true }); };
    modal("<h3>送禮結果</h3>\n    "+lineHtml+"\n    <p class=\"gold\">"+deltaTxt+"</p>\n    <p class=\"sub\">"+fmtDate()+" · 送禮唔計日子</p>",[
      {label:"關閉", role:"g", on:go}
    ], {onDismiss: go});
    try{ saveQ(); }catch(_e){}
  }catch(_e){ try{ toast("送禮出錯，請再試一次。"); }catch(_e2){} }
}
/* ---------- 注入（跟 applyTangGift164／167 先例：自包含，唔依賴 ROM176 後面嘅 const 表；
   呼叫點：pack 載入 GIFT_REACT 賦值行，textfix55Walk 之前，等新句同 pack 句行同一套清洗） ---------- */
function rom176ApplyGiftOverrides(){
  try{
    if(typeof GIFT_PREFS!=="undefined" && GIFT_PREFS && GIFT_PREFS.npcs){
      const NAMES176 = { luk_baakyin:"陸柏言", liu_bingxing:"廖炳星", ngai_wingnaam:"魏詠男", yip_manji:"葉敏芝", mak_zhendong:"麥震東", lok_gasing:"駱家聲", pang_siuki:"彭少祺", chung_choning:"鍾楚凝", gu_mingfai:"顧明輝", so_jiyan:"蘇芷茵", chai_zanhoi:"齊鎮海", ching_tinlok:"程天諾", mei:"關海媚" };
      /* fav＝最愛 2／like＝喜歡 2／dis＝唔鍾意 1–2；likes 寫入 fav＋like（prefKind 嗰陣最愛都顯示「喜」，唔會誤標「普」） */
      const SP176 = {
        luk_baakyin:{ fav:["gift_coffee_beans","gift_memo_pad"], like:["gift_perfume_sample","gift_fashion_mag"], dis:["gift_pineapple_bun_set"] },
        liu_bingxing:{ fav:["gift_pineapple_bun_set","gift_egg_tart_box"], like:["gift_cassette_indie","gift_thermos"], dis:["gift_perfume_sample"] },
        ngai_wingnaam:{ fav:["gift_thermos","gift_pineapple_bun_set"], like:["gift_egg_tart_box","gift_cassette_indie"], dis:["gift_fashion_mag"] },
        yip_manji:{ fav:["gift_perfume_sample","gift_fashion_mag"], like:["gift_hair_clip_set","gift_thermos"], dis:["gift_pineapple_bun_set"] },
        mak_zhendong:{ fav:["gift_thermos","gift_egg_tart_box"], like:["gift_pineapple_bun_set","gift_cassette_indie"], dis:["gift_perfume_sample"] },
        lok_gasing:{ fav:["gift_cassette_indie","gift_coffee_beans"], like:["gift_memo_pad","gift_thermos"], dis:["gift_fashion_mag"] },
        pang_siuki:{ fav:["gift_coffee_beans","gift_memo_pad"], like:["gift_thermos","gift_egg_tart_box"], dis:["gift_perfume_sample"] },
        chung_choning:{ fav:["gift_memo_pad","gift_coffee_beans"], like:["gift_thermos","gift_cassette_indie"], dis:["gift_pineapple_bun_set"] },
        gu_mingfai:{ fav:["gift_pineapple_bun_set","gift_coffee_beans"], like:["gift_thermos","gift_egg_tart_box"], dis:["gift_perfume_sample","gift_fashion_mag"] },
        so_jiyan:{ fav:["gift_perfume_sample","gift_hair_clip_set"], like:["gift_fashion_mag","gift_handmade_sweet"], dis:["gift_pineapple_bun_set"] },
        chai_zanhoi:{ fav:["gift_coffee_beans","gift_memo_pad"], like:["gift_thermos","gift_cassette_indie"], dis:["gift_perfume_sample"] },
        ching_tinlok:{ fav:["gift_cassette_indie","gift_thermos"], like:["gift_coffee_beans","gift_egg_tart_box"], dis:["gift_fashion_mag","gift_perfume_sample"] },
        mei:{ fav:["gift_thermos","gift_memo_pad"], like:["gift_coffee_beans","gift_cassette_indie"], dis:["gift_perfume_sample","gift_fashion_mag"] },
      };
      for(const id in SP176){
        const sp = SP176[id];
        GIFT_PREFS.npcs[id] = {
          relKey:"rel_"+id, displayName:NAMES176[id]||id, mapNpcId:null, requireFlagsAny:[],
          favorites:sp.fav.slice(), likes:sp.fav.concat(sp.like), dislikes:sp.dis.slice()
        };
      }
    }
  }catch(_e){}
  try{
    if(typeof GIFT_REACT!=="undefined" && GIFT_REACT){
      if(!GIFT_REACT.byKey || typeof GIFT_REACT.byKey!=="object") GIFT_REACT.byKey = {};
      if(!Array.isArray(GIFT_REACT.entries)) GIFT_REACT.entries = [];
      const put176 = (npcKey, itemId, pref, lines)=>{
        const key = npcKey+":"+itemId+":"+pref;
        if(GIFT_REACT.byKey[key]) return;
        const ent = { npcKey:npcKey, itemId:itemId, pref:pref, lines:lines, narration:null,
          id:"GR-"+npcKey+(itemId?"-"+itemId:"")+"｜"+pref };
        GIFT_REACT.byKey[key] = ent;
        if(!GIFT_REACT.entries.some(e=>e && e.id===ent.id)) GIFT_REACT.entries.push(ent);
      };
      /* 最愛：每星 2 條 item-specific（24 條） */
      const FAV176 = [
        ["luk_baakyin","gift_coffee_beans","陸柏言：「呢隻豆沖出嚟夠濃，排練捱夜啱用。你居然識得分。」","陸柏言：「排練室得呢啲先頂得住。你有心。」"],
        ["luk_baakyin","gift_memo_pad","陸柏言：「拍紙簿唔起眼，但走位筆記就係靠呢啲。你知我每日要記幾多嘢。」","陸柏言：「記低，就係認真。呢份我收低。」"],
        ["liu_bingxing","gift_pineapple_bun_set","廖炳星：「菠蘿油加奶茶券！你係咪喺茶餐廳裝咗竊聽器，知我度橋就係靠呢啲？」","廖炳星：「啱啱好，肚餓喇。坐低一齊食啦。」"],
        ["liu_bingxing","gift_egg_tart_box","廖炳星：「蛋撻啱啱好，仲熱。我請成組一齊食，你唔好走住。」","廖炳星：「識請人食嘢，就識做人。唔該晒。」"],
        ["ngai_wingnaam","gift_thermos","魏詠男：「保溫瓶實用。捱夜嗰陣有啖熱嘢飲，個人先企得穩。」","魏詠男：「你細心。唔該。」"],
        ["ngai_wingnaam","gift_pineapple_bun_set","魏詠男：「菠蘿油，街坊嘢，啱我。你唔使扮大方，呢啲先係真。」","魏詠男：「食得落，先至有力企返起身。多謝。」"],
        ["yip_manji","gift_perfume_sample","葉敏芝：「呢隻淡香幾啱，唔嗆人。你眼光唔差，算你啦。」","葉敏芝：「唔好以為送啱一次就代表你識我。收低先啦。」"],
        ["yip_manji","gift_fashion_mag","葉敏芝：「呢期合訂我搵咗好耐。你點知我想要？唔好話你估中。」","葉敏芝：「算你啦。呢本我收低。」"],
        ["mak_zhendong","gift_thermos","麥震東：「保溫瓶好，開工成日冇啖熱水。你細心。」","麥震東：「唔該。呢份我收低。」"],
        ["mak_zhendong","gift_egg_tart_box","麥震東：「蛋撻請班武師食啱晒。你識做人。」","麥震東：「下次開工，企我隔籬。」"],
        ["lok_gasing","gift_cassette_indie","駱家聲：「呢隻卡帶……你邊度搵返嚟？原創嘢就係要咁樣先聽到。」","駱家聲：「識聽呢啲，你唔係普通臨記。唔該。」"],
        ["lok_gasing","gift_coffee_beans","駱家聲：「咖啡豆捱夜寫歌必備。你明。」","駱家聲：「有咗呢包，今晚嗰首歌有得寫。」"],
        ["pang_siuki","gift_coffee_beans","彭少祺：「咖啡豆啱，捱夜記料就係靠呢啲。你識我。」","彭少祺：「下次有料，我記得話你知。」"],
        ["pang_siuki","gift_memo_pad","彭少祺：「拍紙簿好，記人名記料唔可以靠個腦。你醒目。」","彭少祺：「呢本我收低，唔該你。」"],
        ["chung_choning","gift_memo_pad","鍾楚凝：「拍紙簿啱，演員就要記低每個細節。你做嘢認真。」","鍾楚凝：「多謝。呢份我收低。」"],
        ["chung_choning","gift_coffee_beans","鍾楚凝：「咖啡豆幾好。入戲之前一杯，個人先定得落嚟。」","鍾楚凝：「你有心。唔該。」"],
        ["gu_mingfai","gift_pineapple_bun_set","顧明輝：「菠蘿油……茶餐廳捱嗰陣就係靠呢啲。你記得我以前係點捱，算你有心。」","顧明輝：「老友，坐低一齊食啦。」"],
        ["gu_mingfai","gift_coffee_beans","顧明輝：「咖啡豆好。夜晚駐唱之前一杯，先開到聲。」","顧明輝：「今晚嗰場，你得閒就嚟聽。」"],
        ["so_jiyan","gift_perfume_sample","蘇芷茵：「呢隻淡香好襯，唔會搶鏡。你細心，我收低啦。」","蘇芷茵：「多謝你。下次見。」"],
        ["so_jiyan","gift_hair_clip_set","蘇芷茵：「髮夾幾靚，簡簡單單啱我。多謝你。」","蘇芷茵：「我會用㗎，你放心。」"],
        ["chai_zanhoi","gift_coffee_beans","齊鎮海：「咖啡豆啱，一哥都要捱夜睇劇本。你識諗。」","齊鎮海：「唔該你。呢包我收低。」"],
        ["chai_zanhoi","gift_memo_pad","齊鎮海：「拍紙簿好。做戲唔可以靠個腦，要寫低。」","齊鎮海：「你做嘢穩陣，我記住你。」"],
        ["ching_tinlok","gift_cassette_indie","程天諾：「呢隻卡帶好正！練舞嗰陣聽呢啲先有火。你識聽嘢！」","程天諾：「多謝你！我即刻帶返練舞室聽。」"],
        ["ching_tinlok","gift_thermos","程天諾：「保溫瓶啱，練舞成身汗就要飲暖水。多謝你！」","程天諾：「你真係細心。我會記住㗎。」"],
      ];
      FAV176.forEach(r=>put176(r[0], r[1], "favorite", [r[2], r[3]]));
      /* 喜歡／唔鍾意：每星各 1 條 tier-generic（24 條） */
      const GEN176 = [
        ["luk_baakyin","liked","陸柏言：「你送嚟嘅嘢，啱我用。唔該。」"],
        ["luk_baakyin","dislike","陸柏言：「呢份心意我收住先。不過下次唔使咁客氣，簡單啲好。」"],
        ["liu_bingxing","liked","廖炳星：「哈哈，啱我口味。呢份我收低，唔該你。」"],
        ["liu_bingxing","dislike","廖炳星：「嘩，咁隆重？我呢啲粗人唔慣呢套，心意收到啦。」"],
        ["ngai_wingnaam","liked","魏詠男：「收到。多謝你仲記得我。」"],
        ["ngai_wingnaam","dislike","魏詠男：「呢啲嘢唔襯我。你留返自己用啦。」"],
        ["yip_manji","liked","葉敏芝：「唔錯。收低先，唔該。」"],
        ["yip_manji","dislike","葉敏芝：「嘩，你當我係邊個？呢啲留返請食晏嗰陣先啦。」"],
        ["mak_zhendong","liked","麥震東：「收到。唔該。」"],
        ["mak_zhendong","dislike","麥震東：「呢啲嘢我唔用得。你留返。」"],
        ["lok_gasing","liked","駱家聲：「啱聽。唔該你。」"],
        ["lok_gasing","dislike","駱家聲：「商業嘢我唔啱。心意收到。」"],
        ["pang_siuki","liked","彭少祺：「唔錯，啱用。唔該。」"],
        ["pang_siuki","dislike","彭少祺：「咁隆重做咩？我呢啲跑情報嘅，實用啲好。」"],
        ["chung_choning","liked","鍾楚凝：「多謝。你有心。」"],
        ["chung_choning","dislike","鍾楚凝：「呢啲我唔啱。你唔使破費。」"],
        ["gu_mingfai","liked","顧明輝：「收到。老友，多謝。」"],
        ["gu_mingfai","dislike","顧明輝：「呢啲嘢唔襯我呢個落魄佬。你留返。」"],
        ["so_jiyan","liked","蘇芷茵：「好靚，我鍾意。多謝你。」"],
        ["so_jiyan","dislike","蘇芷茵：「唔好意思，呢啲我唔係好啱。你心意我收到啦。」"],
        ["chai_zanhoi","liked","齊鎮海：「唔錯。唔該你。」"],
        ["chai_zanhoi","dislike","齊鎮海：「呢啲嘢唔係我嗰套。心意收到。」"],
        ["ching_tinlok","liked","程天諾：「多謝！啱用，我會帶返去練舞室。」"],
        ["ching_tinlok","dislike","程天諾：「呢啲……我唔係好啱用。你留返自己啦，唔好意思。」"],
      ];
      GEN176.forEach(r=>put176(r[0], "", r[1], [r[2]]));
    }
  }catch(_e){}
  try{
    /* NPC_LINES：藍／徐／海媚傾談對白（pack 冇呢三個人；冇佢哋 pickNpcLine 回 "……"） */
    if(typeof NPC_LINES!=="undefined" && NPC_LINES){
      const NL176 = {
        lan:{ name:"藍若曦",
          greet:["阿偉？通告牌嗰邊啱啱先改完，你搵我？","唔好意思，我而家對緊出場次序，你等我一陣。"],
          chat:["排位呢啲嘢，錯一個位成晚就亂晒。我唔敢行開。","你話做臨記辛苦？我哋場記都係咁，邊個唔係由朝企到晚。"],
          advice:["想上位？唔好淨係等機會，要令人記得你係邊個。","通告牌唔會等人。你肯捱，自然有人見到。"],
          intel:["聽聞下個月有套大製作開鏡，通告牌仲未定，你留意下。","有個副導話想搵生面孔試吓文戲，你得閒去片場行下。"],
          pressure:["唔好喺呢個時候煩我，通告牌改到我頭都大埋。","你唔見我忙到連水都冇時間飲咩？"] },
        xu:{ name:"徐寶珊",
          greet:["後生仔，行路望路呀。咦，係你——上次春茗撞過嗰個。","你喺呢度做咩？廣告公司唔係片場，唔好周圍望。"],
          chat:["做廣告呢行，客戶話乜就係乜，你唔啱聽都要笑住應。","你話做臨記辛苦？我由朝九做到夜晚十一，邊日唔係咁。"],
          advice:["想人記得你？第一印象好重要，企出嚟嗰下唔可以縮。","呢行最緊要準時同醒目，遲到一次，人哋就唔再搵你。"],
          intel:["有個客戶想搵個生面孔拍廣告，條件唔高，你可以試下。","聽聞有間大公司想搞個新系列，要好多臨記，你留意通告欄。"],
          pressure:["我而家趕住見客，你有嘢快啲講，唔好阻住我。","唔好喺度阻住晒，我仲有三個會要開。"] },
        mei:{ name:"關海媚",
          greet:["咁啱，喺呢度撞到你。","（佢望咗你一眼，冇即刻行開。）有嘢搵我？"],
          chat:["台上面光鮮，台下面一地雞毛——呢啲嘢，行內人先明。","你以為做台柱風光？收工嗰陣，成個人散晒。"],
          advice:["想紅？首先要企得穩，唔好俾人一眼睇穿你怯。","呢行講嘅係氣場。你企出嚟嗰下，人哋信你，你就贏一半。"],
          intel:["聽聞台慶嗰邊有個大騷，仲爭緊人，你可以留意下。","有個監製話想搵個新面孔試鏡，唔係大製作，但係個好開始。"],
          pressure:["我而家要趕返廠，唔好意思，傾住咁多先。","唔好意思，我趕時間，下次先慢慢傾。"] },
      };
      for(const k in NL176){ if(!NPC_LINES[k]) NPC_LINES[k] = NL176[k]; }
    }
  }catch(_e){}
  try{
    /* PORTRAITS：藍／徐／海媚頭像（fullbody base 圖，dlg-portrait cover＋top 裁切出頭肩） */
    if(typeof PORTRAITS!=="undefined" && PORTRAITS){
      if(!PORTRAITS.npc_lan) PORTRAITS.npc_lan = "assets/story/fullbody/lan_ruoxi_base.webp?v=20a176";
      if(!PORTRAITS.npc_xu) PORTRAITS.npc_xu = "assets/story/fullbody/tsui_poushan_base.webp?v=20a176";
      if(!PORTRAITS.npc_mei) PORTRAITS.npc_mei = "assets/story/fullbody/kwan_hoimei_base.webp?v=20a176";
    }
  }catch(_e){}
  return 1;
}
