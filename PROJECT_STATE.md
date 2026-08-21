# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Manter a **App Factory V1.0 estável** como baseline recuperável para criação e evolução de software por agentes, preservando validação executável, continuidade via GitHub e perfis condicionais.

## Estado

- fase: `V1.0 — estável`;
- versão: `1.0.0`;
- baseline de release: `main` após a auditoria final V1.0;
- V0.1 a V0.9: concluídas, revisadas e integradas;
- Issue #25 / auditoria final V1.0: concluída e aprovada;
- perfil `web-admin`: `v1`;
- perfis `website`, `web-app`, `chrome-extension` e `automation`: `validated`;
- plugin Codex: `1.0.0`, com bootstrap isolado e 11 Skills verificadas sem duplicação;
- CI: Core/Skills/plugin, web-admin starter/recipes, PostgreSQL/Auth real, asset-admin, Living UI, quatro pilotos universais e gate V1 final.

## Decisões vigentes

- intenção de software ativa a Factory automaticamente;
- AI serve ao objetivo, não ao texto literal do prompt;
- reuse-first e maior fatia segura são regras centrais;
- perfis são defaults condicionais, não stacks universais;
- stack `web-admin` não contamina outros tipos por reflexo;
- Living UI / Semantic Motion é transversal quando existe UI;
- Motion Profile default contextual: `ambient`;
- `prefers-reduced-motion` é obrigatório para movimento não essencial;
- `web-admin` tem caminho validado Better Auth + Drizzle + PostgreSQL quando necessário;
- website, web-app, Chrome extension e automation possuem contratos validados próprios;
- instalação limpa, testes executáveis, CI reproduzível, recuperação e continuidade via GitHub são gates permanentes;
- refinamentos não bloqueantes e novos perfis ficam para versões posteriores.

## Evidência da V1.0

- `research/V1.0_FINAL_AUDIT.md`;
- `audits/v1-final/equipment-loans/`;
- `research/evidence/V1_CONTINUITY_HANDOFF.md`;
- `research/evidence/V1_CONTROLLED_RECOVERY.md`;
- `.github/workflows/validate-v1-release.yml`;
- `scripts/validate_v1_bootstrap.py` e `scripts/validate_v1_release.py`.

A auditoria final comprovou bootstrap isolado do plugin, roteamento a partir de linguagem comum, criação de projeto novo, persistência e regra de negócio, browser desktop/mobile, reduced motion, continuidade por segundo agente sem contexto e detecção/recuperação de regressão controlada.

## Próxima ação

Usar V1.0 como baseline estável. Novos trabalhos devem nascer de necessidade real de produto ou manutenção; não criar nova fase apenas para refinamento cosmético ou expansão nominal de cobertura.

Escopos ainda não validados — como mobile nativo, desktop nativo, jogos e cloud complexa — devem receber piloto/evidência próprios antes de virarem perfis estáveis.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. `core/ENTRYPOINT.md`;
4. `skills/factory-router/SKILL.md`;
5. `profiles/README.md`;
6. o perfil indicado pelo produto;
7. `ui/UI_POLICY.md` e `ui/MOTION_POLICY.md` quando houver interface;
8. `research/V1.0_FINAL_AUDIT.md` quando precisar auditar a origem da release.
