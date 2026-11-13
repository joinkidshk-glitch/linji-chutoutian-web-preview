#!/usr/bin/env python3
"""v20a176 實作：將 qa176/rom176_block.js 插入 index.html＋其餘小改動。
全部替換 assert 命中次數；失敗即停，唔會靜默改錯。用法：python3 qa176/apply176.py"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "index.html"
s = P.read_text(encoding="utf-8")

def rep(old, new, expect=1, name=""):
    global s
    n = s.count(old)
    assert n == expect, f"{name}: 命中 {n} 次，預期 {expect} 次：{old[:90]!r}"
    s = s.replace(old, new)
    print(f"OK {name}")

# 1. NPCS：補藍／徐／海媚條目（key 用 romance key；homes＝主場＋副場）
rep(
"""  reporter:{ id:"reporter", name:"周采兒", role:"娛樂記者", face:"npc_chow",
    homes:["rec_star","film_cotton","tvb_harbour","ad_adm"] },""",
"""  reporter:{ id:"reporter", name:"周采兒", role:"娛樂記者", face:"npc_chow",
    homes:["rec_star","film_cotton","tvb_harbour","ad_adm"] },
  /* v20a176 ROM176：補藍／徐／海媚 NPCS 條目（隨機化必須嘅 plumbing；face 頭像＋傾談對白行 rom176ApplyGiftOverrides 注入） */
  lan:{ id:"lan", name:"藍若曦", role:"電視台場記", face:"npc_lan",
    homes:["tvb_longmen","tvb_kowloon"] },
  xu:{ id:"xu", name:"徐寶珊", role:"廣告界女強人", face:"npc_xu",
    homes:["ad_central","ad_adm"] },
  mei:{ id:"mei", name:"關海媚", role:"電視台台柱", face:"npc_mei",
    homes:["ad_adm","rec_hk"] },""",
    name="NPCS lan/xu/mei")

# 2. giveGift 回傳拎走 costsDay:true 殘留（現行規則係送禮唔耗日；v159 同款）
rep("kind, delta:applied, softcap, line, relKey, before, after, costsDay:true",
    "kind, delta:applied, softcap, line, relKey, before, after",
    name="giveGift costsDay 殘留")

# 3. enc79AddFav：週軟頂計數擴到包括 "gift"（對話＋送禮共用 10／週）
rep("/* 好感增減：巧遇來源（enc/beat）受每週軟頂＋級數上限；殺青（wrap）唔計軟頂、仍受級數上限；跌幅直扣 */",
    "/* 好感增減：巧遇／送禮來源（enc/beat/gift）受每週軟頂＋級數上限；殺青（wrap）唔計軟頂、仍受級數上限；跌幅直扣 */",
    name="enc79AddFav 註解")
rep('      if(src==="enc" || src==="beat"){',
    '      if(src==="enc" || src==="beat" || src==="gift"){',
    name="enc79AddFav 軟頂條件")
rep('      if((src==="enc" || src==="beat") && d>0) S.starFavWeek.gain = (S.starFavWeek.gain||0) + d;',
    '      if((src==="enc" || src==="beat" || src==="gift") && d>0) S.starFavWeek.gain = (S.starFavWeek.gain||0) + d;',
    name="enc79AddFav 軟頂入帳")

# 4. 載入點：GIFT_REACT 賦值之後呼叫 rom176ApplyGiftOverrides（同行 append，零行數漂移）
rep('    if(giftReact && (giftReact.byKey || giftReact.entries)) GIFT_REACT = giftReact; try{ if(typeof applyTangGift167==="function") applyTangGift167(); }catch(_t167){}',
    '    if(giftReact && (giftReact.byKey || giftReact.entries)) GIFT_REACT = giftReact; try{ if(typeof applyTangGift167==="function") applyTangGift167(); }catch(_t167){} try{ if(typeof rom176ApplyGiftOverrides==="function") rom176ApplyGiftOverrides(); }catch(_r176){}',
    name="載入點 rom176ApplyGiftOverrides")

# 5. addLocTalkGiftActs：拎走女角傾談＋送禮掣（非女角傾談掣不變；鄧麗萍掣唔喺呢度）
rep(
"""function addLocTalkGiftActs(add, L, npcId){
  // 人物／情報置頂，減少要滾先撳
  if(npcId) add(`同${NPCS[npcId].name}傾談`, talkHintLabel(), talkCostLabel(), ()=>doTalk(npcId,L), "act-priority");
  /* v18d／v19z：romance 送禮；soft 閘不耗日，live +1日 */
  try{
    if(npcId && typeof GiftShop!=="undefined"){
      const rk = GiftShop.romanceKeyFromMapNpc(npcId);
      if(rk){
        const gate = GiftShop.canGive(rk);
        const hint = giftHintLabel(gate.ok, gate.reason);
        /* 傾談已解鎖但庫存空：badge=庫存空，唔再標「未開放」 */
        add(`送禮：${NPCS[npcId].name}`, hint, giftGateBadge(gate), ()=>{
          const live = GiftShop.canGive(rk);
          if(!live.ok){ toast(live.reason||"暫不可送"); return; }
          openGiftPick(rk, L);
        }, (gate.ok || (/庫存|今天|今日|人情急/.test(String(gate.reason||""))))?"act-priority":"");
      }
    }
  }catch(_gf){}
}""",
"""function addLocTalkGiftActs(add, L, npcId){
  // 人物／情報置頂，減少要滾先撳
  /* v20a176 ROM176：六位女角唔再喺地點板傾談／送禮——要撞到先傾得／送得（明星志願嗰套）。
     非女角（導演／對手／何生）傾談掣不變；鄧麗萍送禮掣唔喺呢度（agency_ho 專屬段）。 */
  if(npcId && !(typeof rom176IsWomanNpc==="function" && rom176IsWomanNpc(npcId)))
    add(`同${NPCS[npcId].name}傾談`, talkHintLabel(), talkCostLabel(), ()=>doTalk(npcId,L), "act-priority");
}""",
    name="addLocTalkGiftActs 拎走女角掣")

# 6. openLoc：女角巧遇攔截行先過星巧遇
rep(
"""  /* v20a79 ENC79：紅星巧遇對話先行——有星在場（出沒盤）兼冇主線待播壓住，先播全屏巧遇對話，播完先開 sheet。
     opts.encDone 係巧遇播完返入嚟嘅繞過旗；forceRestore 還原路徑唔觸發。 */""",
"""  /* v20a176 ROM176：女角巧遇攔截——行先過星巧遇（同一入場只觸發一個；有女角嗰陣星唔彈）。
     opts.encDone 同星一樣係巧遇播完返入嚟嘅繞過旗；forceRestore 還原路徑唔觸發。 */
  if(!opts.forceRestore && !opts.encDone && typeof rom176TryIntercept==="function"){
    try{ if(rom176TryIntercept(id)) return; }catch(_e176){}
  }
  /* v20a79 ENC79：紅星巧遇對話先行——有星在場（出沒盤）兼冇主線待播壓住，先播全屏巧遇對話，播完先開 sheet。
     opts.encDone 係巧遇播完返入嚟嘅繞過旗；forceRestore 還原路徑唔觸發。 */""",
    name="openLoc rom176 攔截")

# 7. doTalk 返程：經 rom176BackOpts（巧遇入面傾完唔再擲星巧遇）
rep(
"""  const img = PORTRAITS[npc.face] || "";
  const go = ()=>{ if(ended) enterHome(summary, true); else if(spendDay) runScheduleFromToday(); else if(L) openLoc(L.id, {travelFree:true}); };""",
"""  const img = PORTRAITS[npc.face] || "";
  const go = ()=>{ const back176 = (typeof rom176BackOpts==="function") ? rom176BackOpts() : {travelFree:true}; if(ended) enterHome(summary, true); else if(spendDay) runScheduleFromToday(); else if(L) openLoc(L.id, back176); };""",
    name="doTalk 返程 rom176BackOpts")

# 8. doGiveGift：星分支＋返程經 rom176BackOpts
rep(
"""function doGiveGift(npcKey, itemId, L){
  const res = GiftShop.giveGift(npcKey, itemId);""",
"""function doGiveGift(npcKey, itemId, L){
  /* v20a176 ROM176：紅星送禮唔行 GiftShop.giveGift（calcDelta 夾死 +2／−1、會經 bumpRel 整出假 rel_<star>、
     另有每週 +2 軟頂）——行獨立星路徑（enc79AddFav "gift"，週軟頂 10 共用池）。 */
  if(typeof enc79StarDef==="function" && enc79StarDef(npcKey)){ rom176DoGiveStarGift(npcKey, itemId, L); return; }
  const res = GiftShop.giveGift(npcKey, itemId);""",
    name="doGiveGift 星分支")
rep(
"""  const go = ()=>{
    if(ended) enterHome(summary, true);
    else if(spendDay) runScheduleFromToday();
    else if(L) openLoc(L.id, {travelFree:true});
  };""",
"""  const go = ()=>{
    const back176 = (typeof rom176BackOpts==="function") ? rom176BackOpts() : {travelFree:true};
    if(ended) enterHome(summary, true);
    else if(spendDay) runScheduleFromToday();
    else if(L) openLoc(L.id, back176);
  };""",
    name="doGiveGift 返程 rom176BackOpts")

# 9. openGiftPick：星副標＋取消／dismiss 返程經 rom176BackOpts
rep(
"""    <p class="sub">${npcKey==="tang"?"每日限送 1 次 · 送禮只係公事心意，唔會改變排片關係":"每日每人限送 1 次；同一人一星期最多 +2 好感"}</p>""",
"""    <p class="sub">${npcKey==="tang"?"每日限送 1 次 · 送禮只係公事心意，唔會改變排片關係":((typeof enc79StarDef==="function" && enc79StarDef(npcKey))?"每日每星限送 1 份 · 好感計入每週上限（對話＋送禮共用 10 點）":"每日每人限送 1 次；同一人一星期最多 +2 好感")}</p>""",
    name="openGiftPick 星副標")
rep(
"""      {label:"取消", role:"g", on:()=>{ if(L) openLoc(L.id, {travelFree:true}); }}
    ], {onDismiss:()=>{ if(L) openLoc(L.id, {travelFree:true}); }});""",
"""      {label:"取消", role:"g", on:()=>{ if(L) openLoc(L.id, (typeof rom176BackOpts==="function") ? rom176BackOpts() : {travelFree:true}); }}
    ], {onDismiss:()=>{ if(L) openLoc(L.id, (typeof rom176BackOpts==="function") ? rom176BackOpts() : {travelFree:true}); }});""",
    name="openGiftPick 返程 rom176BackOpts")

# 10. enc79PlayEncounter：收尾嗰句加「送禮」掣
rep(
"""    nb.onclick = ()=>{
      if(step.segFx){ try{ step.segFx(); }catch(_g){} }
      idx++;
      render();
    };
    rowEl.appendChild(nb);""",
"""    nb.onclick = ()=>{
      if(step.segFx){ try{ step.segFx(); }catch(_g){} }
      idx++;
      render();
    };
    /* v20a176 ROM176：收尾嗰句加「送禮」——撞到先送得（星送禮入口）；撳咗就收起巧遇 overlay 去揀禮物。 */
    if(idx >= built.steps.length-1 && typeof rom176CanGiveStarGift==="function" && rom176CanGiveStarGift(starId)){
      const gb = document.createElement("button");
      gb.type = "button"; gb.className = "e79-btn e79-choice"; gb.textContent = "送禮畀" + def.name;
      gb.onclick = ()=>{
        try{ if(typeof rom176SetEncounter==="function") rom176SetEncounter({ kind:"star", starId:starId, locId:locId }); }catch(_g176){}
        finished = true;
        try{ ov.remove(); }catch(_r176){}
        try{ openGiftPick(starId, { id: locId }); }catch(_g176b){ try{ openLoc(locId, { encDone:true }); }catch(_e176){} }
      };
      rowEl.appendChild(gb);
    }
    rowEl.appendChild(nb);""",
    name="星巧遇收尾送禮掣")

# 11. enc79TeaListen：女角風聲 roll（0.35–0.50）＋toast 分支＋rumorId
rep(
"""  if(!gain){
    const pool = [];""",
"""  /* v20a176 ROM176：女角風聲（輕量版）——茶餐廳打聽有機會聽到女角行蹤，P≥0.80 窗 3 日。 */
  if(!gain && roll < 0.50 && typeof rom176TeaTargets==="function"){
    const targets = rom176TeaTargets();
    if(targets.length){
      const t = targets[Math.floor(Math.random()*targets.length)];
      gain = { kind:"romwhisper", key:t };
    }
  }
  if(!gain){
    const pool = [];""",
    name="茶聽女角風聲 roll")
rep(
"""  } else {
    const c = gain.card;""",
"""  } else if(gain.kind==="romwhisper"){
    const nm176 = (typeof rom176WomanName==="function") ? rom176WomanName(gain.key) : gain.key;
    try{ if(typeof rom176GrantWhisper==="function") rom176GrantWhisper(gain.key, "tea"); }catch(_w176){}
    toastMsg = "伙記擦枱嗰陣漏咗句風聲：" + nm176 + "呢幾日會出沒——記入手帳「傳聞 · 風聲」。";
  } else {
    const c = gain.card;""",
    name="茶聽女角風聲 toast")
rep(
"""  return { ok:true, added:true, updated:false, cleared:false, toast:toastMsg, rumorId: gain.kind==="frag" ? gain.card.id : ("wind:"+gain.starId+":"+day) };""",
"""  return { ok:true, added:true, updated:false, cleared:false, toast:toastMsg, rumorId: gain.kind==="frag" ? gain.card.id : (gain.kind==="romwhisper" ? ("romwind:"+gain.key+":"+day) : ("wind:"+gain.starId+":"+day)) };""",
    name="茶聽女角風聲 rumorId")

# 12. people72Html：女角出沒提示＋改提示文案
rep(
"""    const goBit = home
      ? `<div class="people-next"><button type="button" class="people-go" data-npc="${n.id}" data-loc="${home}">去找 · ${homeName||"地圖"}</button></div>`
      : "";
    return `<div class="people-row" style="margin:8px 0;display:flex;gap:8px;align-items:flex-start"><img src="${PORTRAITS[n.face]}" alt="" style="width:40px;height:52px;object-fit:cover;border-radius:6px;border:1px solid var(--line)"/><span style="flex:1"><b>${n.name}</b> · ${n.role}<br><span class="gold">${h} ${v}／100</span>${nextLine}${goBit}</span></div>`;""",
"""    const goBit = home
      ? `<div class="people-next"><button type="button" class="people-go" data-npc="${n.id}" data-loc="${home}">去找 · ${homeName||"地圖"}</button></div>`
      : "";
    /* v20a176 ROM176：女角行加出沒提示（見過寫「常喺」、未見寫「多數喺」；海媚未解鎖唔寫）。 */
    const rk176 = { colleague:"hiu", stylist:"vera", reporter:"choi", lan:"lan", xu:"xu", mei:"mei" }[n.id] || "";
    let haunt176 = "";
    if(rk176){
      const lockedMei176 = (rk176==="mei") && (typeof rom176MeiUnlocked==="function") && !rom176MeiUnlocked();
      if(!lockedMei176){
        const met176 = (typeof rom176WomanMet==="function") ? rom176WomanMet(rk176) : false;
        haunt176 = `<div class="people-next">${met176 ? "常喺" : "多數喺"}${homeName||"佢常去嘅地方"}出沒</div>`;
      }
    }
    return `<div class="people-row" style="margin:8px 0;display:flex;gap:8px;align-items:flex-start"><img src="${PORTRAITS[n.face]}" alt="" style="width:40px;height:52px;object-fit:cover;border-radius:6px;border:1px solid var(--line)"/><span style="flex:1"><b>${n.name}</b> · ${n.role}<br><span class="gold">${h} ${v}／100</span>${nextLine}${haunt176}${goBit}</span></div>`;""",
    name="人脈頁女角出沒提示")
rep(
"""<p class="sub" style="font-size:.75rem">撳「去找」會打開對方常出沒地點，可傾談／送禮。</p>""",
"""<p class="sub" style="font-size:.75rem">去佢常出沒嘅地方撞佢；撞到先可以傾談／送禮。</p>""",
    name="人脈頁提示文案")

# 13. enc79PeopleHtml：紅星段文案（「唔靠送禮」→撞到可以送禮）
rep(
"""紅星唔係熟人，冇得專程去揾：聽風聲、去常出沒嘅地方撞。交情靠撞見傾偈、同台做嘢，唔靠送禮。""",
"""紅星唔係熟人，冇得專程去揾：聽風聲、去常出沒嘅地方撞。撞到嗰陣可以傾偈、送禮。""",
    name="紅星段文案")

# 14. inv72Html：送禮入口提示（撞到先送得）
rep(
"""送禮：地圖遇到 Vera／林曉晴／周采兒，或者喺事務所見過鄧麗萍之後 →「送禮」（${softSocialCostsDay()?"耗 1 日":"唔耗日"}）。""",
"""送禮：喺地點撞到女角／紅星嗰陣先送得（地點板冇送禮掣）；喺事務所見過鄧麗萍之後 →「送禮」（${softSocialCostsDay()?"耗 1 日":"唔耗日"}）。""",
    name="庫存頁送禮提示")

# 15. 插入 ROM176 主 block（殺青回望之前）
block = (ROOT / "qa176" / "rom176_block.js").read_text(encoding="utf-8")
anchor = "/* ---------- 殺青回望（resolvePlannedDay 掛點） ---------- */"
assert s.count(anchor) == 1, f"殺青回望錨命中 {s.count(anchor)} 次"
s = s.replace(anchor, block + "\n" + anchor)
print("OK 插入 ROM176 block")

P.write_text(s, encoding="utf-8")
print("DONE，index.html 新行數：", s.count("\n") + 1)
