import { z } from "zod";

export const loanInputSchema = z.object({
  equipmentId: z.string().trim().min(1, "Selecione um equipamento."),
  responsibleName: z
    .string()
    .trim()
    .min(3, "Informe o nome completo do responsável.")
    .max(100),
  dueDate: z.iso.date("Informe uma data válida."),
});

export type LoanInput = z.infer<typeof loanInputSchema>;
export type EquipmentStatus = "available" | "loaned" | "overdue";

export function localIsoDate(date = new Date()): string {
  const offset = date.getTimezoneOffset() * 60_000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 10);
}

export function classifyEquipmentStatus(
  dueDate: string | null,
  today = localIsoDate(),
): EquipmentStatus {
  if (!dueDate) return "available";
  return dueDate < today ? "overdue" : "loaned";
}

export function validateDueDate(dueDate: string, today = localIsoDate()) {
  if (dueDate < today) {
    throw new LoanRuleError(
      "A data prevista não pode estar no passado.",
      "PAST_DUE_DATE",
    );
  }
}

export class LoanRuleError extends Error {
  constructor(
    message: string,
    public readonly code:
      | "ALREADY_LOANED"
      | "PAST_DUE_DATE"
      | "NOT_FOUND"
      | "ALREADY_RETURNED",
  ) {
    super(message);
    this.name = "LoanRuleError";
  }
}
