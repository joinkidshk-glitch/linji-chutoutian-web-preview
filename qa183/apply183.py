# v20a183 apply：一次過修 v176 review B1–B4＋C1–C9（用戶 2026-11-13 16:30 拍板）。
# 用法：python3 qa183/apply183.py — 對 index.html 做單次掃描取代，每對 old 必須恰好出現一次，
# 否則即停（唔做 blanket replace）。新行數只喺 ROM183 block 插入點＋TryIntercept／PlayEncounter
# 兩處增加；其餘全部原地改（行數不變），resync 見 qa183/resync183.py。
import io, sys

P = 'index.html'
s = io.open(P, encoding='utf-8').read()
orig = s
n = [0]

def rep(old, new, tag):
    global s
    c = s.count(old)
    assert c == 1, 'FAIL %s: 出現 %d 次 (預期 1)\nOLD: %s' % (tag, c, old[:120])
    s = s.replace(old, new)
    n[0] += 1
    print('ok %s' % tag)

# ---------- C5：.people-go 金字對比度 1.87:1 → 深啡字＋加深底（原地改） ----------
rep(
""".people-go, .debt-empty .debt-repay-btn{
  margin-top:6px; min-height:36px; padding:6px 12px; border-radius:10px;
  border:1px solid rgba(201,162,39,.55); background:rgba(201,162,39,.12);
  color:var(--gold,#c9a227); font-weight:700; font-size:.78rem; cursor:pointer;
}""",
""".people-go, .debt-empty .debt-repay-btn{
  margin-top:6px; min-height:36px; padding:6px 12px; border-radius:10px;
  border:1px solid rgba(90,67,40,.65); background:rgba(201,162,39,.28);
  color:#5a4328; font-weight:700; font-size:.78rem; cursor:pointer;
}""",
'C5 people-go 對比度')

# ---------- C7：700 禮物選擇器兩欄（原地 append 去現有 CSS 行，零行數漂移） ----------
rep(
".people-go:active, .debt-empty .debt-repay-btn:active{ transform:scale(.98); }",
""".people-go:active, .debt-empty .debt-repay-btn:active{ transform:scale(.98); }
/* v20a183 C7：700 禮物選擇器兩欄排（10 行變 5 行），尾 3 件唔使碌；取消掣 pinned 不變 */
@media (max-height:720px){ #gift-pick-list{ display:grid; grid-template-columns:1fr 1fr; gap:4px 8px; } #gift-pick-list .act{ margin-bottom:0 !important; padding:6px 8px !important; } }""",
'C7 700 picker 兩欄')

# ---------- C6：教學 inline fallback TUT_NPC 加一句隨機巧遇說明（原地改） ----------
rep(
"\"body\":[\"喺茶餐廳或者事務所「打聽」唔耗日，打聽返嚟嘅傳聞會記入手帳。\",\"而家同熟人傾談或者送禮都唔會計一日（茶錢照扣）；只有訓練、試鏡、休息同跟行程開工先會計日。\"]",
"\"body\":[\"喺茶餐廳或者事務所「打聽」唔耗日，打聽返嚟嘅傳聞會記入手帳。\",\"而家同熟人傾談或者送禮都唔會計一日（茶錢照扣）；只有訓練、試鏡、休息同跟行程開工先會計日。去佢哋常出沒嘅地方，有機會撞到佢哋——撞到先可以傾談／送禮。\"]",
'C6 教學 inline 加巧遇句')
# v20a183 C6 修正：live 教學只行 TUT_MAIN_IDS 四步（TUT_WELCOME／MAP／BOARD／DONE），TUT_NPC 唔顯示；
# 巧遇句要落喺 TUT_MAP body 做第三句先見到（TUT_NPC 嗰句保留，覆蓋重看／其他路徑）。
rep(
"\"body\":[\"地圖上面嘅地點，就係你可以去嘅地方；要先撳入地點，先睇到有咩行動。\",\"能力未夠，就去報名訓練；喺茶餐廳或者事務所「打聽」唔耗日，打聽返嚟嘅傳聞會記入手帳。\"]",
"\"body\":[\"地圖上面嘅地點，就係你可以去嘅地方；要先撳入地點，先睇到有咩行動。\",\"能力未夠，就去報名訓練；喺茶餐廳或者事務所「打聽」唔耗日，打聽返嚟嘅傳聞會記入手帳。\",\"去佢哋常出沒嘅地方，有機會撞到佢哋——撞到先可以傾談／送禮。\"]",
'C6 教學 inline TUT_MAP 加巧遇句（修正）')

