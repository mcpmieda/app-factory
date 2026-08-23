import type {
  StudentRecord,
  StudentStatus,
} from "@/features/students/schemas/student-schema";

export type StudentSort = "recent" | "name" | "classroom";
export type StudentStatusFilter = "all" | StudentStatus;

export type StudentFilters = {
  query: string;
  status: StudentStatusFilter;
  classroom: string;
  sort: StudentSort;
};

export function filterAndSortStudents(
  students: StudentRecord[],
  filters: StudentFilters,
) {
  const query = filters.query.trim().toLocaleLowerCase("pt-BR");

  const filtered = students.filter((student) => {
    if (filters.status !== "all" && student.status !== filters.status) {
      return false;
    }

    if (filters.classroom !== "all" && student.classroom !== filters.classroom) {
      return false;
    }

    if (!query) return true;

    return [
      student.name,
      student.registration,
      student.email,
      student.phone,
      student.course,
      student.classroom,
      student.guardianName,
      student.guardianPhone,
    ].some((value) => value.toLocaleLowerCase("pt-BR").includes(query));
  });

  return [...filtered].sort((left, right) => {
    if (filters.sort === "name") {
      return left.name.localeCompare(right.name, "pt-BR");
    }

    if (filters.sort === "classroom") {
      const byClassroom = left.classroom.localeCompare(
        right.classroom,
        "pt-BR",
        { numeric: true },
      );

      if (byClassroom !== 0) return byClassroom;
      return left.name.localeCompare(right.name, "pt-BR");
    }

    return Date.parse(right.updatedAt) - Date.parse(left.updatedAt);
  });
}

export function summarizeStudents(students: StudentRecord[]) {
  const classrooms = new Set(
    students
      .filter((student) => student.status === "active")
      .map((student) => student.classroom.trim())
      .filter(Boolean),
  );

  return {
    total: students.length,
    active: students.filter((student) => student.status === "active").length,
    inactive: students.filter((student) => student.status === "inactive").length,
    transferred: students.filter((student) => student.status === "transferred")
      .length,
    classrooms: classrooms.size,
  };
}

export function uniqueClassrooms(students: StudentRecord[]) {
  return [...new Set(students.map((student) => student.classroom.trim()))]
    .filter(Boolean)
    .sort((left, right) =>
      left.localeCompare(right, "pt-BR", { numeric: true }),
    );
}
