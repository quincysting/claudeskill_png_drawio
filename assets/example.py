#!/usr/bin/env python3
"""Canonical usage: write layout(d) ONCE, render to BOTH draw.io and native PPTX.

  python3 example.py
    -> /tmp/example.drawio   (open in draw.io)
    -> /tmp/example.pptx     (needs icons: run crop_icons.py first; falls back to
                              coloured tiles if /tmp/icons is empty)

This is a tiny demo of the helper API. For a real job, replace layout() with the
recreation of your studied image (use a fixed-column grid + d.edge between groups),
and pass bg_png=<original> to DrawioBuilder to embed the reference layer.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
W, H = 900, 380
SHADOW = {"g_collect", "g_lake", "g_cons"}
BL, GR, SL = "#2563EB", "#2E7D32", "#455A64"


def layout(d):
    d.txt("title", "Example — Ingest → Lake → Consumers", 14, 8, 700, 22, 16, 1)
    # Collect
    d.grp("g_collect", "Collect", 10, 40, 200, 300, BL, "#EAF2FB")
    d.ic_tb("c_srv", "server", "Servers", 20, 80, 70, 30, "general")
    d.ic_tb("c_k8s", "eks", "K8s", 110, 80, 70, 30)
    d.ic_tb("c_saas", "☁️", "SaaS", 20, 80, 150, 30)      # emoji where no AWS stencil fits
    d.box("c_otel", "OpenTelemetry collectors", 20, 200, 180, 36, "#FFFFFF", BL, 8)
    # Lake
    d.grp("g_lake", "MELT Lake (S3 / Iceberg)", 250, 40, 220, 300, GR, "#EAF7EC")
    for i, (zid, nm) in enumerate([("z_raw", "RAW"), ("z_st", "STAGED"), ("z_bz", "BUSINESS")]):
        d.aws(zid, "", 262, 70 + i * 70, "s3", 36)
        d.box(zid + "t", f"{nm} zone", 305, 70 + i * 70, 150, 36, "#EAF7EC", "none", 8, align="left")
    d.aws("z_glue", "Glue + DQ", 262, 280, "glue", 36)
    # Consumers
    d.grp("g_cons", "Consumers", 510, 40, 200, 300, SL, "#F3F5F6")
    for i, (em, t, ds) in enumerate([("👔", "Executives", "KPIs"), ("🛠️", "SRE", "reliability"),
                                     ("🛡️", "SOC", "threats")]):
        d.pcard(f"p{i}", em, t, ds, 520, 70 + i * 80, 180, 64, SL)
    # flow
    d.edge("g_collect", "g_lake", "OTLP")
    d.edge("g_lake", "g_cons", "serve")


if __name__ == "__main__":
    from drawio_builder import DrawioBuilder
    d = DrawioBuilder(w=W, h=H, shadow_ids=SHADOW)
    layout(d)
    print("drawio:", d.save("/tmp/example.drawio"))
    try:
        from pptx_builder import PptxBuilder
        p = PptxBuilder(w=W, h=H, icon_dir="/tmp/icons", shadow_ids=SHADOW)
        layout(p)
        print("pptx:  ", p.save("/tmp/example.pptx"))
    except Exception as e:
        print("pptx skipped:", e)
