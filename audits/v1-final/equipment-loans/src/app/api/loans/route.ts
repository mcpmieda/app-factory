import { NextResponse } from "next/server";

import { loanInputSchema, LoanRuleError } from "@/features/loans/domain";
import { createLoan } from "@/features/loans/repository";

export async function POST(request: Request) {
  const parsed = loanInputSchema.safeParse(await request.json());
  if (!parsed.success) {
    return NextResponse.json(
      { error: "Dados de empréstimo inválidos." },
      { status: 400 },
    );
  }

  try {
    const id = createLoan(parsed.data);
    return NextResponse.json({ id }, { status: 201 });
  } catch (error) {
    if (error instanceof LoanRuleError) {
      return NextResponse.json(
        { code: error.code, error: error.message },
        { status: error.code === "ALREADY_LOANED" ? 409 : 422 },
      );
    }
    return NextResponse.json({ error: "Falha interna." }, { status: 500 });
  }
}
