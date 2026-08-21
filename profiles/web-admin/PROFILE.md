# Web Admin Profile

Status: `v1-rc`

Este perfil consolida somente decisões comprovadas pelo piloto V0.3. Ele não é uma stack universal para todo software.

## Quando usar

Aplicações administrativas, CRUDs, dashboards, ferramentas internas e sistemas de gestão com UI orientada a dados.

## Base padrão

Instalar por padrão neste perfil, salvo restrição real do projeto:

- TypeScript;
- Next.js App Router;
- React;
- Tailwind CSS;
- shadcn/ui como base do design system;
- Zod para validação/contratos;
- Vitest para testes unitários e de integração adequados;
- Playwright para o fluxo E2E crítico;
- ESLint/configuração oficial do Next para lint específico da stack.

## Módulos ativados por necessidade

### Autenticação

Quando o produto exigir login/identidade própria, preferir **Better Auth** como primeira opção do perfil.

Não instalar auth em projeto que não precisa de identidade.

Regras:

- validar sessão no servidor para operações protegidas;
- não confiar apenas em proteção visual/cliente;
- provider e estratégia de sessão devem considerar o ambiente real.
- o baseline testado do recipe fixa `better-auth` e a CLI correspondente `auth` em 1.7.1;
- executar o check de contrato do schema antes de revisar upgrade e criar migration nova em vez de reescrever histórico aplicado.

### Persistência

Quando o produto possuir dados próprios, preferir **Drizzle** como primeira opção do perfil.

O banco não é fixado universalmente. Escolher provider conforme deploy, volume, concorrência, custo e operação.

- SQLite/better-sqlite3: alternativa local/teste e aplicações realmente adequadas a arquivo local;
- PostgreSQL: recipe de produção validado com `DATABASE_URL`, migrations versionadas e sem persistência no filesystem local;
- outros destinos de produção/serverless: escolher provider apropriado ao ambiente antes de gerar a arquitetura definitiva.

### ReUI

**Opcional e seletivo.** Usar quando um componente avançado, como Data Grid, filtros complexos, Kanban, calendário ou outro padrão administrativo, reduzir trabalho de forma clara.

Após instalar via registry:

- revisar todos os arquivos adicionados;
- remover módulos/dependências não usados;
- executar lint/typecheck/testes;
- adaptar somente o necessário às regras atuais do React/stack.

Não tratar ReUI como segunda base visual paralela ao shadcn.

### Biome

Opcional como formatter/check complementar. Não substituir automaticamente lint específico do framework quando a cobertura não for equivalente.

### Formulários

Começar com a solução mais simples suportada pelo framework/Server Actions.

Adicionar React Hook Form, TanStack Form ou equivalente somente quando complexidade de formulário, validação cliente, campos dinâmicos ou UX justificarem.

### Estado/cache no cliente

Não adicionar TanStack Query, Zustand ou equivalente por padrão. Usar somente quando cache, sincronização cliente, optimistic updates ou estado compartilhado trouxerem ganho real.

### Observabilidade

Sentry/OpenTelemetry e similares entram conforme criticidade, produção e necessidade operacional. Não fazem parte do bootstrap mínimo.

## UI

- shadcn é a fundação;
- ReUI é uma fonte de componentes avançados, não um design system concorrente obrigatório;
- HeroUI é perfil alternativo para produtos em que seu sistema visual seja claramente mais adequado;
- não misturar HeroUI neste perfil apenas por estética.

## Arquitetura padrão

Preferir Server Components/Server Actions e estado local simples quando suficientes.

Adicionar camadas somente quando o comportamento do produto exigir.

Estrutura inicial sugerida:

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

A estrutura pode ser simplificada para apps menores.

## Gate mínimo de qualidade

Quando os scripts existirem:

1. instalação reproduzível (`npm ci` ou equivalente);
2. setup/migrations/seed quando aplicável;
3. format check;
4. lint;
5. typecheck;
6. testes unit/integration relevantes;
7. build;
8. auditoria de dependências proporcional ao risco;
9. Playwright do fluxo crítico;
10. desktop e viewport móvel;
11. console sem erro relevante.

Mudanças de recipe também exigem geração limpa direta de cada caminho de provider/dependência. PostgreSQL/Auth deve exercitar serviço PostgreSQL efêmero real, login/sessão, migration/query e smoke de produção com `next start`.

## Reprodutibilidade

- package manager/linha relevante deve ser consistente entre lockfile, desenvolvimento e CI;
- CI deve usar instalação limpa, não instalação permissiva para esconder lockfile inconsistente;
- typecheck e testes não podem depender silenciosamente de artefatos gerados por execução anterior.

## Segurança mínima

- segredos fora do Git;
- validação server-side para mutações;
- autorização no servidor;
- operações destrutivas protegidas por estado/regra de negócio e confirmação quando apropriado;
- migrations versionadas;
- excluir permanentemente apenas quando o domínio permitir e o comportamento estiver testado.

## Evidência de origem

Perfil derivado de `research/V0.3_WEB_ADMIN_PILOT.md`, da validação reutilizável em `research/V0.5_WEB_ADMIN_STARTER_VALIDATION.md` e do hardening PostgreSQL/recipes em `research/V0.6_WEB_ADMIN_HARDENING.md`.
