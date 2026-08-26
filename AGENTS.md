# AGENTS.md — App Factory

Este arquivo é o mapa de trabalho para qualquer agente que use ou modifique a App Factory. Ele deve permanecer curto; detalhes ficam nos módulos especializados.

## Entrada universal

Pedidos de criação, evolução, manutenção, correção, automação, integração ou continuação de software devem entrar por `skills/factory-router/SKILL.md`, mesmo quando o usuário não mencionar "App Factory".

Leia `core/ENTRYPOINT.md` para o contrato de ativação automática.

A App Factory é **general-purpose**. Sistemas escolares são um domínio válido entre muitos; regras locais pertencem ao projeto/perfil e não limitam o Core.

## Project Adoption Gate

Quando o usuário escolher explicitamente a App Factory para um projeto, quando o projeto vier de um starter da Factory ou quando o repositório já declarar governança pela Factory, **carregue `skills/project-adoption/SKILL.md` e aplique `core/PROJECT_ADOPTION_GATE.md` antes da primeira alteração funcional/visual material**.

Adoção não pode ser apenas nominal ou retroativa. Antes do código, o projeto governado deve tornar recuperáveis pelo menos `AGENTS.md`, `PROJECT_STATE.md`, `.app-factory.json`, classificações de escala/risco/system level/API/Semantic/Independent Verification e, em UI material, design system + Professional UI + Motion Profile.

Execute quando disponível:

```text
project_adoption_gate.py check --phase pre-implementation
```

Um `web-admin` não pode cair silenciosamente em React + CSS próprio como fundação visual: shadcn/ui é o default validado, HeroUI é override transversal quando escolhido e base ad hoc exige desvio explícito. HeroUI não implica efeito ambiental obrigatório.

Projetos legados externos usados apenas para correção pontual não recebem governança durável por reflexo; o gate passa a ser obrigatório quando a Factory é a governança do projeto.

## Antes de agir

1. Entenda o objetivo real do usuário.
2. Leia `core/PRINCIPLES.md`.
3. Siga `core/HUMAN_INTERACTION.md` para decidir o que o agente deve fazer sozinho e o que realmente depende do usuário.
4. Em repositório existente, use `core/CONTEXT_ENGINE.md`/`context-engine` para recuperar mapa incremental e arquivos relevantes.
5. Se o Project Adoption Gate se aplicar, materialize/valide a adoção **antes** de implementação material.
6. Em evolução, manutenção, refactor, debugging, modernização ou revisão de código existente, aplique `core/CHANGE_HYGIENE.md`: preserve comportamento estável sem preservar implementação obsoleta, consolide repair loops e não entregue camadas de tentativas acumuladas.
7. Use `core/AUTONOMY_ENGINE.md`/`autonomy-engine` para recuperar ou inicializar estado e calcular a próxima ação.
8. Classifique a profundidade necessária em `core/PROJECT_SCALE.md`.
9. Classifique também o nível arquitetural em `core/SYSTEM_ENGINEERING.md`. Para `persistent-app` ou superior, identifique fonte autoritativa; para `multi-user-system` ou superior, derive persistência compartilhada, backend/server-side, identidade, autorização, validação, migrations e recovery proporcionais antes de simplificar.
10. **Continuidade após perda do cliente:** para qualquer operação persistente em que fechar o navegador, perder energia/rede ou trocar de dispositivo possa causar efeito parcial, duplicidade, divergência ou perda de progresso, aplique `core/SYSTEM_ENGINEERING.md`. Depois que o servidor aceitar a operação, o estado crítico não pode depender do navegador permanecer aberto. Use, proporcionalmente, idempotência, `operationId`, checkpoint durável, job, transação, lock, reconciliação, status posterior ou compensação. Não transforme mutações pequenas e atômicas em jobs sem necessidade.
11. Quando existir API/integração/webhook/evento/contrato compartilhado relevante, aplique `core/API_ENGINEERING.md`. Para telas/fluxos data-driven que cruzem rede, aplique também `core/DATA_ACCESS_EFFICIENCY.md`: evite frontend `chatty`, N+1 e chamadas redundantes.
12. Para funcionalidade nova, bugfix relevante, regra de negócio ou mudança de contrato/risco, aplique `core/SEMANTIC_ASSURANCE.md` + `core/SEMANTIC_VERIFICATION.md`: escolha semantic depth `scenario`/`domain`/`formal`, materialize spec antes do código e use `semantic-assurance` em `domain`/`formal`.
13. Em `domain`/`formal`, `specs/semantic-assurance.json` deve estar coerente com fingerprint da spec, sem contradições determinísticas, refs quebradas ou perguntas `blocking`.
14. Derive `core/INDEPENDENT_VERIFICATION.md`. Para `independent`/`adversarial`/`release`, carregue `independent-verification` e selecione a menor matriz gratuita/open source que cubra classes de falha diferentes. Projetos simples permanecem `baseline`.
15. Use `core/EXECUTION_FABRIC.md` + `execution-router` para traduzir a ação em capacidades e eliminar backends incapazes/indisponíveis. Verificadores independentes e gates formais preferem GitHub Actions/CI quando capaz.
16. Quando houver histórico local suficiente, aplique `core/LEARNING_ENGINE.md`/`learning-engine` somente entre candidatos já elegíveis; sem evidência suficiente, preserve baseline.
17. Aplique `core/RISK_MODEL.md`; risco, Project Adoption Gate, System Engineering, contrato semântico, API Engineering, Data Access Efficiency, Independent Verification, Change Hygiene e Definition of Done vencem qualquer preferência aprendida.
18. Para software real novo, use `projects/<slug>/` por padrão e siga `core/INSPECTION_ENVIRONMENT.md` para URL canônica, preview e hospedagem quando aplicável.
19. Consulte `core/WORKFLOW.md` para projeto novo ou manutenção.
20. Carregue somente Skills relevantes.
21. Consulte templates, políticas e referências apenas quando necessários.
22. Antes de criar algo do zero, verifique solução consolidada, componente, biblioteca, template, formalismo ou registry adequado.
23. Não misture tecnologias, protocolos, solvers, scanners ou design systems sem ganho claro.

