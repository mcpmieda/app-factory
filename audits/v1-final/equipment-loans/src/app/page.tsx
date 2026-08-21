import Link from "next/link";
import { Boxes, ClockAlert, PackageCheck, Search, Users } from "lucide-react";
import type { LucideIcon } from "lucide-react";

import { AmbientSurface } from "@/components/motion/ambient-surface";
import { buttonVariants } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { localIsoDate, type EquipmentStatus } from "@/features/loans/domain";
import { LoanForm } from "@/features/loans/loan-form";
import { listEquipment } from "@/features/loans/repository";
import { ReturnButton } from "@/features/loans/return-button";

export const dynamic = "force-dynamic";

const statusLabels: Record<EquipmentStatus, string> = {
  available: "Disponível",
  loaned: "Emprestado",
  overdue: "Atrasado",
};

const statusStyles: Record<EquipmentStatus, string> = {
  available: "bg-emerald-50 text-emerald-800 ring-emerald-600/20",
  loaned: "bg-blue-50 text-blue-800 ring-blue-600/20",
  overdue: "bg-rose-50 text-rose-800 ring-rose-600/20",
};

function formatDate(value: string) {
  return new Intl.DateTimeFormat("pt-BR", { timeZone: "UTC" }).format(
    new Date(`${value}T00:00:00Z`),
  );
}

function filterHref(status: string, query: string) {
  const params = new URLSearchParams();
  if (status !== "all") params.set("status", status);
  if (query) params.set("q", query);
  const suffix = params.toString();
  return suffix ? `/?${suffix}` : "/";
}

