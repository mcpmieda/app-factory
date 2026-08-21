"use client";

import { AlertTriangle } from "lucide-react";

import { Button } from "@/components/ui/button";

export default function ErrorPage({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <main className="grid min-h-[70vh] place-items-center px-4">
      <div className="max-w-md space-y-4 text-center">
        <AlertTriangle className="mx-auto size-9 text-destructive" />
        <h1 className="text-xl font-semibold">
          Não foi possível carregar o inventário
        </h1>
        <p className="text-sm text-muted-foreground">
          Tente novamente. Nenhuma alteração foi aplicada aos dados.
        </p>
        <Button onClick={reset}>Tentar novamente</Button>
      </div>
    </main>
  );
}
