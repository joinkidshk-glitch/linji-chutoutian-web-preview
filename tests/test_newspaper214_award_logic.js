// v20a214 NP214 頒獎結果卡報紙版式（logic）
// 來源：index.html 嘅 renderAwardResultHtml／np214AwardPhoto214／fmtNewspaperDate／newspaperEsc／newspaperFullName214
// ＋ awards63FellowsHtml（★）＋ awardsCatsSorted184／awards63FocusCat／awardWinner149／awardWinLine149
// ＋ TEXTFIX55／TEXTFIX57 載入正規化（術語掃蕩）。
// 段：(a) 報紙版式 (b) 保留項（focus 先／同屆提名一次／安慰行／代表作／weakHint／聲望信用行）
//     (c) v211 意圖（metric 第二版用真數據、★圖例、唔再 toast）
//     (d) 相片揀相 (e) 術語正規化（TEXTFIX55_EXACT 6 條＋GIG_SUB 夜半靈異）
//     (f) 報紙路徑零 🏆／零「典禮後仍有人提起」／零碟市／臨記席
// 用法：node tests/test_newspaper214_award_logic.js
// 反證：對 pristine main（冇 np214AwardPhoto214／冇 np214- 版式）乾淨 FAIL，唔 crash。
const fs = require("fs");
const path = require("path");
const SRC = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");
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
  "textfix55DropSents", "textfix55GigField"];
