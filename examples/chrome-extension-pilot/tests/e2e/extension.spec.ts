import { expect, test, chromium } from "@playwright/test";
import path from "node:path";
test("loads the real MV3 extension and toggles its action without console errors", async () => {
  const extensionPath = path.resolve("dist");
  const context = await chromium.launchPersistentContext("", {
    channel: "chromium",
    headless: true,
    args: [
      `--disable-extensions-except=${extensionPath}`,
      `--load-extension=${extensionPath}`,
    ],
  });
  try {
    const page = await context.newPage();
    const errors: string[] = [];
    page.on(
      "console",
      (message) => message.type() === "error" && errors.push(message.text()),
    );
    page.on("pageerror", (error) => errors.push(error.message));
    await page.goto("http://127.0.0.1:4174/");
    const control = page.locator("#focus-lens-pilot button");
    await expect(control).toBeVisible();
    await expect(control).toHaveAccessibleName("Destacar 2 itens");
    await control.click();
    await expect(control).toHaveAttribute("aria-pressed", "true");
    await expect(page.locator(".focus-lens-active")).toHaveCount(2);
    await control.click();
    await expect(page.locator(".focus-lens-active")).toHaveCount(0);
    expect(errors).toEqual([]);
  } finally {
    await context.close();
  }
});
