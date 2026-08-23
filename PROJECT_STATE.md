# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Manter a **App Factory V1.4 estável** como baseline recuperável, autônomo, adaptativo e semanticamente verificável para criação/evolução de software, com hardenings posteriores que impedem falsa completude, adicionam governança proporcional de APIs, verificam a qualidade da própria especificação com **Semantic Assurance** e acrescentam verificação técnica independente gratuita sem alterar os engines V1.1–V1.4.

## Estado

- fase: `V1.4 — estável + governance hardening`;
- versão: `1.4.0`;
- versão dos engines/plugin baseline: `1.4.0`;
- baseline publicada anterior preservada: tag/release `v1.0.0`;
- V1.1 / Issue #32: Context Engine + Autonomy Engine concluídos;
- V1.2 / Issue #36: Execution Fabric + CI Executor concluídos;
- V1.3 / Issue #38: Learning Engine concluído;
- V1.4 / Issue #41: Semantic Verification Layer implementado para a release V1.4;
- System Engineering Contract: classifica `website`/`local-app`/`persistent-app`/`multi-user-system`/`production-system`/`critical-system`, proíbe falsa persistência e torna arquitetura proporcional um gate;
- API Engineering Contract: governança condicional `none`/`lightweight`/`contract`/`governed`, seleção de protocolo, contract-first quando necessário, compatibilidade, segurança e gates executáveis;
- Semantic Assurance Contract: classifica a profundidade da especificação em `scenario`/`domain`/`formal`, normaliza requisitos inspirados em EARS/FRET, mantém domínio/referências explícitos, detecta inconsistências determinísticas, mede rastreabilidade estrutural e calcula semantic diff/impacto antes da implementação;
- Semantic Assurance engine: `engine/semantic_assurance.py` valida IDs/referências, cardinalidades/ranges/enums, dependências conflitantes, perguntas `blocking`, cobertura requisito→AC/invariante→gate e recomenda formalização proporcional sem transformar análise probabilística em prova;
- métodos formais/estruturados preferidos quando realmente aplicáveis: Z3/SMT para restrições, Alloy para relações/cardinalidades, NASA FRET/FRETish para requisitos temporais/reativos, P ou Quint/TLA+ para estados/concorrência/distribuição, DMN para decisões e OPA/Rego ou Cedar para policy/autorização;
- property/stateful/model-based testing: capacidade condicional derivada de invariantes, ranges e máquinas de estado; não substitui exemplos `given/when/then` nem é adicionada a lógica trivial;
- Independent Verification Contract: classifica `baseline`/`independent`/`adversarial`/`release`, usa matriz `free-only` e adiciona evidência determinística independente da IA implementadora sem substituir Semantic Assurance/Verification;
- Independent Verification planner: `engine/independent_verification.py` detecta linguagem/UI/testes/contrato API e seleciona Trivy, Semgrep CE, StrykerJS/mutmut, Schemathesis, OWASP ZAP, axe-core e Lighthouse CI proporcionalmente;
- API standards/tooling preferidos quando aplicáveis: OpenAPI, GraphQL, gRPC/Protobuf, AsyncAPI, Arazzo, RFC 9110, RFC 9457, OWASP API Security, Redocly CLI, oasdiff, Schemathesis e Pact condicional;
- Context Engine: incremental, stdlib, SHA-256, delta `added/changed/removed`, stack/símbolos/imports/dependências locais e exclusão de segredos/build/dependencies/binários;
- Autonomy Engine: `init/status/next/resume/record`, transições explícitas, repair loop default 3, intervenção humana categorizada e fase `specification` quando `spec_required=true`;
- Semantic Verification: `specs/semantic-contract.json` + `specs/verification-plan.json` + `specs/review-evidence.json`, critérios `given/when/then`, fingerprints contra evidência stale e revisão desacoplada para risco médio/alto;
- Semantic Assurance em projetos `domain`/`formal`: `specs/semantic-assurance.json` aponta para o fingerprint do contrato semântico e `SEMANTICS.md` registra somente decisões/limites humanos específicos do projeto;
- clean-context review: `engine/review_packet.py` produz pacote de revisão com spec + diff atual, sem depender do raciocínio da implementação ou de aprovação anterior;
- Execution Fabric: roteamento por capacidades, backends `current_agent/github_ci/sandbox/local_full`, fallback escopado pela tarefa atual e histórico operacional bounded; GitHub CI é executor preferido de gates determinísticos/formais/Independent Verification quando capaz;
- CI Executor: gates declarados/allowlisted, sem comandos de prompt, `shell=False`, sem secrets por padrão, instalação reproduzível somente com lockfile compatível e suporte condicional a `test:visual`;
- Learning Engine: **local-only**, bounded, sem telemetria externa, metadados técnicos allowlisted, amostra mínima/prior conservador e explicação `baseline/learned/insufficient-data`;
- aprendizado: incapacidade, indisponibilidade, failure threshold, risco, contratos arquiteturais/API/semantic-assurance/semantic-verification/independent-verification e Definition of Done sempre vencem score histórico;
- velocidade aprendida: usa duração mediana de execuções bem-sucedidas; falha rápida não melhora preferência;
- `local_full`: não pode ser promovido sobre backend leve capaz somente por aprendizado;
- perfil `web-admin`: `v1`;
- perfis `website`, `web-app`, `chrome-extension` e `automation`: `validated`;
- Skills portáteis: **19**, incluindo `api-engineering`, `semantic-assurance` e `independent-verification`;
- CI: gates V1 anteriores preservados + `Validate V1.4 Semantic Verification` + `Validate System Engineering Contract` + `Validate API Engineering Contract` + `Validate Semantic Assurance` + `Validate Independent Verification`.

