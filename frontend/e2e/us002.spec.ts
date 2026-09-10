import { test, expect } from "@playwright/test";

async function resetMockStore(page: import("@playwright/test").Page) {
  const r = await page.request.post("/api/dev/reset");
  expect(r.ok()).toBeTruthy();
}

test("002: stub banner, five STT, rationale, history, layout, reset", async ({ page }) => {
  await resetMockStore(page);
  page.on("dialog", (d) => d.accept());
  await page.goto("/");

  await expect(page.getByTestId("vf-providers-mode")).toContainText(/Stub mode/i);
  await expect(page.getByTestId("vf-agent-stt").locator("option")).toHaveCount(5);
  await expect(page.getByTestId("vf-agent-judge").locator("option").filter({ hasText: "stronger" })).not.toHaveCount(0);

  await page.getByTestId("vf-view-mobile").click();
  await expect(page.getByTestId("vf-shell")).toHaveAttribute("data-view-mode", "mobile");
  await page.getByTestId("vf-view-desktop").click();
  await expect(page.getByTestId("vf-shell")).toHaveAttribute("data-view-mode", "desktop");

  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-transcript")).toBeVisible({ timeout: 60_000 });
  await expect(page.getByTestId("vf-summary")).toBeVisible();
  await page.getByTestId("vf-rationale-toggle").click();
  await expect(page.getByTestId("vf-rationale-text")).toBeVisible();
  await expect.poll(async () => page.getByTestId("vf-history-row").count()).toBeGreaterThanOrEqual(1);

  const before = await page.getByTestId("vf-history-row").count();
  const stt = page.getByTestId("vf-agent-stt");
  const options = stt.locator("option:not([disabled])");
  const defaultValue = await stt.inputValue();
  let alt = defaultValue;
  const count = await options.count();
  for (let i = 0; i < count; i++) {
    const value = await options.nth(i).getAttribute("value");
    if (value && value !== defaultValue) {
      alt = value;
      break;
    }
  }
  await stt.selectOption(alt);
  await page.getByTestId("vf-run").click();
  await expect
    .poll(async () => page.getByTestId("vf-history-row").count(), { timeout: 60_000 })
    .toBeGreaterThanOrEqual(before + 1);

  await page.getByTestId("vf-demo-reset").click();
  await expect(page.getByTestId("vf-history-empty")).toBeVisible();
  await expect(page.getByTestId("vf-overall")).toContainText("No scores yet");
  await expect(page.getByTestId("vf-recording-picker").locator("option")).not.toHaveCount(0);
});
