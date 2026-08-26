# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Manter a **App Factory V1.4 estável** como baseline general-purpose, recuperável, autônomo, adaptativo e verificável, com **governance hardening** posterior que aumenta qualidade arquitetural, semântica, técnica, visual e de manutenção sem criar artificialmente uma nova linha de engines.

## Estado

- fase: `V1.4 — estável + project adoption governance hardening`;
- versão: `1.4.0`;
- baseline histórica **`V1.4 — estável`**: **19 Skills** portáteis antes da inclusão de `project-adoption`; preservada como referência de compatibilidade dos validadores V1.4;
- baseline publicada anterior preservada: tag/release `v1.0.0`;
- Skills portáteis atuais: **20**;
- V1.1: **Context Engine + Autonomy Engine**;
- V1.2: **Execution Fabric + CI Executor**;
- V1.3: **Learning Engine** local-only, bounded e privacy-safe;
- V1.4: **Semantic Verification** com `specs/semantic-contract.json`, `specs/verification-plan.json`, `specs/review-evidence.json`, fingerprints e revisão desacoplada proporcional;
- **Project Adoption Gate hardening sobre V1.4**: `core/PROJECT_ADOPTION_GATE.md`, `engine/project_adoption.py`, `scripts/project_adoption_gate.py` e Skill `project-adoption` impedem que um projeto governado pela Factory comece implementação material antes de tornar routing/UI/semântica/verificação recuperáveis e passar o gate `pre-implementation`;
- `.app-factory.json` schema v2 é o resumo machine-readable de governança para projetos adotados, preservando documentos/código como fontes reais;
- recuperação honesta: projetos já iniciados que não passaram pelo gate são auditados/adotados antes do próximo bloco, sem fingir compliance retroativo nem reconstruir infraestrutura estável por reflexo;
- **web-admin anti-bypass**: shadcn/ui permanece default validado; HeroUI é override transversal; React + CSS/custom/native como fundação visual exige `ui.deviation` explícito em vez de virar fallback silencioso;
- **HeroUI Overlay Interaction Hardening**: `ui/heroui/OVERLAY_INTERACTION_HARDENING.md` exige semântica correta de link/ação/seleção, fonte única de estado por overlay, fechamento junto à navegação, QA com ponteiro real/hit-testing, runtime gates e mediana de múltiplas amostras;
- **HeroUI sem efeito ambiental obrigatório**: escolher HeroUI define design system e uso transversal de primitives/tokens/overlays/motion, mas não injeta automaticamente partículas, glows, fundos especiais ou outro padrão ambiental;
- Project Adoption delivery gate exige review evidence proporcional para risco semântico médio/alto e estado recuperável de Independent Verification acima de baseline;
- System Engineering Contract: níveis `website`/`local-app`/`persistent-app`/`multi-user-system`/`production-system`/`critical-system`, fonte autoritativa, persistência/identidade/autorização/recovery proporcionais;
- **Client Interruption Resilience**: operações críticas aceitas server-side que possam sofrer efeito parcial, duplicidade, divergência ou perda de progresso com fechamento do navegador/queda de energia/rede devem manter estado crítico fora do cliente e possuir estratégia proporcional de idempotência, checkpoint, status, retomada, reconciliação, transação, lock ou compensação; toda operação materialmente interrompível deve conseguir responder depois: `foi executada?`, `até onde chegou?`, `o que ainda falta?`;
- **API Engineering Contract**: `none`/`lightweight`/`contract`/`governed`, protocolo pela necessidade, contract/compatibilidade/runtime/security quando aplicável; gate **Validate API Engineering Contract** ativo;
- **Semantic Assurance**: profundidade `scenario`/`domain`/`formal`, requisitos EARS/FRET-inspired, domínio/referências, consistência, cobertura estrutural e semantic diff; gate `Validate Semantic Assurance` ativo;
- property/stateful: Hypothesis/fast-check condicionais; **NIST ACTS**/covering arrays somente para combinatória finita material e modelo versionado;
- formalização condicional: Z3/SMT, Alloy, FRET, P, Quint/TLA+, DMN e OPA/Rego/Cedar conforme o problema, nunca stack universal;
- **Independent Verification**: `baseline`/`independent`/`adversarial`/`release`, `free-only`, diversidade de método por classe de falha; ferramentas continuam condicionais à superfície real;
- CI self-check: **actionlint** valida workflows quando aplicável; zizmor complementa segurança de GitHub Actions conforme o modo de Independent Verification;
- field-test hardening: CLI auto-inicializável, recuperação explícita de lockfile legado, invariantes de coleção, lifecycle/migração de storage local, policy-as-code só com sinal material e E2E sincronizado com hidratação;
- Professional UI: `professional-default` é quality bar transversal; admin/dashboard/CRUD continua preferindo shadcn/ui + ReUI seletivo quando não houver escolha explícita de HeroUI; Motion Profile permanece contrato separado;
- HeroUI catalog: `ui/heroui/` mantém catálogo auditado React/Pro/Native/v2 e contrato de interação de overlays como parte nativa da linguagem HeroUI;
- Agent Conformance: corpus versionado + executor de referência + scorer determinístico de worktree; agentes reais são adaptadores opcionais e chain-of-thought não é avaliado;
- Python Evidence: `coverage.py` branch-aware como diagnóstico + `diff-cover` com 100% das linhas executáveis novas/modificadas de `engine/`; sem threshold global arbitrário nem SaaS obrigatório;
- Skill Routing Telemetry: `.factory/skill-routing.json`, local/bounded, registra apenas slugs/origens allowlisted explicitamente roteados; não registra prompt/conteúdo nem desativa Skill automaticamente;
- **Change Hygiene**: `core/CHANGE_HYGIENE.md` vale para manutenção/revisão de projetos criados pela Factory ou externos; preserva comportamento sem preservar implementação obsoleta, exige consolidação após repair loop e impede que histórico de tentativas vire arquitetura final;
- Change Hygiene scanner: `scripts/change_hygiene.py` bloqueia resíduos objetivos, marca shadow copies/suppressions/`!important`/workarounds como advisory e detecta tooling existente sem instalar scanners por checklist;
- projetos externos: mapear baseline/caminho real, não reescrever dívida histórica fora do escopo, mas não adicionar nova camada de dívida na área tocada;
- CI: gates V1 preservados + System Engineering + API Engineering + Semantic Assurance + Independent Verification + Agent Conformance + Python Evidence + Change Hygiene + Web Admin Starter + V1 Release; `scripts/validate_factory.py` protege também Project Adoption Gate, Professional UI e Client Interruption Resilience.

