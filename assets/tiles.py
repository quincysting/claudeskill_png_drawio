#!/usr/bin/env python3
"""Crop a source image into zoomed regional tiles for study (read each tile to
enumerate every cluster/node/label before recreating).

  python3 tiles.py image.png [cols] [rows] [zoom]
    cols,rows default 3,3 ; zoom default 2.4

Writes /tmp/tiles/r<row>c<col>.png. For very dense diagrams use 4x4 or crop
specific regions manually.
"""
import sys, os
from PIL import Image

img = sys.argv[1]
cols = int(sys.argv[2]) if len(sys.argv) > 2 else 3
rows = int(sys.argv[3]) if len(sys.argv) > 3 else 3
zoom = float(sys.argv[4]) if len(sys.argv) > 4 else 2.4
ov = 40  # overlap so nothing is split across a tile edge

im = Image.open(img); W, H = im.size
os.makedirs("/tmp/tiles", exist_ok=True)
for r in range(rows):
    for c in range(cols):
        l = max(0, int(c * W / cols) - ov); u = max(0, int(r * H / rows) - ov)
        rr = min(W, int((c + 1) * W / cols) + ov); bb = min(H, int((r + 1) * H / rows) + ov)
        t = im.crop((l, u, rr, bb)).resize((int((rr - l) * zoom), int((bb - u) * zoom)))
        t.save(f"/tmp/tiles/r{r}c{c}.png")
print(f"image {W}x{H} -> {cols*rows} tiles in /tmp/tiles/ (read each to catalogue elements)")
