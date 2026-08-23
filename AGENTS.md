# AGENTS.md — App Factory

Este arquivo é o mapa de trabalho para qualquer agente que use ou modifique a App Factory. Ele deve permanecer curto; detalhes ficam nos módulos especializados.

## Entrada universal

Pedidos de criação, evolução, manutenção, correção, automação, integração ou continuação de software devem entrar por `skills/factory-router/SKILL.md`, mesmo quando o usuário não mencionar "App Factory".

Leia `core/ENTRYPOINT.md` para o contrato de ativação automática.

A App Factory é **general-purpose**. Sistemas escolares são um domínio válido entre muitos; regras locais de escola, comércio, governo, SaaS, logística, saúde, automação ou outro domínio pertencem ao projeto/perfil e não limitam o Core.

## Antes de agir

1. Entenda o objetivo real do usuário.
2. Leia `core/PRINCIPLES.md`.
3. Siga `core/HUMAN_INTERACTION.md` para decidir o que o agente deve fazer sozinho e o que realmente depende do usuário.
4. Em repositório existente, use `core/CONTEXT_ENGINE.md`/`context-engine` para recuperar mapa incremental e arquivos relevantes.
5. Use `core/AUTONOMY_ENGINE.md`/`autonomy-engine` para recuperar ou inicializar estado e calcular a próxima ação.
6. Classifique a profundidade necessária em `core/PROJECT_SCALE.md`.
7. Classifique também o nível arquitetural em `core/SYSTEM_ENGINEERING.md`. Para `persistent-app` ou superior, identifique fonte autoritativa; para `multi-user-system` ou superior, derive persistência compartilhada, backend/server-side, identidade, autorização, validação, migrations e recovery proporcionais antes de simplificar.
8. Quando existir API/integração/webhook/evento/contrato compartilhado relevante, aplique `core/API_ENGINEERING.md` e `api-engineering`: classifique `none`/`lightweight`/`contract`/`governed`, escolha protocolo/fonte de verdade e gates proporcionais. Backend não implica API formal.
9. Para funcionalidade nova, bugfix relevante, regra de negócio ou mudança de contrato/risco, aplique `core/SEMANTIC_ASSURANCE.md` + `core/SEMANTIC_VERIFICATION.md`: escolha semantic depth `scenario`/`domain`/`formal`, materialize spec antes do código e use `semantic-assurance` em `domain`/`formal`.
10. Em `domain`/`formal`, `specs/semantic-assurance.json` deve estar coerente com fingerprint da spec, sem contradições determinísticas, refs quebradas ou perguntas `blocking`. Property/combinatorial/formal methods entram somente quando a estrutura do domínio justificar.
11. Derive `core/INDEPENDENT_VERIFICATION.md`. Para `independent`/`adversarial`/`release`, carregue `independent-verification` e selecione a menor matriz gratuita/open source que cubra **classes de falha diferentes**. Projetos simples permanecem `baseline`.
12. Ao montar essa matriz, considere superfícies objetivas, não catálogo: workflows GitHub, API, navegador, migrations PostgreSQL, arquitetura declarada, invariantes/estados, combinações finitas, workload/SLO, integrações externas e release. Não rode equivalentes redundantes sem ganho.
13. Use `core/EXECUTION_FABRIC.md` + `execution-router` para traduzir a ação em capacidades e eliminar backends incapazes/indisponíveis. Verificadores independentes e gates formais preferem GitHub Actions/CI quando capaz.
14. Quando houver histórico local suficiente, aplique `core/LEARNING_ENGINE.md`/`learning-engine` somente entre candidatos já elegíveis; sem evidência suficiente, preserve baseline.
15. Aplique `core/RISK_MODEL.md`; risco, contrato semântico, Semantic Assurance, System Engineering, API Engineering, Independent Verification e Definition of Done vencem qualquer preferência aprendida.
16. Para software real novo, use `projects/<slug>/` por padrão e siga `core/INSPECTION_ENVIRONMENT.md` para URL canônica, preview e hospedagem quando aplicável.
17. Consulte `core/WORKFLOW.md` para projeto novo ou manutenção.
18. Carregue somente Skills relevantes.
19. Consulte templates, políticas e referências apenas quando necessários.
20. Antes de criar algo do zero, verifique solução consolidada, componente, biblioteca, template, formalismo ou registry adequado.
21. Não misture tecnologias, protocolos, solvers, scanners ou design systems sem ganho claro.

## Regra de serviço ao usuário

Faça diretamente tudo que estiver ao alcance do agente e for seguro. Não transfira trabalho técnico nem decisões de próximo passo ao usuário apenas por conveniência.

Prefira:

