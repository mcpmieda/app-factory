# AGENTS.md — App Factory

Este arquivo é o mapa de trabalho para qualquer agente que use ou modifique a App Factory. Ele deve permanecer curto; detalhes ficam nos módulos especializados.

## Antes de agir

1. Entenda o objetivo real do usuário.
2. Leia `core/PRINCIPLES.md`.
3. Siga `core/HUMAN_INTERACTION.md` para decidir o que o agente deve fazer sozinho e o que realmente depende do usuário.
4. Use `core/TASK_ROUTER.md` para escolher ChatGPT, Codex ou outro ambiente adequado.
5. Aplique `core/RISK_MODEL.md`.
6. Consulte `core/WORKFLOW.md` para projeto novo ou manutenção.
7. Carregue somente as Skills relevantes.
8. Consulte templates, políticas e referências apenas quando necessários.
9. Antes de criar algo do zero, verifique se existe solução consolidada, componente, biblioteca, template ou registry adequado.
10. Não misture tecnologias, bibliotecas ou design systems sem ganho claro.

## Regra de serviço ao usuário

Faça diretamente tudo que estiver ao alcance do agente e for seguro. Não transfira trabalho técnico ao usuário apenas por conveniência do agente.

Prefira:

- menos cliques;
- menos comandos manuais;
- menos reexplicação de contexto;
- grandes blocos funcionais completos;
- decisões técnicas rotineiras autônomas;
- explicações simples para decisões relevantes.

Consulte o usuário quando a decisão envolver objetivo de produto, preferência subjetiva, gasto, risco destrutivo, dados indisponíveis ou autorização não coberta.

## Continuidade

GitHub é a fonte técnica de verdade. Conversas ajudam a pensar, mas estado, decisões vigentes, código, testes e próximos passos devem ser recuperáveis do repositório.

Ao retomar um projeto, leia primeiro `PROJECT_STATE.md` quando existir; depois siga os links para produto, arquitetura e decisões.

## Escopo

Escopo fechado não significa tarefa minúscula. Prefira fatias funcionais completas que possam ser verificadas de ponta a ponta.

## Validação

Nunca declare uma mudança concluída apenas porque o código foi escrito. Use `core/DEFINITION_OF_DONE.md` e a Skill `verification`.

## Portabilidade

Leia `PORTABILITY.md`. Evite regras que dependam exclusivamente de um fornecedor. Adaptadores específicos podem existir, mas não devem duplicar toda a Factory.