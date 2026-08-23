import { describe, expect, it } from "vitest";

import {
  filterAndSortStudents,
  summarizeStudents,
  uniqueClassrooms,
} from "@/features/students/domain/student-operations";
import type { StudentRecord } from "@/features/students/schemas/student-schema";

function student(
  id: string,
  name: string,
  classroom: string,
  status: StudentRecord["status"],
  updatedAt: string,
): StudentRecord {
  return {
    id,
    name,
    registration: `MAT-${id}`,
    birthDate: "2007-05-20",
    email: `${id}@example.com`,
    phone: "",
    course: "Ensino Médio",
    classroom,
    shift: "not_informed",
    guardianName: "",
    guardianPhone: "",
    notes: "",
    status,
    createdAt: updatedAt,
    updatedAt,
  };
}

const students = [
  student("1", "Bruno Lima", "3º B", "active", "2026-08-21T10:00:00.000Z"),
  student("2", "Ana Souza", "3º A", "inactive", "2026-08-22T10:00:00.000Z"),
  student("3", "Carla Alves", "3º A", "active", "2026-08-20T10:00:00.000Z"),
];

describe("student operations", () => {
  it("resume totais e turmas ativas", () => {
    expect(summarizeStudents(students)).toEqual({
      total: 3,
      active: 2,
      inactive: 1,
      transferred: 0,
      classrooms: 2,
    });
  });

  it("filtra por busca, status e turma", () => {
    const result = filterAndSortStudents(students, {
      query: "carla",
      status: "active",
      classroom: "3º A",
      sort: "name",
    });

    expect(result.map((item) => item.name)).toEqual(["Carla Alves"]);
  });

  it("ordena por atualização recente", () => {
    const result = filterAndSortStudents(students, {
      query: "",
      status: "all",
      classroom: "all",
      sort: "recent",
    });

    expect(result.map((item) => item.name)).toEqual([
      "Ana Souza",
      "Bruno Lima",
      "Carla Alves",
    ]);
  });

  it("lista turmas sem duplicar", () => {
    expect(uniqueClassrooms(students)).toEqual(["3º A", "3º B"]);
  });
});
