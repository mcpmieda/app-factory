# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Validar **Living UI / Semantic Motion** em uma interface real gerada pela Factory, provando no navegador que o padrão `ambient` é vivo, funcional, acessível e independente do design system.

## Estado

- fase: `V0.8 — validação executável de Living UI`;
- baseline oficial: `main` após merge da V0.7 (`f739111e450bd29d57fac9460e32f1c40d404966`);
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
- Issue #19: aberta e liberada para Codex;
- CI: valida Core/Skills/plugin, starter base, recipes SQLite, PostgreSQL/Auth em Postgres real efêmero e `asset-admin` desktop/mobile.

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
- projeto gerado pelo starter V0.7 registra `motionProfile: ambient` em `.app-factory.json`;
- motion não autoriza misturar design systems ou instalar biblioteca nova sem necessidade;
- Better Auth/Drizzle permanecem módulos condicionais do `web-admin`;
- SQLite é local/teste e PostgreSQL é caminho de produção validado;
- instalação limpa e CI reproduzível continuam gates.

## Trabalho atual

- bloco: Issue #19 — validar Living UI em interface real gerada;
- ambiente recomendado: Codex;
- motivo: exige app gerado, CSS/componentes reais, navegador, Playwright desktop/mobile e emulação de reduced motion;
- objetivo: comprovar as seis categorias semânticas e promover apenas primitives que reduzam trabalho futuro;
- regra: não instalar biblioteca de motion por checklist e não fazer merge automático.

## Próxima ação

Executar integralmente a Issue #19 no Codex. Ao concluir, devolver draft PR, CI e evidências para revisão do ChatGPT.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. Issue #19;
4. `ui/MOTION_POLICY.md`;
5. `ui/UI_POLICY.md`;
6. `skills/ui-builder/SKILL.md`;
7. `profiles/web-admin/PROFILE.md`.