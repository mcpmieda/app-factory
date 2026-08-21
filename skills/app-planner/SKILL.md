---
name: app-planner
description: Planeja um novo aplicativo ou uma evolução relevante, transformando a ideia do usuário em escopo, perfil de projeto quando aplicável, arquitetura inicial, riscos, critérios de sucesso e blocos funcionais sem exigir decisões técnicas desnecessárias do usuário.
---

# App Planner

Use quando a tarefa começa como ideia, problema, novo sistema ou grande evolução.

## Processo

1. Reescreva internamente o objetivo em linguagem de resultado.
2. Identifique usuários, fluxos principais, dados e restrições.
3. Separe requisito real de solução sugerida.
4. Pesquise solução existente quando isso puder eliminar trabalho desnecessário.
5. Defina o menor produto que entrega valor real sem reduzir artificialmente a visão final.
6. Verifique se existe perfil validado em `profiles/` que corresponda claramente ao produto.
7. Quando houver perfil adequado, use seus defaults como ponto de partida e ative apenas módulos necessários; requisitos locais têm precedência.
8. Quando não houver perfil adequado, escolha stack somente depois de entender o problema e registrar a justificativa curta.
9. Divida execução em blocos funcionais completos.
10. Para cada bloco, defina critérios observáveis de conclusão a partir da intenção, antes da implementação.
11. Para funcionalidade nova, bugfix relevante, regra de negócio ou mudança de contrato/risco, use `semantic-verification` e materialize `specs/semantic-contract.json` antes do código.
12. Derive o plano de verificação dos critérios da spec; não escreva testes apenas para confirmar retrospectivamente a implementação já feita.
13. Use `core/TASK_ROUTER.md` para orientar onde cada fase deve acontecer.
14. Registre decisões permanentes no repositório, não apenas no chat.

## Autonomia

Não pergunte sobre detalhes técnicos rotineiros que possam ser decididos por boa prática, evidência e um perfil já validado. Recomende uma escolha e siga quando não houver necessidade real de preferência humana.

Pergunte apenas quando faltar regra de negócio, preferência subjetiva importante, orçamento, dado externo necessário ou autorização de risco.

A criação da spec semântica é trabalho do agente. Não transformar o schema em formulário técnico para o usuário preencher. Quando uma regra de negócio estiver realmente ambígua, perguntar apenas essa decisão.

## Saída esperada

Objetivo, usuários/fluxos, escopo, perfil selecionado quando houver, arquitetura inicial, stack recomendada, módulos opcionais ativados, riscos, blocos funcionais, critérios de sucesso e roteamento para a próxima fase.

Quando Semantic Verification for aplicável, a saída durável inclui também o contrato estruturado e o plano inicial de rastreabilidade.
