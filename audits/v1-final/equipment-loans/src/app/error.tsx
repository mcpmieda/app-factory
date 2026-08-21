"use client";

import { AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function ErrorPage({ reset }: { reset: () => void }) {
  return (
    <main className="grid min-h-screen place-items-center px-5">
      <section
        className="max-w-md space-y-4 rounded-2xl border bg-card p-8 text-center shadow-lg"
        role="alert"
      >
        <AlertTriangle
          aria-hidden="true"
          className="mx-auto size-8 text-destructive"
        />
        <h1 className="text-xl font-semibold">
          Não foi possível carregar os empréstimos
        </h1>
        <p className="text-sm text-muted-foreground">
          Tente novamente. Seus registros permanecem salvos.
        </p>
        <Button onClick={reset}>Tentar novamente</Button>
      </section>
    </main>
  );
}
