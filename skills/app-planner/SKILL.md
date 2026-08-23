---
name: app-planner
description: Planeja um novo aplicativo ou uma evolução relevante, transformando a ideia do usuário em escopo, perfil de projeto quando aplicável, arquitetura inicial, riscos, critérios de sucesso, semântica e verificação proporcionais e blocos funcionais sem exigir decisões técnicas desnecessárias do usuário.
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
7. Decida se Semantic Verification é necessária. Quando for, derive também a profundidade de **Semantic Assurance** conforme `core/SEMANTIC_ASSURANCE.md`: `scenario` para regra pequena/isolada, `domain` para múltiplos conceitos/regras/estados/papéis e `formal` somente quando temporalidade, concorrência, safety/liveness, combinatória ou criticidade justificarem.
8. Em `domain`/`formal`, planeje `specs/semantic-assurance.json` com requisitos estruturados, vocabulário/domínio, restrições, rastreabilidade e análise de consistência. O usuário não deve preencher o schema técnico manualmente.
9. Métodos como Z3, Alloy, FRET, P, Quint/TLA+, DMN, OPA ou Cedar são selecionados por tipo de problema e evidência esperada; nenhum deles é default universal.
10. Derive a profundidade de `core/INDEPENDENT_VERIFICATION.md` a partir de risco + nível do sistema + API mode. Projetos simples permanecem `baseline`; sistemas reais/alto risco podem exigir `independent`, `adversarial` ou `release`. O usuário não escolhe scanners manualmente.
11. Quando a verificação ficar acima de `baseline`, planeje somente motores gratuitos/open source tecnicamente aplicáveis e registre a intenção de materializar `VERIFICATION.md`/workflows durante a construção.
12. Separe requisito real de solução sugerida.
13. Pesquise solução existente quando isso puder eliminar trabalho desnecessário.
14. Defina o menor produto que entrega valor real sem reduzir artificialmente a visão final nem rebaixar requisitos de integridade, compartilhamento, segurança, compatibilidade de interfaces, qualidade semântica ou evidência necessária.
15. Verifique se existe perfil validado em `profiles/` que corresponda claramente ao produto.
16. Quando houver perfil adequado, use seus defaults como ponto de partida e ative apenas módulos necessários; requisitos locais e os contratos centrais aplicáveis têm precedência.
17. Quando não houver perfil adequado, escolha stack somente depois de entender o problema e registrar a justificativa curta.
18. Divida execução em blocos funcionais completos.
19. Para cada bloco, defina critérios observáveis de conclusão a partir da intenção, antes da implementação.
20. Para funcionalidade nova, bugfix relevante, regra de negócio ou mudança de contrato/risco, use `semantic-verification` e materialize `specs/semantic-contract.json` antes do código. Para APIs formais, não copie a spec machine-readable inteira para o contrato semântico; registre os comportamentos que precisam de prova.
21. Se a profundidade for `domain`/`formal`, use `semantic-assurance` para normalizar requisitos inspirados em EARS/FRET, analisar consistência/cobertura e resolver perguntas `blocking` antes de implementar.
22. Derive o plano de verificação dos critérios da spec; não escreva testes apenas para confirmar retrospectivamente a implementação já feita. Property/stateful/model-based evidence entra quando invariantes/estados justificarem. Independent Verification adiciona evidência externa, mas não substitui rastreabilidade semântica.
23. Use `core/TASK_ROUTER.md` para orientar onde cada fase deve acontecer; GitHub CI é preferido para matrizes determinísticas quando capaz.
24. Registre decisões permanentes no repositório, não apenas no chat.

## Autonomia

Não pergunte sobre detalhes técnicos rotineiros que possam ser decididos por boa prática, evidência, nível de sistema, modo de governança da API, profundidade semântica, profundidade de Independent Verification e um perfil já validado. Recomende uma escolha e siga quando não houver necessidade real de preferência humana.

Pergunte apenas quando faltar regra de negócio, preferência subjetiva importante, orçamento, dado externo necessário ou autorização de risco.

A criação da spec semântica, modelagem técnica de domínio, classificação da API, seleção de método formal e matriz gratuita de verificação são trabalho do agente. Não transformar schemas/checklists técnicos em formulários para o usuário preencher. Quando uma regra de negócio estiver realmente ambígua, perguntar apenas essa decisão.

## Saída esperada

Objetivo, usuários/fluxos, escopo, **nível de sistema**, fonte autoritativa dos dados quando aplicável, modo/contrato de API quando aplicável, **semantic depth** (`scenario`/`domain`/`formal`) quando Semantic Verification for aplicável, modo de Independent Verification quando acima de `baseline`, perfil selecionado quando houver, arquitetura inicial, stack recomendada, módulos opcionais ativados, riscos, blocos funcionais, critérios de sucesso e roteamento para a próxima fase.

Quando Semantic Verification for aplicável, a saída durável inclui o contrato estruturado e o plano inicial de rastreabilidade. Em `domain`/`formal`, inclui também `semantic-assurance.json`/`SEMANTICS.md` quando útil. Quando Independent Verification estiver acima de `baseline`, inclui a matriz de checks `required/advisory` em `VERIFICATION.md`/workflow equivalente.
