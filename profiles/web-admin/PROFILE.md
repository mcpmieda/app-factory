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
5. materializar specs/verification plan exigidos pela classificação;
6. passar `project_adoption_gate.py check --phase pre-implementation` ou checklist equivalente.

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
- scanners/ferramentas são selecionados somente quando aplicáveis;
- GitHub CI é preferido para a matriz independente quando capaz;
- scanners não substituem testes de autorização, persistência nem revisão semântica.

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

Cache no cliente não deve mascarar arquitetura excessivamente `chatty`.

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
3. ativar automaticamente `ui/AMBIENT_CONSTELLATION_PROFILE.md`;
4. registrar no `.app-factory.json` e estado do projeto:

```text
Motion Profile: ambient
Ambient Surface Profile: ambient-constellation
Constellation Intensity: strong
Dense content: clean islands; constellation remains in shell/header/perimeter
Reduced motion: static constellation fallback
```

5. aplicar constelação de forma forte a shell/header/hero/dashboard overview/login/empty-waiting/AI/modais importantes/painéis e cards especiais quando existirem;
6. manter Data Grid/tabelas/forms densos em superfícies limpas, sem abandonar a assinatura no entorno;
7. adaptar constelação aos tokens/temas HeroUI;
8. validar desktop/mobile/reduced motion e ausência de jank/obstrução.

Pedidos explícitos `ambient constellation`, `ambient constellarion`, `ambiente de constelação` ou equivalentes ativam o mesmo perfil mesmo fora de HeroUI.

### Living UI / Semantic Motion

Motion Profile padrão: **`ambient` contextual**.

Na variante shadcn/ReUI, `ambient` não exige partículas/auroras em toda tela. Aplicar microinterações, feedback de estado, dados, atenção e navegação proporcionalmente.

Na variante HeroUI com `ambient-constellation`, **atenuar o movimento em áreas densas, mas preservar a identidade constelar no shell/perímetro/cabeçalho**.

`prefers-reduced-motion` é obrigatório para movimento não essencial; constelação usa fallback estático. `prefers-reduced-transparency` pode ser progressive enhancement.

## Arquitetura padrão

Preferir Server Components/Server Actions e estado local simples quando suficientes.

Adicionar camadas somente quando o comportamento do produto exigir. Os contratos Core definem profundidade arquitetural, API, eficiência de dados e verificação.

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
14. quando `ambient-constellation` estiver ativo: efeito perceptível, partículas sem interação, dense content limpo, fallback estático e zero flashing/strobe;
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
- operações destrutivas protegidas;
- migrations versionadas;
- APIs expostas seguem contratos Core + security-review;
- DAST/fuzz ativo usa apenas alvo efêmero/autorizado.

## Evidência de origem

Perfil derivado do piloto/hardening web-admin, `core/PROJECT_ADOPTION_GATE.md`, `ui/MOTION_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md`, `ui/AMBIENT_CONSTELLATION_PROFILE.md`, pesquisa `research/AMBIENT_CONSTELLATION_RESEARCH.md` e auditoria final da linha V1.
