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
7. Classifique também o nível arquitetural do produto em `core/SYSTEM_ENGINEERING.md`. Para `persistent-app` ou superior, identifique a fonte autoritativa dos dados; para `multi-user-system` ou superior, derive persistência compartilhada, backend/server-side, identidade, autorização, validação, migrations e recovery proporcionais antes de simplificar a arquitetura.
8. Para funcionalidade nova, bugfix relevante, regra de negócio ou mudança de contrato/risco, use `core/SEMANTIC_VERIFICATION.md` + `semantic-verification`: materialize spec e critérios observáveis antes do código; para docs/chore/refactor pequeno sem mudança observável, mantenha processo leve.
9. Use `core/EXECUTION_FABRIC.md` + `execution-router` para traduzir a ação em capacidades e eliminar backends incapazes/indisponíveis.
10. Quando houver histórico local suficiente, aplique `core/LEARNING_ENGINE.md`/`learning-engine` somente entre candidatos já elegíveis; sem evidência suficiente, preserve o baseline.
11. Aplique `core/RISK_MODEL.md`; risco, contrato semântico, System Engineering Contract e Definition of Done vencem qualquer preferência aprendida.
12. Para software real novo, use `projects/<slug>/` como destino padrão e siga `core/INSPECTION_ENVIRONMENT.md` para URL canônica, preview e hospedagem.
13. Consulte `core/WORKFLOW.md` para projeto novo ou manutenção.
14. Carregue somente as Skills relevantes.
15. Consulte templates, políticas e referências apenas quando necessários.
16. Antes de criar algo do zero, verifique se existe solução consolidada, componente, biblioteca, template ou registry adequado.
17. Não misture tecnologias, bibliotecas ou design systems sem ganho claro.

## Regra de serviço ao usuário

Faça diretamente tudo que estiver ao alcance do agente e for seguro. Não transfira trabalho técnico nem decisões de próximo passo ao usuário apenas por conveniência do agente.

Prefira:

- menos cliques;
- menos comandos manuais;
- menos reexplicação de contexto;
- contexto incremental em vez de releitura integral;
- grandes blocos funcionais completos;
- critérios de aceite derivados da intenção antes da implementação quando o trabalho for funcional;
- decisões técnicas rotineiras autônomas;
- arquitetura simples, mas suficiente para o nível real do sistema;
- `current_agent` + GitHub/CI antes de handoff;
- revisão desacoplada/clean-context quando risco médio/alto exigir prova semântica;
- aprendizado local conservador quando houver evidência real suficiente;
- endereço de inspeção simples e estável sob `escolaieda.com/<slug>` quando a infraestrutura estiver configurada;
- explicações simples para decisões relevantes.

Consulte o usuário quando a decisão envolver objetivo de produto, preferência subjetiva, gasto, risco destrutivo, credencial/dado indisponível ou decisão legal/organizacional.

## Profundidade do processo

Não aplicar o mesmo ritual a todo trabalho. Projetos pequenos usam planejamento leve; aplicações relevantes ou críticas podem usar fluxo spec-driven mais completo. A Factory deve escolher a menor profundidade que preserve segurança, qualidade e continuidade.

Profundidade de processo não autoriza rebaixamento arquitetural: um produto pequeno em quantidade de telas ainda pode ser `multi-user-system` se compartilhar dados institucionais entre usuários/dispositivos.

## Continuidade

GitHub é a fonte técnica de verdade. Conversas ajudam a pensar, mas estado, decisões vigentes, código, testes e próximos passos devem ser recuperáveis do repositório.

Ao retomar um projeto, prefira `resume`: contexto incremental + `.factory/state.json` quando existente + `PROJECT_STATE.md` como estado humano durável. `.factory/execution.json` mantém histórico local bounded de tentativas. `.factory/learning.json` mantém somente aprendizado local allowlisted e fica fora do Git por padrão. O cache `.factory/context/` pode ser regenerado e não substitui arquivos reais.

Quando Semantic Verification for aplicável, `specs/semantic-contract.json`, `specs/verification-plan.json` e `specs/review-evidence.json` são artefatos duráveis/versionáveis do projeto. Se código/spec/plano mudarem, revisão stale não deve ser reutilizada.

Quando System Engineering se aplicar, nível do produto, fonte autoritativa de dados e decisões relevantes de persistência/identidade/autorização/recovery devem permanecer recuperáveis no repositório.

Em outra máquina sem o arquivo local de aprendizado, a Factory deve continuar corretamente pelo baseline seguro; aprendizado é otimização, não requisito de continuidade.

Novos projetos devem receber o template `templates/project/AGENTS.md`, que aponta de volta para a App Factory sem duplicar todo o Core.

## Escopo

Escopo fechado não significa tarefa minúscula. Prefira fatias funcionais completas que possam ser verificadas de ponta a ponta.

## Validação

Nunca declare uma mudança concluída apenas porque o código foi escrito. Use `core/DEFINITION_OF_DONE.md` e a Skill `verification`. Quando existir contrato semântico aplicável, testes/gates precisam rastrear os critérios `must` e o review evidence precisa corresponder ao conteúdo atual. Quando o produto for `multi-user-system` ou superior, verifique também persistência compartilhada real, autorização server-side e demais gates de `core/SYSTEM_ENGINEERING.md`. Falhas entram em repair loop limitado; a Execution Fabric pode trocar o backend da tentativa seguinte antes de envolver o usuário. Learning Engine nunca reduz gates para melhorar score/tempo.

## Portabilidade

Leia `PORTABILITY.md`. Evite regras que dependam exclusivamente de um fornecedor. Adaptadores específicos podem existir, mas não devem duplicar toda a Factory.