# ---------- B2：prefKind 分最愛／喜歡；calcDelta／reactionEntry／reactionLine 跟住認 favorite ----------
rep(
"""  function prefKind(npcKey, itemId){
    const pref = prefFor(npcKey) || { likes:[], dislikes:[] };
    if((pref.likes||[]).indexOf(itemId)>=0) return "liked";""",
"""  function prefKind(npcKey, itemId){
    const pref = prefFor(npcKey) || { likes:[], dislikes:[] };
    if((pref.favorites||[]).indexOf(itemId)>=0) return "favorite"; /* v20a183 B2：最愛獨立回傳，唔再併入 liked */
    if((pref.likes||[]).indexOf(itemId)>=0) return "liked";""",
'B2 prefKind 最愛獨立')
rep(
"""    let delta = kind==="liked" ? (Number(dr.liked)||2)""",
"""    let delta = (kind==="liked" || kind==="favorite") ? (Number(dr.liked)||2) /* v20a183 B2：最愛同喜歡同數（女角 +2；星數值行 rom176StarDelta，唔經呢度） */""",
'B2 calcDelta 最愛同數')
rep(
"""    const prefKey = (pref==="dislike") ? "dislike" : pref;""",
"""    const prefKey = (pref==="dislike") ? "dislike" : (pref==="favorite" ? "liked" : pref); /* v20a183 B2：最愛查句行 :liked（女角 pack 得 :liked 句） */""",
'B2 reactionEntry 最愛查 liked')
rep(
"""    if(pref==="liked") return lines.liked || "佢接過禮物，笑住講：「你記性真好。」";""",
"""    if(pref==="liked" || pref==="favorite") return lines.liked || "佢接過禮物，笑住講：「你記性真好。」"; /* v20a183 B2：最愛 fallback 同喜歡 */""",
'B2 reactionLine 最愛 fallback')

# ---------- B2：openGiftPick 最愛標記「★ 最愛」＋確認 modal 寫明 ----------
rep(
"""    const kind = GiftShop.prefKind(npcKey, itemId);
    const tag = kind==="liked"?"喜":(kind==="dislike"?"慎":"普");""",
"""    const kind = GiftShop.prefKind(npcKey, itemId);
    const tag = kind==="favorite"?"★ 最愛":(kind==="liked"?"喜":(kind==="dislike"?"慎":"普")); /* v20a183 B2：最愛獨立標記，唔同「喜」撞色撞字 */""",
'B2 picker 最愛標記')
rep(
"""      btn.addEventListener("click", ()=>{
        const id = btn.getAttribute("data-give");
        const it = GiftShop.itemById(id);
        modal(`<h3>確認送禮</h3>
          <p>把「<b>${(it&&it.name)||id}</b>」送給 <b>${name}</b>？</p>
          <p class="sub">${giftConfirmCostLine()}</p>`,[""",
"""      btn.addEventListener("click", ()=>{
        const id = btn.getAttribute("data-give");
        const it = GiftShop.itemById(id);
        const kind183 = GiftShop.prefKind(npcKey, id);
        const kindLine183 = kind183==="favorite" ? `<p class="sub">★ 最愛：佢最鍾意呢樣禮物。</p>` : kind183==="liked" ? `<p class="sub">佢幾鍾意呢樣。</p>` : kind183==="dislike" ? `<p class="sub">佢未必鍾意呢樣，要諗清楚。</p>` : "";
        modal(`<h3>確認送禮</h3>
          <p>把「<b>${(it&&it.name)||id}</b>」送給 <b>${name}</b>？</p>
          ${kindLine183}
          <p class="sub">${giftConfirmCostLine()}</p>`,[""",
'B2 確認 modal 最愛句')

