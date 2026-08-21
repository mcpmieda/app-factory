# Changelog

## 1.0.0 — 2026-08-21

Primeira release estável da App Factory.

### Aprovado para release

- auditoria final end-to-end concluída sem blocker objetivo;
- bootstrap isolado do plugin Codex com 11 Skills e integridade origem/cache;
- roteamento por pedido comum sem palavra-chave especial;
- sistema novo de empréstimos criado do zero, com persistência, regras de negócio e browser desktop/mobile;
- Living UI e `prefers-reduced-motion` validados;
- continuidade por segundo agente sem contexto e recuperação de regressão controlada comprovadas;
- gates anteriores de web-admin, PostgreSQL/Auth, Living UI e quatro famílias universais permanecem verdes;
- gerador e starter passam a derivar/registrar a baseline corrente da Factory, eliminando referência operacional antiga a V0.7;
- perfil `web-admin` promovido de `v1-rc` para `v1`.

### Evidência

- `research/V1.0_FINAL_AUDIT.md`;
- `audits/v1-final/equipment-loans/`;
- `research/evidence/V1_CONTINUITY_HANDOFF.md`;
- `research/evidence/V1_CONTROLLED_RECOVERY.md`;
- `.github/workflows/validate-v1-release.yml`.

## 1.0.0-rc.1 — 2026-08-21

Release candidate final da App Factory, sem tag ou publicação antecipada.

### Validado

- bootstrap do plugin Codex 0.149 em `CODEX_HOME` e checkout temporários, com 11 Skills idênticas entre origem e cache;
- roteamento de um pedido comum para `web-admin`, escala M e risco médio sem palavra-chave especial;
- novo sistema fictício de empréstimos criado pelo starter + recipe Drizzle, sem copiar pilotos;
- empréstimo → reload → devolução, atrasados, busca, integridade transacional, desktop, mobile, teclado e reduced motion;
- continuidade por segundo agente sem histórico e recuperação após regressão controlada;
- composição dos gates existentes de Core/Skills/plugin, starter, Living UI, web-admin e quatro pilotos universais;
- varredura de secrets, dados reais e artefatos pesados.

### Evidência

- `research/V1.0_FINAL_AUDIT.md`;
- `audits/v1-final/equipment-loans/`;
- `.github/workflows/validate-v1-release.yml`;
- `scripts/validate_v1_{bootstrap,release}.py`.

## 0.9-universal-validation — 2026-08-21

Validação da Factory fora do perfil `web-admin` com quatro slices completos.

### Validado

- website Astro estático com duas rotas, SEO, desktop/mobile/teclado/reduced motion;
- web-app Vite/React voltado ao usuário final com empty, validação, loading e sucesso;
- extensão Chrome MV3 carregada em Chromium persistent context, permissões mínimas e ZIP de validação;
- automação Python local com erro parcial, dry-run, escrita atômica e idempotência;
- recuperação read-only por agentes sem contexto em website e automation;
- quatro perfis condicionais `validated` e workflow com jobs independentes.

### Evidência

- `research/V0.9_UNIVERSAL_VALIDATION.md`;
- `examples/{website,web-app,chrome-extension,automation}-pilot/`;
- `.github/workflows/validate-universal-pilots.yml`.

## 0.8-living-ui-validation — 2026-08-21

Validação executável de Living UI / Semantic Motion em uma interface administrativa gerada.

### Validado

- app fictício `Pulse Desk` gerado do baseline V0.7 sem auth, banco ou biblioteca de motion adicional;
- categorias ambient, interaction, data, state, attention e navigation em fluxo funcional;
- atenção encerra após foco/abertura e dados não reanimam sem mudança real;
- Playwright desktop, mobile e reduced motion, com gate estrito de console e overflow;
- evidências visuais e relatório em `research/V0.8_LIVING_UI_VALIDATION.md`.

### Promovido

- `AmbientSurface` e `AttentionPulse` como primitives opt-in do starter;
- tokens mínimos de duração/easing e fallback de `prefers-reduced-motion`;
- baseline textual do template alinhado ao manifesto V0.7;
- workflow dedicado de Living UI.

## 0.7-living-ui — 2026-08-21

Política universal Living UI / Semantic Motion.

### Criado

- `ui/MOTION_POLICY.md` como contrato framework-agnostic de movimento;
- Motion Profiles `none`, `subtle`, `ambient` e `expressive`;
- `ambient` como default contextual da Factory;
- categorias semânticas para ambiente, interação, dados, estado, atenção e navegação;
- regras obrigatórias de `prefers-reduced-motion`, performance e adaptação automática de intensidade.

