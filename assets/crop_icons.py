#!/usr/bin/env python3
"""Crop the AWS icons used by the diagram from draw.io stencils into PNGs, so the
PptxBuilder can place them as individual images.

  python3 crop_icons.py [outdir] [alias1 alias2 ...]
    outdir  default /tmp/icons
    aliases default = every alias in aws_icons.AWS4

Renders a grid of mxgraph.aws4 resourceIcons via the draw.io CLI, then auto-trims
each cell (whitespace bbox) so every icon is captured exactly regardless of the
export's bbox/scale rounding.
"""
import sys, os, json, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aws_icons import AWS4, CAT

DRAWIO = os.environ.get("DRAWIO", "/Applications/draw.io.app/Contents/MacOS/draw.io")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/icons"
keys = sys.argv[2:] or list(AWS4)
os.makedirs(OUT, exist_ok=True)
COLS, CELL, ISZ = 8, 80, 64

cells = []
for i, svc in enumerate(keys):
    if svc not in AWS4:
        print("skip unknown alias:", svc); continue
    res, cat = AWS4[svc]; fill, grad = CAT[cat]
    cxx, cyy = (i % COLS) * CELL, (i // COLS) * CELL
    st = (f"sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor={grad};gradientDirection=north;"
          f"fillColor={fill};strokeColor=#ffffff;html=1;aspect=fixed;shape=mxgraph.aws4.resourceIcon;"
          f"resIcon=mxgraph.aws4.{res};")
    cells.append(f'<mxCell id="i{i}" value="" style="{st}" vertex="1" parent="1">'
                 f'<mxGeometry x="{cxx}" y="{cyy}" width="{ISZ}" height="{ISZ}" as="geometry"/></mxCell>')
xml = ('<mxfile><diagram name="icons"><mxGraphModel pageWidth="700" pageHeight="700"><root>'
       '<mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')
open("/tmp/_iconsheet.drawio", "w").write(xml)

sheet = "/tmp/_iconsheet.png"
if os.path.exists(sheet): os.remove(sheet)
subprocess.run([DRAWIO, "--export", "--format", "png", "--scale", "3", "--border", "0",
                "--output", sheet, "/tmp/_iconsheet.drawio", "--no-sandbox"],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for _ in range(25):
    if os.path.exists(sheet) and os.path.getsize(sheet) > 0: break
    time.sleep(2)

from PIL import Image, ImageChops
im = Image.open(sheet).convert("RGB"); W, Hh = im.size
rows = (len(keys) + COLS - 1) // COLS
sx = W / ((COLS - 1) * CELL + ISZ)
sy = Hh / ((rows - 1) * CELL + ISZ)

def trim(img):
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bbox = ImageChops.difference(img, bg).getbbox()
    return img.crop(bbox) if bbox else img

n = 0
for i, svc in enumerate(keys):
    if svc not in AWS4: continue
    cxx, cyy = (i % COLS) * CELL, (i // COLS) * CELL
    L, U = round(cxx * sx), round(cyy * sy)
    R, B = round((cxx + 72) * sx), round((cyy + 72) * sy)  # stop before next tile, then trim
    trim(im.crop((L, U, min(R, W), min(B, Hh)))).save(os.path.join(OUT, svc + ".png"))
    n += 1
print(f"cropped {n} icons -> {OUT}")
