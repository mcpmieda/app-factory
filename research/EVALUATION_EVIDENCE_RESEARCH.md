# Evaluation & Evidence Hardening Research

Data: 2026-08-23

## Pergunta

Como melhorar três lacunas reais da App Factory — conformidade de agentes, cobertura dos engines Python e evidência de uso/roteamento de Skills — sem criar dependência de uma segunda IA, SaaS obrigatório ou telemetria invasiva?

## Conclusão

A melhor arquitetura não é um único "agent harness" nem um badge de coverage. A solução adotada separa três problemas:

1. **Agent Conformance Corpus + scorer determinístico** — cenários versionados, executor de referência e scorer que avalia o worktree/artefatos. Agentes reais podem ser plugados depois sem mudar o contrato.
2. **Python Evidence Gate** — `coverage.py` com branch coverage para visibilidade e `diff-cover` para exigir cobertura das linhas novas/modificadas dos engines, sem impor uma meta arbitrária ao legado inteiro.
3. **Skill Routing Telemetry** — contadores locais agregados de Skills selecionadas, separados do Learning Engine que escolhe backends. Não tenta fingir que observa se um modelo "leu" Markdown.

Nenhuma dessas camadas cria uma nova Skill.

---

## 1. Agent Conformance

### SWE-bench

Referências:

- https://github.com/SWE-bench/SWE-bench
- https://github.com/SWE-bench/SWE-bench/blob/main/docs/reference/harness.md
- https://github.com/SWE-bench/experiments

Padrões úteis:

- tarefa/caso é separado do executor;
- ambiente é reproduzível;
- patch/output é avaliado por um harness, não por afirmação do agente;
- o próprio "gold"/referência pode ser executado para verificar que o benchmark é válido;
- logs/resultados são artefatos separados do score.

O harness oficial é pesado para a Factory (Docker/SWE-bench completo), então **não foi incorporado como dependência**. Foi adotada a arquitetura conceitual: corpus + referência + scorer.

### Inspect AI — UK AI Security Institute

Referências:

- https://inspect.aisi.org.uk/
- https://inspect.aisi.org.uk/tutorial.html
- https://inspect.aisi.org.uk/multiple-scorers.html
- https://github.com/UKGovernmentBEIS/inspect_ai

Padrões úteis:

- agent evals são tarefas com solver/agente, tools, sandbox e scorers separados;
- scorer pode inspecionar diretamente arquivos do sandbox;
- suporta agentes externos/coding agents, portanto o corpus pode futuramente rodar Codex/Claude/Gemini sem o Core depender de um deles;
- múltiplos scorers permitem separar sucesso funcional de findings auxiliares.

Decisão: **INSPIRAR/INTEROPERAR**, não instalar Inspect AI em todo PR. O CI normal valida o corpus e roda um executor de referência stdlib. Uma avaliação periódica com agente real pode consumir o mesmo corpus em Inspect AI ou executor equivalente.

### Regra epistemológica

O conformance scorer não avalia chain-of-thought. Ele avalia apenas estado observável do worktree:

- artefatos obrigatórios;
- validade dos contratos;
- rastreabilidade;
- gates declarados executáveis;
- freshness/review quando o caso exigir;
- ausência de artefatos que provariam over-process em caso deliberadamente leve.

Isso evita depender de raciocínio privado ou de o agente "dizer que seguiu" a Factory.

### Auditabilidade do corpus

Cada caso precisa:

- ID estável;
- prompt de tarefa;
- ações de referência allowlisted, sem shell arbitrário;
- assertions determinísticas;
- pelo menos uma assertion de comportamento/contrato, não apenas `file_exists`.

O executor de referência é o equivalente local do "gold validation": se ele deixar de passar, o caso/scorer está quebrado e não pode ser usado para medir agentes.

---

## 2. Python coverage

### coverage.py

Referência:

- https://coverage.readthedocs.io/
- https://pypi.org/project/coverage/

Versão pesquisada/adotada no CI: `7.15.3` (2026-08-02).

Uso:

- branch coverage habilitada;
- fonte de cobertura limitada a `engine/`;
- relatório de linhas/branches permanece evidência, não "percentual de correção".

### diff-cover

Referências:

- https://github.com/Bachmann1234/diff_cover
- https://pypi.org/project/diff-cover/

