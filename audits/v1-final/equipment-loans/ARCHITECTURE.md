# Architecture

## Baseline

- Next.js App Router + React + TypeScript;
- Tailwind CSS + shadcn/ui;
- Motion Profile: `ambient` contextual per App Factory `ui/MOTION_POLICY.md`;
- Zod at input/configuration boundaries;
- Vitest and Playwright;
- Server Components and Server Actions when sufficient.

## Motion

- use semantic motion for interaction, data, state, attention and navigation;
- use ambient backgrounds/effects only where they do not compete with dense administrative content;
- attenuate to `subtle` in dense tables/reading-heavy views;
- support `prefers-reduced-motion` for non-essential movement;
- do not add another design system only for animation.

## Optional modules

- `auth-better-auth`: identity and protected operations;
- `database-drizzle`: local/test SQLite persistence;
- `database-drizzle-postgres`: PostgreSQL persistence for production-style environments;
- `advanced-ui-reui`: selective advanced administrative components.

Do not add client state, form, observability, motion library or monorepo layers until a concrete flow needs them.

## Decisões deste slice

- recipe ativado: `database-drizzle`, com SQLite somente para execução local/teste;
- sem auth: o audit não exige identidade e não será publicado;
- mutações: Server Actions validadas por Zod; a API existe para contrato E2E local;
- integridade: transação + índice único parcial `one_active_loan_per_equipment`;
- dados: `equipment` e histórico de `loans`, sem exclusão destrutiva;
- UI: Server Component para consulta/filtro e componentes cliente pequenos apenas nos formulários;
- Motion Profile: `ambient` no cabeçalho, atenuado para `subtle` na lista densa, com reduced motion obrigatório.

## Segurança e produção

Todos os registros de seed são fictícios e não existem secrets. Este slice é intencionalmente local. Um deploy real exige escolher provider adequado, autenticar a equipe e autorizar mutações no servidor antes de expor Server Actions/API.
