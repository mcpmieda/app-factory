import type {
  StudentFormValues,
  StudentShift,
  StudentStatus,
} from "@/features/students/schemas/student-schema";

export const INITIAL_FORM: StudentFormValues = {
  name: "",
  registration: "",
  birthDate: "",
  email: "",
  phone: "",
  course: "",
  classroom: "",
  shift: "not_informed",
  guardianName: "",
  guardianPhone: "",
  notes: "",
};

export const STATUS_LABELS: Record<StudentStatus, string> = {
  active: "Ativo",
  inactive: "Arquivado",
  transferred: "Transferido",
};

export const SHIFT_LABELS: Record<StudentShift, string> = {
  not_informed: "Não informado",
  morning: "Matutino",
  afternoon: "Vespertino",
  evening: "Noturno",
  full: "Integral",
};

export type FieldName = keyof StudentFormValues;
export type FieldErrors = Partial<Record<FieldName, string>>;

export type Feedback =
  | {
      status: "success" | "danger";
      title: string;
      description: string;
    }
  | null;

export function formatPhone(value: string) {
  const digits = value.replace(/\D/g, "").slice(0, 11);

  if (digits.length <= 2) return digits;
  if (digits.length <= 6) return digits.replace(/(\d{2})(\d+)/, "($1) $2");
  if (digits.length <= 10) {
    return digits.replace(/(\d{2})(\d{4})(\d{0,4})/, "($1) $2-$3");
  }

  return digits.replace(/(\d{2})(\d{5})(\d{0,4})/, "($1) $2-$3");
}

export function issueMap(issues: { path: PropertyKey[]; message: string }[]) {
  const errors: FieldErrors = {};

  for (const issue of issues) {
    const key = issue.path[0];

    if (
      typeof key === "string" &&
      key in INITIAL_FORM &&
      !errors[key as FieldName]
    ) {
      errors[key as FieldName] = issue.message;
    }
  }

  return errors;
}

export function downloadTextFile(
  fileName: string,
  contents: string,
  type: string,
) {
  const blob = new Blob([contents], { type });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");

  anchor.href = url;
  anchor.download = fileName;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

export function formatDate(value: string) {
  if (!value) return "Não informado";

  const [year, month, day] = value.slice(0, 10).split("-");
  if (!year || !month || !day) return value;

  return `${day}/${month}/${year}`;
}

export function formatDateTime(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(date);
}
