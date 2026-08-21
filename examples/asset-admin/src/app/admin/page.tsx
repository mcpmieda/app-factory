import { Archive, CircleCheckBig, Plus, Search, Wrench } from "lucide-react";
import Link from "next/link";

import { AssetList } from "@/components/asset-list";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { categoryLabels, statusLabels } from "@/features/assets/asset-labels";
import { getAssetStats, listAssets } from "@/features/assets/asset-data";

type SearchParams = Promise<Record<string, string | string[] | undefined>>;

function valueOf(value: string | string[] | undefined) {
  return typeof value === "string" ? value : "";
}

export default async function AdminPage({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  const params = await searchParams;
  const filters = {
    query: valueOf(params.q),
    category: valueOf(params.category),
    status: valueOf(params.status),
    location: valueOf(params.location),
    archived: valueOf(params.archived) === "true",
  };
  const [records, stats] = await Promise.all([
    listAssets(filters),
    getAssetStats(),
  ]);
  const notice = valueOf(params.notice);

  return (
    <main className="mx-auto w-full max-w-7xl space-y-7 px-4 py-7 sm:px-6 sm:py-10">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-medium text-primary">Dashboard</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight">
            Patrimônio escolar
          </h1>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-muted-foreground">
            Inventário demonstrativo com dados totalmente fictícios para validar
            o starter web-admin.
          </p>
        </div>
        <Button asChild>
          <Link href="/admin/assets/new">
            <Plus />
            Novo patrimônio
          </Link>
        </Button>
      </div>

      {notice ? (
        <Alert className="border-emerald-200 bg-emerald-50 text-emerald-950">
          <CircleCheckBig />
          <AlertTitle>Alteração salva</AlertTitle>
          <AlertDescription>
            {notice === "created"
              ? "O patrimônio foi cadastrado."
              : "O patrimônio foi atualizado."}
          </AlertDescription>
        </Alert>
      ) : null}

      <section
        aria-label="Resumo"
        className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4"
      >
        {[
          { label: "Ativos", value: stats.active, icon: CircleCheckBig },
          { label: "Disponíveis", value: stats.available, icon: Search },
          { label: "Em manutenção", value: stats.maintenance, icon: Wrench },
          { label: "Arquivados", value: stats.archived, icon: Archive },
        ].map(({ label, value, icon: Icon }) => (
          <Card key={label}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {label}
              </CardTitle>
              <Icon className="size-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-semibold">{value}</p>
            </CardContent>
          </Card>
        ))}
      </section>

      <section className="space-y-4">
        <div>
          <h2 className="text-lg font-semibold">Inventário</h2>
          <p className="text-sm text-muted-foreground">
            Busca e filtros são aplicados no servidor.
          </p>
        </div>
        <form className="grid gap-3 rounded-xl border bg-background p-4 sm:grid-cols-2 lg:grid-cols-6">
          <div className="relative sm:col-span-2">
            <Search className="absolute left-3 top-2.5 size-4 text-muted-foreground" />
            <Input
              aria-label="Buscar patrimônio"
              className="pl-9"
              defaultValue={filters.query}
              name="q"
              placeholder="Código, descrição ou local"
            />
          </div>
          <select
            aria-label="Categoria"
            className="h-9 rounded-lg border bg-transparent px-3 text-sm"
            defaultValue={filters.category}
            name="category"
          >
            <option value="">Todas as categorias</option>
            {Object.entries(categoryLabels).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
          <select
            aria-label="Situação"
            className="h-9 rounded-lg border bg-transparent px-3 text-sm"
            defaultValue={filters.status}
            name="status"
          >
            <option value="">Todas as situações</option>
            {Object.entries(statusLabels).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
          <Input
            aria-label="Filtrar localização"
            defaultValue={filters.location}
            name="location"
            placeholder="Localização"
          />
          <div className="flex gap-2">
            <Button className="flex-1" type="submit" variant="secondary">
              Filtrar
            </Button>
            <Button
              asChild
              aria-label="Limpar filtros"
              size="icon"
              variant="outline"
            >
              <Link href="/admin">×</Link>
            </Button>
          </div>
          <label className="flex items-center gap-2 text-sm text-muted-foreground sm:col-span-2">
            <input
              defaultChecked={filters.archived}
              name="archived"
              type="checkbox"
              value="true"
            />
            Mostrar somente arquivados
          </label>
        </form>
        <AssetList records={records} />
      </section>
    </main>
  );
}
