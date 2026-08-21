import { expect, test } from "@playwright/test"

const email = process.env.SEED_ADMIN_EMAIL ?? "admin@example.com"
const password = process.env.SEED_ADMIN_PASSWORD ?? "local-pilot-password"

async function signIn(page: import("@playwright/test").Page) {
  await page.goto("/login")
  await page.getByLabel("E-mail").fill(email)
  await page.getByLabel("Senha").fill(password)
  await page.getByRole("button", { name: "Entrar" }).click()
  await expect(page.getByRole("heading", { name: "Visão geral de recursos" })).toBeVisible()
}

test("protects the dashboard and rejects invalid credentials", async ({ page }) => {
  await page.goto("/admin")
  await expect(page).toHaveURL(/\/login$/)
  await page.getByLabel("E-mail").fill(email)
  await page.getByLabel("Senha").fill("incorrect-password")
  await page.getByRole("button", { name: "Entrar" }).click()
  await expect(page.getByText("E-mail ou senha inválidos.", { exact: true })).toBeVisible()
})

test("runs the authenticated resource lifecycle", async ({ page }, testInfo) => {
  const consoleErrors: string[] = []
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text())
  })
  await signIn(page)
  const name = `Recurso E2E ${testInfo.project.name} ${Date.now()}`
  const editedName = `${name} editado`

  await page.getByRole("link", { name: "Novo registro" }).click()
  await page.getByRole("button", { name: "Salvar registro" }).click()
  await expect(page.getByText("Revise os campos destacados.")).toBeVisible()
  await page.getByLabel("Nome").fill(name)
  await page.getByLabel("Categoria").fill("Testes")
  await page.getByLabel("Status").selectOption("allocated")
  await page.getByLabel("Localização").fill("Ambiente E2E")
  await page.getByLabel(/Observações/).fill("Criado pelo Playwright")
  await page.getByRole("button", { name: "Salvar registro" }).click()
  await expect(page.getByText("Registro criado com sucesso.")).toBeVisible()

  await page.getByLabel("Buscar registros").fill(name)
  await page.getByRole("button", { name: "Aplicar filtros" }).click()
  await expect(page.getByText(name, { exact: true })).toBeVisible()
  await page.getByRole("link", { name: `Editar ${name}` }).click()
  await page.getByLabel("Nome").fill(editedName)
  await page.getByRole("button", { name: "Salvar registro" }).click()
  await expect(page.getByText("Registro atualizado com sucesso.")).toBeVisible()

  await page.getByLabel("Buscar registros").fill(editedName)
  await page.getByRole("button", { name: "Aplicar filtros" }).click()
  await page.getByRole("button", { name: `Desativar ${editedName}` }).click()
  await expect(page.getByRole("heading", { name: "Desativar este registro?" })).toBeVisible()
  await page.getByRole("button", { name: "Desativar", exact: true }).click()
  await expect(page.getByText(editedName, { exact: true })).toHaveCount(0)

  await page.getByLabel("Filtrar por atividade").selectOption("inactive")
  await page.getByRole("button", { name: "Aplicar filtros" }).click()
  await expect(page.getByText(editedName, { exact: true })).toBeVisible()
  await page.reload()
  await expect(page.getByText(editedName, { exact: true })).toBeVisible()

  const signOut = page.getByRole("button", { name: "Sair" })
  if (!(await signOut.isVisible())) {
    await page.getByRole("button", { name: "Abrir menu" }).click()
  }
  await signOut.click()
  await expect(page).toHaveURL(/\/login$/)
  await expect(page.getByRole("heading", { name: "Acesse o painel" })).toBeVisible()
  expect(consoleErrors).toEqual([])
})
