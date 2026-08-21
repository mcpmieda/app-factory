# App Factory

Sistema portátil para construir e manter aplicações com agentes de IA de forma consistente, verificável e com mínimo trabalho manual do usuário.

## Objetivo

Transformar uma ideia em software funcional usando um método reutilizável que possa ser seguido por ChatGPT, Codex, Claude Code, Cursor ou outro agente compatível.

A App Factory não é um prompt gigante. Ela combina:

- entrada universal por intenção de software;
- **Context Engine incremental** para recuperar repositórios sem releitura integral desnecessária;
- **Autonomy Engine** para calcular e registrar o próximo passo técnico;
- seleção automática de perfil validado quando aplicável;
- `AGENTS.md` como mapa operacional;
- Core curto e modular;
- 13 Skills especializadas carregadas conforme a tarefa;
- profundidade proporcional por escala XS/S/M/L;
- templates e starters componíveis;
- políticas de UI, **Living UI / Semantic Motion**, dependências e Git;
- roteamento por capacidade, priorizando agente atual + GitHub/CI antes de handoff local;
- verificações automáticas, repair loop limitado e definição objetiva de pronto;
- adaptadores finos por agente;
- GitHub como fonte de verdade para continuidade.

## Experiência desejada

O usuário pode começar somente com o resultado, por exemplo:

> Quero criar um sistema de patrimônio para a escola.

Ele não precisa dizer "use a App Factory", escolher framework, descobrir Skills, selecionar perfil, escolher ChatGPT/Codex ou pedir manualmente cada próxima fase.

A Factory deve reconhecer a intenção, recuperar contexto quando houver projeto existente, entender o produto, classificar escala/risco, selecionar perfil validado, decidir a próxima ação e executar as escolhas técnicas rotineiras por evidência.

Em um projeto existente, a experiência desejada é:

```text
pedido do usuário
→ resume/context
→ next
→ implementar
→ verificar
→ reparar se necessário
→ revisar
→ entregar
```

O usuário só volta ao loop quando existir uma decisão genuinamente humana, dado/credencial indisponível, custo ou risco relevante.

## V1.1 — autonomia executável

### Context Engine

`engine/context_engine.py` cria `.factory/context/repo-map.json` e `SUMMARY.md` com:

- SHA-256 por arquivo e fingerprint global;
- cache incremental de metadados;
- delta `added / changed / removed`;
- stack, manifests, linguagens, símbolos e imports úteis à navegação;
- exclusão padrão de `.env*`, chaves/credenciais, dependências, builds, caches, binários e arquivos grandes.

O mapa é cache de navegação. Arquivos reais e GitHub continuam sendo a autoridade.

### Autonomy Engine

`engine/autonomy_engine.py` mantém `.factory/state.json` e transições entre:

`context → planning → implementation → verification → repair → review → delivery → done`

O repair loop tem limite padrão de 3 tentativas. Ao estagnar, a Factory deve mudar estratégia/executor antes de envolver o usuário. Eventos fora da fase permitida são recusados antes de alterar o estado.

### Roteamento atual

A V1.1 deixou de usar a regra simplista "precisa de testes/build = Codex". A ordem agora é:

1. agente atual + ferramentas disponíveis;
2. GitHub + CI para prova reproduzível;
3. executor leve/sandbox quando disponível;
4. Codex/local quando browser/runtime/debug/migration interativos ou outra capacidade local realmente exigirem.

Definition of Done não é reduzida para economizar executor.

## Comandos internos

O usuário normalmente não precisa executá-los; são a interface portátil entre agentes:

```text
python scripts/factory.py --root <projeto> context
python scripts/factory.py --root <projeto> init --goal "..."
python scripts/factory.py --root <projeto> status
python scripts/factory.py --root <projeto> next
python scripts/factory.py --root <projeto> resume
python scripts/factory.py --root <projeto> record <evento>
```

## Princípio central

A IA deve trabalhar para atingir o objetivo do usuário, não apenas obedecer literalmente ao pedido. Deve fazer sozinha tudo que puder com segurança, reduzir cliques e conhecimento técnico exigido do usuário, recomendar caminhos melhores quando existirem e pedir intervenção humana somente quando houver decisão de negócio, preferência subjetiva, custo, autorização de risco, credencial/dado realmente indisponível ou decisão legal/organizacional.

