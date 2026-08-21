import { describe, expect, it } from "vitest";

import { parseAssetForm } from "./asset-schema";

function validForm() {
  const form = new FormData();
  form.set("code", " pat-042 ");
  form.set("description", "Notebook de laboratório");
  form.set("category", "technology");
  form.set("location", "Laboratório 2");
  form.set("custodian", "Equipe pedagógica");
  form.set("status", "available");
  form.set("notes", "Uso fictício");
  return form;
}

describe("parseAssetForm", () => {
  it("normalizes a valid school asset", () => {
    const result = parseAssetForm(validForm());
    expect(result.success).toBe(true);
    if (result.success) expect(result.data.code).toBe("PAT-042");
  });

  it("converts optional blank text to undefined", () => {
    const form = validForm();
    form.set("custodian", "  ");
    form.set("notes", "");
    const result = parseAssetForm(form);
    expect(result.success).toBe(true);
    if (result.success)
      expect(result.data).toMatchObject({
        custodian: undefined,
        notes: undefined,
      });
  });

  it.each([
    ["code", "x"],
    ["code", "PAT @ 1"],
    ["description", ""],
    ["category", "unknown"],
    ["location", ""],
    ["status", "unknown"],
  ])("rejects invalid %s", (field, value) => {
    const form = validForm();
    form.set(field, value);
    expect(parseAssetForm(form).success).toBe(false);
  });
});
