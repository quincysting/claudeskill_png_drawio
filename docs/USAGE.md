# Usage & API reference

## The core idea: one `layout(d)`, two backends

Write your diagram **once** as a function that takes a builder `d` and calls helper
methods. Run it through `DrawioBuilder` for an editable `.drawio`, and/or
`PptxBuilder` for a native `.pptx`. Both expose the **same** method names.

```python
def layout(d):
    d.txt("title", "My Architecture", 14, 8, 700, 22, 16, 1)
    d.grp("g_lake", "MELT Lake", 250, 40, 220, 300, "#2E7D32", "#EAF7EC")
    d.aws("z_raw", "", 262, 70, "s3", 36)
    d.box("z_raw_t", "RAW zone", 305, 70, 150, 36, fill="#EAF7EC", stroke="none", align="left")
    d.edge("g_collect", "g_lake", "OTLP")

# draw.io
from drawio_builder import DrawioBuilder
d = DrawioBuilder(w=900, h=380, bg_png="original.png", shadow_ids={"g_lake"})
layout(d); d.save("out.drawio")

# native PPTX (same layout!)
from pptx_builder import PptxBuilder
p = PptxBuilder(w=900, h=380, icon_dir="/tmp/icons", shadow_ids={"g_lake"})
layout(p); p.save("out.pptx")
```

## Coordinate system

You work in **source‑image pixel space** (e.g. `1672 × 945`). The draw.io page is set
to that size; the PPTX slide is scaled to a 13.3″‑wide slide at the same aspect.
Tip: place the original PNG as a reference layer (`bg_png=`) and lay shapes on top at
matching pixel coordinates, then toggle the layer to diff.

## Constructors

```python
DrawioBuilder(w=1672, h=945, bg_png=None, bg_opacity=30, shadow_ids=())
PptxBuilder(w=1672, h=945, icon_dir=None, shadow_ids=(), slide_in=13.333)
```

- `bg_png` (draw.io) — embed this image as a **locked, faded reference layer** (hidden by default; toggle in the Layers panel).
- `shadow_ids` — set of group ids that get a subtle drop shadow (depth without heavy borders).
- `icon_dir` (pptx) — folder of cropped AWS icon PNGs (see `crop_icons.py`); missing icons fall back to coloured tiles.

## Helper methods (identical on both builders)

| Method | Purpose |
|---|---|
| `box(id, label, x, y, w, h, fill, stroke, font, fc, bold, align, valign)` | Rounded rectangle with text. `fill="none"`/`stroke="none"` for transparent (label‑only) boxes. |
| `grp(id, label, x, y, w, h, stroke, fill="none", font=9)` | Container/region (title at top). Add its `id` to `shadow_ids` for depth. |
| `band(id, label, x, y, w, h, c, font, fc)` | Solid colour header bar (white bold centred text). |
| `txt(id, label, x, y, w, h, font, bold, align, fc)` | Plain text box (no border/fill). |
| `aws(id, label, x, y, svc, sz=32, catov=None)` | AWS icon by **alias** (see `aws_icons.AWS4`), optional label below. `catov` overrides the category colour. |
| `ic_tb(idp, svc, lab, cx, cw, y, sz, catov)` | Icon **or emoji** centred in a column, with a label below. Pass an emoji string as `svc` for non‑AWS concepts. |
| `pcard(idp, emoji, title, desc, x, y, w, h, c)` | Persona card: round emoji badge + bold title + description. |
| `bv(idp, glyph, lab, cx, cw, y, color)` | Circular value badge (emoji) + label below. |
| `ellipse(id, glyph, x, y, w, h, stroke, fc, font)` | Round badge with a glyph. |
| `edge(s, d, label="", dashed=False)` | Connector from group `s` to group `d` (auto picks side; arrowhead + white label). |
| `save(path)` | Write the file. draw.io validates well‑formedness (catches unescaped `& < >`). |

### Colours
Pass hex strings (`"#2E7D32"`). Borders are auto‑softened toward white for a calmer
look. `aws_icons.CAT` defines the per‑category icon tile colours; `soft(hex, t)`
blends a colour toward white if you need it.

### Icons
- Use **aliases** from `aws_icons.AWS4` (e.g. `"s3"`, `"glue"`, `"eks"`, `"opensearch"`).
- For anything without an AWS stencil, pass an **emoji** to `ic_tb`/`bv`/`pcard`
  (`"☁️"`, `"📱"`, `"👔"`, `"🔒"` …) — rendered as coloured text.
- Adding a new AWS icon? Verify it first (see below) and add to `AWS4`.

## Companion scripts

```bash
# Study a source image (zoomed tiles to read every element)
python3 tiles.py architecture.png 3 3 2.4      # -> /tmp/tiles/r*c*.png

# Verify which raw mxgraph.aws4 resIcon names actually render
python3 verify_icons.py s3 simple_storage_service sagemaker sagemaker_ai
#   -> /tmp/icontest.png  (blank square = name doesn't exist)

# Crop AWS icons for the PPTX backend
python3 crop_icons.py /tmp/icons s3 eks glue   # -> /tmp/icons/<alias>.png

# Render a .drawio to PNG + SVG (and iterate)
bash render.sh out.drawio 1.6                   # -> out.png, out.svg
```

## Recipes

**Declutter a dense diagram:** lighten by relying on `band`/`grp` colour + `shadow_ids`
for structure; keep inner `box` borders thin (automatic); drop tiny repeated icons;
use a clean fixed‑column grid with aligned tops.

**Overlay to check alignment:** build with `bg_png=original.png`, then in draw.io make
the "Original (reference)" layer visible to compare; nudge coordinates; re‑render.

**Export PPTX with real icons:** run `crop_icons.py` for the aliases you use, then
`PptxBuilder(icon_dir="/tmp/icons")`. Every shape stays an editable PowerPoint object.
