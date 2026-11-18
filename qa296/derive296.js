// qa296/derive296.js — v20a296 Q9 推導：現行 index.html + content packs 全部對白，
// 用 runtime 真分類器（dlg106ResolveCategory）分類，逐角逐表情計 live 句數，
// 對返 assets/story/fullbody/ 資產，輸出 A/B/C 三組。
// 用法：node qa296/derive296.js
// 輸出：qa296/derive296.json ＋ 印表。
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..");
const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf-8");

function sliceBetween(startMarker, endMarker) {
  const a = html.indexOf(startMarker);
  if (a < 0) throw new Error("marker not found: " + startMarker);
  const b = endMarker ? html.indexOf(endMarker, a) : html.length;
  if (b < 0) throw new Error("end marker not found: " + endMarker);
  return html.slice(a, b);
}
function sliceLineContaining(marker) {
  const a = html.indexOf(marker);
  if (a < 0) throw new Error("marker not found: " + marker);
  const b = html.indexOf("\n", a);
  return html.slice(a, b < 0 ? html.length : b);
}
const parts = [];
parts.push(sliceLineContaining("const DLG106_CATEGORIES"));
parts.push(sliceLineContaining("const DLG106_CAT_TO_EXPR"));
parts.push(sliceLineContaining("const DLG106_OLD_EMOTION_TO_CAT"));
parts.push(sliceLineContaining("const DLG106_EXPR_TO_CAT"));
parts.push(sliceLineContaining("const DLG106_EMOTION_MAP"));
parts.push(sliceBetween("var DLG106_PUNCT", "/* 阿偉成長階段"));
const code = parts.join("\n");

const NAME2ID = { '阿偉':'awi','何生':'ho_sang','Vera':'vera','林曉晴':'lin_hiu','張子駿':'cheung_tsijun','高俊傑':'ko_chunkit','周采兒':'chow_choiyi','高文瀚':'gao_wenhan','藍若曦':'lan_ruoxi','張克凡':'cheung_hakfan','雷勁':'lui_ging','鄭威廉':'cheng_william','唐素雲':'tong_souwan','方小龍':'fong_siulung','徐寶珊':'tsui_poushan','莫少輝':'mok_siufai','金九':'uncle_kim','鄧麗萍':'tang_laiping','陸柏言':'luk_baakyin','廖炳星':'liu_bingxing','魏詠男':'ngai_wingnaam','葉敏芝':'yip_manji','麥震東':'mak_zhendong','駱家聲':'lok_gasing','彭少祺':'pang_siuki','鍾楚凝':'chung_choning','顧明輝':'gu_mingfai','蘇芷茵':'so_jiyan','齊鎮海':'chai_zanhoi','程天諾':'ching_tinlok','副導演芬姐':'extra_ad_fen','老臨記':'crew_laolinji','阿媽':'shadow_female','場務姐姐':'shadow_female','場務':'shadow_male','副導演':'shadow_male' };

