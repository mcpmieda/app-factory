import { z } from "zod";

import {
  studentBackupSchema,
  studentRecordSchema,
  type StudentBackup,
  type StudentRecord,
} from "@/features/students/schemas/student-schema";

const STORAGE_KEY = "app-factory.student-registration.v2";
const LEGACY_STORAGE_KEY = "app-factory.student-registration.v1";
const recordsSchema = z.array(studentRecordSchema);

const legacyRecordSchema = z.object({
  id: z.string().min(1),
  createdAt: z.string().datetime(),
  name: z.string(),
  registration: z.string(),
  birthDate: z.string(),
  email: z.string(),
  phone: z.string(),
  course: z.string(),
  classroom: z.string(),
});

const legacyRecordsSchema = z.array(legacyRecordSchema);

export type StorageReadResult =
  | { ok: true; students: StudentRecord[]; migrated: boolean }
  | { ok: false; students: []; migrated: false; message: string };

export type BackupReadResult =
  | { ok: true; students: StudentRecord[]; exportedAt: string }
  | { ok: false; students: []; message: string };

export function normalizeRegistration(value: string) {
  return value.trim().toLocaleLowerCase("pt-BR");
}

function hasDuplicateRegistrations(students: StudentRecord[]) {
  const seen = new Set<string>();

  for (const student of students) {
    const normalized = normalizeRegistration(student.registration);
    if (seen.has(normalized)) return true;
    seen.add(normalized);
  }

  return false;
}

export function parseStoredStudents(value: unknown): StudentRecord[] | null {
  const parsed = recordsSchema.safeParse(value);

  if (!parsed.success || hasDuplicateRegistrations(parsed.data)) {
    return null;
  }

  return parsed.data;
}

export function migrateLegacyStudents(value: unknown): StudentRecord[] | null {
  const parsed = legacyRecordsSchema.safeParse(value);

  if (!parsed.success) return null;

  return parsed.data.map((student) => ({
    ...student,
    status: "active",
    shift: "not_informed",
    guardianName: "",
    guardianPhone: "",
    notes: "",
    updatedAt: student.createdAt,
  }));
}

export function readStudents(): StorageReadResult {
  try {
    const currentRaw = window.localStorage.getItem(STORAGE_KEY);

    if (currentRaw) {
      const current = parseStoredStudents(JSON.parse(currentRaw));

      if (!current) {
        return {
          ok: false,
          students: [],
          migrated: false,
          message: "Os dados locais estão em um formato inválido.",
        };
      }

      return { ok: true, students: current, migrated: false };
    }

    const legacyRaw = window.localStorage.getItem(LEGACY_STORAGE_KEY);

    if (!legacyRaw) {
      return { ok: true, students: [], migrated: false };
    }

    const migrated = migrateLegacyStudents(JSON.parse(legacyRaw));

    if (!migrated) {
      return {
        ok: false,
        students: [],
        migrated: false,
        message: "Os dados locais antigos não puderam ser migrados.",
      };
    }

    writeStudents(migrated);
    window.localStorage.removeItem(LEGACY_STORAGE_KEY);

    return { ok: true, students: migrated, migrated: true };
  } catch {
    return {
      ok: false,
      students: [],
      migrated: false,
      message: "Não foi possível ler os cadastros salvos neste navegador.",
    };
  }
}

export function writeStudents(students: StudentRecord[]) {
  const parsed = recordsSchema.parse(students);

  if (hasDuplicateRegistrations(parsed)) {
    throw new Error("A coleção contém matrículas duplicadas.");
  }

  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(parsed));
}

export function hasRegistration(
  students: StudentRecord[],
  registration: string,
  ignoreId?: string,
) {
  const normalized = normalizeRegistration(registration);

  return students.some(
    (student) =>
      student.id !== ignoreId &&
      normalizeRegistration(student.registration) === normalized,
  );
}

export function createStudentBackup(students: StudentRecord[]): StudentBackup {
  const parsedStudents = parseStoredStudents(students);

  if (!parsedStudents) {
    throw new Error("A coleção não pode ser exportada porque é inválida.");
  }

  return studentBackupSchema.parse({
    version: 2,
    exportedAt: new Date().toISOString(),
    students: parsedStudents,
  });
}

export function parseStudentBackup(raw: string): BackupReadResult {
  try {
    const value: unknown = JSON.parse(raw);
    const parsed = studentBackupSchema.safeParse(value);

    if (!parsed.success) {
      return {
        ok: false,
        students: [],
        message: "O arquivo não é um backup válido desta versão do cadastro.",
      };
    }

    if (hasDuplicateRegistrations(parsed.data.students)) {
      return {
        ok: false,
        students: [],
        message: "O backup contém matrículas duplicadas.",
      };
    }

    return {
      ok: true,
      students: parsed.data.students,
      exportedAt: parsed.data.exportedAt,
    };
  } catch {
    return {
      ok: false,
      students: [],
      message: "Não foi possível ler o arquivo de backup.",
    };
  }
}

function csvCell(value: string) {
  const normalized = value.replace(/\r?\n/g, " ");
  return `"${normalized.replace(/"/g, '""')}"`;
}

export function studentsToCsv(students: StudentRecord[]) {
  const header = [
    "Nome",
    "Matrícula",
    "Status",
    "Curso",
    "Turma",
    "Turno",
    "Nascimento",
    "E-mail",
    "Telefone",
    "Responsável",
    "Telefone do responsável",
    "Observações",
  ];

  const rows = students.map((student) =>
    [
      student.name,
      student.registration,
      student.status,
      student.course,
      student.classroom,
      student.shift,
      student.birthDate,
      student.email,
      student.phone,
      student.guardianName,
      student.guardianPhone,
      student.notes,
    ]
      .map(csvCell)
      .join(","),
  );

  return [header.map(csvCell).join(","), ...rows].join("\n");
}
