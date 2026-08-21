import { Boxes } from "lucide-react"
import { redirect } from "next/navigation"
import { LoginForm } from "@/components/login-form"
import { Card, CardContent, CardDescription, CardHeader } from "@/components/ui/card"
import { getCurrentSession } from "@/lib/session"

export default async function LoginPage() {
  if (await getCurrentSession()) redirect("/admin")
  return (
    <main className="grid min-h-screen place-items-center px-4 py-10">
      <div className="w-full max-w-md space-y-6">
        <div className="flex items-center justify-center gap-3 text-sm font-semibold">
          <span className="bg-primary text-primary-foreground grid size-10 place-items-center rounded-xl">
            <Boxes aria-hidden="true" />
          </span>
          App Factory
        </div>
        <Card className="shadow-xl shadow-slate-950/5">
          <CardHeader>
            <h1 className="font-heading text-2xl leading-snug font-medium">Acesse o painel</h1>
            <CardDescription>
              Use a conta administrativa criada pelo comando de setup local.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <LoginForm />
          </CardContent>
        </Card>
      </div>
    </main>
  )
}
