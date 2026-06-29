# Installation

## 1. Prerequisites

### draw.io desktop (required for rendering + icon cropping)
The skill drives the draw.io desktop **CLI** to export PNG/SVG and to crop AWS icon stencils.

- **macOS:** `brew install --cask drawio`
  - CLI lands at `/Applications/draw.io.app/Contents/MacOS/draw.io`
  - ⚠️ The cask installs to `/Applications`, which needs `sudo`/Finder permission — if you're running headless and the install fails, install the app manually once.
- **Windows / Linux:** download from [drawio-desktop releases](https://github.com/jgraph/drawio-desktop/releases).
  - On headless Linux, run the CLI under `xvfb-run` (it's an Electron app).

Override the binary location with the `DRAWIO` environment variable:

```bash
export DRAWIO="/path/to/draw.io"     # used by render.sh, crop_icons.py, verify_icons.py
```

### Python
```bash
pip install pillow          # required (tiles, icon cropping)
pip install python-pptx     # required only for the PPTX backend
```
Python 3.9+ recommended.

## 2. Install as a Claude Code skill

### Option A — `npx` (recommended, no clone)

```bash
npx github:quincysting/claudeskill_png_drawio
```

A zero‑dependency Node installer (`bin/install.js`) copies the skill
(`SKILL.md` + `assets/` + `references/`) into `~/.claude/skills/png-to-drawio`.

- **Custom skills dir:** pass a path or set the env var —
  `npx github:quincysting/claudeskill_png_drawio /my/skills` or `CLAUDE_SKILLS_DIR=/my/skills npx github:…`
- **Re‑install:** an existing copy is moved to `png-to-drawio.bak-<timestamp>`; use `--force` to overwrite without a backup.
- Requires Node ≥ 14 (no npm publish needed — `npx github:` runs straight from the repo).

### Option B — clone & copy

```bash
git clone https://github.com/quincysting/claudeskill_png_drawio.git
mkdir -p ~/.claude/skills
cp -R claudeskill_png_drawio ~/.claude/skills/png-to-drawio
```

Or symlink the clone instead of copying:
`ln -s "$(pwd)/claudeskill_png_drawio" ~/.claude/skills/png-to-drawio`

Claude Code discovers skills in `~/.claude/skills/<name>/SKILL.md`. **Restart Claude Code** (or open a new session); the skill auto‑activates on relevant requests ("turn this png into draw.io", "make this diagram editable", "export to pptx with real shapes").

## 3. Verify the install

```bash
cd ~/.claude/skills/png-to-drawio/assets
python3 example.py            # writes /tmp/example.drawio and /tmp/example.pptx
bash render.sh /tmp/example.drawio 1.6   # writes /tmp/example.png + .svg
```

If `example.png` shows the demo diagram, you're good. If the PPTX step is skipped, install `python-pptx`. If rendering fails, check `$DRAWIO` points at a real draw.io binary.

## 4. (Optional) make AWS icons appear in PPTX

The PPTX backend places AWS icons as small images. Crop the ones you need once:

```bash
python3 crop_icons.py /tmp/icons          # crops every verified icon
# or a subset:
python3 crop_icons.py /tmp/icons s3 eks glue athena lambda
```

Then pass `icon_dir="/tmp/icons"` to `PptxBuilder`. Without cropped icons, the PPTX falls back to coloured tiles (still valid, just no glyphs).
