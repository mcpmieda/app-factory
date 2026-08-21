import { describe, expect, it } from "vitest";

import { studentSchema } from "@/features/students/schemas/student-schema";

const validStudent = {
  name: "Ana Souza",
  registration: "202600123",
  birthDate: "2007-05-20",
  email: "ana@example.com",
  phone: "(71) 99999-9999",
  course: "Ensino Médio",
  classroom: "3º A",
};

describe("studentSchema", () => {
  it("aceita um cadastro válido", () => {
    const result = studentSchema.safeParse(validStudent);
    expect(result.success).toBe(true);
  });

  it("rejeita e-mail inválido", () => {
    const result = studentSchema.safeParse({
      ...validStudent,
      email: "email-invalido",
    });

    expect(result.success).toBe(false);
  });

  it("rejeita data de nascimento no futuro", () => {
    const result = studentSchema.safeParse({
      ...validStudent,
      birthDate: "2999-01-01",
    });

    expect(result.success).toBe(false);
  });

  it("rejeita matrícula com caracteres fora do contrato", () => {
    const result = studentSchema.safeParse({
      ...validStudent,
      registration: "ABC 123",
    });

    expect(result.success).toBe(false);
  });
});
