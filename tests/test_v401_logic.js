// v20a401 UI401-4 邏輯測試：35c 第二版加分歸屬＋主標對調（＋殺青獎勵卡同一 dual 行）。
// 來源：index.html 嘅 renderAwardResultHtml（抽函數獨立 eval，見 test_newspaper214_award_logic.js
// 嘅 fixture 寫法）＋ renderPostShootRewardHtml（抽函數＋iconHtml112／postShootDisplayTitle）。
// 斷言：(a) 雙值嗰陣輸出同舊版逐字相同「幕前聲望 +1 · 業內信用 +2」；
//       (b) 單值嗰陣只出有值嗰項，冇加分嗰項成個名都唔列（唔再裸標籤）；
//       (c) 零值嗰陣成行唔出；(d) 他人奪獎＋陳偉翔入圍：P2 主標「陳偉翔散場」，奪獎行降小標，
//       lead 唔再重複奪獎行；(e) 玩家奪獎：P2 冇相、主標本身就係玩家，沿用舊主標；
//       (f) 旁聽（冇代表作）沿用舊主標，冇小標。
// 用法：node tests/test_v401_logic.js [path-to-index.html]
const fs = require("fs");
const path = require("path");
const htmlPath = process.argv[2] || path.join(__dirname, "..", "index.html");
const SRC = fs.readFileSync(htmlPath, "utf8");
let fails = 0, total = 0;
function ok(name, cond, extra) {
  total++;
  if (!cond) { fails++; console.log("FAIL: " + name + (extra ? " -- " + extra : "")); }
  else console.log("PASS: " + name);
}
function extractFn(name) {
  const i = SRC.indexOf("function " + name + "(");
  if (i < 0) return null;
  let depth = 0, started = false;
  for (let k = i; k < SRC.length; k++) {
    const ch = SRC[k];
    if (ch === "{" || ch === "[") { depth++; started = true; }
    if (ch === "}" || ch === "]") {
      depth--;
      if (started && depth === 0) return SRC.slice(i, k + 1);
    }
  }
  return null;
}
function extractConst(name) {
  const i = SRC.indexOf("const " + name + " =");
  if (i < 0) return null;
  let depth = 0, started = false;
  for (let k = i; k < SRC.length; k++) {
    const ch = SRC[k];
    if (ch === "{" || ch === "[") { depth++; started = true; }
    if (ch === "}" || ch === "]") {
      depth--;
      if (started && depth === 0) return SRC.slice(i, k + 2).replace(/^const /, "var ");
    }
  }
  return null;
}
const FN_NAMES = ["fmtNewspaperDate", "newspaperEsc", "newspaperFullName214",
  "awardsCatsSorted184", "awards63FocusCat", "awards63FellowsHtml",
  "awardWinner149", "awardWinLine149", "np214AwardPhoto214", "renderAwardResultHtml",
  "textfix55Walk", "textfix55Str", "textfix55Note", "textfix55Label",
  "iconHtml112", "postShootDisplayTitle", "renderPostShootRewardHtml"];
const CONST_NAMES = ["START", "NP214_AWARD_PHOTOS_214",
  "TEXTFIX55_EXACT", "TEXTFIX55_PHRASES", "TEXTFIX57_EXACT", "TEXTFIX57_PHRASES",
  "TEXTFIX55_SKIP_KEYS", "TEXTFIX55_NOTE_EXACT", "TEXTFIX55_OPTS_SIMPLE", "EMOJI_ICON112"];