// occ: key = speaker + "\0" + text -> {speaker, text, emotion, sources:Set}
const occ = new Map();
function add(speaker, text, emotion, src) {
  if (!speaker || speaker === "vera" || typeof text !== "string" || !text.trim()) return;
  text = text.replace(/\\"/g, '"');
  const k = speaker + "\0" + text;
  let o = occ.get(k);
  if (!o) { o = { speaker, text, emotion: emotion || null, sources: new Set() }; occ.set(k, o); }
  o.sources.add(src);
  if (emotion && !o.emotion) o.emotion = emotion;
}

// --- 1. ENC blocks ---
for (const m of html.matchAll(/const ENC(?:79|83|84)_DLG_(\w+) =/g)) {
  const sid = m[1] === 'yip_manzi' ? 'yip_manji' : m[1];
  const seg = html.slice(m.index, m.index + 160000);
  const end = seg.search(/\nconst ENC|\n\/\* =====/);
  const body = end > 0 ? seg.slice(0, end) : seg;
  for (const t of body.matchAll(/\[\s*"(S|A|N)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\]/g)) {
    if (t[1] === 'N') continue;
    add(t[1] === 'A' ? 'awi' : sid, t[2], null, "ENC");
  }
}
// --- 2. index.html lines:[...] beats ---
for (const m of html.matchAll(/lines:\s*\[((?:"(?:[^"\\]|\\.)*"\s*,?\s*)+)\]/g)) {
  const back = html.slice(Math.max(0, m.index - 420), m.index);
  const idAll = [...back.matchAll(/speakerId:\s*"([^"]+)"/g)];
  const spAll = [...back.matchAll(/speaker:\s*"([^"]+)"/g)];
  const idm = idAll.length ? idAll[idAll.length - 1] : null;
  const spm = spAll.length ? spAll[spAll.length - 1] : null;
  let sid = null;
  if (idm) sid = idm[1] === 'agent' ? 'ho_sang' : (idm[1] === 'player' ? 'awi' : idm[1]);
  else if (spm) sid = NAME2ID[spm[1]] || null;
  if (!sid) continue;
  const emoM = back.match(/emotion:\s*"([^"]+)"/);
  for (const t of m[1].matchAll(/"((?:[^"\\]|\\.)*)"/g)) add(sid, t[1], emoM ? emoM[1] : null, "LIVE");
}
// --- 2b. index.html text:"..." beats (WF4／結果 beats 用單句 text，唔係 lines 陣列) ---
for (const m of html.matchAll(/text:\s*"((?:[^"\\]|\\.)*)"/g)) {
  const back = html.slice(Math.max(0, m.index - 260), m.index);
  const idAll = [...back.matchAll(/speakerId:\s*"([^"]+)"/g)];
  const spAll = [...back.matchAll(/speaker:\s*"([^"]+)"/g)];
  const idm = idAll.length ? idAll[idAll.length - 1] : null;
  const spm = spAll.length ? spAll[spAll.length - 1] : null;
  let sid = null;
  if (idm) sid = idm[1] === 'agent' ? 'ho_sang' : (idm[1] === 'player' ? 'awi' : idm[1]);
  else if (spm) sid = NAME2ID[spm[1]] || null;
  if (!sid) continue;
  // 排除非對白 text（例如 synopsis／notes 入面嘅 text 欄唔會有 speakerId 緊貼，260 字窗口＋speaker 要求已過濾大半）
  const emoM = back.match(/emotion:\s*"([^"]+)"/);
  add(sid, m[1], emoM ? emoM[1] : null, "LIVE");
}
// --- 3. content packs: story_detail_*.json (recursive beats walk) ---
// Pack 節點本身就係 live 內容（STORY_WIRE 載入後 StoryPlay 播放），除咗：
// (a) R_hiu_meet／R_choi_meet — mock DualMeet 覆寫，pack 版播唔到；(b) R_tang_* — 感情線已取消；
// (c) vera 講者 — Q10／v297 成個移除，唔入 v296 範圍。
const MOCK_OVERRIDDEN = new Set(["R_hiu_meet", "R_choi_meet"]);
function walkPack(node, src, nodeId, isMock) {
  if (Array.isArray(node)) { node.forEach(n => walkPack(n, src, nodeId, isMock)); return; }
  if (!node || typeof node !== "object") return;
  const id = (typeof node.id === "string") ? node.id : nodeId;
  if (Array.isArray(node.lines)) {
    let sid = null;
    if (node.speakerId) sid = node.speakerId === 'agent' ? 'ho_sang' : (node.speakerId === 'player' ? 'awi' : node.speakerId);
    else if (node.speaker) sid = NAME2ID[node.speaker] || null;
    else if (node.characterId) sid = node.characterId;
    const emo = node.emotion || node.expression || null;
    const dead = !isMock && id && (MOCK_OVERRIDDEN.has(id) || id.indexOf("R_tang") === 0);
    if (sid && sid !== "vera" && !dead) for (const t of node.lines) if (typeof t === "string") add(sid, t, emo, src);
  }
  for (const k of Object.keys(node)) {
    if (k === "lines") continue;
    walkPack(node[k], src, id, isMock);
  }
}
for (const f of fs.readdirSync(path.join(ROOT, "content")).filter(f => /^story_detail_.*\.json$/.test(f) || f === "story_beats_phase1.json")) {
  try {
    const d = JSON.parse(fs.readFileSync(path.join(ROOT, "content", f), "utf-8"));
    walkPack(d, "PACK:" + f);
  } catch (e) { console.error("pack parse fail " + f + ": " + e.message); }
}
// --- 4. mock DualMeet (live 版 R_hiu_meet) ---
try {
  const d = JSON.parse(fs.readFileSync(path.join(ROOT, "content", "MOCK_STORY_DUAL_MEET_THICKEN_SOFT_v1.json"), "utf-8"));
  walkPack(d, "MOCK:DUAL_MEET", null, true);
} catch (e) { console.error("mock parse fail: " + e.message); }
// --- 5. NPC core lines ---
const NPCMAP = { agent: 'ho_sang', stylist: 'vera', colleague: 'lin_hiu', director: 'cheung_tsijun', rival: 'ko_chunkit', reporter: 'chow_choiyi' };
try {
  const d = JSON.parse(fs.readFileSync(path.join(ROOT, "content", "npc_lines_core.json"), "utf-8"));
  for (const [k, sid] of Object.entries(NPCMAP)) {
    const ent = d[k]; if (!ent) continue;
    for (const cat of ["greet", "chat", "advice", "intel", "pressure"]) {
      const arr = ent[cat];
      if (Array.isArray(arr)) for (const t of arr) if (typeof t === "string") add(sid, t, null, "CORE");
    }
  }
} catch (e) { console.error("npc core parse fail: " + e.message); }
// --- 6. gift reactions (GIFT source; 註：送禮反應未必行對白舞台，另欄計) ---
try {
  const d = JSON.parse(fs.readFileSync(path.join(ROOT, "content", "gift_react_copy.json"), "utf-8"));
  const walk = (n) => {
    if (Array.isArray(n)) { n.forEach(walk); return; }
    if (!n || typeof n !== "object") return;
    if (typeof n.text === "string" && n.npc) add(n.npc, n.text, null, "GIFT");
    if (typeof n.line === "string" && n.npc) add(n.npc, n.line, null, "GIFT");
    for (const k of Object.keys(n)) walk(n[k]);
  };
  walk(d);
} catch (e) { console.error("gift parse fail: " + e.message); }

