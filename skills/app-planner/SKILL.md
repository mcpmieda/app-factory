---
name: app-planner
description: Planeja um novo aplicativo ou uma evolução relevante, transformando a ideia do usuário em escopo, arquitetura, riscos, semântica e verificação proporcionais, incluindo carga, resiliência, migrations e CI quando materialmente necessários, sem exigir decisões técnicas rotineiras do usuário.
---

# App Planner

Use quando a tarefa começa como ideia, problema, novo sistema ou grande evolução, em qualquer domínio de software.

## Processo

1. Reescreva internamente o objetivo em linguagem de resultado.
2. Identifique usuários, fluxos principais, dados e restrições.
3. Classifique o produto com `core/SYSTEM_ENGINEERING.md` (`website`, `local-app`, `persistent-app`, `multi-user-system`, `production-system` ou `critical-system`) antes de fechar arquitetura.
4. Para `persistent-app` ou superior, registre a **fonte autoritativa dos dados**, fronteira cliente/servidor, persistência e identidade/autorização; não aceite armazenamento só no navegador como persistência final compartilhada.
5. Verifique fronteira de API/integração. Quando existir, aplique `core/API_ENGINEERING.md`, classifique `none`, `lightweight`, `contract` ou `governed`, identifique consumidores e escolha protocolo/contrato proporcional. Backend não implica OpenAPI/API pública.
6. Para API `contract`/`governed`, registre fonte machine-readable e gates mínimos de contrato/compatibilidade/runtime.
7. Decida se Semantic Verification é necessária. Quando for, derive profundidade de **Semantic Assurance** conforme `core/SEMANTIC_ASSURANCE.md`: `scenario`, `domain` ou `formal`.
8. Em `domain`/`formal`, planeje `specs/semantic-assurance.json` com requisitos estruturados, vocabulário/domínio, restrições, estados e rastreabilidade. O usuário não preenche schema técnico manualmente.
9. Métodos formais são selecionados por problema, não por sofisticação: Z3, Alloy, FRET, P, Quint/TLA+, DMN, OPA/Cedar somente quando trouxerem prova melhor.
10. Derive também candidatos de exploração da própria semântica:
    - invariantes/ranges/estados → Hypothesis, fast-check ou equivalente;
    - múltiplas dimensões finitas realmente interativas → NIST ACTS/covering arrays;
    - não introduza property/combinatorial testing em regra trivial.
11. Derive a profundidade de `core/INDEPENDENT_VERIFICATION.md` por risco + sistema + API mode. Projetos simples permanecem `baseline`; sistemas reais/alto risco podem exigir `independent`, `adversarial` ou `release`.
12. Acima de `baseline`, planeje somente motores gratuitos/open source aplicáveis. Além da matriz tradicional, verifique explicitamente se existem superfícies para:
    - workflows GitHub → actionlint/zizmor;
    - PostgreSQL + migrations → Squawk;
    - arquitetura modular declarada → dependency-cruiser/equivalente;
    - workload/SLO/performance → k6;
    - integrações externas materiais → Toxiproxy/equivalente;
    - web multi-browser → Playwright Chromium/Firefox/WebKit quando suportado;
    - REST/OpenAPI `governed` com estado profundo → RESTler como escalonamento, não substituto automático do Schemathesis.
13. Não transforme “produção” em justificativa para todos os motores. Load, chaos/fault injection, combinatorial e deep fuzz exigem pré-condição real.
14. Separe requisito real de solução sugerida.
15. Pesquise solução existente quando isso puder eliminar trabalho desnecessário.
16. Defina o menor produto que entrega valor real sem rebaixar integridade, compartilhamento, segurança, compatibilidade, qualidade semântica ou evidência necessária.
17. Verifique perfil validado em `profiles/` quando corresponder claramente ao produto.
18. Quando houver perfil adequado, use defaults como ponto de partida e ative apenas módulos necessários; contratos centrais têm precedência.
19. Quando não houver perfil adequado, escolha stack após entender problema e registrar justificativa curta.
20. Divida execução em blocos funcionais completos.
21. Para cada bloco, defina critérios observáveis de conclusão antes da implementação.
22. Para funcionalidade nova, bugfix relevante, regra de negócio ou mudança de contrato/risco, materialize `specs/semantic-contract.json` antes do código. APIs formais mantêm schema de interface separado do contrato semântico.
23. Em `domain`/`formal`, use `semantic-assurance` para normalizar requisitos, analisar consistência/cobertura e resolver perguntas `blocking` antes de implementar.
24. Derive verificação dos critérios da spec; não escreva testes apenas para confirmar retrospectivamente a implementação. Property/stateful/combinatorial evidence entra quando invariantes/estados/dimensões justificarem.
25. Independent Verification adiciona evidência externa, mas não substitui rastreabilidade semântica.
26. Para load/fuzz/DAST/fault injection, planeje alvo efêmero/controlado; produção ou serviço de terceiro nunca é alvo por inferência.
27. Use `core/TASK_ROUTER.md` para decidir onde cada fase roda; GitHub CI é preferido para matrizes determinísticas quando capaz.
28. Registre decisões permanentes no repositório, não apenas no chat.

## Autonomia

Não pergunte detalhes técnicos rotineiros resolvíveis por boa prática, evidência, nível de sistema, API mode, semantic depth, perfil e planner determinístico.

Pergunte apenas quando faltar regra de negócio, preferência subjetiva importante, orçamento, dado externo necessário ou autorização de risco.

Classificação da API, modelagem técnica, método formal, property/combinatorial strategy, load/resilience strategy e matriz gratuita de verificação são trabalho do agente. O usuário não escolhe scanner/solver manualmente.

## Saída esperada

Objetivo, usuários/fluxos, escopo, nível de sistema, **fonte autoritativa dos dados** quando aplicável, API mode/contrato, semantic depth, modo de Independent Verification, perfil, arquitetura, stack, riscos, blocos funcionais, critérios de sucesso e roteamento.

Quando relevante, a saída durável também registra:

- contrato semântico e plano de rastreabilidade;
- `semantic-assurance.json`/`SEMANTICS.md` em `domain/formal`;
- property/combinatorial models quando realmente necessários;
- matriz `required/advisory` em `VERIFICATION.md`;
- workload/SLO, migration safety, architecture boundaries, integration resilience e CI hygiene somente quando essas superfícies existirem.