Versão pesquisada/adotada no CI: `10.5.0` (2026-08-08).

O projeto define diff coverage como cobertura das linhas novas/modificadas e recomenda a ideia de responsabilidade sobre linhas tocadas. A Factory adota um gate forte **somente para linhas executáveis novas/modificadas dos engines**.

### Política adotada

- cobertura total/branch: reportada, sem badge de vaidade e sem meta universal;
- diff line coverage de `engine/*.py`: **100% no código novo/modificado**;
- o gate não exige que dívida histórica inteira chegue a 100%;
- exceções devem ser explícitas no código (`pragma`) e justificáveis em revisão, nunca redução silenciosa do threshold;
- sem Codecov/SaaS obrigatório; relatórios ficam em GitHub Actions artifacts/summary.

Motivo: o Core determinístico é pequeno o suficiente para exigir que lógica nova seja exercitada, enquanto a cobertura global continua uma métrica diagnóstica e não uma afirmação de maturidade.

---

## 3. Skill Routing Telemetry

### OpenTelemetry — princípios adotados

Referências:

- https://opentelemetry.io/docs/security/handling-sensitive-data/
- https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/
- https://opentelemetry.io/docs/concepts/signals/metrics/
- https://opentelemetry.io/blog/2026/cardinality-limits-in-opentelemetry/

Padrões úteis:

- minimização de dados: coletar apenas o necessário;
- atributos potencialmente sensíveis ou caros não devem ser default;
- evitar alta cardinalidade em métricas;
- enums/sets curtos e estáveis são preferíveis quando o domínio é conhecido.

### O que a Factory consegue observar de verdade

Um repositório Markdown não consegue provar que um modelo "leu" ou cognitivamente usou uma Skill. Portanto o nome correto é **Skill Routing Telemetry**: registrar somente Skills que o roteamento declarou/selecionou.

### Formato adotado

Arquivo local ignorado pelo Git:

`.factory/skill-routing.json`

Contém apenas agregados:

- quantidade de decisões registradas;
- contagem de seleção por slug de Skill instalado;
- contagem por origem allowlisted (`factory-router`, `app-planner`, `manual`);
- `updated_at` global.

Não contém:

- prompt;
- objetivo/tarefa;
- código;
- nomes pessoais;
- arquivos;
- logs;
- URLs;
- tokens;
- sequência individual de eventos;
- telemetria externa.

A lista de Skills válidas vem de `skills/*/SKILL.md`, limitando cardinalidade ao catálogo instalado.

### Separação do Learning Engine

Skill Routing **não alimenta** automaticamente `recommend_backend()` e não autoriza remover Skills. Frequência baixa pode indicar oportunidade de revisão, mas não prova inutilidade: recovery/security/formalização podem ser raras e ainda essenciais.

---

## Itens pesquisados e não adotados como default

### Codecov

Útil para UI/PR comments e patch coverage, mas introduzir SaaS não é necessário para o objetivo atual. `coverage.py + diff-cover` resolvem o gate local/CI.

### SWE-bench completo

Excelente benchmark de coding agents, mas seus requisitos de Docker/storage/CPU seriam excesso para validar contratos internos da Factory em todo PR.

### Inspect AI obrigatório

Excelente framework e candidato para avaliações periódicas de agentes reais, mas torná-lo dependência de cada PR reduziria portabilidade e exigiria modelo/provider. O corpus foi desenhado para interoperar sem esse acoplamento.

### Telemetria OpenTelemetry completa

Não é necessária. A Factory aproveita os princípios de minimização/cardinalidade, mantendo JSON local stdlib e sem collector/backend.

---

## Arquitetura final

```text
PR normal
  ├─ validators existentes
  ├─ Agent Conformance corpus audit
  │    └─ executor de referência → scorer de worktree
  └─ Python Evidence
       ├─ branch coverage report
       └─ diff coverage gate para engine novo/modificado

execução real de projeto
  └─ roteamento de Skills
       └─ agregado local .factory/skill-routing.json

avaliação periódica/opcional
  └─ agente real (Inspect AI/executor equivalente)
       └─ mesmo corpus + mesmo scorer de worktree
```

Essa arquitetura aumenta evidência sem transformar avaliação, coverage ou telemetria em autoridades maiores que os contratos e o Definition of Done.
