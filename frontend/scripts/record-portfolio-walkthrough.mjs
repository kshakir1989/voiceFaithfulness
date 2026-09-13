/**
 * Record a short voiceFaithfulness UI walkthrough for the personal website.
 * Spawns isolated mock API (:18000) + Vite (:15173), records, encodes MP4.
 *
 *   cd apps/voiceFaithfulness/frontend && node ../scripts/record-portfolio-walkthrough.mjs
 */
import { chromium } from "playwright";
import { mkdirSync, readdirSync, existsSync, rmSync } from "node:fs";
import { join } from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __dirname = fileURLToPath(new URL(".", import.meta.url));
const APP_ROOT = join(__dirname, "..");
const FRONTEND = join(APP_ROOT, "frontend");
const OUT_DIR = join(APP_ROOT, ".walkthrough-capture");
const VIDEO_DEST = join(
  APP_ROOT,
  "..",
  "personalWebsite",
  "public",
  "videos",
  "voice-faithfulness.mp4",
);
const API_PORT = 18000;
const WEB_PORT = 15173;
const BASE = `http://127.0.0.1:${WEB_PORT}`;

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function waitHttp(url, attempts = 60) {
  for (let i = 0; i < attempts; i++) {
    try {
      const r = await fetch(url);
      if (r.ok || r.status === 200) return;
    } catch {
      /* retry */
    }
    await sleep(500);
  }
  throw new Error(`Timeout waiting for ${url}`);
}

function start(cmd, args, opts) {
  const child = spawn(cmd, args, {
    ...opts,
    stdio: ["ignore", "pipe", "pipe"],
  });
  child.stdout.on("data", () => {});
  child.stderr.on("data", () => {});
  return child;
}

async function main() {
  rmSync(OUT_DIR, { recursive: true, force: true });
  mkdirSync(OUT_DIR, { recursive: true });

  const api = start(
    join(APP_ROOT, "backend", ".venv", "bin", "uvicorn"),
    ["app.main:app", "--app-dir", "backend", "--port", String(API_PORT)],
    {
      cwd: APP_ROOT,
      env: { ...process.env, FORCE_MOCK_PROVIDERS: "1" },
    },
  );
  const web = start(
    "npm",
    ["run", "dev", "--", "--host", "127.0.0.1", "--port", String(WEB_PORT)],
    {
      cwd: FRONTEND,
      env: { ...process.env, VF_API_PROXY: `http://127.0.0.1:${API_PORT}` },
    },
  );

  try {
    await waitHttp(`http://127.0.0.1:${API_PORT}/api/health`);
    await waitHttp(BASE);

    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      viewport: { width: 1280, height: 720 },
      recordVideo: { dir: OUT_DIR, size: { width: 1280, height: 720 } },
    });
    const page = await context.newPage();

    await page.goto(BASE, { waitUntil: "networkidle" });
    await page.request.post(`${BASE}/api/dev/reset`);
    await page.reload({ waitUntil: "networkidle" });
    await sleep(1200);

    await page.getByTestId("vf-view-desktop").click();
    await sleep(900);

    await page.getByTestId("vf-stage-source").click();
    await sleep(1100);

    await page.getByTestId("vf-run").click();
    await page.getByTestId("vf-run-score").waitFor({ state: "visible", timeout: 60_000 });
    await sleep(1600);

    await page.getByTestId("vf-stage-transcript").click();
    await sleep(1400);
    await page.getByTestId("vf-stage-summary").click();
    await sleep(1100);
    await page.getByTestId("vf-rationale-toggle").click();
    await sleep(1300);

    await page.getByTestId("vf-stage-judge").click();
    await sleep(1200);
    await page.getByTestId("vf-judge-why").scrollIntoViewIfNeeded();
    await sleep(1800);
    await page.getByTestId("vf-judge-improve").scrollIntoViewIfNeeded();
    await sleep(1600);

    await page.getByTestId("vf-overall").click();
    await sleep(1300);

    await page.getByTestId("vf-graph-selector").selectOption("overall_aggregate");
    await sleep(1100);
    await page.getByTestId("vf-graph-selector").selectOption("agent_compare");
    await sleep(1100);
    await page.getByTestId("vf-graph-selector").selectOption("session_sparkline");
    await sleep(1300);

    await page.getByTestId("vf-history").scrollIntoViewIfNeeded();
    await sleep(1600);

    await context.close();
    await browser.close();

    const webms = readdirSync(OUT_DIR).filter((f) => f.endsWith(".webm"));
    if (!webms.length) throw new Error("No webm recorded");
    const webmPath = join(OUT_DIR, webms[0]);

    const ff = spawnSync(
      "ffmpeg",
      [
        "-y",
        "-i",
        webmPath,
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-an",
        VIDEO_DEST,
      ],
      { encoding: "utf8" },
    );
    if (ff.status !== 0) {
      console.error(ff.stderr);
      throw new Error("ffmpeg failed");
    }
    if (!existsSync(VIDEO_DEST)) throw new Error("mp4 missing");
    console.log("Wrote", VIDEO_DEST);
  } finally {
    api.kill("SIGTERM");
    web.kill("SIGTERM");
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
