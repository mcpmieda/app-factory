# App Factory

Sistema portátil para construir e manter aplicações com agentes de IA de forma consistente, verificável e com mínimo trabalho manual do usuário.

## Objetivo

Transformar uma ideia em software funcional usando um método reutilizável que possa ser seguido por ChatGPT, Codex, Claude Code, Cursor ou outro agente compatível.

A App Factory não é um prompt gigante. Ela combina:

- entrada universal por intenção de software;
- seleção automática de perfil validado quando aplicável;
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

## Experiência desejada

O usuário pode começar somente com o resultado, por exemplo:

> Quero criar um sistema de patrimônio para a escola.

Ele não precisa dizer "use a App Factory", escolher framework, descobrir Skills, selecionar perfil ou decidir sozinho entre ChatGPT e Codex.

A Factory deve reconhecer a intenção, entender o produto, classificar escala/risco, selecionar um perfil já validado quando existir e fazer as escolhas técnicas rotineiras por evidência.

Para o exemplo de patrimônio, o roteador pode reconhecer o perfil `web-admin` e usar seus defaults comprovados, ativando autenticação, banco ou ReUI somente se o produto realmente precisar.

## Princípio central

A IA deve trabalhar para atingir o objetivo do usuário, não apenas obedecer literalmente ao pedido. Deve fazer sozinha tudo que puder com segurança, reduzir cliques e conhecimento técnico exigido do usuário, recomendar caminhos melhores quando existirem e pedir intervenção humana somente quando houver decisão de negócio, preferência subjetiva, autorização de risco ou dado realmente indisponível.

## Comece por aqui

1. `AGENTS.md` — mapa para agentes.
2. `core/ENTRYPOINT.md` — ativação automática por intenção e seleção de perfil.
3. `skills/factory-router/SKILL.md` — roteador universal.
4. `profiles/README.md` — perfis validados por classe de software.
5. `profiles/web-admin/PROFILE.md` — primeiro perfil validado.
6. `APP_FACTORY_PLAN.md` — visão, fases e decisões.
7. `core/PRINCIPLES.md` — princípios universais.
8. `core/HUMAN_INTERACTION.md` — o que a IA faz sozinha e o que depende do usuário.
9. `core/PROJECT_SCALE.md` — profundidade XS/S/M/L.
10. `core/TASK_ROUTER.md` — quando usar ChatGPT, Codex ou outro agente.
11. `core/WORKFLOW.md` — ciclo de projeto novo e manutenção.
12. `core/DEFINITION_OF_DONE.md` — como provar que terminou.
13. `PORTABILITY.md` — continuidade entre agentes.
14. `docs/CODEX_PLUGIN.md` — adaptador Codex validado em piloto.

## Perfis

### web-admin — validado V0.4

Para sistemas administrativos, CRUDs, dashboards e ferramentas internas.

Base comprovada:

- TypeScript;
- Next.js App Router;
- React;
- Tailwind;
- shadcn como base visual;
- Zod;
- Vitest;
- Playwright;
- ESLint/configuração oficial do Next.

Módulos condicionais comprovados:

- Better Auth quando identidade/login forem necessários;
- Drizzle quando houver persistência própria;
- ReUI seletivo para componentes avançados;
- SQLite/better-sqlite3 apenas como alternativa local/teste;
- Biome opcional/complementar.

O perfil completo está em `profiles/web-admin/PROFILE.md`.

## Estrutura atual

```text
app-factory/
├── AGENTS.md
├── APP_FACTORY_PLAN.md
├── PORTABILITY.md
├── .codex-plugin/
├── .agents/plugins/
├── core/
├── skills/
├── profiles/
│   └── web-admin/
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

- A intenção de criar/evoluir software aciona a Factory sem palavra-chave manual.
- A Factory pode selecionar um perfil validado automaticamente depois de entender o produto.
- Perfil não é dogma: requisitos locais têm precedência e módulos opcionais só entram quando necessários.
- GitHub é a fonte técnica de verdade.
- Novos projetos recebem um `AGENTS.md` que aponta para a Factory sem duplicar todo o Core.
- A Factory orienta quando usar ChatGPT e quando usar Codex.
- ChatGPT é preferido para produto, pesquisa, arquitetura conceitual, documentação e revisão.
- Codex é preferido para execução local, múltiplos arquivos, terminal, dependências, testes, build, navegador, debugging e migrations.
- A Factory minimiza trabalho manual do usuário e toma decisões técnicas rotineiras autonomamente.
- A profundidade do processo cresce com escala e risco.
- No perfil `web-admin`, shadcn é a base e ReUI é seletivo por componente.
- HeroUI continua perfil visual alternativo, não mistura automática.
- Pesquisar e reutilizar antes de construir do zero.
- Escopo fechado significa fatia funcional verificável, não microtarefas.
- Baseline/diff/rollback continuam centrais para manutenção de sistemas existentes.
- Regras fortes devem virar testes, scripts ou CI quando isso reduzir risco.
- O núcleo permanece portátil entre agentes.
- A integração Codex foi validada como plugin fino, reutilizando as mesmas Skills sem duplicação.
- Teste local não substitui instalação limpa e CI reproduzível.

## Estado

Versão de trabalho: `0.5-web-admin-starter`

O perfil V0.4 agora possui starter real, gerador e recipes condicionais. A V0.5 também inclui um segundo app de patrimônio escolar fictício criado pelo gerador; a revisão do draft PR e dos gates reproduzíveis ainda precede qualquer declaração de V1 estável.
