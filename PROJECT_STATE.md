# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Concluir a validação **universal** fora do perfil `web-admin` e entregar evidência revisável para a auditoria final V1.0.

## Estado

- fase: `V0.9 — validação universal dos principais tipos de projeto`;
- baseline oficial: `main` após merge da V0.8 (`2fb28bbd4a8d3cde338f52f6521415d17f2a3581`);
- base efetiva da branch após fast-forward de `main`: `5eb720941ff0f5ff5f682502c222652ce95a244c`;
- V0.1 bootstrap: concluída;
- V0.2 pesquisa: concluída e integrada;
- V0.2.1 entry router: concluído e integrado;
- Issue #3 / Codex Plugin: concluída e revisada;
- V0.3 piloto web-admin: concluído, revisado e integrado;
- V0.4 perfil web-admin: concluído e integrado;
- V0.5 starter + segundo app: concluída, revisada e integrada;
- V0.6 hardening PostgreSQL/Auth: concluído, revisado e integrado;
- V0.7 Living UI / Semantic Motion: concluída e integrada;
- V0.8 Living UI executável: concluída, revisada e integrada;
- perfil `web-admin`: `v1-rc`;
- Issues #4, #8, #10, #12, #15 e #19: concluídas;
- Issue #22: implementada na branch `pilot/universal-validation-v0.9`, aguardando revisão/CI do draft PR;
- perfis `website`, `web-app`, `chrome-extension` e `automation`: `validated`;
- CI atual: gates anteriores preservados e quatro jobs universais independentes adicionados.

## Decisões vigentes

- Core permanece neutro e portátil;
- intenção de software ativa a Factory automaticamente;
- processo varia por escala XS/S/M/L;
- AI serve ao objetivo, não ao texto literal do prompt;
- reuse-first: pesquisar/reusar solução madura quando isso reduzir trabalho e risco;
- perfis validados são defaults condicionais, não dogmas;
- stack do `web-admin` não deve contaminar automaticamente outros tipos de projeto;
- `web-admin` usa shadcn como base visual e ReUI seletivamente;
- HeroUI é alternativa visual legítima e pode ser exigido como sistema único;
- Living UI / Semantic Motion é transversal e independente do design system;
- Motion Profile default contextual: `ambient`;
- perfis de motion: `none`, `subtle`, `ambient`, `expressive`;
- `prefers-reduced-motion` é obrigatório para movimento não essencial;
- atenção deve parar/reduzir após cumprir sua função;
- dados/gráficos só devem reanimar quando houver mudança real;
- `AmbientSurface` e `AttentionPulse` são primitives opt-in comprovados;
- Better Auth/Drizzle permanecem módulos condicionais do `web-admin`;
- SQLite é local/teste e PostgreSQL é caminho de produção validado para `web-admin`;
- instalação limpa, testes executáveis, CI reproduzível e continuidade via GitHub permanecem gates.

## Trabalho atual

- bloco: Issue #22 — V0.9 validação universal concluída localmente;
- pilotos: `examples/website-pilot`, `web-app-pilot`, `chrome-extension-pilot`, `automation-pilot`;
- evidência: `research/V0.9_UNIVERSAL_VALIDATION.md` e screenshots V0.9;
- continuidade: website e automation recuperados por agentes isolados sem contexto;
- status final condicionado a checks verdes do draft PR;
- nenhum merge automático.

## Próxima ação

Revisar o draft PR da Issue #22 e aguardar todos os checks. Sem bloqueador objetivo após CI, iniciar diretamente **V1.0 — auditoria final end-to-end em ambiente limpo**, sem fase intermediária de refinamento.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. `research/V0.9_UNIVERSAL_VALIDATION.md` e draft PR da Issue #22;
4. `core/ENTRYPOINT.md`;
5. `skills/factory-router/SKILL.md`;
6. `skills/app-planner/SKILL.md`;
7. `skills/tool-router/SKILL.md`;
8. `ui/UI_POLICY.md` e `ui/MOTION_POLICY.md`;
9. `profiles/README.md` e `profiles/web-admin/PROFILE.md`;
10. o `PROJECT_STATE.md` do piloto relevante.