### Integrado

- `ui-builder` passa a aplicar Semantic Motion independente de HeroUI, shadcn, ReUI ou outro design system;
- templates de produto/arquitetura passam a registrar Motion Profile;
- perfil `web-admin` herda `ambient`, atenuando para `subtle` em telas densas/leitura prolongada;
- starter `web-admin` registra o comportamento de motion sem adicionar biblioteca de animação obrigatória;
- validador estrutural passa a exigir UI e Motion Policy.

### Regras de atenção e dados

- ações importantes podem receber halo/pulso discreto e temporário;
- a animação de atenção deve parar/reduzir após cumprir sua função;
- gráficos e indicadores podem animar entrada/mudança real, mas não devem reanimar sem mudança de dado;
- motion nunca deve competir com leitura, foco, desempenho ou acessibilidade.

## 0.6-web-admin-hardening — 2026-08-21

Hardening pré-V1 do perfil `web-admin`.

### Criado

- resolução simples de capabilities, conflitos e variantes condicionais de recipes;
- recipe `database-drizzle-postgres` sem dependências SQLite;
- migrations, query smoke e `next start` smoke para o caminho PostgreSQL;
- contrato executável de schema Better Auth 1.7.1 e política curta de manutenção;
- CI com geração direta dos recipes SQLite e PostgreSQL/Auth em Postgres efêmero real.

### Validado

- Auth sozinho resolve automaticamente o provider SQLite local;
- combinação explícita SQLite/Auth não duplica recipes;
- PostgreSQL satisfaz a capability de banco do Auth sem instalar `better-sqlite3`;
- migrations/seed são idempotentes e login/sessão usam PostgreSQL real no CI;
- starter base e exemplo V0.5 permanecem gates de regressão;
- perfil promovido no draft para `v1-rc`, preservando deploy público real como fase autorizada separadamente.

## 0.5-web-admin-starter — 2026-08-21

Validação de que o perfil `web-admin` pode gerar aplicações novas sem depender da cópia do piloto V0.3.

### Criado

- starter limpo em `starters/web-admin/template/`;
- gerador Node multiplataforma com proteção de destino, personalização, manifesto e lockfile npm 10.9.9;
- recipes pequenos para Drizzle, Better Auth e decisão seletiva de ReUI;
- segundo app gerado em `examples/asset-admin/` para patrimônio escolar fictício;
- workflow que gera uma cópia temporária e valida starter e exemplo em checkout limpo;
- relatório e evidências visuais V0.5.

### Validado localmente

- Better Auth e Drizzle entram por requisito, não no starter base;
- SQLite é provider somente local/teste;
- ReUI foi corretamente dispensado para uma listagem sem complexidade avançada;
- setup/migrations/seed idempotentes;
- format, lint, typecheck sem artefato prévio, testes, build e audit high/critical;
- fluxo crítico Playwright em desktop/mobile e navegador real sem overlay.

### Próximo gate

Revisar o draft PR e o CI antes de decidir estabilidade V1. Provider de produção e manutenção do schema Better Auth continuam decisões dependentes do destino real.

## 0.4-web-admin-profile — 2026-08-21

Promoção controlada dos aprendizados comprovados pelo piloto V0.3.

### Promovido

- criado `profiles/` como camada de defaults condicionais validados;
- criado `profiles/web-admin/PROFILE.md`;
- `factory-router` passa a selecionar perfil validado quando o produto corresponder claramente;
- `app-planner` passa a aplicar defaults de perfil sem exigir decisões técnicas rotineiras do usuário;
- `core/ENTRYPOINT.md` passa a incluir seleção de perfil;
- shadcn promovido como base visual do perfil `web-admin`;
- ReUI reclassificado como opcional/seletivo por componente;
- Better Auth promovido como primeira opção quando autenticação própria for necessária;
- Drizzle promovido como primeira opção quando persistência própria for necessária;
- Zod, Vitest, Playwright e lint específico do Next promovidos no perfil;
- SQLite/better-sqlite3 mantido como alternativa local/teste;
- Biome mantido como complemento opcional.

### Guardrails aprendidos

- lockfile/package manager devem ser reproduzíveis entre desenvolvimento e CI;
- CI deve usar instalação limpa (`npm ci` ou equivalente), não mascarar inconsistências com instalação permissiva;
- typecheck/testes não podem depender silenciosamente de artefatos gerados previamente;
- operações destrutivas relevantes devem ter proteção de domínio e teste E2E quando apropriado;
- código vindo de registry deve ser auditado e módulos/dependências não usados removidos.

