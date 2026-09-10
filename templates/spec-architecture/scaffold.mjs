#!/usr/bin/env node
/**
 * Scaffold Spec Kit architecture diagram files into an app directory.
 *
 * Usage (from monorepo root):
 *   node templates/spec-architecture/scaffold.mjs apps/<name>
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const templateDir = path.dirname(fileURLToPath(import.meta.url));
const targetArg = process.argv[2];

if (!targetArg) {
  console.error("Usage: node templates/spec-architecture/scaffold.mjs apps/<name>");
  process.exit(1);
}

const repoRoot = path.resolve(templateDir, "../..");
const appDir = path.resolve(repoRoot, targetArg);
const appName = path.basename(appDir);

if (!fs.existsSync(appDir)) {
  fs.mkdirSync(appDir, { recursive: true });
}

const files = [
  "spec-architecture.mmd",
  "spec-architecture.html",
  "render-spec-architecture.mjs",
];

for (const name of files) {
  const src = path.join(templateDir, name);
  let text = fs.readFileSync(src, "utf8");
  if (name.endsWith(".html") || name.endsWith(".mmd")) {
    text = text.replaceAll("APP_NAME", appName);
  }
  // From apps/<name>, apps/value is ../value — template already uses that.
  const dest = path.join(appDir, name);
  fs.writeFileSync(dest, text);
  console.log(`Wrote ${dest}`);
}

console.log(`
Next:
  cd ${path.relative(repoRoot, appDir) || "."}
  node render-spec-architecture.mjs

Update spec-architecture.mmd / .html whenever Spec Kit artifacts change, then re-render.
`);
