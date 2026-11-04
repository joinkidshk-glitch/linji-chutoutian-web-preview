# HUD／map polaroid web-opt notes（?v=19u timeout fix）

> 2026-11-04（Asia/Hong_Kong）｜GD  
> Soft≠PASS。Overwrite 原路徑；舊檔留 `_bak`。

## Problem

Preview `?v=19u` timeout on:

- `assets/ui-physical/hud/hud_shell_bar.png`（was **~240 KB**, 1280×320 RGBA）
- `assets/ui-physical/map-frame/map_polaroid_frame.png`（was **~725 KB**, 940×1130 RGBA）

## Fix

| file | before | after | method |
|---|---:|---:|---|
| `map-frame/map_polaroid_frame.png` | 724824 | **7324** | Pillow procedural cream frame；`contentRectNorm` 對齊 `slices.json` map_polaroid；中心相井 **alpha=0**；厚底邊；少 mid-alpha |
| `map-frame/map_polaroid_frame.jpg` | 93391 | **23046** | black-fill companion refresh |
| `hud/hud_shell_bar.png` | 239629 | **4720** | Pillow procedural plastic／chrome shell bar（canon `shell` `#C8BDB0`／`shell_dark`）；同尺寸 1280×320；保留透明底 |
| `hud/hud_shell_bar.jpg` | 29131 | **17600** | companion refresh |

## Backups（唔刪）

- `map-frame/map_polaroid_frame_bak.png` / `_bak.jpg`
- `hud/hud_shell_bar_bak.png` / `_bak.jpg`

## Layout semantics（unchanged）

`slices.json` → `map_polaroid.contentRectNorm`:

- x≈0.0883, y≈0.0708, w≈0.8234, h≈0.7274  
- outerAspect 1:1.2；transparent photo well；thicker bottom border

iOS／preview 應繼續用**同路徑**（overwrite），唔使改 tip／LIVE wiring；清 cache 後再測 `?v=`。

## Soft notes

- Polaroid／HUD 為程式實體感切圖，非最終彩繪；可再加紙紋／膠面高光。
- Soft≠PASS；**89–92 HOLD**。

## 2026-11-04 polaroid well fix
- Regenerated from `_bak` texture + punched transparent well per slices.json contentRectNorm (was solid black briefly).
- Soft≠PASS.
