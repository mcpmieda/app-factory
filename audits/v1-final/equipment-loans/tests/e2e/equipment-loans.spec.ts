import { expect, test } from "@playwright/test";

function tomorrow() {
  const date = new Date();
  date.setDate(date.getDate() + 1);
  return date.toISOString().slice(0, 10);
}

test.beforeEach(async ({ request }) => {
  const response = await request.post("/api/test/reset");
  expect(response.ok()).toBe(true);
});

test("loan persists through reload and can be returned", async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Empréstimos de equipamentos" }),
  ).toBeVisible();

  await page
    .getByLabel("Equipamento", { exact: true })
    .selectOption("eq-camera-01");
  await page.getByLabel("Responsável").fill("Ana Souza");
  await page.getByLabel("Devolução prevista").fill(tomorrow());
  await page.getByRole("button", { name: "Registrar empréstimo" }).click();
  await expect(page.getByRole("status")).toContainText("Empréstimo registrado");

  const camera = page
    .getByRole("listitem")
    .filter({ hasText: "Câmera fotográfica" });
  await expect(camera).toContainText("Ana Souza");
  await page.reload();
  await expect(camera).toContainText("Ana Souza");
  await camera.getByRole("button", { name: "Registrar devolução" }).click();
  await expect(camera).toContainText("Disponível");
  await page.reload();
  await expect(camera).toContainText("Disponível");

  const overflow = await page.evaluate(
    () =>
      document.documentElement.scrollWidth >
      document.documentElement.clientWidth,
  );
  expect(overflow).toBe(false);
  expect(consoleErrors).toEqual([]);
});

test("blocks an impossible second active loan", async ({ request }) => {
  const payload = {
    equipmentId: "eq-camera-01",
    responsibleName: "Carlos Lima",
    dueDate: tomorrow(),
  };
  expect((await request.post("/api/loans", { data: payload })).status()).toBe(
    201,
  );
  const duplicate = await request.post("/api/loans", { data: payload });
  expect(duplicate.status()).toBe(409);
  await expect(duplicate.json()).resolves.toMatchObject({
    code: "ALREADY_LOANED",
  });
});

test("shows only overdue loans and supports keyboard focus", async ({
  page,
}) => {
  await page.goto("/");
  const overdueFilter = page.getByRole("link", { name: "Atrasados" });
  await overdueFilter.click();
  await expect(page).toHaveURL(/status=overdue/);
  await expect(overdueFilter).toHaveAttribute("aria-current", "page");

  const equipmentList = page.getByTestId("equipment-list");
  const rows = equipmentList.getByRole("listitem");
  await expect(rows).toHaveCount(1);
  await expect(rows.first()).toContainText("Projetor multimídia");
  await expect(rows.first()).toContainText("Marina Lopes");
  await expect(rows.first()).toHaveAttribute("data-status", "overdue");
  await expect(equipmentList.getByText("Notebook laboratório")).toHaveCount(0);
  await expect(equipmentList.getByText("Câmera fotográfica")).toHaveCount(0);

  await page.reload();
  await expect(overdueFilter).toHaveAttribute("aria-current", "page");
  await expect(rows).toHaveCount(1);
  await expect(rows.first()).toHaveAttribute("data-status", "overdue");

  await page.keyboard.press("Home");
  await page.keyboard.press("Tab");
  await expect(page.locator(":focus")).toBeVisible();
});

test("honors reduced motion preference", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  const animation = await page
    .locator(".ambient-surface")
    .evaluate((element) => getComputedStyle(element, "::before").animationName);
  expect(animation).toBe("none");
});
