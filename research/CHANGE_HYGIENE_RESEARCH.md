# Change Hygiene Research

## Pergunta

Como a App Factory deve editar/revisar sistemas existentes sem acumular patches, código morto, CSS em camadas, implementações paralelas e artefatos temporários — inclusive quando o sistema foi criado fora da Factory?

## Conclusão

A regra mais forte encontrada não é simplesmente "faça cleanup": é tratar **code health como critério de aprovação da mudança**, mantendo o escopo focado e usando automação apenas para sinais objetivos.

A arquitetura adotada combina:

1. **net code health** na área tocada;
2. **replace, don't shadow** para implementação substituída;
3. **consolidation pass** obrigatório após repair loops;
4. exceção explícita para compatibilidade temporária;
5. ferramentas condicionais para dead code/CSS/duplication;
6. scanner stdlib-first com blockers objetivos e heurísticas advisory.

## Fontes fortes

### Google Engineering Practices

- Code Review Standard: https://google.github.io/eng-practices/review/reviewer/standard.html
- What to look for: https://google.github.io/eng-practices/review/reviewer/looking-for.html
- Small CLs: https://google.github.io/eng-practices/review/developer/small-cls.html

Pontos adotados:

- a mudança deve melhorar, ou no mínimo não degradar, a saúde geral do código;
- pequenas complexidades acumuladas também deterioram sistemas;
- mudanças devem ser autocontidas e manter o sistema funcionando;
- refactors estruturais maiores devem, quando possível, ser separados de feature/bugfix;
- testes devem acompanhar mudanças e refactors;
- deletar arquivos inteiros não deve ser desencorajado por métricas simplistas de tamanho do diff.

### Chromium

- Firmware code review guidelines: https://www.chromium.org/chromium-os/developer-library/guides/code-review/firmware-code-reviews/
- Submitting code best practices: https://www.chromium.org/chromium-os/developer-library/guides/code-review/code-reviews-and-submitting-code/

Pontos adotados:

- um logical change por revisão sempre que possível;
- refactor separado de mudança funcional quando o acoplamento dificultar revisão;
- regressão deve ganhar teste reproduzível;
- rollback/revert é ferramenta válida; não continuar acumulando patch apenas porque já houve tentativa anterior.

### Microsoft Engineering Fundamentals Playbook

- Maintainability: https://microsoft.github.io/code-with-engineering-playbook/non-functional-requirements/maintainability/
- Reviewer guidance: https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/

Pontos adotados:

- maintainability envolve modularidade, legibilidade, testabilidade e gestão de dependências;
- revisão humana deve olhar design/manutenibilidade, enquanto linters automatizam erros mecânicos;
- refactoring regular é parte da manutenção, não atividade excepcional.

## Ferramentas avaliadas

### ESLint

Fonte: https://eslint.org/docs/latest/rules/

Adequado como primeira linha JS/TS para:

- unused variables;
- unreachable code;
- duplicate class members/imports/conditions;
- useless assignments e outros erros objetivos.

Decisão: **reutilizar o lint existente**; não instalar um segundo linter equivalente apenas por Change Hygiene.

### Knip

- https://github.com/webpro-nl/knip
- https://knip.dev/typescript/unused-exports
- https://knip.dev/overview/first-cleanup

Cobertura diferente de ESLint:

- arquivos não usados;
- exports não usados;
- dependencies/devDependencies não usadas;
- análise do grafo do projeto.

Decisão: default recomendado para dead-code de JS/TS quando o projeto puder ser modelado. Se já estiver configurado, o agente deve executá-lo ao consolidar manutenção/refactor relevante. Se não estiver, permanece condicional; não instalar em todo projeto simples.

Motivo de cautela: entradas dinâmicas/frameworks podem exigir configuração e produzir falso positivo se o grafo não estiver descrito corretamente.

### Stylelint

Fonte: https://stylelint.io/user-guide/rules/