## Decisões vigentes

- intenção de software ativa a Factory automaticamente;
- AI serve ao objetivo, não ao texto literal do prompt;
- GitHub é a fonte técnica de verdade; conversa não é a autoridade operacional;
- `resume`/Context Engine recuperam contexto antes de depender de memória de conversa;
- `.factory/context/` é cache regenerável, não fonte de verdade;
- `.factory/state.json` mantém continuidade do Autonomy Engine e pode ser versionado em handoffs importantes;
- `.factory/execution.json` mantém histórico bounded local de tentativas e fica fora do Git por padrão;
- `.factory/learning.json` mantém aprendizado local allowlisted e fica fora do Git por padrão;
- ausência do arquivo de learning em outra máquina não bloqueia continuidade: a Factory usa o baseline seguro e reaprende;
- o agente calcula próxima ação, necessidade de spec, nível do sistema, modo da API, **semantic depth**, profundidade de Independent Verification e executor; o usuário não conduz fases técnicas rotineiras nem escolhe solver/model checker/scanner manualmente;
- System Engineering decide profundidade mínima do produto; processo leve não pode rebaixar arquitetura real;
- API Engineering só entra quando existe fronteira de API/integração relevante; backend não implica OpenAPI automaticamente;
- API `contract`/`governed` possui fonte de verdade machine-readable adequada ao protocolo e compatibilidade/gates proporcionais;
- REST não é obrigatório: protocolo é escolhido pelo comportamento; GraphQL, gRPC, AsyncAPI e Arazzo são condicionais;
- Semantic Assurance decide a qualidade/profundidade da própria especificação; Semantic Verification prova implementação↔spec; API Engineering governa interfaces; Independent Verification fornece evidência técnica externa; não duplicar responsabilidades;
- `scenario` é o default semântico leve quando invariantes + critérios observáveis bastam; `domain` só entra quando conceitos/relações/papéis/estados/regras interagem; `formal` só entra quando a natureza/criticidade do problema justificar;
- requisitos `domain`/`formal` usam estrutura inspirada em EARS/FRET (scope/precondition/trigger/component/response/timing + refs), sem exigir runtime Cucumber nem sintaxe textual universal;
- `semantic-assurance.json` não duplica OpenAPI, schema de banco ou arquitetura; ele guarda somente domínio/requisitos/consistência/rastreabilidade que alteram significado;
- coverage semântica é cobertura estrutural de rastreabilidade, não “percentual de verdade”; 100% não prova que a interpretação humana original está correta;
- findings probabilísticos de IA são hipóteses/advisory até serem resolvidos por estrutura, prova formal/determinística ou decisão humana de domínio;
- semantic diff usa IDs estáveis/fingerprints e propaga impacto a requisitos, ACs, invariantes e gates declarados; evidência afetada precisa ser refeita;
- Z3, Alloy, FRET, P, Quint/TLA+, DMN, OPA/Rego e Cedar são opções condicionais e substituíveis; nenhuma vira dependência universal;
- formalização só conta como prova quando possui artefato versionado, `source_refs` e gate executado quando marcada `required`;
- métodos formais provam propriedades do modelo fornecido, não que o modelo representa perfeitamente o desejo humano; assumptions/limites permanecem explícitos;
- Independent Verification é `free-only` por padrão: não exige segunda IA paga, SaaS comercial ou scanner premium;
- GitHub Actions é o executor preferido dos scanners/gates determinísticos quando capaz; runner próprio/local é fallback quando minutos/custo forem problema;
- projetos simples permanecem `baseline`; sistemas reais/alto risco sobem para `independent`, `adversarial` ou `release` somente quando sinais objetivos justificarem;
- Trivy/Semgrep/axe são verificadores independentes de custo baixo/moderado; mutation testing, Schemathesis e ZAP entram conforme risco/superfície; Lighthouse exige baseline estável para virar gate bloqueante;
- active DAST/fuzz destrutivo nunca usa produção por inferência; somente ambiente descartável ou alvo explicitamente autorizado;
- ferramenta indisponível não vira `pass`; checks `required` precisam executar ou receber exceção explícita e versionada;
- scanners/model checkers determinísticos não contam como `independent-agent` de Semantic Verification e não entendem sozinhos a intenção do produto;
- ferramentas de API/verification/formal são defaults substituíveis por equivalentes gratuitos; versões usadas em CI devem ser fixadas/reproduzíveis;
- funcionalidade nova, bugfix relevante, regra de negócio, contrato de dados/API ou mudança estrutural de médio/alto risco recebe Semantic Verification antes da implementação;
- documentação/chore e refactor pequeno sem mudança observável permanecem leves;
- `specs/semantic-contract.json` é o alvo verificável quando Semantic Verification se aplica, mas não duplica contrato OpenAPI/GraphQL/Protobuf/AsyncAPI;
- todo critério `must` deve apontar para evidência executável/gate declarado em `specs/verification-plan.json`;
- rastreabilidade não substitui a execução real dos gates;
- risco médio/alto exige revisão `independent-agent` quando disponível ou `clean-context` provider-neutral; deterministic CI sozinho não é reviewer semântico suficiente;
- review evidence é ligado por fingerprint à spec, plano e conteúdo revisado; mudança posterior torna a aprovação stale;
- visual regression é condicional a baseline visual estável e risco material, evitando snapshots frágeis em UI exploratória;
- Context Engine não finge possuir call graph universal; Semantic Assurance usa somente um grafo semântico explícito por IDs/referências, não inferência mágica de todo o código;
- typecheck/build/lockfile/runtime são defesa padrão contra APIs/bibliotecas inexistentes; integrações pouco tipadas/de runtime recebem smoke/integration test quando necessário;
- backend é escolhido por capacidade, não por marca;
- ordem baseline: `current_agent → github_ci → sandbox → local_full` entre backends elegíveis;
- aprendizado só pode reordenar candidatos leves já elegíveis com evidência suficiente;
- dados insuficientes preservam o baseline;
- prompts nunca viram shell diretamente e nunca entram no dataset de learning;
- Learning Engine não persiste prompt, objetivo do usuário, nomes pessoais, código, conteúdo de arquivos, summaries/logs, task keys, secrets ou URLs privadas;
- eventos de learning carregados do disco são tratados como entrada não confiável e reconstruídos pelo schema seguro;
- falha técnica entra em repair/fallback limitado; não vira pergunta ao usuário por reflexo;
- intervenção humana continua reservada a produto/regra de negócio, preferência subjetiva, custo, risco alto, credencial/dado indisponível e decisão legal/organizacional;
- reuse-first, baseline/diff/rollback, instalação limpa, testes executáveis e CI reproduzível continuam gates permanentes;
- Living UI / Semantic Motion permanece transversal quando existe UI, com `ambient` contextual e `prefers-reduced-motion` obrigatório.

