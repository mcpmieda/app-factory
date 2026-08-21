# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Manter a **App Factory V1.3 estável** como baseline recuperável, autônomo e adaptativo para criação/evolução de software: recuperar contexto, calcular a próxima ação, escolher executor por capacidade e usar aprendizado técnico local somente quando houver evidência suficiente, sem reduzir segurança ou verificabilidade.

## Estado

- fase: `V1.3 — estável`;
- versão: `1.3.0`;
- baseline publicada anterior preservada: tag/release `v1.0.0`;
- V1.1 / Issue #32: Context Engine + Autonomy Engine concluídos;
- V1.2 / Issue #36: Execution Fabric + CI Executor concluídos;
- V1.3 / Issue #38: Learning Engine implementado para a release V1.3;
- Context Engine: incremental, stdlib, SHA-256, delta `added/changed/removed`, stack/símbolos/imports/dependências locais e exclusão de segredos/build/dependencies/binários;
- Autonomy Engine: `init/status/next/resume/record`, transições explícitas, repair loop default 3 e intervenção humana categorizada;
- Execution Fabric: roteamento por capacidades, backends `current_agent/github_ci/sandbox/local_full`, fallback escopado pela tarefa atual e histórico operacional bounded;
- CI Executor: gates declarados/allowlisted, sem comandos de prompt, `shell=False`, sem secrets por padrão e instalação reproduzível somente com lockfile compatível;
- Learning Engine: **local-only**, bounded, sem telemetria externa, metadados técnicos allowlisted, amostra mínima/prior conservador e explicação `baseline/learned/insufficient-data`;
- aprendizado: incapacidade, indisponibilidade, failure threshold, risco e Definition of Done sempre vencem score histórico;
- velocidade aprendida: usa duração mediana de execuções bem-sucedidas; falha rápida não melhora preferência;
- `local_full`: não pode ser promovido sobre backend leve capaz somente por aprendizado;
- perfil `web-admin`: `v1`;
- perfis `website`, `web-app`, `chrome-extension` e `automation`: `validated`;
- plugin Codex: `1.3.0`, com 15 Skills portáteis;
- CI: gates V1 anteriores preservados + `Validate V1.3 Learning Engine`.

## Decisões vigentes

- intenção de software ativa a Factory automaticamente;
- AI serve ao objetivo, não ao texto literal do prompt;
- GitHub é a fonte técnica de verdade; conversa não é a autoridade operacional;
- `resume`/Context Engine recuperam contexto antes de depender de memória de conversa;
- `.factory/context/` é cache regenerável, não fonte de verdade;
- `.factory/state.json` mantém continuidade do Autonomy Engine e pode ser versionado em handoffs importantes;
- `.factory/execution.json` mantém histórico bounded local de tentativas e fica fora do Git por padrão;
- `.factory/learning.json` mantém aprendizado local allowlisted e fica fora do Git por padrão;
- ausência do arquivo de learning em outra máquina não bloqueia continuidade: a Factory usa o baseline seguro V1.2 e reaprende;
- o agente calcula próxima ação e executor; o usuário não conduz fases técnicas rotineiras;
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

## Evidência V1.3

- `core/LEARNING_ENGINE.md`;
- `engine/learning_engine.py`;
- integração em `engine/execution_engine.py` e `scripts/factory.py`;
- `skills/learning-engine/SKILL.md`;
- `scripts/validate_v1_3.py`;
- `tests/v1_3/`;
- `.github/workflows/validate-v1-3-learning.yml`;
- `research/V1.3_LEARNING_ENGINE_VALIDATION.md`.

A validação V1.3 cobre privacidade do schema, sanitização de arquivo local adulterado, dataset bounded, amostra mínima, prior conservador, escolha aprendida apenas entre backends elegíveis, incapacidade acima de score, proteção de `local_full`, failure threshold da tarefa atual, isolamento entre tarefas, duração somente de execuções bem-sucedidas, persistência entre sessões e integração CLI.

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

Usar V1.3 como baseline corrente. Em projeto existente, começar por `resume`; deixar Context/Autonomy recuperar o estado, Execution Fabric filtrar executores, Learning Engine influenciar somente quando houver evidência confiável e CI provar o resultado.

Escopos ainda não validados — como mobile nativo, desktop nativo, jogos e cloud complexa — continuam exigindo piloto/evidência próprios antes de virarem perfis estáveis.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. `python scripts/factory.py --root <projeto> resume` quando o runtime estiver disponível;
3. este `PROJECT_STATE.md` quando estiver modificando a própria Factory;
4. `core/ENTRYPOINT.md`;
5. `core/CONTEXT_ENGINE.md`, `core/AUTONOMY_ENGINE.md`, `core/EXECUTION_FABRIC.md` e `core/LEARNING_ENGINE.md`;
6. `skills/factory-router/SKILL.md`, `skills/execution-router/SKILL.md` e `skills/learning-engine/SKILL.md`;
7. o perfil indicado pelo produto;
8. `ui/UI_POLICY.md` e `ui/MOTION_POLICY.md` quando houver interface.
