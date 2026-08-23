# Semantic Verification

## Objetivo

A Factory não deve provar apenas que o código compila ou que os testes existentes passam. Para trabalho funcional relevante, ela também precisa provar que a implementação corresponde ao objetivo e às regras acordadas.

## Regra proporcional

Não transformar toda mudança em burocracia pesada.

A especificação semântica é exigida por padrão para:

- funcionalidade nova;
- bugfix de comportamento relevante;
- alteração de regra de negócio;
- mudança de dados/API com impacto observável;
- refactor de médio/alto risco.

Pode ser dispensada para documentação, chores e refactors pequenos que não mudam comportamento observável.

## Artefatos

Quando aplicável, usar artefatos versionáveis no projeto:

```text
specs/semantic-contract.json
specs/verification-plan.json
specs/review-evidence.json
```

### semantic-contract.json

É o alvo verificável antes do código. Deve conter, proporcionalmente ao problema:

- objetivo;
- tipo de mudança e risco;
- escopo dentro/fora;
- assumptions explícitas;
- invariantes/regras de negócio;
- contratos de dados quando relevantes;
- interfaces/API quando relevantes;
- critérios de aceite observáveis em `given / when / then`.

Critérios `must` são obrigatórios para a entrega.

Quando houver API `contract`/`governed`, não copie o OpenAPI/GraphQL/Protobuf/AsyncAPI inteiro para a spec semântica. O contrato machine-readable continua sendo autoridade da interface conforme `core/API_ENGINEERING.md`; a spec semântica registra somente os comportamentos e invariantes que precisam de prova, como autorização, compatibilidade, paginação, idempotência, retry, erro ou workflow crítico.

### verification-plan.json

É derivado da spec, não inventado depois da implementação. Cada critério de aceite recebe uma linha de rastreabilidade.

Todo critério `must` precisa apontar para pelo menos uma evidência executável ligada a um gate declarado do repositório, por exemplo:

- teste unitário/integrado;
- E2E/browser;
- gate funcional;
- lint/compatibility/contract test de API quando aplicável;
- visual regression quando aplicável.

O plano não substitui a execução dos testes. Ele liga intenção → teste/gate para reduzir testes que apenas confirmam uma implementação errada.

### review-evidence.json

Registra a revisão semântica depois da implementação/verificação.

Para risco médio/alto, `deterministic-ci` sozinho não basta. É exigido um modo desacoplado:

- `independent-agent`: outro agente/contexto revisa;
- `clean-context`: nova passagem recebe somente spec + estado verificável, sem usar o raciocínio da implementação.

O registro fica amarrado por fingerprints à spec, ao plano e ao conteúdo revisado. Se código/spec/plano mudarem depois, a revisão fica stale.

## Fluxo

Para trabalho funcional relevante:

```text
planning
→ specification
→ implementation
→ verification
→ review desacoplado
→ delivery
```

A fase `specification` deve terminar antes da implementação.

Para APIs com contrato formal, a definição/alteração do contrato de interface faz parte da especificação e deve preceder consumidores que dependam do novo comportamento. `core/API_ENGINEERING.md` define a forma desse contrato; este módulo define a prova de que a intenção foi atendida.

## Independência realista

A Factory é provider-neutral. Não exigir API paga ou Codex somente para criar um segundo reviewer.

Ordem desejada:

1. segundo agente/contexto independente, quando disponível;
2. clean-context review com pacote restrito a spec + evidência verificável;
3. deterministic CI continua como prova complementar, nunca como substituto exclusivo para risco médio/alto.

## Visual regression

Screenshot diffing é uma evidência forte quando a UI já possui baseline visual estável. Não deve ser obrigatório em toda interface exploratória, porque baselines instáveis geram ruído e burocracia. Em UI madura/release, prefira Playwright screenshot comparison como gate quando mudanças visuais involuntárias forem risco material.

## APIs e bibliotecas

`core/API_ENGINEERING.md` é a fonte de verdade para desenho, protocolo, contrato, compatibilidade e gates específicos de APIs.

Typecheck, build, lockfile e runtime/E2E continuam sendo a primeira defesa contra uso incorreto de bibliotecas/APIs. Quando uma integração não é protegida por tipos ou só falha em runtime, a spec/verification plan deve exigir smoke/integration evidence específica. Para APIs `contract`/`governed`, lint do contrato, compatibilidade, testes negativos/property-based ou consumer/provider contracts podem ser evidências executáveis conforme o risco.

Consulta externa de documentação não é gate universal porque pode introduzir rede/instabilidade no CI. Referências externas orientam desenho; o projeto deve versionar o contrato e os gates que realmente precisa executar.

## Context Engine e impacto

O mapa atual de imports é deliberadamente leve. Não fingir precisão de call graph universal com regex. Grafo semântico profundo deve ser promovido somente após pilotos por linguagem/stack provarem baixo falso-positivo e utilidade real.

## Regra final

`lint + typecheck + build + testes verdes` não é suficiente para declarar sucesso funcional quando existe uma spec semântica aplicável. A entrega precisa também demonstrar rastreabilidade dos critérios `must` e revisão válida contra o contrato atual.

Da mesma forma, uma API com spec válida mas sem evidência de comportamento crítico não está semanticamente provada; contrato de interface e comportamento executável se complementam.