## Evidência de governance hardening

- `core/SYSTEM_ENGINEERING.md`;
- `scripts/validate_system_engineering.py`;
- `.github/workflows/validate-system-engineering.yml`;
- `core/API_ENGINEERING.md`;
- `skills/api-engineering/SKILL.md`;
- `templates/project/API.md`;
- `templates/api/redocly.yaml` e `templates/api/README.md`;
- `scripts/validate_api_engineering.py`;
- `.github/workflows/validate-api-engineering.yml`;
- `core/SEMANTIC_ASSURANCE.md`;
- `engine/semantic_assurance.py`;
- `scripts/semantic_assurance.py`;
- `skills/semantic-assurance/SKILL.md`;
- `templates/project/SEMANTICS.md`;
- `research/SEMANTIC_ASSURANCE_RESEARCH.md`;
- `scripts/validate_semantic_assurance.py`;
- `.github/workflows/validate-semantic-assurance.yml`;
- `core/INDEPENDENT_VERIFICATION.md`;
- `engine/independent_verification.py`;
- `scripts/independent_verification.py`;
- `skills/independent-verification/SKILL.md`;
- `templates/project/VERIFICATION.md` e `templates/verification/README.md`;
- `scripts/validate_independent_verification.py`;
- `.github/workflows/validate-independent-verification.yml`;
- integração em `AGENTS.md`, Factory Router, App Planner, Workflow, Definition of Done, Semantic Verification e templates;
- validators de regressão preservam engines V1.1–V1.4 e recipes `auth-better-auth`/`database-drizzle-postgres`.

