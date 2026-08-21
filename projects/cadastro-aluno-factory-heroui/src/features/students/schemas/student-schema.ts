import { z } from "zod";

function isRealCalendarDate(value: string) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);

  if (!match) return false;

  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const date = new Date(Date.UTC(year, month - 1, day));

  return (
    date.getUTCFullYear() === year &&
    date.getUTCMonth() === month - 1 &&
    date.getUTCDate() === day
  );
}

function isNotFutureDate(value: string) {
  const today = new Date().toISOString().slice(0, 10);
  return value <= today;
}

export const studentSchema = z.object({
  name: z
    .string()
    .trim()
    .min(3, "Informe o nome completo.")
    .max(120, "O nome deve ter no máximo 120 caracteres."),
  registration: z
    .string()
    .trim()
    .min(3, "Informe a matrícula.")
    .max(30, "A matrícula deve ter no máximo 30 caracteres.")
    .regex(/^[A-Za-z0-9._/-]+$/, "Use apenas letras, números, ponto, hífen, barra ou sublinhado."),
  birthDate: z
    .string()
    .min(1, "Informe a data de nascimento.")
    .refine(isRealCalendarDate, "Informe uma data válida.")
    .refine(isNotFutureDate, "A data de nascimento não pode estar no futuro."),
  email: z
    .string()
    .trim()
    .email("Informe um e-mail válido.")
    .max(160, "O e-mail deve ter no máximo 160 caracteres."),
  phone: z
    .string()
    .trim()
    .max(20, "O telefone está muito longo.")
    .refine((value) => {
      if (!value) return true;
      const digits = value.replace(/\D/g, "");
      return digits.length === 10 || digits.length === 11;
    }, "Informe um telefone com DDD."),
  course: z
    .string()
    .trim()
    .min(2, "Informe o curso.")
    .max(80, "O curso deve ter no máximo 80 caracteres."),
  classroom: z
    .string()
    .trim()
    .min(1, "Informe a turma.")
    .max(40, "A turma deve ter no máximo 40 caracteres."),
});

export const studentRecordSchema = studentSchema.extend({
  id: z.string().min(1),
  createdAt: z.string().datetime(),
});

export type StudentFormValues = z.infer<typeof studentSchema>;
export type StudentRecord = z.infer<typeof studentRecordSchema>;
