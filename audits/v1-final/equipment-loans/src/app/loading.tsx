export default function Loading() {
  return (
    <main
      aria-busy="true"
      aria-label="Carregando equipamentos"
      className="mx-auto min-h-screen w-full max-w-7xl animate-pulse space-y-6 px-5 py-8 motion-reduce:animate-none sm:px-8"
    >
      <div className="h-20 rounded-2xl bg-muted" />
      <div className="grid gap-4 sm:grid-cols-3">
        <div className="h-28 rounded-xl bg-muted" />
        <div className="h-28 rounded-xl bg-muted" />
        <div className="h-28 rounded-xl bg-muted" />
      </div>
      <div className="h-96 rounded-xl bg-muted" />
    </main>
  );
}
