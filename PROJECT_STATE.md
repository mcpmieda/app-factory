# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Manter a **App Factory V1.4 estável** como baseline recuperável, autônomo, adaptativo e semanticamente verificável para criação/evolução de software geral, com hardenings posteriores que impedem falsa completude, adicionam governança proporcional de APIs, verificam a qualidade da própria especificação com **Semantic Assurance** e ampliam verificação técnica independente gratuita sem alterar os engines V1.1–V1.4.

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
- Semantic Assurance Contract: classifica `scenario`/`domain`/`formal`, normaliza requisitos inspirados em EARS/FRET, mantém domínio/referências explícitos, detecta inconsistências determinísticas, mede rastreabilidade estrutural e calcula semantic diff/impacto;
- Semantic Assurance engine: `engine/semantic_assurance.py` valida IDs/referências, cardinalidades/ranges/enums, dependências conflitantes, perguntas `blocking`, cobertura requisito→AC/invariante→gate e recomenda formalização proporcional sem transformar análise probabilística em prova;
- field-test hardening (Gestão de Alunos): CLI Semantic Assurance auto-inicializável, bootstrap explícito para legado sem lockfile, policy-as-code apenas com sinal de acesso, invariantes entre registros, lifecycle versionado para dados locais e disciplina de E2E com hidratação/escopo;
- métodos formais/estruturados preferidos quando aplicáveis: Z3/SMT, Alloy, NASA FRET/FRETish, P, Quint/TLA+, DMN e OPA/Rego/Cedar;
- property/stateful/model-based testing: Hypothesis (Python) e fast-check (JS/TS) são defaults condicionais derivados de invariantes/ranges/estados; não substituem `given/when/then`, Schemathesis ou mutation testing;
- combinatorial testing: **NIST ACTS** ou covering-array equivalent entra somente quando múltiplas dimensões finitas interagirem; só vira gate obrigatório com modelo combinatorial versionado;
- Independent Verification Contract: classifica `baseline`/`independent`/`adversarial`/`release`, usa matriz `free-only` e adiciona evidência independente sem substituir Semantic Assurance/Verification;
- Independent Verification planner schema v2: `engine/independent_verification.py` detecta linguagem/UI/testes/API, workflows GitHub, PostgreSQL/migrations, architecture rules, semantic depth/modelo combinatorial, load tests e RESTler config; recebe também sinal de integrações externas materiais;
- verificação do próprio CI: **actionlint** valida correção de GitHub Actions e **zizmor** valida segurança de workflows quando aplicável;
- segurança/robustez especializada: **Squawk** para migrations PostgreSQL; **dependency-cruiser**/equivalente para limites arquiteturais declarados; **k6** para load/concurrency com SLO/baseline; **Toxiproxy** para resiliência de rede usando proxy/stub controlado;
- API deep fuzz: Schemathesis continua default; Microsoft RESTler é escalonamento `governed`/OpenAPI para estados profundos, normalmente release/nightly;
- SAST: Semgrep CE continua default; Opengrep é substituto qualificado após piloto, não scanner paralelo;
- browser release: Playwright pode expandir Chromium + Firefox + WebKit quando o produto realmente suporta esses engines; plataforma específica não ganha matriz artificial;
- matriz anterior preservada: Trivy, Semgrep CE, StrykerJS/mutmut, Schemathesis, OWASP ZAP, axe-core + Playwright e Lighthouse CI continuam defaults condicionais nas respectivas classes;
- API standards/tooling quando aplicáveis: OpenAPI, GraphQL, gRPC/Protobuf, AsyncAPI, Arazzo, RFC 9110, RFC 9457, OWASP API Security, Redocly CLI, oasdiff, Schemathesis e Pact;
- Context Engine: incremental, stdlib, SHA-256, delta `added/changed/removed`, stack/símbolos/imports/dependências locais e exclusão de segredos/build/dependencies/binários;
- Autonomy Engine: `init/status/next/resume/record`, transições explícitas, repair loop default 3, intervenção humana categorizada e fase `specification` quando `spec_required=true`;
- Semantic Verification: `specs/semantic-contract.json` + `specs/verification-plan.json` + `specs/review-evidence.json`, critérios `given/when/then`, fingerprints contra evidência stale e revisão desacoplada para risco médio/alto;
- Semantic Assurance em `domain`/`formal`: `specs/semantic-assurance.json` aponta para fingerprint do contrato semântico e `SEMANTICS.md` registra decisões/limites humanos específicos;
- clean-context review: `engine/review_packet.py` produz pacote spec + diff atual sem depender do raciocínio da implementação/aprovação anterior;
- Execution Fabric: `current_agent/github_ci/sandbox/local_full`, fallback escopado pela tarefa e histórico bounded; GitHub CI é executor preferido de gates determinísticos/formais/Independent Verification quando capaz;
- CI Executor: gates declarados/allowlisted, sem comandos de prompt, `shell=False`, sem secrets por padrão, instalação reproduzível com lockfile e suporte condicional a `test:visual`;
- Learning Engine: **local-only**, bounded, sem telemetria externa, metadados técnicos allowlisted, amostra mínima/prior conservador e explicação `baseline/learned/insufficient-data`;
- aprendizado: incapacidade, indisponibilidade, failure threshold, risco, contratos arquiteturais/API/semantic-assurance/semantic-verification/independent-verification e DoD vencem score histórico;
- `local_full`: não é promovido sobre backend leve capaz somente por aprendizado;
- perfil `web-admin`: `v1`;
- perfis `website`, `web-app`, `chrome-extension` e `automation`: `validated`;
- Skills portáteis: **19**, incluindo `api-engineering`, `semantic-assurance` e `independent-verification`;
- CI: gates V1 preservados + `Validate V1.4 Semantic Verification` + `Validate System Engineering Contract` + `Validate API Engineering Contract` + `Validate Semantic Assurance` + `Validate Independent Verification`.

