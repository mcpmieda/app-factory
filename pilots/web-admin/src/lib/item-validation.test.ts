import { describe, expect, it } from "vitest"
import { itemInputSchema, parseItemForm } from "./item-validation"

const validItem = {
  name: "Notebook da equipe",
  category: "Equipamentos",
  status: "available",
  location: "Sala 3",
  notes: "Uso compartilhado",
}

describe("itemInputSchema", () => {
  it("normalizes valid fields", () => {
    const result = itemInputSchema.parse({ ...validItem, name: "  Notebook da equipe  " })
    expect(result.name).toBe("Notebook da equipe")
  })

  it("converts blank optional notes to null", () => {
    expect(itemInputSchema.parse({ ...validItem, notes: "  " }).notes).toBeNull()
  })

  it.each([
    ["name", "x"],
    ["category", ""],
    ["location", ""],
    ["status", "lost"],
    ["notes", "x".repeat(501)],
  ])("rejects an invalid %s", (field, value) => {
    expect(itemInputSchema.safeParse({ ...validItem, [field]: value }).success).toBe(false)
  })
})

describe("parseItemForm", () => {
  it("maps browser form data into a validated item", () => {
    const form = new FormData()
    for (const [key, value] of Object.entries(validItem)) form.set(key, value)
    expect(parseItemForm(form)).toMatchObject({ success: true, data: validItem })
  })

  it("returns field errors instead of throwing", () => {
    const result = parseItemForm(new FormData())
    expect(result.success).toBe(false)
    if (!result.success) expect(result.error.flatten().fieldErrors.name).toBeDefined()
  })
})
