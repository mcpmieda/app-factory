---
name: verification
description: Verifica se uma implementação realmente funciona usando checks estáticos, testes, build, comportamento real, navegador e revisão por impacto antes de considerar a tarefa concluída.
---

# Verification

## Objetivo

Produzir evidência proporcional ao risco, não apenas confiança textual.

## Sequência padrão

Quando disponível e relevante:

1. validar sintaxe/configuração;
2. lint;
3. typecheck;
4. testes direcionados;
5. build;
6. iniciar aplicação;
7. exercitar fluxo principal;
8. testar browser/E2E quando houver UI;
9. verificar regressão direta;
10. revisar diff e efeitos colaterais prováveis.

## Testes por comportamento

Prefira contratos observáveis: `condição/entrada → comportamento esperado → estado/saída esperado`.

Quando um bug importante for corrigido, avalie criar teste ou guardrail que impeça reincidência.

## Revisão proporcional

Mudança localizada: revisar diff, dependências diretas e testes afetados. Mudança estrutural, incidente sistêmico ou release importante: ampliar auditoria.

## Comunicação

Relate separadamente o que foi implementado, testado, validado em execução real, o que não pôde ser verificado e riscos restantes. Nunca converter "não consegui testar" em "funciona".