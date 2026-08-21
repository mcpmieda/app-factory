"use client";

import { Boxes, LogOut, ShieldCheck } from "lucide-react";
import { useRouter } from "next/navigation";
import { useTransition } from "react";

import { Button } from "@/components/ui/button";
import { authClient } from "@/lib/auth-client";

export function AdminShell({
  children,
  userName,
}: {
  children: React.ReactNode;
  userName: string;
}) {
  const router = useRouter();
  const [pending, startTransition] = useTransition();

  function signOut() {
    startTransition(async () => {
      await authClient.signOut();
      router.replace("/login");
      router.refresh();
    });
  }

  return (
    <div className="min-h-screen bg-muted/35">
      <header className="border-b bg-background/95 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6">
          <div className="flex min-w-0 items-center gap-3">
            <span className="grid size-9 shrink-0 place-items-center rounded-xl bg-primary text-primary-foreground">
              <Boxes aria-hidden="true" className="size-5" />
            </span>
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold">
                Patrimônio Escolar
              </p>
              <p className="hidden items-center gap-1 text-xs text-muted-foreground sm:flex">
                <ShieldCheck aria-hidden="true" className="size-3" /> Área
                administrativa protegida
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="hidden max-w-44 truncate text-sm text-muted-foreground md:block">
              {userName}
            </span>
            <Button
              aria-label="Sair"
              disabled={pending}
              onClick={signOut}
              size="sm"
              variant="outline"
            >
              <LogOut aria-hidden="true" />
              <span className="hidden sm:inline">
                {pending ? "Saindo…" : "Sair"}
              </span>
            </Button>
          </div>
        </div>
      </header>
      {children}
    </div>
  );
}
