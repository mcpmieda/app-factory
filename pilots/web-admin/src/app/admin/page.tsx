import { CircleCheck, PackageCheck, Plus, Search, Wrench } from "lucide-react"
import Link from "next/link"
import { ItemsGrid } from "@/components/items-grid"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { getItemMetrics, listItems } from "@/lib/items"

type SearchParams = Promise<{ q?: string; status?: string; activity?: string; notice?: string }>

const notices: Record<string, string> = {
  created: "Registro criado com sucesso.",
  updated: "Registro atualizado com sucesso.",
}

export default async function AdminPage({ searchParams }: { searchParams: SearchParams }) {
  const params = await searchParams
  const activity =
    params.activity === "inactive" || params.activity === "all" ? params.activity : "active"
  const [records, metrics] = await Promise.all([
    listItems({ query: params.q, status: params.status, activity }),
    getItemMetrics(),
  ])
  const rows = records.map((item) => ({
    ...item,
    updatedAt: new Intl.DateTimeFormat("pt-BR", { dateStyle: "short" }).format(item.updatedAt),
  }))

  return (
    <main className="mx-auto w-full max-w-7xl space-y-8 p-4 py-8 sm:p-8">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-muted-foreground text-sm font-medium">Painel administrativo</p>
          <h1 className="text-3xl font-semibold tracking-tight">Visão geral de recursos</h1>
          <p className="text-muted-foreground mt-2">
            Consulte, cadastre e mantenha os registros em um único lugar.
          </p>
        </div>
        <Button asChild>
          <Link href="/admin/items/new">
            <Plus /> Novo registro
          </Link>
        </Button>
      </div>
      {params.notice && notices[params.notice] ? (
        <Alert className="border-emerald-200 bg-emerald-50 text-emerald-950">
          <CircleCheck />
          <AlertTitle>Pronto</AlertTitle>
          <AlertDescription>{notices[params.notice]}</AlertDescription>
        </Alert>
      ) : null}
      <section aria-label="Indicadores" className="grid gap-4 sm:grid-cols-3">
        <Card>
          <CardHeader className="flex-row items-center justify-between">
            <div>
              <CardDescription>Total de registros</CardDescription>
              <CardTitle className="mt-1 text-3xl">{metrics.total}</CardTitle>
            </div>
            <PackageCheck className="text-muted-foreground" />
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="flex-row items-center justify-between">
            <div>
              <CardDescription>Ativos</CardDescription>
              <CardTitle className="mt-1 text-3xl">{metrics.active}</CardTitle>
            </div>
            <CircleCheck className="text-emerald-600" />
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="flex-row items-center justify-between">
            <div>
              <CardDescription>Em manutenção</CardDescription>
              <CardTitle className="mt-1 text-3xl">{metrics.maintenance}</CardTitle>
            </div>
            <Wrench className="text-amber-600" />
          </CardHeader>
        </Card>
      </section>
      <Card>
        <CardHeader>
          <CardTitle>Registros</CardTitle>
          <CardDescription>
            Busca textual, filtros, edição e ciclo seguro de desativação.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-5">
          <form className="grid gap-3 lg:grid-cols-[1fr_180px_180px_auto]" role="search">
            <div className="relative">
              <Search className="text-muted-foreground absolute top-2.5 left-3 size-4" />
              <Input
                className="pl-9"
                name="q"
                defaultValue={params.q}
                placeholder="Buscar nome, categoria ou local"
                aria-label="Buscar registros"
              />
            </div>
            <select
              name="status"
              defaultValue={params.status ?? "all"}
              className="border-input bg-background h-9 rounded-md border px-3 text-sm"
              aria-label="Filtrar por status"
            >
              <option value="all">Todos os status</option>
              <option value="available">Disponível</option>
              <option value="allocated">Alocado</option>
              <option value="maintenance">Manutenção</option>
            </select>
            <select
              name="activity"
              defaultValue={activity}
              className="border-input bg-background h-9 rounded-md border px-3 text-sm"
              aria-label="Filtrar por atividade"
            >
              <option value="active">Somente ativos</option>
              <option value="inactive">Somente inativos</option>
              <option value="all">Ativos e inativos</option>
            </select>
            <Button type="submit" variant="outline">
              Aplicar filtros
            </Button>
          </form>
          <ItemsGrid data={rows} />
        </CardContent>
      </Card>
    </main>
  )
}
