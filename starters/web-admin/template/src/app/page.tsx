import { ArrowRight, Boxes, CheckCircle2, ShieldCheck } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { projectConfig } from "@/config/project";

const foundations = [
  "Next.js App Router e TypeScript",
  "Tailwind CSS e shadcn/ui",
  "Zod, Vitest e Playwright",
  "ESLint oficial do Next",
];

export default function Home() {
  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,var(--color-primary)/0.08,transparent_36%),linear-gradient(to_bottom,var(--color-background),var(--color-muted)/0.55)] px-5 py-10 sm:px-8 lg:py-16">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-8">
        <header className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="grid size-10 place-items-center rounded-xl bg-primary text-primary-foreground shadow-sm">
              <Boxes aria-hidden="true" className="size-5" />
            </span>
            <div>
              <p className="text-sm font-semibold">{projectConfig.name}</p>
              <p className="text-xs text-muted-foreground">Perfil web-admin</p>
            </div>
          </div>
          <span className="rounded-full border bg-background/80 px-3 py-1 text-xs font-medium text-muted-foreground backdrop-blur">
            Factory {projectConfig.factoryBaseline}
          </span>
        </header>

        <section className="grid gap-6 lg:grid-cols-[1.35fr_0.65fr]">
          <Card className="overflow-hidden border-primary/15 bg-card/90 shadow-xl shadow-primary/5">
            <CardHeader className="space-y-5 p-7 sm:p-10">
              <div className="w-fit rounded-full border border-primary/15 bg-primary/5 px-3 py-1 text-xs font-semibold text-primary">
                Starter limpo e componível
              </div>
              <div className="space-y-3">
                <h1 className="max-w-2xl text-3xl font-semibold leading-tight tracking-tight sm:text-5xl">
                  Comece pelo domínio, não pela infraestrutura.
                </h1>
                <CardDescription className="max-w-2xl text-base leading-7 sm:text-lg">
                  {projectConfig.description} A base inclui somente ferramentas
                  comprovadas; autenticação, banco e UI avançada entram por
                  necessidade.
                </CardDescription>
              </div>
              <Button className="w-fit" size="lg">
                Definir primeira fatia
                <ArrowRight aria-hidden="true" />
              </Button>
            </CardHeader>
          </Card>

          <Card className="bg-foreground text-background shadow-xl">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <ShieldCheck aria-hidden="true" className="size-5" />
                Base aprovada
              </CardTitle>
              <CardDescription className="text-background/65">
                Sem serviços ou estado global impostos.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3 text-sm">
                {foundations.map((foundation) => (
                  <li className="flex items-start gap-2" key={foundation}>
                    <CheckCircle2
                      aria-hidden="true"
                      className="mt-0.5 size-4 shrink-0 text-emerald-400"
                    />
                    {foundation}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </section>

        <section className="grid gap-4 sm:grid-cols-3">
          {[
            ["Auth", "Ative Better Auth apenas se houver identidade própria."],
            ["Dados", "Ative Drizzle e escolha o provider pelo ambiente real."],
            [
              "UI avançada",
              "Adote ReUI seletivamente quando a complexidade justificar.",
            ],
          ].map(([title, description]) => (
            <Card className="bg-card/70" key={title}>
              <CardHeader>
                <CardTitle className="text-base">{title}</CardTitle>
                <CardDescription className="leading-6">
                  {description}
                </CardDescription>
              </CardHeader>
            </Card>
          ))}
        </section>
      </div>
    </main>
  );
}
