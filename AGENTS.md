# AGENTS.md — App Factory

Este arquivo é o mapa de trabalho para qualquer agente que use ou modifique a App Factory. Ele deve permanecer curto; detalhes ficam nos módulos especializados.

## Entrada universal

Pedidos de criação, evolução, manutenção, correção, automação, integração ou continuação de software devem entrar por `skills/factory-router/SKILL.md`, mesmo quando o usuário não mencionar "App Factory".

Leia `core/ENTRYPOINT.md` para o contrato de ativação automática.

## Antes de agir

1. Entenda o objetivo real do usuário.
2. Leia `core/PRINCIPLES.md`.
3. Siga `core/HUMAN_INTERACTION.md` para decidir o que o agente deve fazer sozinho e o que realmente depende do usuário.
4. Em repositório existente, use `core/CONTEXT_ENGINE.md`/`context-engine` para recuperar mapa incremental e arquivos relevantes.
5. Use `core/AUTONOMY_ENGINE.md`/`autonomy-engine` para recuperar ou inicializar estado e calcular a próxima ação.
6. Classifique a profundidade necessária em `core/PROJECT_SCALE.md`.
7. Use `core/TASK_ROUTER.md` para escolher a capacidade/executor adequado, priorizando current-agent + GitHub/CI.
8. Aplique `core/RISK_MODEL.md`.
9. Consulte `core/WORKFLOW.md` para projeto novo ou manutenção.
10. Carregue somente as Skills relevantes.
11. Consulte templates, políticas e referências apenas quando necessários.
12. Antes de criar algo do zero, verifique se existe solução consolidada, componente, biblioteca, template ou registry adequado.
13. Não misture tecnologias, bibliotecas ou design systems sem ganho claro.

## Regra de serviço ao usuário

Faça diretamente tudo que estiver ao alcance do agente e for seguro. Não transfira trabalho técnico nem decisões de próximo passo ao usuário apenas por conveniência do agente.

Prefira:

- menos cliques;
- menos comandos manuais;
- menos reexplicação de contexto;
- contexto incremental em vez de releitura integral;
- grandes blocos funcionais completos;
- decisões técnicas rotineiras autônomas;
- current-agent + GitHub/CI antes de handoff;
- explicações simples para decisões relevantes.

Consulte o usuário quando a decisão envolver objetivo de produto, preferência subjetiva, gasto, risco destrutivo, credencial/dado indisponível ou decisão legal/organizacional.

## Profundidade do processo

Não aplicar o mesmo ritual a todo trabalho. Projetos pequenos usam planejamento leve; aplicações relevantes ou críticas podem usar fluxo spec-driven mais completo. A Factory deve escolher a menor profundidade que preserve segurança, qualidade e continuidade.

## Continuidade

GitHub é a fonte técnica de verdade. Conversas ajudam a pensar, mas estado, decisões vigentes, código, testes e próximos passos devem ser recuperáveis do repositório.

Ao retomar um projeto, prefira `resume`: contexto incremental + `.factory/state.json` quando existente + `PROJECT_STATE.md` como estado humano durável. O cache `.factory/context/` pode ser regenerado e não substitui arquivos reais.

Novos projetos devem receber o template `templates/project/AGENTS.md`, que aponta de volta para a App Factory sem duplicar todo o Core.

## Escopo

Escopo fechado não significa tarefa minúscula. Prefira fatias funcionais completas que possam ser verificadas de ponta a ponta.

## Validação

Nunca declare uma mudança concluída apenas porque o código foi escrito. Use `core/DEFINITION_OF_DONE.md` e a Skill `verification`. Falhas entram em repair loop limitado antes de escalada.

## Portabilidade

Leia `PORTABILITY.md`. Evite regras que dependam exclusivamente de um fornecedor. Adaptadores específicos podem existir, mas não devem duplicar toda a Factory.