Regras úteis:

- `no-duplicate-selectors`;
- `declaration-block-no-duplicate-properties`;
- `no-descending-specificity`;
- `declaration-no-important` quando a política do projeto permitir;
- limites de specificity quando houver design CSS compatível.

Decisão: usar quando CSS é material e Stylelint já faz parte/é justificado pela stack. `!important` novo vira sinal de revisão, não falha universal: reset, third-party CSS e accessibility podem ter justificativas reais.

### Ruff / Vulture

- https://docs.astral.sh/ruff/rules/unused-import/
- https://docs.astral.sh/ruff/rules/unused-variable/
- https://github.com/jendrikseipp/vulture

Decisão:

- Ruff/Pyflakes é primeira linha Python para imports/vars inúteis;
- Vulture complementa para dead functions/classes/unreachable, mas Python dinâmico pode gerar falso positivo;
- quando usado como gate novo, preferir configuração explícita/alta confiança em vez de deletar automaticamente tudo que reportar.

### jscpd

- https://github.com/kucherenko/jscpd
- https://github.com/kucherenko/jscpd/blob/master/docs/ci-and-hooks.md

Ponto forte: detecta copy/paste em muitas linguagens e suporta threshold/CI.

Decisão: **não adotar threshold universal de duplicação**. Um percentual global pode incentivar abstração prematura ou penalizar duplicação intencional. Use como hotspot/advisory ou gate somente quando o projeto possuir baseline/configuração estável e o delta for material.

## Ideias rejeitadas

### "Todo `!important` deve falhar"

Rejeitado. É sinal forte de cascade debt, mas existem usos legítimos. O scanner marca novo `!important` como advisory e Stylelint pode torná-lo gate por política do projeto.

### "Qualquer arquivo `v2` deve ser proibido"

Rejeitado. Versionamento pode ser requisito real. Só há advisory quando uma cópia com sufixo `old/new/fixed/final/copy/v2` coexiste com um irmão-base plausível.

### "Rodar Knip/Vulture/jscpd/Stylelint em todo sistema"

Rejeitado. Ferramentas têm pré-condições e falsos positivos. A Factory continua proporcional.

### "Refatorar todo legado antes de editar"

Rejeitado. Isso aumenta risco e escopo. Em sistema externo, primeiro preserve baseline e reduza dívida diretamente ligada à área tocada; não use a manutenção solicitada como justificativa para reescrita global.

### "Preservar implementação antiga para reduzir risco"

Rejeitado como regra geral. Preservar **comportamento** é essencial; preservar código obsoleto pode aumentar risco. Dupla implementação só permanece com compatibilidade real, condição de remoção e testes de transição.

## Arquitetura resultante

`core/CHANGE_HYGIENE.md` é um contrato transversal, não uma nova fase nem nova Skill.

Fluxo de manutenção:

```text
baseline
  ↓
caracterizar comportamento
  ↓
implementar/refatorar
  ↓
verificar
  ↓
repair loop limitado (se necessário)
  ↓
CONSOLIDAR
  ├─ remover tentativas descartadas
  ├─ remover código morto/orfandade
  ├─ eliminar shadow implementations
  ├─ revisar suppressions/overrides
  └─ remover temporários
  ↓
verificar novamente
  ↓
review/delivery
```

O scanner `scripts/change_hygiene.py` é deliberadamente conservador:

- blocker: conflict marker e arquivo temporário/backup rastreado;
- advisory: possível shadow-copy, nova suppression, `!important` adicionado e dívida temporária marcada;
- tooling detection: mostra ferramentas já disponíveis sem instalar nada automaticamente.

## Regra final

A versão entregue deve parecer **a implementação que escolheríamos se já soubéssemos qual solução funcionaria**, e não um registro de todas as tentativas necessárias para descobri-la. O histórico de tentativas pertence ao Git/PR; a árvore final pertence ao produto.
