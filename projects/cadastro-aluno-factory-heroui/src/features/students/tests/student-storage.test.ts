import { describe, expect, it } from "vitest";

import {
  createStudentBackup,
  migrateLegacyStudents,
  parseStoredStudents,
  parseStudentBackup,
  studentsToCsv,
} from "@/features/students/data/student-storage";
import type { StudentRecord } from "@/features/students/schemas/student-schema";

const record: StudentRecord = {
  id: "student-1",
  name: "Ana Souza",
  registration: "202600123",
  birthDate: "2007-05-20",
  email: "ana@example.com",
  phone: "(71) 99999-9999",
  course: "Ensino Médio",
  classroom: "3º A",
  shift: "morning",
  guardianName: "Maria Souza",
  guardianPhone: "(71) 98888-7777",
  notes: 'Observação com "aspas".',
  status: "active",
  createdAt: "2026-08-20T10:00:00.000Z",
  updatedAt: "2026-08-21T10:00:00.000Z",
};

const duplicateRecord: StudentRecord = {
  ...record,
  id: "student-2",
  registration: " 202600123 ",
};

describe("student storage contracts", () => {
  it("migra registros da versão 1 sem inventar turno", () => {
    const migrated = migrateLegacyStudents([
      {
        id: "legacy-1",
        createdAt: "2026-08-20T10:00:00.000Z",
        name: "Aluno legado",
        registration: "LEGACY-1",
        birthDate: "2008-01-10",
        email: "legacy@example.com",
        phone: "",
        course: "Ensino Médio",
        classroom: "2º B",
      },
    ]);

    expect(migrated).toHaveLength(1);
    expect(migrated?.[0]).toMatchObject({
      status: "active",
      shift: "not_informed",
      guardianName: "",
      notes: "",
      updatedAt: "2026-08-20T10:00:00.000Z",
    });
  });

  it("rejeita coleção v2 com matrículas equivalentes duplicadas ao ler", () => {
    expect(parseStoredStudents([record, duplicateRecord])).toBeNull();
  });

  it("faz round-trip de backup versionado", () => {
    const backup = createStudentBackup([record]);
    const parsed = parseStudentBackup(JSON.stringify(backup));

    expect(parsed.ok).toBe(true);
    if (parsed.ok) {
      expect(parsed.students).toEqual([record]);
    }
  });

  it("não cria backup de uma coleção com matrículas duplicadas", () => {
    expect(() => createStudentBackup([record, duplicateRecord])).toThrow(
      "A coleção não pode ser exportada porque é inválida.",
    );
  });

  it("rejeita backup recebido com matrículas equivalentes duplicadas", () => {
    const parsed = parseStudentBackup(
      JSON.stringify({
        version: 2,
        exportedAt: "2026-08-22T12:00:00.000Z",
        students: [record, duplicateRecord],
      }),
    );

    expect(parsed.ok).toBe(false);
  });

  it("rejeita arquivo de backup incompatível", () => {
    const parsed = parseStudentBackup(
      JSON.stringify({ version: 99, students: [] }),
    );

    expect(parsed.ok).toBe(false);
  });

  it("exporta CSV escapando aspas", () => {
    const csv = studentsToCsv([record]);

    expect(csv).toContain('"Ana Souza"');
    expect(csv).toContain('"Observação com ""aspas""."');
  });
});
