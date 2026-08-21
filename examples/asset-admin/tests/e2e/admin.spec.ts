import { expect, test } from "@playwright/test";

function collectConsoleErrors(page: import("@playwright/test").Page) {
  const errors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") errors.push(message.text());
  });
  return errors;
}

function visibleText(page: import("@playwright/test").Page, text: string) {
  return page.getByText(text, { exact: true }).filter({ visible: true });
}

async function login(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("E-mail").fill("admin@example.com");
  await page.getByLabel("Senha").fill("local-admin-password");
  await page.getByRole("button", { name: "Entrar" }).click();
  await expect(
    page.getByRole("heading", { name: "Patrimônio escolar" }),
  ).toBeVisible();
}

test("protects the dashboard and rejects invalid credentials", async ({
  page,
}) => {
  const consoleErrors = collectConsoleErrors(page);
  await page.goto("/admin");
  await expect(page).toHaveURL(/\/login/);
  await page.getByLabel("E-mail").fill("admin@example.com");
  await page.getByLabel("Senha").fill("senha-incorreta");
  await page.getByRole("button", { name: "Entrar" }).click();
  await expect(
    page.getByText("E-mail ou senha inválidos.", { exact: true }),
  ).toBeVisible();
  expect(consoleErrors).toEqual([
    "Failed to load resource: the server responded with a status of 401 (UNAUTHORIZED)",
  ]);
});

test("runs the critical asset lifecycle with persistence", async ({ page }) => {
  const consoleErrors = collectConsoleErrors(page);
  const suffix = `${test.info().project.name.replace(/\W/g, "").slice(-6)}-${Date.now()}`;
  const code = `E2E-${suffix}`.toUpperCase();

  await login(page);
  await page.getByRole("link", { name: "Novo patrimônio" }).click();
  await page.getByLabel("Código patrimonial").fill(code);
  await page.getByLabel("Descrição").fill("Tablet fictício para validação");
  await page.getByLabel("Categoria").selectOption("technology");
  await page.getByLabel("Localização / setor").fill("Biblioteca fictícia");
  await page.getByLabel("Responsável (opcional)").fill("Equipe de exemplo");
  await page.getByLabel("Situação").selectOption("available");
  await page.getByRole("button", { name: "Salvar patrimônio" }).click();
  await expect(page.getByText("O patrimônio foi cadastrado.")).toBeVisible();

  await page.getByLabel("Buscar patrimônio").fill(code);
  await page.getByRole("button", { name: "Filtrar" }).click();
  await expect(visibleText(page, code)).toBeVisible();
  await page.getByRole("link", { name: `Editar ${code}` }).click();
  await page.getByLabel("Localização / setor").fill("Sala de leitura fictícia");
  await page.getByLabel("Situação").selectOption("maintenance");
  await page.getByRole("button", { name: "Salvar patrimônio" }).click();
  await expect(page.getByText("O patrimônio foi atualizado.")).toBeVisible();

  await page.getByLabel("Buscar patrimônio").fill(code);
  await page.getByRole("button", { name: "Filtrar" }).click();
  await expect(visibleText(page, "Sala de leitura fictícia")).toBeVisible();
  await expect(visibleText(page, "Manutenção")).toBeVisible();

  await page.getByRole("button", { name: `Arquivar ${code}` }).click();
  await expect(page.getByRole("alertdialog")).toContainText(
    "poderá ser reativado",
  );
  await page.getByRole("button", { name: "Confirmar arquivamento" }).click();
  await expect(page.getByText(code, { exact: true })).toHaveCount(0);

  await page.getByLabel("Buscar patrimônio").fill(code);
  await page.getByLabel("Mostrar somente arquivados").check();
  await page.getByRole("button", { name: "Filtrar" }).click();
  await expect(visibleText(page, code)).toBeVisible();
  await page.getByRole("button", { name: `Reativar ${code}` }).click();
  await expect(page.getByText(code, { exact: true })).toHaveCount(0);

  await page.getByLabel("Mostrar somente arquivados").uncheck();
  await page.getByRole("button", { name: "Filtrar" }).click();
  await expect(visibleText(page, code)).toBeVisible();
  await page.reload();
  await expect(visibleText(page, code)).toBeVisible();

  await page.getByRole("button", { name: "Sair" }).click();
  await expect(
    page.getByRole("heading", { name: "Acesse o painel" }),
  ).toBeVisible();
  expect(consoleErrors).toEqual([]);
});
