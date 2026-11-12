// v20a128 A3 N16・邏輯測試：巧遇第三方講者偵測 enc79ThirdParty128。
// 驗：副導／導演／場務／伙記開頭嘅「N」步認到第三方（名＋影 stem＋去前綴文案）；
// 純旁白／主角句／抉擇步唔認。
// 反證：對 pristine main 行 → enc79ThirdParty128 唔存在 → FAIL。
// 用法：node tests/test_ui128n16_logic.js [path-to-index.html]
const fs = require('fs');
const path = require('path');
const htmlPath = process.argv[2] || path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
let fails = [];
function ok(name, cond){ if(!cond) fails.push(name); console.log((cond?'PASS':'FAIL')+' '+name); }
function extractBlock(startMarker){
  const i = html.indexOf(startMarker);
  if(i<0) throw new Error('not found: '+startMarker);
  let depth=0, j=html.indexOf('{', i);
  for(; j<html.length; j++){
    if(html[j]==='{') depth++;
    else if(html[j]==='}'){ depth--; if(depth===0) break; }
  }
  return html.slice(i, j+1);
}
let mapSrc, fnSrc;
try{
  mapSrc = extractBlock('const ENC79_THIRD128 = {');
  fnSrc = extractBlock('function enc79ThirdParty128(step){');
}catch(e){
  // 反證：pristine main 冇 enc79ThirdParty128——乾淨 FAIL，唔好 crash。
  ok('enc79ThirdParty128 存在（pristine 冇，預期 FAIL）', false);
  console.log('TOTAL FAIL: enc79ThirdParty128 唔存在');
  process.exit(1);
}
eval(mapSrc + '\n' + fnSrc);

ok('副導句認到第三方', JSON.stringify(enc79ThirdParty128({who:"N", text:"副導：喂，後生仔，企喺度做乜？唔好阻住大佬度橋啦。"})) === JSON.stringify({name:"副導", stem:"shadow_male", text:"喂，後生仔，企喺度做乜？唔好阻住大佬度橋啦。"}));
ok('導演句認到第三方', JSON.stringify(enc79ThirdParty128({who:"N", text:"導演：Action！"})) === JSON.stringify({name:"導演", stem:"shadow_male", text:"Action！"}));
ok('場務句認到第三方', JSON.stringify(enc79ThirdParty128({who:"N", text:"場務：各位，食飯啦！"})).includes('"name":"場務"'));
ok('裸伙記句認到第三方（LEGACY 冇裸伙記，呢度補咗）', JSON.stringify(enc79ThirdParty128({who:"N", text:"伙記：先生，要加水嗎？"})).includes('"name":"伙記"'));
ok('純旁白唔認（冇「職銜：」開頭）', enc79ThirdParty128({who:"N", text:"金龍茶餐廳下晝三點幾，冷氣唔夠凍。"}) === null);
ok('阿偉句唔認（唔係第三方）', enc79ThirdParty128({who:"N", text:"阿偉：我係阿偉。"}) === null);
ok('星句唔認（who S）', enc79ThirdParty128({who:"S", text:"副導：喂…"}) === null);
ok('抉擇步唔認', enc79ThirdParty128({choice:true, who:"N", text:"副導：揀邊個？"}) === null);
ok('空步唔認唔 crash', enc79ThirdParty128(null) === null && enc79ThirdParty128({who:"N", text:""}) === null);

console.log(fails.length ? 'TOTAL FAIL: '+fails.join(', ') : 'TOTAL PASS');
process.exit(fails.length ? 1 : 0);
