# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Revisar a implementação da **V0.8 Living UI / Semantic Motion**, já comprovada em interface gerada, antes de decidir o merge.

## Estado

- fase: `V0.8 — implementada, aguardando revisão do draft PR`;
- baseline oficial: `main` no início da Issue #19 (`2730c2a2e8915abbebf5c3e00133b416f5229354`);
- V0.1 bootstrap: concluída;
- V0.2 pesquisa: concluída e integrada;
- V0.2.1 entry router: concluído e integrado;
- Issue #3 / Codex Plugin: concluída e revisada;
- V0.3 piloto web-admin: concluído, revisado e integrado;
- V0.4 perfil web-admin: concluído e integrado;
- V0.5 starter + segundo app: concluída, revisada e integrada;
- V0.6 hardening PostgreSQL/Auth: concluído, revisado e integrado;
- V0.7 Living UI / Semantic Motion: concluída, CI aprovada e integrada;
- perfil `web-admin`: `v1-rc`;
- Issues #4, #8, #10, #12 e #15: concluídas;
- Issue #19: implementação concluída na branch `codex/issue-19-living-ui-validation`, sem merge;
- `examples/living-ui-admin`: app Pulse Desk gerado pelo baseline V0.7 e validado em desktop/mobile/reduced motion;
- CI: mantém Core/Skills/plugin, starter/recipes/asset-admin e adiciona gate dedicado Living UI.

## Decisões vigentes

- Core permanece neutro e portátil;
- intenção de software ativa a Factory automaticamente;
- processo varia por escala XS/S/M/L;
- perfis validados são defaults condicionais, não dogmas;
- `web-admin` usa shadcn como base visual e ReUI seletivamente;
- HeroUI é alternativa visual legítima e pode ser exigido como sistema único;
- Living UI / Semantic Motion é transversal e independente do design system;
- Motion Profile default contextual: `ambient`;
- perfis: `none`, `subtle`, `ambient`, `expressive`;
- motion deve comunicar ambiente, interação, dados, estado, atenção ou navegação;
- `prefers-reduced-motion` é obrigatório para movimento não essencial;
- leitura longa, densidade, concentração e performance podem atenuar `ambient` para comportamento `subtle`;
- atenção deve parar/reduzir após cumprir a função;
- dados/gráficos só devem reanimar quando houver mudança real;
- `AmbientSurface` e `AttentionPulse` são os únicos primitives promovidos pela V0.8;
- motion de dado específico do produto não deve virar abstração genérica sem contrato de mudança real;
- projeto gerado pelo starter V0.7 registra `motionProfile: ambient` em `.app-factory.json`;
- motion não autoriza misturar design systems ou instalar biblioteca nova sem necessidade;
- Better Auth/Drizzle permanecem módulos condicionais do `web-admin`;
- SQLite é local/teste e PostgreSQL é caminho de produção validado;
- instalação limpa e CI reproduzível continuam gates.

## Trabalho atual

- bloco concluído: Issue #19 — validar Living UI em interface real gerada;
- evidência: `research/V0.8_LIVING_UI_VALIDATION.md` e três screenshots úteis;
- checks locais: instalação limpa, format, lint, typecheck, testes, build, audit, Playwright desktop/mobile/reduced motion e inspeção visual;
- promoção: dois wrappers pequenos + tokens/reduced-motion no starter;
- regra vigente: revisar o draft PR e CI; não fazer merge automático.

## Próxima ação

Revisar o draft PR da Issue #19, os checks remotos e as evidências; merge permanece decisão humana separada.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. o draft PR da Issue #19;
4. `research/V0.8_LIVING_UI_VALIDATION.md`;
5. `examples/living-ui-admin/`;
6. `ui/MOTION_POLICY.md`;
7. `profiles/web-admin/PROFILE.md`.
