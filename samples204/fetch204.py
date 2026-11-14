#!/usr/bin/env python3
"""v20a204: download PixelLab character rotations (south/east/west) and
normalize to the stage anchor: 128x128, alpha-bbox height 102px, foot bottom
y115 (bbox bottom exclusive), horizontally centred. Same anchor as the
existing 12 px_* frames (v170/v181)."""
import json, subprocess, sys, urllib.request
from PIL import Image

CHARS = {
    "lan_ruoxi": "b65c7069-1b7b-4a3f-b32d-c51b0064114e",
    "shum_yingsuet": "7dfc9968-258a-4caf-a841-b04b1cff5bc2",
    "kong_siying": "b8b1ec05-322c-4690-ae68-f4a0549f02e9",
}
HELPER = "/home/hatch/workspace/custom-connectors/custom.pixellab/bin/pixellab.py"
SAMPLES = "/home/hatch/workspace/linji-work204/samples204"
OUT = "/home/hatch/workspace/linji-work204/assets/story/awards"

def get_char(cid):
    r = subprocess.run(["python3", HELPER, "get-character", cid],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)

def normalize(src, dst):
    im = Image.open(src).convert("RGBA")
    bb = im.getchannel("A").getbbox()
    if not bb:
        raise SystemExit("empty alpha: " + src)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    scale = 102 / h
    nw, nh = max(1, round(w * scale)), 102
    crop = im.crop(bb).resize((nw, nh), Image.NEAREST)
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    x = (128 - nw) // 2
    canvas.paste(crop, (x, 13), crop)
    canvas.save(dst)
    bb2 = canvas.getchannel("A").getbbox()
    print(f"{dst.split('/')[-1]}: raw h={h} -> {bb2} h={bb2[3]-bb2[1]}")
    assert bb2[3] == 115 and bb2[3] - bb2[1] == 102, "anchor mismatch"

for sid, cid in CHARS.items():
    urls = get_char(cid)["rotation_urls"]
    for d in ("south", "east", "west"):
        raw = f"{SAMPLES}/{sid}_{d}_raw.png"
        r = subprocess.run(["curl", "-sS", "--retry", "5", "--retry-all-errors",
                            "-A", "Mozilla/5.0", "-o", raw, urls[d]],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            raise SystemExit(f"download failed {sid} {d}: {r.stderr.strip()}")
        normalize(raw, f"{OUT}/px_{sid}_{d}.png")
print("OK: 9 files")