const missing = [];
for (const n of FN_NAMES) if (!extractFn(n)) missing.push(n);
for (const n of CONST_NAMES) if (!extractConst(n)) missing.push(n);
if (missing.length) {
  console.log("MISSING: " + missing.join(", "));
  process.exit(1);
}
const defs = [];
for (const n of FN_NAMES) defs.push(extractFn(n));
for (const n of CONST_NAMES) defs.push(extractConst(n));
const sandbox = `
var S = { dayIndex: 152, fame: 20 };
var NEWS82_IMGS = {
  np214_award_awi: "assets/story/newspaper/photo_awi_ceremony.webp",
  np214_award_lok: "assets/story/newspaper/photo_lok_ceremony.webp"
};
${defs.join("\n")}
`;
eval(sandbox);
const count = (s, sub) => s.split(sub).length - 1;
// ---- 35c packs（跟 test_newspaper214_award_logic.js 嘅 fixture） ----
const FEL = [
  { star: "駱家聲", title: "熱浪之夏" },
  { star: "齊鎮海", title: "俠影劍蹤主題曲" },
  { star: "廖炳星", title: "夜半靈異" }
];
const CAT_NEW = { id: "music_new", label: "最佳新人獎", outcome: "nominated",
  line: "入圍咗，未攞獎——街外已經有人記得嗰個樣。", repWorkTitle: "冬日暖歌賀歲合唱",
  weakHint62: "歌藝未夠穩。", fellows63: FEL, winner63: FEL[0] };
const CAT_LEAD = { id: "film_lead", label: "最佳男主角", outcome: "won",
  line: "台上念到你個名。影藝獎今晚企到台中央。", repWorkTitle: "新春大吉", weakHint62: "", fellows63: FEL, winner63: null };
const baseNom = {
  displayName: "星河金碟夜", year: 1990, venue99: "金禧大酒店大禮堂",
  categories: [CAT_NEW], bestOutcome: "nominated",
  repWork62: "冬日暖歌賀歲合唱", dayIndex: 151,
  press: { paperName: "娛樂快報", headline: "金碟夜新人輩出",
    dek: "星河金碟夜結束。金禧大酒店大禮堂嗰晚，陳偉翔嘅名第一次出現喺典禮側記。" },
  news: { outlet: "晚間娛樂快訊", line: "金碟夜散場：金禧大酒店大禮堂，掌聲未完。" },
  metricEcho: "sales", metricEchoLabel: "銷量榜"
};
const baseWon = {
  displayName: "維港影藝獎", year: 1990, venue99: "金禧大酒店大禮堂",
  categories: [CAT_LEAD], bestOutcome: "won",
  repWork62: "新春大吉", dayIndex: 151,
  press: { paperName: "娛樂快報", headline: "陳偉翔奪最佳男主角", dek: "維港影藝獎揭曉。" },
  news: { outlet: "晚間娛樂快訊", line: "影藝獎散場：觀禮席都有鏡頭掃過。" },
  metricEcho: "boxOffice", metricEchoLabel: "票房話題"
};
const baseGal = {
  displayName: "星河金碟夜", year: 1990, venue99: "金禧大酒店大禮堂",
  categories: [{ id: "music_new", label: "最佳新人獎", outcome: "gallery",
    line: "你坐後排，睇人上台領獎。", repWorkTitle: "", weakHint62: "",
    fellows63: FEL, winner63: FEL[0] }],
  bestOutcome: "gallery", repWork62: "", dayIndex: 151,
  press: { paperName: "娛樂快報", headline: "金碟夜新人輩出", dek: "金碟夜揭曉。" },
  news: { outlet: "晚間娛樂快訊", line: "金碟夜散場：掌聲未完。" },
  metricEcho: "sales", metricEchoLabel: "銷量榜"
};
const withRewards = (pack, r) => Object.assign({}, pack, { rewardsApplied: r });
// ---- (a–c) 35c dual 行 ----
const outBoth = renderAwardResultHtml(withRewards(baseNom, { stageVolume: 1, industryCredit: 2 }));
ok("a 雙值輸出同舊版逐字相同", outBoth.includes("幕前聲望 +1 · 業內信用 +2"));
const outCredit = renderAwardResultHtml(withRewards(baseNom, { stageVolume: 0, industryCredit: 2 }));
ok("b 只得信用：出「業內信用 +2」，唔再裸列「幕前聲望」",
  outCredit.includes("業內信用 +2") && !outCredit.includes("幕前聲望"));
