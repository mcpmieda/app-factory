"use client";

import {
  Activity,
  ArrowUpRight,
  BellRing,
  Check,
  CircleAlert,
  Gauge,
  LoaderCircle,
  Radio,
  RefreshCw,
  Sparkles,
} from "lucide-react";
import type { CSSProperties } from "react";
import { useEffect, useRef, useState } from "react";

import { AmbientSurface } from "@/components/motion/ambient-surface";
import { AttentionPulse } from "@/components/motion/attention-pulse";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { projectConfig } from "@/config/project";

type ProcessingState = "idle" | "processing" | "success";

const queueItems = [
  { label: "Triagem automática", status: "Operando", value: "18 itens" },
  { label: "Revisão da equipe", status: "Atenção", value: "3 itens" },
  { label: "Concluídos hoje", status: "Estável", value: "42 itens" },
];

export function PulseDeskDashboard() {
  const [capacity, setCapacity] = useState(68);
  const [metricRevision, setMetricRevision] = useState(0);
  const [metricMessage, setMetricMessage] = useState(
    "Última atualização às 14:32",
  );
  const [processingState, setProcessingState] =
    useState<ProcessingState>("idle");
  const [attentionActive, setAttentionActive] = useState(true);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const processingTimer = useRef<number | null>(null);

  useEffect(() => {
    return () => {
      if (processingTimer.current !== null) {
        window.clearTimeout(processingTimer.current);
      }
    };
  }, []);

  function refreshWithoutChange() {
    setMetricMessage("Reconsulta concluída: nenhum valor mudou");
  }

  function applyCapacityChange() {
    if (capacity === 82) {
      setMetricMessage("Capacidade já está no valor mais recente");
      return;
    }

    setCapacity(82);
    setMetricRevision((revision) => revision + 1);
    setMetricMessage("Mudança real recebida: +14 pontos");
  }

  function processQueue() {
    if (processingTimer.current !== null) {
      window.clearTimeout(processingTimer.current);
    }

    setProcessingState("processing");
    processingTimer.current = window.setTimeout(() => {
      setProcessingState("success");
      processingTimer.current = null;
    }, 1_600);
  }

  function acknowledgeAttention() {
    setAttentionActive(false);
  }

  function handleDrawerChange(open: boolean) {
    setDrawerOpen(open);
    if (open) acknowledgeAttention();
  }

  const metricStyle = {
    "--metric-value": `${capacity}%`,
  } as CSSProperties;
  const processingMessage =
    processingState === "processing"
      ? "Validando 18 itens em segundo plano."
      : processingState === "success"
        ? "18 itens validados com sucesso."
        : "";

  return (
    <main className="min-h-screen overflow-x-clip bg-slate-950 text-slate-50">
      <AmbientSurface
        className="border-b border-white/10"
        data-testid="ambient-hero"
        tone="hero"
      >
        <div className="relative mx-auto flex w-full max-w-7xl flex-col gap-8 px-5 pb-10 pt-6 sm:px-8 lg:pb-14">
          <header className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <span className="grid size-11 place-items-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-cyan-200 shadow-lg shadow-cyan-950/30">
                <Radio aria-hidden="true" className="size-5" />
              </span>
              <div>
                <p className="font-semibold tracking-tight">
                  {projectConfig.name}
                </p>
                <p className="text-xs text-slate-400">Central de operações</p>
              </div>
            </div>
            <span className="rounded-full border border-emerald-300/20 bg-emerald-300/10 px-3 py-1.5 text-xs font-medium text-emerald-200">
              <span className="mr-2 inline-block size-1.5 rounded-full bg-emerald-300" />
              Sistema estável
            </span>
          </header>

          <section className="grid items-end gap-8 lg:grid-cols-[1.2fr_0.8fr]">
            <div className="space-y-5">
              <div className="inline-flex items-center gap-2 rounded-full border border-cyan-200/15 bg-white/5 px-3 py-1.5 text-xs font-medium text-cyan-100 backdrop-blur">
                <Sparkles aria-hidden="true" className="size-3.5" />
                Turno da tarde em fluxo
              </div>
              <div className="space-y-3">
                <h1 className="max-w-3xl text-4xl font-semibold leading-tight tracking-[-0.04em] text-balance sm:text-6xl">
                  Decisões claras, no ritmo da operação.
                </h1>
                <p className="max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
                  Acompanhe a fila, perceba mudanças reais e resolva somente o
                  que exige intervenção humana.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 rounded-3xl border border-white/10 bg-white/[0.055] p-4 backdrop-blur-xl">
              <div className="rounded-2xl bg-white/[0.055] p-4">
                <p className="text-xs text-slate-400">Em fluxo</p>
                <p className="mt-2 text-3xl font-semibold">63</p>
                <p className="mt-1 text-xs text-emerald-300">+8 nesta hora</p>
              </div>
              <div className="rounded-2xl bg-white/[0.055] p-4">
                <p className="text-xs text-slate-400">Tempo médio</p>
                <p className="mt-2 text-3xl font-semibold">4m</p>
                <p className="mt-1 text-xs text-cyan-300">dentro da meta</p>
              </div>
            </div>
          </section>
        </div>
      </AmbientSurface>

      <div className="mx-auto grid w-full max-w-7xl gap-5 px-5 py-8 sm:px-8 lg:grid-cols-[1.35fr_0.65fr] lg:py-10">
        <section className="space-y-5" aria-labelledby="operations-title">
          <div className="flex flex-wrap items-end justify-between gap-3">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-300">
                Agora
              </p>
              <h2 className="mt-1 text-2xl font-semibold" id="operations-title">
                Pulso da operação
              </h2>
            </div>
            <Button
              className="motion-control border-white/10 bg-white/5 text-slate-100 hover:bg-white/10"
              onClick={refreshWithoutChange}
              variant="outline"
            >
              <RefreshCw aria-hidden="true" />
              Reconsultar
            </Button>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <Card className="motion-card border-0 bg-slate-900 text-slate-50 ring-white/10 sm:col-span-2">
              <CardHeader className="gap-3 sm:grid-cols-[1fr_auto]">
                <div>
                  <CardDescription className="text-slate-400">
                    Capacidade disponível
                  </CardDescription>
                  <CardTitle className="mt-1 flex items-baseline gap-2 text-3xl">
                    <span
                      className="metric-value"
                      data-testid="capacity-value"
                      key={metricRevision}
                    >
                      {capacity}%
                    </span>
                    <span className="text-xs font-normal text-slate-400">
                      da meta diária
                    </span>
                  </CardTitle>
                </div>
                <Button
                  className="motion-control mt-2 bg-cyan-300 text-slate-950 hover:bg-cyan-200 sm:mt-0"
                  onClick={applyCapacityChange}
                >
                  Simular mudança real
                  <ArrowUpRight aria-hidden="true" />
                </Button>
              </CardHeader>
              <CardContent className="space-y-3">
                <div
                  aria-label={`Capacidade disponível: ${capacity}%`}
                  aria-valuemax={100}
                  aria-valuemin={0}
                  aria-valuenow={capacity}
                  className="h-3 overflow-hidden rounded-full bg-white/8"
                  data-motion-revision={metricRevision}
                  data-testid="capacity-meter"
                  role="progressbar"
                  style={metricStyle}
                >
                  <div className="metric-fill h-full rounded-full bg-gradient-to-r from-cyan-400 to-emerald-300" />
                </div>
                <p aria-live="polite" className="text-xs text-slate-400">
                  {metricMessage}
                </p>
              </CardContent>
            </Card>

            {queueItems.map((item) => (
              <Card
                className="motion-card border-0 bg-slate-900/80 text-slate-50 ring-white/10"
                key={item.label}
              >
                <CardHeader>
                  <CardDescription className="text-slate-400">
                    {item.label}
                  </CardDescription>
                  <CardTitle className="text-2xl">{item.value}</CardTitle>
                </CardHeader>
                <CardContent>
                  <span className="inline-flex items-center gap-2 text-xs text-slate-300">
                    <span className="size-1.5 rounded-full bg-cyan-300" />
                    {item.status}
                  </span>
                </CardContent>
              </Card>
            ))}

            <AmbientSurface
              className="min-h-44 rounded-xl ring-1 ring-white/10 sm:col-span-2"
              data-testid="ambient-empty"
              tone="empty"
            >
              <div className="relative flex h-full min-h-44 flex-col items-center justify-center gap-3 px-6 py-8 text-center">
                <span className="grid size-10 place-items-center rounded-2xl bg-cyan-300/10 text-cyan-200">
                  <Check aria-hidden="true" className="size-5" />
                </span>
                <div>
                  <h3 className="font-medium">Nenhum bloqueio crítico</h3>
                  <p className="mt-1 text-sm text-slate-400">
                    A superfície continua viva sem competir com a leitura.
                  </p>
                </div>
              </div>
            </AmbientSurface>
          </div>
        </section>

        <aside className="space-y-5" aria-label="Ações e estado">
          <AttentionPulse
            active={attentionActive}
            className="rounded-xl"
            data-testid="attention-pulse"
          >
            <Card className="border-amber-300/25 bg-amber-300/[0.075] text-slate-50 ring-amber-200/10">
              <CardHeader>
                <div className="flex items-center justify-between gap-3">
                  <span className="grid size-9 place-items-center rounded-xl bg-amber-300/10 text-amber-200">
                    <BellRing aria-hidden="true" className="size-4" />
                  </span>
                  <span className="rounded-full bg-amber-300/10 px-2.5 py-1 text-xs font-medium text-amber-200">
                    Pendente há 12 min
                  </span>
                </div>
                <CardTitle className="mt-3">
                  Revisão humana necessária
                </CardTitle>
                <CardDescription className="leading-6 text-slate-300">
                  Três solicitações têm sinais conflitantes e aguardam decisão.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Dialog open={drawerOpen} onOpenChange={handleDrawerChange}>
                  <DialogTrigger asChild>
                    <Button
                      className="motion-control w-full bg-amber-300 text-slate-950 hover:bg-amber-200"
                      onFocus={acknowledgeAttention}
                    >
                      Revisar pendência
                      <ArrowUpRight aria-hidden="true" />
                    </Button>
                  </DialogTrigger>
                  <DialogContent data-testid="review-drawer">
                    <DialogHeader>
                      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-amber-600">
                        Contexto preservado
                      </p>
                      <DialogTitle>Revisão de prioridade</DialogTitle>
                      <DialogDescription>
                        A mudança de contexto é curta e mantém a fila visível ao
                        fundo. A atenção deixa de pulsar assim que você entra na
                        revisão.
                      </DialogDescription>
                    </DialogHeader>
                    <div className="space-y-3 rounded-2xl bg-muted p-4">
                      <div className="flex items-start gap-3">
                        <CircleAlert
                          aria-hidden="true"
                          className="mt-0.5 size-5 shrink-0 text-amber-600"
                        />
                        <div>
                          <p className="font-medium">Solicitação PD-204</p>
                          <p className="mt-1 text-sm leading-6 text-muted-foreground">
                            Urgência alta, mas sem impacto operacional
                            confirmado.
                          </p>
                        </div>
                      </div>
                    </div>
                    <DialogFooter>
                      <DialogClose asChild>
                        <Button variant="outline">Deixar para depois</Button>
                      </DialogClose>
                      <DialogClose asChild>
                        <Button onClick={() => setAttentionActive(false)}>
                          Marcar como revisada
                        </Button>
                      </DialogClose>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </CardContent>
            </Card>
          </AttentionPulse>

          <Card className="border-0 bg-slate-900 text-slate-50 ring-white/10">
            <CardHeader>
              <span className="grid size-9 place-items-center rounded-xl bg-violet-300/10 text-violet-200">
                <Gauge aria-hidden="true" className="size-4" />
              </span>
              <CardTitle className="mt-3">Processamento de fila</CardTitle>
              <CardDescription className="leading-6 text-slate-400">
                O estado permanece legível mesmo quando o movimento é reduzido.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button
                className="motion-control w-full border-white/10 bg-white/5 text-slate-100 hover:bg-white/10"
                disabled={processingState === "processing"}
                onClick={processQueue}
                variant="outline"
              >
                {processingState === "processing" ? (
                  <LoaderCircle
                    aria-hidden="true"
                    className="state-spinner"
                    data-testid="state-spinner"
                  />
                ) : processingState === "success" ? (
                  <Check aria-hidden="true" />
                ) : (
                  <Activity aria-hidden="true" />
                )}
                {processingState === "processing"
                  ? "Processando…"
                  : processingState === "success"
                    ? "Fila processada"
                    : "Processar fila"}
              </Button>
              <p
                aria-live="polite"
                className="min-h-5 text-center text-xs text-slate-400"
                data-processing-state={processingState}
                data-testid="processing-state"
              >
                {processingMessage}
              </p>
            </CardContent>
          </Card>
        </aside>
      </div>
    </main>
  );
}
