---
name: png-to-drawio
description: Recreate a PNG/image of an architecture (or any boxes-and-arrows) diagram as an EDITABLE draw.io (.drawio) file — and optionally a native PowerPoint with real shapes. Use when someone has a raster/AI-generated diagram (e.g. from GPT-image/Codex/Nano-Banana) and wants it editable or vector, or asks to "turn this png into draw.io", "make this diagram editable", "convert image to drawio/mxgraph", or "export the diagram to pptx with real shapes (not a picture)". Ships a verified AWS icon-name map, a draw.io + pptx builder with one shared layout, an icon-name verifier, and a render→compare→iterate loop.
---

# PNG → draw.io (and native PPTX)

## The one thing to know
**There is no reliable automated raster→editable-shapes converter.** draw.io can import an image only as a *picture*, not as shapes. The robust path is **recreation**: study the image, rebuild it as native mxGraph shapes, and tighten with a render→compare loop. Two corollaries:

- **Recreate from the spec, not the pixels.** AI image models garble text/icons. Use the authoritative architecture (SDD / design doc / the user's intent) as ground truth; use the image only for layout.
- **Recreate once → it becomes the editable source.** AI image-gen is non-deterministic and non-editable; the `.drawio` you produce is the durable, versionable artifact (and exports cleanly to PNG/SVG/PDF/PPTX).

## Prerequisites
- **draw.io desktop CLI** (for rendering): `/Applications/draw.io.app/Contents/MacOS/draw.io` on macOS — install with `brew install --cask drawio` (needs sudo for /Applications; if you can't, ask the user to install).
- `python3` + `Pillow`. For PPTX: `python-pptx`. The PPTX icon crop step also uses the draw.io CLI.

## Workflow
1. **Study the source.** `python3 assets/tiles.py <image.png>` writes zoomed regional tiles to `/tmp/tiles/`; read each and enumerate every cluster, node, icon, and label. Cross-check labels against the real spec — don't trust the image's text.
2. **Build the layout** with `assets/drawio_builder.py`. Write one `layout(d)` function using the helpers (`box · grp · band · txt · aws · ic_tb · pcard · bv · edge`). Use a **grid** (fixed columns with aligned tops/bottoms) — it reads far cleaner than copying the source's spacing. Pass `bg_png=<original>` so it's embedded as a **locked, faded reference layer** the recreation overlays (toggle in the Layers panel to diff).
3. **Use only icon names that render.** AWS `mxgraph.aws4` resIcon names are inconsistent — MANY plausible names render as a blank tile. See `references/aws4-icon-map.md` for the verified set (and the known-blank list). For any new icon, run `python3 assets/verify_icons.py name1 name2 …`, render, and view which resolve.
4. **Render → compare → iterate.** `bash assets/render.sh <file.drawio>` exports a PNG + SVG. View it; for alignment, also export with the reference layer visible to overlay on the original. Fix coordinates/labels and repeat 2–4× — this loop is the whole game.
5. **Declutter (optional).** The builder softens borders and supports a shadow set for depth; drop micro-icons and tiny repeated labels to calm dense diagrams.
6. **Export native PPTX (optional).** Crop icons once: `python3 assets/crop_icons.py` → `/tmp/icons/`. Then run the **same** `layout(d)` through `PptxBuilder` (identical interface) — see `assets/example.py`. Every box/icon/label becomes an editable PowerPoint object (not a flat picture).

## Gotchas (hard-won — read these)
- **Escape `& < >` in every label** or draw.io stops parsing at the bad character and silently renders only the part *before* it. The builder escapes for you; if you hand-write XML, don't forget.
- **`timeout` isn't on macOS.** Don't wrap the CLI in `timeout`; run it and poll for the output file (`for i in $(seq 1 25); do [ -s out.png ] && break; sleep 3; done`). Electron export prints a harmless `task_policy_set` warning — ignore it.
- **Icon-name roulette:** e.g. S3 is `s3` (NOT `simple_storage_service`); SageMaker is `sagemaker` (NOT `sagemaker_ai`); OpenSearch is `elasticsearch_service` (NOT `opensearch_service`); IAM is `identity_and_access_management`. Verify before trusting.
- **Emoji work** for non-AWS concepts (SaaS, personas, value icons) — macOS/PowerPoint render them in colour. Use them where no AWS stencil fits.
- **PPTX fonts are tiny** because the layout is in the image's pixel space scaled to a 13.3" slide — that's faithful to a dense diagram; users zoom. To make text bigger, give the diagram a larger canvas or fewer columns.
- **draw.io can't export PPTX** itself; LibreOffice can't import SVG→Impress headless. Use the `PptxBuilder` path for native shapes, or embed a hi-res PNG/SVG for a picture slide.

## Files
- `references/aws4-icon-map.md` — verified resIcon names + known-blank names to avoid + how to verify new ones.
- `assets/aws_icons.py` — `AWS4` map, `CAT` category colours, `soft()` (shared by both builders).
- `assets/drawio_builder.py` — `DrawioBuilder` (write `layout(d)`, then `d.save("x.drawio")`).
- `assets/pptx_builder.py` — `PptxBuilder` (same interface → native `.pptx`; needs cropped icons).
- `assets/crop_icons.py` — crop the AWS icons you use from draw.io stencils into `/tmp/icons/*.png` (for PPTX).
- `assets/verify_icons.py` — render candidate resIcon names so you can see which resolve.
- `assets/render.sh` — draw.io CLI export wrapper (PNG + SVG).
- `assets/tiles.py` — crop an image into zoomed tiles for study.
- `assets/example.py` — a minimal `layout(d)` run through BOTH backends (the canonical usage).
