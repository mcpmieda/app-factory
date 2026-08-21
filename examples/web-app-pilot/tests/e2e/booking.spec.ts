import { expect, test } from "@playwright/test";
test.beforeEach(async ({ page }, info) => {
  if (info.project.name === "reduced-motion")
    await page.emulateMedia({ reducedMotion: "reduce" });
});
test("user completes booking end to end", async ({ page }, info) => {
  const errors: string[] = [];
  page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
  await page.goto("/");
  await page
    .getByRole("button", { name: /Ver horários/ })
    .first()
    .click();
  await page.getByRole("button", { name: "Continuar" }).click();
  await page.getByLabel("Nome").fill("Ana Lima");
  await page.getByLabel("E-mail").fill("ana@example.test");
  await page.getByRole("button", { name: "Confirmar reserva" }).click();
  await expect(
    page.getByRole("heading", { name: "Confirmando sua reserva…" }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Seu encontro já tem lugar." }),
  ).toBeVisible();
  if (info.project.name === "desktop") {
    await page.screenshot({
      path: "../../research/evidence/v0.9-web-app-success.png",
      fullPage: true,
    });
  }
  await expect(page.getByText("Sala Aurora")).toBeVisible();
  expect(
    await page.evaluate(
      () =>
        document.documentElement.scrollWidth >
        document.documentElement.clientWidth,
    ),
  ).toBe(false);
  expect(errors).toEqual([]);
});
test("empty state is recoverable", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel("Buscar espaço").fill("nenhum");
  await expect(
    page.getByRole("heading", { name: "Nenhum espaço encontrado" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Limpar busca" }).click();
  await expect(
    page.getByRole("heading", { name: "Sala Aurora" }),
  ).toBeVisible();
});
test("reduced motion removes ambient loop", async ({ page }, info) => {
  test.skip(info.project.name !== "reduced-motion", "reduced only");
  await page.goto("/");
  await expect(page.locator(".app-shell")).toHaveCSS("overflow", "hidden");
  expect(
    await page
      .locator(".app-shell")
      .evaluate((el) => getComputedStyle(el, "::before").animationName),
  ).toBe("none");
});