# ---------- C1／C6 呼叫點：pack 載入＋清洗之後行 rom183 覆寫（同行 append，零行數漂移） ----------
rep(
"""    try{ textfix55SimplePack(d); }catch(_t55){}""",
"""    try{ textfix55SimplePack(d); }catch(_t55){} try{ if(typeof rom183ApplyLineOverrides==="function") rom183ApplyLineOverrides(); }catch(_e183){} /* v20a183 C1/C6：NPC_LINES 粵語 greet＋教學巧遇句，載入正規化（唔直改 pack JSON） */""",
'C1/C6 覆寫呼叫點')
rep(
"""    try{ if(giftReact) textfix55Walk(giftReact, null, null, TEXTFIX55_OPTS_GIFT); }catch(_t55){}""",
"""    try{ if(giftReact) textfix55Walk(giftReact, null, null, TEXTFIX55_OPTS_GIFT); }catch(_t55){} try{ if(typeof rom183ApplyGiftReactFix==="function") rom183ApplyGiftReactFix(); }catch(_e183){} /* v20a183 C3：55 條女角反應句過粵語 filter（清洗之後行，唔直改 pack JSON） */""",
'C3 覆寫呼叫點')

# ---------- C2：ROM176_GREET.xu 改初遇版（見過版搬去 ROM183_GREET_MET） ----------
rep(
"""  xu:"徐寶珊：「後生仔，行路望路呀。咦，係你——上次春茗撞過嗰個。」",""",
"""  xu:"徐寶珊：「後生仔，行路望路呀。咦，係你——啱啱先撞到，唔好意思。」", /* v20a183 C2：初遇版，唔預設春茗；見過版喺 ROM183_GREET_MET */""",
'C2 ROM176_GREET.xu 初遇版')
# ---------- C4：ROM176_GREET.mei 刪舞台指示 ----------
rep(
"""  mei:"關海媚：「咁啱，喺呢度撞到你。」（佢望咗你一眼，冇即刻行開。）",""",
"""  mei:"關海媚：「咁啱，喺呢度撞到你。」", /* v20a183 C4：刪括號舞台指示，淨留對白 */""",
'C4 ROM176_GREET.mei')

# ---------- C2／C4：NL176 注入表同款（index.html code，唔係 pack JSON） ----------
rep(
"""          greet:["後生仔，行路望路呀。咦，係你——上次春茗撞過嗰個。","你喺呢度做咩？廣告公司唔係片場，唔好周圍望。"],""",
"""          greet:["後生仔，行路望路呀。咦，係你——啱啱先撞到，唔好意思。","你喺呢度做咩？廣告公司唔係片場，唔好周圍望。"], /* v20a183 C2：同 ROM176_GREET.xu */""",
'C2 NL176.xu 初遇版')
rep(
"""          greet:["咁啱，喺呢度撞到你。","（佢望咗你一眼，冇即刻行開。）有嘢搵我？"],""",
"""          greet:["咁啱，喺呢度撞到你。","有嘢搵我？"], /* v20a183 C4：刪括號舞台指示，淨留對白 */""",
'C4 NL176.mei')

# ---------- C2：TryIntercept 設旗前捕捉見過未；doneToday 記埋地點（B3 用） ----------
rep(
"""    /* 觸發入帳（跳過都計，防刷）：冷卻／上限／次數即時生效；撞到呢次即計見過 */
    sd.triggered = (sd.triggered||0) + 1;
    S.romWeek.count = (S.romWeek.count||0) + 1;
    sd.doneToday[pick.key] = 1;""",
"""    /* 觸發入帳（跳過都計，防刷）：冷卻／上限／次數即時生效；撞到呢次即計見過 */
    const metBefore183 = rom176WomanMet(pick.key); /* v20a183 C2：設旗前捕捉見過未（設旗後再問永遠係見過） */
    sd.triggered = (sd.triggered||0) + 1;
    S.romWeek.count = (S.romWeek.count||0) + 1;
    sd.doneToday[pick.key] = locId; /* v20a183 B3：記埋邊個地點撞到，等地點板在場行跟返巧遇盤 */""",
'C2/B3 TryIntercept 入帳')
rep(
"""    rom176PlayEncounter(pick.key, locId);
    return true;""",
"""    rom176PlayEncounter(pick.key, locId, metBefore183);
    return true;""",
'C2 PlayEncounter 傳 metBefore')

