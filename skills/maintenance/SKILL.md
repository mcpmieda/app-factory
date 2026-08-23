---
name: maintenance
description: Modifica sistemas existentes com baseline, escopo fechado, revisão por impacto, rollback proporcional, Change Hygiene e foco em preservar comportamento estável sem acumular implementações obsoletas.
---

# Maintenance

## Antes de alterar

- recupere estado vigente e baseline seguro;
- entenda o comportamento que não pode ser quebrado;
- feche o escopo;
- identifique dependências diretas;
- classifique risco;
- leia `core/CHANGE_HYGIENE.md`;
- em projeto externo, descubra primeiro o caminho de execução real e fontes de verdade existentes; não assuma que organização ruim significa que toda a dívida precisa ser reescrita agora.

## Implementação

Altere o necessário para entregar o bloco solicitado. "Mínimo" significa evitar reescrita irrelevante, não limitar a solução a uma microcorreção incompleta.

Preserve **comportamento**, não implementação obsoleta. Quando uma função, componente, estilo, rota, configuração ou caminho de execução for realmente substituído, prefira corrigir/substituir a origem e remover o caminho antigo em vez de criar `new`, `fixed`, `final`, `v2`, wrappers sucessivos ou overrides que apenas o neutralizam.

Refactor local indispensável pode acompanhar a correção. Refactor estrutural grande deve, quando possível, ficar separado da mudança funcional para deixar revisão/rollback claros.

## Falha

Não continue empilhando patches sobre estado incerto. Compare com o baseline e, quando mais seguro, reverta a tentativa e reaplique a solução limpa.

Repair loop é espaço de experimentação, não arquitetura final. Tentativas descartadas podem existir temporariamente durante diagnóstico, mas devem desaparecer antes da entrega.

## Consolidação obrigatória

Depois que a solução funcionar e **antes** da revisão final:

1. compare o estado final com o baseline;
2. remova tentativas anteriores ainda presentes;
3. remova código morto, imports/exports/dependências/handlers/estilos/arquivos que ficaram órfãos;
4. elimine shadow implementations e CSS/config em camadas quando a origem puder ser corrigida;
5. revise suppressions e `!important` novos;
6. mantenha dupla implementação apenas quando houver compatibilidade real + condição objetiva de remoção + testes de transição;
7. execute `scripts/change_hygiene.py` quando a Factory estiver disponível e trate blockers; advisories exigem julgamento, não remoção automática;
8. rode novamente as regressões **depois** da limpeza.

Se a versão entregue só funciona porque patches anteriores continuam anulando uns aos outros, a tarefa não está pronta.

## Revisão

Priorize diff, chamadas/dependências diretas, dados de entrada/saída, UI afetada, permissões, testes relacionados e **net code health da área tocada**.

Pergunta de fechamento: **se soubéssemos desde o início qual solução funcionaria, implementaríamos o estado final exatamente desta forma?** Se a resposta for não porque o código ainda contém histórico de tentativas, consolide novamente.

Reserve auditoria integral para mudança estrutural, incidente sistêmico, troca de dependência central ou release importante.