const CONST_NAMES = ["START", "NP214_AWARD_PHOTOS_214",
  "TEXTFIX55_EXACT", "TEXTFIX55_PHRASES", "TEXTFIX57_EXACT", "TEXTFIX57_PHRASES",
  "TEXTFIX55_SKIP_KEYS", "TEXTFIX57_KEY_RENAME", "TEXTFIX55_NOTE_EXACT", "TEXTFIX55_OPTS_SIMPLE",
  "TEXTFIX55_GIG_EXACT", "TEXTFIX55_GIG_SUB", "TEXTFIX57_GIG_REQ", "TEXTFIX55_GIG_PHRASES",
  "TEXTFIX55_POLICY_KW", "TEXTFIX55_ERA_KW"];
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
// ---- test packs（跟 test_awards186／192 嘅寫法） ----
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
const nomPack = {
  displayName: "星河金碟夜", year: 1990, venue99: "金禧大酒店大禮堂",
  categories: [CAT_NEW], bestOutcome: "nominated",
  repWork62: "冬日暖歌賀歲合唱", dayIndex: 151,
  press: { paperName: "娛樂快報", headline: "金碟夜新人輩出",
    dek: "星河金碟夜結束。金禧大酒店大禮堂嗰晚，陳偉翔嘅名第一次出現喺典禮側記。" },
  news: { outlet: "晚間娛樂快訊", line: "金碟夜散場：金禧大酒店大禮堂，掌聲未完。" },
  metricEcho: "sales", metricEchoLabel: "銷量榜",
  rewardsApplied: { stageVolume: 1, industryCredit: 2 }
};
const wonPack = {
  displayName: "維港影藝獎", year: 1990, venue99: "金禧大酒店大禮堂",
  categories: [CAT_LEAD], bestOutcome: "won",
  repWork62: "新春大吉", dayIndex: 151,
  press: { paperName: "娛樂快報", headline: "陳偉翔奪最佳男主角", dek: "維港影藝獎揭曉。" },
  news: { outlet: "晚間娛樂快訊", line: "影藝獎散場：觀禮席都有鏡頭掃過。" },
  metricEcho: "boxOffice", metricEchoLabel: "票房話題",
  rewardsApplied: { stageVolume: 3, industryCredit: 1 }
};
const galleryPack = {
  displayName: "星河金碟夜", year: 1990, venue99: "金禧大酒店大禮堂",
  categories: [{ id: "music_new", label: "最佳新人獎", outcome: "gallery",
    line: "你坐後排，睇人上台領獎。", repWorkTitle: "", weakHint62: "",
    fellows63: FEL, winner63: FEL[0] }],
  bestOutcome: "gallery", repWork62: "", dayIndex: 151,
  press: { paperName: "娛樂快報", headline: "金碟夜新人輩出", dek: "金碟夜揭曉。" },
  news: { outlet: "晚間娛樂快訊", line: "金碟夜散場：掌聲未完。" },
  metricEcho: "sales", metricEchoLabel: "銷量榜",
  rewardsApplied: { stageVolume: 0, industryCredit: 0 }
};
/* 旁聽＋得主係其他人（廖炳星）：第二版寫佢嘅奪獎行，但冇相 */
const galOtherPack = {
  displayName: "星河金碟夜", year: 1990, venue99: "金禧大酒店大禮堂",
  categories: [{ id: "music_new", label: "最佳新人獎", outcome: "gallery",
    line: "你坐後排，睇人上台領獎。", repWorkTitle: "", weakHint62: "",
    fellows63: [{ star: "廖炳星", title: "夜半靈異" }, { star: "齊鎮海", title: "俠影劍蹤主題曲" }],
    winner63: { star: "廖炳星", title: "夜半靈異" } }],
  bestOutcome: "gallery", repWork62: "", dayIndex: 151,
  press: { paperName: "娛樂快報", headline: "金碟夜新人輩出", dek: "金碟夜揭曉。" },
  news: { outlet: "晚間娛樂快訊", line: "金碟夜散場：掌聲未完。" },
  metricEcho: "sales", metricEchoLabel: "銷量榜",
  rewardsApplied: { stageVolume: 0, industryCredit: 0 }
};
const count = (s, sub) => s.split(sub).length - 1;
const outNom = renderAwardResultHtml(nomPack);
const outWon = renderAwardResultHtml(wonPack);
const outGal = renderAwardResultHtml(galleryPack);
const outGalOther = renderAwardResultHtml(galOtherPack);
// ---- (a) 報紙版式 ----
ok("a1 報頭係維港日報＋英文報名", outNom.includes("維港日報") && outNom.includes("VICTORIA HARBOUR DAILY"));
ok("a2 日期係典禮日＋1（1990年6月2日 星期六）", outNom.includes("1990年6月2日 星期六"));
ok("a3 大標題係 pack.press.headline", outNom.includes("金碟夜新人輩出"));
ok("a4 副題係 pack.press.dek", outNom.includes("星河金碟夜結束。"));
ok("a5 主文兩欄＋右直欄影視娛樂", outNom.includes("np214-body2") && outNom.includes("影視娛樂"));
ok("a6 兩版（第一版＋第二版切換）", outNom.includes("第一版") && outNom.includes("第二版"));
ok("a7 版尾在位", outNom.includes("第一版 · 頒獎結果") && outNom.includes("第二版 · 銷量榜"));
ok("a8 唔再係票根式卡片（冇 psr-sheet／psr-cards／psr-press）",
  !outNom.includes("psr-sheet") && !outNom.includes("psr-cards") && !outNom.includes("psr-press"));
ok("a9 冇 dayIndex 嗰陣日期跌返 S.dayIndex＋1（1990年6月3日 星期日）",
  renderAwardResultHtml(Object.assign({}, nomPack, { dayIndex: undefined })).includes("1990年6月3日 星期日"));
// ---- (b) 保留項 ----
ok("b1 focus 格行先（最佳新人獎行喺同屆提名之前）",
  outNom.indexOf("最佳新人獎") < outNom.indexOf("同屆提名"));
ok("b2 同屆提名只出一次", count(outNom, "同屆提名") === 1);
ok("b3 fellows 只得一個節點", count(outNom, "psr-fellows63") === 1);
ok("b4 安慰行在位（何生差少少啫）", outNom.includes("差少少啫，唔緊要，下年再嚟過。"));
ok("b5 代表作行在位（冬日暖歌賀歲合唱）", outNom.includes("冬日暖歌賀歲合唱"));
ok("b6 weakHint 診斷在位", outNom.includes("歌藝未夠穩。"));
ok("b7 聲望／信用行逐字保留", outNom.includes("幕前聲望 +1 · 業內信用 +2"));
ok("b8 獎項 label 各出一次（最佳新人獎）", count(outNom, "最佳新人獎") === 1);
// ---- (c) v211 意圖 ----
ok("c1 metric 第二版用真實得主數據（駱家聲憑《熱浪之夏》奪獎）",
  outNom.includes("駱家聲憑《熱浪之夏》奪獎"));
