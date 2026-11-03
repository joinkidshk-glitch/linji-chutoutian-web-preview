# v19p Soft≠PASS · 出圖 HOLD · 唔 publish

P0 on phone web preview (`index.html` only). Gigs JSON packs, story JSON, Soft status, and art untouched. Soft≠PASS stays. 出圖 HOLD. 唔 publish.

1. SAVE `starVolunteer_map_v19o` → `starVolunteer_map_v19p`.
2. `gigCardHtml` rate line: close the v19m block comment (`/* v19m：無 soft-try 支線 */`). The unclosed `/*` had swallowed `rk`, `sealImg`, `seasonBit`, `bpBit`, `tip`, `discRaw`, `disc`, and `eraTxt` until the next `*/`, so board cards threw ReferenceError on render.
3. Drop unused `const soft = gate.ok && (gate.softTry || …)` in `gigCardHtml`. Rate stays two branches only: 暫未能報 vs 可報名試鏡 %.
