---
name: maintenance
description: Modifica sistemas existentes com baseline, escopo fechado, revisão por impacto, rollback proporcional e foco em preservar comportamento estável fora da mudança solicitada.
---

# Maintenance

## Antes de alterar

- recupere estado vigente e baseline seguro;
- entenda o comportamento que não pode ser quebrado;
- feche o escopo;
- identifique dependências diretas;
- classifique risco.

## Implementação

Altere o necessário para entregar o bloco solicitado. "Mínimo" significa evitar reescrita irrelevante, não limitar a solução a uma microcorreção incompleta.

## Falha

Não continue empilhando patches sobre estado incerto. Compare com o baseline e, quando mais seguro, reverta a tentativa e reaplique a solução limpa.

## Revisão

Priorize diff, chamadas/dependências diretas, dados de entrada/saída, UI afetada, permissões e testes relacionados.

Reserve auditoria integral para mudança estrutural, incidente sistêmico, troca de dependência central ou release importante.