## Decisões vigentes

- intenção de software ativa a Factory automaticamente;
- AI serve ao objetivo, não ao texto literal do prompt;
- GitHub é fonte técnica de verdade; conversa não é autoridade operacional;
- o Core é **general-purpose**: pode construir software escolar ou de qualquer outro domínio; regras escolares ficam em projetos/perfis, nunca limitam System/Semantic/API/Independent Verification;
- `resume`/Context Engine recuperam contexto antes de depender de memória de conversa;
- `.factory/context/` é cache regenerável; `.factory/state.json` mantém continuidade; `.factory/execution.json` e `.factory/learning.json` permanecem locais/bounded por padrão;
- ausência de learning local não bloqueia continuidade: baseline seguro continua funcionando;
- o agente calcula próxima ação, spec, nível do sistema, API mode, semantic depth, Independent Verification e executor; usuário não escolhe solver/model checker/scanner manualmente;
- System Engineering decide profundidade mínima; processo leve não rebaixa arquitetura real;
- API Engineering só entra em fronteira relevante; backend não implica OpenAPI;
- REST não é obrigatório; protocolo é escolhido pelo comportamento;
- Semantic Assurance decide qualidade/profundidade da spec; Semantic Verification prova implementação↔spec; API Engineering governa interfaces; Independent Verification fornece evidência técnica externa;
- `scenario` é default semântico leve; `domain` exige interação real de conceitos/regras; `formal` só quando natureza/criticidade justificar;
- requisitos `domain/formal` usam estrutura EARS/FRET sem exigir Cucumber/FRET universal;
- coverage semântica é rastreabilidade estrutural, não “percentual de verdade”;
- findings probabilísticos da IA permanecem hipóteses/advisory até estrutura/prova/decisão humana;
- semantic diff propaga impacto por IDs/fingerprints e invalida evidência dependente;
- Z3, Alloy, FRET, P, Quint/TLA+, DMN, OPA/Rego e Cedar são opções condicionais/substituíveis;
- formalização só conta como prova com artefato versionado, `source_refs` e gate executado quando `required`;
- Hypothesis/fast-check entram quando invariantes/ranges/estados justificarem; lógica trivial permanece em exemplos normais;
- NIST ACTS entra para espaço combinatório finito real e só bloqueia com modelo versionado;
- Independent Verification é `free-only`: não exige segunda IA paga, SaaS comercial ou scanner premium;
- **diversidade de método vence quantidade de scanners**: não rodar equivalentes redundantes sem ganho;
- GitHub Actions é executor preferido quando capaz, mas actionlint/zizmor verificam o próprio laboratório quando workflows existirem;
- projetos simples permanecem `baseline`; sistemas reais/alto risco sobem somente por sinais objetivos;
- Squawk só em PostgreSQL+migrations; dependency-cruiser/equivalente só quando arquitetura for materializável; k6 só com workload/SLO/baseline; Toxiproxy só com integração externa material;
- load/fuzz/DAST/fault injection nunca usam produção/terceiro como alvo por inferência;
- Schemathesis continua API fuzz principal; RESTler é escalonamento stateful profundo; Semgrep CE continua SAST default e Opengrep é alternativa qualificada;
- cross-browser Playwright entra quando suporte multi-engine for requisito real;
- ferramenta indisponível não vira `pass`; check required executa ou recebe exceção explícita/versionada;
- scanners/model checkers não contam como `independent-agent` e não entendem intenção sozinhos;
- ferramentas de API/verification/formal são defaults substituíveis por equivalentes gratuitos; versões em CI são fixadas/reproduzíveis;
- funcionalidade nova, bugfix relevante, regra de negócio, contrato de dados/API ou mudança estrutural médio/alto risco recebe Semantic Verification antes da implementação;
- documentação/chore/refactor pequeno sem mudança observável permanecem leves;
- `specs/semantic-contract.json` não duplica contrato OpenAPI/GraphQL/Protobuf/AsyncAPI;
- todo critério `must` aponta para evidência executável/gate; rastreabilidade não substitui execução;
- risco médio/alto exige revisão `independent-agent` ou `clean-context`; deterministic CI sozinho não é reviewer semântico;
- review evidence é fingerprinted e fica stale após mudança dependente;
- visual regression depende de baseline estável/risco material;
- typecheck/build/lockfile/runtime defendem contra APIs inexistentes; integrações pouco tipadas ganham smoke/integration quando necessário;
- backend é escolhido por capacidade, não marca; baseline `current_agent → github_ci → sandbox → local_full`;
- aprendizado só reordena candidatos leves já elegíveis com evidência suficiente; dados insuficientes preservam baseline;
- prompts nunca viram shell diretamente nem entram no learning dataset;
- falha técnica entra em repair/fallback limitado antes de perguntar ao usuário;
- intervenção humana fica para produto/regra, preferência subjetiva, custo, alto risco, credencial/dado indisponível e decisão legal/organizacional;
- reuse-first, baseline/diff/rollback, instalação limpa, testes executáveis e CI reproduzível continuam permanentes;
- Living UI / Semantic Motion permanece transversal quando existe UI, com `ambient` contextual e `prefers-reduced-motion` obrigatório.

