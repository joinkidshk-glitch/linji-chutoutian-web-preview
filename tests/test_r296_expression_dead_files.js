// v20a296 Q9 表情死檔補齊：邏輯測試。
//   (1) 26 張新表情圖入庫＋每張 ≥1 句 live 實線（句數＝qa296/derive296.json，
//       用 runtime 真分類器 dlg106ResolveCategory 逐句分類，唔係 corpus 句數）；
//   (2) 兩句新對白行返啱嘅表情分類：徐寶珊 serious（R_xu_crisis）、
//       張子駿 angry（A_tsijun_crisis）；林曉晴 serious 唔使加對白
//       （npc_lines_core 已有 1 句 live）；
//   (3) 守門：有 live 句但缺資產嘅組，只准剩返 4 位新星嗰 16 張
//       （hon_sauting／kong_siying／shum_yingsuet／wu_meilam，連 base 都冇，
//       v290 已定剪影頂住，等新星美術票）；其他角一張都唔准缺；
//   (4) fullbody 總數 237→261（v297 刪 kwan_hoimei 2 張）。
// 推導本身由 qa296/derive296.js 做（單一來源）；呢個測試即場重跑推導再斷言，
// 唔讀舊快照。
// 用法：node tests/test_r296_expression_dead_files.js [path-to-index.html]
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const HERE = path.join(__dirname, "..");
const ROOT = process.argv[2] ? path.dirname(path.resolve(process.argv[2])) : HERE;
const FB = path.join(ROOT, "assets", "story", "fullbody");

let fails = [];
function ok(name, cond) {
  console.log((cond ? "PASS " : "FAIL ") + name);
  if (!cond) fails.push(name);
}

// 即場重跑推導（寫 qa296/derive296.json）
execFileSync("node", [path.join(ROOT, "qa296", "derive296.js")],
  { stdio: "ignore" });
const derived = JSON.parse(
  fs.readFileSync(path.join(ROOT, "qa296", "derive296.json"), "utf-8"));
const sp = derived.speakers;
const have = derived.have || {};

// ---------- (1) 26 張新圖：存在＋WebP＋>50KB＋live 句數 ----------
const NEW296 = [
  ["cheung_hakfan_think.webp", "cheung_hakfan", "think", 1],
  ["cheung_tsijun_angry.webp", "cheung_tsijun", "angry", 1],
  ["chow_choiyi_shy.webp", "chow_choiyi", "shy", 2],
  ["crew_laolinji_smile.webp", "crew_laolinji", "smile", 1],
  ["gao_wenhan_think.webp", "gao_wenhan", "think", 1],
  ["ho_sang_shy.webp", "ho_sang", "shy", 3],
  ["ko_chunkit_sad.webp", "ko_chunkit", "sad", 1],
  ["ko_chunkit_surprise.webp", "ko_chunkit", "surprise", 1],
  ["lan_ruoxi_surprise.webp", "lan_ruoxi", "surprise", 1],
  ["lan_ruoxi_angry.webp", "lan_ruoxi", "angry", 3],
  ["lin_hiu_surprise.webp", "lin_hiu", "surprise", 2],
  ["lin_hiu_think.webp", "lin_hiu", "think", 1],
  ["lin_hiu_angry.webp", "lin_hiu", "angry", 1],
  ["lui_ging_sad.webp", "lui_ging", "sad", 1],
  ["lui_ging_shy.webp", "lui_ging", "shy", 1],
  ["lui_ging_think.webp", "lui_ging", "think", 3],
  ["so_jiyan_think.webp", "so_jiyan", "think", 2],
  ["so_jiyan_angry.webp", "so_jiyan", "angry", 2],
  ["tong_souwan_sad.webp", "tong_souwan", "sad", 2],
  ["tong_souwan_think.webp", "tong_souwan", "think", 1],
  ["tsui_poushan_smile.webp", "tsui_poushan", "smile", 1],
  ["tsui_poushan_sad.webp", "tsui_poushan", "sad", 1],
  ["tsui_poushan_surprise.webp", "tsui_poushan", "surprise", 1],
  ["tsui_poushan_think.webp", "tsui_poushan", "think", 2],
  ["tsui_poushan_angry.webp", "tsui_poushan", "angry", 2],
  ["yip_manji_think.webp", "yip_manji", "think", 3],
];
ok("v296 新圖 26 張", NEW296.length === 26);
for (const [fn, speaker, expr, n] of NEW296) {
  const p = path.join(FB, fn);
  let good = fs.existsSync(p) && fs.statSync(p).size > 50000;
  if (good) {
    const head = fs.readFileSync(p).subarray(0, 12);
    good = head.subarray(0, 4).toString() === "RIFF" &&
      head.subarray(8, 12).toString() === "WEBP";
  }
  ok(fn + " 存在＋WebP 檔頭＋>50KB", good);
  const live = (sp[speaker] && sp[speaker][expr] && sp[speaker][expr].live) || [];
  ok(fn + " 有 " + n + " 句 live 實線（推導實測）", live.length === n);
}