## Regra de serviço ao usuário

Faça diretamente tudo que estiver ao alcance do agente e for seguro. Não transfira trabalho técnico nem decisões de próximo passo ao usuário apenas por conveniência.

Prefira menos cliques/comandos/reexplicação, contexto incremental, grandes blocos funcionais completos, critérios de aceite derivados da intenção antes da implementação, Project Adoption Gate verde antes do código em projetos governados, decisões técnicas rotineiras autônomas, arquitetura simples mas suficiente e uma implementação final consolidada em vez de patches sucessivos.

Consulte o usuário quando a decisão envolver objetivo de produto, regra de domínio realmente ambígua, preferência subjetiva, gasto, risco destrutivo, credencial/dado indisponível ou decisão legal/organizacional.

## Profundidade do processo

Não aplicar o mesmo ritual a todo trabalho. Projetos pequenos usam planejamento leve; aplicações relevantes/críticas podem usar fluxo completo. Escolha a menor profundidade que preserve segurança, qualidade e continuidade.

Profundidade de processo não autoriza rebaixamento arquitetural. Uma operação simples não precisa de infraestrutura assíncrona pesada; uma operação crítica que possa ficar inconsistente com a perda do cliente não pode ser tratada como simples apenas para reduzir código.

## Continuidade

GitHub é fonte técnica de verdade. Conversas ajudam a pensar, mas estado, decisões, código, testes e próximos passos devem ser recuperáveis do repositório.

Ao retomar, prefira `resume`: contexto incremental + `.factory/state.json` quando existente + `PROJECT_STATE.md`.

Projetos governados pela Factory mantêm `.app-factory.json` schema v2 como resumo machine-readable da adoção/roteamento; ele não substitui documentos ou código.

Quando System Engineering se aplicar, nível, fonte autoritativa, persistência, identidade, autorização e recovery relevantes ficam recuperáveis. Quando operações críticas puderem sobreviver ao navegador/cliente, a arquitetura também deve registrar como responder depois de uma interrupção: **foi executada, até onde chegou e o que ainda falta**.

Em API `contract`/`governed`, consumidores, contrato e compatibilidade/gates ficam recuperáveis em arquitetura/API/contrato machine-readable. Quando aquisição de dados for material, agregadores por caso de uso, paginação, batching/retry, read models/cache e request budget/evidência ficam recuperáveis.

Quando Independent Verification estiver acima de `baseline`, modo, checks, ambiente seguro, thresholds/modelos e exceções ficam recuperáveis em `VERIFICATION.md` e workflows/configs.

Sem learning local em outra máquina, a Factory continua pelo baseline seguro.

## Escopo

Escopo fechado não significa tarefa minúscula. Prefira fatias funcionais completas verificáveis ponta a ponta.

## Validação

Nunca declare concluído só porque código foi escrito. Use `core/DEFINITION_OF_DONE.md` e Skill `verification`.

Em projeto governado pela Factory, `project_adoption_gate.py check --phase delivery` faz parte da revisão final.

Em manutenção/revisão de sistema existente, rode a consolidação de `core/CHANGE_HYGIENE.md` antes da revisão final e reverifique depois da limpeza.

Em `multi-user-system`+, verifique persistência compartilhada real, autorização server-side e System Engineering. Para operações críticas interrompíveis, teste quando material a perda do cliente e a posterior retomada/reconciliação sem duplicidade nem perda de progresso.

## Portabilidade

Leia `PORTABILITY.md`. Evite regras que dependam exclusivamente de fornecedor. Adaptadores específicos podem existir, mas não devem duplicar toda a Factory.
