# AGENTS.md — App Factory

Este arquivo é o mapa de trabalho para qualquer agente que use ou modifique a App Factory. Ele deve permanecer curto; detalhes ficam nos módulos especializados.

## Entrada universal

Pedidos de criação, evolução, manutenção, correção, automação, integração ou continuação de software devem entrar por `skills/factory-router/SKILL.md`, mesmo quando o usuário não mencionar "App Factory".

Leia `core/ENTRYPOINT.md` para o contrato de ativação automática.

A App Factory é **general-purpose**. Sistemas escolares são um domínio válido entre muitos; regras locais de escola, comércio, governo, SaaS, logística, saúde, automação ou outro domínio pertencem ao projeto/perfil e não limitam o Core.

## Project Adoption Gate

Quando o usuário escolher explicitamente a App Factory para um projeto, quando o projeto vier de um starter da Factory ou quando o repositório já declarar governança pela Factory, **carregue `skills/project-adoption/SKILL.md` e aplique `core/PROJECT_ADOPTION_GATE.md` antes da primeira alteração funcional/visual material**.

Adoção não pode ser apenas nominal ou retroativa. Antes do código, o projeto governado deve tornar recuperáveis pelo menos `AGENTS.md`, `PROJECT_STATE.md`, `.app-factory.json`, classificações de escala/risco/system level/API/Semantic/Independent Verification e, em UI material, design system + Professional UI + Motion Profile. Quando Semantic Verification for requerida, specs/planos exigidos entram antes da implementação.

Execute quando disponível:

```text
project_adoption_gate.py check --phase pre-implementation
```

Um `web-admin` não pode cair silenciosamente em React + CSS próprio como fundação visual: shadcn/ui é o default validado, HeroUI é override transversal quando escolhido e base ad hoc exige desvio explícito. HeroUI principal herda `ambient-constellation strong`.

Projetos legados externos usados apenas para correção pontual não recebem governança durável por reflexo; o gate passa a ser obrigatório quando a Factory é a governança do projeto.

## Antes de agir

1. Entenda o objetivo real do usuário.
2. Leia `core/PRINCIPLES.md`.
3. Siga `core/HUMAN_INTERACTION.md` para decidir o que o agente deve fazer sozinho e o que realmente depende do usuário.
4. Em repositório existente, use `core/CONTEXT_ENGINE.md`/`context-engine` para recuperar mapa incremental e arquivos relevantes.
5. Se o Project Adoption Gate se aplicar, materialize/valide a adoção **antes** de implementação material; recuperação de um projeto já iniciado deve registrar honestamente a lacuna em vez de fingir conformidade retroativa.
6. Em evolução, manutenção, refactor, debugging, modernização ou revisão de código existente, aplique `core/CHANGE_HYGIENE.md` e `maintenance`: preserve comportamento estável sem preservar implementação obsoleta, consolide repair loops e não entregue camadas de tentativas acumuladas.
7. Use `core/AUTONOMY_ENGINE.md`/`autonomy-engine` para recuperar ou inicializar estado e calcular a próxima ação.
8. Classifique a profundidade necessária em `core/PROJECT_SCALE.md`.
9. Classifique também o nível arquitetural em `core/SYSTEM_ENGINEERING.md`. Para `persistent-app` ou superior, identifique fonte autoritativa; para `multi-user-system` ou superior, derive persistência compartilhada, backend/server-side, identidade, autorização, validação, migrations e recovery proporcionais antes de simplificar.
10. Quando existir API/integração/webhook/evento/contrato compartilhado relevante, aplique `core/API_ENGINEERING.md` e `api-engineering`: classifique `none`/`lightweight`/`contract`/`governed`, escolha protocolo/fonte de verdade e gates proporcionais. Backend não implica API formal. Para telas/fluxos data-driven que cruzem rede, aplique também `core/DATA_ACCESS_EFFICIENCY.md`: evite frontend `chatty`, N+1 e chamadas redundantes; prefira composição orientada ao caso de uso, batching/paralelismo, paginação, retry/rate-limit e read models somente quando trouxerem ganho real. Esta regra também vale para Server Actions/Server Components/RPC mesmo sem API pública formal.
11. Para funcionalidade nova, bugfix relevante, regra de negócio ou mudança de contrato/risco, aplique `core/SEMANTIC_ASSURANCE.md` + `core/SEMANTIC_VERIFICATION.md`: escolha semantic depth `scenario`/`domain`/`formal`, materialize spec antes do código e use `semantic-assurance` em `domain`/`formal`.
12. Em `domain`/`formal`, `specs/semantic-assurance.json` deve estar coerente com fingerprint da spec, sem contradições determinísticas, refs quebradas ou perguntas `blocking`. Property/combinatorial/formal methods entram somente quando a estrutura do domínio justificar.
13. Derive `core/INDEPENDENT_VERIFICATION.md`. Para `independent`/`adversarial`/`release`, carregue `independent-verification` e selecione a menor matriz gratuita/open source que cubra **classes de falha diferentes**. Projetos simples permanecem `baseline`.
14. Ao montar essa matriz, considere superfícies objetivas, não catálogo: workflows GitHub, API, navegador, migrations PostgreSQL, arquitetura declarada, invariantes/estados, combinações finitas, workload/SLO, integrações externas e release. Não rode equivalentes redundantes sem ganho.
15. Use `core/EXECUTION_FABRIC.md` + `execution-router` para traduzir a ação em capacidades e eliminar backends incapazes/indisponíveis. Verificadores independentes e gates formais preferem GitHub Actions/CI quando capaz.
16. Quando houver histórico local suficiente, aplique `core/LEARNING_ENGINE.md`/`learning-engine` somente entre candidatos já elegíveis; sem evidência suficiente, preserve baseline.
17. Aplique `core/RISK_MODEL.md`; risco, Project Adoption Gate, contrato semântico, Semantic Assurance, System Engineering, API Engineering, Data Access Efficiency, Independent Verification, Change Hygiene e Definition of Done vencem qualquer preferência aprendida.
18. Para software real novo, use `projects/<slug>/` por padrão e siga `core/INSPECTION_ENVIRONMENT.md` para URL canônica, preview e hospedagem quando aplicável.
19. Consulte `core/WORKFLOW.md` para projeto novo ou manutenção.
20. Carregue somente Skills relevantes.
21. Consulte templates, políticas e referências apenas quando necessários.
22. Antes de criar algo do zero, verifique solução consolidada, componente, biblioteca, template, formalismo ou registry adequado.
23. Não misture tecnologias, protocolos, solvers, scanners ou design systems sem ganho claro.

