# Web Admin Profile

Status: `v1`

Este perfil consolida somente decisões comprovadas pelo piloto V0.3 e pelos hardenings posteriores. Ele não é uma stack universal para todo software.

## Quando usar

Aplicações administrativas, CRUDs, dashboards, ferramentas internas e sistemas de gestão com UI orientada a dados.

## Project Adoption Gate antes do código

Quando o projeto for governado pela App Factory, este perfil **não pode ser aplicado apenas depois que a primeira UI já foi construída**.

Antes da primeira implementação funcional/visual material:

1. aplicar `core/PROJECT_ADOPTION_GATE.md` / `project-adoption`;
2. registrar `.app-factory.json` schema v2 com `profile = web-admin`;
3. registrar system level, risco, API mode, Semantic Verification/depth e Independent Verification;
4. registrar design system + Professional UI + Motion Profile;
5. para sistemas persistentes, registrar fonte autoritativa e recovery; para operações críticas interrompíveis, aplicar `core/SYSTEM_ENGINEERING.md`;
6. materializar specs/verification plan exigidos pela classificação;
7. passar `project_adoption_gate.py check --phase pre-implementation` ou checklist equivalente.

**React + CSS próprio, HTML/CSS nativo ou UI hand-rolled não são fallback silencioso deste perfil.** Se virarem a fundação visual, precisam de `ui.deviation` explícito com uma restrição real que justifique não usar o default validado. O fato de a aplicação existente usar React/Vite não é, sozinho, uma justificativa.

## Base padrão

Instalar por padrão neste perfil, salvo restrição real do projeto **ou escolha explícita de HeroUI como linguagem principal**:

- TypeScript;
- Next.js App Router;
- React;
- Tailwind CSS;
- shadcn/ui como base do design system;
- Zod para validação/contratos;
- Vitest para testes unitários e de integração adequados;
- Playwright para o fluxo E2E crítico;
- ESLint/configuração oficial do Next para lint específico da stack.

A stack do projeto existente pode ser preservada quando reconstruí-la seria inadequado. Preservar React/Vite/Cloudflare ou outra infraestrutura **não implica** preservar uma camada visual ad hoc: o design system deve ser avaliado separadamente e integrado de forma compatível quando possível.

Se o produto for explicitamente definido como **sistema HeroUI**, não instalar shadcn/ReUI por reflexo deste perfil. Usar HeroUI transversalmente e seguir a seção `HeroUI override` abaixo.

## Módulos ativados por necessidade

### Autenticação

Quando o produto exigir login/identidade própria, preferir **Better Auth** como primeira opção do perfil, salvo arquitetura/identidade já definida pelo produto.

Não instalar auth em projeto que não precisa de identidade.

Regras:

- validar sessão no servidor para operações protegidas;
- não confiar apenas em proteção visual/cliente;
- provider e estratégia de sessão devem considerar o ambiente real;
- executar checks/migrations adequados sem reescrever histórico aplicado.

### Persistência

Quando o produto possuir dados próprios, preferir **Drizzle** como primeira opção do perfil quando compatível.

O banco não é fixado universalmente. Escolher provider conforme deploy, volume, concorrência, custo e operação.

- SQLite/better-sqlite3: alternativa local/teste e aplicações realmente adequadas a arquivo local;
- PostgreSQL: opção de produção quando o caso exigir persistência compartilhada/robusta;
- outros destinos de produção/serverless: escolher provider apropriado ao ambiente antes de gerar a arquitetura definitiva.

### Continuidade após perda do cliente

Para `persistent-app` ou superior, a UI não pode ser a única guardiã de uma operação crítica.

Quando fechar o navegador, perder energia/rede ou trocar de dispositivo puder causar efeito parcial, duplicidade, divergência ou perda de progresso:

- persistir estado crítico server-side após aceitação do comando;
- usar identificador de operação/checkpoint/status quando necessário;
- reconciliar resultado ambíguo antes de repetir escrita;
- permitir retomada/status posterior quando o fluxo for demorado;
- registrar progresso por item em lotes quando execução parcial for material;
- escolher job, transação, lock, idempotência ou compensação apenas conforme a necessidade.

Não transformar pequenas mutações atômicas em jobs sem motivo. Seguir `core/SYSTEM_ENGINEERING.md`.

### APIs e integrações

Next.js Server Components/Server Actions continuam sendo a opção simples quando frontend e backend pertencem à mesma aplicação e não existe consumidor independente.

Quando o produto expuser/consumir API relevante, tiver web + mobile/extensão, integração externa, webhook, eventos ou evolução independente entre consumidor/provedor:

- aplicar `core/API_ENGINEERING.md` e `api-engineering`;
- classificar a interface como `none`, `lightweight`, `contract` ou `governed`;
- não exigir OpenAPI apenas porque há backend;
- escolher protocolo/contrato pela necessidade;
- ferramentas de contrato/compatibilidade são condicionais, não bootstrap universal.

Para telas administrativas orientadas a dados, aplicar também `core/DATA_ACCESS_EFFICIENCY.md` quando houver round trips materiais:

- evitar frontend `chatty`, N+1 e waterfalls sem dependência real;
- preferir composição orientada ao caso de uso quando vários dados são sempre necessários juntos;
- não criar endpoint monolítico apenas para reduzir contagem de requests;
- usar batching/paralelismo, paginação, seleção de campos, retry/rate-limit, read models e cache somente quando trouxerem ganho real;
- registrar/testar request budget quando custo, latência, quota ou estabilidade forem materiais.

### Independent Verification