ok("c2 won 版第二版係玩家奪獎行（陳偉翔憑《新春大吉》奪獎）",
  outWon.includes("陳偉翔憑《新春大吉》奪獎"));
ok("c3 gallery 版第二版係得主奪獎行（駱家聲憑《熱浪之夏》奪獎）",
  outGal.includes("駱家聲憑《熱浪之夏》奪獎"));
ok("c3b gallery 得主係其他人嗰陣第二版一樣寫實（廖炳星憑《夜半靈異》奪獎）",
  outGalOther.includes("廖炳星憑《夜半靈異》奪獎"));
ok("c4 唔再有 stub 句「典禮後仍有人提起」",
  !outNom.includes("典禮後仍有人提起") && !outWon.includes("典禮後仍有人提起") && !outGal.includes("典禮後仍有人提起") && !outGalOther.includes("典禮後仍有人提起"));
ok("c5 同屆提名加「★為得主」圖例", outNom.includes("★為得主"));
ok("c6 得主行有 ★ 標記（★ 駱家聲）", outNom.includes("★ 駱家聲"));
ok("c6b won 版同屆提名加玩家一行（★ 陳偉翔《新春大吉》＋★為得主圖例，v211 C1 還原）",
  outWon.includes("★ 陳偉翔《新春大吉》") && outWon.includes("★為得主"));
ok("c6c won 版同屆提名玩家行排第一（喺駱家聲之前）",
  outWon.indexOf("★ 陳偉翔") < outWon.indexOf("駱家聲"));
