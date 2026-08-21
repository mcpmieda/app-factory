# web-admin — piloto V0.3

> Arquitetura candidata derivada da V0.2. Ainda não é starter estável.

## Objetivo

Validar a App Factory em um sistema administrativo realista sem carregar dependências que o produto não precisa.

## Base candidata

- TypeScript;
- Next.js como forte candidato para o piloto full-stack;
- Tailwind CSS;
- shadcn/ui;
- ReUI para padrões avançados de admin;
- Zod para contratos/validação;
- Playwright para E2E;
- Vitest para unit/integration quando adequado.

## Módulos opcionais

### auth

Candidato: Better Auth.

Ativar somente se o projeto exigir login/identidade.

### database

Candidato: Drizzle + banco escolhido conforme o ambiente.

Ativar somente se houver persistência própria.

### forms

Avaliar React Hook Form ou TanStack Form conforme complexidade e integração com componentes adotados. Não congelar antes do piloto.

### client-server-state

TanStack Query entra quando cache/mutações client-side trouxerem benefício real. Não usar por padrão em toda página se Server Components/Server Actions ou fetch simples resolverem melhor.

### observability

Sentry/OpenTelemetry somente quando o ambiente/criticidade justificar.

### monorepo

Turborepo somente se houver múltiplos apps/pacotes com benefício concreto.

## Estrutura candidata

```text
src/
├── app/
├── components/
│   ├── ui/
│   └── layout/
├── features/
│   └── <feature>/
│       ├── components/
│       ├── schemas/
│       ├── api/
│       └── tests/
├── lib/
├── config/
└── types/
```

A organização feature-based foi reforçada por referências como Bulletproof React e pelo dashboard starter auditado. A Factory deve adaptar, não copiar cegamente.

## Fatia piloto

Construir um módulo completo de exemplo, como `items` ou `users`, contendo:

- listagem;
- busca/filtros;
- criação;
- edição;
- validação;
- persistência quando o módulo de banco estiver ativo;
- loading/empty/error/success states;
- responsividade;
- testes unitários úteis;
- fluxo E2E com Playwright.

## Definition of Done do piloto

- lint/format validado;
- typecheck;
- testes;
- build;
- aplicação executa;
- fluxo crítico passa em Playwright;
- desktop e mobile verificados;
- nenhum segredo no repositório;
- diff revisado;
- agentes conseguem retomar pelo GitHub sem contexto da conversa.

## O que o piloto deve responder

1. A estrutura é simples para uma IA navegar?
2. shadcn + ReUI convivem sem conflito relevante?
3. Better Auth + Drizzle funciona de forma limpa quando ativado?
4. Zod integra bem os contratos necessários?
5. Playwright oferece feedback suficiente para o agente corrigir sozinho?
6. Biome simplifica o tooling sem perder checks importantes?
7. O Codex Plugin descobre e aplica as Skills corretamente?
8. O processo exige pouca intervenção manual do usuário?

Somente depois dessas respostas os candidatos viram defaults da V1.