## Regra de serviço ao usuário

Faça diretamente tudo que estiver ao alcance do agente e for seguro. Não transfira trabalho técnico nem decisões de próximo passo ao usuário apenas por conveniência.

Prefira:

- menos cliques/comandos/reexplicação;
- contexto incremental;
- grandes blocos funcionais completos;
- critérios de aceite derivados da intenção antes da implementação;
- Project Adoption Gate verde antes do código em projetos governados pela Factory;
- Semantic Assurance proporcional antes de tratar spec complexa como pronta;
- decisões técnicas rotineiras autônomas;
- arquitetura simples, mas suficiente;
- APIs/contratos somente na profundidade necessária;
- aquisição de dados eficiente: cliente pede o caso de uso, backend compõe quando apropriado, sem regra artificial de "uma chamada por tela" nem endpoint gigante;
- métodos formais/property/combinatorial somente quando o problema justificar;
- verificadores independentes por **diversidade de método**, não quantidade de nomes;
- ferramentas gratuitas/open source quando equivalentes adequados existirem;
- `current_agent` + GitHub/CI antes de handoff;
- revisão desacoplada/clean-context quando risco médio/alto exigir prova semântica;
- manutenção com uma implementação final consolidada em vez de patches sucessivos;
- aprendizado local conservador;
- explicações simples para decisões relevantes.

Consulte o usuário quando a decisão envolver objetivo de produto, regra de domínio realmente ambígua, preferência subjetiva, gasto, risco destrutivo, credencial/dado indisponível ou decisão legal/organizacional. Nunca introduza ferramenta paga para Independent Verification ou método formal por inferência.

## Profundidade do processo

Não aplicar o mesmo ritual a todo trabalho. Projetos pequenos usam planejamento leve; aplicações relevantes/críticas podem usar fluxo completo. Escolha a menor profundidade que preserve segurança, qualidade e continuidade.

Profundidade de processo não autoriza rebaixamento arquitetural. Semantic Assurance segue `scenario → domain → formal`; Independent Verification segue `baseline → independent → adversarial → release`.

A mesma proporcionalidade vale aos motores: actionlint/zizmor exigem workflows; Squawk exige PostgreSQL+migrations; property/combinatorial exige modelo semântico adequado; k6 exige workload/SLO/baseline útil; Toxiproxy exige integração material; RESTler é escalonamento de REST/OpenAPI `governed`; cross-browser só entra quando o produto promete suporte multi-engine. Change Hygiene também é proporcional: scanner stdlib-first é leve; Knip/Stylelint/Vulture/jscpd entram somente quando stack, risco e configuração justificarem. Data Access Efficiency também é proporcional: agregação, batching, cache, read model e request budget só entram quando custo/latência/quota/estabilidade justificarem.

