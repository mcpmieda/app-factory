# Web Admin Profile

Status: `v1`

Este perfil consolida somente decisões comprovadas pelo piloto V0.3 e pelos hardenings posteriores. Ele não é uma stack universal para todo software.

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
- provider e estratégia de sessão devem considerar o ambiente real;
- o baseline testado do recipe fixa `better-auth` e a CLI correspondente `auth` em 1.7.1;
- executar o check de contrato do schema antes de revisar upgrade e criar migration nova em vez de reescrever histórico aplicado.

### Persistência

Quando o produto possuir dados próprios, preferir **Drizzle** como primeira opção do perfil.

O banco não é fixado universalmente. Escolher provider conforme deploy, volume, concorrência, custo e operação.

- SQLite/better-sqlite3: alternativa local/teste e aplicações realmente adequadas a arquivo local;
- PostgreSQL: recipe de produção validado com `DATABASE_URL`, migrations versionadas e sem persistência no filesystem local;
- outros destinos de produção/serverless: escolher provider apropriado ao ambiente antes de gerar a arquitetura definitiva.

### APIs e integrações

Next.js Server Components/Server Actions continuam sendo a opção simples quando frontend e backend pertencem à mesma aplicação e não existe consumidor independente.

Quando o produto expuser/consumir API relevante, tiver web + mobile/extensão, integração externa, webhook, eventos ou evolução independente entre consumidor/provedor:

- aplicar `core/API_ENGINEERING.md` e `api-engineering`;
- classificar a interface como `none`, `lightweight`, `contract` ou `governed`;
- não exigir OpenAPI apenas porque há backend;
- para HTTP compartilhado `contract`/`governed`, preferir OpenAPI como fonte de verdade e gates proporcionais;
- GraphQL, gRPC, AsyncAPI e Arazzo entram somente quando o comportamento do produto justificar;
- Redocly/oasdiff/Schemathesis/Pact são ferramentas condicionais, não parte obrigatória do bootstrap mínimo.

Para telas administrativas orientadas a dados, aplicar também `core/DATA_ACCESS_EFFICIENCY.md` quando houver round trips materiais:

- evitar frontend `chatty`, N+1 e waterfalls sem dependência real;
- quando vários dados são sempre necessários juntos, preferir endpoint/Server Action/composição orientada ao caso de uso em vez de o cliente montar a tela com muitas chamadas pequenas;
- não substituir isso por um endpoint monolítico `/api/tudo`;
- manter serviços internos pequenos e composáveis mesmo quando a fronteira externa é agregada;
- usar batching/paralelismo, paginação, seleção de campos, retry/`Retry-After`, read models e cache somente quando trouxerem ganho real;
- para telas críticas, registrar/testar request budget quando custo, latência, quota ou estabilidade forem materiais;
- não usar threshold universal de chamadas por tela: a justificativa vem do fluxo real.

### Independent Verification

Este perfil não instala scanners no bootstrap. A profundidade vem de `core/INDEPENDENT_VERIFICATION.md`.

- admin simples/baixo risco pode permanecer `baseline` ou `independent`;
- sistema administrativo multiusuário real tende a `adversarial` quando autenticação, dados compartilhados ou API/superfície web justificarem;
- release de produção/alto risco pode elevar para `release`;
- Trivy/Semgrep/axe, mutation testing, Schemathesis, ZAP e Lighthouse são selecionados somente quando aplicáveis;
- GitHub CI é preferido para a matriz independente quando capaz;
- scanners não substituem testes de autorização, persistência nem revisão semântica.

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

Cache no cliente não deve mascarar uma arquitetura excessivamente `chatty`. Primeiro elimine chamadas redundantes/N+1 e defina a fronteira de dados adequada; depois use cache quando houver benefício próprio de UX/sincronização.

### Observabilidade

Sentry/OpenTelemetry e similares entram conforme criticidade, produção e necessidade operacional. Não fazem parte do bootstrap mínimo.

Quando `core/DATA_ACCESS_EFFICIENCY.md` for material, observabilidade pode incluir contagem de requests por fluxo crítico, chamadas ao provedor, `429`/retries e latência, sem registrar dados sensíveis.

## UI

- shadcn é a fundação visual padrão deste perfil;
- ReUI é uma fonte de componentes avançados, não um design system concorrente obrigatório;
- HeroUI é perfil visual alternativo para produtos em que seu sistema visual seja claramente mais adequado;
- não misturar HeroUI neste perfil apenas por estética ou para obter animações;
- toda interface herda `ui/MOTION_POLICY.md`.

