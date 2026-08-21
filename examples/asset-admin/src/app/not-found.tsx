import Link from "next/link";

import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <main className="grid min-h-screen place-items-center px-4 text-center">
      <div className="space-y-4">
        <p className="text-sm font-medium text-primary">404</p>
        <h1 className="text-2xl font-semibold">Registro não encontrado</h1>
        <Button asChild>
          <Link href="/admin">Voltar ao inventário</Link>
        </Button>
      </div>
    </main>
  );
}