## Continuidade

GitHub é fonte técnica de verdade. Conversas ajudam a pensar, mas estado, decisões, código, testes e próximos passos devem ser recuperáveis do repositório.

Ao retomar, prefira `resume`: contexto incremental + `.factory/state.json` quando existente + `PROJECT_STATE.md`. `.factory/execution.json` e `.factory/learning.json` ficam locais/bounded por padrão; `.factory/context/` é regenerável.

Projetos governados pela Factory mantêm `.app-factory.json` schema v2 como resumo machine-readable da adoção/roteamento; ele não substitui documentos ou código, mas impede que outra conversa perca a decisão de processo/design/risco.

Quando Semantic Verification se aplicar, `specs/semantic-contract.json`, `specs/verification-plan.json` e `specs/review-evidence.json` são artefatos duráveis/versionáveis. Mudanças podem tornar evidência stale.

Em `domain`/`formal`, `specs/semantic-assurance.json` e decisões específicas em `SEMANTICS.md` permanecem recuperáveis. Semantic diff deve ser considerado antes de reutilizar prova antiga. Modelos property/combinatorial/formal que virarem gates também ficam versionados.

Quando System Engineering se aplicar, nível, fonte autoritativa, persistência, identidade, autorização e recovery relevantes ficam recuperáveis.

Em API `contract`/`governed`, consumidores, contrato e compatibilidade/gates ficam recuperáveis em arquitetura/API/contrato machine-readable. Quando aquisição de dados for material, agregadores por caso de uso, paginação, batching/retry, read models/cache e request budget/evidência ficam recuperáveis em `ARCHITECTURE.md`, `API.md` ou equivalente conforme `core/DATA_ACCESS_EFFICIENCY.md`.

Quando Independent Verification estiver acima de `baseline`, modo, checks `required/advisory`, ambiente seguro, thresholds/modelos e exceções ficam recuperáveis em `VERIFICATION.md` e workflows/configs.

Sem learning local em outra máquina, a Factory continua pelo baseline seguro.

Novos projetos recebem `templates/project/AGENTS.md`; `SEMANTICS.md` entra somente em `domain`/`formal`; `VERIFICATION.md` entra quando a profundidade justificar.

## Escopo

Escopo fechado não significa tarefa minúscula. Prefira fatias funcionais completas verificáveis ponta a ponta.

## Validação

Nunca declare concluído só porque código foi escrito. Use `core/DEFINITION_OF_DONE.md` e Skill `verification`.

Em projeto governado pela Factory, `project_adoption_gate.py check --phase delivery` (ou checklist equivalente) faz parte da revisão final.

Em manutenção/revisão de sistema existente, rode a consolidação de `core/CHANGE_HYGIENE.md` antes da revisão final e reverifique depois da limpeza. O fato de um bug ter desaparecido não basta se a solução ainda depende de código morto, shadow implementation, override acumulado ou tentativa temporária.

Quando Semantic Assurance for `domain`/`formal`, a spec precisa estar ready antes da implementação. Quando contrato semântico se aplicar, gates rastreiam critérios `must` e review evidence corresponde ao conteúdo atual. Em `multi-user-system`+, verifique persistência compartilhada real, autorização server-side e System Engineering. Em API `contract`/`governed`, verifique contrato/compatibilidade/runtime/segurança. Em fluxo data-driven material, verifique N+1, chamadas redundantes, paginação, rate-limit/retry e request budget quando aplicáveis. Quando Independent Verification selecionar checks `required`, execute-os em GitHub CI/ambiente equivalente.

Mutation/property/combinatorial testing, Schemathesis/RESTler, ZAP, SAST/supply-chain, migration/architecture checks, load/resilience, browser/accessibility e CI self-check são evidências complementares e condicionais. Nenhum substitui Semantic Assurance ou revisão semântica independente.

Falhas entram em repair loop limitado; Execution Fabric pode trocar backend antes de envolver o usuário. Learning Engine nunca reduz gates para melhorar score/tempo. Ao sair do repair loop com solução válida, Change Hygiene consolida o estado antes da entrega.

## Portabilidade

Leia `PORTABILITY.md`. Evite regras que dependam exclusivamente de fornecedor. Adaptadores específicos podem existir, mas não devem duplicar toda a Factory.
