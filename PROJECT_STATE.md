# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Manter a **App Factory V1.4 estável** como baseline general-purpose, recuperável, autônomo, adaptativo e verificável, com **governance hardening** posterior que aumenta qualidade arquitetural, semântica, técnica, visual e de manutenção sem alterar a linha de engines V1.1–V1.4 nem transformar toda tarefa em processo pesado.

## Estado

- fase: `V1.4 — estável + governance hardening`;
- versão: `1.4.0`;
- versão dos engines/plugin baseline: `1.4.0`;
- baseline publicada anterior preservada: tag/release `v1.0.0`;
- Skills portáteis: **19**;
- V1.1: **Context Engine + Autonomy Engine**;
- V1.2: **Execution Fabric + CI Executor**;
- V1.3: **Learning Engine** local-only, bounded e privacy-safe;
- V1.4: **Semantic Verification** com `specs/semantic-contract.json`, `specs/verification-plan.json`, `specs/review-evidence.json`, fingerprints e revisão desacoplada proporcional;
- System Engineering Contract: níveis `website`/`local-app`/`persistent-app`/`multi-user-system`/`production-system`/`critical-system`, fonte autoritativa, persistência/identidade/autorização/recovery proporcionais;
- **API Engineering Contract**: `none`/`lightweight`/`contract`/`governed`, protocolo pela necessidade, contract/compatibilidade/runtime/security quando aplicável; gate **Validate API Engineering Contract** ativo;
- **Semantic Assurance**: profundidade `scenario`/`domain`/`formal`, requisitos EARS/FRET-inspired, domínio/referências, consistência, cobertura estrutural e semantic diff; gate `Validate Semantic Assurance` ativo;
- property/stateful: Hypothesis/fast-check condicionais; **NIST ACTS**/covering arrays somente para combinatória finita material e modelo versionado;
- formalização condicional: Z3/SMT, Alloy, FRET, P, Quint/TLA+, DMN e OPA/Rego/Cedar conforme o problema, nunca stack universal;
- **Independent Verification**: `baseline`/`independent`/`adversarial`/`release`, `free-only`, diversidade de método por classe de falha; actionlint/zizmor verificam GitHub Actions quando aplicável; Trivy, Semgrep CE, StrykerJS/mutmut, Schemathesis, ZAP, axe/Playwright, Lighthouse, Squawk, dependency-cruiser, k6 e Toxiproxy continuam condicionais;
- field-test hardening: CLI auto-inicializável, recuperação explícita de lockfile legado, invariantes de coleção, lifecycle/migração de storage local, policy-as-code só com sinal material e E2E sincronizado com hidratação;
- Professional UI: `professional-default` é quality bar transversal; admin/dashboard/CRUD continua preferindo shadcn/ui + ReUI seletivo, HeroUI segue alternativa; Motion Profile permanece contrato separado;
- Agent Conformance: corpus versionado + executor de referência + scorer determinístico de worktree; agentes reais são adaptadores opcionais e chain-of-thought não é avaliado;
- Python Evidence: `coverage.py` branch-aware como diagnóstico + `diff-cover` com 100% das linhas executáveis novas/modificadas de `engine/`; sem threshold global arbitrário nem SaaS obrigatório;
- Skill Routing Telemetry: `.factory/skill-routing.json`, local/bounded, registra apenas slugs/origens allowlisted explicitamente roteados; não registra prompt/conteúdo nem desativa Skill automaticamente;
- **Change Hygiene**: `core/CHANGE_HYGIENE.md` vale para manutenção/revisão de projetos criados pela Factory ou externos; preserva comportamento sem preservar implementação obsoleta, exige consolidação após repair loop e impede que histórico de tentativas vire arquitetura final;
- Change Hygiene scanner: `scripts/change_hygiene.py` bloqueia resíduos objetivos (conflitos/temporários rastreados), marca shadow copies/suppressions/`!important`/workarounds como advisory e detecta tooling existente sem instalar scanners por checklist;
- ferramentas de higiene condicionais: lint/typecheck primeiro; Knip para dead files/exports/dependencies JS/TS; Ruff/Pyflakes + Vulture configurado em Python; Stylelint para dívida CSS; jscpd para hotspots/delta sem percentual universal;
- projetos externos: mapear baseline/caminho real, não reescrever dívida histórica fora do escopo, mas não adicionar nova camada de dívida na área tocada;
- CI: gates V1 preservados + System Engineering + **Validate API Engineering Contract** + Semantic Assurance + Independent Verification + Agent Conformance + Python Evidence + Change Hygiene + Web Admin Starter + V1 Release.

