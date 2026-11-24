/* v395 MINIGAME PROTOTYPE — 殺青「最後一 take」小遊戲（Cue 點走位＋對白節奏拍點）。
   範圍（prototype，唔係正式實裝）：
   - 淨係玩到個機制：殺青嗰陣彈出，allowlist 只得 3 張臨記級電影通告
     （見 MINIGAME395_ALLOWLIST）；另加 ?minigame=cue|rhythm 直接試玩入口。
   - 唔接獎勵／平衡系統：呢個檔唔可以 call 任何加聲望／信用／片酬／好感嘅函數，
     唔讀唔寫遊戲狀態、唔存檔、唔掂瀏覽器存檔。結果畫面只顯示判定，不寫入任何數值。
     （tests/test_v395_static.py 靜態守門：全檔掃描禁詞。）
   - 判定窗：完美 ±80ms／良好 ±80–250ms／普通 ±250–500ms／失手（>500ms 或無撳）。
     長音：按住 ≥80% 時長先算完成。
   - 方向二「紙本手帳 · 實物劇組」；直向手機、單手操作；Cue 圈心 ≥60px、
     跳過掣 60×44px；四級判定顏色＋形狀雙碼（完美金星／良好藍圈／普通灰半圓／失手紅叉）。
   - window.__mg395 係實駕用 debug handle（當前局 kind／時間軸／已判數），唔係遊戲邏輯。
   載入：index.html 檔尾 <script src="minigame395.js">；本檔自帶 CSS 注入＋load 自啟
   （?minigame 參數），唔靠主 script 呼叫。 */
