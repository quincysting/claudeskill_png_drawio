#!/usr/bin/env python3
"""Render candidate mxgraph.aws4 resIcon names so you can SEE which resolve.
Many plausible names render as a blank tile — always verify before using one.

  python3 verify_icons.py s3 simple_storage_service sagemaker sagemaker_ai ...

Writes /tmp/icontest.png — open it; names under a blank coloured square do NOT
exist (use a different name). Pass the raw mxgraph.aws4 resIcon name (not the
aws_icons alias).
"""
import sys, os, subprocess, time

DRAWIO = os.environ.get("DRAWIO", "/Applications/draw.io.app/Contents/MacOS/draw.io")
names = sys.argv[1:]
if not names:
    print(__doc__); sys.exit(1)

cells = []
for i, nm in enumerate(names):
    x, y = 10 + (i % 5) * 160, 10 + (i // 5) * 120
    st = (f"sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=#945DF2;gradientDirection=north;"
          f"fillColor=#4D27AA;strokeColor=#fff;html=1;aspect=fixed;shape=mxgraph.aws4.resourceIcon;"
          f"resIcon=mxgraph.aws4.{nm};")
    cells.append(f'<mxCell id="n{i}" value="{nm}" style="{st}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="46" height="46" as="geometry"/></mxCell>')
rows = (len(names) + 4) // 5
xml = (f'<mxfile><diagram name="t"><mxGraphModel pageWidth="820" pageHeight="{rows*120+40}"><root>'
       '<mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + '</root></mxGraphModel></diagram></mxfile>')
open("/tmp/_icontest.drawio", "w").write(xml)
out = "/tmp/icontest.png"
if os.path.exists(out): os.remove(out)
subprocess.run([DRAWIO, "--export", "--format", "png", "--scale", "1.4",
                "--output", out, "/tmp/_icontest.drawio", "--no-sandbox"],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for _ in range(25):
    if os.path.exists(out) and os.path.getsize(out) > 0: break
    time.sleep(2)
print("wrote", out, "- view it; blank squares = name does not exist")
