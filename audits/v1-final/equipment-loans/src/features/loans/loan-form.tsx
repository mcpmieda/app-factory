"use client";

import { useActionState, useEffect, useRef } from "react";
import { useFormStatus } from "react-dom";
import { CalendarClock, Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { initialActionState } from "./action-state";
import { createLoanAction } from "./actions";

type AvailableItem = { id: string; name: string; assetTag: string };

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <Button className="w-full sm:w-auto" disabled={pending} type="submit">
      {pending ? (
        <>
          <span
            aria-hidden="true"
            className="size-3 animate-spin rounded-full border-2 border-current border-r-transparent motion-reduce:animate-none"
          />
          Registrando…
        </>
      ) : (
        <>
          <Plus aria-hidden="true" /> Registrar empréstimo
        </>
      )}
    </Button>
  );
}

export function LoanForm({
  availableItems,
  today,
}: {
  availableItems: AvailableItem[];
  today: string;
}) {
  const [state, action] = useActionState(createLoanAction, initialActionState);
  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    if (state.status === "success") formRef.current?.reset();
  }, [state]);

  return (
    <form action={action} className="grid gap-4" ref={formRef}>
      <div className="grid gap-2">
        <Label htmlFor="equipmentId">Equipamento</Label>
        <select
          aria-describedby="equipment-help"
          className="h-9 w-full rounded-lg border bg-background px-3 text-sm outline-none focus-visible:ring-3 focus-visible:ring-ring/50 disabled:opacity-60"
          disabled={availableItems.length === 0}
          id="equipmentId"
          name="equipmentId"
          required
        >
          <option value="">Selecione um item disponível</option>
          {availableItems.map((item) => (
            <option key={item.id} value={item.id}>
              {item.assetTag} — {item.name}
            </option>
          ))}
        </select>
        <p className="text-xs text-muted-foreground" id="equipment-help">
          Itens já emprestados não podem ser selecionados.
        </p>
        {state.fieldErrors?.equipmentId?.map((error) => (
          <p className="text-xs text-destructive" key={error}>
            {error}
          </p>
        ))}
      </div>

      <div className="grid gap-2 sm:grid-cols-2">
        <div className="grid gap-2">
          <Label htmlFor="responsibleName">Responsável</Label>
          <Input
            id="responsibleName"
            name="responsibleName"
            placeholder="Nome completo"
            required
          />
          {state.fieldErrors?.responsibleName?.map((error) => (
            <p className="text-xs text-destructive" key={error}>
              {error}
            </p>
          ))}
        </div>
        <div className="grid gap-2">
          <Label htmlFor="dueDate">Devolução prevista</Label>
          <div className="relative">
            <CalendarClock
              aria-hidden="true"
              className="pointer-events-none absolute left-3 top-2.5 size-4 text-muted-foreground"
            />
            <Input
              className="pl-9"
              id="dueDate"
              min={today}
              name="dueDate"
              required
              type="date"
            />
          </div>
          {state.fieldErrors?.dueDate?.map((error) => (
            <p className="text-xs text-destructive" key={error}>
              {error}
            </p>
          ))}
        </div>
      </div>

      <div className="flex flex-col-reverse items-start gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div aria-live="polite" className="min-h-5 text-sm">
          {state.status !== "idle" && (
            <p
              className={
                state.status === "error"
                  ? "text-destructive"
                  : "text-emerald-700"
              }
              role={state.status === "error" ? "alert" : "status"}
            >
              {state.message}
            </p>
          )}
        </div>
        <SubmitButton />
      </div>
    </form>
  );
}