## Decisões vigentes

- o Core é **general-purpose**; domínio escolar é apenas um dos domínios possíveis;
- intenção de desenvolvimento ativa `factory-router`; usuário não precisa nomear App Factory;
- GitHub é fonte técnica de verdade; chat não é continuidade operacional;
- `resume`/Context Engine recuperam contexto antes de depender de memória;
- arquitetura, API mode, semantic depth, matriz independente e executor são decisões técnicas da Factory;
- System Engineering decide profundidade arquitetural mínima; processo leve não autoriza falsa persistência/segurança;
- Semantic Assurance avalia qualidade da especificação; Semantic Verification prova implementação↔intenção; API Engineering governa interfaces; Independent Verification tenta quebrar/provar tecnicamente por métodos distintos;
- ferramentas formais, scanners, load/fault/cross-browser entram apenas com pré-condição real;
- ferramenta indisponível nunca vira `pass`;
- critérios `must` apontam para evidência executável; risco médio/alto exige revisão desacoplada proporcional;
- Evaluation Evidence mede resultados observáveis: Agent Conformance não avalia raciocínio privado; coverage é diagnóstico/diff gate; Skill Routing é telemetria agregada local;
- **preservar comportamento não significa preservar implementação obsoleta**;
- todo trabalho em código existente aplica Change Hygiene, independentemente da origem do projeto;
- repair loop pode experimentar, mas a entrega passa por consolidação: remover tentativas descartadas, código morto/orfandade, shadow implementations, overrides/suppressions/temporários desnecessários e reverificar depois;
- duas implementações só coexistem quando há compatibilidade/migração real, consumidor/razão identificável, condição objetiva de remoção e testes de transição;
- CSS deve corrigir a causa antes de acumular specificity/`!important`;
- tooling de dead code/duplicação é proporcional; heurística não autoriza remoção automática de código dinâmico;
- refactor grande deve, quando possível, ser separado da mudança funcional; refactor local necessário pode acompanhar a correção;
- a árvore final deve representar a solução vigente que escolheríamos se já soubéssemos qual abordagem funcionaria; histórico de tentativas permanece no Git/PR.

## Evidência corrente

- Core/engines: `core/`, `engine/`, `skills/`, `scripts/`, `tests/`;
- Change Hygiene: `core/CHANGE_HYGIENE.md`, `scripts/change_hygiene.py`, `tests/change_hygiene/`, `research/CHANGE_HYGIENE_RESEARCH.md`, `.github/workflows/validate-change-hygiene.yml`;
- Evaluation Evidence: `evals/agent-conformance/`, `.github/workflows/validate-agent-conformance.yml`, `.github/workflows/validate-python-evidence.yml`;
- decisões duráveis: `docs/DECISIONS.md` (D-086–D-090 para Change Hygiene; D-081–D-085 para Evaluation Evidence);
- manutenção: `skills/maintenance/SKILL.md`, `core/WORKFLOW.md`, `core/DEFINITION_OF_DONE.md`, `templates/project/AGENTS.md`.

## Próxima ação

Usar este baseline em criação e evolução. Em projeto existente: recuperar baseline → caracterizar comportamento → implementar/reparar → verificar → **consolidar com Change Hygiene** → reverificar → revisar/entregar. Em projeto externo, adotar o mesmo fluxo sem exigir documentos históricos da Factory como pré-condição para começar.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. `PROJECT_STATE.md` quando estiver modificando a própria Factory;
3. `core/ENTRYPOINT.md` e `core/WORKFLOW.md`;
4. `core/CHANGE_HYGIENE.md` + `skills/maintenance/SKILL.md` para código existente;
5. `core/SYSTEM_ENGINEERING.md`, `core/API_ENGINEERING.md`, `core/SEMANTIC_ASSURANCE.md`, `core/SEMANTIC_VERIFICATION.md` e `core/INDEPENDENT_VERIFICATION.md` quando aplicáveis;
6. `core/CONTEXT_ENGINE.md`, `core/AUTONOMY_ENGINE.md`, `core/EXECUTION_FABRIC.md`, `core/LEARNING_ENGINE.md`;
7. perfil/UI policies apenas quando o produto exigir.
