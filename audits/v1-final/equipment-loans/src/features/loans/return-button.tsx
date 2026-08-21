"use client";

import { useActionState } from "react";
import { useFormStatus } from "react-dom";
import { Check } from "lucide-react";

import { Button } from "@/components/ui/button";
import { initialActionState } from "./action-state";
import { returnLoanAction } from "./actions";

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <Button disabled={pending} size="sm" type="submit" variant="outline">
      <Check aria-hidden="true" />{" "}
      {pending ? "Salvando…" : "Registrar devolução"}
    </Button>
  );
}

export function ReturnButton({ loanId }: { loanId: string }) {
  const [state, action] = useActionState(returnLoanAction, initialActionState);
  return (
    <form action={action} className="flex flex-col items-start gap-1">
      <input name="loanId" type="hidden" value={loanId} />
      <SubmitButton />
      <span
        aria-live="polite"
        className={
          state.status === "error"
            ? "text-xs text-destructive"
            : "text-xs text-emerald-700"
        }
      >
        {state.message}
      </span>
    </form>
  );
}
