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
8. Quando existir API/integração/webhook/evento ou contrato compartilhado relevante, aplique `core/API_ENGINEERING.md` e `api-engineering`: classifique `none`/`lightweight`/`contract`/`governed`, escolha protocolo/fonte de verdade e gates proporcionais. Não crie API formal apenas porque existe backend.
9. Para funcionalidade nova, bugfix relevante, regra de negócio ou mudança de contrato/risco, aplique `core/SEMANTIC_ASSURANCE.md` + `core/SEMANTIC_VERIFICATION.md`: escolha semantic depth `scenario`/`domain`/`formal`, materialize spec antes do código e use `semantic-assurance` em `domain`/`formal` para validar a qualidade da especificação antes de implementar.
10. Em `domain`/`formal`, `specs/semantic-assurance.json` deve estar coerente com o fingerprint da spec, sem contradições determinísticas, refs quebradas ou perguntas `blocking`. Z3/Alloy/FRET/P/Quint/TLA+/DMN/OPA/Cedar entram somente quando o tipo de propriedade justificar.
11. Derive a profundidade de `core/INDEPENDENT_VERIFICATION.md`. Para `independent`/`adversarial`/`release`, carregue `independent-verification` e selecione apenas motores gratuitos/open source aplicáveis. Projetos simples permanecem `baseline`.
12. Use `core/EXECUTION_FABRIC.md` + `execution-router` para traduzir a ação em capacidades e eliminar backends incapazes/indisponíveis. Verificadores independentes e gates formais devem preferir GitHub Actions/CI quando esse backend puder executar a prova.
13. Quando houver histórico local suficiente, aplique `core/LEARNING_ENGINE.md`/`learning-engine` somente entre candidatos já elegíveis; sem evidência suficiente, preserve o baseline.
14. Aplique `core/RISK_MODEL.md`; risco, contrato semântico, Semantic Assurance, System Engineering Contract, API Engineering Contract, Independent Verification quando aplicável e Definition of Done vencem qualquer preferência aprendida.
15. Para software real novo, use `projects/<slug>/` como destino padrão e siga `core/INSPECTION_ENVIRONMENT.md` para URL canônica, preview e hospedagem.
16. Consulte `core/WORKFLOW.md` para projeto novo ou manutenção.
17. Carregue somente as Skills relevantes.
18. Consulte templates, políticas e referências apenas quando necessários.
19. Antes de criar algo do zero, verifique se existe solução consolidada, componente, biblioteca, template, formalismo ou registry adequado.
20. Não misture tecnologias, bibliotecas, protocolos, solvers, scanners ou design systems sem ganho claro.

## Regra de serviço ao usuário

Faça diretamente tudo que estiver ao alcance do agente e for seguro. Não transfira trabalho técnico nem decisões de próximo passo ao usuário apenas por conveniência do agente.

Prefira:

- menos cliques;
- menos comandos manuais;
- menos reexplicação de contexto;
- contexto incremental em vez de releitura integral;
- grandes blocos funcionais completos;
- critérios de aceite derivados da intenção antes da implementação quando o trabalho for funcional;
- Semantic Assurance proporcional antes de tratar uma spec complexa como pronta;
- decisões técnicas rotineiras autônomas;
- arquitetura simples, mas suficiente para o nível real do sistema;
- APIs/contratos somente na profundidade que consumidores e risco realmente exigirem;
- métodos formais somente quando o tipo de problema justificar;
- verificadores independentes somente quando risco/arquitetura justificarem;
- ferramentas gratuitas/open source quando equivalentes adequados existirem;
- `current_agent` + GitHub/CI antes de handoff;
- revisão desacoplada/clean-context quando risco médio/alto exigir prova semântica;
- aprendizado local conservador quando houver evidência real suficiente;
- endereço de inspeção simples e estável sob `escolaieda.com/<slug>` quando a infraestrutura estiver configurada;
- explicações simples para decisões relevantes.

Consulte o usuário quando a decisão envolver objetivo de produto, regra de domínio realmente ambígua, preferência subjetiva, gasto, risco destrutivo, credencial/dado indisponível ou decisão legal/organizacional. Nunca introduza ferramenta paga para Independent Verification ou método formal por inferência.

## Profundidade do processo

Não aplicar o mesmo ritual a todo trabalho. Projetos pequenos usam planejamento leve; aplicações relevantes ou críticas podem usar fluxo spec-driven mais completo. A Factory deve escolher a menor profundidade que preserve segurança, qualidade e continuidade.

