# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Manter a **App Factory V1.1 estável** como baseline recuperável e mais autônomo para criação/evolução de software, reduzindo releitura de repositórios, handoffs manuais e dependência de um executor específico sem reduzir verificabilidade.

## Estado

- fase: `V1.1 — estável`;
- versão: `1.1.0`;
- baseline anterior preservada: tag/release `v1.0.0`;
- Issue #32 / Autonomous Context Engine: concluída na release V1.1;
- Context Engine: incremental, stdlib, SHA-256, delta `added/changed/removed`, mapa de stack/símbolos/imports e exclusão de segredos/build/dependencies/binários;
- Autonomy Engine: `init/status/next/resume/record`, fases explícitas, repair loop default 3 e intervenção humana categorizada;
- execução: current-agent + GitHub/CI primeiro; Codex/local passa a ser fallback de capacidade real, não regra automática;
- perfil `web-admin`: `v1`;
- perfis `website`, `web-app`, `chrome-extension` e `automation`: `validated`;
- plugin Codex: `1.1.0`, com 13 Skills verificadas sem duplicação;
- CI: gates V1.0 preservados + `Validate V1.1 Autonomous Context` + composição V1 release line.

## Decisões vigentes

- intenção de software ativa a Factory automaticamente;
- AI serve ao objetivo, não ao texto literal do prompt;
- `resume`/Context Engine devem recuperar contexto antes de reconstruir estado a partir de conversa;
- `.factory/context/` é cache regenerável e não fonte de verdade;
- `.factory/state.json` é estado compacto de continuidade e pode ser versionado em handoffs importantes;
- o agente calcula e executa o próximo passo técnico; não pede ao usuário para conduzir fases rotineiras;
- falha técnica entra em reparo limitado; ao estagnar, mudar estratégia/executor antes de envolver o usuário;
- intervenção humana é reservada a produto/regra de negócio, preferência subjetiva, custo, risco alto, credencial/dado indisponível e decisão legal/organizacional;
- current-agent + GitHub/CI deve ser tentado antes de Codex quando fornecer prova suficiente;
- Codex/local continua correto quando browser/runtime/debug/migration interativos ou outra capacidade local forem realmente necessários;
- reuse-first e maior fatia segura continuam regras centrais;
- perfis são defaults condicionais, não stacks universais;
- stack `web-admin` não contamina outros tipos por reflexo;
- Living UI / Semantic Motion é transversal quando existe UI;
- Motion Profile default contextual: `ambient`;
- `prefers-reduced-motion` é obrigatório para movimento não essencial;
- instalação limpa, testes executáveis, CI reproduzível, recuperação e continuidade via GitHub são gates permanentes.

## Evidência V1.1

- `research/V1.1_AUTONOMOUS_CONTEXT_VALIDATION.md`;
- `engine/context_engine.py`;
- `engine/autonomy_engine.py`;
- `scripts/factory.py`;
- `scripts/validate_v1_1.py`;
- `tests/v1_1/`;
- `.github/workflows/validate-v1-1-autonomy.yml`;
- `.github/workflows/validate-v1-release.yml`.

O gate dedicado comprovou 13 Skills estruturalmente válidas, máquina de estados, repair loop limitado, retomada sem histórico, detecção de mudança externa e cache incremental. No repositório real, a segunda passagem reaproveitou os metadados dos 504 arquivos mapeados e reprocessou 0 arquivos.

## Evidência V1.0 preservada

- `research/V1.0_FINAL_AUDIT.md`;
- `audits/v1-final/equipment-loans/`;
- `research/evidence/V1_CONTINUITY_HANDOFF.md`;
- `research/evidence/V1_CONTROLLED_RECOVERY.md`;
- `scripts/validate_v1_bootstrap.py` e `scripts/validate_v1_release.py`.

## Próxima ação

Usar V1.1 como baseline corrente. Em projeto existente, começar por `resume`; deixar a Factory recuperar contexto, calcular a próxima ação e continuar até conclusão/bloqueio real.

Escopos ainda não validados — como mobile nativo, desktop nativo, jogos e cloud complexa — continuam exigindo piloto/evidência próprios antes de virarem perfis estáveis.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. `python scripts/factory.py --root <projeto> resume` quando o runtime estiver disponível no projeto/checkout;
3. este `PROJECT_STATE.md` quando estiver modificando a própria Factory;
4. `core/ENTRYPOINT.md`;
5. `core/CONTEXT_ENGINE.md` e `core/AUTONOMY_ENGINE.md`;
6. `skills/factory-router/SKILL.md`;
7. o perfil indicado pelo produto;
8. `ui/UI_POLICY.md` e `ui/MOTION_POLICY.md` quando houver interface.
