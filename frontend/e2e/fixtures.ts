import { test as base, expect } from "@playwright/test";
import { addCoverageReport } from "monocart-reporter";

const coverageOn = process.env.COVERAGE === "1";

type CoverageFixtures = {
  autoCoverage: void;
};

export const test = base.extend<CoverageFixtures>({
  autoCoverage: [
    async ({ page }, use) => {
      if (coverageOn) {
        await page.coverage.startJSCoverage({ resetOnNavigation: false });
      }
      await use();
      if (coverageOn) {
        const jsCoverage = await page.coverage.stopJSCoverage();
        await addCoverageReport(jsCoverage, test.info());
      }
    },
    { scope: "test", auto: true },
  ],
});

export { expect };