### Living UI / Semantic Motion

Motion Profile padrão: **`ambient` contextual**.

Em `web-admin`, isso não significa manter partículas, auroras ou fundos animados em tabelas densas. Aplicar:

- microinterações em botões, cards, campos, menus e ações;
- feedback animado de loading/saving/success/error quando útil;
- gráficos e indicadores com transição apenas para mudanças reais;
- ações que exigem atenção com halo/pulso discreto e temporário;
- navegação/modais/painéis com transições curtas e previsíveis;
- atmosfera ambiente em login, espera, empty states, cabeçalhos e áreas com espaço visual quando não competir com dados.

Atenuar automaticamente para comportamento `subtle` em tabelas, leitura prolongada, dashboards muito densos ou situações de desempenho/concentração.

`prefers-reduced-motion` é obrigatório para movimento não essencial.

## Arquitetura padrão

Preferir Server Components/Server Actions e estado local simples quando suficientes.

Adicionar camadas somente quando o comportamento do produto exigir. `core/SYSTEM_ENGINEERING.md` define a profundidade mínima do sistema; `core/API_ENGINEERING.md` define a profundidade da interface quando houver uma API/integração real; `core/DATA_ACCESS_EFFICIENCY.md` define eficiência de aquisição/composição quando a tela cruza rede de forma material; `core/INDEPENDENT_VERIFICATION.md` define a profundidade da prova externa.

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

A estrutura pode ser simplificada para apps menores. Se houver contrato formal de API, use diretório `api/` ou equivalente adequado ao stack sem forçar essa pasta a projetos sem contrato independente. `VERIFICATION.md` entra somente quando Independent Verification ficar acima de `baseline`.

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
11. console sem erro relevante;
12. motion coerente com o perfil e `prefers-reduced-motion` quando UI relevante for alterada;
13. para API `contract`/`governed`, gates de contrato/compatibilidade/runtime/security definidos em `core/API_ENGINEERING.md`;
14. para fluxo data-driven em que quota/custo/latência sejam materiais, evidência proporcional de `core/DATA_ACCESS_EFFICIENCY.md` — por exemplo request count, ausência de N+1, batching/paginação/retry quando aplicável;
15. para Independent Verification acima de `baseline`, checks `required` selecionados em `core/INDEPENDENT_VERIFICATION.md`.

Mudanças de recipe também exigem geração limpa direta de cada caminho de provider/dependência. PostgreSQL/Auth deve exercitar serviço PostgreSQL efêmero real, login/sessão, migration/query e smoke de produção com `next start`.

## Reprodutibilidade

- package manager/linha relevante deve ser consistente entre lockfile, desenvolvimento e CI;
- CI deve usar instalação limpa, não instalação permissiva para esconder lockfile inconsistente;
- typecheck e testes não podem depender silenciosamente de artefatos gerados por execução anterior;
- ferramentas de API e Independent Verification usadas como gate devem ter versão/commit fixado, não depender de `latest` em CI.

## Segurança mínima

- segredos fora do Git;
- validação server-side para mutações;
- autorização no servidor;
- operações destrutivas protegidas por estado/regra de negócio e confirmação quando apropriado;
- migrations versionadas;
- excluir permanentemente apenas quando o domínio permitir e o comportamento estiver testado;
- APIs expostas seguem `core/API_ENGINEERING.md` + `skills/security-review` em vez de duplicar um checklist específico neste perfil;
- superfícies data-driven seguem `core/DATA_ACCESS_EFFICIENCY.md` para evitar que otimização de cliente enfraqueça autorização, cache scope ou limites de provedor;
- scanners independentes seguem `core/INDEPENDENT_VERIFICATION.md`; ZAP/fuzz ativo usa apenas alvo efêmero/autorizado.

## Evidência de origem

Perfil derivado de `research/V0.3_WEB_ADMIN_PILOT.md`, da validação reutilizável em `research/V0.5_WEB_ADMIN_STARTER_VALIDATION.md`, do hardening PostgreSQL/recipes em `research/V0.6_WEB_ADMIN_HARDENING.md`, da política universal de motion em `ui/MOTION_POLICY.md` e da auditoria final `research/V1.0_FINAL_AUDIT.md`.