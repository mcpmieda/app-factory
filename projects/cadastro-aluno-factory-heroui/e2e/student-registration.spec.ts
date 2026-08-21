import { expect, test, type Page } from "@playwright/test";

async function fillStudent(page: Page, registration = "202600123") {
  await page.getByLabel("Nome completo").fill("Ana Souza");
  await page.getByLabel("Matrícula").fill(registration);
  await page.getByLabel("Data de nascimento").fill("2007-05-20");
  await page.getByLabel("E-mail").fill("ana@example.com");
  await page.getByLabel("Telefone").fill("71999999999");
  await page.getByLabel("Curso").fill("Ensino Médio");
  await page.getByLabel("Turma").fill("3º A");
}

test.beforeEach(async ({ page }) => {
  await page.goto("/");
  await page.evaluate(() => window.localStorage.clear());
  await page.reload();
});

test("cadastra aluno em uma única etapa e mantém após recarregar", async ({
  page,
}) => {
  const consoleErrors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  await fillStudent(page);
  await page.getByRole("button", { name: "Cadastrar aluno" }).click();

  await expect(page.getByText("Aluno cadastrado")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Ana Souza" })).toBeVisible();

  await page.reload();

  await expect(page.getByRole("heading", { name: "Ana Souza" })).toBeVisible();
  expect(consoleErrors).toEqual([]);
});

test("impede matrícula duplicada", async ({ page }) => {
  await fillStudent(page);
  await page.getByRole("button", { name: "Cadastrar aluno" }).click();
  await expect(page.getByText("Aluno cadastrado")).toBeVisible();

  await fillStudent(page);
  await page.getByRole("button", { name: "Cadastrar aluno" }).click();

  await expect(page.getByText("Matrícula já cadastrada")).toBeVisible();
});
