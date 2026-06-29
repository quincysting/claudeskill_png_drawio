# The method: how to recreate a PNG as editable shapes

This is the reasoning behind the skill — useful whether you're driving it through
Claude or doing it by hand.

## 0. Accept the core truth: there is no auto‑converter

draw.io (and every reliable tool) can only **import a raster as a picture**, not as
shapes. "Image → editable shapes" converters are either nonexistent or low‑fidelity
(CV/OCR guesses that mangle dense diagrams). The dependable path is **recreation**.
That sounds slow — this skill's whole job is to make it fast and repeatable.

Two consequences shape everything below:

- **Recreate from the spec, not the pixels.** AI image models garble text and icons.
  Treat the image as a *layout reference*, and use the authoritative architecture
  (design doc, the user's intent) as the source of truth for labels.
- **The recreation becomes the source of truth.** AI image‑gen is non‑deterministic
  and non‑editable; your `.drawio` is the durable, versionable artifact that re‑exports
  to PNG/SVG/PDF/PPTX cleanly.

## 1. Study

Crop the source into zoomed tiles (`tiles.py`) and read each one. Enumerate, region by
region: every container, node, icon, and label. Note the left‑to‑right flow and the
colour grouping. Write the inventory down before drawing anything.

## 2. Lay out on a grid (don't copy the mess)

AI diagrams are often visually busy. You'll get a cleaner, more credible result by
recreating on a **disciplined grid**: fixed column x‑positions, aligned tops/bottoms,
consistent gutters. Map each studied cluster to a column. This is usually *better*
than the original, not just equal.

## 3. Use icons that actually render

The single biggest time‑sink in draw.io's AWS set is that **icon names are
inconsistent and many plausible names render blank**:

- S3 is `s3`, **not** `simple_storage_service`
- SageMaker is `sagemaker`, **not** `sagemaker_ai`
- OpenSearch is `elasticsearch_service`, **not** `opensearch_service`
- IAM is `identity_and_access_management`, **not** `iam_identity_center`

The verified set lives in [`../references/aws4-icon-map.md`](../references/aws4-icon-map.md)
and `assets/aws_icons.py`. For any new icon, run `verify_icons.py <names…>`, view the
output, and only use names that show a glyph. For non‑AWS concepts (SaaS, personas,
value badges), use **emoji** — they render in colour on macOS/PowerPoint.

## 4. Render → compare → iterate

This loop is the whole game:

1. Build the `.drawio`.
2. `render.sh file.drawio` → PNG/SVG.
3. **View it.** Compare against the source (toggle the embedded reference layer for a
   true overlay).
4. Fix coordinates/labels; repeat 2–4×.

Well‑formedness matters: a single unescaped `&`, `<`, or `>` in a label makes draw.io
**silently stop parsing** and render only the part before it. The builders escape for
you and validate on `save()`; if you hand‑write XML, don't forget.

## 5. Declutter (optional but recommended)

To calm a dense diagram without losing content: soften/thin inner borders (automatic),
let `band` headers and `grp` tints carry the colour‑coding, add subtle container
shadows (`shadow_ids`) for depth, drop tiny repeated micro‑icons, and replace cramped
repeated boxes with a single caption (e.g. "Public/Private subnets · AZ 1‑3").

## 6. Export native PPTX (optional)

draw.io can't emit PPTX, and LibreOffice can't import SVG→Impress headless. Instead:

1. Crop the AWS icons you use once (`crop_icons.py` → `/tmp/icons`).
2. Run the **same** `layout(d)` through `PptxBuilder(icon_dir="/tmp/icons")`.

Every box/icon/label becomes an editable PowerPoint object — not a flat picture. (If
you only need a *picture* slide, embed a hi‑res PNG/SVG instead; but that's not
editable, which defeats the purpose.)

## Environment gotchas

- **macOS has no `timeout`.** Don't wrap the draw.io CLI in it — run it and poll for the
  output file. The Electron `task_policy_set` stderr warning is harmless.
- **draw.io desktop needs `sudo`/Finder to install** to `/Applications`. If you can't,
  ask the user to install it once, then use the CLI.
- **Headless Linux:** run the Electron CLI under `xvfb-run`.
- **Tiny PPTX fonts** are expected — the layout is in the image's pixel space scaled to a
  13.3″ slide, which is faithful to a dense diagram. Users zoom; or give the diagram a
  larger canvas / fewer columns for bigger text.