ok("c7 presentAwardResult 唔再叫 toast（v211 A1，source check；推辭 toast 留喺 presentAwardInvite，唔入呢段）",
  (() => {
    const a = SRC.indexOf("function presentAwardResult");
    const b = SRC.indexOf("function presentAwardInvite(", a);
    // rebase 後 v211 嘅 hideToast211() 註解本身提到 toast() 字面——先剝走 /* */ 註解再驗（同 B2 stub 陷阱同一做法）
    const seg = SRC.slice(a, b).replace(/\/\*[\s\S]*?\*\//g, "");
    return !seg.includes("toast(") && seg.includes("hideToast211()");
  })());
// ---- (d) 相片揀相 ----
const phNom = np214AwardPhoto214(nomPack);
const phWon = np214AwardPhoto214(wonPack);
const phGal = np214AwardPhoto214(galleryPack);
ok("d1 入圍焦點用陳偉翔相", phNom && phNom.key === "np214_award_awi" && phNom.src.includes("photo_awi_ceremony.webp"));
ok("d2 玩家贏用陳偉翔相", phWon && phWon.key === "np214_award_awi");
ok("d3 得主係駱家聲用駱家聲相（gallery）", phGal && phGal.key === "np214_award_lok" && phGal.src.includes("photo_lok_ceremony.webp"));
ok("d4 其他得主冇相就 null", np214AwardPhoto214({
  displayName: "星河金碟夜", bestOutcome: "gallery",
  categories: [{ id: "music_new", label: "最佳新人獎", outcome: "gallery",
    line: "旁聽。", repWorkTitle: "", weakHint62: "",
    fellows63: [{ star: "齊鎮海", title: "俠影劍蹤主題曲" }], winner63: { star: "齊鎮海", title: "俠影劍蹤主題曲" } }],
  repWork62: ""
}) === null);
ok("d5 推辭嗰陣唔用陳偉翔相（得主駱家聲就用駱家聲相）",
  np214AwardPhoto214(nomPack, { declined: true }) && np214AwardPhoto214(nomPack, { declined: true }).key === "np214_award_lok");
ok("d6 推辭＋玩家贏嗰陣冇相（玩家冇去，得主資料唔齊）",
  np214AwardPhoto214(wonPack, { declined: true }) === null);
ok("d7 入圍嗰陣結果卡第一版出陳偉翔相、第二版都出（唔係駱家聲）",
  outNom.includes("photo_awi_ceremony.webp") && !outNom.includes("photo_lok_ceremony.webp"));
ok("d8 gallery 嗰陣結果卡出駱家聲相（第一版）",
  outGal.includes("photo_lok_ceremony.webp"));
ok("d9 NEWS82_IMGS 冇嗰陣跌返常量路徑（assets/story/newspaper/）",
  (() => {
    const keep = NEWS82_IMGS; NEWS82_IMGS = null;
    const p = np214AwardPhoto214(nomPack); NEWS82_IMGS = keep;
    return p && p.src === "assets/story/newspaper/photo_awi_ceremony.webp";
  })());
// ---- (e) 術語正規化 ----
/* 呢 6 句係 STUB_AWARDS_CEREMONY_v1.json 嘅真實舊字串（TEXTFIX55_EXACT 嘅 key，一字唔差先對得上）。 */
const OLD_AWARD_STUB = {
  inviteDek: "唱片年終有金碟夜。你收到一張席位信——碟市邊個上鏡，席上見。",
  headline: "金碟夜，碟市多個名",
  dek: "星河金碟夜結束。有臨記席名字第一次出現喺典禮側記。",
  newsLine: "金碟夜散場：碟市掌聲未完。",
  galleryLine: "你坐席上，聽人謝唱片公司。你記住碟市點樣叫人名。",
  newsLine2: "台慶頒獎夜散場：臨記席都有鏡頭掃過。"
};
const cleaned = textfix55Walk(JSON.parse(JSON.stringify(OLD_AWARD_STUB)), null, null, TEXTFIX55_OPTS_SIMPLE);
ok("e1 TEXTFIX55_EXACT 走一遍：6 句舊字串全部乾淨（冇碟市／臨記席）",
  !JSON.stringify(cleaned).includes("碟市") && !JSON.stringify(cleaned).includes("臨記席"));
ok("e2 「金碟夜，碟市多個名」→「金碟夜新人輩出」", cleaned.headline === "金碟夜新人輩出");
ok("e2b 請柬句「碟市邊個上鏡」→「邊個上台領獎」",
  cleaned.inviteDek === "唱片年終有金碟夜。你收到一張席位信——邊個上台領獎，席上見。");
ok("e2c 旁聽句「碟市點樣叫人名」→「樂壇點樣叫人名」",
  cleaned.galleryLine === "你坐席上，聽人謝唱片公司。你記住樂壇點樣叫人名。");
ok("e2d 「臨記席都有鏡頭掃過」→「觀禮席都有鏡頭掃過」",
  cleaned.newsLine2 === "台慶頒獎夜散場：觀禮席都有鏡頭掃過。");
ok("e3 「碟市掌聲未完」→「掌聲未完」", cleaned.newsLine === "金碟夜散場：掌聲未完。");
ok("e4 GIG_SUB：workTitle「夜半靈異主題曲主唱」→「夜半靈異」",
  textfix55GigField("夜半靈異主題曲主唱", "workTitle") === "夜半靈異");
ok("e5 GIG_SUB：title「《夜半靈異主題曲主唱》主唱」→「《夜半靈異》主唱」",
  textfix55GigField("《夜半靈異主題曲主唱》主唱", "title") === "《夜半靈異》主唱");
// ---- (f) 報紙路徑零 🏆／零術語 ----
ok("f1 渲染結果零 🏆", !outNom.includes("🏆") && !outWon.includes("🏆") && !outGal.includes("🏆") && !outGalOther.includes("🏆"));
ok("f2 渲染結果零碟市／臨記席", !outNom.includes("碟市") && !outNom.includes("臨記席") && !outWon.includes("碟市"));
ok("f3 圖說唔寫獎項 label（最佳新人獎只出一次，見 b8）", count(outNom, "最佳新人獎") === 1);
console.log(`\n${total - fails}/${total} passed`);
if (fails) process.exit(1);
