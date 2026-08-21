# App Factory

Sistema portátil para construir e manter aplicações com agentes de IA de forma consistente, verificável e com mínimo trabalho manual do usuário.

## Objetivo

Transformar uma ideia em software funcional usando um método reutilizável que possa ser seguido por ChatGPT, Codex, Claude Code, Cursor ou outro agente compatível.

A App Factory não é um prompt gigante. Ela combina:

- `AGENTS.md` como mapa operacional;
- Core curto e modular;
- Skills especializadas carregadas conforme a tarefa;
- profundidade proporcional por escala XS/S/M/L;
- templates e starters componíveis;
- políticas de UI, dependências e Git;
- roteamento entre ChatGPT, Codex e outros agentes;
- verificações automáticas e definição objetiva de pronto;
- adaptadores finos por agente;
- GitHub como fonte de verdade para continuidade.

## Princípio central

A IA deve trabalhar para atingir o objetivo do usuário, não apenas obedecer literalmente ao pedido. Deve fazer sozinha tudo que puder com segurança, reduzir cliques e conhecimento técnico exigido do usuário, recomendar caminhos melhores quando existirem e pedir intervenção humana somente quando houver decisão de negócio, preferência subjetiva, autorização de risco ou dado realmente indisponível.

## Comece por aqui

1. `AGENTS.md` — mapa para agentes.
2. `APP_FACTORY_PLAN.md` — visão, fases e decisões já tomadas.
3. `core/PRINCIPLES.md` — princípios universais.
4. `core/HUMAN_INTERACTION.md` — o que a IA faz sozinha e o que depende do usuário.
5. `core/PROJECT_SCALE.md` — profundidade XS/S/M/L.
6. `core/TASK_ROUTER.md` — quando usar ChatGPT, Codex ou outro agente.
7. `core/WORKFLOW.md` — ciclo de projeto novo e manutenção.
8. `core/DEFINITION_OF_DONE.md` — como provar que terminou.
9. `PORTABILITY.md` — continuidade entre agentes.
10. `docs/CODEX_PLUGIN.md` — adaptador Codex validado em piloto.

## Estrutura atual

```text
app-factory/
├── AGENTS.md
├── APP_FACTORY_PLAN.md
├── PORTABILITY.md
├── .codex-plugin/
│   └── plugin.json
├── .agents/plugins/
│   └── marketplace.json
├── core/
│   ├── PRINCIPLES.md
│   ├── HUMAN_INTERACTION.md
│   ├── PROJECT_SCALE.md
│   ├── TASK_ROUTER.md
│   ├── WORKFLOW.md
│   ├── RISK_MODEL.md
│   └── DEFINITION_OF_DONE.md
├── skills/
│   ├── app-planner/
│   ├── architecture/
│   ├── tool-router/
│   ├── ui-builder/
│   ├── maintenance/
│   ├── database/
│   ├── debugging/
│   ├── security-review/
│   ├── verification/
│   └── deployment/
├── policies/
├── templates/
├── starters/
│   └── web-admin/
├── ui/
├── registry/
├── pilots/
│   └── web-admin/
├── research/
└── scripts/
```

## Decisões consolidadas

- GitHub é a fonte técnica de verdade.
- A Factory orienta o usuário sobre quando usar ChatGPT e quando usar Codex.
- ChatGPT é preferido para produto, pesquisa, arquitetura conceitual, documentação e revisão.
- Codex é preferido para execução local, múltiplos arquivos, terminal, dependências, testes, build, navegador, debugging e migrations.
- A Factory minimiza trabalho manual do usuário e toma decisões técnicas rotineiras autonomamente.
- A profundidade do processo cresce com escala e risco; projeto pequeno não recebe ritual de sistema crítico.
- Sistemas administrativos avaliam primeiro shadcn + ReUI; HeroUI é perfil alternativo, não mistura obrigatória.
- Pesquisar e reutilizar antes de construir do zero.
- Escopo fechado significa fatia funcional verificável, não microtarefas.
- Baseline/diff/rollback continuam centrais para manutenção de sistemas existentes.
- Regras fortes devem virar testes, scripts ou CI quando isso reduzir risco de forma concreta.
- O núcleo permanece portátil entre agentes.
- A integração Codex foi validada como plugin fino, reutilizando as mesmas Skills sem duplicação.

## Estado

Versão de trabalho: `0.3-web-admin-pilot`

A pesquisa avaliou 58 referências, o adaptador Codex passou por piloto real e o piloto `web-admin` da Issue #4 foi implementado com autenticação, banco, CRUD, testes e evidência de navegador. O experimento aguarda revisão em draft PR antes de qualquer promoção de defaults da V1.
