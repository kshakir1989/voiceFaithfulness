import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Given, When, Then } = createBdd();

Given("the app is open", async ({ page }) => {
  await page.goto("/");
});

Then("I see the voiceFaithfulness brand", async ({ page }) => {
  await expect(page.getByTestId("vf-shell")).toBeVisible();
  await expect(page.getByRole("heading", { name: "voiceFaithfulness" })).toBeVisible();
});

Given("recordings and agents are loaded", async ({ page }) => {
  await expect(page.getByTestId("vf-recording-picker")).toBeVisible();
  await expect(page.getByTestId("vf-agent-stt")).toBeVisible();
  await expect(page.getByTestId("vf-agent-judge")).toBeVisible();
  await expect(page.getByTestId("vf-recording-picker").locator("option")).not.toHaveCount(0);
});

When("I run the faithfulness pipeline", async ({ page }) => {
  await page.getByTestId("vf-run").click();
  await expect(page.getByTestId("vf-run-score")).toBeVisible({ timeout: 60_000 });
});

Then("I see a completed score and overall percentage", async ({ page }) => {
  await expect(page.getByTestId("vf-run-score")).toContainText("Score:");
  await expect(page.getByTestId("vf-overall")).not.toContainText("No scores yet");
});
