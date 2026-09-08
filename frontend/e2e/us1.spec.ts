import { test, expect } from "@playwright/test";

test("US1: score a preloaded recording end-to-end", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByTestId("vf-recording-picker")).toBeVisible();
  await expect(page.getByTestId("vf-recording-picker").locator("option")).not.toHaveCount(0);
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-run-score")).toBeVisible({ timeout: 60_000 });
  await expect(page.getByTestId("vf-run-score")).toContainText("Score:");
  await expect(page.getByTestId("vf-overall")).not.toContainText("No scores yet");
});

test("shell shows brand", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "voiceFaithfulness" })).toBeVisible();
});
