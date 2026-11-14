# -*- coding: utf-8 -*-
"""v20a211 apply：七項改動（A1／B1／B2／C1／C2／C3＋B7），逐個字串替換＋次數核實。"""
import sys

p = "index.html"
src = open(p, encoding="utf-8").read()
orig = src

def rep(old, new, n=1, label=""):
    global src
    c = src.count(old)
    assert c == n, f"{label}: expected {n}, found {c}: {old[:90]!r}"
    src = src.replace(old, new)

# ---------- A1：結果卡開出嗰刻收起 toast ----------
rep("""function show(id){document.querySelectorAll(".view").forEach(v=>v.classList.remove("on"));document.getElementById(id).classList.add("on")}""",
"""function hideToast211(){ /* v20a211 A1：結果卡開出嗰刻收起 toast——toast 本身係「結果已出」通知，開卡後已無用；清計時＋class，唔等 1.8s 自然熄（v207 實駕見 toast 喺 700 提名版遮住眉題）；toast() 本身一字唔改，其他 toast 用途唔受影響。 */
  try{ clearTimeout(toast._t); }catch(_e){}
  const t = document.getElementById("toast");
  if(t){ t.classList.remove("on","has-stamp","has-sub"); t.replaceChildren(); t.setAttribute("aria-hidden","true"); }
  const app = document.getElementById("app");
  if(app) app.classList.remove("toast-up","keep-sheet");
}
function show(id){document.querySelectorAll(".view").forEach(v=>v.classList.remove("on"));document.getElementById(id).classList.add("on")}""",
    label="A1 helper")
rep("""    modal(renderAwardResultHtml(pack), [
      { label: "收下這晚", role: "p", on: cont }
    ], { onDismiss: cont, keepSheetContent:true, awardSheet:true }); /* v20a207 C3：結果卡掛 awd-sheet-on 放寬 88dvh */
    try{ toast((pack.displayName||"頒獎夜")+"・結果", { sub: pack.tierLabel||"", stamp:true }); }catch(_e){}""",
"""    try{ hideToast211(); }catch(_e){} /* v20a211 A1：開卡前收起 toast（唔再開卡後即叫 toast()——嗰句就係遮住 700 提名版眉題嘅元兇） */
    modal(renderAwardResultHtml(pack), [
      { label: "收下這晚", role: "p", on: cont }
    ], { onDismiss: cont, keepSheetContent:true, awardSheet:true }); /* v20a207 C3：結果卡掛 awd-sheet-on 放寬 88dvh */""",
    label="A1 present")

# ---------- C3：請柬席位去重（gallery 先刪，nominee 保留） ----------
rep("""  const tierBit = pack.tierLabel ? `<p class="psr-sub">席位：${pack.tierLabel}</p>` : "";""",
"""  /* v20a211 C3：gallery 請柬席位去重——tierBit「席位：旁聽席」同下面 gate 行「今晚席位：觀禮。」講同一樣嘢，gallery 嗰陣唔出 tierBit；nominee 嗰陣 gate 行係入圍門檻句、唔講席位，tierBit「席位：入圍／提名」保留。 */
  const tierBit = (pack.tier === "gallery") ? "" : (pack.tierLabel ? `<p class="psr-sub">席位：${pack.tierLabel}</p>` : "");""",
    label="C3 tierBit")

# ---------- B2：won 版銷量卡點名得主＋作品 ----------
rep("""  const win149 = (typeof awardWinner149 === "function") ? awardWinner149(pack) : null;
  const metricLine = pack.metricEcho
    ? `<article class="psr-card psr-metrics">
        <div class="psr-kicker"><span class="psr-icon">${iconHtml112("✨")}</span> ${pack.metricEchoLabel||"餘韻"}</div>
        <h4 class="psr-title">${win149 ? ((pack.metricEchoLabel||"") + "——" + awardWinLine149(win149) + "，典禮後仍有人提起。") : ((pack.metricEchoLabel||"")+"——典禮後仍有人提起。")}</h4>
      </article>` : "";""",
"""  const win149 = (typeof awardWinner149 === "function") ? awardWinner149(pack) : null;
  /* v20a211 B2：won 版銷量卡唔再係 stub——awardWinner149 喺 won 分支刻意回 null（得主係阿偉，唔係對手），
     呢度由 won 類別攞返玩家＋代表作（動態，唔寫死作品名），沿用同一模板：「阿偉憑《冬日暖歌賀歲合唱》奪獎，典禮後仍有人提起。」 */
  const wonCat211 = (Array.isArray(pack.categories) ? pack.categories : []).find(c=> c && c.outcome === "won") || null;
  const win211 = win149 || (wonCat211 ? { star: "阿偉", title: (wonCat211.repWorkTitle || pack.repWork62 || "") } : null);
  const metricLine = pack.metricEcho
    ? `<article class="psr-card psr-metrics">
        <div class="psr-kicker"><span class="psr-icon">${iconHtml112("✨")}</span> ${pack.metricEchoLabel||"餘韻"}</div>
        <h4 class="psr-title">${win211 ? ((pack.metricEchoLabel||"") + "——" + awardWinLine149(win211) + "，典禮後仍有人提起。") : ((pack.metricEchoLabel||"")+"——典禮後仍有人提起。")}</h4>
      </article>` : "";""",
    label="B2 metric")

