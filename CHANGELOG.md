# Changelog

## 0.2-research — 2026-08-21

Pesquisa estruturada e validação do primeiro adaptador real da App Factory.

### Pesquisa

- triagem de 58 repositórios e ferramentas;
- classificação ADOTAR / INSPIRAR / DESCARTAR;
- shortlist P0/P1/P2;
- confirmação de shadcn + ReUI como eixo preferencial do perfil `web-admin`;
- HeroUI mantido como perfil alternativo;
- Better Auth + Drizzle + Zod definidos como candidatos de piloto, não defaults universais;
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

### Próxima fase

V0.3: piloto `web-admin` da Issue #4 para validar a stack candidata em aplicação real antes de promover defaults da V1.

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

### Próxima fase

V0.2: pesquisa estruturada de referências externas antes de congelar o primeiro starter.