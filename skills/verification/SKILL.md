---
name: verification
description: Verifica se uma implementação realmente funciona usando checks estáticos, testes, build, comportamento real, navegador, rastreabilidade semântica, verificadores independentes e revisão por impacto antes de considerar a tarefa concluída.
---

# Verification

## Objetivo

Produzir evidência proporcional ao risco, não apenas confiança textual.

## Antes dos testes

Quando `core/SEMANTIC_VERIFICATION.md` se aplicar:

1. validar `specs/semantic-contract.json`;
2. gerar/atualizar `specs/verification-plan.json` a partir dos critérios;
3. garantir que todo critério `must` aponta para evidência executável;
4. só então usar os gates como prova.

Quando `core/SEMANTIC_ASSURANCE.md` for `domain/formal`, valide também consistência, semantic diff e candidatos a property/stateful/combinatorial tests antes de tratar a spec como ready.

Quando `core/INDEPENDENT_VERIFICATION.md` se aplicar, derive a matriz `baseline`/`independent`/`adversarial`/`release` e carregue `independent-verification`. O objetivo é diversidade de método, não quantidade de scanners.

## Sequência padrão

Quando disponível e relevante:

1. validar sintaxe/configuração;
2. lint;
3. typecheck;
4. testes direcionados derivados dos critérios/contratos;
5. build;
6. iniciar aplicação/serviços de teste;
7. exercitar fluxo principal;
8. browser/E2E quando houver UI;
9. visual regression quando houver baseline estável e risco material;
10. executar a matriz independente selecionada;
11. verificar regressão direta;
12. revisar diff/impacto;
13. para risco médio/alto com spec, realizar revisão desacoplada antes de delivery.

## Testes por comportamento

Prefira contratos observáveis: `condição/entrada → comportamento esperado → estado/saída esperado`.

Quando houver spec, use IDs `AC-###` como rastreabilidade no plano de verificação. O teste continua idiomático para a stack; o vínculo formal fica em `verification-plan.json`.

Quando um bug importante for corrigido, avalie teste/guardrail contra reincidência.

## Verificação independente

A camada é proporcional e `free-only`. Não instalar tudo em todo projeto.

Classes possíveis, sempre condicionais:

- supply chain/secrets/misconfiguration — Trivy;
- SAST — Semgrep CE ou substituto validado;
- mutation — StrykerJS/mutmut;
- domain property/stateful — Hypothesis/fast-check quando Semantic Assurance justificar;
- combinatorial — NIST ACTS/equivalente quando houver modelo finito material;
- API fuzz/stateful — Schemathesis; RESTler apenas como escalonamento `governed` profundo;
- DAST — OWASP ZAP em alvo efêmero/autorizado;
- CI correctness/security — actionlint/zizmor quando workflows existirem;
- PostgreSQL migration safety — Squawk quando aplicável;
- architecture conformance — dependency-cruiser/equivalente quando limites estiverem declarados;
- browser/accessibility — Playwright/axe, com Chromium+Firefox+WebKit somente se suporte multi-engine for requisito;
- page quality — Lighthouse CI com baseline;
- load/concurrency — k6 com SLO/workload real;
- network resilience — Toxiproxy/equivalente com proxy/stub controlado.

Ferramenta indisponível não significa `pass`. Check `required` precisa executar ou receber exceção explícita/versionada.

Não rode equivalentes redundantes sem ganho. Semgrep+Opengrep em paralelo, por exemplo, não é default; Opengrep é alternativa qualificada. Schemathesis permanece API fuzz principal; RESTler é escalonamento.

## Alvos seguros

DAST ativo, fuzz destrutivo, load e fault injection nunca inferem produção/terceiro como alvo. Use preview/local/ambiente efêmero e dados fictícios. Toxiproxy degrada um proxy/stub controlado, não o serviço externo real.

## APIs/bibliotecas

Typecheck/build capturam boa parte de imports/assinaturas inexistentes em stacks tipadas. Para integração não tipada/runtime, adicione smoke/integration test ligado ao critério afetado.

`core/API_ENGINEERING.md` decide contrato e gates específicos. Independent Verification decide execução adversarial sem duplicar o contrato.

## Revisão proporcional

Mudança localizada: revisar diff, dependências diretas e testes afetados. Mudança estrutural/incidente/release: ampliar auditoria.

Quando Semantic Verification exigir revisão desacoplada, prefira outro agente/contexto; se indisponível, faça `clean-context` usando apenas spec, conteúdo/diff e evidências.

Scanners, mutation, property testing, fuzzing, load tests e model checkers **não substituem** revisão semântica independente: não entendem sozinhos a intenção.

## Comunicação

Relate separadamente o que foi implementado, testado, validado em execução real, testado por motores independentes, o que não pôde ser verificado e riscos restantes. Nunca converter "não consegui testar" em "funciona".