// ---------- (2) 兩句新對白：落點＋分類 ----------
// 徐寶珊 serious：R_xu_crisis（story_detail_romance_lan_xu.json）
const xuSerious = (sp.tsui_poushan && sp.tsui_poushan.serious && sp.tsui_poushan.serious.live) || [];
ok("徐寶珊 serious 有 1 句 live（孤兒復活）", xuSerious.length === 1);
ok("徐寶珊 serious 嗰句係新加嗰句「呢單生意，我唔係講笑。你跟我做嘢，就要認真。」",
  xuSerious.some(l => l.text === "呢單生意，我唔係講笑。你跟我做嘢，就要認真。"));
ok("徐寶珊 serious 嗰句出自 R_xu_crisis pack",
  xuSerious.some(l => (l.sources || []).some(s => s.includes("story_detail_romance_lan_xu.json"))));
// 張子駿 angry：A_tsijun_crisis（story_detail_rival_mentor.json）
const tsijunAngry = (sp.cheung_tsijun && sp.cheung_tsijun.angry && sp.cheung_tsijun.angry.live) || [];
ok("張子駿 angry 有 1 句 live（死檔復活）", tsijunAngry.length === 1);
ok("張子駿 angry 嗰句係新加嗰句「收聲，聽我講埋先。」",
  tsijunAngry.some(l => l.text === "收聲，聽我講埋先。"));
ok("張子駿 angry 嗰句出自 A_tsijun_crisis pack",
  tsijunAngry.some(l => (l.sources || []).some(s => s.includes("story_detail_rival_mentor.json"))));
// 林曉晴 serious：唔使加對白，舊句已 live
const hiuSerious = (sp.lin_hiu && sp.lin_hiu.serious && sp.lin_hiu.serious.live) || [];
ok("林曉晴 serious 有 1 句 live（唔使加對白，檔案一直存在）", hiuSerious.length === 1);

// ---------- (3) 守門：缺資產嘅 live 組只准係 4 位新星 ----------
const BLOCKED = new Set(["hon_sauting", "kong_siying", "shum_yingsuet", "wu_meilam"]);
const SHADOWS = new Set(["shadow_male", "shadow_female", "shadow_elder", "generic_cinema_asst"]);
const EXPRS = ["smile", "serious", "sad", "surprise", "shy", "think", "angry"];
const missing = [];
for (const speaker of Object.keys(sp).sort()) {
  if (SHADOWS.has(speaker) || speaker === "awi") continue;
  for (const expr of EXPRS) {
    const live = (sp[speaker][expr] && sp[speaker][expr].live) || [];
    if (live.length > 0 && !(have[speaker] || []).includes(expr)) {
      missing.push(speaker + "_" + expr + ".webp");
    }
  }
}
const blockedMissing = missing.filter(f => [...BLOCKED].some(b => f.startsWith(b + "_")));
ok("缺資產嘅 live 組全部係 4 位新星（其餘角一張都唔准缺）",
  missing.length === blockedMissing.length && missing.length > 0);
ok("4 位新星缺 16 張（hon 3／kong 4／shum 4／wu 5）", missing.length === 16);
for (const b of [...BLOCKED].sort()) {
  ok("新星 " + b + " 冇 base 檔（blocked，等新星美術票）",
    !(have[b] || []).includes("base"));
}

// ---------- (4) fullbody 總數 ----------
ok("fullbody 總數 237→261", derived.totalFiles === 261);
ok("fullbody 磁碟實數 261", fs.readdirSync(FB).filter(f => f.endsWith(".webp") || f.endsWith(".png")).length === 261);

console.log("RESULT " + (fails.length ? "FAIL (" + fails.length + ")" : "PASS"));
process.exit(fails.length ? 1 : 0);
