import { test, expect } from "@playwright/test";

async function resetMockStore(page: import("@playwright/test").Page) {
  const r = await page.request.post("/api/dev/reset");
  expect(r.ok()).toBeTruthy();
}

test("US1: score a preloaded recording end-to-end", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  await expect(page.getByTestId("vf-recording-picker")).toBeVisible();
  await expect(page.getByTestId("vf-recording-picker").locator("option")).not.toHaveCount(0);
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-run-score")).toBeVisible({ timeout: 60_000 });
  await expect(page.getByTestId("vf-run-score")).toContainText("Score:");
  await expect(page.getByTestId("vf-overall")).not.toContainText("No scores yet");
});

test("US2: choose a non-default transcription agent", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  const stt = page.getByTestId("vf-agent-stt");
  await expect(stt.locator("option")).not.toHaveCount(0);
  const options = stt.locator("option:not([disabled])");
  const count = await options.count();
  expect(count).toBeGreaterThan(1);
  const defaultValue = await stt.inputValue();
  let altValue = defaultValue;
  for (let i = 0; i < count; i++) {
    const value = await options.nth(i).getAttribute("value");
    if (value && value !== defaultValue) {
      altValue = value;
      break;
    }
  }
  expect(altValue).not.toBe(defaultValue);
  await stt.selectOption(altValue);
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-run-stt")).toHaveText(altValue, { timeout: 60_000 });
  await expect(page.getByTestId("vf-score-row").filter({ hasText: `STT: ${altValue};` })).toBeVisible();
});

test("US3: choose a non-default judge agent", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  const judge = page.getByTestId("vf-agent-judge");
  await expect(judge.locator("option")).not.toHaveCount(0);
  const options = judge.locator("option:not([disabled])");
  const count = await options.count();
  expect(count).toBeGreaterThan(1);
  const defaultValue = await judge.inputValue();
  let altValue = defaultValue;
  for (let i = 0; i < count; i++) {
    const value = await options.nth(i).getAttribute("value");
    if (value && value !== defaultValue) {
      altValue = value;
      break;
    }
  }
  expect(altValue).not.toBe(defaultValue);
  await judge.selectOption(altValue);
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-run-judge")).toHaveText(altValue, { timeout: 60_000 });
  await expect(page.getByTestId("vf-score-row").filter({ hasText: `judge: ${altValue}` })).toBeVisible();
});

test("US4: preview audio before run", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  const audio = page.getByTestId("vf-audio-preview");
  await expect(audio).toBeVisible();
  const src = await audio.getAttribute("src");
  expect(src).toMatch(/\/api\/recordings\/.+\/audio/);
});

test("US4: show transcript and summary after run", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-transcript")).toBeVisible({ timeout: 60_000 });
  await expect(page.getByTestId("vf-transcript")).not.toHaveText("");
  await expect(page.getByTestId("vf-summary")).toBeVisible();
  await expect(page.getByTestId("vf-summary")).not.toHaveText("");
});

test("US4: upload local recording into picker", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  const before = await page.getByTestId("vf-recording-picker").locator("option").count();
  await page.getByTestId("vf-upload").setInputFiles("../data/preloaded/preload-02.wav");
  await expect
    .poll(async () => page.getByTestId("vf-recording-picker").locator("option").count())
    .toBeGreaterThan(before);
  await expect(page.getByTestId("vf-audio-preview")).toBeVisible();
});

test("US5: teaching shows ingest on load", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  await expect(page.getByTestId("vf-teach")).toHaveAttribute("data-concept", "ingest");
  await expect(page.getByTestId("vf-teach-log")).toContainText("ingest");
});

test("US5: successful run covers all five teaching concepts", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-run-score")).toBeVisible({ timeout: 60_000 });
  const log = page.getByTestId("vf-teach-log");
  for (const concept of ["ingest", "transcript", "summary", "judge", "aggregate"]) {
    await expect(log).toContainText(concept, { timeout: 10_000 });
  }
  await expect(page.getByTestId("vf-teach")).toHaveAttribute("data-concept", "aggregate");
});

test("US6: empty dashboard graph state", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  await expect(page.getByTestId("vf-overall")).toContainText("No scores yet");
  await expect(page.getByTestId("vf-graph-selector")).toBeVisible();
  await expect(page.getByTestId("vf-graph-empty")).toBeVisible();
});

test("US6: switch graph views after a score", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-run-score")).toBeVisible({ timeout: 60_000 });
  await expect(page.getByTestId("vf-graph-per-recording")).toBeVisible();
  await page.getByTestId("vf-graph-selector").selectOption("overall_aggregate");
  await expect(page.getByTestId("vf-graph-overall")).toBeVisible();
  await expect(page.getByTestId("vf-graph-overall")).toContainText("88");
});

test("honesty: stub mode banner and stubbed scores notice", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  await expect(page.getByTestId("vf-providers-mode")).toContainText("Stub mode");
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-run-score")).toBeVisible({ timeout: 60_000 });
  await expect(page.getByTestId("vf-stub-scores")).toBeVisible();
});

test("honesty: blocked demo recording fails clearly", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  await page.getByTestId("vf-recording-picker").selectOption("preload-blocked");
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-error")).toBeVisible({ timeout: 30_000 });
  await expect(page.getByTestId("vf-error")).toContainText(/blocked|all-ages|cannot be scored/i);
});

test("US7: rate limit shows banner and leaves overall unchanged", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  await expect(page.getByTestId("vf-overall")).toContainText("No scores yet");
  await page.route("**/api/runs", async (route) => {
    if (route.request().method() === "POST") {
      await route.fulfill({
        status: 429,
        contentType: "application/json",
        body: JSON.stringify({
          detail: { code: "rate_limited", message: "Free-tier rate limit reached." },
        }),
      });
      return;
    }
    await route.continue();
  });
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-error")).toBeVisible();
  await expect(page.getByTestId("vf-error")).toHaveAttribute("data-error-code", "rate_limited");
  await expect(page.getByTestId("vf-overall")).toContainText("No scores yet");
});

test("US7: run in progress shows 409 banner", async ({ page }) => {
  await resetMockStore(page);
  await page.goto("/");
  await page.route("**/api/runs", async (route) => {
    if (route.request().method() === "POST") {
      await route.fulfill({
        status: 409,
        contentType: "application/json",
        body: JSON.stringify({
          detail: { code: "run_in_progress", message: "Another pipeline run is active." },
        }),
      });
      return;
    }
    await route.continue();
  });
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-error")).toHaveAttribute("data-error-code", "run_in_progress");
  await expect(page.getByTestId("vf-error")).toContainText(/in progress|active/i);
});

test("shell shows brand", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "voiceFaithfulness" })).toBeVisible();
});