# ---------- C1：won 版同屆提名加玩家一行（金 chip 得主標記） ----------
rep("""  const winRaw = c.winner63 || ((c.outcome === "gallery" && fl[0]) ? fl[0] : null) || null;
  const win = (winRaw && typeof winRaw === "object") ? winRaw : ((typeof winRaw === "string" && winRaw) ? { star: winRaw, title: "" } : null);
  const parts = fl.map(f=>{
    const isW = win && f.star === win.star && (!win.title || f.title === win.title);
    return (isW ? iconHtml112("🏆") + " " : "") + f.star + "《" + f.title + "》";
  });
  const head = win ? ("同屆提名（" + iconHtml112("🏆") + " 為得主）") : "同屆提名";
  return '<p class="psr-fellows63">' + head + "：" + parts.join("、") + "</p>";""",
"""  const winRaw = c.winner63 || ((c.outcome === "gallery" && fl[0]) ? fl[0] : null) || null;
  const win = (winRaw && typeof winRaw === "object") ? winRaw : ((typeof winRaw === "string" && winRaw) ? { star: winRaw, title: "" } : null);
  const parts = fl.map(f=>{
    const isW = win && f.star === win.star && (!win.title || f.title === win.title);
    return (isW ? iconHtml112("🏆") + " " : "") + f.star + "《" + f.title + "》";
  });
  /* v20a211 C1：won 版同屆提名加玩家一行——得主係阿偉，唔喺 fellows 名單入面，舊寫法行首無圖例、無任何 🏆 標記，
     讀者唔知第四個提名人去咗邊。加「阿偉《代表作》🏆」做第一項（代表作由 c.repWorkTitle 動態取，金底 chip 同 v207 C2 一致），行首一併加圖例。 */
  const isWon211 = c.outcome === "won";
  if(isWon211){
    const meTitle211 = c.repWorkTitle || "";
    parts.unshift(iconHtml112("🏆") + " 阿偉" + (meTitle211 ? "《" + meTitle211 + "》" : ""));
  }
  const head = (win || isWon211) ? ("同屆提名（" + iconHtml112("🏆") + " 為得主）") : "同屆提名";
  return '<p class="psr-fellows63">' + head + "：" + parts.join("、") + "</p>";""",
    label="C1 fellows")

# ---------- C2：字幕框高度釘死 93px ----------
rep(""".awd62-caption{margin-top:10px;background:#1d1430;border:3px solid #8a6d2f;box-shadow:4px 4px 0 #0d0918;color:#ffe9b0;padding:8px 12px;min-height:54px; /* v20a207 B2：padding 10→8，提名 700 留 4px */font-size:15px;line-height:1.55;text-align:center;white-space:pre-line}""",
""".awd62-caption{margin-top:10px;background:#1d1430;border:3px solid #8a6d2f;box-shadow:4px 4px 0 #0d0918;color:#ffe9b0;padding:8px 12px;height:93px; /* v20a211 C2：字幕框高度釘死 93px（全域 border-box，93 即總高）——基線實測 names 69px／suspense 54px／reveal 54–93px 來回跳，frame 跟住跳 7–12px（music 提名 700 係 24px）；93＝實測最長揭曉字幕 3 行高，1–2 行留空唔縮，frame 全程唔郁。空字幕 beat（walkup／glamour）display:none 維持不變——嗰兩段跳位係 v174 已接受 trade-off（glamour 同時收起卡列）。 */font-size:15px;line-height:1.55;text-align:center;white-space:pre-line}""",
    label="C2 caption")

