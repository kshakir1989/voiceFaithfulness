import { defineConfig, devices } from "@playwright/test";
import type { CoverageReportOptions } from "monocart-coverage-reports";

const coverageOptions: CoverageReportOptions = {
  outputDir: "coverage",
  reports: [
    ["v8", { inline: true }],
    "console-summary",
    "lcov",
  ],
  entryFilter: (entry) => {
    const url = String(entry.url ?? "");
    if (!url || url.startsWith("node:")) return false;
    if (url.includes("node_modules")) return false;
    if (url.includes("@vite") || url.includes("@react-refresh") || url.includes("/@fs/")) return false;
    return true;
  },
  sourcePath: (filePath) => {
    const p = String(filePath).replace(/\\/g, "/");
    const idx = p.indexOf("/src/");
    if (idx >= 0) return p.slice(idx + 1);
    if (p.startsWith("src/")) return p;
    return p;
  },
  sourceFilter: (sourcePath) => {
    const p = String(sourcePath).replace(/\\/g, "/");
    if (p.includes("node_modules")) return false;
    // App sources only — exclude vendor packages that also use a src/ folder (recharts/d3).
    return (
      /^src\/(App\.tsx|main\.tsx|theme\.ts|index\.css|vite-env\.d\.ts)$/.test(p) ||
      /^src\/components\//.test(p)
    );
  },
};

export default defineConfig({
  testDir: "./e2e",
  timeout: 90_000,
  workers: 1,
  fullyParallel: false,
  reporter: [
    ["list"],
    [
      "monocart-reporter",
      {
        name: "voiceFaithfulness e2e coverage",
        outputFile: "coverage/monocart-report.html",
        coverage: coverageOptions,
      },
    ],
  ],
  use: {
    ...devices["Desktop Chrome"],
    baseURL: "http://127.0.0.1:5173",
    headless: true,
  },
  webServer: [
    {
      command: "backend/.venv/bin/uvicorn app.main:app --app-dir backend --port 8000",
      cwd: "..",
      url: "http://127.0.0.1:8000/api/health",
      reuseExistingServer: !process.env.CI,
      env: {
        FORCE_MOCK_PROVIDERS: "1",
      },
    },
    {
      command: "npm run build && npm run preview -- --host 127.0.0.1 --port 5173",
      url: "http://127.0.0.1:5173",
      reuseExistingServer: !process.env.CI,
    },
  ],
});
