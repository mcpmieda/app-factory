"use server";

import { revalidatePath } from "next/cache";

import type { ActionState } from "./action-state";
import { loanInputSchema, LoanRuleError } from "./domain";
import { createLoan, returnLoan } from "./repository";

export async function createLoanAction(
  _previous: ActionState,
  formData: FormData,
): Promise<ActionState> {
  const parsed = loanInputSchema.safeParse({
    equipmentId: formData.get("equipmentId"),
    responsibleName: formData.get("responsibleName"),
    dueDate: formData.get("dueDate"),
  });

  if (!parsed.success) {
    return {
      status: "error",
      message: "Revise os campos destacados.",
      fieldErrors: parsed.error.flatten().fieldErrors,
    };
  }

  try {
    createLoan(parsed.data);
    revalidatePath("/");
    return { status: "success", message: "Empréstimo registrado." };
  } catch (error) {
    return {
      status: "error",
      message:
        error instanceof LoanRuleError
          ? error.message
          : "Não foi possível registrar o empréstimo.",
    };
  }
}

export async function returnLoanAction(
  _previous: ActionState,
  formData: FormData,
): Promise<ActionState> {
  const loanId = formData.get("loanId");
  if (typeof loanId !== "string" || !loanId) {
    return { status: "error", message: "Empréstimo inválido." };
  }

  try {
    returnLoan(loanId);
    revalidatePath("/");
    return { status: "success", message: "Devolução registrada." };
  } catch (error) {
    return {
      status: "error",
      message:
        error instanceof LoanRuleError
          ? error.message
          : "Não foi possível registrar a devolução.",
    };
  }
}