# ---------- B1＋B7：高舞台幾何（HS211）＋梯形光柱 ----------
# HS211 定義：放喺 play 函數 try 內 beats 之前
rep("""  try{
    const beats = awards62CeremonyBeats(pack);""",
"""  try{
    /* v20a211 B1：高 viewport（innerHeight ≥850，即 932）先用高舞台 480×540（×1.25），矮 viewport（700）留返 480×432——
       700 提名版 frame 已經 644px（＋C2 字幕釘死 93px 後 668px），canvas 再高會頂爆 viewport 出捲軸；932 黑帶由 232px 收窄到 ~170px。
       FLOOR／人物／光池／glyph／閃粉全部按 HSC211＝HS211/432 比例換算（跟 v207 B2 ×1.2 同一做法），闊度唔郁、唔拉伸、觀眾暗帶唔加唔減、舞台-only 方向不變。 */
    const HS211 = (typeof window !== "undefined" && window.innerHeight >= 850) ? 540 : 432;
    const HSC211 = HS211 / 432;
    const beats = awards62CeremonyBeats(pack);""",
    label="B1 HS211")
# canvas backing 動態高
rep("""stage.innerHTML = '<div class="awd62-frame">'
      + '<div class="awd62-canvaswrap"><canvas class="awd62-canvas" width="720" height="648"></canvas>'""",
"""stage.innerHTML = '<div class="awd62-frame">'
      + '<div class="awd62-canvaswrap"><canvas class="awd62-canvas" width="720" height="' + Math.round(HS211 * 1.5) + '"></canvas>' /* v20a211 B1：backing 高跟 HS211（432→648／540→810，×1.5 transform 不變） */""",
    label="B1 backing")
# glamour overlay aspect 動態
rep("""      glamHtml = '<div class="awd63-glamour"><div class="awd63-glamour-panel"><img src="' + posterOf(pack.repGigId63) + '" alt="《' + repTitle + '》作品圖"/>'""",
"""      glamHtml = '<div class="awd63-glamour" style="aspect-ratio:480/' + HS211 + '"><div class="awd63-glamour-panel"><img src="' + posterOf(pack.repGigId63) + '" alt="《' + repTitle + '》作品圖"/>' /* v20a211 B1：glamour overlay 高跟 HS211（CSS 480/432 留做短 viewport 後備） */""",
    label="B1 glamour")
# FLOOR 按比例
rep("""    const FLOOR = 314; /* v20a181：橫向重建——木地板 y200–334（深 134px＝37.2% canvas 高）；v20a187 B1 更正：地板改 y228–310（深 82px＝22.8% 高），「佔畫面下半約四成」係讀錯參考圖（實測下半 29%，見 review §4 B1）；人物腳底跟同一常數，行前腳 272；舊 v177 FLOOR 250／圓台講台一併作廢；v20a207 B2：canvas 加高 360→432，地板按比例 y274–372（深 98px＝22.7%），FLOOR 262→314（地板深 41% 處，腳底以下空地板 58px）；行前腳 FLOOR＋10＝324 */""",
"""    const FLOOR = Math.round(314 * HSC211); /* v20a181：橫向重建——木地板 y200–334（深 134px＝37.2% canvas 高）；v20a187 B1 更正：地板改 y228–310（深 82px＝22.8% 高），「佔畫面下半約四成」係讀錯參考圖（實測下半 29%，見 review §4 B1）；人物腳底跟同一常數，行前腳 272；舊 v177 FLOOR 250／圓台講台一併作廢；v20a207 B2：canvas 加高 360→432，地板按比例 y274–372（深 98px＝22.7%），FLOOR 262→314（地板深 41% 處，腳底以下空地板 58px）；行前腳 FLOOR＋10＝324；v20a211 B1：高舞台 FLOOR＝314×1.25＝393（地板 y343–465，深 122px＝22.6%，比例不變） */""",
    label="B1 FLOOR")
# drawFigure 預設 dispH 按比例
rep("""      const dispH = o.dispH || (s.kind === "player" ? 140 : 136); /* v20a181：px 幀 dispH 112（人物約 89px＝框高四分一）、玩家 116；燕尾服同樣 112，齊高；v20a207 B2：136／140（人物約 108px），人物大返 */""",
"""      const dispH = o.dispH || (s.kind === "player" ? Math.round(140 * HSC211) : Math.round(136 * HSC211)); /* v20a181：px 幀 dispH 112（人物約 89px＝框高四分一）、玩家 116；燕尾服同樣 112，齊高；v20a207 B2：136／140（人物約 108px），人物大返；v20a211 B1：高舞台 170／175（人物約 135px） */""",
    label="B1 dispH default")
