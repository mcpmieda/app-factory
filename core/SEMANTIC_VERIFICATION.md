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

## Semantic Assurance antes da verificação

`core/SEMANTIC_ASSURANCE.md` complementa esta camada e cuida da **qualidade da própria especificação** antes da implementação.

A divisão é:

- Semantic Assurance: requisitos estão claros, coerentes, suficientemente completos e rastreáveis?
- Semantic Verification: a implementação satisfaz a especificação atual?

Para profundidade `scenario`, o contrato semântico abaixo pode ser suficiente. Para `domain`/`formal`, `specs/semantic-assurance.json` adiciona vocabulário, domínio, requisitos normalizados, restrições, consistência, cobertura e semantic diff sem duplicar os critérios deste arquivo.

Uma spec estruturalmente válida ainda pode conter interpretação humana errada. Por isso Semantic Assurance pode gerar perguntas e formalizações, mas não substitui decisão de domínio nem revisão desacoplada.

## Artefatos

Quando aplicável, usar artefatos versionáveis no projeto:

```text
specs/semantic-contract.json
specs/semantic-assurance.json   # somente em depth domain/formal
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

### semantic-assurance.json

Quando `core/SEMANTIC_ASSURANCE.md` selecionar profundidade `domain` ou `formal`, este artefato liga requisitos estruturados aos critérios/invariantes deste contrato e ao modelo de domínio relevante.

Ele não substitui `semantic-contract.json`, banco/schema, OpenAPI ou arquitetura. Seu propósito é eliminar ambiguidade evitável, detectar referências/contradições estruturadas, medir cobertura de rastreabilidade e calcular impacto semântico.

### verification-plan.json

É derivado da spec, não inventado depois da implementação. Cada critério de aceite recebe uma linha de rastreabilidade.

Todo critério `must` precisa apontar para pelo menos uma evidência executável ligada a um gate declarado do repositório, por exemplo:

- teste unitário/integrado;
- E2E/browser;
- gate funcional;
- property/stateful test quando aplicável;
- lint/compatibility/contract test de API quando aplicável;
- visual regression quando aplicável;
- evidência de Independent Verification quando um motor externo provar o critério ou risco relacionado;
- gate formal selecionado por Semantic Assurance quando a propriedade realmente depender dele.

O plano não substitui a execução dos testes. Ele liga intenção → teste/gate para reduzir testes que apenas confirmam uma implementação errada.

### review-evidence.json

Registra a revisão semântica depois da implementação/verificação.

Para risco médio/alto, `deterministic-ci` sozinho não basta. É exigido um modo desacoplado:

- `independent-agent`: outro agente/contexto revisa;
- `clean-context`: nova passagem recebe somente spec + estado verificável, sem usar o raciocínio da implementação.

O registro fica amarrado por fingerprints à spec, ao plano e ao conteúdo revisado. Se código/spec/plano mudarem depois, a revisão fica stale.

Quando Semantic Assurance detectar semantic diff material, os critérios/invariantes/gates impactados também precisam ser considerados stale até nova prova.

## Fluxo

Para trabalho funcional relevante:

```text
planning
→ semantic assurance proporcional
→ specification
→ implementation
→ verification
→ review desacoplado
→ delivery
```

A fase `specification` deve terminar antes da implementação. Em `domain`/`formal`, isso inclui resolver erros determinísticos e perguntas `blocking` de Semantic Assurance.

Para APIs com contrato formal, a definição/alteração do contrato de interface faz parte da especificação e deve preceder consumidores que dependam do novo comportamento. `core/API_ENGINEERING.md` define a forma desse contrato; este módulo define a prova de que a intenção foi atendida.

## Model/property-based evidence

`given/when/then` continua sendo a forma legível principal dos critérios. Quando o domínio tiver ranges, invariantes, decisões combinatórias ou máquina de estados, `core/SEMANTIC_ASSURANCE.md` pode recomendar property-based/stateful/model-based testing para explorar casos que os exemplos manuais não cobrem.

Contraexemplo encontrado por esses motores deve virar regressão reproduzível quando material.

## Evidência browser/E2E em interfaces reais

Testes de navegador devem provar comportamento, não depender acidentalmente da simplicidade momentânea da tela.

Regras práticas quando a UI cresce:

- escopar locators a uma região estável (`form`, dialog, painel, landmark, row/card) antes de selecionar por label/role quando o mesmo conceito puder aparecer em mais de um lugar;
- preferir role/label/nome acessível dentro dessa região a seletores frágeis de CSS ou posição;
- quando o teste manipular `localStorage`, IndexedDB, sessão ou fixture depois da navegação, esperar um sinal explícito de hidratação/readiness **antes** da mutação, ou semear o estado antes da inicialização;
- não interpretar corrida de inicialização como falha de regra de negócio nem “corrigir” o produto para satisfazer um teste mal sincronizado;
- evidência deve afirmar o invariante/resultado do critério. Texto incidental, animação ou detalhe visual só vira assert obrigatório quando fizer parte da especificação.

Essas regras não criam um novo framework de testes; são disciplina para manter a evidência semântica válida conforme a interface fica mais densa.

## Independent Verification

`core/INDEPENDENT_VERIFICATION.md` é complementar e **não substitui** Semantic Verification.

Ele adiciona motores determinísticos que podem tentar reprovar a implementação por métodos diferentes dos testes escritos pela IA, por exemplo mutation testing, Schemathesis, OWASP ZAP, Semgrep, Trivy, axe-core e Lighthouse CI.

A divisão de responsabilidade é:

- Semantic Assurance responde **"a especificação está suficientemente boa para implementar?"**;
- Semantic Verification responde **"isso corresponde ao que foi especificado?"**;
- Independent Verification responde **"motores externos conseguem encontrar falhas que os testes/implementação podem ter deixado passar?"**.

Resultados de scanners podem ser ligados a critérios `must` quando realmente provarem parte deles, mas não devem ser usados como substituto genérico da revisão semântica.

Mutation testing, SAST, DAST e fuzzing **não entendem sozinhos a intenção** do produto. Um sistema pode passar em todos eles e ainda implementar a regra de negócio errada.

## Independência realista

A Factory é provider-neutral. Não exigir API paga ou Codex somente para criar um segundo reviewer.

Ordem desejada:

1. segundo agente/contexto independente, quando disponível;
2. clean-context review com pacote restrito a spec + evidência verificável;
3. deterministic CI e Independent Verification continuam como provas complementares, nunca como substituto exclusivo para risco médio/alto.

A camada independente é `free-only` por padrão e não exige segunda IA paga.

## Visual regression

Screenshot diffing é uma evidência forte quando a UI já possui baseline visual estável. Não deve ser obrigatório em toda interface exploratória, porque baselines instáveis geram ruído e burocracia. Em UI madura/release, prefira Playwright screenshot comparison como gate quando mudanças visuais involuntárias forem risco material.

## APIs e bibliotecas

`core/API_ENGINEERING.md` é a fonte de verdade para desenho, protocolo, contrato, compatibilidade e gates específicos de APIs.

Typecheck, build, lockfile e runtime/E2E continuam sendo a primeira defesa contra uso incorreto de bibliotecas/APIs. Quando uma integração não é protegida por tipos ou só falha em runtime, a spec/verification plan deve exigir smoke/integration evidence específica. Para APIs `contract`/`governed`, lint do contrato, compatibilidade, testes negativos/property-based ou consumer/provider contracts podem ser evidências executáveis conforme o risco.

Quando API Engineering selecionar testes adversariais como Schemathesis/DAST, `core/INDEPENDENT_VERIFICATION.md` define sua execução proporcional e segura sem duplicar o contrato de API.

Consulta externa de documentação não é gate universal porque pode introduzir rede/instabilidade no CI. Referências externas orientam desenho; o projeto deve versionar o contrato e os gates que realmente precisa executar.

## Context Engine e impacto

O mapa atual de imports é deliberadamente leve. Não fingir precisão de call graph universal com regex. Grafo semântico profundo deve ser promovido somente após pilotos por linguagem/stack provarem baixo falso-positivo e utilidade real.

`engine/semantic_assurance.py` mantém um grafo semântico **explícito** por IDs/referências de domínio e pode calcular impacto requisito → AC/invariante → gate. Isso é diferente de inferir automaticamente todo o call graph do código.

## Regra final

`lint + typecheck + build + testes verdes` não é suficiente para declarar sucesso funcional quando existe uma spec semântica aplicável. A entrega precisa também demonstrar rastreabilidade dos critérios `must` e revisão válida contra o contrato atual.

Da mesma forma, uma API com spec válida mas sem evidência de comportamento crítico não está semanticamente provada; contrato de interface, Semantic Assurance proporcional, comportamento executável e verificação independente se complementam.