- menos cliques/comandos/reexplicação;
- contexto incremental;
- grandes blocos funcionais completos;
- critérios de aceite derivados da intenção antes da implementação;
- Semantic Assurance proporcional antes de tratar spec complexa como pronta;
- decisões técnicas rotineiras autônomas;
- arquitetura simples, mas suficiente;
- APIs/contratos somente na profundidade necessária;
- métodos formais/property/combinatorial somente quando o problema justificar;
- verificadores independentes por **diversidade de método**, não quantidade de nomes;
- ferramentas gratuitas/open source quando equivalentes adequados existirem;
- `current_agent` + GitHub/CI antes de handoff;
- revisão desacoplada/clean-context quando risco médio/alto exigir prova semântica;
- aprendizado local conservador;
- explicações simples para decisões relevantes.

Consulte o usuário quando a decisão envolver objetivo de produto, regra de domínio realmente ambígua, preferência subjetiva, gasto, risco destrutivo, credencial/dado indisponível ou decisão legal/organizacional. Nunca introduza ferramenta paga para Independent Verification ou método formal por inferência.

## Profundidade do processo

Não aplicar o mesmo ritual a todo trabalho. Projetos pequenos usam planejamento leve; aplicações relevantes/críticas podem usar fluxo completo. Escolha a menor profundidade que preserve segurança, qualidade e continuidade.

Profundidade de processo não autoriza rebaixamento arquitetural. Semantic Assurance segue `scenario → domain → formal`; Independent Verification segue `baseline → independent → adversarial → release`.

A mesma proporcionalidade vale aos motores: actionlint/zizmor exigem workflows; Squawk exige PostgreSQL+migrations; property/combinatorial exige modelo semântico adequado; k6 exige workload/SLO/baseline útil; Toxiproxy exige integração material; RESTler é escalonamento de REST/OpenAPI `governed`; cross-browser só entra quando o produto promete suporte multi-engine.

## Continuidade

GitHub é fonte técnica de verdade. Conversas ajudam a pensar, mas estado, decisões, código, testes e próximos passos devem ser recuperáveis do repositório.

Ao retomar, prefira `resume`: contexto incremental + `.factory/state.json` quando existente + `PROJECT_STATE.md`. `.factory/execution.json` e `.factory/learning.json` ficam locais/bounded por padrão; `.factory/context/` é regenerável.

Quando Semantic Verification se aplicar, `specs/semantic-contract.json`, `specs/verification-plan.json` e `specs/review-evidence.json` são artefatos duráveis/versionáveis. Mudanças podem tornar evidência stale.

Em `domain`/`formal`, `specs/semantic-assurance.json` e decisões específicas em `SEMANTICS.md` permanecem recuperáveis. Semantic diff deve ser considerado antes de reutilizar prova antiga. Modelos property/combinatorial/formal que virarem gates também ficam versionados.

Quando System Engineering se aplicar, nível, fonte autoritativa, persistência, identidade, autorização e recovery relevantes ficam recuperáveis.

Em API `contract`/`governed`, consumidores, contrato e compatibilidade/gates ficam recuperáveis em arquitetura/API/contrato machine-readable.

Quando Independent Verification estiver acima de `baseline`, modo, checks `required/advisory`, ambiente seguro, thresholds/modelos e exceções ficam recuperáveis em `VERIFICATION.md` e workflows/configs.

Sem learning local em outra máquina, a Factory continua pelo baseline seguro.

Novos projetos recebem `templates/project/AGENTS.md`; `SEMANTICS.md` entra somente em `domain`/`formal`; `VERIFICATION.md` entra quando a profundidade justificar.

## Escopo

Escopo fechado não significa tarefa minúscula. Prefira fatias funcionais completas verificáveis ponta a ponta.

## Validação

Nunca declare concluído só porque código foi escrito. Use `core/DEFINITION_OF_DONE.md` e Skill `verification`.

Quando Semantic Assurance for `domain`/`formal`, a spec precisa estar ready antes da implementação. Quando contrato semântico se aplicar, gates rastreiam critérios `must` e review evidence corresponde ao conteúdo atual. Em `multi-user-system`+, verifique persistência compartilhada real, autorização server-side e System Engineering. Em API `contract`/`governed`, verifique contrato/compatibilidade/runtime/segurança. Quando Independent Verification selecionar checks `required`, execute-os em GitHub CI/ambiente equivalente.

Mutation/property/combinatorial testing, Schemathesis/RESTler, ZAP, SAST/supply-chain, migration/architecture checks, load/resilience, browser/accessibility e CI self-check são evidências complementares e condicionais. Nenhum substitui Semantic Assurance ou revisão semântica independente.

Falhas entram em repair loop limitado; Execution Fabric pode trocar backend antes de envolver o usuário. Learning Engine nunca reduz gates para melhorar score/tempo.

## Portabilidade

Leia `PORTABILITY.md`. Evite regras que dependam exclusivamente de fornecedor. Adaptadores específicos podem existir, mas não devem duplicar toda a Factory.
