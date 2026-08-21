"use client"

import { Boxes, LayoutDashboard, LogOut, Menu } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import type { ReactNode } from "react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { authClient } from "@/lib/auth-client"

function Navigation() {
  return (
    <nav aria-label="Navegação principal" className="space-y-1">
      <Link
        className="bg-sidebar-accent flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium"
        href="/admin"
      >
        <LayoutDashboard className="size-4" /> Visão geral
      </Link>
    </nav>
  )
}

function Brand() {
  return (
    <div className="flex items-center gap-3 font-semibold">
      <span className="bg-primary text-primary-foreground grid size-9 place-items-center rounded-lg">
        <Boxes className="size-5" />
      </span>
      Recursos
    </div>
  )
}

export function AdminShell({ children, userName }: { children: ReactNode; userName: string }) {
  const router = useRouter()
  async function signOut() {
    await authClient.signOut()
    router.replace("/login")
    router.refresh()
  }

  return (
    <div className="min-h-screen md:grid md:grid-cols-[240px_1fr]">
      <aside className="bg-sidebar border-sidebar-border hidden border-r p-5 md:flex md:flex-col">
        <Brand />
        <div className="mt-8 flex-1">
          <Navigation />
        </div>
        <div className="border-sidebar-border space-y-3 border-t pt-4">
          <p className="text-muted-foreground truncate text-xs">
            Conectado como
            <br />
            <strong className="text-foreground">{userName}</strong>
          </p>
          <Button variant="outline" className="w-full justify-start" onClick={signOut}>
            <LogOut /> Sair
          </Button>
        </div>
      </aside>
      <div className="min-w-0">
        <header className="bg-background/85 sticky top-0 z-40 flex h-16 items-center justify-between border-b px-4 backdrop-blur md:hidden">
          <Brand />
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" aria-label="Abrir menu">
                <Menu />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-72 p-5">
              <SheetHeader className="p-0">
                <SheetTitle>
                  <Brand />
                </SheetTitle>
              </SheetHeader>
              <div className="mt-8">
                <Navigation />
              </div>
              <Button variant="outline" className="mt-8 w-full justify-start" onClick={signOut}>
                <LogOut /> Sair
              </Button>
            </SheetContent>
          </Sheet>
        </header>
        {children}
      </div>
    </div>
  )
}
