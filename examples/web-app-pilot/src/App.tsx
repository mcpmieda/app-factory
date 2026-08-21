import { useMemo, useState } from "react";
import { bookingSchema, spaces, type Booking, type Space } from "./booking";
import "./App.css";
type Step = "choose" | "details" | "form" | "loading" | "success";
type Errors = Partial<Record<keyof Booking, string>>;
function Stepper({ step }: { step: Step }) {
  const active = step === "choose" ? 1 : step === "details" ? 2 : 3;
  return (
    <ol className="stepper" aria-label="Progresso da reserva">
      {["Escolha", "Horário", "Confirmação"].map((label, index) => (
        <li className={index + 1 <= active ? "active" : ""} key={label}>
          <span>{index + 1}</span>
          {label}
        </li>
      ))}
    </ol>
  );
}
function SpaceCard({
  space,
  onChoose,
}: {
  space: Space;
  onChoose: (space: Space) => void;
}) {
  return (
    <article className={`space-card ${space.tone}`}>
      <div className="space-visual" aria-hidden="true">
        <span></span>
        <span></span>
      </div>
      <p className="capacity">Até {space.capacity} pessoas</p>
      <h2>{space.name}</h2>
      <p>{space.feature}</p>
      <button onClick={() => onChoose(space)}>
        Ver horários <span aria-hidden="true">→</span>
      </button>
    </article>
  );
}
export default function App() {
  const [step, setStep] = useState<Step>("choose");
  const [selected, setSelected] = useState<Space>();
  const [query, setQuery] = useState("");
  const [date, setDate] = useState("2026-08-25");
  const [period, setPeriod] = useState<Booking["period"]>("Manhã");
  const [errors, setErrors] = useState<Errors>({});
  const filtered = useMemo(
    () =>
      spaces.filter((space) =>
        space.name.toLowerCase().includes(query.trim().toLowerCase()),
      ),
    [query],
  );
  function choose(space: Space) {
    setSelected(space);
    setStep("details");
  }
  function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = Object.fromEntries(
      new FormData(event.currentTarget),
    ) as Record<string, string>;
    const parsed = bookingSchema.safeParse({ ...data, date, period });
    if (!parsed.success) {
      const next: Errors = {};
      for (const issue of parsed.error.issues)
        next[issue.path[0] as keyof Booking] = issue.message;
      setErrors(next);
      return;
    }
    setErrors({});
    setStep("loading");
    window.setTimeout(() => setStep("success"), 450);
  }
  function reset() {
    setSelected(undefined);
    setQuery("");
    setStep("choose");
  }
  return (
    <main>
      <header className="app-header">
        <a href="#inicio" className="brand">
          <span>e.</span>Encontro
        </a>
        <Stepper step={step} />
        <a
          className="help"
          aria-label="Abrir ajuda"
          href="mailto:ajuda@encontro.example"
        >
          ?
        </a>
      </header>
      <section id="inicio" className="app-shell">
        {step === "choose" ? (
          <>
            <div className="intro">
              <p className="eyebrow">Reserve seu espaço</p>
              <h1>Onde sua próxima ideia vai acontecer?</h1>
              <p>
                Escolha um ambiente, encontre um horário e confirme. Sem
                cadastro.
              </p>
            </div>
            <label className="search">
              <span>Buscar espaço</span>
              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Ex.: Aurora"
              />
            </label>
            {filtered.length ? (
              <div className="space-grid">
                {filtered.map((space) => (
                  <SpaceCard key={space.id} space={space} onChoose={choose} />
                ))}
              </div>
            ) : (
              <div className="empty" role="status">
                <span aria-hidden="true">⌕</span>
                <h2>Nenhum espaço encontrado</h2>
                <p>Tente buscar por outro nome.</p>
                <button onClick={() => setQuery("")}>Limpar busca</button>
              </div>
            )}
          </>
        ) : null}
        {step === "details" && selected ? (
          <section className="flow-card">
            <button className="back" onClick={() => setStep("choose")}>
              ← Voltar aos espaços
            </button>
            <p className="eyebrow">{selected.name}</p>
            <h1>Escolha quando encontrar.</h1>
            <div className="choice-row">
              <label>
                Data
                <input
                  aria-label="Data"
                  type="date"
                  min="2026-08-22"
                  value={date}
                  onChange={(event) => setDate(event.target.value)}
                />
              </label>
              <fieldset>
                <legend>Período</legend>
                {(["Manhã", "Tarde"] as const).map((value) => (
                  <label className="radio" key={value}>
                    <input
                      type="radio"
                      name="period"
                      checked={period === value}
                      onChange={() => setPeriod(value)}
                    />
                    <span>
                      {value}
                      <small>
                        {value === "Manhã" ? "09:00 — 12:00" : "14:00 — 17:00"}
                      </small>
                    </span>
                  </label>
                ))}
              </fieldset>
            </div>
            <button className="primary" onClick={() => setStep("form")}>
              Continuar
            </button>
          </section>
        ) : null}
        {step === "form" && selected ? (
          <section className="flow-card">
            <button className="back" onClick={() => setStep("details")}>
              ← Alterar horário
            </button>
            <p className="eyebrow">Última etapa</p>
            <h1>Quem fará a reserva?</h1>
            <div className="summary">
              <strong>{selected.name}</strong>
              <span>
                {date} · {period}
              </span>
            </div>
            <form onSubmit={submit} noValidate>
              <label>
                Nome
                <input
                  name="name"
                  aria-invalid={Boolean(errors.name)}
                  aria-describedby={errors.name ? "name-error" : undefined}
                />
                {errors.name ? (
                  <small id="name-error" className="error">
                    {errors.name}
                  </small>
                ) : null}
              </label>
              <label>
                E-mail
                <input
                  name="email"
                  type="email"
                  aria-invalid={Boolean(errors.email)}
                  aria-describedby={errors.email ? "email-error" : undefined}
                />
                {errors.email ? (
                  <small id="email-error" className="error">
                    {errors.email}
                  </small>
                ) : null}
              </label>
              <button className="primary" type="submit">
                Confirmar reserva
              </button>
            </form>
          </section>
        ) : null}
        {step === "loading" ? (
          <section className="state-card" aria-live="polite">
            <span className="loader" aria-hidden="true"></span>
            <h1>Confirmando sua reserva…</h1>
            <p>Estamos preparando os detalhes.</p>
          </section>
        ) : null}
        {step === "success" && selected ? (
          <section className="state-card success" aria-live="polite">
            <span className="check" aria-hidden="true">
              ✓
            </span>
            <p className="eyebrow">Tudo certo</p>
            <h1>Seu encontro já tem lugar.</h1>
            <p>
              <strong>{selected.name}</strong>
              <br />
              {date} · {period}
            </p>
            <button className="primary" onClick={reset}>
              Fazer outra reserva
            </button>
          </section>
        ) : null}
      </section>
      <footer>
        <span>Cenário fictício · Nenhum dado é persistido</span>
        <span>Motion Profile: ambient contextual</span>
      </footer>
    </main>
  );
}
