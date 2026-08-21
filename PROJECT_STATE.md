# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Validar a App Factory de forma **universal** fora do perfil `web-admin`, usando quatro famílias representativas (`website`, `web-app`, `chrome-extension`, `automation`) antes da auditoria final V1.0.

## Estado

- fase: `V0.9 — validação universal dos principais tipos de projeto`;
- baseline oficial: `main` após merge da V0.8 (`2fb28bbd4a8d3cde338f52f6521415d17f2a3581`);
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
- Issue #22: aberta e liberada para Codex;
- CI atual: Core/Skills/plugin, web-admin starter e recipes, PostgreSQL/Auth real, asset-admin e Living UI desktop/mobile/reduced-motion.

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

- bloco: Issue #22 — V0.9 validação universal;
- ambiente recomendado: Codex;
- pilotos exigidos: website, web-app, Chrome extension MV3 e automation local;
- objetivo: provar classificação, escolha de stack, reuse-first, implementação, teste e handoff fora do `web-admin`;
- regra: construir a menor fatia funcional completa por tipo, não quatro produtos grandes;
- perfis novos só devem ser promovidos após evidência do piloto;
- nenhum merge automático.

## Próxima ação

Executar integralmente a Issue #22 no Codex. Ao concluir, devolver draft PR, CI, evidências e relatório `research/V0.9_UNIVERSAL_VALIDATION.md` para revisão do ChatGPT.

Se a V0.9 terminar sem bloqueador objetivo, a próxima fase deve ser diretamente **V1.0 — auditoria final end-to-end em ambiente limpo**, sem criar novas fases intermediárias apenas por refinamento.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. Issue #22;
4. `core/ENTRYPOINT.md`;
5. `skills/factory-router/SKILL.md`;
6. `skills/app-planner/SKILL.md`;
7. `skills/tool-router/SKILL.md`;
8. `ui/UI_POLICY.md` e `ui/MOTION_POLICY.md`;
9. `profiles/README.md` e `profiles/web-admin/PROFILE.md`;
10. `research/V0.8_LIVING_UI_VALIDATION.md`.