const outStage = renderAwardResultHtml(withRewards(baseNom, { stageVolume: 1, industryCredit: 0 }));
ok("b 只得聲望：出「幕前聲望 +1」，唔再裸列「業內信用」",
  outStage.includes("幕前聲望 +1") && !outStage.includes("業內信用"));
const outZero = renderAwardResultHtml(withRewards(baseNom, { stageVolume: 0, industryCredit: 0 }));
ok("c 零值：成行唔出", !outZero.includes("psr-dual"));
// ---- (a–c) 殺青獎勵卡同一 dual 行 ----
const psrBoth = renderPostShootRewardHtml({ title: "試玩通告", type: "電影", cards: [], dualDelta: { stageVolume: 1, industryCredit: 2 } });
ok("a2 殺青卡雙值逐字相同", psrBoth.includes("幕前聲望 +1 · 業內信用 +2"));
const psrCredit = renderPostShootRewardHtml({ title: "試玩通告", type: "電影", cards: [], dualDelta: { stageVolume: 0, industryCredit: 2 } });
ok("b2 殺青卡只得信用：唔裸列聲望", psrCredit.includes("業內信用 +2") && !psrCredit.includes("幕前聲望"));
const psrZero = renderPostShootRewardHtml({ title: "試玩通告", type: "電影", cards: [], dualDelta: {} });
ok("c2 殺青卡零值：成行唔出", !psrZero.includes("psr-dual"));
// ---- (d) 他人奪獎＋陳偉翔入圍：主標對調 ----
ok("d1 P2 主標係「陳偉翔散場」", outBoth.includes('<h3 class="np214-headline2">陳偉翔散場</h3>'));
ok("d2 奪獎行降做小標（np214-subhead401）",
  outBoth.includes("np214-subhead401") && outBoth.includes("駱家聲憑《熱浪之夏》奪獎"));
ok("d3 奪獎行全篇只出一次（小標；唔再主標＋lead 各一次）",
  count(outBoth, "駱家聲憑《熱浪之夏》奪獎") === 1);
ok("d4 lead 唔再以奪獎行開頭，淨低觀察對象句",
  outBoth.includes("散場報道的觀察對象，是憑《冬日暖歌賀歲合唱》入圍的陳偉翔"));
// ---- (e) 玩家奪獎：P2 冇相、主標本身就係玩家，唔存在圖文錯配，沿用舊主標 ----
// （win149 係 null——winner63 係 null，因為得主就係玩家；奪獎行由 playerWinLine214 出。）
const outWon = renderAwardResultHtml(withRewards(baseWon, { stageVolume: 3, industryCredit: 1 }));
ok("e1 玩家奪獎：P2 主標沿用玩家奪獎行", outWon.includes('<h3 class="np214-headline2">陳偉翔憑《新春大吉》奪獎</h3>'));
ok("e2 玩家奪獎：冇小標（唔使降）", !outWon.includes("np214-subhead401"));
ok("e3 玩家奪獎行仍在位（主標）", outWon.includes("陳偉翔憑《新春大吉》奪獎"));
// ---- (f) 旁聽（冇代表作）：沿用舊主標，冇小標 ----
const outGal = renderAwardResultHtml(withRewards(baseGal, { stageVolume: 0, industryCredit: 0 }));
ok("f1 旁聽：P2 主標沿用得主奪獎行", outGal.includes('<h3 class="np214-headline2">駱家聲憑《熱浪之夏》奪獎</h3>'));
ok("f2 旁聽：冇小標", !outGal.includes("np214-subhead401"));
console.log("\n" + (fails ? "FAILED: " + fails + " / " + total : "ALL PASS (" + total + ")"));
process.exit(fails ? 1 : 0);