# lightPool 高按比例
rep("""      ctx.fillStyle = "rgba(255,217,104,0.16)"; ctx.fillRect(cx - w / 2, F - 120, w, 120); /* v20a174 B1：光池高 66→99（×1.5，蓋過 72px 人仔）；v20a207 B2：99→120（蓋過 108px 人仔） */""",
"""      ctx.fillStyle = "rgba(255,217,104,0.16)"; ctx.fillRect(cx - w / 2, F - Math.round(120 * HSC211), w, Math.round(120 * HSC211)); /* v20a174 B1：光池高 66→99（×1.5，蓋過 72px 人仔）；v20a207 B2：99→120（蓋過 108px 人仔）；v20a211 B1：高舞台 150（蓋過 135px 人仔） */""",
    label="B1 lightPool")
# B7：spotlight207 改做梯形光柱（連埋入面嘅光池 rect 一併按比例）
rep("""    const spotlight207 = (cx, w, fy)=>{ /* v20a207 C1：揭曉得主專屬 spotlight——舊版得主淨係 alpha 1＋淡光池（0.16），
      實測得主／落選者亮度只差 3%，肉眼分唔到。呢度加光柱（由紅帶底灑落腳底）＋加光光池＋地面光暈三層，
      得主企喺光入面，落選者再暗（見 reveal 分支 alpha），一眼分到邊個得獎。只喺 reveal 用，suspense 照舊 lightPool。 */
      const F = (fy != null) ? fy : FLOOR;
      ctx.fillStyle = "rgba(255,220,120,0.30)"; ctx.fillRect(cx - w / 2 - 14, 40, w + 28, F - 40);
      ctx.fillStyle = "rgba(255,217,104,0.22)"; ctx.fillRect(cx - w / 2, F - 120, w, 120);
      ctx.fillStyle = "rgba(255,217,104,0.45)"; ctx.fillRect(cx - w / 2 - 8, F - 6, w + 16, 6);
    };""",
"""    const spotlight207 = (cx, w, fy)=>{ /* v20a211 B7：揭曉光柱改做由上射落嚟嘅梯形光柱——取代 v207 直身光柱（上下同闊，望落似光管）。
      上窄（w×0.5）由框頂 y=0 起，下闊（w＋44）到腳底 F，暖白縱向漸變＋中央亮芯＋腳底光灘；喺 canvas 層畫、得主人物之前畫（人物唔會被光蓋住），
      DOM 文字層（橫額／數字條／白牌／字幕／卡列）喺 canvas 之上，唔會被遮。跟住得主 slot 企位（呼叫點傳 fp.x）。只喺 reveal 用；dimVeil207 落選者暗罩一字唔郁。 */
      const F = (fy != null) ? fy : FLOOR;
      const topW211 = Math.round(w * 0.5), botW211 = w + 44;
      const g211 = ctx.createLinearGradient(0, 0, 0, F);
      g211.addColorStop(0, "rgba(255,244,200,0.42)");
      g211.addColorStop(0.55, "rgba(255,228,140,0.30)");
      g211.addColorStop(1, "rgba(255,220,120,0.20)");
      ctx.fillStyle = g211;
      ctx.beginPath();
      ctx.moveTo(cx - topW211 / 2, 0); ctx.lineTo(cx + topW211 / 2, 0);
      ctx.lineTo(cx + botW211 / 2, F); ctx.lineTo(cx - botW211 / 2, F);
      ctx.closePath(); ctx.fill();
      /* 中央亮芯：同一梯形收窄版，令光柱有方向感（頂光源→下散開） */
      const g211b = ctx.createLinearGradient(0, 0, 0, F);
      g211b.addColorStop(0, "rgba(255,250,220,0.38)");
      g211b.addColorStop(1, "rgba(255,230,150,0.16)");
      ctx.fillStyle = g211b;
      ctx.beginPath();
      ctx.moveTo(cx - topW211 * 0.28, 0); ctx.lineTo(cx + topW211 * 0.28, 0);
      ctx.lineTo(cx + botW211 * 0.28, F); ctx.lineTo(cx - botW211 * 0.28, F);
      ctx.closePath(); ctx.fill();
      ctx.fillStyle = "rgba(255,217,104,0.22)"; ctx.fillRect(cx - w / 2, F - Math.round(120 * HSC211), w, Math.round(120 * HSC211));
      ctx.fillStyle = "rgba(255,217,104,0.45)"; ctx.fillRect(cx - w / 2 - 8, F - 6, w + 16, 6);
    };""",
    label="B7 spotlight")
