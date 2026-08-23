---
name: app-planner
description: Planeja um novo aplicativo ou uma evolução relevante, transformando a ideia do usuário em escopo, perfil de projeto quando aplicável, arquitetura inicial, riscos, critérios de sucesso, verificação proporcional e blocos funcionais sem exigir decisões técnicas desnecessárias do usuário.
---

# App Planner

Use quando a tarefa começa como ideia, problema, novo sistema ou grande evolução.

## Processo

1. Reescreva internamente o objetivo em linguagem de resultado.
2. Identifique usuários, fluxos principais, dados e restrições.
3. Classifique o produto com `core/SYSTEM_ENGINEERING.md` (`website`, `local-app`, `persistent-app`, `multi-user-system`, `production-system` ou `critical-system`) antes de fechar a arquitetura.
4. Para `persistent-app` ou superior, registre fonte autoritativa dos dados, fronteira cliente/servidor, persistência e requisitos de identidade/autorização; não aceite armazenamento apenas no navegador como arquitetura final compartilhada.
5. Verifique se existe uma fronteira de API/integração relevante. Quando existir, aplique `core/API_ENGINEERING.md`, classifique a interface como `none`, `lightweight`, `contract` ou `governed`, identifique consumidores e escolha o protocolo/contrato proporcional. Não obrigue OpenAPI ou API pública apenas porque o sistema tem backend.
6. Para API `contract`/`governed`, registre a fonte de verdade machine-readable adequada ao protocolo e os gates mínimos de contrato/compatibilidade/runtime antes de fechar a arquitetura.
7. Derive a profundidade de `core/INDEPENDENT_VERIFICATION.md` a partir de risco + nível do sistema + API mode. Projetos simples permanecem `baseline`; sistemas reais/alto risco podem exigir `independent`, `adversarial` ou `release`. O usuário não escolhe scanners manualmente.
8. Quando a verificação ficar acima de `baseline`, planeje somente motores gratuitos/open source tecnicamente aplicáveis e registre a intenção de materializar `VERIFICATION.md`/workflows durante a construção.
9. Separe requisito real de solução sugerida.
10. Pesquise solução existente quando isso puder eliminar trabalho desnecessário.
11. Defina o menor produto que entrega valor real sem reduzir artificialmente a visão final nem rebaixar requisitos de integridade, compartilhamento, segurança, compatibilidade de interfaces ou evidência necessária.
12. Verifique se existe perfil validado em `profiles/` que corresponda claramente ao produto.
13. Quando houver perfil adequado, use seus defaults como ponto de partida e ative apenas módulos necessários; requisitos locais, `core/SYSTEM_ENGINEERING.md`, `core/API_ENGINEERING.md` e `core/INDEPENDENT_VERIFICATION.md` quando aplicáveis têm precedência.
14. Quando não houver perfil adequado, escolha stack somente depois de entender o problema e registrar a justificativa curta.
15. Divida execução em blocos funcionais completos.
16. Para cada bloco, defina critérios observáveis de conclusão a partir da intenção, antes da implementação.
17. Para funcionalidade nova, bugfix relevante, regra de negócio ou mudança de contrato/risco, use `semantic-verification` e materialize `specs/semantic-contract.json` antes do código. Para APIs formais, não copie a spec machine-readable inteira para o contrato semântico; registre os comportamentos que precisam de prova.
18. Derive o plano de verificação dos critérios da spec; não escreva testes apenas para confirmar retrospectivamente a implementação já feita. Independent Verification adiciona evidência externa, mas não substitui essa rastreabilidade.
19. Use `core/TASK_ROUTER.md` para orientar onde cada fase deve acontecer; GitHub CI é preferido para a matriz independente quando capaz.
20. Registre decisões permanentes no repositório, não apenas no chat.

## Autonomia

Não pergunte sobre detalhes técnicos rotineiros que possam ser decididos por boa prática, evidência, nível de sistema, modo de governança da API, profundidade de Independent Verification e um perfil já validado. Recomende uma escolha e siga quando não houver necessidade real de preferência humana.

Pergunte apenas quando faltar regra de negócio, preferência subjetiva importante, orçamento, dado externo necessário ou autorização de risco.

A criação da spec semântica, a classificação técnica da API e a seleção da matriz gratuita de verificação são trabalho do agente. Não transformar schemas/checklists técnicos em formulários para o usuário preencher. Quando uma regra de negócio estiver realmente ambígua, perguntar apenas essa decisão.

## Saída esperada

Objetivo, usuários/fluxos, escopo, **nível de sistema**, fonte autoritativa dos dados quando aplicável, modo/contrato de API quando aplicável, modo de Independent Verification quando acima de `baseline`, perfil selecionado quando houver, arquitetura inicial, stack recomendada, módulos opcionais ativados, riscos, blocos funcionais, critérios de sucesso e roteamento para a próxima fase.

Quando Semantic Verification for aplicável, a saída durável inclui também o contrato estruturado e o plano inicial de rastreabilidade. Quando Independent Verification estiver acima de `baseline`, a saída durável inclui a matriz de checks `required/advisory` em `VERIFICATION.md`/workflow equivalente.
