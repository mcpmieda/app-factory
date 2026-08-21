# Web Admin Pilot

Piloto V0.3 da App Factory: painel administrativo local para gestão de recursos genéricos. Ele valida uma fatia vertical com autenticação, dashboard, busca/filtros, criação, edição, desativação reversível, exclusão de inativos e persistência SQLite.

> Este diretório é um experimento isolado. Não é o starter oficial da App Factory.

## Requisitos

- Node.js 22+ (validado também com Node.js 24);
- npm 10+.

## Executar localmente

```bash
npm install
npm run setup
npm run dev
```

Abra `http://localhost:3000`. O setup cria `.env.local` ignorado pelo Git, gera um secret aleatório, aplica migrations e cria uma conta de demonstração. As credenciais locais iniciais são `admin@example.com` / `local-pilot-password`; altere `SEED_ADMIN_*` antes do primeiro seed quando necessário.

O comando é idempotente: não sobrescreve ambiente, usuário ou registros já existentes.

## Verificação

```bash
npm run format:check
npm run lint
npm run typecheck
npm run test:coverage
npm run build
npm run e2e
```

Para uma máquina sem Chromium do Playwright, execute uma vez `npx playwright install chromium`.

## Estrutura relevante

- `src/app/api/auth/[...all]/route.ts`: endpoint Better Auth;
- `src/app/admin/`: área protegida e Server Actions autenticadas;
- `src/db/schema.ts`: schema de autenticação e recursos;
- `drizzle/`: migrations versionadas;
- `scripts/`: ambiente local, migrate e seed;
- `tests/e2e/`: jornada crítica desktop e mobile.

## Segurança e limites

- cadastro público está desativado; apenas o seed local cria o administrador;
- toda leitura administrativa passa pelo layout protegido e toda mutação revalida a sessão no servidor;
- exclusão permanente só aceita registros já inativos;
- SQLite e as credenciais de demonstração são escolhas locais do piloto, não recomendações de produção;
- somente `.env.example` é versionado; banco e `.env.local` permanecem ignorados.

Resultados, decisões e limitações completas estão em [`research/V0.3_WEB_ADMIN_PILOT.md`](../../research/V0.3_WEB_ADMIN_PILOT.md).
