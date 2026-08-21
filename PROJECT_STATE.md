# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Formalizar e validar a política universal **Living UI / Semantic Motion**, independente de HeroUI, shadcn, ReUI ou outro design system, após a promoção do perfil `web-admin` para `v1-rc`.

## Estado

- fase: `V0.7 — Living UI / Semantic Motion`;
- baseline oficial anterior: `main` após merge do PR #14 (`3d81d6aa0d0d8a36ff070e5bd5d09b276aa6ae5f`);
- V0.1 bootstrap: concluída;
- V0.2 pesquisa: concluída e integrada;
- V0.2.1 entry router: concluído e integrado;
- Issue #3 / Codex Plugin: concluída e revisada;
- V0.3 piloto web-admin: concluído, revisado e integrado;
- V0.4 perfil web-admin: concluído e integrado;
- V0.5 starter + segundo app: concluída, revisada e integrada;
- V0.6 hardening PostgreSQL/Auth: concluído, revisado e integrado;
- perfil `web-admin`: `v1-rc`;
- Issues #4, #8, #10 e #12: concluídas;
- Issue #15: Living UI / Semantic Motion em implementação/revisão;
- CI: valida Core/Skills/plugin, starter base, recipes SQLite diretos, PostgreSQL/Auth em banco real efêmero e exemplo `asset-admin`.

## Decisões vigentes

- Core permanece neutro e portátil;
- Codex usa adaptador/plugin fino sem duplicar Skills;
- intenção de software ativa a Factory automaticamente;
- processo varia por escala XS/S/M/L;
- Factory pode selecionar perfil validado em `profiles/` após entender o produto;
- perfil não é dogma e módulos opcionais só entram quando necessários;
- no perfil `web-admin`, shadcn é a base visual e ReUI é seletivo;
- HeroUI continua alternativa visual legítima e pode ser exigido pelo usuário como sistema único;
- Living UI / Semantic Motion é transversal e independente do design system;
- Motion Profile default contextual: `ambient`;
- perfis disponíveis: `none`, `subtle`, `ambient`, `expressive`;
- motion deve comunicar ambiente, interação, dados, estado, atenção ou navegação; animação sem função deve ser removida;
- `prefers-reduced-motion` é obrigatório para movimento não essencial;
- telas densas, leitura longa, concentração ou performance limitada atenuam `ambient` para comportamento `subtle` quando necessário;
- ações importantes podem usar atenção temporária, mas o movimento deve parar/reduzir após cumprir a função;
- gráficos podem animar mudanças reais e não devem reanimar sem alteração de dado;
- Better Auth é primeira opção condicional de auth no `web-admin`;
- Drizzle é primeira opção condicional de persistência;
- SQLite/better-sqlite3 permanece provider local/teste;
- PostgreSQL é caminho de produção validado por recipe/CI para `web-admin`;
- migrations destrutivas não devem ser aplicadas automaticamente sem análise;
- instalação limpa, recipes gerados e CI reproduzível são gates de qualidade.

## Trabalho atual

- bloco: Issue #15 — Living UI / Semantic Motion universal;
- ambiente: ChatGPT + GitHub;
- motivo: esta fase formaliza regras/contratos e templates; não exige ainda execução local pesada;
- implementação: `ui/MOTION_POLICY.md`, `ui/UI_POLICY.md`, `ui-builder`, templates e perfil `web-admin`;
- regra: motion não impõe biblioteca nova nem mistura design systems.

## Próxima ação

Validar CI da V0.7 e integrar a política. Em fase executável posterior, provar o Motion Profile em UI real gerada, incluindo reduced motion, desktop/mobile, atenção temporária e dados/estados quando aplicáveis.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. `ui/MOTION_POLICY.md`;
4. `ui/UI_POLICY.md`;
5. `skills/ui-builder/SKILL.md`;
6. `profiles/web-admin/PROFILE.md`;
7. Issue #15.