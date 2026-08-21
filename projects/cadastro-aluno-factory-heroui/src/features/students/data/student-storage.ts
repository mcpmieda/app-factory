import {
  studentRecordSchema,
  type StudentRecord,
} from "@/features/students/schemas/student-schema";
import { z } from "zod";

const STORAGE_KEY = "app-factory.student-registration.v1";
const recordsSchema = z.array(studentRecordSchema);

export type StorageReadResult =
  | { ok: true; students: StudentRecord[] }
  | { ok: false; students: []; message: string };

export function readStudents(): StorageReadResult {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);

    if (!raw) {
      return { ok: true, students: [] };
    }

    const parsedJson: unknown = JSON.parse(raw);
    const parsed = recordsSchema.safeParse(parsedJson);

    if (!parsed.success) {
      return {
        ok: false,
        students: [],
        message: "Os dados locais estão em um formato inválido.",
      };
    }

    return { ok: true, students: parsed.data };
  } catch {
    return {
      ok: false,
      students: [],
      message: "Não foi possível ler os cadastros salvos neste navegador.",
    };
  }
}

export function writeStudents(students: StudentRecord[]) {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(students));
}

export function hasRegistration(
  students: StudentRecord[],
  registration: string,
) {
  const normalized = registration.trim().toLocaleLowerCase("pt-BR");

  return students.some(
    (student) =>
      student.registration.trim().toLocaleLowerCase("pt-BR") === normalized,
  );
}