# ---------- C2：PlayEncounter 徐寶珊分見過／未見過；B1：modal 加好感行 ----------
rep(
"""function rom176PlayEncounter(key, locId){""",
"""function rom176PlayEncounter(key, locId, metBefore183){""",
'C2 PlayEncounter 簽名')
rep(
"""  let greet = ROM176_GREET[key] || "";
  try{
    const pack = ((typeof NPC_LINES!=="undefined" ? NPC_LINES : null) || {})[def.npcId]
      || ((typeof NPC_LINES_CORE!=="undefined" ? NPC_LINES_CORE : null) || {})[def.npcId];
    if(pack && Array.isArray(pack.greet) && pack.greet.length) greet = pack.greet[0];
  }catch(_g){}""",
"""  let greet = ROM176_GREET[key] || "";
  try{
    const pack = ((typeof NPC_LINES!=="undefined" ? NPC_LINES : null) || {})[def.npcId]
      || ((typeof NPC_LINES_CORE!=="undefined" ? NPC_LINES_CORE : null) || {})[def.npcId];
    if(pack && Array.isArray(pack.greet) && pack.greet.length) greet = pack.greet[0];
  }catch(_g){}
  /* v20a183 C2：徐寶珊見過先講「上次春茗」，未見過講初遇版（pack 冇 xu，行 ROM176_GREET／ROM183_GREET_MET）。 */
  if(key==="xu"){ const met183 = (typeof metBefore183==="boolean") ? metBefore183 : rom183XuMetBefore183(); greet = met183 ? ROM183_GREET_MET.xu : (ROM176_GREET.xu || greet); }""",
'C2 PlayEncounter 徐寶珊分版')
rep(
"""    + "<p class=\\"sub\\">喺"+(L.name||locId)+"撞到佢。傾談／送禮唔耗日；今日唔會再撞到佢。</p>",""",
"""    + "<p class=\\"sub\\">喺"+(L.name||locId)+"撞到佢。傾談／送禮唔耗日；今日唔會再撞到佢。"+rom183RelText183(key)+"</p>",""",
'B1 modal 好感行')

# ---------- B3：地點板在場行跟返巧遇盤 ----------
rep(
"""  let who = hub ? "" : (npcId ? `在場：${NPCS[npcId].name}（${NPCS[npcId].role}）` : "");""",
"""  let who = hub ? "" : rom183WhoLine183(L, npcId); /* v20a183 B3：在場行跟返巧遇盤（啱啱撞過嗰位優先，唔再話另一位「在場」） */""",
'B3 who 行跟巧遇盤')

# ---------- B1／B4／C8：人脈頁女角行 ----------
rep(
"""    const rk176 = { colleague:"hiu", stylist:"vera", reporter:"choi", lan:"lan", xu:"xu", mei:"mei" }[n.id] || "";""",
"""    const rk176 = { colleague:"hiu", stylist:"vera", reporter:"choi", lan:"lan", xu:"xu", mei:"mei" }[n.id] || ""; const rel183 = (typeof rom183RelLine183==="function") ? rom183RelLine183(rk176) : ""; /* v20a183 B1：感情進度行（讀 S.story.rel，淨顯示，鎖邏輯唔郁） */""",
'B1 人脈頁 rel 行變數')
rep(
"""    const goBit = home
      ? `<div class="people-next"><button type="button" class="people-go" data-npc="${n.id}" data-loc="${home}">去找 · ${homeName||"地圖"}</button></div>`
      : "";""",
"""    const lockedMeiGo183 = (rk176==="mei") && (typeof rom176MeiUnlocked==="function") && !rom176MeiUnlocked(); /* v20a183 B4：海媚未解鎖，掣唔生效 */
    const goBit = home
      ? (lockedMeiGo183 ? `<div class="people-next">主線再行前啲先撞到佢</div>` : `<div class="people-next"><button type="button" class="people-go" data-npc="${n.id}" data-loc="${home}">去 ${homeName||"地圖"} 行下</button></div>`)
      : "";""",
'B4/C8 海媚鎖掣＋掣名改行下')
rep(
"""    return `<div class="people-row" style="margin:8px 0;display:flex;gap:8px;align-items:flex-start"><img src="${PORTRAITS[n.face]}" alt="" style="width:40px;height:52px;object-fit:cover;border-radius:6px;border:1px solid var(--line)"/><span style="flex:1"><b>${n.name}</b> · ${n.role}<br><span class="gold">${h} ${v}／100</span>${nextLine}${haunt176}${goBit}</span></div>`;""",
"""    return `<div class="people-row" style="margin:8px 0;display:flex;gap:8px;align-items:flex-start"><img src="${PORTRAITS[n.face]}" alt="" style="width:40px;height:52px;object-fit:cover;border-radius:6px;border:1px solid var(--line)"/><span style="flex:1"><b>${n.name}</b> · ${n.role}<br><span class="gold">${h} ${v}／100</span>${nextLine}${haunt176}${rel183}${goBit}</span></div>`;""",
'B1 人脈頁 rel 行接入')

