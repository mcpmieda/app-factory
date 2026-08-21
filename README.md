# App Factory

Sistema portátil para construir e manter aplicações com agentes de IA de forma consistente, verificável e com mínimo trabalho manual do usuário.

## Objetivo

Transformar uma ideia em software funcional usando um método reutilizável que possa ser seguido por ChatGPT, Codex, Claude Code, Cursor ou outro agente compatível.

A App Factory não é um prompt gigante. Ela combina:

- `AGENTS.md` como mapa operacional;
- Core curto e modular;
- Skills especializadas carregadas conforme a tarefa;
- templates por tipo de projeto;
- políticas de UI, dependências e Git;
- roteamento entre ChatGPT, Codex e outros agentes;
- verificações automáticas e definição objetiva de pronto;
- GitHub como fonte de verdade para continuidade.

## Princípio central

A IA deve trabalhar para atingir o objetivo do usuário, não apenas obedecer literalmente ao pedido. Deve fazer sozinha tudo que puder com segurança, reduzir cliques e conhecimento técnico exigido do usuário, recomendar caminhos melhores quando existirem e pedir intervenção humana somente quando houver decisão de negócio, preferência subjetiva, autorização de risco ou dado realmente indisponível.

## Comece por aqui

1. `AGENTS.md` — mapa para agentes.
2. `APP_FACTORY_PLAN.md` — visão, fases e decisões já tomadas.
3. `core/PRINCIPLES.md` — princípios universais.
4. `core/HUMAN_INTERACTION.md` — o que a IA faz sozinha e o que depende do usuário.
5. `core/TASK_ROUTER.md` — quando usar ChatGPT, Codex ou outro agente.
6. `core/WORKFLOW.md` — ciclo de projeto novo e manutenção.
7. `core/DEFINITION_OF_DONE.md` — como provar que terminou.
8. `PORTABILITY.md` — continuidade entre agentes.

## Estrutura V0.1

```text
app-factory/
├── AGENTS.md
├── APP_FACTORY_PLAN.md
├── PORTABILITY.md
├── core/
│   ├── PRINCIPLES.md
│   ├── HUMAN_INTERACTION.md
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
│   ├── GIT.md
│   └── DEPENDENCIES.md
├── templates/
│   ├── project/
│   └── github/workflows/
├── starters/
├── ui/
├── registry/
├── research/
└── scripts/
```

## Decisões já consolidadas

- GitHub é a fonte técnica de verdade.
- A Factory deve orientar o usuário sobre quando usar ChatGPT e quando usar Codex.
- ChatGPT é preferido para produto, pesquisa, arquitetura conceitual, documentação e revisão.
- Codex é preferido para execução local, múltiplos arquivos, terminal, dependências, testes, build, navegador, debugging e migrations.
- A Factory deve minimizar trabalho manual do usuário e tomar decisões técnicas rotineiras autonomamente.
- Sistemas administrativos devem avaliar primeiro shadcn + ReUI; HeroUI é alternativa seletiva, não mistura obrigatória.
- Pesquisar e reutilizar antes de construir do zero.
- Escopo fechado significa fatia funcional verificável, não microtarefas.
- Baseline/diff/rollback continuam centrais para manutenção de sistemas existentes.
- Regras fortes devem virar testes, scripts ou CI quando isso reduzir risco de forma concreta.
- O núcleo deve permanecer portátil entre agentes.

## Estado

Versão: `0.1-bootstrap`

A V0.2 executará pesquisa estruturada de referências externas antes de congelar o primeiro starter e a arquitetura V1.