## Decisões vigentes

- o Core é **general-purpose**; domínio escolar é apenas um dos domínios possíveis;
- intenção de desenvolvimento ativa `factory-router`; usuário não precisa nomear App Factory;
- **projeto explicitamente governado pela App Factory precisa passar Project Adoption Gate antes da implementação material**;
- ativação universal do router não injeta governança permanente em repositório legado usado apenas para um reparo pontual;
- `.app-factory.json` schema v2 registra adoção/roteamento sem substituir `PROJECT_STATE.md`, arquitetura, specs ou código;
- GitHub é fonte técnica de verdade; chat não é continuidade operacional;
- `resume`/Context Engine recuperam contexto antes de depender de memória;
- arquitetura, API mode, semantic depth, matriz independente, perfil/UI e executor são decisões técnicas da Factory;
- Semantic Verification exigida é materializada antes do código; spec criada depois do código é recuperação, não conformidade normal;
- ferramentas formais, scanners, load/fault/cross-browser entram apenas com pré-condição real;
- ferramenta indisponível nunca vira `pass`;
- critérios `must` apontam para evidência executável; risco médio/alto exige revisão desacoplada proporcional;
- **web-admin não pode usar React + CSS próprio como fallback silencioso**; base ad hoc exige desvio explícito;
- **escolha explícita de HeroUI para o sistema inteiro prevalece sobre o default visual administrativo shadcn/ReUI**;
- HeroUI não implica atmosfera visual adicional obrigatória; efeitos decorativos dependem do produto/projeto;
- em HeroUI, link/ação/seleção preservam a semântica real mesmo dentro de Drawer/Popover; aparência de coleção não justifica substituir navegação por selection behavior;
- overlay controlado tem uma única fonte de estado; listener global de rota não deve competir com o handler da interação quando o próprio clique pode fechar e navegar;
- QA de overlay usa hit-testing/ponteiro real quando possível, captura exceções de runtime e mede latência por múltiplas amostras/mediana;
- **operação crítica aceita pelo servidor não pode depender da permanência do navegador para conservar o único estado necessário à conclusão/recuperação** quando interrupção puder causar perda, duplicidade ou inconsistência;
- em resultado remoto ambíguo, reconciliar antes de repetir escrita; retry cego é proibido quando a operação pode já ter sido aplicada;
- operações em lote registram progresso por unidade quando parcialidade for material;
- pequenas mutações atômicas e seguras não precisam virar jobs: o requisito é sobrevivência e determinismo, não uma tecnologia específica;
- **preservar comportamento não significa preservar implementação obsoleta**;
- todo trabalho em código existente aplica Change Hygiene, independentemente da origem do projeto;
- repair loop pode experimentar, mas a entrega passa por consolidação;
- duas implementações só coexistem quando há compatibilidade/migração real com condição objetiva de remoção e testes;
- CSS deve corrigir a causa antes de acumular specificity/`!important`;
- a árvore final deve representar a solução vigente que escolheríamos se já soubéssemos qual abordagem funcionaria; histórico de tentativas permanece no Git/PR.

