# Soft QA · 《臨記出頭天》 web preview v19w

**Overall: PASS with nits**

Soft session only. No code changes, no publish, no tip.

URL exercised: `https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19w&softBehaviorGate=1`

Fresh game: title showed only「新遊戲」(繼續 hidden), so `starVolunteer_map_v19w` was empty. Skipped tutorial via「跳過教學」, confirmed week 1「到處逛逛」, entered the map. Did not grind weeks or open 1989–1992.

## Checklist

| Item | Result | Evidence |
|---|---|---|
| A. Boot / no blank crash | PASS | Title and map render. Isolated 19w console: only `favicon.ico` 404. Earlier story-loc 404s (`?v=19v`) were from leftover `?v=19t` / `?v=19v` tabs, closed before the clean reload. |
| A. Soft flag | PASS | Address bar kept `softBehaviorGate=1` through play. |
| A. SAVE key `starVolunteer_map_v19w` | PASS | In page source: `const SAVE = "starVolunteer_map_v19w"` with v19w Soft comment. Not read from devtools (no storage script). Continue was hidden at boot, so this key was empty; older `starVolunteer_map_*` keys were not enumerated or cleared. |
| A. Version tip 19w | PASS | URL `?v=19w`. Source SAVE comment and asset queries `?v=19w`. No separate on-screen "19w" badge (matches 唔 tip). |
| B. 茶水間 `cafe_cha`（金龍茶餐廳）bg | PASS | Sheet strip shows cha-chaan-teng art (`bg_loc_cafe_cha.jpg?v=19w`), not a broken placeholder. `05-cafe-cha-bg.png` |
| B. 何生事務所 `agency_ho` bg | PASS with nit | Strip shows office (lamp, cabinets, desk). Full asset includes the cork board; the 92px `center 42% / cover` banner still crops most of the portrait. `07-agency-ho-bg.png` |
| B. Optional 灣仔唱片 `rec_wanchai` | NIT | Sheet has actions but **no** loc background. `bg_loc_rec_wanchai.jpg?v=19w` is HTTP 200; `LOC_SHEET_BG` only wires `cafe_cha` and `agency_ho`. `14-rec-wanchai-no-bg.png` |
| C. Locked gig Detail CTAs | PASS | 星河電視台 week-1 board,「靈異屋邨夜話」: only「暫未能報」+「離開」. No「搏一搏」/ soft-try /「試下報名」. `09-gig-detail-locked.png` |
| C. Toast vs bottom CTAs | PASS | Far-view and C1 result CTAs stay clear. 19w cover fix holds visually. |
| C. Synopsis | PASS | Synopsis sits in a scroll region above the CTAs; not badly clipped. `09-gig-detail-locked.png` |
| C. `stamp_complete` | PASS (not seen broken) | `assets/ui-physical/toast/stamp_complete.png?v=19w` HTTP 200. Stamp graphic was not shown on far-view toast or C1「劇情結算」. |
| D. HUD fame / favor / rumors | PASS | Map/home: 幕前聲量 5, 業內信用 10→11 after C1. Notebook tabs 傳聞 and 人情債. `04-map-week1.png`, `12-rumors.png`, `13-debt-mei.png` |
| D. Soft C1 cafe | PASS | Cafe offers「播事態：先學做動作戲／先賺」with the C1 face line. Played through to two Chinese choices and「劇情結算」. No engineering terms on the cards. `10-c1-story.png`, `11-c1-result.png` |
| D. Soft C3 fame / C4 favor / C5 rumor | SKIPPED (not on UI yet) | Stub gates are later than week 1 (C3 fame>16 @ tvb after C2; C4 favor≥1 @ agency; C5 rumor + autumn/winter). Not forced. |
| D. No-flag still runs | PASS | `?v=19w` without `softBehaviorGate` boots; 繼續 resumes the same save onto the map. `15-no-soft-flag-title.png` |
| E. 鄧 Soft meet | SKIPPED | No 鄧 / 鄧麗萍 entry on the week-1 map or sheets. Mock gate is C5 done + favor≥1 @ agency_ho (`R_tang_meet` only). Not reachable without a multi-week grind; no save edit. |
| F. 美兒 naming | PASS | 人情債:「債主：化妝姐美兒」. No English "May". `13-debt-mei.png` |
| F. 遠觀 | PASS | 金龍茶餐廳「遠觀：廖炳星」: look text, rumor line, loc, only「離開」. No soft-try. Sound not confirmed (no player / no audio error). `06-farview-liu.png` |
| F. Week-1 board mostly locked | NIT (expected) | 星河 four cards all「暫未能報 · 條件未合」. First open also showed tutor「能力不夠」. `08-board-lock-tutor.png` |
| G. HOLD (not failed) | noted | No Vera bust 404 this session. Title hero is the existing smile portrait (raise_brow not rechecked as new art). 1989–1992 not opened. |

## Top nits (non-blocking)

1. Company loc sheets (sampled 灣仔唱片) do not show a background. File exists; only cafe + agency are mounted in `LOC_SHEET_BG`.
2. Cafe/agency sheet art is a 92px cover crop, so the cork and the booth are easy to miss in the banner even though the source jpgs are intact.
3. Toast text「已遠觀廖炳星。」stays in the accessibility tree / `innerText` after it has visually gone. It did **not** cover bottom CTAs.
4. Week-1 company board is all locked (expected nit).
5. Sole console error on the clean 19w load: `favicon.ico` 404.

## Blockers

None for this Soft pass.

## Footer

**Soft≠PASS.** This note is a Soft preview check only. It is not a PASS to tip, merge, or publish. Vera busts, hero raise_brow redo, and 1989–1992 deep content stay HOLD.

## Screenshots

- `/workspace/qa-v19w/01-boot-title.png`
- `/workspace/qa-v19w/02-tutorial-skip.png`
- `/workspace/qa-v19w/03-post-tutorial.png`
- `/workspace/qa-v19w/04-map-week1.png`
- `/workspace/qa-v19w/05-cafe-cha-bg.png`
- `/workspace/qa-v19w/06-farview-liu.png`
- `/workspace/qa-v19w/07-agency-ho-bg.png`
- `/workspace/qa-v19w/08-board-lock-tutor.png`
- `/workspace/qa-v19w/09-gig-detail-locked.png`
- `/workspace/qa-v19w/10-c1-story.png`
- `/workspace/qa-v19w/11-c1-result.png`
- `/workspace/qa-v19w/12-rumors.png`
- `/workspace/qa-v19w/13-debt-mei.png`
- `/workspace/qa-v19w/14-rec-wanchai-no-bg.png`
- `/workspace/qa-v19w/15-no-soft-flag-title.png`
