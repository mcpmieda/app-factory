import { expect, test, type Page } from "@playwright/test";

async function fillStudent(
  page: Page,
  registration = "202600123",
  name = "Ana Souza",
) {
  const form = page.locator("#student-form");

  await form.getByLabel("Nome completo").fill(name);
  await form.getByLabel("Matrícula").fill(registration);
  await form.getByLabel("Data de nascimento").fill("2007-05-20");
  await form.getByLabel("E-mail").fill("ana@example.com");
  await form.getByLabel("Telefone", { exact: true }).fill("71999999999");
  await form.getByLabel("Curso / etapa").fill("Ensino Médio");
  await form.getByLabel("Turma", { exact: true }).fill("3º A");
  await form.getByLabel("Turno", { exact: true }).selectOption("morning");
  await form.getByLabel("Responsável", { exact: true }).fill("Maria Souza");
  await form.getByLabel("Telefone do responsável").fill("71988887777");
  await form.getByLabel("Observações").fill("Cadastro de teste.");
}

function studentRow(page: Page, name: string) {
  return page.locator("article.student-row").filter({ hasText: name });
}

test.beforeEach(async ({ page }) => {
  await page.goto("/");
  await page.evaluate(() => window.localStorage.clear());
  await page.reload();
});

test("cadastra aluno e mantém após recarregar", async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  await fillStudent(page);
  await page.getByRole("button", { name: "Cadastrar aluno" }).click();

  await expect(page.getByText("Aluno cadastrado")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Ana Souza" })).toBeVisible();
  await expect(page.getByText("1 resultado")).toBeVisible();

  await page.reload();

  await expect(page.getByRole("heading", { name: "Ana Souza" })).toBeVisible();
  expect(consoleErrors).toEqual([]);
});

test("impede matrícula duplicada", async ({ page }) => {
  await fillStudent(page);
  await page.getByRole("button", { name: "Cadastrar aluno" }).click();
  await expect(page.getByText("Aluno cadastrado")).toBeVisible();

  await fillStudent(page, "202600123", "Outra Ana");
  await page.getByRole("button", { name: "Cadastrar aluno" }).click();

  await expect(page.getByText("Matrícula já cadastrada")).toBeVisible();
});

test("edita, pesquisa, abre detalhes e arquiva aluno", async ({ page }) => {
  await fillStudent(page);
  await page.getByRole("button", { name: "Cadastrar aluno" }).click();

  const row = studentRow(page, "Ana Souza");
  await row.getByRole("button", { name: "Editar" }).click();

  const form = page.locator("#student-form");
  await form.getByLabel("Nome completo").fill("Ana Silva");
  await form.getByLabel("Status do aluno").selectOption("active");
  await page.getByRole("button", { name: "Salvar alterações" }).click();

  await expect(page.getByText("Cadastro atualizado")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Ana Silva" })).toBeVisible();

  await page.getByLabel("Pesquisar alunos").fill("MAT-NAO-EXISTE");
  await expect(page.getByText("Nenhum cadastro encontrado")).toBeVisible();

  await page.getByLabel("Pesquisar alunos").fill("Ana Silva");
  const editedRow = studentRow(page, "Ana Silva");
  await editedRow.getByRole("button", { name: "Detalhes" }).click();
  await expect(editedRow.getByText("20/05/2007")).toBeVisible();
  await expect(editedRow.getByText("Maria Souza")).toBeVisible();

  await editedRow.getByRole("button", { name: "Arquivar" }).click();
  await expect(page.getByText("Aluno arquivado")).toBeVisible();
  await expect(editedRow.getByText("Arquivado", { exact: true })).toBeVisible();

  await page.getByLabel("Filtrar por status").selectOption("active");
  await expect(page.getByText("Nenhum cadastro encontrado")).toBeVisible();

  await page.getByLabel("Filtrar por status").selectOption("inactive");
  await expect(page.getByRole("heading", { name: "Ana Silva" })).toBeVisible();
});

test("migra automaticamente cadastros da versão anterior", async ({ page }) => {
  await page.evaluate(() => {
    window.localStorage.setItem(
      "app-factory.student-registration.v1",
      JSON.stringify([
        {
          id: "legacy-1",
          createdAt: "2026-08-20T10:00:00.000Z",
          name: "Aluno Legado",
          registration: "LEGACY-1",
          birthDate: "2008-01-10",
          email: "legacy@example.com",
          phone: "",
          course: "Ensino Médio",
          classroom: "2º B",
        },
      ]),
    );
  });

  await page.reload();

  await expect(page.getByText("Cadastros atualizados")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Aluno Legado" })).toBeVisible();

  const migrated = await page.evaluate(() =>
    window.localStorage.getItem("app-factory.student-registration.v2"),
  );

  expect(migrated).toContain('"shift":"not_informed"');
  expect(migrated).toContain('"status":"active"');
});

test("restaura backup versionado substituindo os dados atuais", async ({
  page,
}) => {
  await fillStudent(page);
  await page.getByRole("button", { name: "Cadastrar aluno" }).click();

  const now = "2026-08-22T12:00:00.000Z";
  const backup = {
    version: 2,
    exportedAt: now,
    students: [
      {
        id: "restored-1",
        name: "Bruno Restaurado",
        registration: "REST-001",
        birthDate: "2006-04-12",
        email: "bruno@example.com",
        phone: "",
        course: "Ensino Médio",
        classroom: "2º C",
        shift: "afternoon",
        guardianName: "",
        guardianPhone: "",
        notes: "Registro restaurado por backup.",
        status: "active",
        createdAt: now,
        updatedAt: now,
      },
    ],
  };

  page.once("dialog", (dialog) => dialog.accept());

  await page.getByLabel("Selecionar arquivo de backup").setInputFiles({
    name: "backup.json",
    mimeType: "application/json",
    buffer: Buffer.from(JSON.stringify(backup)),
  });

  await expect(page.getByText("Backup restaurado")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Bruno Restaurado" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Ana Souza" })).not.toBeVisible();
});
