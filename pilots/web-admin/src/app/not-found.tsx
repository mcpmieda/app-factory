import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function NotFound() {
  return (
    <main className="grid min-h-screen place-items-center p-4 text-center">
      <div>
        <p className="text-muted-foreground text-sm">404</p>
        <h1 className="mt-2 text-3xl font-semibold">Registro não encontrado</h1>
        <p className="text-muted-foreground mt-2">
          Ele pode ter sido excluído ou o endereço está incorreto.
        </p>
        <Button asChild className="mt-6">
          <Link href="/admin">Voltar ao painel</Link>
        </Button>
      </div>
    </main>
  )
}