// --- classify with the real runtime classifier ---
const rows = [...occ.values()].map(o => ({ speaker: o.speaker, text: o.text, emotion: o.emotion, sources: [...o.sources] }));
const driver = `
;__out = input.map((row) => {
  const cat = dlg106ResolveCategory({ emotion: row.emotion || null, text: row.text });
  return { speaker: row.speaker, text: row.text, emotion: row.emotion, sources: row.sources, category: cat, expr: DLG106_CAT_TO_EXPR[cat] || "base" };
});
`;
const input = rows;
let __out;
eval(code + driver);

// aggregate: per (speaker, expr): distinct live texts (LIVE/ENC/CORE/MOCK/PACK-live), gift texts
const LIVE_SRCS = new Set(["LIVE", "ENC", "CORE", "MOCK:DUAL_MEET"]);
const agg = {}; // speaker -> expr -> {live:[], pack:[], gift:[]}
for (const r of __out) {
  const sp = agg[r.speaker] || (agg[r.speaker] = {});
  const e = sp[r.expr] || (sp[r.expr] = { live: [], pack: [], gift: [] });
  const isLive = r.sources.some(s => LIVE_SRCS.has(s) || s.startsWith("PACK:"));
  const isGift = r.sources.includes("GIFT");
  if (isLive) e.live.push({ text: r.text, sources: r.sources, category: r.category });
  else if (isGift) e.gift.push({ text: r.text, sources: r.sources, category: r.category });
}
// assets
const FB = path.join(ROOT, "assets", "story", "fullbody");
const files = new Set(fs.readdirSync(FB));
const have = {}; // stem -> Set(expr)
for (const fn of files) {
  const m = fn.match(/^(.+)_(base|smile|serious|sad|surprise|shy|think|angry)\.(webp|png)$/);
  if (m) { (have[m[1]] || (have[m[1]] = new Set())).add(m[2]); }
}
const result = { speakers: agg, have: Object.fromEntries(Object.entries(have).map(([k, v]) => [k, [...v]])), totalFiles: files.size };
fs.writeFileSync(path.join(__dirname, "derive296.json"), JSON.stringify(result, null, 1), "utf-8");