# ---------- C9：開局 intro 入場唔計出行額度 ----------
rep(
"""              openLoc(locId);
              toast(committed ? ("已用預設行程 · 到"+c1Where+"可播開局劇情") : ("到"+c1Where+"先可播開局劇情"));""",
"""              openLoc(locId, {travelFree:true}); /* v20a183 C9：開局 intro（屋企 modal「去睇劇情」掣）係系統引導入場，唔計出行額度 */
              toast(committed ? ("已用預設行程 · 到"+c1Where+"可播開局劇情") : ("到"+c1Where+"先可播開局劇情"));""",
'C9 intro 入場免費')

# ---------- TDZ 修正：rk176 宣告行要喺 lockedMeiGo183 之前（原位置喺 goBit 之後，直接讀會 TDZ） ----------
# 行數不變：將 rk176 行（連 rel183）由 goBit 之後搬去 home 行之前。
_rk183 = '    const rk176 = { colleague:"hiu", stylist:"vera", reporter:"choi", lan:"lan", xu:"xu", mei:"mei" }[n.id] || ""; const rel183 = (typeof rom183RelLine183==="function") ? rom183RelLine183(rk176) : ""; /* v20a183 B1：感情進度行（讀 S.story.rel，淨顯示，鎖邏輯唔郁） */'
assert s.count(_rk183) == 1, 'FAIL rk176 行搬前：搵唔到／唔唯一'
s = s.replace(_rk183 + '\n', '', 1)
_home183 = '    const home = (n.id==="agent") ? "agency_ho" : ((n.homes && n.homes[0]) || "");'
assert s.count(_home183) == 1, 'FAIL rk176 行搬前：home 行搵唔到'
s = s.replace(_home183, _rk183 + '\n' + _home183, 1)
n[0] += 1
print('ok B1/B4 rk176 搬前（TDZ 修正，行數不變）')

