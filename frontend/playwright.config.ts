import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  timeout: 90_000,
  workers: 1,
  fullyParallel: false,
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
      command: "npm run dev -- --host 127.0.0.1 --port 5173",
      url: "http://127.0.0.1:5173",
      reuseExistingServer: !process.env.CI,
    },
  ],
});
