# PROJECT_STATE

> Estado vigente da App Factory. Não usar como diário.

## Objetivo atual

Endurecer o perfil `web-admin` antes da V1, provando recipes diretamente em geração limpa, adicionando um caminho PostgreSQL de produção e formalizando manutenção segura de Better Auth/schema.

## Estado

- fase: `V0.6 — hardening pré-V1 do perfil web-admin`;
- baseline oficial: `main` após merge do PR #11 (`7339a25f401813f6c05778e3f30228f518914a95`);
- V0.1 bootstrap: concluída;
- V0.2 pesquisa: concluída e integrada;
- V0.2.1 entry router: concluído e integrado;
- Issue #3 / Codex Plugin: concluída e revisada;
- V0.3 piloto web-admin: concluído, revisado, CI reproduzível e integrado;
- V0.4 perfil web-admin: concluído e integrado;
- V0.5 starter + segundo app: concluída, revisada e integrada;
- Issues #4, #8 e #10: concluídas;
- Issue #12: aberta e liberada para Codex;
- CI: valida Core/Skills/plugin, piloto V0.3, starter V0.5 e exemplo `asset-admin` em checkout limpo.

## Decisões vigentes

- Core permanece neutro e portátil;
- Codex usa adaptador/plugin fino sem duplicar Skills;
- intenção de software ativa a Factory automaticamente;
- processo varia por escala XS/S/M/L;
- Factory pode selecionar perfil validado em `profiles/` após entender o produto;
- perfil não é dogma e módulos opcionais só entram quando necessários;
- no perfil `web-admin`, shadcn é a base visual;
- ReUI é opcional/seletivo por componente avançado;
- Better Auth é primeira opção condicional quando o projeto exige autenticação própria;
- Drizzle é primeira opção condicional quando o projeto exige persistência própria;
- SQLite/better-sqlite3 permanece provider local/teste, não default universal de produção;
- V0.6 deve validar PostgreSQL como caminho de produção sem contaminar o starter base;
- Zod, Vitest, Playwright e lint oficial do Next fazem parte da base validada do perfil;
- Biome permanece opcional/complementar;
- starters permanecem componíveis, sem serviços opcionais impostos;
- instalação limpa, recipes gerados e CI reproduzível são gates de qualidade;
- migrations destrutivas não devem ser aplicadas automaticamente sem análise.

## Trabalho atual

- bloco: Issue #12 — hardening pré-V1 do perfil `web-admin`;
- ambiente recomendado: Codex;
- motivo: exige geração real de projetos, recipes, PostgreSQL, migrations, auth, CI, build e smoke de produção;
- objetivo imediato: transformar `web-admin` em candidato `v1-rc` sem expandir ainda para outros perfis;
- regra: abrir draft PR e não fazer merge automático.

## Próxima ação

Executar integralmente a Issue #12 no Codex. Ao concluir, devolver o draft PR e os checks para revisão do ChatGPT.

## Handoff

Outro agente deve começar por:

1. `AGENTS.md`;
2. este `PROJECT_STATE.md`;
3. Issue #12;
4. `profiles/web-admin/PROFILE.md`;
5. `starters/web-admin/README.md`;
6. `research/V0.5_WEB_ADMIN_STARTER_VALIDATION.md`;
7. `.github/workflows/validate-web-admin-starter.yml`.