// print table
const EXPRS = ["smile", "serious", "sad", "surprise", "shy", "think", "angry"];
console.log("總抽取 (speaker,text)：" + rows.length);
console.log("fullbody 檔案總數：" + files.size);
console.log("");
console.log("speaker | expr: live句數/pack句數/資產(有=✓缺=✗) — 只列非 base");
for (const sp of Object.keys(agg).sort()) {
  const stems = sp === "awi" ? ["awi", "awi_s2", "awi_s3", "awi_c1", "awi_c4", "awi_c8", "awi_c10"] : [sp];
  const cells = [];
  for (const ex of EXPRS) {
    const e = (agg[sp] || {})[ex];
    const nLive = e ? e.live.length : 0;
    const nPack = e ? e.pack.length : 0;
    const hasAny = stems.some(s => (have[s] || new Set()).has(ex));
    const hasAll = stems.every(s => (have[s] || new Set()).has(ex));
    const mark = hasAll ? "✓" : (hasAny ? "~" : "✗");
    if (nLive > 0 || nPack > 0 || !hasAll) cells.push(ex + ":" + nLive + "/" + nPack + "/" + mark);
  }
  console.log(sp + " | " + cells.join("  "));
}
console.log("");
console.log("=== A組：有 live 句但缺資產（要出圖）===");
const SHADOWS = new Set(["shadow_male", "shadow_female", "shadow_elder", "generic_cinema_asst"]);
for (const sp of Object.keys(agg).sort()) {
  if (SHADOWS.has(sp)) continue;
  const stems = sp === "awi" ? ["awi", "awi_s2", "awi_s3", "awi_c1", "awi_c4", "awi_c8", "awi_c10"] : [sp];
  for (const ex of EXPRS) {
    const e = (agg[sp] || {})[ex];
    if (e && e.live.length > 0) {
      const missing = stems.filter(s => !(have[s] || new Set()).has(ex));
      if (missing.length) console.log(sp + ":" + ex + " live " + e.live.length + " 句，缺：" + missing.map(s => s + "_" + ex + ".webp").join(", "));
    }
  }
}
console.log("");
console.log("=== B組：零 live 句＋缺資產（死組；要補對白＋出圖，或確認死）===");
for (const sp of Object.keys(agg).sort()) {
  if (SHADOWS.has(sp)) continue;
  const stems = sp === "awi" ? ["awi", "awi_s2", "awi_s3", "awi_c1", "awi_c4", "awi_c8", "awi_c10"] : [sp];
  for (const ex of EXPRS) {
    const e = (agg[sp] || {})[ex];
    const nLive = e ? e.live.length : 0;
    const nPack = e ? e.pack.length : 0;
    const missing = stems.filter(s => !(have[s] || new Set()).has(ex));
    if (nLive === 0 && missing.length) console.log(sp + ":" + ex + " live 0 / pack " + nPack + "，缺：" + missing.map(s => s + "_" + ex + ".webp").join(", "));
  }
}
console.log("");
console.log("=== C組：零 live 句但資產存在（孤兒；要補對白）===");
for (const sp of Object.keys(agg).sort()) {
  if (SHADOWS.has(sp)) continue;
  const stems = sp === "awi" ? ["awi", "awi_s2", "awi_s3", "awi_c1", "awi_c4", "awi_c8", "awi_c10"] : [sp];
  for (const ex of EXPRS) {
    const e = (agg[sp] || {})[ex];
    const nLive = e ? e.live.length : 0;
    const nPack = e ? e.pack.length : 0;
    const hasAny = stems.some(s => (have[s] || new Set()).has(ex));
    if (nLive === 0 && hasAny) console.log(sp + ":" + ex + " live 0 / pack " + nPack + "，資產存在：" + stems.filter(s => (have[s] || new Set()).has(ex)).join(", "));
  }
}
console.log("");
console.log("=== base 缺失檢查 ===");
for (const sp of Object.keys(agg).sort()) {
  const stems = sp === "awi" ? ["awi", "awi_s2", "awi_s3", "awi_c1", "awi_c4", "awi_c8", "awi_c10"] : [sp];
  for (const s of stems) if (!(have[s] || new Set()).has("base")) console.log("缺 base：" + s);
}
