# Changelog

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
- CI deve usar instalação limpa (`npm ci` ou equivalente), não mascarar inconsistência com instalação permissiva;
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