/**
 * Render spec-architecture.html → spec-architecture.png
 * Run from the app directory:
 *   node render-spec-architecture.mjs
 * Uses @playwright/test from apps/value if not installed in this app.
 */
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const dir = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(dir, "spec-architecture.html");
const pngPath = path.join(dir, "spec-architecture.png");
const valueRoot = path.resolve(dir, "../value");

async function loadChromium() {
  try {
    const { chromium } = await import("@playwright/test");
    return chromium;
  } catch {
    const require = createRequire(path.join(valueRoot, "package.json"));
    return require("@playwright/test").chromium;
  }
}

const chromium = await loadChromium();
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 2800, height: 2400 } });
await page.goto(pathToFileURL(htmlPath).href);
await page.waitForSelector(".mermaid svg", { timeout: 60_000 });
await page.locator("body").screenshot({ path: pngPath, type: "png" });
await browser.close();
console.log(`Wrote ${pngPath}`);