# ---------- ROM183 block：插入喺 rom176ApplyGiftOverrides 之後、殺青回望之前 ----------
anchor = """/* ---------- 殺青回望（resolvePlannedDay 掛點） ---------- */"""
assert s.count(anchor) == 1, 'FAIL anchor 殺青回望'
block = """/* ===== v20a183 ROM183：修 v176 設計 review B1–B4＋C1–C9（用戶 2026-11-13 16:30 拍板一次過修）。
   全部顯示／文案／入口層修法：唔改 SAVE key／softRev／?v=，唔直改 content/ pack JSON（C1／C3／C6
   行載入正規化，呼叫點喺 pack 賦值＋TEXTFIX55 清洗之後），唔改鎖邏輯（B1 淨顯示；B4 淨係收起
   未解鎖嘅掣；C9 淨係開局 intro 入場免費，travel114 上限／計數本身唔郁）。===== */
const ROM183_GREET_MET = {
  xu:"徐寶珊：「後生仔，行路望路呀。咦，係你——上次春茗撞過嗰個。」", /* C2：見過版（只喺 metBefore183 嗰陣用） */
};
const ROM183_PACK_GREET = { /* C1：三位舊女角 pack greet[0] 粵語版（ROM176_GREET 嗰句去 speaker 前綴） */
  colleague:"咦，阿偉？咁啱嘅，喺呢度撞到你。",
  stylist:"咁啱。你今日呢身……算啦，唔講住，行埋嚟傾兩句。",
  reporter:"阿偉！啱啱好，我有單嘢想問你——唔係訪問，純粹八卦。",
};
function rom183XuMetBefore183(){
  try{
    if(typeof StoryOC!=="undefined" && StoryOC.isDone) return !!StoryOC.isDone("R_xu_meet");
    if(S && S.story && S.story.done) return !!S.story.done["R_xu_meet"];
  }catch(_e){}
  return false;
}
function rom183RelVal183(key){
  try{
    if(!key) return 0;
    if(typeof StoryOC!=="undefined" && StoryOC.getRel) return Number(StoryOC.getRel("rel_"+key))||0;
    if(S && S.story && S.story.rel) return Number(S.story.rel["rel_"+key])||0;
  }catch(_e){}
  return 0;
}
function rom183RelText183(key){ /* B1：巧遇 modal 細字（rel 0 嗰陣都出，等玩家知有呢條數） */
  try{ if(!key) return ""; return "而家好感 "+rom183RelVal183(key)+"／5。"; }catch(_e){ return ""; }
}
function rom183RelLine183(rk){ /* B1：人脈頁女角行感情進度（淨顯示，讀 S.story.rel） */
  try{ if(!rk) return ""; return '<div class="people-next">感情：好感 '+rom183RelVal183(rk)+'／5</div>'; }catch(_e){ return ""; }
}
function rom183WhoLine183(L, npcId){ /* B3：地點板在場行——今日喺呢度撞過嘅女角優先 */
  try{
    if(L && typeof S!=="undefined" && S && S.romDay && S.romDay.day===(S.dayIndex|0) && S.romDay.doneToday){
      for(const k in S.romDay.doneToday){
        if(S.romDay.doneToday[k]!==L.id) continue;
        const d = (typeof rom176WomanDef==="function") ? rom176WomanDef(k) : null;
        if(!d) continue;
        const npc = (typeof NPCS!=="undefined") ? NPCS[d.npcId] : null;
        return "在場："+d.name+"（"+(npc ? npc.role : "")+"） · 今日已經撞過佢，聽日再嚟";
      }
    }
  }catch(_e){}
  return npcId ? ("在場："+NPCS[npcId].name+"（"+NPCS[npcId].role+"）") : "";
}
function rom183ApplyLineOverrides(){ /* C1：pack greet[0] 改粵語（runtime 覆寫，唔直改 pack JSON）；C6：教學加巧遇句 */
  try{
    const NL = (typeof NPC_LINES!=="undefined" ? NPC_LINES : null) || null;
    if(NL){
      for(const id in ROM183_PACK_GREET){
        if(NL[id] && Array.isArray(NL[id].greet) && NL[id].greet.length) NL[id].greet[0] = ROM183_PACK_GREET[id];
      }
    }
  }catch(_e){}
  try{
    const TUTS = [];
    if(typeof TUTORIAL!=="undefined" && TUTORIAL) TUTS.push(TUTORIAL);
    if(typeof TUTORIAL_ZH_HK!=="undefined" && TUTORIAL_ZH_HK && TUTS.indexOf(TUTORIAL_ZH_HK)<0) TUTS.push(TUTORIAL_ZH_HK);
    const LINE183 = "去佢哋常出沒嘅地方，有機會撞到佢哋——撞到先可以傾談／送禮。";
    TUTS.forEach(t=>{
      const steps = (t && Array.isArray(t.steps)) ? t.steps : [];
      steps.forEach(st=>{
        if(!st) return; if(st.id==="TUT_MAP"){ if(Array.isArray(st.body) && st.body.join("").indexOf("撞到")<0) st.body.push(LINE183); } else if(st.id!=="TUT_NPC") return; /* v20a183 C6 修正：live 教學只行 TUT_MAIN_IDS 四步，TUT_NPC 唔顯示，巧遇句要落喺 TUT_MAP 先見到 */
        ["body","bodyAlt"].forEach(k=>{
          const arr = st[k];
          if(Array.isArray(arr) && arr.length>1 && typeof arr[1]==="string" && arr[1].indexOf("撞到")<0) arr[1] = arr[1] + LINE183;
        });
      });
    });
  }catch(_e){}
  return 1;
}
function rom183ApplyGiftReactFix(){ /* C3：55 條女角反應句過粵語 filter（runtime 覆寫 byKey＋entries 兩份，唔直改 pack JSON） */
  try{
    const R = (typeof GIFT_REACT!=="undefined" && GIFT_REACT) || null;
    if(!R) return 0;
    const EXACT183 = {
      "Vera：「這條顏色很乾淨，不會搶鏡頭，也適合日常出門。你有想過我平常穿什麼，還是碰巧選中？」": "Vera：「呢條色幾乾淨，唔會搶鏡，平時出街都啱著。你有冇諗過我平時著咩，定係撞啱？」",
      "Vera：「花可以，包裝也不俗氣。你是想說什麼，還是只想我看見紅色？」": "Vera：「花得，包裝都唔老土。你想講咩，定係只想我見到紅色？」",
      "Vera：「實用就好。造型間很乾，有熱水比什麼都實際。」": "Vera：「實用就好。造型間好乾，有熱水好過咩。」",
      "林曉晴：「保溫瓶？你是不是看見我冬天抱著紙杯發抖？太實用了。」": "林曉晴：「保溫瓶？你係咪見到我冬天抱住紙杯震？真係實用。」",
      "林曉晴：「我可以裝熱水，也可以裝涼茶。這份心意比什麼名牌都實際，謝謝你。」": "林曉晴：「裝熱水得，裝涼茶都得。呢份心意比咩名牌都實際，唔該你。」",
      "林曉晴：「我現在就夾上——你看看，是不是整齊一點？」": "林曉晴：「我而家就夾上——你睇下，係咪整齊啲？」",
      "林曉晴：「卡帶？是不是你從哪個通告聽來的？我最喜歡這種『有人記掛你』的情報味。」": "林曉晴：「卡帶？係咪你喺邊個通告聽返嚟？我最鍾意呢種『有人記掛你』嘅情報味。」",
      "林曉晴：「這……也太貴重了。你是不是搞錯對象？我只是臨記，收這個會睡不著。」": "林曉晴：「呢樣……貴重得滯。你係咪搞錯咗對象？我只係個臨記，收呢樣會瞓唔著。」",
      "藍若曦：「換別的吧。卡帶、小甜品，什麼都好，別用香味包裝我。」": "藍若曦：「換第二樣啦。卡帶、小甜品，咩都好，唔好用香味包裝我。」",
      "徐寶珊：「年份還過得去。你開始懂，場上什麼叫『識玩』。」": "徐寶珊：「年份都仲過得去。你開始識，場上咩叫『識玩』。」",
    };
    const fixLine = (ln)=>{
      if(typeof ln!=="string") return ln;
      if(Object.prototype.hasOwnProperty.call(EXACT183, ln)) return EXACT183[ln];
      if(ln.indexOf("是不是")<0 && ln.indexOf("什麼")<0) return ln;
      return ln.split("是不是").join("係咪").split("什麼").join("咩");
    };
    const fixEnt = (ent)=>{
      if(!ent || !Array.isArray(ent.lines)) return;
      for(let i=0;i<ent.lines.length;i++) ent.lines[i] = fixLine(ent.lines[i]);
      if(typeof ent.narration==="string") ent.narration = fixLine(ent.narration);
    };
    (R.entries||[]).forEach(fixEnt);
    if(R.byKey && typeof R.byKey==="object") for(const k in R.byKey) fixEnt(R.byKey[k]);
    return 1;
  }catch(_e){ return 0; }
}

"""
s = s.replace(anchor, block + anchor)
n[0] += 1
print('ok ROM183 block 插入')

io.open(P, 'w', encoding='utf-8').write(s)
print('取代 %d 處；行數 %d → %d' % (n[0], orig.count('\n') + 1, s.count('\n') + 1))