(function(){
"use strict";

/* ===== PURE 395 BEGIN — 純函數（tests/test_v395_logic.js 抽出嚟 eval 驗證） ===== */
var MINIGAME395_ALLOWLIST = ["gig_1990_film_204", "gig_1990_film_205", "gig_1990_film_206"];
/* allowlist 揀法：1990 年臨記級電影通告，春／夏／秋各一，全部開局數值接得到
   （204 春 1 日 req {}；205 夏 2 日 req {}；206 秋 3 日 req stamina 55，開局體能 75）。
   唔揀主線強制通告；殺青先彈，唔改其他流程。 */
function minigame395Eligible(gigId){
  return MINIGAME395_ALLOWLIST.indexOf(String(gigId || "")) >= 0;
}
/* 四級判定：|dt|≤80 完美；≤250 良好；≤500 普通；>500 失手。 */
function minigame395Judge(deltaMs){
  var a = Math.abs(Number(deltaMs) || 0);
  if(a <= 80) return "perfect";
  if(a <= 250) return "good";
  if(a <= 500) return "ok";
  return "miss";
}
/* 長音完成閾值：按住時長 ≥80% 先算完成。 */
function minigame395HoldDone(heldMs, totalMs){
  var t = Number(totalMs) || 0;
  if(t <= 0) return false;
  return (Number(heldMs) || 0) >= 0.8 * t;
}
/* 直接試玩入口參數：?minigame=cue | ?minigame=rhythm，其餘 null。 */
function minigame395ParamFromSearch(search){
  try{
    var q = new URLSearchParams(String(search || ""));
    var v = q.get("minigame");
    if(v === "cue" || v === "rhythm") return v;
    return null;
  }catch(_e){ return null; }
}
var _mg395PickCount = 0;
/* 殺青觸發輪換：第一單 cue、第二單 rhythm、如此類推（兩機制喺殺青路都試得到；
   直接參數唔經呢度）。 */
function minigame395PickKind(gigId){
  _mg395PickCount++;
  return (_mg395PickCount % 2 === 1) ? "cue" : "rhythm";
}
/* ===== PURE 395 END ===== */

var MG395_GRADES = {
  perfect: { label: "完美", icon: "★", color: "#FFD700" },
  good:    { label: "良好", icon: "●", color: "#4A9EFF" },
  ok:      { label: "普通", icon: "◐", color: "#A0A0A0" },
  miss:    { label: "失手", icon: "✕", color: "#FF4444" }
};
/* 殺青去重 key：掛 window 做 live binding（index.html afterDayRes 讀寫
   window.mg395DoneKey395；同一單同一日只彈一次）。 */
try{ if(typeof window.mg395DoneKey395 === "undefined") window.mg395DoneKey395 = null; }catch(_e){}

/* ---------- CSS（方向二：米紙＋場記板黑底＋粉筆 X） ---------- */
var MG395_CSS = [
"#mg395-overlay{position:fixed;inset:0;z-index:99999;display:flex;justify-content:center;background:rgba(26,20,16,.72);font-family:\"Noto Serif CJK TC\",\"Songti TC\",\"PMingLiU\",serif;color:#1a1410;}",
"#mg395-overlay *{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}",
".mg395-sheet{width:min(390px,100%);height:100%;max-height:844px;margin:0 auto;background:#f2ebd8;display:flex;flex-direction:column;overflow:hidden;position:relative;}",
".mg395-head{padding:14px 16px 8px;border-bottom:2px solid #1a1410;background:#e6d2a8;}",
".mg395-head h2{margin:0;font-size:19px;letter-spacing:.06em;}",
".mg395-head .mg395-sub{margin:3px 0 0;font-size:12px;color:#6b5340;}",
".mg395-tag{display:inline-block;margin-left:8px;padding:1px 7px;border:2px solid #9e2f2f;color:#9e2f2f;border-radius:4px;font-size:11px;font-weight:900;letter-spacing:.12em;transform:rotate(-3deg);vertical-align:middle;}",
".mg395-stage{flex:1;position:relative;overflow:hidden;padding:10px 14px;}",
".mg395-hint{font-family:\"Kaiti TC\",\"STKaiti\",\"KaiTi\",\"Noto Serif CJK TC\",serif;font-size:13px;color:#6b5340;text-align:center;margin:0 0 8px;}",
".mg395-map{position:relative;height:148px;background:#efe6cf;border:1.5px solid #6b5340;border-radius:8px;overflow:hidden;touch-action:none;}",
".mg395-map .mg395-maplabel{position:absolute;left:8px;top:6px;font-size:11px;color:#8a7a5f;letter-spacing:.1em;}",
".mg395-x{position:absolute;width:40px;height:40px;margin:-20px 0 0 -20px;color:#c0452c;font-size:34px;line-height:40px;text-align:center;font-weight:900;opacity:.85;}",
".mg395-x.done{color:#b8860b;opacity:1;text-shadow:0 0 8px #ffd700;}",
".mg395-x.done::after{content:\"到位\";position:absolute;left:50%;top:38px;transform:translateX(-50%);font-size:11px;color:#8a6d00;}",
".mg395-awei{position:absolute;width:60px;height:60px;margin:-30px 0 0 -30px;border-radius:50%;background:#fbf6e6;border:2px solid #1a1410;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900;cursor:grab;touch-action:none;box-shadow:0 2px 6px rgba(0,0,0,.35);z-index:5;}",
".mg395-awei.dragging{cursor:grabbing;box-shadow:0 0 0 4px rgba(201,162,39,.55),0 2px 6px rgba(0,0,0,.35);}",
".mg395-tracks{display:flex;gap:8px;height:230px;margin-top:10px;background:#22201e;border-radius:8px;padding:10px 8px;position:relative;overflow:hidden;}",
".mg395-tracks::before{content:\"\";position:absolute;left:0;right:0;top:0;height:22px;background:repeating-linear-gradient(90deg,#f2ebd8 0 14px,#22201e 14px 28px);opacity:.9;}",
".mg395-track{flex:1;position:relative;background:rgba(255,255,255,.06);border-radius:6px;touch-action:none;cursor:pointer;}",
".mg395-ring{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;border:3px solid #fff;box-shadow:0 0 10px rgba(255,255,255,.8);display:none;}",
".mg395-ring .mg395-core{position:absolute;left:50%;top:50%;width:40px;height:40px;margin:-20px 0 0 -20px;border-radius:50%;border:2px solid rgba(255,255,255,.9);background:rgba(255,255,255,.15);}",
".mg395-ring.hit-perfect{border-color:#ffd700;box-shadow:0 0 14px #ffd700;}",
".mg395-ring.hit-good{border-color:#4a9eff;box-shadow:0 0 14px #4a9eff;}",
".mg395-ring.hit-ok{border-color:#a0a0a0;box-shadow:0 0 10px #a0a0a0;}",
".mg395-ring.hit-miss{border-color:#ff4444;box-shadow:0 0 10px #ff4444;}",
".mg395-legend{display:flex;gap:12px;justify-content:center;margin-top:10px;font-size:12px;color:#3a2e22;}",
".mg395-legend span b{font-size:15px;}",
".mg395-script{background:#fbf6e6;border:1.5px solid #6b5340;border-radius:8px;padding:10px 12px;min-height:96px;}",
".mg395-script .mg395-line{margin:2px 0;font-size:14px;line-height:1.6;color:#b8ab90;}",
".mg395-script .mg395-line.done{color:#8a7a5f;text-decoration:line-through;}",
".mg395-script .mg395-line.current{color:#1a1410;font-weight:700;}",
".mg395-script .mg395-line.current::before{content:\"▸ \";color:#c0452c;}",
".mg395-lane{position:relative;height:120px;margin-top:10px;background:#e9e2cf;border:1.5px solid #6b5340;border-radius:8px;overflow:hidden;touch-action:none;}",
".mg395-lane::before{content:\"\";position:absolute;left:0;right:0;top:24px;bottom:24px;background:repeating-linear-gradient(0deg,transparent 0 17px,#b8ab90 17px 18px);opacity:.5;}",
".mg395-hitline{position:absolute;left:28%;top:0;bottom:0;width:3px;background:#fff;box-shadow:0 0 8px rgba(255,255,255,.9);z-index:3;}",
".mg395-note{position:absolute;top:50%;transform:translate(-50%,-50%);font-size:26px;line-height:1;z-index:2;white-space:nowrap;}",
".mg395-note.long{font-size:26px;letter-spacing:.1em;}",
".mg395-note.judged{opacity:.25;}",
".mg395-holdbar{height:10px;background:#d8cfb6;border:1px solid #6b5340;border-radius:5px;margin-top:8px;overflow:hidden;position:relative;}",
".mg395-holdfill{height:100%;width:0%;background:linear-gradient(90deg,#6bcb77,#ffd700,#ff7a5c);}",
".mg395-holdmark{position:absolute;left:80%;top:0;bottom:0;width:2px;background:#c0452c;}",
".mg395-holdlabel{font-size:11px;color:#6b5340;text-align:center;margin-top:3px;}",
".mg395-tap{width:100%;min-height:64px;margin-top:10px;border:2px solid #1a1410;border-radius:10px;background:#c9a227;color:#1a1410;font-size:20px;font-weight:900;letter-spacing:.2em;touch-action:none;cursor:pointer;}",
".mg395-tap:active{background:#b8860b;}",
".mg395-pop{position:absolute;left:50%;top:38%;transform:translate(-50%,-50%);z-index:20;pointer-events:none;font-size:26px;font-weight:900;text-shadow:1px 1px 0 #000,-1px 1px 0 #000,1px -1px 0 #000,-1px -1px 0 #000;background:rgba(0,0,0,.45);border-radius:8px;padding:4px 12px;white-space:nowrap;}",
".mg395-foot{display:flex;align-items:center;gap:10px;padding:10px 14px 16px;border-top:2px solid #1a1410;background:#e6d2a8;}",
".mg395-skip{flex:0 0 auto;width:60px;min-height:44px;border:1.5px solid #6b5340;border-radius:8px;background:#d8cfb6;color:#3a2e22;font-size:14px;cursor:pointer;}",
".mg395-footnote{flex:1;font-size:11px;color:#6b5340;line-height:1.5;margin:0;}",
".mg395-result{position:absolute;inset:0;background:#f2ebd8;z-index:30;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;text-align:center;}",
".mg395-result h3{margin:0 0 4px;font-size:22px;}",
".mg395-result .mg395-rsub{margin:0 0 14px;font-size:12px;color:#6b5340;}",
".mg395-grades{display:flex;gap:10px;margin-bottom:12px;}",
".mg395-grade{width:74px;padding:10px 4px;background:#fbf6e6;border:1.5px solid #6b5340;border-radius:8px;}",
".mg395-grade .mg395-gicon{font-size:26px;line-height:1;}",
".mg395-grade .mg395-glabel{font-size:12px;margin-top:4px;}",
".mg395-grade .mg395-gcount{font-size:22px;font-weight:900;margin-top:2px;}",
".mg395-rextra{font-size:13px;color:#3a2e22;margin:0 0 4px;}",
".mg395-rnote{font-size:11px;color:#6b5340;margin:10px 0 16px;line-height:1.6;}",
".mg395-done{width:200px;min-height:48px;border:2px solid #1a1410;border-radius:10px;background:#c9a227;color:#1a1410;font-size:17px;font-weight:900;cursor:pointer;}",
".mg395-count{position:absolute;inset:0;z-index:25;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:900;color:#1a1410;text-shadow:0 0 12px #ffd700;pointer-events:none;}"
].join("\n");

var _mg395CssDone = false;
function mg395InjectCss(){
  if(_mg395CssDone) return;
  try{
    if(typeof document === "undefined") return;
    var st = document.createElement("style");
    st.setAttribute("data-mg395", "1");
    st.textContent = MG395_CSS;
    document.head.appendChild(st);
    _mg395CssDone = true;
  }catch(_e){}
}

var _mg395Open = false;
function mg395GradeChip(grade){
  var g = MG395_GRADES[grade] || MG395_GRADES.miss;
  return '<span style="color:' + g.color + '">' + g.icon + " " + g.label + "</span>";
}

/* 共用：結果畫面。counts={perfect,good,ok,miss}；extraHtml 係走位／長音行。 */
function mg395ShowResult(sheet, kind, counts, extraHtml, onDone){
  var old = sheet.querySelector(".mg395-result");
  if(old) old.remove();
  var total = (counts.perfect|0) + (counts.good|0) + (counts.ok|0) + (counts.miss|0);
  var best = counts.perfect === total && total > 0 ? "全數完美！導演都忍唔住拍掌。"
    : counts.miss === 0 ? "順利完成，呢 take 收得貨。"
    : "有甩漏都唔緊要，試玩版唔計分。";
  var res = document.createElement("div");
  res.className = "mg395-result";
  res.id = "mg395-result";
  var gradesHtml = ["perfect", "good", "ok", "miss"].map(function(k){
    var g = MG395_GRADES[k];
    return '<div class="mg395-grade"><div class="mg395-gicon" style="color:' + g.color + '">' + g.icon +
      '</div><div class="mg395-glabel">' + g.label +
      '</div><div class="mg395-gcount">' + (counts[k] | 0) + "</div></div>";
  }).join("");
  res.innerHTML = "<h3>最後一 take · 完成</h3>" +
    '<p class="mg395-rsub">' + best + "</p>" +
    '<div class="mg395-grades">' + gradesHtml + "</div>" +
    (extraHtml || "") +
    '<p class="mg395-rnote">試玩版：結果只作顯示，唔會寫入聲望、信用、片酬或好感。<br>失手唔扣分，跳過照原獎勵。</p>' +
    '<button type="button" class="mg395-done" id="mg395-done">完成</button>';
  sheet.appendChild(res);
  var btn = res.querySelector("#mg395-done");
  if(btn) btn.addEventListener("click", function(){ mg395Close(onDone); });
}

function mg395Close(onDone){
  try{
    var ov = document.getElementById("mg395-overlay");
    if(ov && ov.parentNode) ov.parentNode.removeChild(ov);
  }catch(_e){}
  _mg395Open = false;
  try{ if(window.__mg395) window.__mg395 = null; }catch(_e2){}
  if(typeof onDone === "function"){
    try{ onDone(); }catch(_e3){}
  }
}

/* 共用：開 overlay 骨架，回 sheet＋stage＋pop 函數。 */
function mg395OpenShell(kind, opts){
  mg395InjectCss();
  if(_mg395Open) return null;
  _mg395Open = true;
  var ov = document.createElement("div");
  ov.id = "mg395-overlay";
  var title = kind === "cue" ? "Cue 點走位" : "對白節奏拍點";
  ov.innerHTML =
    '<div class="mg395-sheet">' +
      '<div class="mg395-head"><h2>最後一 take · ' + title + '<span class="mg395-tag">試玩版</span></h2>' +
      '<p class="mg395-sub">' + (opts.gigTitle ? "《" + String(opts.gigTitle).replace(/[<>&"]/g, "") + "》殺青" : "殺青場戲") + " · 撳＋拖，唔會計分</p></div>" +
      '<div class="mg395-stage" id="mg395-stage"></div>' +
      '<div class="mg395-foot"><button type="button" class="mg395-skip" id="mg395-skip">跳過</button>' +
      '<p class="mg395-footnote">跳過即離開小遊戲，殺青獎勵照常結算；<br>結果唔會寫入任何數值。</p></div>' +
    "</div>";
  document.body.appendChild(ov);
  var sheet = ov.querySelector(".mg395-sheet");
  var stage = ov.querySelector("#mg395-stage");
  var skipBtn = ov.querySelector("#mg395-skip");
  var closed = false;
  var closeOnce = function(){
    if(closed) return;
    closed = true;
    mg395Close(opts.onDone || null);
  };
  if(skipBtn) skipBtn.addEventListener("click", closeOnce);
  var pop = function(text, color){
    try{
      var old = stage.querySelector(".mg395-pop");
      if(old) old.remove();
      var el = document.createElement("div");
      el.className = "mg395-pop";
      el.style.color = color || "#fff";
      el.textContent = text;
      stage.appendChild(el);
      setTimeout(function(){ if(el.parentNode) el.parentNode.removeChild(el); }, 650);
    }catch(_e){}
  };
  return { ov: ov, sheet: sheet, stage: stage, closeOnce: closeOnce, pop: pop,
    isClosed: function(){ return closed; } };
}

/* ---------- 機制 1：Cue 點走位 ---------- */
function mg395PlayCue(shell, opts){
  var stage = shell.stage;
  stage.innerHTML =
    '<p class="mg395-hint">拖阿偉去紅色 X 記號走位 · 圓圈縮到最細嗰陣撳</p>' +
    '<div class="mg395-map" id="mg395-map"><span class="mg395-maplabel">走位圖 · 俯視片場</span>' +
      '<div class="mg395-x" data-x="1" style="left:20%;top:34%;">✕</div>' +
      '<div class="mg395-x" data-x="2" style="left:76%;top:64%;">✕</div>' +
      '<div class="mg395-awei" id="mg395-awei">偉</div>' +
    "</div>" +
    '<div class="mg395-tracks" id="mg395-tracks"></div>' +
    '<div class="mg395-legend"><span><b style="color:#b8860b">★</b> 完美 ±80ms</span>' +
    '<span><b style="color:#4a9eff">●</b> 良好 ±250ms</span>' +
    '<span><b style="color:#a0a0a0">◐</b> 普通 ±500ms</span>' +
    '<span><b style="color:#ff4444">✕</b> 失手</span></div>';
  var map = stage.querySelector("#mg395-map");
  var token = stage.querySelector("#mg395-awei");
  var tracksEl = stage.querySelector("#mg395-tracks");
  var counts = { perfect: 0, good: 0, ok: 0, miss: 0 };
  var movesDone = 0;
  var movesTotal = 2;
  var t0 = performance.now() + 900; /* 900ms 準備時間 */
  /* 4 個 Cue 點：目標時刻（由開局計），每隔 1400ms 一個。 */
  var cues = [1500, 2900, 4300, 5700].map(function(t, i){
    return { t: t, judged: null, el: null, ring: null };
  });
  var trackEls = [];
  cues.forEach(function(cue, i){
    var tr = document.createElement("div");
    tr.className = "mg395-track";
    tr.setAttribute("role", "button");
    tr.setAttribute("aria-label", "Cue 點 " + (i + 1));
    var ring = document.createElement("div");
    ring.className = "mg395-ring";
    ring.innerHTML = '<div class="mg395-core"></div>';
    tr.appendChild(ring);
    tracksEl.appendChild(tr);
    trackEls.push(tr);
    cue.el = tr; cue.ring = ring;
    tr.addEventListener("pointerdown", function(ev){
      try{ ev.preventDefault(); }catch(_e){}
      mg395CueTap(i);
    });
  });
  /* 走位拖放：pointer 拖阿偉，近 X（36px 內）即吸附到位。 */
  var tokenPos = { x: 50, y: 80 }; /* %（起點：圖底中央） */
  var dragging = false;
  function placeToken(){
    token.style.left = tokenPos.x + "%";
    token.style.top = tokenPos.y + "%";
  }
  placeToken();
  function mapPoint(ev){
    var r = map.getBoundingClientRect();
    return { x: (ev.clientX - r.left) / r.width * 100, y: (ev.clientY - r.top) / r.height * 100, w: r.width, h: r.height };
  }
  function checkXs(){
    var xs = map.querySelectorAll(".mg395-x:not(.done)");
    var r = map.getBoundingClientRect();
    for(var i = 0; i < xs.length; i++){
      var xr = xs[i].getBoundingClientRect();
      var dx = (xr.left + xr.width / 2) - (r.left + tokenPos.x / 100 * r.width);
      var dy = (xr.top + xr.height / 2) - (r.top + tokenPos.y / 100 * r.height);
      if(Math.sqrt(dx * dx + dy * dy) < 36){
        xs[i].classList.add("done");
        movesDone++;
        tokenPos.x = (xr.left + xr.width / 2 - r.left) / r.width * 100;
        tokenPos.y = (xr.top + xr.height / 2 - r.top) / r.height * 100;
        placeToken();
        shell.pop("到位 ★", "#ffd700");
        break;
      }
    }
  }
  token.addEventListener("pointerdown", function(ev){
    try{ ev.preventDefault(); ev.stopPropagation(); }catch(_e){}
    dragging = true;
    token.classList.add("dragging");
    try{ token.setPointerCapture(ev.pointerId); }catch(_e2){}
  });
  token.addEventListener("pointermove", function(ev){
    if(!dragging) return;
    var p = mapPoint(ev);
    tokenPos.x = Math.max(6, Math.min(94, p.x));
    tokenPos.y = Math.max(12, Math.min(88, p.y));
    placeToken();
    checkXs();
  });
  var endDrag = function(){
    if(!dragging) return;
    dragging = false;
    token.classList.remove("dragging");
    checkXs();
  };
  token.addEventListener("pointerup", endDrag);
  token.addEventListener("pointercancel", endDrag);

  function judgeCue(i, grade){
    var cue = cues[i];
    if(!cue || cue.judged) return;
    cue.judged = grade;
    counts[grade]++;
    cue.ring.classList.add("hit-" + grade);
    var g = MG395_GRADES[grade];
    shell.pop(g.icon + " " + g.label, g.color);
    if(window.__mg395) window.__mg395.judged = counts;
  }
  function mg395CueTap(i){
    if(shell.isClosed()) return;
    var now = performance.now() - t0;
    var cue = cues[i];
    if(!cue || cue.judged) return;
    var dt = now - cue.t;
    if(Math.abs(dt) > 500) return; /* 離拍子太遠：唔計，唔扣分 */
    judgeCue(i, minigame395Judge(dt));
  }
  var raf = 0, ended = false;
  function finish(){
    if(ended) return;
    ended = true;
    try{ cancelAnimationFrame(raf); }catch(_e){}
    setTimeout(function(){
      if(shell.isClosed()) return;
      mg395ShowResult(shell.sheet, "cue", counts,
        '<p class="mg395-rextra">走位：' + movesDone + " / " + movesTotal + " 個 X 記號到位</p>",
        opts.onDone || null);
    }, 700);
  }
  function tick(){
    if(shell.isClosed() || ended) return;
    var now = performance.now() - t0;
    var allJudged = true;
    cues.forEach(function(cue){
      if(cue.judged){
        cue.ring.style.display = "block";
        return;
      }
      allJudged = false;
      if(now < cue.t - 1000){ cue.ring.style.display = "none"; return; }
      if(now > cue.t + 500){
        judgeCue(cues.indexOf(cue), "miss");
        cue.ring.style.display = "block";
        return;
      }
      /* 縮圈：1000ms 前 100px → 目標時刻 40px。 */
      var p = Math.max(0, Math.min(1, (now - (cue.t - 1000)) / 1000));
      var size = Math.round(100 - 60 * p);
      cue.ring.style.display = "block";
      cue.ring.style.width = size + "px";
      cue.ring.style.height = size + "px";
    });
    if(allJudged) finish();
    else raf = requestAnimationFrame(tick);
  }
  try{
    window.__mg395 = { kind: "cue", t0: t0, cues: cues.map(function(c){ return c.t; }), judged: counts };
  }catch(_e){}
  var cd = document.createElement("div");
  cd.className = "mg395-count";
  cd.textContent = "準備…";
  stage.appendChild(cd);
  setTimeout(function(){ if(cd.parentNode) cd.parentNode.removeChild(cd); }, 850);
  raf = requestAnimationFrame(tick);
}

/* ---------- 機制 2：對白節奏拍點 ---------- */
function mg395PlayRhythm(shell, opts){
  var stage = shell.stage;
  /* 殺青場戲台詞（對白＝廣東話；其餘 UI 字＝書面語）。 */
  var lines = [
    { text: "埋位！最後一 take，唔好眨眼。", len: "short", hit: 1600 },
    { text: "呢句對白，我練咗成晚。", len: "short", hit: 3100 },
    { text: "導演話，呢個眼神要再狠啲。", len: "mid", hit: 4600 },
    { text: "收工之後，我請全組食糖水。", len: "mid", hit: 6100 },
    { text: "由臨記行到今日，呢一 take，就係我哋成組人嘅心血。", len: "long", hit: 7700, dur: 1600 }
  ];
  var NOTE_ICON = { short: "♪", mid: "♬", long: "♫" };
  stage.innerHTML =
    '<div class="mg395-script" id="mg395-script"></div>' +
    '<div class="mg395-lane" id="mg395-lane"><div class="mg395-hitline"></div></div>' +
    '<div class="mg395-holdbar"><div class="mg395-holdfill" id="mg395-holdfill"></div><div class="mg395-holdmark"></div></div>' +
    '<p class="mg395-holdlabel">長音：按住唔放，到 80% 紅線先放手（長句 ♫）</p>' +
    '<button type="button" class="mg395-tap" id="mg395-tap">撳</button>';
  var scriptEl = stage.querySelector("#mg395-script");
  var lane = stage.querySelector("#mg395-lane");
  var tapBtn = stage.querySelector("#mg395-tap");
  var holdFill = stage.querySelector("#mg395-holdfill");
  scriptEl.innerHTML = lines.map(function(l, i){
    return '<p class="mg395-line" data-i="' + i + '">' + l.text + "</p>";
  }).join("");
  var counts = { perfect: 0, good: 0, ok: 0, miss: 0 };
  var longDone = null; /* true=完成 / false=未完成 / null=未判 */
  var t0 = performance.now() + 900;
  var notes = lines.map(function(l, i){
    var el = document.createElement("div");
    el.className = "mg395-note" + (l.len === "long" ? " long" : "");
    el.textContent = NOTE_ICON[l.len];
    el.style.color = l.len === "short" ? "#3d9e57" : l.len === "mid" ? "#4a9eff" : "#8a6ab0";
    el.style.display = "none";
    lane.appendChild(el);
    return { line: l, i: i, el: el, judged: null };
  });
  var LEAD = 1800; /* 音符提前 1800ms 由右滑入拍點線（28% 處）。 */
  var holding = false, holdStart = 0, holdPressDt = 0, heldMs = 0, holdJudged = false;
  var raf = 0, ended = false;

  function markLine(i, cls){
    var ps = scriptEl.querySelectorAll(".mg395-line");
    ps.forEach(function(p, j){
      p.classList.remove("current");
      if(j < i) p.classList.add("done");
    });
    if(ps[i]) ps[i].classList.add("current");
  }
  function judgeNote(i, grade){
    var n = notes[i];
    if(!n || n.judged) return;
    n.judged = grade;
    counts[grade]++;
    n.el.classList.add("judged");
    var g = MG395_GRADES[grade];
    shell.pop(g.icon + " " + g.label, g.color);
    if(window.__mg395) window.__mg395.judged = counts;
  }
  function tapNow(){
    if(shell.isClosed() || ended) return;
    var now = performance.now() - t0;
    /* 長音按住優先：長音頭到線 ±500ms 內按下＝開始按住。 */
    var ln = notes[notes.length - 1];
    if(ln && !ln.judged && !holdJudged && Math.abs(now - ln.line.hit) <= 500 && !holding){
      holding = true; holdStart = now; holdPressDt = now - ln.line.hit; heldMs = 0;
      return;
    }
    /* 其餘音符：取最近未判嗰粒，±500ms 內先判。 */
    var best = null, bestDt = 1e9;
    notes.forEach(function(n){
      if(n.judged || n.line.len === "long") return;
      var dt = now - n.line.hit;
      if(Math.abs(dt) < Math.abs(bestDt)){ best = n; bestDt = dt; }
    });
    if(best && Math.abs(bestDt) <= 500) judgeNote(best.i, minigame395Judge(bestDt));
  }
  function releaseHold(){
    if(!holding) return;
    holding = false;
    var ln = notes[notes.length - 1];
    if(!ln || ln.judged || holdJudged) return;
    holdJudged = true;
    if(minigame395HoldDone(heldMs, ln.line.dur)){
      longDone = true;
      judgeNote(ln.i, minigame395Judge(holdPressDt));
    }else{
      longDone = false;
      judgeNote(ln.i, "miss");
      shell.pop("再長點", "#ff4444");
    }
    holdFill.style.width = "0%";
  }
  tapBtn.addEventListener("pointerdown", function(ev){
    try{ ev.preventDefault(); }catch(_e){}
    tapNow();
  });
  tapBtn.addEventListener("pointerup", releaseHold);
  tapBtn.addEventListener("pointercancel", releaseHold);
  tapBtn.addEventListener("pointerleave", releaseHold);
  lane.addEventListener("pointerdown", function(ev){
    try{ ev.preventDefault(); }catch(_e){}
    tapNow();
  });
  lane.addEventListener("pointerup", releaseHold);
  lane.addEventListener("pointercancel", releaseHold);

  function finish(){
    if(ended) return;
    ended = true;
    try{ cancelAnimationFrame(raf); }catch(_e){}
    setTimeout(function(){
      if(shell.isClosed()) return;
      mg395ShowResult(shell.sheet, "rhythm", counts,
        '<p class="mg395-rextra">長音：' + (longDone === true ? "完成（按住 ≥80%）" : longDone === false ? "未完成（放手太早）" : "未試") + "</p>",
        opts.onDone || null);
    }, 700);
  }
  function tick(){
    if(shell.isClosed() || ended) return;
    var now = performance.now() - t0;
    var allJudged = true, current = 0;
    notes.forEach(function(n){
      if(n.judged){
        n.el.style.display = "none";
        return;
      }
      allJudged = false;
      if(now >= n.line.hit) current = n.i;
      if(now < n.line.hit - LEAD){ n.el.style.display = "none"; return; }
      if(now > n.line.hit + 500 && n.line.len !== "long"){
        judgeNote(n.i, "miss");
        n.el.style.display = "none";
        return;
      }
      if(n.line.len === "long" && now > n.line.hit + n.line.dur + 500 && !holdJudged){
        /* 長音過晒都冇撳：失手。 */
        holdJudged = true; longDone = false;
        judgeNote(n.i, "miss");
        n.el.style.display = "none";
        return;
      }
      /* 由右（100%）滑向拍點線（28%），1800ms 走完全程；長音過線後留喺線附近。 */
      var p = Math.max(0, Math.min(1, (now - (n.line.hit - LEAD)) / LEAD));
      var x = 100 - (100 - 28) * p;
      if(n.line.len === "long" && now > n.line.hit){
        var tail = Math.min(1, (now - n.line.hit) / n.line.dur);
        x = 28 - 18 * tail;
      }
      n.el.style.display = "block";
      n.el.style.left = x + "%";
    });
    /* 按住中：累計時長＋填充條。 */
    if(holding){
      var ln = notes[notes.length - 1];
      heldMs = now - holdStart;
      holdFill.style.width = Math.min(100, heldMs / ln.line.dur * 100) + "%";
      if(minigame395HoldDone(heldMs, ln.line.dur) && !holdJudged){
        /* 夠 80% 即判完成，唔使等放手（放手後只清條）。 */
        holdJudged = true; longDone = true;
        judgeNote(ln.i, minigame395Judge(holdPressDt));
        /* 唔再另彈「完美長音」：judgeNote 已按按下時機彈返正確級別。 */
      }
    }
    markLine(current);
    if(allJudged) finish();
    else raf = requestAnimationFrame(tick);
  }
  try{
    window.__mg395 = { kind: "rhythm", t0: t0, notes: lines.map(function(l){ return l.hit; }), judged: counts };
  }catch(_e){}
  markLine(0);
  var cd = document.createElement("div");
  cd.className = "mg395-count";
  cd.textContent = "準備…";
  stage.appendChild(cd);
  setTimeout(function(){ if(cd.parentNode) cd.parentNode.removeChild(cd); }, 850);
  raf = requestAnimationFrame(tick);
}

/* ---------- 入口 ---------- */
function openMinigame395(kind, opts){
  opts = opts || {};
  if(kind !== "cue" && kind !== "rhythm") kind = "cue";
  if(typeof document === "undefined") return false;
  var shell = mg395OpenShell(kind, opts);
  if(!shell) return false;
  try{
    if(kind === "cue") mg395PlayCue(shell, opts);
    else mg395PlayRhythm(shell, opts);
  }catch(_e){
    mg395Close(opts.onDone || null);
    return false;
  }
  return true;
}

/* 直接試玩入口：?minigame=cue | ?minigame=rhythm（load 後開，唔使打通成局）。 */
function minigame395BootDirect(){
  try{
    if(typeof document === "undefined" || typeof location === "undefined") return;
    var kind = minigame395ParamFromSearch(location.search || "");
    if(!kind) return;
    var go = function(){ openMinigame395(kind, { direct: true, gigTitle: "", onDone: null }); };
    if(document.readyState === "complete") setTimeout(go, 50);
    else window.addEventListener("load", function(){ setTimeout(go, 50); });
  }catch(_e){}
}

/* 掛 global：主 script（IIFE 內）嘅殺青鉤子經呢啲名呼叫。 */
try{
  window.MINIGAME395_ALLOWLIST = MINIGAME395_ALLOWLIST;
  window.minigame395Eligible = minigame395Eligible;
  window.minigame395Judge = minigame395Judge;
  window.minigame395HoldDone = minigame395HoldDone;
  window.minigame395ParamFromSearch = minigame395ParamFromSearch;
  window.minigame395PickKind = minigame395PickKind;
  window.openMinigame395 = openMinigame395;
  window.minigame395BootDirect = minigame395BootDirect;
}catch(_e){}

minigame395BootDirect();

})();
