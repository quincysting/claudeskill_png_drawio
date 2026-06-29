#!/usr/bin/env node
/**
 * png-to-drawio — Claude Code skill installer (zero dependencies).
 *
 *   npx github:quincysting/claudeskill_png_drawio        # install to ~/.claude/skills
 *   npx github:quincysting/claudeskill_png_drawio --force # overwrite without keeping a backup
 *   npx github:quincysting/claudeskill_png_drawio /custom/skills/dir
 *
 * Honors $CLAUDE_SKILLS_DIR. Copies only the skill itself (SKILL.md + assets/ +
 * references/) into <skills-dir>/png-to-drawio — not the repo docs/examples.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILL = 'png-to-drawio';
const PARTS = ['SKILL.md', 'assets', 'references'];
const SKIP = new Set(['__pycache__', '.DS_Store', '.git', 'node_modules']);
const pkgRoot = path.resolve(__dirname, '..');

const args = process.argv.slice(2);
const force = args.includes('--force') || args.includes('-f');
const posArg = args.find((a) => !a.startsWith('-'));
const skillsDir =
  posArg || process.env.CLAUDE_SKILLS_DIR || path.join(os.homedir(), '.claude', 'skills');
const dest = path.join(skillsDir, SKILL);

function copyRecursive(src, dst) {
  const st = fs.statSync(src);
  if (st.isDirectory()) {
    fs.mkdirSync(dst, { recursive: true });
    for (const entry of fs.readdirSync(src)) {
      if (SKIP.has(entry)) continue;
      copyRecursive(path.join(src, entry), path.join(dst, entry));
    }
  } else {
    fs.copyFileSync(src, dst);
  }
}

function main() {
  process.stdout.write('\n  ▸ png-to-drawio — Claude skill installer\n\n');

  for (const p of PARTS) {
    if (!fs.existsSync(path.join(pkgRoot, p))) {
      console.error(`  ✗ cannot find "${p}" in the package (corrupt download?) — aborting.`);
      process.exit(1);
    }
  }

  if (fs.existsSync(dest)) {
    if (!force) {
      const backup = `${dest}.bak-${Date.now()}`;
      fs.renameSync(dest, backup);
      console.log(`  • existing install moved to ${backup}`);
    } else {
      fs.rmSync(dest, { recursive: true, force: true });
      console.log('  • overwrote existing install (--force)');
    }
  }

  fs.mkdirSync(dest, { recursive: true });
  for (const p of PARTS) copyRecursive(path.join(pkgRoot, p), path.join(dest, p));

  console.log(`  ✓ installed skill "${SKILL}" → ${dest}`);
  console.log('\n  Next steps:');
  console.log('   1. Install the draw.io desktop CLI:  brew install --cask drawio');
  console.log('   2. Python deps:                      pip install pillow python-pptx');
  console.log('   3. Restart Claude Code, then ask:    "turn this png into draw.io"\n');
}

try {
  main();
} catch (err) {
  console.error('  ✗ install failed:', err && err.message ? err.message : err);
  process.exit(1);
}
