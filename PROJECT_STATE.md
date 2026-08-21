# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Manter a **App Factory V1.2 estável** como baseline recuperável e autônomo para criação/evolução de software, escolhendo o executor por capacidade e usando o agente atual + GitHub/CI antes de qualquer executor local completo sempre que essa rota conseguir provar o trabalho.

## Estado

- fase: `V1.2 — estável`;
- versão: `1.2.0`;
- baseline publicada anterior preservada: tag/release `v1.0.0`;
- V1.1 / Issue #32: Context Engine + Autonomy Engine concluídos;
- V1.2 / Issue #36: Execution Fabric concluída;
- Context Engine: incremental, stdlib, SHA-256, delta `added/changed/removed`, stack/símbolos/imports/dependências locais e exclusão de segredos/build/dependencies/binários;
- Autonomy Engine: `init/status/next/resume/record`, transições explícitas, repair loop default 3 e intervenção humana categorizada;
- Execution Fabric: roteamento por capacidades, backend atual/CI/sandbox/local, histórico bounded de tentativas e fallback previsível;
- CI Executor: gates declarados/allowlisted, sem comandos de prompt, `shell=False`, sem secrets por padrão;
- execução: `current_agent → github_ci → sandbox → local_full`, respeitando capacidades e disponibilidade reais;
- perfil `web-admin`: `v1`;
- perfis `website`, `web-app`, `chrome-extension` e `automation`: `validated`;
- plugin Codex: `1.2.0`, com 14 Skills verificadas sem duplicação;
- CI: gates V1 anteriores preservados + `Validate V1.2 Execution Fabric`.

## Decisões vigentes

- intenção de software ativa a Factory automaticamente;
- AI serve ao objetivo, não ao texto literal do prompt;
- `resume`/Context Engine recuperam contexto antes de depender de memória de conversa;
- `.factory/context/` é cache regenerável, não fonte de verdade;
- `.factory/state.json` mantém continuidade do Autonomy Engine;
- `.factory/execution.json` mantém histórico bounded de execução, sem logs brutos;
- o agente calcula a próxima ação e o backend; o usuário não conduz fases técnicas rotineiras;
- backend é escolhido por capacidade, não por marca;
- `current_agent` é preferido quando consegue implementar/revisar diretamente;
- `github_ci` é executor real para comandos determinísticos, build, testes, headless browser e serviços efêmeros;
- `sandbox`/`local_full` só entram quando declarados disponíveis e necessários;
- Codex é um possível `local_full`, não dependência arquitetural;
- prompts nunca viram shell diretamente;
- eventos fora de fase são rejeitados antes de alterar estado;
- falha técnica entra em repair/fallback limitado; não vira pergunta ao usuário por reflexo;
- intervenção humana continua reservada a produto/regra de negócio, preferência subjetiva, custo, risco alto, credencial/dado indisponível e decisão legal/organizacional;
- reuse-first, baseline/diff/rollback, instalação limpa, testes executáveis e CI reproduzível continuam gates permanentes;
- Living UI / Semantic Motion permanece transversal quando existe UI, com `ambient` contextual e `prefers-reduced-motion` obrigatório.

## Evidência V1.2

- `core/EXECUTION_FABRIC.md`;
- `engine/execution_engine.py`;
- `engine/ci_executor.py`;
- `skills/execution-router/SKILL.md`;
- `scripts/factory.py`;
- `scripts/validate_v1_2.py`;
- `tests/v1_2/`;
- `.github/workflows/validate-v1-2-execution.yml`.

A validação V1.2 comprova current-agent para planejamento/implementação quando suficiente, GitHub CI para verificação determinística/headless, recusa de backend incapaz, ausência de backend local implícito, fallback após falhas repetidas e descoberta de gates sem executar strings arbitrárias vindas de prompt.

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

Usar V1.2 como baseline corrente e implementar o Learning Engine em evolução separada, para que aprendizado use dados gerados pela Execution Fabric sem alterar regras de segurança/capacidade.

Escopos ainda não validados — como mobile nativo, desktop nativo, jogos e cloud complexa — continuam exigindo piloto/evidência próprios antes de virarem perfis estáveis.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. `python scripts/factory.py --root <projeto> resume` quando o runtime estiver disponível;
3. este `PROJECT_STATE.md` quando estiver modificando a própria Factory;
4. `core/ENTRYPOINT.md`;
5. `core/CONTEXT_ENGINE.md`, `core/AUTONOMY_ENGINE.md` e `core/EXECUTION_FABRIC.md`;
6. `skills/factory-router/SKILL.md` e `skills/execution-router/SKILL.md`;
7. o perfil indicado pelo produto;
8. `ui/UI_POLICY.md` e `ui/MOTION_POLICY.md` quando houver interface.
