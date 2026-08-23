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
2. gerar/atualizar `specs/verification-plan.json` a partir dos critérios da spec;
3. garantir que todo critério `must` aponta para evidência executável real;
4. só então usar os gates como prova do requisito.

Isso reduz o risco de o agente escrever testes que apenas confirmam a implementação que ele próprio escolheu, em vez do comportamento pedido.

Quando `core/INDEPENDENT_VERIFICATION.md` se aplicar, derive também a matriz independente (`baseline`/`independent`/`adversarial`/`release`) e carregue `independent-verification`. O objetivo é adicionar métodos que não dependam dos mesmos casos escritos pela IA implementadora.

## Sequência padrão

Quando disponível e relevante:

1. validar sintaxe/configuração;
2. lint;
3. typecheck;
4. testes direcionados derivados dos critérios/contratos aplicáveis;
5. build;
6. iniciar aplicação;
7. exercitar fluxo principal;
8. testar browser/E2E quando houver UI;
9. usar visual regression quando houver baseline estável e regressão visual for risco material;
10. executar verificadores independentes selecionados, como Trivy/Semgrep/axe, mutation testing, Schemathesis ou OWASP ZAP;
11. verificar regressão direta;
12. revisar diff e efeitos colaterais prováveis;
13. para risco médio/alto com spec, realizar revisão desacoplada antes de delivery.

## Testes por comportamento

Prefira contratos observáveis: `condição/entrada → comportamento esperado → estado/saída esperado`.

Quando houver spec semântica, use IDs `AC-###` como rastreabilidade no plano de verificação. O teste pode continuar idiomático para a stack; o vínculo formal fica no `verification-plan.json`.

Quando um bug importante for corrigido, avalie criar teste ou guardrail que impeça reincidência.

## Verificação independente

A camada independente é proporcional e `free-only` por padrão. Não instalar tudo em todo projeto.

- Trivy/Semgrep/axe são bons candidatos para evidência independente de custo baixo/moderado;
- mutation testing serve para verificar a força dos próprios testes;
- Schemathesis gera casos adversariais quando API Engineering selecionar esse gate;
- OWASP ZAP observa o sistema de fora e deve usar ambiente efêmero/autorizado;
- Lighthouse CI entra quando performance/qualidade tiver baseline estável.

Ferramenta indisponível não significa `pass`. Checks `required` precisam executar ou receber exceção explícita e justificável.

## APIs/bibliotecas

Typecheck e build capturam grande parte de imports/assinaturas inexistentes em stacks tipadas. Para integração não tipada ou dependente de runtime, adicione smoke/integration test ligado ao critério afetado. Não trate documentação externa como substituta de execução real.

`core/API_ENGINEERING.md` decide o contrato e a necessidade de gates específicos. `core/INDEPENDENT_VERIFICATION.md` decide como esses gates adversariais se combinam com outros verificadores sem duplicar o contrato da API.

## Revisão proporcional

Mudança localizada: revisar diff, dependências diretas e testes afetados. Mudança estrutural, incidente sistêmico ou release importante: ampliar auditoria.

Quando Semantic Verification exigir revisão desacoplada, prefira outro agente/contexto; se indisponível, faça uma nova passagem `clean-context` usando apenas spec, conteúdo/diff necessário e evidências, sem usar o raciocínio da implementação como prova.

Scanners determinísticos, mutation testing e fuzzing **não substituem** essa revisão semântica independente: eles não entendem sozinhos a intenção do produto.

## Comunicação

Relate separadamente o que foi implementado, testado, validado em execução real, testado por motores independentes, o que não pôde ser verificado e riscos restantes. Nunca converter "não consegui testar" em "funciona".