## Evidência V1.4 preservada

- `core/SEMANTIC_VERIFICATION.md`;
- `engine/semantic_verification.py`;
- `engine/review_packet.py`;
- fase `specification` e guards em `engine/autonomy_engine.py`;
- integração em `scripts/factory.py`;
- `skills/semantic-verification/SKILL.md`;
- `scripts/validate_v1_4.py`;
- `tests/v1_4/`;
- `.github/workflows/validate-v1-4-semantic.yml`.

A validação V1.4 cobre spec proporcional, invariantes/IDs, critérios `must`, rastreabilidade até gates declarados, stale spec/plan/review, recusa de deterministic-CI-only review em risco médio/alto, clean-context review, fingerprint do conteúdo atual, pacote spec+diff sem raciocínio anterior, fase semântica do Autonomy Engine, compatibilidade do fluxo legado e integração CLI.

## Evidência V1.3 preservada

- `core/LEARNING_ENGINE.md`;
- `engine/learning_engine.py`;
- integração em `engine/execution_engine.py` e `scripts/factory.py`;
- `skills/learning-engine/SKILL.md`;
- `scripts/validate_v1_3.py`;
- `tests/v1_3/`;
- `.github/workflows/validate-v1-3-learning.yml`;
- `research/V1.3_LEARNING_ENGINE_VALIDATION.md`.

## Evidência V1.2 preservada

- `core/EXECUTION_FABRIC.md`;
- `engine/execution_engine.py`;
- `engine/ci_executor.py`;
- `skills/execution-router/SKILL.md`;
- `scripts/validate_v1_2.py`;
- `tests/v1_2/`;
- `.github/workflows/validate-v1-2-execution.yml`.

## Evidência V1.1 preservada

- `research/V1.1_AUTONOMOUS_CONTEXT_VALIDATION.md`;
- `engine/context_engine.py`;
- `engine/autonomy_engine.py`;
- `tests/v1_1/`;
- `.github/workflows/validate-v1-1-autonomy.yml`.

## Evidência V1.0 preservada

- `research/V1.0_FINAL_AUDIT.md`;
- `audits/v1-final/equipment-loans/`;
- `research/evidence/V1_CONTINUITY_HANDOFF.md`;
- `research/evidence/V1_CONTROLLED_RECOVERY.md`;
- `scripts/validate_v1_bootstrap.py` e `scripts/validate_v1_release.py`.

## Próxima ação

Usar V1.4 como baseline de engines com System/API/Semantic Assurance/Independent Verification como governance hardening corrente. Em projeto existente, começar por `resume`; deixar Context/Autonomy recuperar o estado, Factory Router classificar sistema/API/Semantic/Independent Verification, Semantic Assurance validar a qualidade da spec quando `domain`/`formal`, Execution Fabric filtrar executores, Learning Engine influenciar somente quando houver evidência confiável, CI provar comportamento/arquitetura/contratos com gates proporcionais e revisão desacoplada fechar o gap entre intenção, especificação e implementação quando o risco justificar.

Escopos ainda não validados — como call graph semântico profundo universal, mobile nativo, desktop nativo, jogos e cloud complexa — continuam exigindo piloto/evidência próprios antes de virarem capacidades/perfis estáveis.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. `python scripts/factory.py --root <projeto> resume` quando o runtime estiver disponível;
3. este `PROJECT_STATE.md` quando estiver modificando a própria Factory;
4. `core/ENTRYPOINT.md`;
5. `core/SYSTEM_ENGINEERING.md`, `core/API_ENGINEERING.md`, `core/SEMANTIC_ASSURANCE.md` e `core/INDEPENDENT_VERIFICATION.md` quando aplicáveis;
6. `core/CONTEXT_ENGINE.md`, `core/AUTONOMY_ENGINE.md`, `core/SEMANTIC_VERIFICATION.md`, `core/EXECUTION_FABRIC.md` e `core/LEARNING_ENGINE.md`;
7. `skills/factory-router/SKILL.md`, `skills/app-planner/SKILL.md`, `skills/api-engineering/SKILL.md`, `skills/semantic-assurance/SKILL.md`, `skills/semantic-verification/SKILL.md`, `skills/independent-verification/SKILL.md`, `skills/execution-router/SKILL.md` e `skills/learning-engine/SKILL.md`;
8. o perfil indicado pelo produto;
9. `ui/UI_POLICY.md` e `ui/MOTION_POLICY.md` quando houver interface.