Este perfil não instala scanners no bootstrap. A profundidade vem de `core/INDEPENDENT_VERIFICATION.md`.

- admin simples/baixo risco pode permanecer `baseline` ou `independent`;
- sistema administrativo multiusuário real tende a `adversarial` quando autenticação, dados compartilhados ou API/superfície web justificarem;
- release de produção/alto risco pode elevar para `release`;
- verificadores são selecionados somente quando aplicáveis;
- GitHub CI é preferido para a matriz independente quando capaz;
- verificações automatizadas não substituem testes de autorização, persistência nem revisão semântica.

### ReUI

**Opcional e seletivo**, somente na base shadcn deste perfil. Usar quando componente administrativo avançado reduzir trabalho de forma clara.

Após instalar via registry:

- revisar arquivos adicionados;
- remover módulos/dependências não usados;
- executar lint/typecheck/testes;
- adaptar somente o necessário.

Não tratar ReUI como segunda base visual paralela ao shadcn. Em sistema explicitamente HeroUI, não adicionar ReUI apenas para preencher estética/catálogo.

### Biome

Opcional como formatter/check complementar. Não substituir automaticamente lint específico do framework quando a cobertura não for equivalente.

### Formulários

Começar com a solução mais simples suportada pelo framework/design system.

Adicionar React Hook Form, TanStack Form ou equivalente somente quando a complexidade justificar.

### Estado/cache no cliente

Não adicionar TanStack Query, Zustand ou equivalente por padrão. Usar somente quando cache, sincronização cliente, optimistic updates ou estado compartilhado trouxerem ganho real.

Cache no cliente não deve mascarar arquitetura excessivamente `chatty` nem se tornar fonte autoritativa de estado crítico institucional.

### Observabilidade

Sentry/OpenTelemetry e similares entram conforme criticidade, produção e necessidade operacional. Não fazem parte do bootstrap mínimo.

## UI

- shadcn é a fundação visual padrão deste perfil **quando o produto não escolheu HeroUI**;
- ReUI é fonte seletiva de componentes avançados na variante shadcn;
- **HeroUI é perfil visual alternativo** para produtos em que seu sistema visual seja claramente mais adequado;
- uma escolha explícita de **sistema inteiro baseado em HeroUI/HeroUI Pro** prevalece sobre o default shadcn/ReUI;
- não misturar HeroUI com shadcn/ReUI apenas por estética;
- toda interface herda `ui/MOTION_POLICY.md` e `ui/PROFESSIONAL_UI_PROFILE.md`.

### HeroUI override

Quando HeroUI for a linguagem principal:

1. consultar `ui/heroui/README.md` e os catálogos HeroUI antes de construir equivalentes;
2. não instalar shadcn/ReUI por padrão deste perfil;
3. registrar `Design System: HeroUI`, `Professional UI Profile` e `Motion Profile` no `.app-factory.json` e estado do projeto;
4. usar HeroUI em shell, formulários, dados, overlays, feedback, tokens, temas e motion quando aplicável;
5. adaptar composição, cores e densidade ao produto sem imitar componentes de outro design system;
6. validar desktop/mobile/reduced motion e ausência de jank/obstrução.

A escolha de HeroUI **não ativa nenhum efeito ambiental obrigatório**. Atmosfera e decoração são decisões do projeto.

### Living UI / Semantic Motion

Motion Profile padrão: **`ambient` contextual**.

Na variante shadcn/ReUI ou HeroUI, `ambient` não exige partículas, auroras ou outro efeito específico em toda tela. Aplicar microinterações, feedback de estado, dados, atenção e navegação proporcionalmente.

`prefers-reduced-motion` é obrigatório para movimento não essencial; `prefers-reduced-transparency` pode ser progressive enhancement.

## Arquitetura padrão

Preferir Server Components/Server Actions e estado local simples quando suficientes.

Adicionar camadas somente quando o comportamento do produto exigir. Os contratos Core definem profundidade arquitetural, continuidade de operações, API, eficiência de dados e verificação.

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

1. Project Adoption Gate `pre-implementation` verde antes do código em projeto governado;
2. instalação reproduzível;
3. setup/migrations/seed quando aplicável;
4. format check;
5. lint;
6. typecheck;
7. testes unit/integration relevantes;
8. build;
9. auditoria de dependências proporcional ao risco;
10. Playwright do fluxo crítico;
11. desktop e viewport móvel;
12. console sem erro relevante;
13. motion coerente com o perfil e `prefers-reduced-motion`;
14. operações críticas interrompíveis verificadas quanto a estado durável, idempotência/reconciliação/retomada quando aplicável;
15. para API/fluxos data-driven/Independent Verification, executar gates proporcionais selecionados;
16. Project Adoption Gate `delivery` verde antes de conclusão em projeto governado.

## Reprodutibilidade

- package manager/linha relevante deve ser consistente entre lockfile, desenvolvimento e CI;
- CI deve usar instalação limpa;
- typecheck e testes não podem depender silenciosamente de artefatos gerados por execução anterior;
- ferramentas usadas como gate devem ter versão/commit fixado quando necessário.

## Segurança mínima

- segredos fora do Git;
- validação server-side para mutações;
- autorização no servidor;
- operações de alto impacto protegidas;
- migrations versionadas;
- APIs expostas seguem contratos Core + security-review;
- verificações ativas usam apenas alvo autorizado e ambiente apropriado.

## Evidência de origem

Perfil derivado do piloto/hardening web-admin, `core/PROJECT_ADOPTION_GATE.md`, `core/SYSTEM_ENGINEERING.md`, `ui/MOTION_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md` e auditoria final da linha V1.