## Evidência de governance hardening

- `core/SYSTEM_ENGINEERING.md` e `scripts/validate_system_engineering.py`;
- `core/API_ENGINEERING.md`, `skills/api-engineering/SKILL.md`, templates API e `scripts/validate_api_engineering.py`;
- `core/SEMANTIC_ASSURANCE.md`, `engine/semantic_assurance.py`, `scripts/semantic_assurance.py`, `skills/semantic-assurance/SKILL.md`, `templates/project/SEMANTICS.md`, `research/SEMANTIC_ASSURANCE_RESEARCH.md` e `scripts/validate_semantic_assurance.py`;
- `core/INDEPENDENT_VERIFICATION.md`, `engine/independent_verification.py`, `scripts/independent_verification.py`, `skills/independent-verification/SKILL.md`, `templates/project/VERIFICATION.md`, `templates/verification/README.md`, `research/VERIFICATION_ENRICHMENT_RESEARCH.md` e `scripts/validate_independent_verification.py`;
- integração em AGENTS, Factory Router, App Planner, Workflow, DoD, Semantic Verification e templates;
- validators preservam engines V1.1–V1.4 e recipes `auth-better-auth`/`database-drizzle-postgres`.

## Evidência V1.4 preservada

- `core/SEMANTIC_VERIFICATION.md`;
- `engine/semantic_verification.py`;
- `engine/review_packet.py`;
- fase `specification`/guards em `engine/autonomy_engine.py`;
- integração em `scripts/factory.py`;
- `skills/semantic-verification/SKILL.md`;
- `scripts/validate_v1_4.py`;
- `tests/v1_4/`;
- `.github/workflows/validate-v1-4-semantic.yml`.

A validação V1.4 cobre spec proporcional, invariantes/IDs, critérios `must`, rastreabilidade até gates declarados, stale spec/plan/review, recusa de deterministic-CI-only review em risco médio/alto, clean-context review, fingerprint do conteúdo atual, pacote spec+diff, fase semântica do Autonomy Engine, fluxo legado e CLI.

## Evidência V1.3 preservada

- `core/LEARNING_ENGINE.md`;
- `engine/learning_engine.py`;
- integração em `engine/execution_engine.py`/`scripts/factory.py`;
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

Usar V1.4 como baseline de engines com System/API/Semantic Assurance/Independent Verification como governance hardening corrente. Em projeto existente, começar por `resume`; deixar Context/Autonomy recuperar estado, Router classificar sistema/API/Semantic/Independent Verification, Semantic Assurance validar spec e derivar propriedades/modelos quando úteis, planner escolher a menor matriz independente por classe de falha, Execution Fabric selecionar executor, CI provar comportamento/arquitetura/contratos e revisão desacoplada fechar o gap entre intenção, especificação e implementação.

Escopos ainda não validados — como call graph semântico profundo universal, mobile nativo, desktop nativo, jogos e cloud complexa — continuam exigindo piloto/evidência próprios antes de virarem capacidades/perfis estáveis.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. `python scripts/factory.py --root <projeto> resume` quando runtime estiver disponível;
3. este `PROJECT_STATE.md` ao modificar a própria Factory;
4. `core/ENTRYPOINT.md`;
5. `core/SYSTEM_ENGINEERING.md`, `core/API_ENGINEERING.md`, `core/SEMANTIC_ASSURANCE.md` e `core/INDEPENDENT_VERIFICATION.md` quando aplicáveis;
6. `core/CONTEXT_ENGINE.md`, `core/AUTONOMY_ENGINE.md`, `core/SEMANTIC_VERIFICATION.md`, `core/EXECUTION_FABRIC.md` e `core/LEARNING_ENGINE.md`;
7. Skills `factory-router`, `app-planner`, `api-engineering`, `semantic-assurance`, `semantic-verification`, `independent-verification`, `execution-router` e `learning-engine`;
8. perfil indicado pelo produto;
9. `ui/UI_POLICY.md` e `ui/MOTION_POLICY.md` quando houver interface.