Profundidade de processo não autoriza rebaixamento arquitetural: um produto pequeno em quantidade de telas ainda pode ser `multi-user-system` se compartilhar dados institucionais entre usuários/dispositivos. Da mesma forma, uma API interna simples pode permanecer `lightweight`, enquanto uma interface pública/compartilhada pode exigir modo `contract`/`governed` mesmo em um projeto pequeno. Semantic Assurance segue `scenario → domain → formal`; Independent Verification segue `baseline → independent → adversarial → release`.

## Continuidade

GitHub é a fonte técnica de verdade. Conversas ajudam a pensar, mas estado, decisões vigentes, código, testes e próximos passos devem ser recuperáveis do repositório.

Ao retomar um projeto, prefira `resume`: contexto incremental + `.factory/state.json` quando existente + `PROJECT_STATE.md` como estado humano durável. `.factory/execution.json` mantém histórico local bounded de tentativas. `.factory/learning.json` mantém somente aprendizado local allowlisted e fica fora do Git por padrão. O cache `.factory/context/` pode ser regenerado e não substitui arquivos reais.

Quando Semantic Verification for aplicável, `specs/semantic-contract.json`, `specs/verification-plan.json` e `specs/review-evidence.json` são artefatos duráveis/versionáveis do projeto. Se código/spec/plano mudarem, revisão stale não deve ser reutilizada.

Quando semantic depth for `domain`/`formal`, `specs/semantic-assurance.json` e decisões específicas em `SEMANTICS.md` devem permanecer recuperáveis. Semantic diff deve ser considerado antes de reutilizar testes/review antigos.

Quando System Engineering se aplicar, nível do produto, fonte autoritativa de dados e decisões relevantes de persistência/identidade/autorização/recovery devem permanecer recuperáveis no repositório.

Quando API Engineering estiver em modo `contract`/`governed`, modo, consumidores, fonte de verdade do contrato e decisões de compatibilidade/gates também devem permanecer recuperáveis, preferencialmente em `ARCHITECTURE.md`, `API.md` e no próprio contrato machine-readable.

Quando Independent Verification estiver acima de `baseline`, modo, checks `required/advisory`, ambiente seguro de teste, thresholds e exceções devem permanecer recuperáveis, preferencialmente em `VERIFICATION.md` e workflows/configs versionados.

Em outra máquina sem o arquivo local de aprendizado, a Factory deve continuar corretamente pelo baseline seguro; aprendizado é otimização, não requisito de continuidade.

Novos projetos devem receber o template `templates/project/AGENTS.md`, que aponta de volta para a App Factory sem duplicar todo o Core. `templates/project/SEMANTICS.md` entra somente em `domain`/`formal`; `templates/project/VERIFICATION.md` entra quando a profundidade de verificação justificar.

## Escopo

Escopo fechado não significa tarefa minúscula. Prefira fatias funcionais completas que possam ser verificadas de ponta a ponta.

## Validação

Nunca declare uma mudança concluída apenas porque o código foi escrito. Use `core/DEFINITION_OF_DONE.md` e a Skill `verification`. Quando Semantic Assurance for `domain`/`formal`, a especificação precisa estar ready antes da implementação. Quando existir contrato semântico aplicável, testes/gates precisam rastrear os critérios `must` e o review evidence precisa corresponder ao conteúdo atual. Quando o produto for `multi-user-system` ou superior, verifique também persistência compartilhada real, autorização server-side e demais gates de `core/SYSTEM_ENGINEERING.md`. Quando houver API `contract`/`governed`, verifique contrato, compatibilidade, comportamento runtime e segurança conforme `core/API_ENGINEERING.md`. Quando Independent Verification selecionar checks `required`, execute-os em GitHub CI/ambiente equivalente; mutation testing, Schemathesis, OWASP ZAP, Semgrep, Trivy, axe/Lighthouse são evidências complementares e não substituem Semantic Assurance/revisão semântica independente. Falhas entram em repair loop limitado; a Execution Fabric pode trocar o backend da tentativa seguinte antes de envolver o usuário. Learning Engine nunca reduz gates para melhorar score/tempo.

## Portabilidade

Leia `PORTABILITY.md`. Evite regras que dependam exclusivamente de um fornecedor. Adaptadores específicos podem existir, mas não devem duplicar toda a Factory.