export default async function Home({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; status?: string }>;
}) {
  const params = await searchParams;
  const query = params.q?.trim() ?? "";
  const status = ["available", "loaned", "overdue"].includes(
    params.status ?? "",
  )
    ? (params.status as EquipmentStatus)
    : "all";
  const items = listEquipment();
  const normalizedQuery = query.toLocaleLowerCase("pt-BR");
  const filtered = items.filter((item) => {
    const matchesStatus = status === "all" || item.status === status;
    const haystack = [
      item.name,
      item.assetTag,
      item.category,
      item.responsibleName ?? "",
    ]
      .join(" ")
      .toLocaleLowerCase("pt-BR");
    return (
      matchesStatus && (!normalizedQuery || haystack.includes(normalizedQuery))
    );
  });
  const availableItems = items
    .filter((item) => item.status === "available")
    .map(({ id, name, assetTag }) => ({ id, name, assetTag }));
  const counts = {
    available: items.filter((item) => item.status === "available").length,
    loaned: items.filter((item) => item.status === "loaned").length,
    overdue: items.filter((item) => item.status === "overdue").length,
  };

  return (
    <main className="min-h-screen bg-[linear-gradient(to_bottom,var(--color-background),var(--color-muted)/0.45)] px-5 py-7 sm:px-8 lg:py-10">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-6">
        <AmbientSurface className="rounded-2xl border bg-card/90 p-6 shadow-sm sm:p-8">
          <div className="flex flex-col justify-between gap-5 lg:flex-row lg:items-center">
            <div className="flex items-start gap-4">
              <span className="grid size-11 shrink-0 place-items-center rounded-xl bg-primary text-primary-foreground shadow-sm">
                <Boxes aria-hidden="true" className="size-5" />
              </span>
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Controle escolar
                </p>
                <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
                  Empréstimos de equipamentos
                </h1>
                <p className="mt-2 max-w-2xl text-sm leading-6 text-muted-foreground">
                  Veja onde está cada item, registre saídas e acompanhe
                  devoluções atrasadas.
                </p>
              </div>
            </div>
            <a
              className={cn(buttonVariants({ size: "lg" }), "w-full sm:w-auto")}
              href="#novo-emprestimo"
            >
              Registrar empréstimo
            </a>
          </div>
        </AmbientSurface>

        <section
          aria-label="Resumo dos equipamentos"
          className="grid gap-3 sm:grid-cols-3"
        >
          {(
            [
              [
                "Disponíveis",
                counts.available,
                PackageCheck,
                "text-emerald-700",
              ],
              ["Emprestados no prazo", counts.loaned, Users, "text-blue-700"],
              ["Atrasados", counts.overdue, ClockAlert, "text-rose-700"],
            ] as Array<[string, number, LucideIcon, string]>
          ).map(([label, value, Icon, color]) => (
            <Card key={String(label)}>
              <CardContent className="flex items-center justify-between pt-1">
                <div>
                  <p className="text-sm text-muted-foreground">{label}</p>
                  <p className="mt-1 text-3xl font-semibold">{value}</p>
                </div>
                <Icon aria-hidden="true" className={cn("size-6", color)} />
              </CardContent>
            </Card>
          ))}
        </section>

        <section className="grid items-start gap-6 xl:grid-cols-[minmax(0,1fr)_23rem]">
          <Card>
            <CardHeader className="border-b">
              <CardTitle>Itens e disponibilidade</CardTitle>
              <CardDescription>
                Busque por item, patrimônio ou responsável.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-5">
              <form className="flex flex-col gap-2 sm:flex-row" role="search">
                {status !== "all" && (
                  <input name="status" type="hidden" value={status} />
                )}
                <div className="relative flex-1">
                  <Search
                    aria-hidden="true"
                    className="pointer-events-none absolute left-3 top-2.5 size-4 text-muted-foreground"
                  />
                  <Input
                    className="pl-9"
                    defaultValue={query}
                    name="q"
                    placeholder="Buscar equipamento ou responsável"
                  />
                </div>
                <button
                  className={buttonVariants({ variant: "secondary" })}
                  type="submit"
                >
                  Buscar
                </button>
              </form>

              <nav
                aria-label="Filtrar por situação"
                className="flex flex-wrap gap-2"
              >
                {[
                  ["all", "Todos"],
                  ["available", "Disponíveis"],
                  ["loaned", "Emprestados"],
                  ["overdue", "Atrasados"],
                ].map(([value, label]) => (
                  <Link
                    aria-current={status === value ? "page" : undefined}
                    className={buttonVariants({
                      variant: status === value ? "default" : "outline",
                      size: "sm",
                    })}
                    href={filterHref(value, query)}
                    key={value}
                  >
                    {label}
                  </Link>
                ))}
              </nav>

              {filtered.length === 0 ? (
                <div className="rounded-xl border border-dashed p-8 text-center">
                  <PackageCheck
                    aria-hidden="true"
                    className="mx-auto mb-3 size-7 text-muted-foreground"
                  />
                  <p className="font-medium">Nenhum equipamento encontrado</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Ajuste a busca ou escolha outro filtro.
                  </p>
                </div>
              ) : (
                <ul className="grid gap-3" data-testid="equipment-list">
                  {filtered.map((item) => (
                    <li
                      className="grid gap-4 rounded-xl border p-4 transition-colors hover:bg-muted/35 sm:grid-cols-[minmax(0,1fr)_auto] sm:items-center"
                      data-status={item.status}
                      key={item.id}
                    >
                      <div className="min-w-0">
                        <div className="flex flex-wrap items-center gap-2">
                          <h2 className="font-medium">{item.name}</h2>
                          <span
                            className={cn(
                              "rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset",
                              statusStyles[item.status],
                            )}
                          >
                            {statusLabels[item.status]}
                          </span>
                        </div>
                        <p className="mt-1 text-sm text-muted-foreground">
                          {item.assetTag} · {item.category}
                        </p>
                        {item.responsibleName && item.dueDate && (
                          <p className="mt-2 text-sm">
                            Com <strong>{item.responsibleName}</strong> ·
                            devolução {formatDate(item.dueDate)}
                          </p>
                        )}
                      </div>
                      {item.loanId && <ReturnButton loanId={item.loanId} />}
                    </li>
                  ))}
                </ul>
              )}
            </CardContent>
          </Card>

          <Card className="scroll-mt-6 xl:sticky xl:top-6" id="novo-emprestimo">
            <CardHeader className="border-b">
              <CardTitle>Novo empréstimo</CardTitle>
              <CardDescription>
                Apenas itens disponíveis aparecem aqui.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <LoanForm
                availableItems={availableItems}
                today={localIsoDate()}
              />
            </CardContent>
          </Card>
        </section>
      </div>
    </main>
  );
}