## Comece por aqui

Para usar como plugin no Codex 0.149 a partir de um checkout limpo:

```text
codex --enable plugins plugin marketplace add <raiz-do-app-factory>
codex --enable plugins plugin add app-factory@app-factory-local
```

Depois basta descrever o software em linguagem comum. A palavra “App Factory” não é necessária.

Para navegar no núcleo:

1. `AGENTS.md` — mapa para agentes.
2. `core/ENTRYPOINT.md` — ativação automática por intenção.
3. `core/CONTEXT_ENGINE.md` — recuperação incremental de repositório.
4. `core/AUTONOMY_ENGINE.md` — estado e próxima ação.
5. `skills/factory-router/SKILL.md` — roteador universal.
6. `core/TASK_ROUTER.md` — roteamento por capacidade/executor.
7. `profiles/README.md` e `profiles/*/PROFILE.md` — defaults condicionais comprovados.
8. `ui/UI_POLICY.md` e `ui/MOTION_POLICY.md` — interface e Living UI.
9. `core/HUMAN_INTERACTION.md` — limites da intervenção humana.
10. `core/DEFINITION_OF_DONE.md` — prova de conclusão.
11. `PORTABILITY.md` — continuidade entre agentes.
12. `docs/CODEX_PLUGIN.md` — adaptador Codex.

## Living UI / Semantic Motion

O design system e o movimento são decisões separadas. Um projeto pode usar HeroUI, shadcn, ReUI, componentes próprios ou outro kit e ainda seguir a mesma linguagem de movimento.

Motion Profiles:

- `none` — sem movimento não essencial;
- `subtle` — microinterações/transições discretas;
- `ambient` — **default contextual**: feedback semântico e atmosfera viva onde apropriado;
- `expressive` — motion mais presente quando faz parte da identidade/experiência.

`prefers-reduced-motion` é obrigatório para movimento não essencial.

## Perfis

### web-admin — V1 estável (`v1`)

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

HeroUI continua uma escolha visual alternativa válida e explícita; não há mistura automática de design systems.

### Perfis universais (`validated`)

`website`, `web-app`, `chrome-extension` e `automation` possuem piloto completo e gates próprios. Seus frameworks de piloto são evidência, não stacks universais congeladas.

## Estrutura atual

```text
app-factory/
├── AGENTS.md
├── PROJECT_STATE.md
├── core/
│   ├── CONTEXT_ENGINE.md
│   └── AUTONOMY_ENGINE.md
├── engine/
│   ├── context_engine.py
│   └── autonomy_engine.py
├── skills/
├── profiles/
├── templates/
├── starters/
├── ui/
├── policies/
├── examples/
├── projects/
├── audits/
├── research/
└── scripts/
    ├── factory.py
    └── validate_v1_1.py
```

## Decisões consolidadas

- intenção de software aciona a Factory sem palavra-chave manual;
- GitHub é a fonte técnica de verdade;
- Context Engine reduz releitura, mas não substitui arquivos reais;
- Autonomy Engine decide continuidade técnica sem o usuário conduzir fases;
- current-agent + GitHub/CI vem antes de handoff quando fornece prova suficiente;
- Codex/local é executor de capacidade, não centro obrigatório da arquitetura;
- falhas entram em repair loop limitado;
- perfil não é dogma: requisitos locais têm precedência;
- Living UI / Semantic Motion é transversal e independente do design system;
- pesquisar e reutilizar antes de construir do zero;
- escopo fechado significa fatia funcional verificável, não microtarefas;
- baseline/diff/rollback continuam centrais para manutenção;
- regras fortes devem virar testes, scripts ou CI quando isso reduzir risco;
- núcleo e estado operacional permanecem portáveis entre agentes;
- teste local não substitui instalação limpa e CI reproduzível.

## Estado

Versão estável: **`1.1.0` — App Factory V1.1**.

A V1.1 preserva toda a evidência da V1.0 e adiciona Context Engine + Autonomy Engine. O gate dedicado comprovou máquina de estados, retomada sem conversa anterior, mudança externa de contexto, limite de reparo e cache incremental. No próprio repositório da Factory, a segunda passagem reutilizou os metadados dos **505 arquivos mapeados** e reprocessou **0**.
