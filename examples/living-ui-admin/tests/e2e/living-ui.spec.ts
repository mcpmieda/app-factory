import { expect, test, type Page } from "@playwright/test";

function observeConsoleErrors(page: Page) {
  const errors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(message.text());
  });
  return errors;
}

test("keeps the generated admin usable on desktop and mobile", async ({
  page,
}) => {
  const errors = observeConsoleErrors(page);

  await page.goto("/");

  await expect(
    page.getByRole("heading", {
      name: "Decisões claras, no ritmo da operação.",
    }),
  ).toBeVisible();
  await expect(page.getByTestId("ambient-hero")).toBeVisible();
  await expect(page.getByTestId("ambient-empty")).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Revisar pendência" }),
  ).toBeEnabled();

  const hasHorizontalOverflow = await page.evaluate(
    () =>
      document.documentElement.scrollWidth >
      document.documentElement.clientWidth,
  );
  expect(hasHorizontalOverflow).toBe(false);
  expect(errors).toEqual([]);
});

test("animates data only when the value really changes", async ({ page }) => {
  const errors = observeConsoleErrors(page);
  await page.goto("/");

  const meter = page.getByTestId("capacity-meter");
  await expect(meter).toHaveAttribute("data-motion-revision", "0");
  await expect(page.getByTestId("capacity-value")).toHaveText("68%");

  await page.getByRole("button", { name: "Reconsultar" }).click();
  await expect(
    page.getByText("Reconsulta concluída: nenhum valor mudou"),
  ).toBeVisible();
  await expect(meter).toHaveAttribute("data-motion-revision", "0");

  await page.getByRole("button", { name: "Simular mudança real" }).click();
  await expect(page.getByTestId("capacity-value")).toHaveText("82%");
  await expect(meter).toHaveAttribute("data-motion-revision", "1");

  await page.getByRole("button", { name: "Simular mudança real" }).click();
  await expect(
    page.getByText("Capacidade já está no valor mais recente"),
  ).toBeVisible();
  await expect(meter).toHaveAttribute("data-motion-revision", "1");
  expect(errors).toEqual([]);
});

test("communicates processing and success without motion-only information", async ({
  page,
}) => {
  const errors = observeConsoleErrors(page);
  await page.goto("/");

  await page.getByRole("button", { name: "Processar fila" }).click();
  const state = page.getByTestId("processing-state");
  await expect(state).toHaveAttribute("data-processing-state", "processing");
  await expect(
    page.getByRole("button", { name: "Processando…" }),
  ).toBeDisabled();
  await expect(state).toContainText("Validando 18 itens");

  await expect(state).toHaveAttribute("data-processing-state", "success");
  await expect(state).toContainText("18 itens validados com sucesso");
  await expect(
    page.getByRole("button", { name: "Fila processada" }),
  ).toBeEnabled();
  expect(errors).toEqual([]);
});

test("stops attention after focus and preserves focus through the drawer", async ({
  page,
}) => {
  const errors = observeConsoleErrors(page);
  await page.goto("/");

  const attention = page.getByTestId("attention-pulse");
  const trigger = page.getByRole("button", { name: "Revisar pendência" });
  await expect(attention).toHaveAttribute("data-attention-active", "true");

  await trigger.focus();
  await expect(trigger).toBeFocused();
  await expect(attention).toHaveAttribute("data-attention-active", "false");
  expect(
    await attention.evaluate(
      (element) => getComputedStyle(element, "::before").animationName,
    ),
  ).toBe("none");

  await trigger.press("Enter");
  const drawer = page.getByTestId("review-drawer");
  await expect(drawer).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Revisão de prioridade" }),
  ).toBeVisible();

  await page.keyboard.press("Escape");
  await expect(drawer).toBeHidden();
  await expect(trigger).toBeFocused();
  expect(errors).toEqual([]);
});

test("keeps semantic motion active in the standard profile", async ({
  page,
}, testInfo) => {
  test.skip(testInfo.project.name !== "chromium-desktop");
  const errors = observeConsoleErrors(page);
  await page.goto("/");

  const heroAnimation = await page
    .getByTestId("ambient-hero")
    .evaluate((element) => getComputedStyle(element, "::before").animationName);
  const attentionAnimation = await page
    .getByTestId("attention-pulse")
    .evaluate((element) => getComputedStyle(element, "::before").animationName);

  expect(heroAnimation).toBe("ambient-drift");
  expect(attentionAnimation).toBe("attention-halo");
  expect(errors).toEqual([]);
});

test("removes non-essential movement when reduced motion is requested", async ({
  page,
}, testInfo) => {
  test.skip(testInfo.project.name !== "chromium-reduced-motion");
  const errors = observeConsoleErrors(page);
  await page.goto("/");

  for (const testId of ["ambient-hero", "ambient-empty", "attention-pulse"]) {
    const animationName = await page
      .getByTestId(testId)
      .evaluate(
        (element) => getComputedStyle(element, "::before").animationName,
      );
    expect(animationName).toBe("none");
  }

  await page.getByRole("button", { name: "Simular mudança real" }).click();
  await expect(page.getByTestId("capacity-value")).toHaveText("82%");
  const reducedTransitionDuration = await page
    .getByTestId("capacity-meter")
    .locator(".metric-fill")
    .evaluate((element) =>
      Number.parseFloat(getComputedStyle(element).transitionDuration),
    );
  expect(reducedTransitionDuration).toBeLessThanOrEqual(0.001);

  await page.getByRole("button", { name: "Processar fila" }).click();
  await expect(page.getByTestId("state-spinner")).toHaveCSS(
    "animation-name",
    "none",
  );
  await expect(page.getByTestId("processing-state")).toHaveAttribute(
    "data-processing-state",
    "success",
  );

  await page.getByRole("button", { name: "Revisar pendência" }).click();
  await expect(page.getByTestId("review-drawer")).toHaveCSS(
    "animation-name",
    "none",
  );
  expect(errors).toEqual([]);
});
