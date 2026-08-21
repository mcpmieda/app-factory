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
- políticas de UI, **Living UI / Semantic Motion**, dependências e Git;
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

Interfaces recebem também um **Motion Profile** independente do design system. O default contextual é `ambient`: movimento vivo e semântico quando ajuda, atenuado automaticamente em leitura longa, telas densas, acessibilidade ou desempenho limitado.

## Princípio central

A IA deve trabalhar para atingir o objetivo do usuário, não apenas obedecer literalmente ao pedido. Deve fazer sozinha tudo que puder com segurança, reduzir cliques e conhecimento técnico exigido do usuário, recomendar caminhos melhores quando existirem e pedir intervenção humana somente quando houver decisão de negócio, preferência subjetiva, autorização de risco ou dado realmente indisponível.

## Comece por aqui

Para usar no Codex 0.149 a partir de um checkout limpo:

```text
codex --enable plugins plugin marketplace add <raiz-do-app-factory>
codex --enable plugins plugin add app-factory@app-factory-local
```

Depois, basta descrever o software em linguagem comum — por exemplo, `Quero criar um sistema simples para controlar empréstimos`. A palavra “App Factory” não é necessária. Para gerar diretamente o baseline administrativo validado, use `node scripts/create-web-admin.mjs <destino> <nome> [--recipe <id>]`.

1. `AGENTS.md` — mapa para agentes.
2. `core/ENTRYPOINT.md` — ativação automática por intenção e seleção de perfil.
3. `skills/factory-router/SKILL.md` — roteador universal.
4. `profiles/README.md` — perfis validados por classe de software.
5. `profiles/*/PROFILE.md` — defaults condicionais comprovados por família.
6. `ui/UI_POLICY.md` — seleção e consistência de interface.
7. `ui/MOTION_POLICY.md` — Living UI / Semantic Motion independente de framework.
8. `APP_FACTORY_PLAN.md` — visão, fases e decisões.
9. `core/PRINCIPLES.md` — princípios universais.
10. `core/HUMAN_INTERACTION.md` — o que a IA faz sozinha e o que depende do usuário.
11. `core/PROJECT_SCALE.md` — profundidade XS/S/M/L.
12. `core/TASK_ROUTER.md` — quando usar ChatGPT, Codex ou outro agente.
13. `core/WORKFLOW.md` — ciclo de projeto novo e manutenção.
14. `core/DEFINITION_OF_DONE.md` — como provar que terminou.
15. `PORTABILITY.md` — continuidade entre agentes.
16. `docs/CODEX_PLUGIN.md` — adaptador Codex validado em piloto e auditoria final.

## Living UI / Semantic Motion

O design system e o movimento são decisões separadas.

Um projeto pode usar HeroUI, shadcn, ReUI, componentes próprios ou outro kit e ainda seguir a mesma linguagem de movimento da Factory.

Motion Profiles:

- `none` — sem movimento não essencial;
- `subtle` — microinterações/transições discretas;
- `ambient` — **default contextual**: microinterações, feedback semântico e atmosfera viva onde apropriado;
- `expressive` — motion mais presente quando faz parte da identidade/experiência.

A política cobre seis funções: ambiente, interação, dados, estado, atenção e navegação. `prefers-reduced-motion` é obrigatório para movimento não essencial. Ações importantes podem receber atenção temporária; gráficos podem animar mudanças reais; animação que não ajuda a compreender ou usar a interface deve ser removida.

## Perfis

### web-admin — V1 estável (`v1`)

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
- PostgreSQL como caminho de produção validado por recipe, migrations e CI efêmero;
- Biome opcional/complementar.

O perfil herda `Motion Profile: ambient`, reduzindo para comportamento `subtle` em tabelas e telas muito densas quando necessário.

O perfil completo está em `profiles/web-admin/PROFILE.md`.

### Perfis universais (`validated`)

`website`, `web-app`, `chrome-extension` e `automation` possuem um piloto completo e gates próprios. Os perfis registram contratos condicionais; Astro, Vite/React, Vite vanilla e Python foram adequados aos pilotos, mas não são stacks universais congeladas. Veja `research/V0.9_UNIVERSAL_VALIDATION.md`.

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
│   ├── web-admin/
│   ├── website/
│   ├── web-app/
│   ├── chrome-extension/
│   └── automation/
├── policies/
├── templates/
├── starters/
│   └── web-admin/
├── ui/
│   ├── UI_POLICY.md
│   └── MOTION_POLICY.md
├── registry/
├── pilots/
│   └── web-admin/
├── examples/
│   ├── website-pilot/
│   ├── web-app-pilot/
│   ├── chrome-extension-pilot/
│   └── automation-pilot/
├── audits/
│   └── v1-final/
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
- Living UI / Semantic Motion é transversal e não depende do design system.
- `ambient` é o Motion Profile default contextual, com atenuação automática quando o contexto pede sobriedade, foco, desempenho ou acessibilidade.
- Pesquisar e reutilizar antes de construir do zero.
- Escopo fechado significa fatia funcional verificável, não microtarefas.
- Baseline/diff/rollback continuam centrais para manutenção de sistemas existentes.
- Regras fortes devem virar testes, scripts ou CI quando isso reduzir risco.
- O núcleo permanece portátil entre agentes.
- A integração Codex foi validada como plugin fino, reutilizando as mesmas Skills sem duplicação.
- Teste local não substitui instalação limpa e CI reproduzível.

## Estado

Versão estável: **`1.0.0` — App Factory V1.0**.

A auditoria final comprovou bootstrap isolado do plugin, roteamento por pedido comum, criação real de um novo sistema do zero, persistência e regras de negócio, desktop/mobile/reduced-motion, continuidade por segundo agente sem contexto e recuperação após regressão controlada. O perfil `web-admin` está em `v1`; os perfis `website`, `web-app`, `chrome-extension` e `automation` permanecem `validated` até acumularem mais evidência.

Escopos ainda não validados — como mobile nativo, desktop nativo, jogos e infraestrutura cloud complexa — ficam para versões posteriores e não são promessa da V1.0.
