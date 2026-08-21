import { expect, test } from "@playwright/test";

test.beforeEach(async ({ page }, info) => {
  if (info.project.name === "reduced-motion") {
    await page.emulateMedia({ reducedMotion: "reduce" });
  }
});
test("complete institutional journey has no overflow", async ({
  page,
}, info) => {
  const errors: string[] = [];
  page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toContainText(
    "Curiosidade",
  );
  await expect(
    page.getByRole("heading", {
      name: "Formação inteira, não ensino em partes.",
    }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Espaços que convidam a experimentar." }),
  ).toBeVisible();
  if (info.project.name === "desktop") {
    await page.screenshot({
      path: "../../research/evidence/v0.9-website-desktop.png",
      fullPage: true,
    });
  }
  await page.getByRole("link", { name: "Conheça nosso projeto" }).click();
  await expect(page).toHaveURL(/\/projeto\/?$/);
  await expect(
    page.getByRole("heading", {
      name: "Aprender é criar relações com o mundo.",
    }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () =>
        document.documentElement.scrollWidth >
        document.documentElement.clientWidth,
    ),
  ).toBe(false);
  expect(errors).toEqual([]);
});
test("keyboard focus and CTA work", async ({ page }) => {
  await page.goto("/");
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("link", { name: "Pular para o conteúdo" }),
  ).toBeFocused();
  await expect(
    page.getByRole("link", { name: "Agendar uma visita" }),
  ).toHaveAttribute("href", /^mailto:/);
});
test("reduced motion disables ambient loop", async ({ page }, info) => {
  test.skip(info.project.name !== "reduced-motion", "reduced-motion only");
  await page.goto("/");
  await expect(page.locator(".orb-one")).toHaveCSS("animation-name", "none");
});