# draw() W/H 跟 HS211
rep("""      const W = 480, H = 432; /* v20a207 B2：舞台加高 360→432（10:9）；backing 720×648，全部繪圖經 1.5× transform（imageSmoothingEnabled=false，像素邊保持硬淨）；闊度唔郁（直向 viewport 闊度係樽頸），加高先收窄到上下空帶 */""",
"""      const W = 480, H = HS211; /* v20a207 B2：舞台加高 360→432（10:9）；backing 720×648，全部繪圖經 1.5× transform（imageSmoothingEnabled=false，像素邊保持硬淨）；闊度唔郁（直向 viewport 闊度係樽頸），加高先收窄到上下空帶；v20a211 B1：高 viewport H＝540（backing 720×810），矮 viewport 留 432 */""",
    label="B1 draw WH")
# 明確 dispH: 136（燕尾服／reveal／glamour／walkup／out 共 5 處，全部喺 play 函數內）——用全檔計數核實
c136 = src.count("dispH: 136")
assert c136 == 5, f"B1 tux dispH count {c136}"
src = src.replace("dispH: 136", "dispH: Math.round(136 * HSC211)")
# glyph 頂位按比例
rep("""                drawTrophyGlyph(fp.x, FLOOR + fp.y - 129);""",
"""                drawTrophyGlyph(fp.x, FLOOR + fp.y - Math.round(129 * HSC211));""",
    label="B1 glyph tux")
rep("""                drawTrophyGlyph(fp.x, FLOOR + fp.y - 61);""",
"""                drawTrophyGlyph(fp.x, FLOOR + fp.y - Math.round(61 * HSC211));""",
    label="B1 glyph fellow")
c129 = src.count("FLOOR - 129")
assert c129 == 1, f"B1 FLOOR-129 count {c129}"
src = src.replace("FLOOR - 129", "FLOOR - Math.round(129 * HSC211)")
# 彩紙底界
rep("""        if(b.id === "reveal" || b.id === "comfort"){ /* v20a149 B1：comfort 期間彩紙繼續落；v20a174 B1：彩紙底界 244→364（H＋4）；v20a207 B2：364→436（H 432＋4） */""",
"""        if(b.id === "reveal" || b.id === "comfort"){ /* v20a149 B1：comfort 期間彩紙繼續落；v20a174 B1：彩紙底界 244→364（H＋4）；v20a207 B2：364→436（H 432＋4）；v20a211 B1：高舞台 HS211＋4 */""",
    label="B1 confetti comment")
rep("""          confetti.forEach(p=>{ p.y += p.v; p.x += p.sway; if(p.y > 436){ p.y = -8; p.x = Math.floor(Math.random() * 480); } });""",
"""          confetti.forEach(p=>{ p.y += p.v; p.x += p.sway; if(p.y > HS211 + 4){ p.y = -8; p.x = Math.floor(Math.random() * 480); } });""",
    label="B1 confetti bound")
# names／reveal 閃粉 y 帶按比例
rep("""          const fy = 225 + ((tick * 41 + i * 53) % 120); /* v20a174 B1：names 閃粉 y 帶 150–230 → 225–345（×1.5） */""",
"""          const fy = Math.round(225 * HSC211) + ((tick * 41 + i * 53) % Math.round(120 * HSC211)); /* v20a174 B1：names 閃粉 y 帶 150–230 → 225–345（×1.5）；v20a211 B1：高舞台 ×1.25（281–431） */""",
    label="B1 names sparkle")
rep("""            const fy = 307 + ((tick * 31 + i * 37) % 39); /* v20a174 B1：reveal 閃粉 y 帶 205–231 → 307–346（×1.5） */""",
"""            const fy = Math.round(307 * HSC211) + ((tick * 31 + i * 37) % Math.round(39 * HSC211)); /* v20a174 B1：reveal 閃粉 y 帶 205–231 → 307–346（×1.5）；v20a211 B1：高舞台 ×1.25（384–433） */""",
    label="B1 reveal sparkle")

open(p, "w", encoding="utf-8").write(src)
print("OK applied; bytes", len(orig), "->", len(src))
# 殘留檢查：play 函數內唔應該再有硬編碼 432 幾何（註解除外唔計）
import re
i = src.find("function awards62PlayCeremony(")
j = src.find("function awards63FellowsHtml(")
play = src[i:j]
for pat in ["const W = 480, H = 432", "const FLOOR = 314;", "height=\"648\"", "dispH: 136",
            "FLOOR + fp.y - 129", "FLOOR + fp.y - 61", "p.y > 436", "F - 120"]:
    print(("STILL PRESENT!! " if pat in play else "gone ok       ") + pat)
print("spotlight207 calls:", play.count("spotlight207(fp.x,"))
print("dimVeil207 untouched:", "rgba(10,6,20,0.45)" in play)