### Próxima fase

Gerar um starter `web-admin` limpo a partir do perfil validado e provar a Factory criando um segundo aplicativo do zero. O piloto V0.3 permanece como evidência, não como template copiado cegamente.

## 0.3-web-admin-pilot — 2026-08-21

Piloto real de aplicação administrativa da App Factory.

### Validado

- aplicação Next/React/TypeScript com Tailwind e shadcn;
- Better Auth + Drizzle + SQLite local;
- Zod, Vitest e Playwright;
- Data Grid real do ReUI;
- autenticação, CRUD, busca, filtros, desativação, reativação e exclusão segura;
- desktop/mobile e persistência após reload;
- CI reproduzível em checkout limpo;
- audit sem vulnerabilidades high/critical no gate;
- revisão ChatGPT após execução Codex.

### Aprendizados

- ReUI agrega valor em componentes avançados, mas exige auditoria pós-registry;
- SQLite não deve virar default universal de produção;
- Biome não substituiu o lint específico do Next neste piloto;
- teste local isolado não provou reprodutibilidade: o GitHub CI encontrou lockfile inconsistente e dependência do typecheck em `.next`, ambos corrigidos antes do merge.

## 0.2.1-alpha — 2026-08-21

Ativação automática da App Factory por intenção de software.

### Criado

- `core/ENTRYPOINT.md` com contrato de entrada universal;
- Skill `factory-router` para pedidos como criar, melhorar, corrigir, automatizar ou continuar software sem exigir a frase "use a App Factory";
- `templates/project/AGENTS.md` para novos projetos manterem vínculo explícito com a Factory;
- plugin Codex atualizado para anunciar roteamento automático;
- validador estrutural passa a exigir o entrypoint, router e template de handoff.

### Experiência desejada

Um pedido simples como `Quero criar um sistema de patrimônio para a escola` deve ser suficiente para classificar o trabalho, escolher profundidade, carregar Skills, decidir ChatGPT/Codex e iniciar o maior bloco seguro possível.

## 0.2-research — 2026-08-21

Pesquisa estruturada e validação do primeiro adaptador real da App Factory.

### Pesquisa

- triagem de 58 repositórios e ferramentas;
- classificação ADOTAR / INSPIRAR / DESCARTAR;
- shortlist P0/P1/P2;
- confirmação inicial de shadcn + ReUI como eixo candidato do perfil `web-admin`;
- HeroUI mantido como perfil alternativo;
- Better Auth + Drizzle + Zod definidos como candidatos de piloto;
- Playwright definido como forte candidato E2E;
- Spec Kit incorporado como referência para fluxo spec-driven proporcional à escala.

### Arquitetura

- criado `core/PROJECT_SCALE.md` com perfis XS/S/M/L;
- Core continua portátil e neutro;
- adaptadores específicos ficam fora do núcleo;
- starter `web-admin` passa a ser componível, sem auth/banco/observabilidade/monorepo obrigatórios;
- Agent Skills passam a ter validador dedicado.

### Codex Plugin

- `openai/skills` removido como fonte atual e `openai/plugins` adotado como referência;
- criada camada `.codex-plugin/plugin.json`;
- criado marketplace repo-local apontando para a própria raiz;
- criado `scripts/validate_plugin.py`;
- CI passou a validar estrutura, Skills e plugin;
- Issue #3 executou piloto real no Codex CLI `0.149.0`;
- 10 Skills foram descobertas e 4 exercitadas em smoke test;
- hashes origem/cache das Skills exercitadas foram idênticos;
- nenhuma duplicação de `skills/` ou `core/` foi necessária.

## 0.1-bootstrap — 2026-08-20

Primeiro bootstrap da App Factory.

### Criado

- mapa `AGENTS.md`;
- princípios centrais;
- política de interação humano/agente;
- roteador ChatGPT/Codex;
- workflow universal;
- modelo de risco;
- Definition of Done;
- portabilidade entre agentes;
- 10 Skills iniciais;
- templates de produto, arquitetura e estado;
- política UI shadcn/ReUI/HeroUI;
- políticas de Git e dependências;
- plano de pesquisa de 30–50 repositórios;
- camada futura Registry/MCP;
- estratégia de starters;
- validador estrutural em Python;
- template de GitHub Actions;
- registro formal de decisões.

### Origem

Esta versão consolida decisões das conversas de planejamento e filtra os princípios úteis da pasta histórica `Boas práticas/`.