## Evidência corrente

- Project Adoption Gate: `core/PROJECT_ADOPTION_GATE.md`, `engine/project_adoption.py`, `scripts/project_adoption_gate.py`, `skills/project-adoption/SKILL.md`, `tests/project_adoption/`, templates/AGENTS, `profiles/web-admin/PROFILE.md` e `scripts/validate_factory.py`;
- System Engineering/Client Interruption Resilience: `core/SYSTEM_ENGINEERING.md`, `skills/factory-router/SKILL.md`, `skills/project-adoption/SKILL.md`, `templates/project/ARCHITECTURE.md`, `profiles/web-admin/PROFILE.md`, `AGENTS.md` e `scripts/validate_factory.py`;
- Core/engines: `core/`, `engine/`, `skills/`, `scripts/`, `tests/`;
- HeroUI catalog e hardening: `ui/heroui/`, incluindo `HEROUI_NATIVE_REDESIGN_CONTRACT.md`, `TEMPORAL_MOTION_QA.md` e `OVERLAY_INTERACTION_HARDENING.md`;
- Change Hygiene: `core/CHANGE_HYGIENE.md`, `scripts/change_hygiene.py`, `tests/change_hygiene/`, `research/CHANGE_HYGIENE_RESEARCH.md`, `.github/workflows/validate-change-hygiene.yml`;
- Evaluation Evidence: `evals/agent-conformance/`, `.github/workflows/validate-agent-conformance.yml`, `.github/workflows/validate-python-evidence.yml`;
- decisões duráveis: `docs/DECISIONS.md`;
- manutenção: `skills/maintenance/SKILL.md`, `core/WORKFLOW.md`, `core/DEFINITION_OF_DONE.md`, `templates/project/AGENTS.md`.

## Próxima ação

Usar este baseline em criação e evolução. Em projeto governado: detectar adoção → classificar → materializar `.app-factory.json`/estado/specs → passar `pre-implementation` → implementar → verificar/consolidar → passar `delivery`. Em sistemas persistentes, identificar antes do código as operações que podem sobreviver ao cliente e registrar a estratégia de continuidade/reconciliação. Em HeroUI, usar os contratos/catálogos nativos sem inferir um efeito ambiental universal. Em projeto existente: recuperar baseline → caracterizar comportamento → implementar/reparar → verificar → consolidar com Change Hygiene → reverificar → revisar/entregar.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. `PROJECT_STATE.md` quando estiver modificando a própria Factory;
3. `core/ENTRYPOINT.md`, `core/PROJECT_ADOPTION_GATE.md`, `core/SYSTEM_ENGINEERING.md` e `core/WORKFLOW.md`;
4. `skills/factory-router/SKILL.md` e `skills/project-adoption/SKILL.md` quando o projeto for governado;
5. `core/CHANGE_HYGIENE.md` + `skills/maintenance/SKILL.md` para código existente;
6. contratos Core conforme o problema;
7. para UI: `ui/UI_POLICY.md`, `ui/PROFESSIONAL_UI_PROFILE.md` e `ui/MOTION_POLICY.md`;
8. para HeroUI: `ui/heroui/README.md`, catálogos oficiais indexados e `ui/heroui/OVERLAY_INTERACTION_HARDENING.md` quando houver overlays/navegação.
