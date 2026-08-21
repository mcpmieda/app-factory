# web-admin — perfil validado V0.4

> Este diretório descreve como gerar o futuro starter `web-admin`. O código do piloto em `pilots/web-admin/` continua sendo evidência experimental e não deve ser copiado cegamente como template definitivo.

## Objetivo

Criar sistemas administrativos reais com bootstrap enxuto, UI consistente, módulos opcionais e verificações reproduzíveis.

## Base padrão do perfil

- TypeScript;
- Next.js App Router;
- React;
- Tailwind CSS;
- shadcn/ui como base do design system;
- Zod para validação/contratos;
- Vitest para unit/integration adequados;
- Playwright para E2E crítico;
- ESLint/configuração oficial do Next para lint específico.

Detalhes e limites: `profiles/web-admin/PROFILE.md`.

## Módulos opcionais ativados por necessidade

### auth

Primeira opção do perfil quando login/identidade forem necessários: **Better Auth**.

Não instalar autenticação em projetos que não precisam dela.

### database

Primeira opção do perfil quando houver persistência própria: **Drizzle**.

O provider deve ser decidido conforme o ambiente. SQLite/better-sqlite3 fica como alternativa local/teste, não default de produção.

### advanced-ui

**ReUI seletivo**, por componente. Recomendado quando Data Grid, filtros complexos, calendário, Kanban ou outro padrão avançado reduzir trabalho de forma concreta.

Após instalação:
- revisar arquivos/dependências gerados;
- remover módulos não usados;
- executar lint/typecheck/testes.

### formatting

Biome pode ser usado como formatter complementar. Não substitui automaticamente o lint oficial do framework.

### forms

Começar simples. Avaliar React Hook Form/TanStack Form apenas quando a complexidade justificar.

### client-server-state

TanStack Query, Zustand ou equivalente entram apenas quando cache/sincronização/estado compartilhado trouxerem benefício real.

### observability

Sentry/OpenTelemetry somente conforme criticidade e operação real.

### monorepo

Turborepo somente se existirem múltiplos apps/pacotes com benefício concreto.

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
│       ├── data/
│       └── tests/
├── lib/
├── config/
└── types/
```

Simplificar para projetos menores quando necessário.

## Primeira fatia funcional

O starter deve permitir construir um módulo completo como `items`, `users` ou equivalente, contendo quando aplicável:

- listagem;
- busca/filtros;
- criação;
- edição;
- validação;
- persistência;
- loading/empty/error/success states;
- responsividade;
- testes unitários úteis;
- fluxo E2E com Playwright.

## Gate obrigatório de reprodutibilidade

O piloto V0.3 demonstrou que teste local não basta. O starter deve prever CI em checkout limpo com:

1. package manager/lockfile consistente;
2. instalação reproduzível (`npm ci` ou equivalente);
3. setup/migrations/seed quando aplicável;
4. format check;
5. lint;
6. typecheck sem depender de artefato gerado previamente;
7. testes unit/integration;
8. build;
9. auditoria de dependências proporcional;
10. Playwright desktop/mobile do fluxo crítico.

## Definition of Done

- instalação limpa passa;
- lint/format validado;
- typecheck;
- testes;
- build;
- aplicação executa;
- fluxo crítico passa em Playwright;
- desktop e mobile verificados;
- nenhum segredo no repositório;
- operações destrutivas relevantes têm proteção e teste;
- diff revisado;
- agentes conseguem retomar pelo GitHub sem contexto da conversa.

## O que já foi respondido pelo piloto V0.3

1. **A estrutura é navegável por IA?** Sim, com documentação curta + código organizado + estado no GitHub.
2. **shadcn + ReUI convivem?** Sim, mas ReUI funciona melhor como fonte seletiva de componentes avançados, não como segunda base obrigatória.
3. **Better Auth + Drizzle funcionam juntos?** Sim no piloto; ambos foram promovidos como primeiras opções condicionais do perfil.
4. **Zod funcionou bem?** Sim; promoção aprovada.
5. **Playwright fornece feedback suficiente?** Sim; promoção aprovada como E2E crítico.
6. **Biome substitui ESLint?** Não neste perfil; fica opcional/complementar.
7. **Codex Plugin aplica Skills corretamente?** Sim, validado na fase anterior.
8. **O processo reduziu intervenção manual?** Sim; o Codex executou scaffold, dependências, migrations, testes, browser e correções, e o ChatGPT fez a revisão/gates.

## Próximo passo técnico

Transformar este perfil em um starter gerável limpo, separado do piloto, e validá-lo criando um segundo app do zero. Só então marcar o starter como V1 estável.